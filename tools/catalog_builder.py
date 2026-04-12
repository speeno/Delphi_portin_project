"""
Legacy Object Catalog 빌더

정적 분석(L2) 결과를 통합하여 Legacy Object Catalog를 생성한다.
.pas 파서 결과(이벤트 핸들러, SQL, 검증, 고객사 분기)와
.dfm 파서 결과(폼-이벤트 바인딩)를 결합하여
각 이벤트 핸들러를 하나의 Legacy Object로 매핑한다.

사용법:
  python catalog_builder.py <analysis_dir> <output_path>
"""

import json
import sys
import os


def load_json(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_catalog(analysis_dir: str) -> list[dict]:
    """분석 결과를 통합하여 Legacy Object Catalog를 생성한다."""

    event_flow = load_json(os.path.join(analysis_dir, "event_flow.json"))
    query_catalog = load_json(os.path.join(analysis_dir, "query_catalog.json"))
    validation_rules = load_json(os.path.join(analysis_dir, "validation_rules.json"))
    customer_variants = load_json(os.path.join(analysis_dir, "customer_variants.json"))
    pas_inventory = load_json(os.path.join(analysis_dir, "pas_inventory.json"))

    pas_map = {}
    for pas in pas_inventory:
        unit_name = pas.get("unit_name", "")
        pas_map[unit_name] = pas

    handler_map: dict[str, dict] = {}
    for evt in event_flow:
        form = evt.get("form", "")
        handler = evt.get("handler", "")
        if not handler:
            continue

        object_id = f"{form}.{handler}"
        if object_id not in handler_map:
            handler_map[object_id] = {
                "object_id": object_id,
                "type": "event_handler",
                "form": form,
                "form_class": evt.get("form_class", ""),
                "component": evt.get("component", ""),
                "component_type": evt.get("component_type", ""),
                "event": evt.get("event", ""),
                "handler_name": handler,
                "unit": "",
                "depends_on": [],
                "touches_tables": [],
                "sql_queries": [],
                "validations": [],
                "customer_variants": [],
                "risk_level": "low",
            }

    for pas in pas_inventory:
        unit = pas.get("unit_name", "")
        for eh in pas.get("event_handlers", []):
            class_name = eh.get("class", "")
            method = eh.get("method", "")
            object_id = f"{class_name}.{method}"

            if object_id not in handler_map:
                handler_map[object_id] = {
                    "object_id": object_id,
                    "type": "event_handler",
                    "form": class_name,
                    "form_class": "",
                    "component": "",
                    "component_type": "",
                    "event": eh.get("event_type", ""),
                    "handler_name": method,
                    "unit": pas.get("file", ""),
                    "depends_on": [],
                    "touches_tables": [],
                    "sql_queries": [],
                    "validations": [],
                    "customer_variants": [],
                    "risk_level": "low",
                }
            else:
                handler_map[object_id]["unit"] = pas.get("file", "")

            for dep in pas.get("interface_uses", []) + pas.get("implementation_uses", []):
                if dep not in handler_map[object_id]["depends_on"]:
                    handler_map[object_id]["depends_on"].append(dep)

    for sql_entry in query_catalog:
        unit = sql_entry.get("unit", "")
        tables = sql_entry.get("tables", [])

        for oid, obj in handler_map.items():
            if unit and unit in obj.get("unit", ""):
                obj["sql_queries"].append({
                    "sql": sql_entry.get("sql", ""),
                    "type": sql_entry.get("type", ""),
                })
                for t in tables:
                    if t not in obj["touches_tables"]:
                        obj["touches_tables"].append(t)

    for val in validation_rules:
        unit = val.get("unit", "")
        for oid, obj in handler_map.items():
            if unit and unit in obj.get("unit", ""):
                obj["validations"].append({
                    "type": val.get("type", ""),
                    "message": val.get("message", val.get("code", "")),
                })

    for var in customer_variants:
        unit = var.get("unit", "")
        for oid, obj in handler_map.items():
            if unit and unit in obj.get("unit", ""):
                variant_value = var.get("variant_value", "")
                if variant_value and variant_value not in obj["customer_variants"]:
                    obj["customer_variants"].append(variant_value)

    for obj in handler_map.values():
        risk = "low"
        if obj["customer_variants"]:
            risk = "medium"
        if len(obj["touches_tables"]) > 2:
            risk = "medium"
        has_write = any(
            s.get("type") in ("INSERT", "UPDATE", "DELETE")
            for s in obj["sql_queries"]
        )
        if has_write:
            risk = "high"
        if has_write and obj["customer_variants"]:
            risk = "critical"
        obj["risk_level"] = risk

    return sorted(handler_map.values(), key=lambda x: x["object_id"])


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <analysis_dir> <output_path>")
        sys.exit(1)

    analysis_dir = sys.argv[1]
    output_path = sys.argv[2]

    catalog = build_catalog(analysis_dir)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    risk_counts = {}
    for obj in catalog:
        r = obj["risk_level"]
        risk_counts[r] = risk_counts.get(r, 0) + 1

    print(f"Legacy Object Catalog built: {len(catalog)} objects -> {output_path}")
    print(f"  Risk distribution: {risk_counts}")
    print(f"  Objects with SQL: {sum(1 for o in catalog if o['sql_queries'])}")
    print(f"  Objects with variants: {sum(1 for o in catalog if o['customer_variants'])}")
    print(f"  Objects with validations: {sum(1 for o in catalog if o['validations'])}")


if __name__ == "__main__":
    main()
