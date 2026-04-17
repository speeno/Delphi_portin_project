"""
MariaDB / MySQL 스키마 메타 추출기 (L4 실행 도구)

INFORMATION_SCHEMA를 통해 DB 스키마 정보만 추출한다 (데이터·전체 덤프 없음):
- 테이블 목록 및 컬럼 정보 (타입, NULL, 기본값, 코멘트)
- PK/FK 관계
- 인덱스 정보
- 트리거/프로시저/뷰 목록

사용법:
  python schema_extractor.py --host <host> --port <port> --user <user> \\
      --password <password> --database <database> --output <output_dir>

여러 서버(SSH·MySQL3 포함)는 extract_server_schema.py 를 사용:
  python tools/db/extract_server_schema.py --server-id remote_138

의존성:
  pip install mysql-connector-python
"""

import argparse
import json
import os
import sys

# 동일 디렉터리 모듈 (스크립트 직접 실행 시)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import schema_core  # noqa: E402


def get_connection(args):
    try:
        import mysql.connector
    except ImportError:
        print("Error: mysql-connector-python 패키지가 필요합니다.")
        print("  pip install mysql-connector-python")
        sys.exit(1)

    return mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
    )


def main():
    parser = argparse.ArgumentParser(description="MariaDB/MySQL 스키마 메타 추출기")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    conn = get_connection(args)
    cursor = conn.cursor()

    print(f"Extracting schema from {args.database}...")

    bundle = schema_core.extract_modern_full(cursor, args.database)

    for name, data in [
        ("tables", bundle["tables"]),
        ("columns", bundle["columns"]),
        ("keys", bundle["keys"]),
        ("indexes", bundle["indexes"]),
        ("routines", bundle["routines"]),
        ("triggers", bundle["triggers"]),
        ("views", bundle["views"]),
        ("db_impact_matrix", bundle["db_impact_matrix"]),
    ]:
        path = os.path.join(args.output, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {name}: {path}")

    summary_path = os.path.join(args.output, "schema_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(bundle["schema_summary"], f, ensure_ascii=False, indent=2)

    slim = {
        "schema_summary": bundle["schema_summary"],
        "tables": bundle["tables"],
        "columns": bundle["columns"],
        "keys": bundle["keys"],
        "indexes": bundle["indexes"],
        "routines": bundle["routines"],
        "triggers": bundle["triggers"],
        "views": bundle["views"],
    }
    with open(os.path.join(args.output, "schema_bundle.json"), "w", encoding="utf-8") as f:
        json.dump(slim, f, ensure_ascii=False, indent=2)

    print(f"\nSchema extraction complete:")
    for k, v in bundle["schema_summary"].items():
        if k != "database":
            print(f"  {k}: {v}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
