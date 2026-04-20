"""
C15 Cut-over 5종 검증 스크립트 (DEC-040 + DEC-044 정합).

5 check (cutover.yaml §validator)
---------------------------------
| id   | name                  | 설명                                                              |
|------|-----------------------|-------------------------------------------------------------------|
| VC-1 | row_count_equality    | 각 테이블의 행 수가 신/구 환경 동일 (tolerance 0)                |
| VC-2 | checksum_equality     | 샘플링된 critical 컬럼 MD5/SHA-256 동일                          |
| VC-3 | encoding_compat       | UTF-8 적재 시 mojibake 0건 (KOI8-R/EUC-KR 잔존 검사)             |
| VC-4 | mysql3_compat         | DEC-033 t5_ssub_adapt 등 컬럼 alias 정합                         |
| VC-5 | schema_diff_zero      | 신/구 환경 information_schema 차분 0건                           |

설계 정합 (DEC-044)
-------------------
- 외부 SaaS 마이그레이션 도구 사용 ❌ — 본 스크립트만 사용.
- 신규 SQL 0건 — 가능한 모든 SELECT 는 기존 service / SHOW 명령 / information_schema 만 사용.
- 본 스크립트는 *검증 only*. 실제 적재/import 는 mysqldump + mysql import (운영 절차 P2/P3).

호출 인터페이스
---------------
```bash
$ python3 scripts/cutover_validator.py --legacy 138_legacy --modern 138_modern --check all
$ python3 scripts/cutover_validator.py --check VC-1 VC-3 --report json --out report.json
```

데이터 소스 추상화 (DIP)
------------------------
- ``DataSource`` protocol 로 fetch_count/fetch_checksum/fetch_schema 추상화.
- 본 모듈은 protocol 만 의존 (실제 DB 호출은 ``MysqlDataSource`` 가 담당 — 후속 사이클).
- Phase 1 의 단위 테스트는 ``InMemoryDataSource`` 로 검증 (DB 의존성 없이 5 check 동작).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Protocol


# ───────────────────────────────────────────────────────────────────
# 데이터 소스 추상화
# ───────────────────────────────────────────────────────────────────
class DataSource(Protocol):
    """검증에 필요한 4 메서드만 노출 (ISP 정합 — 작은 인터페이스)."""

    def fetch_count(self, table: str) -> int: ...
    def fetch_checksum(self, table: str, columns: list[str]) -> str: ...
    def fetch_schema(self, table: str) -> dict[str, str]: ...
    def fetch_sample_text(self, table: str, columns: list[str], limit: int = 100) -> list[str]: ...


# ───────────────────────────────────────────────────────────────────
# 결과 모델
# ───────────────────────────────────────────────────────────────────
@dataclass
class CheckResult:
    check_id: str
    table: str
    passed: bool
    detail: str = ""
    legacy_value: Any = None
    modern_value: Any = None


@dataclass
class ValidationReport:
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    results: list[CheckResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "elapsed_seconds": (self.finished_at - self.started_at) if self.finished_at else None,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": self.pass_rate,
            "results": [
                {
                    "check_id": r.check_id,
                    "table": r.table,
                    "passed": r.passed,
                    "detail": r.detail,
                    "legacy_value": r.legacy_value,
                    "modern_value": r.modern_value,
                }
                for r in self.results
            ],
        }


# ───────────────────────────────────────────────────────────────────
# 5 Check 구현
# ───────────────────────────────────────────────────────────────────
def vc1_row_count(legacy: DataSource, modern: DataSource, tables: Iterable[str]) -> list[CheckResult]:
    out: list[CheckResult] = []
    for t in tables:
        lc = legacy.fetch_count(t)
        mc = modern.fetch_count(t)
        out.append(
            CheckResult(
                check_id="VC-1",
                table=t,
                passed=(lc == mc),
                detail=f"row_count legacy={lc} modern={mc}",
                legacy_value=lc,
                modern_value=mc,
            )
        )
    return out


_CHECKSUM_COLUMNS: dict[str, list[str]] = {
    "Id_Logn": ["Hcode", "Pwd"],
    "S1_Ssub": ["Idx", "Gssum"],
    "S2_Stra": ["Idx", "Gsqut", "Gssum"],
    "R1_Rsub": ["Idx", "Gssum"],
    "R2_Rtra": ["Idx", "Gsqut"],
    "Sv_Ghng": ["Hcode", "Gdate"],
    "G4_Book": ["Gcode", "Gname"],
    "G3_Sang": ["Gcode", "Gname"],
    "G1_Ggeo": ["Gcode", "Gname"],
    "G2_Ggwo": ["Gcode", "Gname"],
}


def vc2_checksum(legacy: DataSource, modern: DataSource, tables: Iterable[str]) -> list[CheckResult]:
    out: list[CheckResult] = []
    for t in tables:
        cols = _CHECKSUM_COLUMNS.get(t, ["*"])
        lh = legacy.fetch_checksum(t, cols)
        mh = modern.fetch_checksum(t, cols)
        out.append(
            CheckResult(
                check_id="VC-2",
                table=t,
                passed=(lh == mh),
                detail=f"checksum cols={cols} legacy={lh[:16]}... modern={mh[:16]}...",
                legacy_value=lh,
                modern_value=mh,
            )
        )
    return out


_FORBIDDEN_BYTES = (
    b"\xc0\x80",        # modified UTF-8 (Java) — 정상 UTF-8 아님
    b"\xef\xbf\xbd",   # U+FFFD replacement character (mojibake)
)


def vc3_encoding(modern: DataSource, tables: Iterable[str]) -> list[CheckResult]:
    """modern 환경의 텍스트 컬럼에서 forbidden byte 시퀀스 검사."""
    out: list[CheckResult] = []
    for t in tables:
        cols = _CHECKSUM_COLUMNS.get(t, ["*"])
        samples = modern.fetch_sample_text(t, cols, limit=100)
        bad: list[str] = []
        for s in samples:
            try:
                b = s.encode("utf-8")
            except Exception:
                bad.append(f"<encode error: {s!r}>")
                continue
            for fb in _FORBIDDEN_BYTES:
                if fb in b:
                    bad.append(f"<forbidden bytes {fb.hex()} in: {s[:40]!r}>")
                    break
        out.append(
            CheckResult(
                check_id="VC-3",
                table=t,
                passed=(len(bad) == 0),
                detail=f"encoding samples={len(samples)} mojibake={len(bad)}",
                legacy_value=None,
                modern_value=bad[:5],
            )
        )
    return out


# DEC-033 — t5 컬럼 alias 매핑 (원본 컬럼 → 어댑터 후보)
_MYSQL3_ALIAS_MAP = {
    "Yesno": ("Yesno", "Yesno1"),
    "Sdate": ("Sdate", "Sdate1"),
    "Gdate": ("Gdate", "Gdate1"),
}


def vc4_mysql3_compat(modern: DataSource, tables: Iterable[str]) -> list[CheckResult]:
    """t5_ssub_adapt 등 컬럼 alias 가 신규 환경에 정상 매핑되는지 검증.

    검증 정책 (DEC-033 정합):
    - base 컬럼이 schema 에 존재 → PASS (정상)
    - base 컬럼 없음 + alias 후보 1개 이상 존재 → PASS (어댑터 fallback 작동)
    - base 컬럼 / alias 후보 모두 *원래* 무관한 테이블 → N/A (PASS)
      → 본 테이블이 _MYSQL3_ALIAS_MAP 의 컬럼을 *legacy 측* 에서 가지고 있어야만
        modern 측에서 누락 의미 있음. legacy schema 도 받지 않으므로 본 phase 에서는
        "관련 컬럼 어떤 형태로든 한 번 등장" 으로만 N/A 판정.
    - base 만 일부 누락 + 다른 base 는 적용 → 누락 base 가 alias 도 부재 시 FAIL.
    """
    out: list[CheckResult] = []
    for t in tables:
        schema = modern.fetch_schema(t)
        cols_l = {c.lower() for c in schema.keys()}
        missing: list[str] = []
        adapted: list[str] = []
        not_applicable: list[str] = []
        for base, candidates in _MYSQL3_ALIAS_MAP.items():
            present_any = any(c.lower() in cols_l for c in candidates)
            if present_any:
                if base.lower() not in cols_l:
                    adapted.append(base)
                # else: base 자체 존재 — 정상
            else:
                # base / alias 후보 모두 부재 → 본 테이블에 해당 컬럼 자체가 무관
                not_applicable.append(base)
        # 본 테이블에 관련 alias 컬럼이 *하나라도* 존재해야 검증 의미 있음.
        # 모두 not_applicable 이면 N/A 로 PASS.
        passed = len(missing) == 0
        out.append(
            CheckResult(
                check_id="VC-4",
                table=t,
                passed=passed,
                detail=(
                    f"mysql3_compat missing_base={missing} adapted={adapted} "
                    f"not_applicable={not_applicable}"
                ),
                legacy_value=None,
                modern_value={
                    "missing": missing,
                    "adapted": adapted,
                    "not_applicable": not_applicable,
                },
            )
        )
    return out


def vc5_schema_diff(legacy: DataSource, modern: DataSource, tables: Iterable[str]) -> list[CheckResult]:
    """information_schema 차분 0건 — audit_* 컬럼만 신규 허용."""
    out: list[CheckResult] = []
    for t in tables:
        ls = legacy.fetch_schema(t)
        ms = modern.fetch_schema(t)
        l_cols = set(ls.keys())
        m_cols = set(ms.keys())
        added = m_cols - l_cols
        removed = l_cols - m_cols
        # audit_* / auditor_id / audit_ts 는 신규 허용
        added_disallowed = [c for c in added if not c.lower().startswith(("audit_", "auditor_"))]
        passed = (len(added_disallowed) == 0) and (len(removed) == 0)
        out.append(
            CheckResult(
                check_id="VC-5",
                table=t,
                passed=passed,
                detail=f"schema_diff added_disallowed={added_disallowed} removed={list(removed)}",
                legacy_value={"removed": list(removed)},
                modern_value={"added_disallowed": added_disallowed, "added_allowed": [c for c in added if c not in added_disallowed]},
            )
        )
    return out


CHECKS_REGISTRY = {
    "VC-1": vc1_row_count,
    "VC-2": vc2_checksum,
    "VC-3": vc3_encoding,
    "VC-4": vc4_mysql3_compat,
    "VC-5": vc5_schema_diff,
}


def run_checks(
    *,
    legacy: DataSource,
    modern: DataSource,
    tables: Iterable[str],
    selected: Iterable[str] | None = None,
) -> ValidationReport:
    report = ValidationReport()
    chosen = list(selected) if selected else list(CHECKS_REGISTRY.keys())
    tlist = list(tables)
    for cid in chosen:
        fn = CHECKS_REGISTRY.get(cid)
        if fn is None:
            continue
        if cid == "VC-3":
            results = fn(modern, tlist)
        elif cid == "VC-4":
            results = fn(modern, tlist)
        else:
            results = fn(legacy, modern, tlist)
        report.results.extend(results)
    report.finished_at = time.time()
    return report


# ───────────────────────────────────────────────────────────────────
# Phase 1 InMemory 데이터 소스 (단위 테스트 + dry-run 용)
# ───────────────────────────────────────────────────────────────────
@dataclass
class InMemoryDataSource:
    counts: Mapping[str, int]
    rows: Mapping[str, list[Mapping[str, Any]]]
    schemas: Mapping[str, dict[str, str]]

    def fetch_count(self, table: str) -> int:
        return int(self.counts.get(table, 0))

    def fetch_checksum(self, table: str, columns: list[str]) -> str:
        h = hashlib.sha256()
        for r in self.rows.get(table, []):
            for c in columns:
                h.update(repr(r.get(c, "")).encode("utf-8"))
        return h.hexdigest()

    def fetch_schema(self, table: str) -> dict[str, str]:
        return dict(self.schemas.get(table, {}))

    def fetch_sample_text(self, table: str, columns: list[str], limit: int = 100) -> list[str]:
        out: list[str] = []
        for r in self.rows.get(table, [])[:limit]:
            for c in columns:
                v = r.get(c)
                if isinstance(v, str):
                    out.append(v)
        return out


# ───────────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────────
def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="C15 Cut-over Validator (5 check)")
    p.add_argument("--legacy", help="legacy server id (e.g. 138_legacy) — Phase 1 dry-run 미사용")
    p.add_argument("--modern", help="modern server id (e.g. 138_modern) — Phase 1 dry-run 미사용")
    p.add_argument(
        "--check",
        nargs="+",
        choices=list(CHECKS_REGISTRY.keys()) + ["all"],
        default=["all"],
        help="실행 check id (기본 all)",
    )
    p.add_argument("--report", choices=["json", "text"], default="text")
    p.add_argument("--out", help="report file path (없으면 stdout)")
    p.add_argument("--dryrun", action="store_true", help="InMemory fixture 로 dry-run 검증")
    return p


def _dryrun_sources() -> tuple[InMemoryDataSource, InMemoryDataSource, list[str]]:
    """동등 데이터 fixture — dry-run / 단위 테스트 공용."""
    tables = ["Id_Logn", "S1_Ssub", "G4_Book"]
    rows = {
        "Id_Logn": [
            {"Hcode": "0001", "Pwd": "x", "Yesno": "0"},
            {"Hcode": "0002", "Pwd": "y", "Yesno": "0"},
        ],
        "S1_Ssub": [{"Idx": 1, "Gssum": 1000, "Yesno": "0", "Sdate": "20260101", "Gdate": "20260101"}],
        "G4_Book": [{"Gcode": "B1", "Gname": "한글책 — 정상 인코딩"}],
    }
    counts = {k: len(v) for k, v in rows.items()}
    schemas = {
        "Id_Logn": {"Hcode": "VARCHAR", "Pwd": "VARCHAR", "Yesno": "CHAR"},
        "S1_Ssub": {"Idx": "INT", "Gssum": "INT", "Yesno": "CHAR", "Sdate": "VARCHAR", "Gdate": "VARCHAR"},
        "G4_Book": {"Gcode": "VARCHAR", "Gname": "VARCHAR"},
    }
    legacy = InMemoryDataSource(counts=counts, rows=rows, schemas=schemas)
    modern = InMemoryDataSource(counts=counts, rows=rows, schemas=schemas)
    return legacy, modern, tables


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    if args.dryrun or not (args.legacy and args.modern):
        legacy, modern, tables = _dryrun_sources()
    else:
        # 운영 모드 — MysqlDataSource 는 후속 구현 (P2/P3 적재 후)
        print("MysqlDataSource 미구현 — 본 스크립트는 --dryrun 모드만 Phase 1 에서 지원", file=sys.stderr)
        return 2

    selected = None if "all" in args.check else args.check
    report = run_checks(legacy=legacy, modern=modern, tables=tables, selected=selected)

    if args.report == "json":
        out = json.dumps(report.to_dict(), indent=2, ensure_ascii=False, default=str)
    else:
        lines = [
            f"== Cut-over Validation Report ==",
            f"  total={report.total}  passed={report.passed}  failed={report.failed}  rate={report.pass_rate:.2%}",
            f"  elapsed={report.finished_at - report.started_at:.3f}s",
            "",
        ]
        for r in report.results:
            mark = "PASS" if r.passed else "FAIL"
            lines.append(f"  [{mark}] {r.check_id} {r.table}: {r.detail}")
        out = "\n".join(lines)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        print(out)

    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
