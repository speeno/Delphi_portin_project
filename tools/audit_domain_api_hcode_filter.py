#!/usr/bin/env python3
"""DSN-DEC-12 보강 — 도메인 서비스 SQL 정적 점검: Hcode 필터 누락 검수.

배경
----
DSN-DEC-12 의 ownership 가드는 **로그인 시 JWT/사용자 컨텍스트** 만 보호한다. 출고/입고/
정산 등 도메인 서비스가 ``Hcode`` 필터 없이 ``WHERE`` 절을 짜면 동일 DB 내 타사 row 가
여전히 반환될 수 있다 ([docs/decision-login-db-routing.md](../docs/decision-login-db-routing.md) M4 별건).

본 도구는 ``backend/app/services/*.py`` 의 **SQL 리터럴**을 AST 로 추출하고,
**다중 테넌트 테이블** 에 대해 ``Hcode/hcode`` 필터 참조가 없는 SELECT/UPDATE/DELETE 문을
WARN 으로 분류한다.

테이블 분류
-----------
- **multi_tenant** (감사 대상): ``S1_Ssub``, ``G4_Book``, ``G6_Geo``, ``G7_Ggeo``, ``Tax_Invoice``,
  ``Cash_Book``, ``S2_Csub``, ``Pay_*``, ``Im_Inset`` 등 — 회사별 row 가 같은 DB 에 섞이는 테이블.
- **system** (제외): ``Id_Logn``, ``Web_Admin``, ``account_directory`` 등 — 인증/메타.
- **unknown** : 분류되지 않은 테이블 (``--strict`` 시 별도 카운트).

화이트리스트 마커
-----------------
   sql = "SELECT ... FROM Tax_Invoice WHERE ..."  # noqa: hcode-guard
서비스 함수 단위로 ``# noqa: hcode-guard``  마커를 SQL 리터럴 직전 또는 같은 줄에 두면
의도적 예외로 간주한다.

사용
----
    python3 tools/audit_domain_api_hcode_filter.py
    python3 tools/audit_domain_api_hcode_filter.py --strict   # WARN > 0 시 exit 2
    python3 tools/audit_domain_api_hcode_filter.py --json /tmp/hcode_audit.json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SERVICES_DIR = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "app" / "services"
)
DEFAULT_OUT = REPO_ROOT / "analysis" / "welove_domain_api_hcode_audit.json"


# 회사 hcode 컬럼이 의미를 갖는 다중 테넌트 테이블 (보강 시 본 set 만 갱신).
MULTI_TENANT_TABLES = frozenset(
    {
        # Subu*/Sobo* 거래/원장
        "S1_Ssub", "S1_Smast", "S2_Csub", "S2_Cmast", "S5_Pay", "Pay",
        # 마스터
        "G4_Book", "G6_Geo", "G7_Ggeo", "G2_Pub", "G3_Pcust",
        # 정산/세금/현금
        "Tax_Invoice", "Cash_Book", "Cash_Sub", "Cash_Income",
        # 입출고/반품/일일/월별
        "Im_Inset", "Im_Iout", "Out_Set", "Out_Sub",
        "Re_Sub", "Re_Mast",
        "Day_Sub", "Mon_Sub", "Year_Sub",
        # 운송/택배
        "Courier_Sub",
    }
)

# 인증/메타 — Hcode 가 의미 없거나 오히려 cross-tenant 가 정상인 테이블.
SYSTEM_TABLES = frozenset(
    {
        "Id_Logn",
        "Web_Admin", "Account_Directory", "Tenants_Directory", "Member_Signup",
        "Login_Id_Index",
        # 마스터 서버 정보 / 설정
        "Server_Registry", "Distributor_Limits",
        # 외부 API 캐시
        "Open_Api_Cache",
    }
)


_FROM_TABLE_RE = re.compile(
    r"\b(?:FROM|JOIN|UPDATE|INTO)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)
_HCODE_REF_RE = re.compile(r"\bHcode\b", re.IGNORECASE)
_HAS_WHERE_RE = re.compile(r"\bWHERE\b", re.IGNORECASE)
_DML_HEAD_RE = re.compile(r"^\s*(SELECT|UPDATE|DELETE|INSERT)\b", re.IGNORECASE)
_NOQA_RE = re.compile(r"#\s*noqa:\s*hcode-guard", re.IGNORECASE)


@dataclass
class Finding:
    file: str
    function: str
    lineno: int
    tables: list[str]
    severity: str  # info | warn
    reason: str
    sql_excerpt: str


@dataclass
class Stats:
    files_scanned: int = 0
    sql_literals: int = 0
    findings_warn: int = 0
    findings_info: int = 0
    skipped_noqa: int = 0
    multi_tenant_tables_seen: set[str] = field(default_factory=set)


def _classify_tables(tables: list[str]) -> tuple[list[str], list[str], list[str]]:
    multi: list[str] = []
    system: list[str] = []
    unknown: list[str] = []
    for t in tables:
        if t in MULTI_TENANT_TABLES:
            multi.append(t)
        elif t in SYSTEM_TABLES:
            system.append(t)
        else:
            unknown.append(t)
    return multi, system, unknown


def _collect_module_str_constants(tree: ast.AST) -> dict[str, str]:
    """모듈 레벨에서 ``NAME = <문자열식>`` 으로 정의된 SQL 조각 상수를 수집.

    ``f"... {X} ..."`` 처럼 SQL 본문이 외부 상수 ``X`` 를 인라인으로 끼워넣는
    컨벤션(예: [`inbound_service.SQL_DELETE_LINE`](../도서물류관리프로그램/backend/app/services/inbound_service.py))
    을 정확히 잡기 위해 SQL 텍스트 평가 시 본 상수 사전을 사용한다.
    """
    consts: dict[str, str] = {}
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name):
                evaluated = _eval_str_node(node.value, consts)
                if evaluated is not None:
                    consts[t.id] = evaluated
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            evaluated = _eval_str_node(node.value, consts)
            if evaluated is not None:
                consts[node.target.id] = evaluated
    return consts


def _eval_str_node(node: ast.AST, consts: dict[str, str]) -> str | None:
    """문자열만 결합되는 단순 식을 평가. 변수는 ``consts`` 에서 인라인."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                parts.append(v.value)
            elif isinstance(v, ast.FormattedValue):
                inner = v.value
                if isinstance(inner, ast.Name) and inner.id in consts:
                    parts.append(consts[inner.id])
                else:
                    sub = _eval_str_node(inner, consts)
                    if sub is None:
                        # 평가 불가 — 원본 placeholder 표시 ({placeholders} 같은 SQL 형식 보존 X 가능)
                        parts.append("<<dyn>>")
                    else:
                        parts.append(sub)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _eval_str_node(node.left, consts)
        right = _eval_str_node(node.right, consts)
        if left is None or right is None:
            return None
        return left + right
    if isinstance(node, ast.Call):
        # "...".format(...) — 첫 인자 base 만 평가.
        return None
    return None


def _iter_sql_literals(tree: ast.AST, consts: dict[str, str]):
    """``ast`` 노드 중 SELECT/UPDATE/DELETE/INSERT 로 시작하는 평가 가능한 SQL 식을 추출.

    함수 내부의 변수 참조도 모듈 상수에 해당하면 인라인 치환된다.
    부모-우선 순회로 ``JoinedStr`` / ``BinOp`` 내부 자식 ``Constant`` 가 별도로
    emit 되지 않게 한다 — 짧은 partial SQL 로 인한 false positive 방지.
    """
    seen: set[tuple[int, str]] = set()

    def _emit(node: ast.AST, sql: str):
        if not _DML_HEAD_RE.match(sql):
            return None
        key = (getattr(node, "lineno", 0) or 0, sql)
        if key in seen:
            return None
        seen.add(key)
        return node, sql

    def _visit(node: ast.AST):
        """반환값: True 면 본 노드 자식은 더 보지 않는다 (parent emitted)."""
        if isinstance(node, ast.JoinedStr):
            evaluated = _eval_str_node(node, consts)
            if evaluated is not None and _DML_HEAD_RE.match(evaluated):
                emitted = _emit(node, evaluated)
                if emitted:
                    yield emitted
            return  # JoinedStr 내부 Constant 는 더 보지 않는다.
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            evaluated = _eval_str_node(node, consts)
            if evaluated is not None and _DML_HEAD_RE.match(evaluated):
                emitted = _emit(node, evaluated)
                if emitted:
                    yield emitted
                return
            # 평가 실패 — 자식으로 내려간다.
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            emitted = _emit(node, node.value)
            if emitted:
                yield emitted
            return
        for child in ast.iter_child_nodes(node):
            yield from _visit(child)

    yield from _visit(tree)


def _enclosing_function(tree: ast.AST, lineno: int) -> str:
    name = "<module>"
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.lineno or 0) <= lineno <= (node.end_lineno or node.lineno):
                name = node.name
    return name


def _line_has_noqa(text: str, lineno: int) -> bool:
    lines = text.splitlines()
    if not (0 < lineno <= len(lines)):
        return False
    same = lines[lineno - 1]
    if _NOQA_RE.search(same):
        return True
    # 직전 줄
    if lineno >= 2 and _NOQA_RE.search(lines[lineno - 2]):
        return True
    return False


def audit_file(path: Path) -> tuple[list[Finding], Stats]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    stats = Stats(files_scanned=1)
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as e:
        findings.append(
            Finding(
                file=str(path),
                function="<module>",
                lineno=getattr(e, "lineno", 0) or 0,
                tables=[],
                severity="warn",
                reason=f"SyntaxError: {e.msg}",
                sql_excerpt="",
            )
        )
        stats.findings_warn += 1
        return findings, stats

    consts = _collect_module_str_constants(tree)
    for node, sql in _iter_sql_literals(tree, consts):
        stats.sql_literals += 1
        lineno = getattr(node, "lineno", 0) or 0
        fn_name = _enclosing_function(tree, lineno)
        tables = _FROM_TABLE_RE.findall(sql)
        multi, system, unknown = _classify_tables(tables)
        stats.multi_tenant_tables_seen.update(multi)

        excerpt = (sql[:200] + ("…" if len(sql) > 200 else "")).strip()

        if _line_has_noqa(text, lineno):
            stats.skipped_noqa += 1
            continue

        if not multi:
            # 시스템/unknown 만 있는 경우 — info 로 기록.
            if unknown:
                findings.append(
                    Finding(
                        file=str(path),
                        function=fn_name,
                        lineno=lineno,
                        tables=tables,
                        severity="info",
                        reason="unknown_tables_only",
                        sql_excerpt=excerpt,
                    )
                )
                stats.findings_info += 1
            continue

        # 다중 테넌트 테이블이 등장하는 SQL — Hcode 참조 검사.
        has_hcode = bool(_HCODE_REF_RE.search(sql))
        has_where = bool(_HAS_WHERE_RE.search(sql))
        if not has_hcode:
            severity = "warn" if has_where else "info"
            reason = (
                "missing_hcode_filter_on_multi_tenant_table"
                if has_where
                else "multi_tenant_table_no_where_clause"
            )
            findings.append(
                Finding(
                    file=str(path),
                    function=fn_name,
                    lineno=lineno,
                    tables=tables,
                    severity=severity,
                    reason=reason,
                    sql_excerpt=excerpt,
                )
            )
            if severity == "warn":
                stats.findings_warn += 1
            else:
                stats.findings_info += 1
    return findings, stats


def audit_dir(root: Path) -> dict[str, Any]:
    all_findings: list[Finding] = []
    agg = Stats()
    for p in sorted(root.glob("*.py")):
        if p.name.startswith("__"):
            continue
        findings, st = audit_file(p)
        all_findings.extend(findings)
        agg.files_scanned += st.files_scanned
        agg.sql_literals += st.sql_literals
        agg.findings_warn += st.findings_warn
        agg.findings_info += st.findings_info
        agg.skipped_noqa += st.skipped_noqa
        agg.multi_tenant_tables_seen.update(st.multi_tenant_tables_seen)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "files_scanned": agg.files_scanned,
            "sql_literals": agg.sql_literals,
            "warn": agg.findings_warn,
            "info": agg.findings_info,
            "skipped_noqa": agg.skipped_noqa,
            "multi_tenant_tables_seen": sorted(agg.multi_tenant_tables_seen),
        },
        "findings": [f.__dict__ for f in all_findings],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--root", default=str(DEFAULT_SERVICES_DIR))
    parser.add_argument("--json", default=str(DEFAULT_OUT))
    parser.add_argument(
        "--strict",
        action="store_true",
        help="warn > 0 시 exit 2 (PR/CI 가드용)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists():
        print(f"[ERR] root not found: {root}", file=sys.stderr)
        return 2
    report = audit_dir(root)

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {out}")
    s = report["summary"]
    print(
        f"  files={s['files_scanned']}  sql_literals={s['sql_literals']}  "
        f"warn={s['warn']}  info={s['info']}  skipped_noqa={s['skipped_noqa']}"
    )
    if args.strict and s["warn"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
