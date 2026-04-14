#!/usr/bin/env python3
"""
MariaDB 접속 프로브 (레거시 서버: charset=utf8 권장).

비밀번호는 환경 변수 MARIADB_PASSWORD 만 사용합니다. 저장소에 비밀을 넣지 마세요.

  export MARIADB_PASSWORD='...'
  python3 debug/db_connect_probe.py
  python3 debug/db_connect_probe.py --write-json dashboard/data/db-status.json

호스트 목록: 환경 변수 MARIADB_HOSTS (쉼표 구분) 또는 아래 기본값.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_HOSTS = [
    "115.68.3.153",
    "115.68.3.154",
    "115.68.3.155",
    "115.68.7.138",
]


def try_connect(host: str, port: int, user: str, password: str, charset: str) -> tuple[bool, str]:
    try:
        import mysql.connector
    except ImportError:
        return False, "mysql-connector-python 미설치 (pip install mysql-connector-python)"

    try:
        c = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connection_timeout=12,
            charset=charset,
            use_unicode=True,
        )
        cur = c.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        c.close()
        return True, f"SELECT 1 성공 (charset={charset})"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"[:220]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-json",
        metavar="PATH",
        help="비밀 없이 결과만 JSON으로 저장 (예: dashboard/data/db-status.json)",
    )
    parser.add_argument("--port", type=int, default=int(os.environ.get("MARIADB_PORT", "3306")))
    parser.add_argument("--user", default=os.environ.get("MARIADB_USER", "root"))
    args = parser.parse_args()

    password = os.environ.get("MARIADB_PASSWORD")
    if not password:
        print("MARIADB_PASSWORD 환경 변수를 설정하세요.", file=sys.stderr)
        return 1

    raw = os.environ.get("MARIADB_HOSTS", "")
    hosts = [h.strip() for h in raw.split(",") if h.strip()] if raw else DEFAULT_HOSTS

    results = []
    for host in hosts:
        ok, detail = try_connect(host, args.port, args.user, password, "utf8")
        results.append({"host": host, "reachable": ok, "detail": detail})

    payload = {
        "checkedAt": datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat(),
        "mysqlPort": args.port,
        "sshPortNote": "DB는 일반적으로 3306. 22는 SSH.",
        "clientCharset": "utf8",
        "charsetNote": "utf8mb4 미지원 서버 대비 utf8로 프로브",
        "hosts": results,
        "successCount": sum(1 for r in results if r["reachable"]),
        "totalHosts": len(results),
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.write_json:
        out = args.write_json
        parent = os.path.dirname(os.path.abspath(out))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Wrote {out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
