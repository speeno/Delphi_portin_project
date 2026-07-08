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

_ALLOWED_HELPERS = frozenset(
    {
        "enforce_hcode_isolation",
        "coalesce_request_hcode",
        # ACC-DATA-03 보강 — 식별자/범위/패턴 tamper 가드 (deps.py).
        "enforce_hcode_identity",
        "enforce_hcode_range",
        "enforce_hcode_pattern",
        # 라우터 내부 래퍼 — 동일 정책의 thin alias.
        "_require_publisher_hcode",
        "_guard_billing_hcode",
        "resolve_scope_hcode",
        # DEC-090 — 행=출판사(G7.Gcode) 도메인(T2 정산): 격리 계정만 강제,
        # 물류/총판은 선택 필터(기본 전체 합산 — 레거시 Subu47 동등).
        "resolve_publisher_row_scope",
    }
)
_PATH_HCODE_KEY_MARKERS = (
    "{order_key}",
    "{receipt_key}",
    "{return_key}",
    "{billing_key}",
)
_NOQA_MARKER = "noqa: hcode-router-coalesce"

# 테넌트 스코프를 결정하는 식별자 파라미터(인자명 또는 Query alias).
#   - hcode/hcodeFrom/hcodeTo : courier 등 hcode 직접/구간
#   - customerCode/customerPattern : ledger — 서비스에서 그대로 Hcode 필터로 사용
_SCOPE_IDENT_NAMES = frozenset(
    {
        "hcode",
        "hcodeFrom",
        "hcodeTo",
        "hcode_from",
        "hcode_to",
        "customerCode",
        "customer_code",
        "customerPattern",
        "customer_pattern",
    }
)


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
    scope_identifier_endpoints: int = 0
    path_hcode_key_endpoints: int = 0
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


def _param_defaults(func: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, ast.expr | None]:
    defaults: dict[str, ast.expr | None] = {}
    pdefs = list(func.args.defaults)
    if pdefs:
        for a, d in zip(func.args.args[-len(pdefs):], pdefs):
            defaults[a.arg] = d
    for a, d in zip(func.args.kwonlyargs, list(func.args.kw_defaults)):
        defaults[a.arg] = d
    return defaults


def _query_alias(default: ast.expr | None) -> str | None:
    """``Query(..., alias="x")`` 의 alias 문자열을 반환(없으면 None)."""
    if not isinstance(default, ast.Call):
        return None
    if not (isinstance(default.func, ast.Name) and default.func.id == "Query"):
        return None
    for kw in default.keywords:
        if kw.arg == "alias" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    return None


def _tenant_scope_idents(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """시그니처에서 테넌트 스코프 식별자 파라미터(인자명/Query alias)를 수집."""
    defaults = _param_defaults(func)
    args = list(func.args.args) + list(func.args.kwonlyargs)
    found: list[str] = []
    for a in args:
        d = defaults.get(a.arg)
        # Query 파라미터만 대상(Depends/Body 모델 제외).
        if not (isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "Query"):
            continue
        alias = _query_alias(d)
        if a.arg in _SCOPE_IDENT_NAMES:
            found.append(a.arg)
        elif alias and alias in _SCOPE_IDENT_NAMES:
            found.append(alias)
    return found


def _collect_hcode_body_models(tree: ast.AST) -> set[str]:
    """``hcode`` 필드를 가진 Pydantic BaseModel 클래스명 집합."""
    models: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {
            (b.id if isinstance(b, ast.Name) else getattr(b, "attr", ""))
            for b in node.bases
        }
        if "BaseModel" not in base_names:
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                if stmt.target.id == "hcode":
                    models.add(node.name)
                    break
    return models


def _has_body_hcode_param(
    func: ast.FunctionDef | ast.AsyncFunctionDef, body_models: set[str]
) -> bool:
    """POST/PATCH body 모델 파라미터가 hcode 필드를 갖는지."""
    for a in list(func.args.args) + list(func.args.kwonlyargs):
        ann = a.annotation
        name = ann.id if isinstance(ann, ast.Name) else None
        if name and name in body_models:
            return True
    return False


def _body_text(source_lines: list[str], func: ast.AST) -> str:
    start = getattr(func, "lineno", 1) - 1
    end = getattr(func, "end_lineno", start + 1)
    return "\n".join(source_lines[start:end])


def _has_path_hcode_key(path: str) -> bool:
    """합성키 path 에 hcode 세그먼트가 포함된 상세/출력 GET."""
    return any(marker in path for marker in _PATH_HCODE_KEY_MARKERS)


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
    body_models = _collect_hcode_body_models(tree)
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

        # 검출 축 1) GET 의 optional ``hcode: Query(None)`` (기존 정책).
        is_optional_hcode_get = method == "GET" and _has_optional_hcode_query(node)
        if is_optional_hcode_get:
            stats.optional_hcode_endpoints += 1

        # 검출 축 2) 메서드 무관 — 테넌트 스코프 식별자 파라미터 / body hcode.
        idents = _tenant_scope_idents(node)
        has_body_hcode = (
            method in ("POST", "PUT", "PATCH")
            and _has_body_hcode_param(node, body_models)
        )
        if idents or has_body_hcode:
            stats.scope_identifier_endpoints += 1

        has_path_hcode_key = (
            method == "GET" and bool(path_str) and _has_path_hcode_key(path_str)
        )
        if has_path_hcode_key:
            stats.path_hcode_key_endpoints += 1

        if not (is_optional_hcode_get or idents or has_body_hcode or has_path_hcode_key):
            continue

        body = _body_text(src_lines, node)
        if _NOQA_MARKER in body:
            stats.skipped_noqa += 1
            continue

        signal_bits: list[str] = []
        if is_optional_hcode_get:
            signal_bits.append("optional_hcode_query")
        if idents:
            signal_bits.append("idents=" + ",".join(sorted(set(idents))))
        if has_body_hcode:
            signal_bits.append("body_hcode")
        if has_path_hcode_key:
            signal_bits.append("path_hcode_key")
        signal = "; ".join(signal_bits)

        if _calls_helper(body):
            findings.append(
                Finding(
                    file=str(path),
                    function=node.name,
                    path=path_str or "",
                    method=method,
                    lineno=node.lineno,
                    severity="info",
                    reason=f"scoped_with_helper ({signal})",
                    recommended_action="OK — enforce_hcode_* 가드 사용 확인",
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
                reason=f"scoped_without_helper ({signal})",
                recommended_action=(
                    "라우터에서 enforce_hcode_isolation / enforce_hcode_identity / "
                    "enforce_hcode_range / enforce_hcode_pattern 로 감싸 "
                    "JWT scope 자동 주입 + tamper(타사 hcode 403) 가드 부여"
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
            "scope_identifier_endpoints": stats.scope_identifier_endpoints,
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
        f"scope_idents={stats.scope_identifier_endpoints} "
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
