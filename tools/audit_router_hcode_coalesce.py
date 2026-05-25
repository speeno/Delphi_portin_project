#!/usr/bin/env python3
"""ACC-DATA-03 보강 — 라우터 정적 점검: optional ``hcode`` Query 누락 가드.

배경
----
[`tools/audit_domain_api_hcode_filter.py`](audit_domain_api_hcode_filter.py) 는 서비스 레이어
SQL 패턴(``WHERE Hcode``)만 검수한다. 하지만 라우터가 ``hcode`` Query 를 받고도
서비스에 그대로(``hcode=hcode``) 전달하면 빈 hcode 입력 시 SQL 의 동적 분기가
작동해 **타사 row 가 노출**될 수 있다(도서 마스터 125,861건 vs 스코프 59건 회귀와 동일 클래스).

본 도구는 ``backend/app/routers/*.py`` 의 모든 list/집계 GET 엔드포인트를 AST 로 훑어,
``hcode: str | None = Query(None)`` (optional) 시그니처를 갖는 함수가 본문에서
``enforce_hcode_isolation`` 또는 ``coalesce_request_hcode`` 를 호출하지 않으면
``critical`` 로 분류한다.

화이트리스트 마커
-----------------
함수 docstring 또는 주석에 ``# noqa: hcode-router-coalesce`` 가 있으면 의도적 예외로 간주.

사용
----
    python3 tools/audit_router_hcode_coalesce.py
    python3 tools/audit_router_hcode_coalesce.py --strict   # CRITICAL > 0 시 exit 2
    python3 tools/audit_router_hcode_coalesce.py --json /tmp/router_hcode_audit.json
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROUTERS_DIR = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers"
)
DEFAULT_OUT = REPO_ROOT / "analysis" / "welove_router_hcode_audit.json"

_ALLOWED_HELPERS = frozenset({"enforce_hcode_isolation", "coalesce_request_hcode"})
_NOQA_MARKER = "noqa: hcode-router-coalesce"


@dataclass
class Finding:
    file: str
    function: str
    path: str
    method: str
    lineno: int
    severity: str
    reason: str
    recommended_action: str


@dataclass
class Stats:
    files_scanned: int = 0
    endpoints_seen: int = 0
    optional_hcode_endpoints: int = 0
    findings_critical: int = 0
    findings_info: int = 0
    skipped_noqa: int = 0


def _route_path_method(deco: ast.expr) -> tuple[str, str] | None:
    if not isinstance(deco, ast.Call):
        return None
    func = deco.func
    if not isinstance(func, ast.Attribute):
        return None
    if not isinstance(func.value, ast.Name) or func.value.id != "router":
        return None
    method = func.attr.upper()
    path = ""
    if deco.args and isinstance(deco.args[0], ast.Constant):
        path = str(deco.args[0].value)
    return method, path


def _has_optional_hcode_query(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """함수 시그니처 안에 ``hcode: ... = Query(None)`` 형태가 있는지 검사."""
    args = list(func.args.args) + list(func.args.kwonlyargs)
    pdefs = list(func.args.defaults)
    kw_defs = list(func.args.kw_defaults)
    defaults: dict[str, ast.expr | None] = {}
    if pdefs:
        for a, d in zip(func.args.args[-len(pdefs):], pdefs):
            defaults[a.arg] = d
    for a, d in zip(func.args.kwonlyargs, kw_defs):
        defaults[a.arg] = d
    for a in args:
        if a.arg != "hcode":
            continue
        d = defaults.get("hcode")
        if not isinstance(d, ast.Call):
            continue
        if isinstance(d.func, ast.Name) and d.func.id == "Query":
            # 첫 인자가 None 또는 ... 모두 optional. 단 hcode 가 required (...) 일 때는 제외.
            if d.args:
                first = d.args[0]
                if isinstance(first, ast.Constant) and first.value is None:
                    return True
                if isinstance(first, ast.Constant) and first.value is Ellipsis:
                    return False
            return True
    return False


def _body_text(source_lines: list[str], func: ast.AST) -> str:
    start = getattr(func, "lineno", 1) - 1
    end = getattr(func, "end_lineno", start + 1)
    return "\n".join(source_lines[start:end])


def _calls_helper(body_text: str) -> bool:
    return any(h + "(" in body_text for h in _ALLOWED_HELPERS)


def _scan_file(path: Path, stats: Stats) -> list[Finding]:
    findings: list[Finding] = []
    src = path.read_text(encoding="utf-8")
    src_lines = src.split("\n")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return findings
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        method = path_str = None
        for d in node.decorator_list:
            mp = _route_path_method(d)
            if mp:
                method, path_str = mp
                break
        if method is None:
            continue
        stats.endpoints_seen += 1
        # 본 도구는 GET (목록/집계) 위주. POST/PUT/PATCH/DELETE 는 단건 처리/식별자.
        if method != "GET":
            continue
        if not _has_optional_hcode_query(node):
            continue
        stats.optional_hcode_endpoints += 1
        body = _body_text(src_lines, node)
        if _NOQA_MARKER in body:
            stats.skipped_noqa += 1
            continue
        if _calls_helper(body):
            findings.append(
                Finding(
                    file=str(path),
                    function=node.name,
                    path=path_str or "",
                    method=method,
                    lineno=node.lineno,
                    severity="info",
                    reason="optional_hcode_with_helper",
                    recommended_action="OK — enforce_hcode_isolation 사용 확인",
                )
            )
            stats.findings_info += 1
            continue
        findings.append(
            Finding(
                file=str(path),
                function=node.name,
                path=path_str or "",
                method=method,
                lineno=node.lineno,
                severity="critical",
                reason="optional_hcode_without_helper",
                recommended_action=(
                    "라우터에서 enforce_hcode_isolation(hcode, ctx) 로 감싸 "
                    "JWT scope 자동 주입 + tamper 가드 부여"
                ),
            )
        )
        stats.findings_critical += 1
    return findings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true", help="critical > 0 시 exit 2")
    p.add_argument(
        "--json",
        type=Path,
        default=DEFAULT_OUT,
        help=f"결과 JSON 경로 (default: {DEFAULT_OUT.relative_to(REPO_ROOT)})",
    )
    p.add_argument(
        "--routers-dir",
        type=Path,
        default=DEFAULT_ROUTERS_DIR,
        help="대상 라우터 디렉토리",
    )
    args = p.parse_args()

    stats = Stats()
    all_findings: list[Finding] = []
    for fp in sorted(args.routers_dir.glob("*.py")):
        if fp.name.startswith("_"):
            continue
        stats.files_scanned += 1
        all_findings.extend(_scan_file(fp, stats))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "files_scanned": stats.files_scanned,
            "endpoints_seen": stats.endpoints_seen,
            "optional_hcode_endpoints": stats.optional_hcode_endpoints,
            "critical": stats.findings_critical,
            "info": stats.findings_info,
            "skipped_noqa": stats.skipped_noqa,
        },
        "findings": [f.__dict__ for f in all_findings],
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        f"[router-hcode-audit] files={stats.files_scanned} "
        f"endpoints={stats.endpoints_seen} "
        f"optional_hcode={stats.optional_hcode_endpoints} "
        f"critical={stats.findings_critical} info={stats.findings_info} "
        f"skipped_noqa={stats.skipped_noqa}"
    )
    for f in all_findings:
        if f.severity == "critical":
            rel = Path(f.file).relative_to(REPO_ROOT)
            print(
                f"  CRITICAL {rel}:{f.lineno} {f.method} {f.path} "
                f"{f.function} — {f.reason}"
            )

    if args.strict and stats.findings_critical > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
