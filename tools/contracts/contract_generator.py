"""
Migration Contract 생성기 (L3 작업 분해)

Legacy Object Catalog의 이벤트 핸들러를 분석하여
각 기능에 대한 Migration Contract(API 계약)를 자동 생성한다.

입력: Legacy Object Catalog + Feature Input Template
출력: migration/contracts/*.yaml

사용법:
  python contract_generator.py <catalog_path> <output_dir>
"""

import json
import sys
import os
import re
from datetime import datetime


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_api_path(form: str, handler: str) -> str:
    """폼명과 핸들러명에서 RESTful API 경로를 생성한다."""
    form_clean = re.sub(r'^(frm|form|dlg)', '', form, flags=re.IGNORECASE)
    form_clean = re.sub(r'([A-Z])', r'-\1', form_clean).strip('-').lower()

    action = "unknown"
    handler_lower = handler.lower()
    if "save" in handler_lower or "insert" in handler_lower or "add" in handler_lower or "create" in handler_lower:
        action = "create"
    elif "update" in handler_lower or "edit" in handler_lower or "modify" in handler_lower:
        action = "update"
    elif "delete" in handler_lower or "remove" in handler_lower or "cancel" in handler_lower:
        action = "delete"
    elif "search" in handler_lower or "find" in handler_lower or "query" in handler_lower or "list" in handler_lower:
        action = "list"
    elif "click" in handler_lower:
        btn_name = re.sub(r'click$', '', handler_lower, flags=re.IGNORECASE)
        btn_name = re.sub(r'^btn', '', btn_name, flags=re.IGNORECASE)
        action = btn_name or "action"
    elif "print" in handler_lower or "report" in handler_lower:
        action = "print"

    return f"/api/{form_clean}/{action}"


def infer_http_method(handler: str, sql_types: list[str]) -> str:
    handler_lower = handler.lower()
    if any(t in ("INSERT",) for t in sql_types) or "save" in handler_lower or "create" in handler_lower or "add" in handler_lower:
        return "POST"
    if any(t in ("UPDATE",) for t in sql_types) or "update" in handler_lower or "edit" in handler_lower:
        return "PUT"
    if any(t in ("DELETE",) for t in sql_types) or "delete" in handler_lower or "remove" in handler_lower:
        return "DELETE"
    return "GET"


def generate_contract(obj: dict) -> dict:
    """Legacy Object에서 Migration Contract를 생성한다."""
    form = obj.get("form", "")
    handler = obj.get("handler_name", "")
    sql_types = [s.get("type", "") for s in obj.get("sql_queries", [])]

    contract_id = f"api.{form}.{handler}".lower().replace(" ", "_")
    api_path = generate_api_path(form, handler)
    method = infer_http_method(handler, sql_types)

    side_effects = []
    for sql in obj.get("sql_queries", []):
        sql_type = sql.get("type", "")
        if sql_type in ("INSERT", "UPDATE", "DELETE"):
            tables = set()
            for p in [re.compile(r'\bINTO\s+(\w+)', re.I), re.compile(r'\bUPDATE\s+(\w+)', re.I), re.compile(r'\bFROM\s+(\w+)', re.I)]:
                for m in p.finditer(sql.get("sql", "")):
                    tables.add(m.group(1))
            for t in tables:
                effect = f"{sql_type.lower()} {t}"
                if effect not in side_effects:
                    side_effects.append(effect)

    validation_rules = []
    for v in obj.get("validations", []):
        validation_rules.append({
            "type": v.get("type", ""),
            "message": v.get("message", ""),
        })

    return {
        "contract_id": contract_id,
        "legacy_source": [obj.get("object_id", "")],
        "api_path": api_path,
        "http_method": method,
        "description": f"{form}의 {handler} 동작을 웹 API로 구현",
        "request_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "response_schema": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "data": {"type": "object"},
            },
        },
        "validation_rules": validation_rules,
        "side_effects": side_effects,
        "tables_affected": obj.get("touches_tables", []),
        "customer_variants": obj.get("customer_variants", []),
        "risk_level": obj.get("risk_level", "low"),
        "equivalence_tests": [],
        "created_at": datetime.now().isoformat(),
        "status": "draft",
    }


def save_as_yaml(contract: dict, output_dir: str):
    """계약을 YAML 형식으로 저장한다."""
    filename = contract["contract_id"].replace(".", "_") + ".yaml"
    filepath = os.path.join(output_dir, filename)

    lines = []
    lines.append(f"contract_id: {contract['contract_id']}")
    lines.append(f"api_path: {contract['api_path']}")
    lines.append(f"http_method: {contract['http_method']}")
    lines.append(f"description: \"{contract['description']}\"")
    lines.append(f"risk_level: {contract['risk_level']}")
    lines.append(f"status: {contract['status']}")
    lines.append(f"created_at: {contract['created_at']}")
    lines.append("")
    lines.append("legacy_source:")
    for s in contract["legacy_source"]:
        lines.append(f"  - \"{s}\"")
    lines.append("")
    lines.append("tables_affected:")
    for t in contract["tables_affected"]:
        lines.append(f"  - {t}")
    lines.append("")
    lines.append("side_effects:")
    for e in contract["side_effects"]:
        lines.append(f"  - \"{e}\"")
    lines.append("")
    lines.append("validation_rules:")
    for v in contract["validation_rules"]:
        lines.append(f"  - type: {v['type']}")
        lines.append(f"    message: \"{v['message']}\"")
    lines.append("")
    lines.append("customer_variants:")
    for cv in contract["customer_variants"]:
        lines.append(f"  - {cv}")
    lines.append("")
    lines.append("equivalence_tests: []")
    lines.append("")
    lines.append("request_schema:")
    lines.append("  type: object")
    lines.append("  properties: {}")
    lines.append("  required: []")
    lines.append("")
    lines.append("response_schema:")
    lines.append("  type: object")
    lines.append("  properties:")
    lines.append("    success: { type: boolean }")
    lines.append("    message: { type: string }")
    lines.append("    data: { type: object }")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return filepath


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <catalog_path> <output_dir>")
        sys.exit(1)

    catalog_path = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    catalog = load_json(catalog_path)

    high_risk = [o for o in catalog if o.get("risk_level") in ("high", "critical")]
    medium_risk = [o for o in catalog if o.get("risk_level") == "medium"]
    low_risk = [o for o in catalog if o.get("risk_level") == "low"]

    priority_order = high_risk + medium_risk + low_risk

    contracts = []
    for obj in priority_order:
        if not obj.get("sql_queries") and not obj.get("validations"):
            continue

        contract = generate_contract(obj)
        filepath = save_as_yaml(contract, output_dir)
        contracts.append(contract)

    summary_path = os.path.join(output_dir, "_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_contracts": len(contracts),
            "by_method": {m: sum(1 for c in contracts if c["http_method"] == m) for m in ("GET", "POST", "PUT", "DELETE")},
            "by_risk": {r: sum(1 for c in contracts if c["risk_level"] == r) for r in ("critical", "high", "medium", "low")},
        }, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(contracts)} Migration Contracts -> {output_dir}")
    print(f"  By method: GET={sum(1 for c in contracts if c['http_method']=='GET')}, POST={sum(1 for c in contracts if c['http_method']=='POST')}, PUT={sum(1 for c in contracts if c['http_method']=='PUT')}, DELETE={sum(1 for c in contracts if c['http_method']=='DELETE')}")


if __name__ == "__main__":
    main()
