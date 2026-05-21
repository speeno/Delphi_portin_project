#!/usr/bin/env python3
"""감사 로그(`audit.auth`) 분류기 — DSN-DEC-08/09/12 운영 진단.

목적
----
`audit.auth` 로거가 출력한 ``auth.login {...JSON...}`` 라인을 파싱해
[docs/welove-cross-tenant-exposure-runbook.md](../docs/welove-cross-tenant-exposure-runbook.md) §2
의 8개 카테고리(A~H)로 분류 + 카운트 출력한다.

특징
----
- 표준 입력 또는 파일 경로 모두 지원.
- 라인 한 줄에 JSON 이 아닌 텍스트가 섞여 있어도 ``{...}`` 구간만 떼어 파싱.
- 비밀번호/토큰은 입력 단계에서도 결과에서도 절대 출력하지 않는다 (감사 정책 G3).
- ``--per-user`` 옵션으로 사용자별 빈도 상위 N 명 출력 (사고 추적용).
- 단일 책임: 본 도구는 분류·집계만. 자동 정정은 ``tools/audit_welove_routing_consistency.py`` 가 담당.

비밀 정책
---------
- 본 도구는 비밀번호 / 토큰 / 평문 자격증명을 어떤 입력에서도 읽지 않는다.
- 출력에는 사용자 ID 와 카운트만 포함.

사용
----
    python3 tools/classify_login_audit_logs.py /var/log/audit-auth.log
    cat /var/log/audit-auth.log | python3 tools/classify_login_audit_logs.py
    python3 tools/classify_login_audit_logs.py audit.log --per-user 10
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


_CATEGORY_ORDER: tuple[str, ...] = (
    "A_SEED_MISMATCH",
    "B_INDEX_STALE",
    "C_AMBIGUOUS_NARROWING",
    "D_DIRECTORY_SWEEP_HIT",
    "E_OWNERSHIP_VIOLATION",
    "F_TOKEN_BUILD_FAILED",
    "G_INVALID_CREDENTIALS",
    "H_AMBIGUOUS_STRICT",
)


_CATEGORY_DOC: dict[str, str] = {
    "A_SEED_MISMATCH": "성공 응답인데 (server_id, resolved_db) 가 시드/매트릭스에 없음 — 시드 누락",
    "B_INDEX_STALE": "lazy_refreshed=true 후 성공 — 인덱스 신선도 저하 (야간 재빌드 검토)",
    "C_AMBIGUOUS_NARROWING": "ambiguous_narrowed=true + candidate_attempts >= 2 (정상 default 동작)",
    "D_DIRECTORY_SWEEP_HIT": "directory_sweep=true 로 성공 — 신규 가입자/인덱스 누락",
    "E_OWNERSHIP_VIOLATION": "DSN-DEC-12 — 타사 매핑이 차단됐음 (가드가 동작한 흔적)",
    "F_TOKEN_BUILD_FAILED": "reason=token_build_failed — 토큰 빌드 회귀 (즉시 PR)",
    "G_INVALID_CREDENTIALS": "reason=invalid_credentials* — 정상 401",
    "H_AMBIGUOUS_STRICT": "ambiguous_strict=true — strict 모드 차단",
}


@dataclass
class ClassificationResult:
    counts: dict[str, int]
    per_user: collections.Counter
    total_lines: int
    parse_failures: int


def _iter_records_from_lines(lines: Iterable[str]) -> Iterable[dict]:
    """``auth.login {...}`` / ``... {...}`` / 순수 JSON 라인을 통합 파싱."""
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        idx = line.find("{")
        if idx < 0:
            continue
        chunk = line[idx:]
        try:
            yield json.loads(chunk)
        except Exception:
            continue


def _classify_record(rec: dict) -> str:
    """단일 감사 record → 카테고리 코드.

    분류 규칙은 위 ``_CATEGORY_DOC`` 와 1:1.
    우선순위: E (가장 중요) > F > A > H > B > D > C > G.
    """
    result = (rec.get("result") or "").strip()
    reason = (rec.get("reason") or "").strip()
    ownership_violation = bool(rec.get("ownership_violation"))
    ambiguous_strict = bool(rec.get("ambiguous_strict"))
    ambiguous_narrowed = bool(rec.get("ambiguous_narrowed"))
    lazy_refreshed = bool(rec.get("lazy_refreshed"))
    directory_sweep = bool(rec.get("directory_sweep"))
    candidate_attempts = int(rec.get("candidate_attempts") or 0)
    seed_mismatch = bool(rec.get("seed_mismatch"))

    if ownership_violation:
        return "E_OWNERSHIP_VIOLATION"
    if reason == "token_build_failed":
        return "F_TOKEN_BUILD_FAILED"
    if seed_mismatch:
        return "A_SEED_MISMATCH"
    if ambiguous_strict and result == "failure":
        return "H_AMBIGUOUS_STRICT"
    if lazy_refreshed and result == "success":
        return "B_INDEX_STALE"
    if directory_sweep and result == "success":
        return "D_DIRECTORY_SWEEP_HIT"
    if ambiguous_narrowed and candidate_attempts >= 2:
        return "C_AMBIGUOUS_NARROWING"
    if reason in ("invalid_credentials", "invalid_credentials_after_probe", "ambiguous_route"):
        return "G_INVALID_CREDENTIALS"
    return "G_INVALID_CREDENTIALS"


def classify(lines: Iterable[str]) -> ClassificationResult:
    counts: dict[str, int] = {c: 0 for c in _CATEGORY_ORDER}
    per_user: collections.Counter = collections.Counter()
    total = 0
    failures = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        total += 1
        idx = line.find("{")
        if idx < 0:
            failures += 1
            continue
        try:
            rec = json.loads(line[idx:])
        except Exception:
            failures += 1
            continue
        cat = _classify_record(rec)
        counts[cat] = counts.get(cat, 0) + 1
        gcode = (rec.get("gcode") or "").strip()
        if gcode:
            per_user[(gcode, cat)] += 1
    return ClassificationResult(
        counts=counts,
        per_user=per_user,
        total_lines=total,
        parse_failures=failures,
    )


def _print_report(result: ClassificationResult, per_user_top: int) -> None:
    print(f"총 라인 수      = {result.total_lines}")
    print(f"파싱 실패       = {result.parse_failures}")
    print()
    print("카테고리 집계")
    print("-" * 80)
    for cat in _CATEGORY_ORDER:
        n = result.counts.get(cat, 0)
        doc = _CATEGORY_DOC[cat]
        print(f"  {cat:<28} {n:>8}  {doc}")
    if per_user_top > 0 and result.per_user:
        print()
        print(f"사용자별 상위 {per_user_top} 건 (gcode, category)")
        print("-" * 80)
        for (gcode, cat), n in result.per_user.most_common(per_user_top):
            print(f"  {gcode:<24} {cat:<28} {n:>6}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="audit.auth 로그 분류기 (DSN-DEC-08/09/12)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="감사 로그 파일 경로 (생략/-: stdin)",
    )
    parser.add_argument(
        "--per-user",
        type=int,
        default=0,
        help="사용자별 상위 N 건도 함께 출력 (기본 0 = 미출력)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 형식 출력 (자동화 파이프라인용)",
    )
    args = parser.parse_args(argv)

    if args.path == "-" or not args.path:
        result = classify(sys.stdin)
    else:
        p = Path(args.path)
        if not p.exists():
            print(f"[ERR] file not found: {p}", file=sys.stderr)
            return 2
        with p.open("r", encoding="utf-8", errors="replace") as fh:
            result = classify(fh)

    if args.json:
        out = {
            "total_lines": result.total_lines,
            "parse_failures": result.parse_failures,
            "counts": {c: result.counts.get(c, 0) for c in _CATEGORY_ORDER},
            "category_doc": _CATEGORY_DOC,
        }
        if args.per_user > 0:
            out["per_user_top"] = [
                {"gcode": g, "category": c, "count": n}
                for (g, c), n in result.per_user.most_common(args.per_user)
            ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        _print_report(result, args.per_user)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
