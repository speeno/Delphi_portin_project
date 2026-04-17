#!/usr/bin/env python3
"""
servers.yaml 프로필로 DB 스키마 메타만 추출 (데이터·전체 덤프 없음).

- 모던 MySQL/MariaDB: INFORMATION_SCHEMA (schema_core)
- mysql3_protocol: SHOW TABLES / SHOW FIELDS / SHOW KEYS / SHOW CREATE TABLE (schema_legacy)

사용법
------
  cd /path/to/Delphi_porting
  python3 tools/db/extract_server_schema.py --server-id remote_138

  # 출력 디렉터리 지정 (기본: debug/output/schema/<server-id>/)
  python3 tools/db/extract_server_schema.py --server-id remote_153 -o /tmp/schema-153

환경 변수
----------
  BLS_SERVERS_CONFIG  servers.yaml 경로 (미설정 시 도서물류관리프로그램/backend/servers.yaml)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_TOOLS_DB = Path(__file__).resolve().parent
_REPO_ROOT = _TOOLS_DB.parent.parent
_BACKEND = _REPO_ROOT / "도서물류관리프로그램" / "backend"

sys.path.insert(0, str(_TOOLS_DB))

if _BACKEND.is_dir():
    sys.path.insert(0, str(_BACKEND))


def _connect_product(profile: dict):
    from app.core.ssh_tunnels import mysql_connect_host_port  # noqa: E402

    mysql_host, mysql_port = mysql_connect_host_port(profile)
    password = profile.get("password") or os.environ.get("BLS_MYSQL_ROOT_PASSWORD", "")

    if profile.get("mysql3_protocol"):
        from pymysql_compat import connect_mysql3  # noqa: E402

        return (
            "mysql3",
            connect_mysql3(
                host=mysql_host,
                port=mysql_port,
                user=profile["user"],
                password=str(password),
                database=profile["database"],
                connect_timeout=int(profile.get("connect_timeout", 45)),
                read_timeout=int(profile.get("read_timeout", 300)),
            ),
            profile,
        )

    import pymysql  # noqa: E402

    conn = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=profile["user"],
        password=str(password),
        database=profile["database"],
        charset=profile.get("charset", "utf8"),
        connect_timeout=int(profile.get("connect_timeout", 15)),
        read_timeout=int(profile.get("read_timeout", 120)),
    )
    return ("pymysql", conn, profile)


def _close(kind: str, conn, profile: dict) -> None:
    if kind == "mysql3":
        from pymysql_compat import close_mysql3  # noqa: E402

        close_mysql3(conn)
    else:
        conn.close()


def _write_bundle(out_dir: Path, bundle: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
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
        path = out_dir / f"{name}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if bundle.get("table_ddl"):
        (out_dir / "table_ddl.json").write_text(
            json.dumps(bundle["table_ddl"], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    summary = bundle["schema_summary"]
    (out_dir / "schema_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 단일 번들( diff 도구용 )
    slim = {
        "schema_summary": summary,
        "tables": bundle["tables"],
        "columns": bundle["columns"],
        "keys": bundle["keys"],
        "indexes": bundle["indexes"],
        "routines": bundle["routines"],
        "triggers": bundle["triggers"],
        "views": bundle["views"],
    }
    if bundle.get("table_ddl"):
        slim["table_ddl"] = bundle["table_ddl"]
    (out_dir / "schema_bundle.json").write_text(
        json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="스키마 메타만 추출 (전체 DB 덤프/스냅샷 없음)",
    )
    ap.add_argument("--server-id", required=True, help="servers.yaml 의 서버 id")
    ap.add_argument(
        "-o",
        "--output",
        default=None,
        help="출력 디렉터리 (기본: debug/output/schema/<server-id>/)",
    )
    args = ap.parse_args()

    if not _BACKEND.is_dir():
        print(
            "[ERROR] 도서물류관리프로그램/backend 가 없습니다. "
            "BLS_SERVERS_CONFIG 로 YAML 경로를 지정하거나 저장소 구성을 확인하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    from app.core.config import get_server_profile, load_config  # noqa: E402

    load_config(force=True)
    profile = get_server_profile(args.server_id)
    if profile is None:
        print(f"[ERROR] Unknown server id: {args.server_id}", file=sys.stderr)
        sys.exit(1)

    database = str(profile.get("database") or "")
    if not database:
        print("[ERROR] profile.database 가 비어 있습니다.", file=sys.stderr)
        sys.exit(1)

    out_dir = (
        Path(args.output)
        if args.output
        else _REPO_ROOT / "debug" / "output" / "schema" / args.server_id
    )

    kind, conn, profile = _connect_product(profile)
    try:
        if kind == "mysql3":
            from pymysql_compat import query_mysql3  # noqa: E402

            charset = str(profile.get("mysql3_charset") or "euc-kr")

            def q(sql: str):
                return query_mysql3(conn, sql, charset=charset)

            import schema_legacy  # noqa: E402

            bundle = schema_legacy.extract_mysql3_meta(q, database)
        else:
            import schema_core  # noqa: E402

            cur = conn.cursor()
            try:
                bundle = schema_core.extract_modern_full(cur, database)
            finally:
                cur.close()
    finally:
        _close(kind, conn, profile)

    _write_bundle(out_dir, bundle)
    print(f"[OK] schema meta → {out_dir}")
    print(f"     mode={bundle['schema_summary'].get('extraction_mode')}, tables={bundle['schema_summary'].get('tables')}")


if __name__ == "__main__":
    main()
