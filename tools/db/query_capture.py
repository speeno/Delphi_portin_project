"""
DB 쿼리 캡처 파이프라인 (L4 실행 도구 / Capture Harness)

MariaDB general log를 모니터링하여 실행되는 쿼리를 실시간으로 캡처하고,
정규화하여 JSON 파일로 저장한다.

기능:
1. General log 파일 tail 모드
2. 캡처된 쿼리 정규화 (파라미터 마스킹, 공백 정리)
3. 업무 흐름별 세션 그룹핑
4. JSON 파일 출력

사용법:
  python query_capture.py --mode file --log-path /var/log/mysql/general.log --output captured_queries.json
  python query_capture.py --mode table --host <host> --user <user> --password <password> --database <database> --output captured_queries.json

의존성 (table 모드):
  pip install mysql-connector-python
"""

import re
import json
import sys
import os
import time
import argparse
from datetime import datetime


def normalize_query(sql: str) -> str:
    """쿼리를 정규화한다 (파라미터 마스킹, 공백 정리)."""
    normalized = re.sub(r"'[^']*'", "'?'", sql)
    normalized = re.sub(r'\b\d+\b', '?', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def classify_query(sql: str) -> str:
    upper = sql.strip().upper()
    for keyword in ["SELECT", "INSERT", "UPDATE", "DELETE", "CALL", "BEGIN", "COMMIT", "ROLLBACK", "SET", "SHOW"]:
        if upper.startswith(keyword):
            return keyword
    return "OTHER"


def parse_general_log_line(line: str) -> dict | None:
    """General log 한 줄을 파싱한다."""
    pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}T[\d:.]+Z?)\s+(\d+)\s+(\w+)\s+(.*)',
    )
    match = pattern.match(line.strip())
    if not match:
        simple = re.compile(r'\s*(\d+)\s+(\w+)\s+(.*)')
        simple_match = simple.match(line.strip())
        if simple_match:
            return {
                "timestamp": datetime.now().isoformat(),
                "connection_id": int(simple_match.group(1)),
                "command": simple_match.group(2),
                "argument": simple_match.group(3),
            }
        return None

    return {
        "timestamp": match.group(1),
        "connection_id": int(match.group(2)),
        "command": match.group(3),
        "argument": match.group(4),
    }


def tail_file(filepath: str, callback, interval: float = 0.5):
    """파일을 tail -f 방식으로 모니터링한다."""
    with open(filepath, 'r') as f:
        f.seek(0, 2)
        print(f"Tailing {filepath}... (Ctrl+C to stop)")
        try:
            while True:
                line = f.readline()
                if line:
                    callback(line)
                else:
                    time.sleep(interval)
        except KeyboardInterrupt:
            print("\nCapture stopped.")


def capture_from_table(args) -> list[dict]:
    """mysql.general_log 테이블에서 쿼리를 캡처한다."""
    try:
        import mysql.connector
    except ImportError:
        print("Error: mysql-connector-python 필요")
        sys.exit(1)

    conn = mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database="mysql",
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_time, user_host, thread_id, command_type, argument
        FROM mysql.general_log
        WHERE command_type = 'Query'
        AND argument NOT LIKE '%general_log%'
        ORDER BY event_time DESC
        LIMIT 1000
    """)

    results = []
    for row in cursor.fetchall():
        sql = row[4]
        if isinstance(sql, bytes):
            sql = sql.decode('utf-8', errors='replace')

        query_type = classify_query(sql)
        if query_type in ("SET", "SHOW", "OTHER"):
            continue

        results.append({
            "timestamp": str(row[0]),
            "user": row[1],
            "thread_id": row[2],
            "sql": sql,
            "normalized": normalize_query(sql),
            "type": query_type,
            "tables": extract_tables(sql),
        })

    cursor.close()
    conn.close()
    return results


def extract_tables(sql: str) -> list[str]:
    tables = set()
    for p in [
        re.compile(r'\bFROM\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bJOIN\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bINTO\s+(\w+)', re.IGNORECASE),
        re.compile(r'\bUPDATE\s+(\w+)', re.IGNORECASE),
    ]:
        for m in p.finditer(sql):
            tables.add(m.group(1))
    return sorted(tables)


def main():
    parser = argparse.ArgumentParser(description="DB 쿼리 캡처 파이프라인")
    parser.add_argument("--mode", choices=["file", "table"], required=True)
    parser.add_argument("--log-path", help="General log file path (file mode)")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", default="")
    parser.add_argument("--database", default="mysql")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.mode == "file":
        if not args.log_path:
            print("--log-path required for file mode")
            sys.exit(1)

        captured = []

        def on_line(line):
            parsed = parse_general_log_line(line)
            if parsed and parsed["command"] == "Query":
                sql = parsed["argument"]
                qtype = classify_query(sql)
                if qtype not in ("SET", "SHOW", "OTHER"):
                    entry = {
                        **parsed,
                        "normalized": normalize_query(sql),
                        "type": qtype,
                        "tables": extract_tables(sql),
                    }
                    captured.append(entry)
                    print(f"  [{qtype}] {sql[:100]}")

                    if len(captured) % 100 == 0:
                        with open(args.output, "w", encoding="utf-8") as f:
                            json.dump(captured, f, ensure_ascii=False, indent=2)

        try:
            tail_file(args.log_path, on_line)
        finally:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(captured, f, ensure_ascii=False, indent=2)
            print(f"\nCaptured {len(captured)} queries -> {args.output}")

    elif args.mode == "table":
        results = capture_from_table(args)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Captured {len(results)} queries -> {args.output}")


if __name__ == "__main__":
    main()
