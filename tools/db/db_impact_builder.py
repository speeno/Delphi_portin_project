"""
DB Impact Matrix 빌더 (산출물 #4)

SQL Catalog(산출물 #3)의 결과와 DB 스키마 정보를 결합하여
폼/이벤트별 DB 영향도 매트릭스를 생성한다.

사용법:
  python db_impact_builder.py <analysis_dir> <output_path>
"""

import json
import sys
import os


def load_json(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_impact_matrix(analysis_dir: str) -> dict:
    query_catalog = load_json(os.path.join(analysis_dir, "query_catalog.json"))
    event_flow = load_json(os.path.join(analysis_dir, "event_flow.json"))

    table_impact: dict[str, dict] = {}

    for sql_entry in query_catalog:
        tables = sql_entry.get("tables", [])
        sql_type = sql_entry.get("type", "UNKNOWN")
        unit = sql_entry.get("unit", "")

        for table in tables:
            if table not in table_impact:
                table_impact[table] = {
                    "table_name": table,
                    "operations": {"SELECT": 0, "INSERT": 0, "UPDATE": 0, "DELETE": 0, "CALL": 0},
                    "accessed_by_units": [],
                    "accessed_by_forms": [],
                    "total_references": 0,
                    "has_write": False,
                }

            if sql_type in table_impact[table]["operations"]:
                table_impact[table]["operations"][sql_type] += 1
            table_impact[table]["total_references"] += 1

            if sql_type in ("INSERT", "UPDATE", "DELETE"):
                table_impact[table]["has_write"] = True

            if unit and unit not in table_impact[table]["accessed_by_units"]:
                table_impact[table]["accessed_by_units"].append(unit)

    form_handlers = {}
    for evt in event_flow:
        form = evt.get("form", "")
        handler = evt.get("handler", "")
        if form:
            form_handlers.setdefault(form, []).append(handler)

    unit_form_map = {}
    pas_inventory = load_json(os.path.join(analysis_dir, "pas_inventory.json"))
    for pas in pas_inventory:
        unit_name = pas.get("unit_name", "")
        for eh in pas.get("event_handlers", []):
            class_name = eh.get("class", "")
            if class_name:
                unit_form_map[unit_name] = class_name

    for table_name, info in table_impact.items():
        for unit in info["accessed_by_units"]:
            form = unit_form_map.get(unit, "")
            if form and form not in info["accessed_by_forms"]:
                info["accessed_by_forms"].append(form)

    crud_matrix = []
    for table_name, info in sorted(table_impact.items()):
        ops = info["operations"]
        crud_matrix.append({
            "table": table_name,
            "C": ops["INSERT"],
            "R": ops["SELECT"],
            "U": ops["UPDATE"],
            "D": ops["DELETE"],
            "total": info["total_references"],
            "write_access": info["has_write"],
            "forms": info["accessed_by_forms"],
            "units": info["accessed_by_units"],
        })

    return {
        "table_details": table_impact,
        "crud_matrix": crud_matrix,
        "summary": {
            "total_tables": len(table_impact),
            "tables_with_write": sum(1 for t in table_impact.values() if t["has_write"]),
            "total_sql_references": sum(t["total_references"] for t in table_impact.values()),
        },
    }


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <analysis_dir> <output_path>")
        sys.exit(1)

    analysis_dir = sys.argv[1]
    output_path = sys.argv[2]

    matrix = build_impact_matrix(analysis_dir)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)

    print(f"DB Impact Matrix: {output_path}")
    print(f"  Tables: {matrix['summary']['total_tables']}")
    print(f"  Tables with write: {matrix['summary']['tables_with_write']}")
    print(f"  Total SQL references: {matrix['summary']['total_sql_references']}")


if __name__ == "__main__":
    main()
