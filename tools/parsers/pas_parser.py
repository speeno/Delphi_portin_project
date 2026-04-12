"""
델파이 유닛 파일(.pas) 파서

.pas 파일에서 다음을 추출한다:
- uses 절 (interface/implementation 구분)
- 클래스/타입 선언
- 프로시저/함수 선언
- SQL 문자열 패턴
- 이벤트 핸들러 패턴
- 검증/유효성 검사 패턴
- 고객사 분기 패턴

사용법:
  python pas_parser.py <source_dir> <output_dir>
"""

import re
import json
import sys
import os
from pathlib import Path
from typing import Any


def find_pas_files(source_dir: str) -> list[str]:
    return sorted(str(p) for p in Path(source_dir).rglob("*.pas"))


def extract_uses(content: str, section: str) -> list[str]:
    """interface 또는 implementation의 uses 절에서 유닛 목록을 추출한다."""
    sec_pattern = re.compile(
        rf'\b{section}\b(.*?)(?:\bimplementation\b|\binitialization\b|\bfinalization\b|\bend\b\.)',
        re.DOTALL | re.IGNORECASE,
    )
    sec_match = sec_pattern.search(content)
    if not sec_match:
        return []

    uses_pattern = re.compile(r'\buses\b(.*?);', re.DOTALL | re.IGNORECASE)
    uses_match = uses_pattern.search(sec_match.group(1))
    if not uses_match:
        return []

    return [u.strip() for u in re.split(r'[,\s]+', uses_match.group(1)) if u.strip()]


def extract_sql(content: str) -> list[dict]:
    """SQL 문자열 패턴(SELECT, INSERT, UPDATE, DELETE, CALL)을 추출한다."""
    sql_patterns = [
        re.compile(r"'((?:SELECT|INSERT|UPDATE|DELETE|CALL)\b[^']*)'", re.IGNORECASE),
        re.compile(r"SQL\.(?:Text|Add)\s*(?::=|\()\s*'([^']*(?:SELECT|INSERT|UPDATE|DELETE|CALL)[^']*)'", re.IGNORECASE),
        re.compile(r"CommandText\s*:=\s*'([^']*(?:SELECT|INSERT|UPDATE|DELETE|CALL)[^']*)'", re.IGNORECASE),
    ]

    sqls = []
    seen = set()
    for pattern in sql_patterns:
        for m in pattern.finditer(content):
            sql = m.group(1).strip()
            normalized = re.sub(r'\s+', ' ', sql).upper()
            if normalized not in seen and len(sql) > 10:
                seen.add(normalized)
                sql_type = "UNKNOWN"
                for t in ["SELECT", "INSERT", "UPDATE", "DELETE", "CALL"]:
                    if normalized.startswith(t):
                        sql_type = t
                        break

                tables = extract_tables_from_sql(sql)
                sqls.append({
                    "sql": sql,
                    "type": sql_type,
                    "tables": tables,
                    "line": content[:m.start()].count("\n") + 1,
                })
    return sqls


def extract_tables_from_sql(sql: str) -> list[str]:
    """SQL에서 테이블 이름을 추출한다."""
    tables = set()
    patterns = [
        re.compile(r'\bFROM\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bJOIN\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bINTO\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bUPDATE\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bDELETE\s+FROM\s+(\w+)', re.IGNORECASE),
    ]
    for p in patterns:
        for m in p.finditer(sql):
            tables.add(m.group(1))
    return sorted(tables)


def extract_event_handlers(content: str) -> list[dict]:
    """이벤트 핸들러(OnClick, OnChange 등) 구현을 추출한다."""
    handler_pattern = re.compile(
        r'procedure\s+T(\w+)\.(\w+)\(([^)]*)\)\s*;',
        re.IGNORECASE,
    )
    handlers = []
    for m in handler_pattern.finditer(content):
        class_name = m.group(1)
        method_name = m.group(2)
        params = m.group(3).strip()

        event_type = "method"
        for prefix in ["btn", "Button"]:
            if prefix.lower() in method_name.lower() and "click" in method_name.lower():
                event_type = "button_click"
                break
        if "Change" in method_name:
            event_type = "change"
        elif "KeyPress" in method_name or "KeyDown" in method_name:
            event_type = "keypress"
        elif "DblClick" in method_name:
            event_type = "double_click"
        elif "Enter" in method_name:
            event_type = "enter"
        elif "Exit" in method_name:
            event_type = "exit"
        elif "Timer" in method_name:
            event_type = "timer"

        handlers.append({
            "class": class_name,
            "method": method_name,
            "params": params,
            "event_type": event_type,
            "line": content[:m.start()].count("\n") + 1,
        })
    return handlers


def extract_validation_patterns(content: str) -> list[dict]:
    """검증/유효성 검사 패턴을 추출한다."""
    validations = []

    msg_patterns = [
        re.compile(r"(ShowMessage|MessageDlg|Application\.MessageBox)\s*\(\s*'([^']*)'", re.IGNORECASE),
        re.compile(r'raise\s+Exception\.Create\s*\(\s*\'([^\']*)\'\s*\)', re.IGNORECASE),
    ]

    for pattern in msg_patterns:
        for m in pattern.finditer(content):
            msg = m.group(2) if m.lastindex >= 2 else m.group(1)
            validations.append({
                "type": "message" if "Message" in m.group(0) else "exception",
                "message": msg,
                "line": content[:m.start()].count("\n") + 1,
            })

    check_patterns = re.compile(
        r'if\s+.*(?:Trim|IsEmpty|Length|= \'\').*then\b',
        re.IGNORECASE,
    )
    for m in check_patterns.finditer(content):
        validations.append({
            "type": "empty_check",
            "code": m.group(0).strip()[:120],
            "line": content[:m.start()].count("\n") + 1,
        })

    return validations


def extract_customer_variants(content: str) -> list[dict]:
    """고객사별 분기 패턴을 추출한다."""
    variants = []

    patterns = [
        re.compile(r"(?:if|case)\s+.*(?:customer|client|고객|거래처|company)\w*\s*(?:=|:)\s*'?(\w+)'?", re.IGNORECASE),
        re.compile(r"(?:if|case)\s+.*(?:site|센터|현장|warehouse)\w*\s*(?:=|:)\s*'?(\w+)'?", re.IGNORECASE),
    ]

    for pattern in patterns:
        for m in pattern.finditer(content):
            variants.append({
                "variant_value": m.group(1) if m.lastindex else "",
                "code": m.group(0).strip()[:150],
                "line": content[:m.start()].count("\n") + 1,
            })

    return variants


def classify_unit(filepath: str, content: str) -> str:
    """유닛의 유형을 분류한다."""
    lower_path = filepath.lower()
    lower_content = content.lower()

    if "tdatamodule" in lower_content or "tadoquery" in lower_content or "tfdquery" in lower_content:
        return "data_module"
    if "tform" in lower_content:
        return "form"
    if "tframe" in lower_content:
        return "frame"
    if re.search(r'\b(report|rpt|print)\b', lower_path, re.IGNORECASE):
        return "report"
    if re.search(r'\b(common|util|lib|shared)\b', lower_path, re.IGNORECASE):
        return "common"
    if re.search(r'\b(batch|scheduler|job)\b', lower_path, re.IGNORECASE):
        return "batch"
    if re.search(r'\b(scan|print|label|device|serial|com\d)\b', lower_path, re.IGNORECASE):
        return "device"
    return "unit"


def parse_pas_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    unit_match = re.search(r'\bunit\s+(\w+)\s*;', content, re.IGNORECASE)
    unit_name = unit_match.group(1) if unit_match else Path(filepath).stem

    interface_uses = extract_uses(content, "interface")
    implementation_uses = extract_uses(content, "implementation")
    sqls = extract_sql(content)
    handlers = extract_event_handlers(content)
    validations = extract_validation_patterns(content)
    variants = extract_customer_variants(content)
    unit_type = classify_unit(filepath, content)

    return {
        "file": filepath,
        "unit_name": unit_name,
        "unit_type": unit_type,
        "line_count": content.count("\n") + 1,
        "file_size": os.path.getsize(filepath),
        "interface_uses": interface_uses,
        "implementation_uses": implementation_uses,
        "sql_count": len(sqls),
        "sqls": sqls,
        "event_handler_count": len(handlers),
        "event_handlers": handlers,
        "validation_count": len(validations),
        "validations": validations,
        "customer_variant_count": len(variants),
        "customer_variants": variants,
    }


def build_unit_dependency_graph(results: list[dict]) -> dict:
    nodes = set()
    edges = []

    for r in results:
        name = r["unit_name"]
        nodes.add(name)
        for dep in r["interface_uses"] + r["implementation_uses"]:
            nodes.add(dep)
            edges.append({"from": name, "to": dep, "type": "uses"})

    return {
        "nodes": sorted(nodes),
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
    }


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    pas_files = find_pas_files(source_dir)
    if not pas_files:
        print(f"No .pas files found in {source_dir}")
        sys.exit(0)

    print(f"Parsing {len(pas_files)} .pas files...")
    results = []
    for i, f in enumerate(pas_files, 1):
        try:
            results.append(parse_pas_file(f))
        except Exception as e:
            print(f"  Error parsing {f}: {e}")
        if i % 50 == 0:
            print(f"  Processed {i}/{len(pas_files)}...")

    dep_graph = build_unit_dependency_graph(results)

    inventory_path = os.path.join(output_dir, "pas_inventory.json")
    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    dep_path = os.path.join(output_dir, "unit_dependency_graph.json")
    with open(dep_path, "w", encoding="utf-8") as f:
        json.dump(dep_graph, f, ensure_ascii=False, indent=2)

    all_sqls = []
    for r in results:
        for sql in r["sqls"]:
            all_sqls.append({
                "unit": r["unit_name"],
                "file": r["file"],
                **sql,
            })
    sql_path = os.path.join(output_dir, "query_catalog.json")
    with open(sql_path, "w", encoding="utf-8") as f:
        json.dump(all_sqls, f, ensure_ascii=False, indent=2)

    all_validations = []
    for r in results:
        for v in r["validations"]:
            all_validations.append({
                "unit": r["unit_name"],
                "file": r["file"],
                **v,
            })
    val_path = os.path.join(output_dir, "validation_rules.json")
    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(all_validations, f, ensure_ascii=False, indent=2)

    all_variants = []
    for r in results:
        for v in r["customer_variants"]:
            all_variants.append({
                "unit": r["unit_name"],
                "file": r["file"],
                **v,
            })
    var_path = os.path.join(output_dir, "customer_variants.json")
    with open(var_path, "w", encoding="utf-8") as f:
        json.dump(all_variants, f, ensure_ascii=False, indent=2)

    type_counts: dict[str, int] = {}
    for r in results:
        t = r["unit_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    summary = {
        "total_pas_files": len(results),
        "total_lines": sum(r["line_count"] for r in results),
        "unit_types": type_counts,
        "total_sqls": len(all_sqls),
        "total_event_handlers": sum(r["event_handler_count"] for r in results),
        "total_validations": len(all_validations),
        "total_customer_variants": len(all_variants),
        "dependency_graph_nodes": dep_graph["total_nodes"],
        "dependency_graph_edges": dep_graph["total_edges"],
    }

    summary_path = os.path.join(output_dir, "analysis_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nAnalysis complete:")
    print(f"  PAS files: {summary['total_pas_files']}")
    print(f"  Total lines: {summary['total_lines']}")
    print(f"  SQL queries: {summary['total_sqls']}")
    print(f"  Event handlers: {summary['total_event_handlers']}")
    print(f"  Validations: {summary['total_validations']}")
    print(f"  Customer variants: {summary['total_customer_variants']}")
    print(f"\nOutputs: {output_dir}/")


if __name__ == "__main__":
    main()
