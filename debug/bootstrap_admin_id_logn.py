#!/usr/bin/env python3
"""
Id_Logn 테이블에 관리자 계정을 생성하거나 갱신하는 스크립트.

사용법
------
  # 기본 dry-run (SQL만 출력, DB 변경 없음)
  python debug/bootstrap_admin_id_logn.py --server-id remote_138

  # 실제 적용
  python debug/bootstrap_admin_id_logn.py --server-id remote_138 --apply

  # 관리자 정보 지정 (기본: 환경 변수 BLS_ADMIN_*)
  python debug/bootstrap_admin_id_logn.py --server-id remote_138 --apply \
      --gcode admin --gpass admin123 --hcode 00000 --gname "관리자"

환경 변수 (--옵션 미지정 시 폴백)
---------------------------------
  BLS_ADMIN_GCODE   관리자 로그인 ID    (기본 admin)
  BLS_ADMIN_GPASS   관리자 비밀번호     (기본 admin123)
  BLS_ADMIN_HCODE   소속 코드           (기본 00000)
  BLS_ADMIN_GNAME   시스템 별칭         (기본 관리자)
  BLS_ADMIN_HNAME   표시 이름           (기본 시스템관리자)

전략
----
1. 기존 Id_Logn 에서 f11~f89 컬럼이 가장 많이 'O'인 행을 템플릿으로 복제.
2. 해당 행의 f** 값을 그대로 쓰되, gcode/gpass/hcode/gname/hname 만 교체.
3. 이미 동일 gcode가 있으면 UPDATE, 없으면 INSERT.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# 웹 프로젝트의 backend 경로를 sys.path 에 추가해 config/ssh_tunnels 재사용
_BACKEND = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.core.config import get_server_profile, load_config  # noqa: E402
from app.core.ssh_tunnels import mysql_connect_host_port  # noqa: E402

# f** 컬럼 목록 (Id_Logn 스키마 기준)
F_COLUMNS = [
    f"f{d1}{d2}"
    for d1 in (1, 2, 3, 4, 5, 6, 7, 8)
    for d2 in (1, 2, 3, 4, 5, 6, 7, 8, 9)
]


def _connect(profile: dict) -> "pymysql.connections.Connection":
    """프로필에 따라 pymysql 또는 mysql3 연결을 반환합니다."""
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


def _execute(conn, sql: str, profile: dict) -> int:
    if profile.get("mysql3_protocol"):
        from pymysql_compat import query_mysql3
        charset = str(profile.get("mysql3_charset") or "euc-kr")
        query_mysql3(conn, sql, charset=charset)
        return 0
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
        return cur.rowcount


def _close(conn, profile: dict) -> None:
    if profile.get("mysql3_protocol"):
        from pymysql_compat import close_mysql3
        close_mysql3(conn)
    else:
        conn.close()


def _esc(val: str) -> str:
    return val.replace("\\", "\\\\").replace("'", "\\'")


def main() -> None:
    load_config(force=True)

    ap = argparse.ArgumentParser(description="Id_Logn 관리자 부트스트랩")
    ap.add_argument("--server-id", required=True, help="servers.yaml 서버 id")
    ap.add_argument("--apply", action="store_true", help="실제 DB 반영 (없으면 dry-run)")
    ap.add_argument("--gcode", default=os.environ.get("BLS_ADMIN_GCODE", "admin"))
    ap.add_argument("--gpass", default=os.environ.get("BLS_ADMIN_GPASS", "admin123"))
    ap.add_argument("--hcode", default=os.environ.get("BLS_ADMIN_HCODE", "00000"))
    ap.add_argument("--gname", default=os.environ.get("BLS_ADMIN_GNAME", "관리자"))
    ap.add_argument("--hname", default=os.environ.get("BLS_ADMIN_HNAME", "시스템관리자"))
    args = ap.parse_args()

    profile = get_server_profile(args.server_id)
    if profile is None:
        print(f"[ERROR] Unknown server id: {args.server_id}")
        sys.exit(1)

    conn = _connect(profile)
    try:
        # 1) 기존 행 중 f** 컬럼에 'O'가 가장 많은 행을 템플릿으로 선택
        f_cols_csv = ", ".join(F_COLUMNS)
        template_sql = f"SELECT {f_cols_csv} FROM Id_Logn ORDER BY id LIMIT 50"
        rows = _query(conn, template_sql, profile)

        best_row = None
        best_score = -1
        for r in rows:
            score = sum(1 for fc in F_COLUMNS if str(r.get(fc) or "").strip().upper() == "O")
            if score > best_score:
                best_score = score
                best_row = r

        if best_row is None:
            # 기존 데이터가 없으면 모두 'O'로 채움
            best_row = {fc: "O" for fc in F_COLUMNS}
            print("[INFO] Id_Logn이 비어 있어 f** 전체를 'O'로 설정합니다.")
        else:
            print(f"[INFO] 템플릿 행 선택됨 (f** 중 'O' 개수: {best_score}/{len(F_COLUMNS)})")

        # 2) 기존에 동일 gcode가 있는지 확인
        check_sql = f"SELECT id FROM Id_Logn WHERE gcode = '{_esc(args.gcode)}' LIMIT 1"
        existing = _query(conn, check_sql, profile)

        if existing:
            # UPDATE
            set_parts = [
                f"hcode = '{_esc(args.hcode)}'",
                f"hname = '{_esc(args.hname)}'",
                f"gname = '{_esc(args.gname)}'",
                f"gpass = '{_esc(args.gpass)}'",
            ]
            for fc in F_COLUMNS:
                val = str(best_row.get(fc) or "O").strip() or "O"
                set_parts.append(f"`{fc}` = '{_esc(val)}'")
            sql = (
                f"UPDATE Id_Logn SET {', '.join(set_parts)} "
                f"WHERE gcode = '{_esc(args.gcode)}'"
            )
            action = "UPDATE"
        else:
            # INSERT
            cols = ["hcode", "hname", "gcode", "gname", "gpass"] + [f"`{fc}`" for fc in F_COLUMNS]
            vals = [
                f"'{_esc(args.hcode)}'",
                f"'{_esc(args.hname)}'",
                f"'{_esc(args.gcode)}'",
                f"'{_esc(args.gname)}'",
                f"'{_esc(args.gpass)}'",
            ]
            for fc in F_COLUMNS:
                val = str(best_row.get(fc) or "O").strip() or "O"
                vals.append(f"'{_esc(val)}'")
            sql = f"INSERT INTO Id_Logn ({', '.join(cols)}) VALUES ({', '.join(vals)})"
            action = "INSERT"

        print(f"\n[{action}] SQL:")
        print(sql)
        print()

        if args.apply:
            _execute(conn, sql, profile)
            print(f"[OK] {action} 완료 (gcode={args.gcode})")
        else:
            print("[DRY-RUN] --apply 플래그 없이 실행됨. DB 변경 없음.")
    finally:
        _close(conn, profile)


if __name__ == "__main__":
    main()
