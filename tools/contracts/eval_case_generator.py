"""
Eval Case 생성기 (L7 평가)

Migration Contract와 Legacy Object Catalog를 기반으로
각 계약에 대한 Eval Case(평가 케이스)를 자동 생성한다.

5축 평가 체계:
- Outcome: DB delta 비교
- Process: validation 수행 여부
- UI/UX: 메시지/상태 일치
- Efficiency: 응답 시간/쿼리 수
- Variant: 고객사별 분기 테스트

사용법:
  python eval_case_generator.py <catalog_path> <contracts_dir> <output_dir>
"""

import json
import sys
import os
import re
from datetime import datetime


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_outcome_cases(obj: dict, contract_id: str) -> list[dict]:
    """Outcome eval: DB delta 기반 테스트 케이스 생성"""
    cases = []
    tables = obj.get("touches_tables", [])
    sql_queries = obj.get("sql_queries", [])

    write_ops = [s for s in sql_queries if s.get("type") in ("INSERT", "UPDATE", "DELETE")]
    if not write_ops:
        cases.append({
            "eval_id": f"{contract_id}-outcome-readonly-001",
            "eval_axis": "outcome",
            "description": "읽기 전용 동작 - DB 변경 없음 확인",
            "input": {"_comment": "기본 조회 파라미터를 채워 넣으세요"},
            "expected_db_delta": {t: "no change" for t in tables},
            "expected_response": {"success": True},
            "variant": "default",
        })
    else:
        for i, op in enumerate(write_ops, 1):
            sql_type = op.get("type", "")
            delta = {}
            sql_text = op.get("sql", "")
            op_tables = set()
            for p in [re.compile(r'\bINTO\s+(\w+)', re.I), re.compile(r'\bUPDATE\s+(\w+)', re.I), re.compile(r'\bFROM\s+(\w+)', re.I)]:
                for m in p.finditer(sql_text):
                    op_tables.add(m.group(1))

            for t in op_tables:
                if sql_type == "INSERT":
                    delta[t] = "+1 row"
                elif sql_type == "UPDATE":
                    delta[t] = "row(s) updated"
                elif sql_type == "DELETE":
                    delta[t] = "-1 row"

            cases.append({
                "eval_id": f"{contract_id}-outcome-{sql_type.lower()}-{i:03d}",
                "eval_axis": "outcome",
                "description": f"{sql_type} 동작 - DB delta 확인",
                "input": {"_comment": f"{sql_type} 테스트 데이터를 채워 넣으세요"},
                "expected_db_delta": delta,
                "expected_response": {"success": True},
                "variant": "default",
            })

    return cases


def generate_process_cases(obj: dict, contract_id: str) -> list[dict]:
    """Process eval: validation 수행, 트랜잭션 경계 검증"""
    cases = []
    validations = obj.get("validations", [])

    for i, v in enumerate(validations[:5], 1):
        cases.append({
            "eval_id": f"{contract_id}-process-validation-{i:03d}",
            "eval_axis": "process",
            "description": f"필수 검증 수행 확인: {v.get('message', v.get('type', ''))}",
            "input": {"_comment": "검증 실패 조건의 입력 데이터를 채워 넣으세요"},
            "expected_response": {"success": False},
            "expected_messages": [v.get("message", "")],
            "variant": "default",
        })

    if obj.get("sql_queries"):
        cases.append({
            "eval_id": f"{contract_id}-process-tx-001",
            "eval_axis": "process",
            "description": "트랜잭션 경계 검증 - 실패 시 전체 롤백 확인",
            "input": {"_comment": "중간 단계에서 실패하는 데이터를 채워 넣으세요"},
            "expected_db_delta": {t: "no change (rolled back)" for t in obj.get("touches_tables", [])},
            "expected_response": {"success": False},
            "variant": "default",
        })

    return cases


def generate_variant_cases(obj: dict, contract_id: str) -> list[dict]:
    """Variant eval: 고객사별 분기 테스트"""
    cases = []
    variants = obj.get("customer_variants", [])

    for v in variants:
        cases.append({
            "eval_id": f"{contract_id}-variant-{v.lower()}-001",
            "eval_axis": "variant",
            "description": f"고객사 {v} 전용 분기 동작 확인",
            "input": {"customer": v, "_comment": f"고객사 {v}의 테스트 데이터를 채워 넣으세요"},
            "expected_db_delta": {},
            "expected_response": {"success": True},
            "variant": v,
        })

    return cases


def generate_efficiency_case(obj: dict, contract_id: str) -> list[dict]:
    """Efficiency eval: 응답 시간, 쿼리 수 검증"""
    return [{
        "eval_id": f"{contract_id}-efficiency-001",
        "eval_axis": "efficiency",
        "description": "응답 시간 및 쿼리 수 검증",
        "input": {"_comment": "일반적인 입력 데이터를 채워 넣으세요"},
        "expected_max_response_ms": 1500,
        "expected_max_queries": len(obj.get("sql_queries", [])) + 2,
        "variant": "default",
    }]


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <catalog_path> <contracts_dir> <output_dir>")
        sys.exit(1)

    catalog_path = sys.argv[1]
    contracts_dir = sys.argv[2]
    output_dir = sys.argv[3]
    os.makedirs(output_dir, exist_ok=True)

    catalog = load_json(catalog_path)

    catalog_map = {obj["object_id"]: obj for obj in catalog}

    total_cases = 0
    axis_counts = {"outcome": 0, "process": 0, "variant": 0, "efficiency": 0}

    for obj in catalog:
        if not obj.get("sql_queries") and not obj.get("validations"):
            continue

        contract_id = f"api.{obj['form']}.{obj['handler_name']}".lower()

        all_cases = []
        all_cases.extend(generate_outcome_cases(obj, contract_id))
        all_cases.extend(generate_process_cases(obj, contract_id))
        all_cases.extend(generate_variant_cases(obj, contract_id))
        all_cases.extend(generate_efficiency_case(obj, contract_id))

        if all_cases:
            filename = contract_id.replace(".", "_") + "_eval.json"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(all_cases, f, ensure_ascii=False, indent=2)
            total_cases += len(all_cases)

            for c in all_cases:
                axis = c.get("eval_axis", "")
                if axis in axis_counts:
                    axis_counts[axis] += 1

    print(f"Generated {total_cases} Eval Cases -> {output_dir}")
    print(f"  By axis: {axis_counts}")


if __name__ == "__main__":
    main()
