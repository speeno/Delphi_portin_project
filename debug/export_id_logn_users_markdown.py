#!/usr/bin/env python3
"""
Id_Logn 테이블의 사용자 계정 목록을 마크다운 테이블로 저장합니다.
비밀번호(gpass) 컬럼은 의도적으로 제외합니다.

사용법
------
  # 기본 (remote_138 → debug/output/user-accounts.md)
  python debug/export_id_logn_users_markdown.py --server-id remote_138

  # 출력 경로 지정
  python debug/export_id_logn_users_markdown.py --server-id remote_153 \
      -o docs/user-list.md

  # 상세 f** 권한 컬럼 포함
  python debug/export_id_logn_users_markdown.py --server-id remote_138 \
      --include-flags
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.core.config import get_server_profile, load_config  # noqa: E402
from app.core.ssh_tunnels import mysql_connect_host_port  # noqa: E402

CORE_COLUMNS = ["id", "hcode", "hname", "gcode", "gname"]

F_COLUMNS = [
    f"f{d1}{d2}"
    for d1 in (1, 2, 3, 4, 5, 6, 7, 8)
    for d2 in (1, 2, 3, 4, 5, 6, 7, 8, 9)
]


def _connect(profile: dict):
    mysql_host, mysql_port = mysql_connect_host_port(profile)
    password = profile.get("password") or os.environ.get("BLS_MYSQL_ROOT_PASSWORD", "")

    if profile.get("mysql3_protocol"):
        from pymysql_compat import connect_mysql3
        return connect_mysql3(
            host=mysql_host, port=mysql_port,
            user=profile["user"], password=str(password),
            database=profile["database"],
            connect_timeout=int(profile.get("connect_timeout", 30)),
            read_timeout=int(profile.get("read_timeout", 120)),
        )

    import pymysql
    return pymysql.connect(
        host=mysql_host, port=mysql_port,
        user=profile["user"], password=str(password),
        database=profile["database"], charset=profile.get("charset", "utf8"),
        connect_timeout=int(profile.get("connect_timeout", 15)),
        read_timeout=int(profile.get("read_timeout", 120)),
        cursorclass=pymysql.cursors.DictCursor,
    )


def _query(conn, sql: str, profile: dict) -> list[dict]:
    if profile.get("mysql3_protocol"):
        from pymysql_compat import query_mysql3
        charset = str(profile.get("mysql3_charset") or "euc-kr")
        return query_mysql3(conn, sql, charset=charset)
    with conn.cursor() as cur:
        cur.execute(sql)
        return list(cur.fetchall())


def _close(conn, profile: dict) -> None:
    if profile.get("mysql3_protocol"):
        from pymysql_compat import close_mysql3
        close_mysql3(conn)
    else:
        conn.close()


def _safe(val) -> str:
    if val is None:
        return ""
    s = str(val).strip()
    return s.replace("|", "\\|")


def main() -> None:
    load_config(force=True)

    ap = argparse.ArgumentParser(description="Id_Logn 사용자 목록 → Markdown 내보내기")
    ap.add_argument("--server-id", required=True, help="servers.yaml 서버 id")
    ap.add_argument("-o", "--output", default=None, help="출력 파일 경로 (기본: debug/output/user-accounts.md)")
    ap.add_argument("--include-flags", action="store_true", help="f11~f89 권한 컬럼도 포함")
    args = ap.parse_args()

    profile = get_server_profile(args.server_id)
    if profile is None:
        print(f"[ERROR] Unknown server id: {args.server_id}")
        sys.exit(1)

    out_path = Path(args.output) if args.output else Path(__file__).resolve().parent / "output" / "user-accounts.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    columns = list(CORE_COLUMNS)
    if args.include_flags:
        columns.extend(F_COLUMNS)
    columns.append("gmemo")

    cols_csv = ", ".join(f"`{c}`" for c in columns)
    sql = f"SELECT {cols_csv} FROM Id_Logn ORDER BY id"

    conn = _connect(profile)
    try:
        rows = _query(conn, sql, profile)
    finally:
        _close(conn, profile)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"<!-- 생성 일시: {now} -->",
        f"<!-- server_id: {args.server_id} -->",
        "<!-- 주의: 비밀번호(gpass) 컬럼은 의도적으로 제외되었습니다. -->",
        "",
        "# Id_Logn 사용자 계정 목록",
        "",
        f"- 서버: `{args.server_id}` ({profile.get('label', '')})",
        f"- 총 {len(rows)}건",
        f"- 생성 일시: {now}",
        "",
    ]

    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines.append(header)
    lines.append(sep)

    for r in rows:
        vals = [_safe(r.get(c)) for c in columns]
        lines.append("| " + " | ".join(vals) + " |")

    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {len(rows)}건 → {out_path}")


if __name__ == "__main__":
    main()
