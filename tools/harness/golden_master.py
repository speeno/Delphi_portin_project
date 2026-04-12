"""
Golden Master / Test Harness (L7 평가 PoC)

기존 시스템(델파이)에서 업무 흐름을 실행하여
DB 변경 전/후 스냅샷을 캡처하고,
신규 시스템(웹 API)의 결과와 자동 비교한다.

기능:
1. DB 스냅샷 캡처 (특정 테이블의 특정 조건 레코드)
2. 스냅샷 비교 (row-level diff)
3. 비교 결과 리포트 생성

사용법:
  python golden_master.py capture --config <config.json> --output <snapshot.json>
  python golden_master.py compare --before <before.json> --after <after.json> --expected <expected.json> --output <report.json>

의존성:
  pip install mysql-connector-python
"""

import json
import sys
import os
import argparse
from datetime import datetime


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def capture_snapshot(config: dict) -> dict:
    """DB 스냅샷을 캡처한다."""
    try:
        import mysql.connector
    except ImportError:
        print("Error: mysql-connector-python 필요")
        sys.exit(1)

    db_config = config.get("database", {})
    conn = mysql.connector.connect(
        host=db_config.get("host", "localhost"),
        port=db_config.get("port", 3306),
        user=db_config.get("user", "root"),
        password=db_config.get("password", ""),
        database=db_config.get("database", ""),
    )
    cursor = conn.cursor(dictionary=True)

    snapshot = {
        "captured_at": datetime.now().isoformat(),
        "database": db_config.get("database", ""),
        "tables": {},
    }

    for table_config in config.get("tables", []):
        table_name = table_config["name"]
        where = table_config.get("where", "1=1")
        order_by = table_config.get("order_by", "")
        limit = table_config.get("limit", 1000)

        query = f"SELECT * FROM {table_name} WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        query += f" LIMIT {limit}"

        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            for k, v in row.items():
                if isinstance(v, (bytes, bytearray)):
                    row[k] = v.hex()
                elif hasattr(v, 'isoformat'):
                    row[k] = v.isoformat()
                elif isinstance(v, set):
                    row[k] = list(v)

        snapshot["tables"][table_name] = {
            "row_count": len(rows),
            "rows": rows,
        }

    cursor.close()
    conn.close()
    return snapshot


def compare_snapshots(before: dict, after: dict, expected_delta: dict | None = None) -> dict:
    """두 스냅샷을 비교한다."""
    report = {
        "compared_at": datetime.now().isoformat(),
        "tables": {},
        "summary": {
            "total_tables": 0,
            "tables_changed": 0,
            "rows_added": 0,
            "rows_removed": 0,
            "rows_modified": 0,
            "match": True,
        },
    }

    all_tables = set(list(before.get("tables", {}).keys()) + list(after.get("tables", {}).keys()))
    report["summary"]["total_tables"] = len(all_tables)

    for table in all_tables:
        before_data = before.get("tables", {}).get(table, {"rows": [], "row_count": 0})
        after_data = after.get("tables", {}).get(table, {"rows": [], "row_count": 0})

        before_rows = before_data.get("rows", [])
        after_rows = after_data.get("rows", [])

        added = max(0, len(after_rows) - len(before_rows))
        removed = max(0, len(before_rows) - len(after_rows))

        before_set = {json.dumps(r, sort_keys=True, default=str) for r in before_rows}
        after_set = {json.dumps(r, sort_keys=True, default=str) for r in after_rows}

        new_rows = after_set - before_set
        deleted_rows = before_set - after_set

        table_report = {
            "before_count": len(before_rows),
            "after_count": len(after_rows),
            "rows_added": len(new_rows),
            "rows_removed": len(deleted_rows),
            "changed": len(new_rows) > 0 or len(deleted_rows) > 0,
        }

        if table_report["changed"]:
            report["summary"]["tables_changed"] += 1
            report["summary"]["rows_added"] += len(new_rows)
            report["summary"]["rows_removed"] += len(deleted_rows)

        if expected_delta:
            expected = expected_delta.get(table, "no change")
            if expected == "no change":
                table_report["expected_match"] = not table_report["changed"]
            elif "+1 row" in str(expected):
                table_report["expected_match"] = len(new_rows) == 1
            elif "-1 row" in str(expected):
                table_report["expected_match"] = len(deleted_rows) == 1
            else:
                table_report["expected_match"] = True

            if not table_report.get("expected_match", True):
                report["summary"]["match"] = False

        report["tables"][table] = table_report

    return report


def main():
    parser = argparse.ArgumentParser(description="Golden Master / Test Harness")
    subparsers = parser.add_subparsers(dest="command")

    cap = subparsers.add_parser("capture")
    cap.add_argument("--config", required=True, help="Capture config JSON")
    cap.add_argument("--output", required=True, help="Output snapshot JSON")

    cmp = subparsers.add_parser("compare")
    cmp.add_argument("--before", required=True, help="Before snapshot JSON")
    cmp.add_argument("--after", required=True, help="After snapshot JSON")
    cmp.add_argument("--expected", help="Expected delta JSON (optional)")
    cmp.add_argument("--output", required=True, help="Output report JSON")

    args = parser.parse_args()

    if args.command == "capture":
        config = load_json(args.config)
        snapshot = capture_snapshot(config)
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        print(f"Snapshot captured: {args.output}")
        for table, data in snapshot["tables"].items():
            print(f"  {table}: {data['row_count']} rows")

    elif args.command == "compare":
        before = load_json(args.before)
        after = load_json(args.after)
        expected = load_json(args.expected) if args.expected else None
        report = compare_snapshots(before, after, expected)
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Comparison report: {args.output}")
        print(f"  Tables changed: {report['summary']['tables_changed']}/{report['summary']['total_tables']}")
        print(f"  Match: {'✓' if report['summary']['match'] else '✗'}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
