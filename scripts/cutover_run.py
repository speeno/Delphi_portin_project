"""C15 운영 cut-over 자동화 스크립트 (Phase 2 — T6).

목적
----
P1~P6 운영 절차 (cutover.yaml §scope.procedure) 를 안전하게 자동/반자동 실행.
실 DB 적재(P2/P3) 와 DNS/proxy 스위치(P6) 는 외부 의존 — 본 스크립트는 *오케스트레이션*
역할만 수행: 사전 게이트 → validator (P4) → 리포트 → 실패 시 rollback 시뮬레이션.

설계 원칙 (DEC-040/044/042/041 정합)
------------------------------------
- 외부 SaaS 호출 ❌ (DEC-044) — 본 스크립트는 stdlib + scripts/cutover_validator 만 사용.
- 신규 비즈니스 SQL 0건 — validator/adapters 가 시스템 쿼리만 수행.
- ``--confirm`` 플래그 없이는 P6 (운영 전환) 단계 *진입 금지*.
- OQ 차단 게이트(``cutover_block: true``) 미해소 시 즉시 종료 (rc=3).
- 실패/롤백은 동일 리포트 JSON 에 ``rollback_started_at`` / ``rollback_elapsed_sec`` 기록.

CLI
---
```bash
$ python3 scripts/cutover_run.py --legacy 138_legacy --modern 138_modern --dryrun
$ python3 scripts/cutover_run.py --legacy 138_legacy --modern 138_modern --confirm
$ python3 scripts/cutover_run.py --dryrun --out reports/run_138.json
```
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "migration" / "contracts" / "cutover.yaml"

# 프로젝트 루트를 sys.path 에 두어 scripts.cutover_validator 임포트 안정화.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cutover_validator import (  # noqa: E402  (import after sys.path setup)
    ValidationReport,
    _dryrun_sources,
    _resolve_tables,
    _build_live_source,
    run_checks,
)


# ───────────────────────────────────────────────────────────────────
# 모델
# ───────────────────────────────────────────────────────────────────
@dataclass
class StepRecord:
    id: str
    name: str
    started_at: float
    finished_at: float | None = None
    ok: bool | None = None
    note: str = ""

    def finish(self, *, ok: bool, note: str = "") -> None:
        self.finished_at = time.time()
        self.ok = ok
        self.note = note

    @property
    def elapsed_sec(self) -> float | None:
        if self.finished_at is None:
            return None
        return round(self.finished_at - self.started_at, 3)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "elapsed_sec": self.elapsed_sec,
            "ok": self.ok,
            "note": self.note,
        }


@dataclass
class RunReport:
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    mode: str = "dryrun"            # "dryrun" | "live"
    confirmed: bool = False         # --confirm
    legacy: str = ""
    modern: str = ""
    steps: list[StepRecord] = field(default_factory=list)
    validator: dict[str, Any] | None = None
    rollback_started_at: float | None = None
    rollback_elapsed_sec: float | None = None
    blocked_by: list[str] = field(default_factory=list)
    success: bool = False

    def add_step(self, step_id: str, name: str) -> StepRecord:
        s = StepRecord(id=step_id, name=name, started_at=time.time())
        self.steps.append(s)
        return s

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "elapsed_sec": (
                round(self.finished_at - self.started_at, 3)
                if self.finished_at else None
            ),
            "mode": self.mode,
            "confirmed": self.confirmed,
            "legacy": self.legacy,
            "modern": self.modern,
            "blocked_by": self.blocked_by,
            "steps": [s.to_dict() for s in self.steps],
            "validator": self.validator,
            "rollback_started_at": self.rollback_started_at,
            "rollback_elapsed_sec": self.rollback_elapsed_sec,
            "success": self.success,
        }


# ───────────────────────────────────────────────────────────────────
# OQ 차단 게이트 (정적 — cutover.yaml 파싱)
# ───────────────────────────────────────────────────────────────────
def find_blocking_open_questions() -> list[str]:
    """cutover.yaml 의 ``cutover_block: true`` OQ 가 미해소이면 모두 반환.

    cutover.yaml 은 일부 섹션이 yaml-strict 가 아니어서 (procedure 시퀀스 + 동일
    들여쓰기의 매핑 키), 본 함수는 ``open_questions_handling`` 블록 내부만
    line-by-line 으로 파싱한다 — 다른 섹션의 동일 키워드 오탐을 방지.
    """
    text = CONTRACT.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_section = False
    section_indent: int | None = None
    out: list[str] = []
    current_id: str | None = None
    current_block: bool | None = None
    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("open_questions_handling:"):
            in_section = True
            section_indent = len(raw) - len(raw.lstrip())
            continue
        if not in_section:
            continue
        # 섹션 종료 — 들여쓰기가 ``open_questions_handling:`` 키와 동일 이하 인
        # 새 키 (예: ``acceptance_criteria:`` 또는 최상위 ``decisions:``).
        # 들여쓰기가 더 깊은 줄(자식 매핑/시퀀스)은 절대 boundary 가 아님.
        if stripped and not stripped.startswith("#") and not stripped.startswith("- "):
            indent = len(raw) - len(raw.lstrip())
            if section_indent is not None and indent <= section_indent and ":" in stripped:
                break
        # 각 OQ 항목 시작
        m_id = re.match(r"-\s*id:\s*([A-Z0-9\-]+)", stripped)
        if m_id:
            if current_id and current_block:
                out.append(current_id)
            current_id = m_id.group(1)
            current_block = None
            continue
        m_blk = re.match(r"cutover_block:\s*(true|false)", stripped)
        if m_blk and current_id:
            current_block = m_blk.group(1).strip().lower() == "true"
    if current_id and current_block:
        out.append(current_id)
    return out


# ───────────────────────────────────────────────────────────────────
# 실행 단계
# ───────────────────────────────────────────────────────────────────
def _exec_p1_lock(report: RunReport) -> bool:
    s = report.add_step("P1", "운영 lock (read-only 모드 전환)")
    if report.mode == "dryrun":
        s.finish(ok=True, note="dryrun — 실제 read-only 전환 생략")
        return True
    s.finish(
        ok=True,
        note="DBA 수기 절차 — 본 스크립트는 안내만 제공 (외부 명령 호출 없음)",
    )
    return True


def _exec_p2_dump(report: RunReport) -> bool:
    s = report.add_step("P2", "mysqldump (per server) + checksum 산출")
    s.finish(
        ok=True,
        note=(
            "본 스크립트는 mysqldump/import 를 직접 실행하지 않는다 — "
            "운영 절차에 따라 수기 실행 후 본 단계는 PASS 표식만 기록"
        ),
    )
    return True


def _exec_p3_import(report: RunReport) -> bool:
    s = report.add_step("P3", "신규 환경 import + 스키마 어댑터 검증")
    s.finish(ok=True, note="외부 절차 — PASS 표식만 기록")
    return True


def _exec_p4_validator(
    report: RunReport, *, legacy_id: str | None, modern_id: str | None,
    profiles: str | None, tables_arg: list[str] | None,
) -> tuple[bool, ValidationReport]:
    s = report.add_step("P4", "cutover_validator 5종 (VC-1~5)")
    if report.mode == "dryrun":
        legacy, modern, tables = _dryrun_sources()
    else:
        if profiles:
            import os as _os
            _os.environ["BLS_C15_PROFILES"] = profiles
        if not (legacy_id and modern_id):
            s.finish(ok=False, note="--legacy/--modern 누락 (live mode)")
            return False, ValidationReport()
        try:
            legacy = _build_live_source(legacy_id)
            modern = _build_live_source(modern_id)
        except Exception as exc:  # noqa: BLE001
            s.finish(ok=False, note=f"data source build failed: {exc}")
            return False, ValidationReport()
        tables = _resolve_tables(tables_arg)
        if not tables:
            s.finish(ok=False, note="no tables resolved (provide --tables)")
            return False, ValidationReport()
    vr = run_checks(legacy=legacy, modern=modern, tables=tables)
    ok = vr.failed == 0
    s.finish(
        ok=ok,
        note=f"total={vr.total} passed={vr.passed} failed={vr.failed}",
    )
    return ok, vr


def _exec_p5_uat(report: RunReport) -> bool:
    s = report.add_step("P5", "사용자 검수 (UAT 합격)")
    s.finish(
        ok=True,
        note="UAT 합격 여부는 외부 게이트 — 본 스크립트는 표식만 기록",
    )
    return True


def _exec_p6_switch(report: RunReport) -> bool:
    s = report.add_step("P6", "운영 전환 (DNS/proxy 스위치)")
    if report.mode == "dryrun":
        s.finish(ok=True, note="dryrun — DNS/proxy 스위치 생략")
        return True
    if not report.confirmed:
        s.finish(
            ok=False,
            note="--confirm 미지정 — P6 (운영 전환) 거부",
        )
        return False
    s.finish(
        ok=True,
        note="DNS/proxy 스위치는 운영 절차로 수기 처리 — 본 단계는 게이트 통과 기록",
    )
    return True


def _execute_rollback(report: RunReport) -> None:
    """롤백 4 step 시뮬레이션 (외부 명령 없음)."""
    report.rollback_started_at = time.time()
    rs = report.add_step("ROLLBACK", "rollback 절차 4 step (시뮬레이션)")
    for note in (
        "1. 신규 환경 read-only mode 전환",
        "2. DNS/proxy 레거시 EXE 환경으로 스위치",
        "3. 24h 윈도우 내 신규 데이터 reconciliation",
        "4. 사후 RCA 작성 + DEC 보강",
    ):
        time.sleep(0.001)  # ordering 식별
        report.add_step(f"ROLLBACK.{note[:1]}", note).finish(ok=True)
    rs.finish(ok=True, note="rollback simulation completed")
    report.rollback_elapsed_sec = round(time.time() - report.rollback_started_at, 3)


# ───────────────────────────────────────────────────────────────────
# 메인 오케스트레이션
# ───────────────────────────────────────────────────────────────────
def execute(args: argparse.Namespace) -> tuple[RunReport, int]:
    report = RunReport(
        mode="dryrun" if args.dryrun else "live",
        confirmed=bool(args.confirm),
        legacy=args.legacy or "",
        modern=args.modern or "",
    )

    # OQ 차단 게이트 — live 모드에서는 미해소 시 즉시 종료 (rc=3).
    # dryrun 은 게이트를 *경고*만 기록 (--ignore-oq-block 동치) — 운영 절차 학습/회귀 용.
    blocking = find_blocking_open_questions()
    s_gate = report.add_step("GATE", "OQ 차단 게이트 검사")
    if blocking and report.mode == "live" and not args.ignore_oq_block:
        report.blocked_by = blocking
        s_gate.finish(
            ok=False,
            note=f"unresolved cutover_block OQ: {blocking} (해소 후 재실행)",
        )
        report.finished_at = time.time()
        return report, 3
    if blocking:
        report.blocked_by = blocking
        s_gate.finish(
            ok=True,
            note=(
                f"WARN — cutover_block OQ 미해소 ({blocking}) 가 있으나 "
                f"{'dryrun' if report.mode == 'dryrun' else '--ignore-oq-block'} 로 진행"
            ),
        )
    else:
        s_gate.finish(ok=True, note="모든 cutover_block OQ 해소 확인")

    # P1~P6 실행 — 단계별 실패 시 즉시 rollback.
    if not _exec_p1_lock(report):
        _execute_rollback(report)
        report.finished_at = time.time()
        return report, 1
    if not _exec_p2_dump(report):
        _execute_rollback(report)
        report.finished_at = time.time()
        return report, 1
    if not _exec_p3_import(report):
        _execute_rollback(report)
        report.finished_at = time.time()
        return report, 1
    p4_ok, vr = _exec_p4_validator(
        report,
        legacy_id=args.legacy,
        modern_id=args.modern,
        profiles=args.profiles,
        tables_arg=args.tables,
    )
    report.validator = vr.to_dict() if vr.results or vr.finished_at else None
    if not p4_ok:
        _execute_rollback(report)
        report.finished_at = time.time()
        return report, 1
    if not _exec_p5_uat(report):
        _execute_rollback(report)
        report.finished_at = time.time()
        return report, 1
    if not _exec_p6_switch(report):
        # P6 거부는 rollback 트리거 아님 — 운영 lock 만 유지.
        report.finished_at = time.time()
        return report, 4

    report.success = True
    report.finished_at = time.time()
    return report, 0


# ───────────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────────
def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="C15 운영 cut-over 오케스트레이션 (P1~P6)")
    p.add_argument("--legacy", help="legacy server id")
    p.add_argument("--modern", help="modern server id")
    p.add_argument("--profiles", help="DB 프로필 YAML 경로 (선택)")
    p.add_argument("--tables", nargs="+", help="검증 대상 테이블 (생략 시 contract 사용)")
    p.add_argument("--dryrun", action="store_true", help="InMemory fixture 로 dry-run")
    p.add_argument(
        "--confirm",
        action="store_true",
        help="P6 운영 전환을 명시 승인 (live mode 필수, dryrun 무시)",
    )
    p.add_argument(
        "--ignore-oq-block",
        action="store_true",
        help="(권장하지 않음) live mode 에서 OQ 차단 게이트 무시 — 운영팀 합의 필수",
    )
    p.add_argument("--out", help="리포트 JSON 출력 경로 (없으면 stdout)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    report, rc = execute(args)
    payload = json.dumps(report.to_dict(), indent=2, ensure_ascii=False, default=str)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"report written: {args.out}", file=sys.stderr)
    else:
        print(payload)
    return rc


if __name__ == "__main__":
    sys.exit(main())
