#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List non-root MySQL users from each host in seak80 servers.yaml.

Run from repository root:
  python3 debug/list_mysql_non_root_users.py

  python3 debug/list_mysql_non_root_users.py --config web/seak80-sample/backend/servers.yaml

Requires: PyYAML, pymysql. Reads credentials from servers.yaml (often gitignored).
Tries client charset utf8mb4, then utf8 (MySQL 5.1 rejects utf8mb4).
"""
from __future__ import annotations

import argparse
import sys
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "web" / "seak80-sample" / "backend" / "servers.yaml"

try:
    import pymysql
    import yaml
except ImportError as e:
    print("Install deps: pip install pymysql pyyaml", e, file=sys.stderr)
    sys.exit(1)

_SYSTEM_USERS = (
    "mysql.sys",
    "mysql.session",
    "mysql.infoschema",
    "debian-sys-maint",
)
_SQL = (
    "SELECT User, Host FROM mysql.user "
    "WHERE User != 'root' AND User != '' "
    "AND User NOT IN ("
    + ",".join(repr(x) for x in _SYSTEM_USERS)
    + ") ORDER BY User, Host"
)


def decode_yaml_raw(raw: bytes) -> str:
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def connect_with_charset(host: str, port: int, user: str, password: str):
    last_err = None
    for charset in ("utf8mb4", "utf8"):
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database="mysql",
                charset=charset,
                connect_timeout=15,
                read_timeout=60,
            )
            return conn, charset
        except pymysql.Error as e:
            last_err = e
            if e.args and e.args[0] == 1115 and "utf8mb4" in str(e).lower():
                continue
            raise
    raise last_err


def main() -> int:
    ap = argparse.ArgumentParser(description="List non-root mysql.user rows per YAML host.")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = ap.parse_args()
    cfg_path = args.config
    if not cfg_path.is_file():
        print(f"Missing config: {cfg_path}", file=sys.stderr)
        return 1
    data = yaml.safe_load(StringIO(decode_yaml_raw(cfg_path.read_bytes())))
    servers = (data or {}).get("servers") or []
    if not servers:
        print("No servers in YAML")
        return 0

    for s in servers:
        if not isinstance(s, dict):
            continue
        host = s.get("host")
        port = int(s.get("port", 3306))
        user = s.get("user")
        password = str(s.get("password", ""))
        sid = (s.get("id") or host or "?").strip()
        print(f"\n=== {sid} ({host}:{port}) ===")
        try:
            conn, charset = connect_with_charset(host, port, user, password)
        except pymysql.Error as e:
            print(f"CONNECT_FAILED: {e}")
            continue
        print(f"(client charset: {charset})")
        try:
            with conn.cursor() as cur:
                cur.execute(_SQL)
                rows = cur.fetchall()
            if not rows:
                print("(no rows; or no privilege to read mysql.user)")
            else:
                for u, h in rows:
                    print(f"  {u!r} @ {h!r}")
        except pymysql.Error as e:
            print(f"QUERY_FAILED: {e}")
        finally:
            conn.close()
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
