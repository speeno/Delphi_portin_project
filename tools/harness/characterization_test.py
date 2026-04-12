"""
Characterization Test 생성기

캡처된 쿼리 데이터(Capture Harness)에서
SQL의 입력-출력 쌍을 테스트 케이스로 변환한다.

"현재 시스템이 이렇게 동작한다"를 기록하여
신규 시스템의 회귀를 감지하는 테스트를 자동 생성한다.

사용법:
  python characterization_test.py <captured_queries.json> <output_dir>
"""

import json
import sys
import os
import re
from datetime import datetime


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_session(queries: list[dict]) -> dict[str, list[dict]]:
    """쿼리를 세션(connection_id)별로 그룹화한다."""
    sessions: dict[str, list[dict]] = {}
    for q in queries:
        conn_id = str(q.get("connection_id", q.get("thread_id", "unknown")))
        sessions.setdefault(conn_id, []).append(q)
    return sessions


def identify_workflows(session_queries: list[dict]) -> list[dict]:
    """세션 내 쿼리를 업무 흐름 단위로 분리한다."""
    workflows = []
    current = []
    last_type = None

    for q in session_queries:
        qtype = q.get("type", "")

        if qtype == "BEGIN" or (not current and qtype in ("INSERT", "UPDATE", "DELETE")):
            if current:
                workflows.append(current)
            current = [q]
        elif qtype == "COMMIT" or qtype == "ROLLBACK":
            current.append(q)
            workflows.append(current)
            current = []
        else:
            current.append(q)

        last_type = qtype

    if current:
        workflows.append(current)

    return workflows


def generate_test_from_workflow(workflow: list[dict], index: int) -> dict | None:
    """업무 흐름에서 Characterization Test를 생성한다."""
    writes = [q for q in workflow if q.get("type") in ("INSERT", "UPDATE", "DELETE")]
    reads = [q for q in workflow if q.get("type") == "SELECT"]

    if not writes and not reads:
        return None

    all_tables = set()
    for q in workflow:
        for t in q.get("tables", []):
            all_tables.add(t)

    test = {
        "test_id": f"char-test-{index:04d}",
        "type": "characterization",
        "generated_at": datetime.now().isoformat(),
        "description": f"캡처된 업무 흐름 #{index} 재현 테스트",
        "workflow": {
            "total_queries": len(workflow),
            "reads": len(reads),
            "writes": len(writes),
            "tables": sorted(all_tables),
        },
        "queries": [
            {
                "sql": q.get("sql", q.get("normalized", "")),
                "type": q.get("type", ""),
                "tables": q.get("tables", []),
            }
            for q in workflow
        ],
        "assertions": [],
    }

    for w in writes:
        sql_type = w.get("type", "")
        for table in w.get("tables", []):
            if sql_type == "INSERT":
                test["assertions"].append({
                    "type": "db_delta",
                    "table": table,
                    "expected": "row_inserted",
                })
            elif sql_type == "UPDATE":
                test["assertions"].append({
                    "type": "db_delta",
                    "table": table,
                    "expected": "row_updated",
                })
            elif sql_type == "DELETE":
                test["assertions"].append({
                    "type": "db_delta",
                    "table": table,
                    "expected": "row_deleted",
                })

    if not writes:
        for r in reads:
            for table in r.get("tables", []):
                test["assertions"].append({
                    "type": "result_count",
                    "table": table,
                    "expected": "non_empty",
                })

    return test


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <captured_queries.json> <output_dir>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    queries = load_json(input_path)
    sessions = group_by_session(queries)

    all_tests = []
    test_index = 1

    for session_id, session_queries in sessions.items():
        workflows = identify_workflows(session_queries)
        for wf in workflows:
            test = generate_test_from_workflow(wf, test_index)
            if test:
                all_tests.append(test)
                test_index += 1

    output_path = os.path.join(output_dir, "characterization_tests.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_tests, f, ensure_ascii=False, indent=2)

    summary = {
        "total_tests": len(all_tests),
        "total_sessions": len(sessions),
        "total_assertions": sum(len(t["assertions"]) for t in all_tests),
        "test_types": {
            "with_writes": sum(1 for t in all_tests if t["workflow"]["writes"] > 0),
            "read_only": sum(1 for t in all_tests if t["workflow"]["writes"] == 0),
        },
    }

    summary_path = os.path.join(output_dir, "char_test_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(all_tests)} Characterization Tests -> {output_dir}")
    print(f"  With writes: {summary['test_types']['with_writes']}")
    print(f"  Read-only: {summary['test_types']['read_only']}")
    print(f"  Total assertions: {summary['total_assertions']}")


if __name__ == "__main__":
    main()
