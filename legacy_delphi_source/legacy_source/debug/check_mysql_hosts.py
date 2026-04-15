#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote MySQL connectivity check and optional schema export.

Credentials ONLY via environment variables or --password-file (never commit secrets):
  MYSQL_USER, MYSQL_PASSWORD (or --password-file path)
  MYSQL_HOST          single host, or use MYSQL_HOSTS
  MYSQL_HOSTS         comma-separated hosts (overrides MYSQL_HOST if set)
  MYSQL_PORT          default 3306
  MYSQL_DATABASE      database name; required for --export (unless --database)
  MYSQL_CHARSET       client charset (default utf8; use utf8mb4 on MySQL 5.5.3+ if supported)

Usage:
  export MYSQL_USER=... MYSQL_PASSWORD=...
  export MYSQL_HOSTS='host1,host2'
  python3 debug/check_mysql_hosts.py

  python3 debug/check_mysql_hosts.py --export --database mydb
  # After export, 14-db-code-vs-live.md is refreshed unless --no-crossref.

  python3 debug/check_mysql_hosts.py --crossref-only   # refresh 14-db-code-vs-live.md from existing CSV

  python3 debug/check_mysql_hosts.py --tcp-probe --hosts 'h1,h2'   # port open only (no auth)

Optional: pip install -r debug/requirements-db.txt  (pymysql)
"""
from __future__ import annotations

import argparse
import csv
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "phase1-structure"

try:
    import pymysql
except ImportError:
    pymysql = None  # type: ignore


def tcp_probe(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """Return (success, message). Success means TCP connect to port accepted."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "port_open"
    except socket.timeout:
        return False, "timeout"
    except OSError as e:
        return False, str(e)


def mask(s: str | None, keep: int = 2) -> str:
    if not s:
        return "(empty)"
    if len(s) <= keep:
        return "***"
    return s[:keep] + "***"


def parse_hosts(args: argparse.Namespace) -> list[str]:
    raw = (os.environ.get("MYSQL_HOSTS") or "").strip()
    if args.hosts:
        raw = args.hosts
    if raw:
        return [h.strip() for h in raw.split(",") if h.strip()]
    h = (args.host or os.environ.get("MYSQL_HOST") or "").strip()
    if h:
        return [h]
    return []


def default_charset() -> str:
    """PyMySQL client charset; utf8mb4 fails on older MySQL (error 1115)."""
    return (os.environ.get("MYSQL_CHARSET") or "utf8").strip() or "utf8"


def connect_params(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str | None,
    charset: str | None = None,
):
    cs = (charset or default_charset()).strip() or "utf8"
    kw: dict = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "connect_timeout": 15,
        "charset": cs,
        "cursorclass": pymysql.cursors.DictCursor,
    }
    if database:
        kw["database"] = database
    return kw


def check_host(
    host: str, port: int, user: str, password: str, charset: str | None = None
) -> tuple[bool, str]:
    if not pymysql:
        return False, "pymysql not installed (pip install -r debug/requirements-db.txt)"
    try:
        kw = connect_params(host, port, user, password, None, charset)
        conn = pymysql.connect(**kw)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS ok")
                row = cur.fetchone()
                if row and row.get("ok") == 1:
                    return True, "OK SELECT 1"
                return True, "OK (unexpected row)"
        finally:
            conn.close()
    except pymysql.Error as e:
        return False, f"{type(e).__name__}: {e}"


def list_databases(conn) -> list[str]:
    with conn.cursor() as cur:
        cur.execute("SHOW DATABASES")
        rows = cur.fetchall()
    out = []
    for r in rows:
        name = r["Database"] if isinstance(r, dict) else r[0]
        if name not in ("information_schema", "performance_schema", "mysql", "sys"):
            out.append(name)
    return sorted(out)


def export_schema_sql(conn, database: str, path: Path) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT TABLE_NAME FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA=%s AND TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME",
            (database,),
        )
        tables = [r["TABLE_NAME"] for r in cur.fetchall()]
    lines = [
        f"-- Schema export (no data) for `{database}`",
        "SET NAMES utf8mb4;\n",
    ]
    with conn.cursor() as cur:
        for t in tables:
            cur.execute(f"SHOW CREATE TABLE `{database}`.`{t}`")
            row = cur.fetchone()
            ddl = None
            for k, v in row.items():
                if isinstance(k, str) and "create" in k.lower():
                    ddl = v
                    break
            if ddl is None:
                ddl = list(row.values())[-1]
            lines.append(f"\n-- Table `{t}`\n")
            lines.append(ddl + ";\n")
    path.write_text("".join(lines), encoding="utf-8")


def export_columns_csv(conn, database: str, path: Path) -> None:
    sql = """
    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION,
           COLUMN_DEFAULT, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH,
           COLUMN_TYPE, COLUMN_KEY, EXTRA
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = %s
    ORDER BY TABLE_NAME, ORDINAL_POSITION
    """
    with conn.cursor() as cur:
        cur.execute(sql, (database,))
        rows = cur.fetchall()
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def export_tables_summary_md(conn, database: str, path: Path, host: str) -> None:
    sql = """
    SELECT TABLE_NAME, ENGINE, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH, INDEX_LENGTH, TABLE_COMMENT
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
    """
    with conn.cursor() as cur:
        cur.execute(sql, (database,))
        rows = cur.fetchall()
    lines = [
        f"# MySQL tables summary (`{database}`)\n\n",
        f"- **Host**: `{host}`\n",
        f"- **Table count**: {len(rows)}\n\n",
        "| TABLE_NAME | ENGINE | TABLE_ROWS | DATA_LENGTH | INDEX_LENGTH | COMMENT |\n",
        "|------------|--------|------------|-------------|--------------|---------|\n",
    ]
    for r in rows:
        cmt = (r.get("TABLE_COMMENT") or "").replace("|", " ").replace("\n", " ")[:80]
        lines.append(
            f"| `{r['TABLE_NAME']}` | {r.get('ENGINE') or ''} | "
            f"{r.get('TABLE_ROWS') or 0} | {r.get('DATA_LENGTH') or 0} | "
            f"{r.get('INDEX_LENGTH') or 0} | {cmt} |\n"
        )
    path.write_text("".join(lines), encoding="utf-8")


def run_crossref_subprocess(columns_csv: Path) -> int:
    """Regenerate 14-db-code-vs-live.md via crossref_schema_vs_code.py."""
    xref = ROOT / "debug" / "crossref_schema_vs_code.py"
    print("\nUpdating 14-db-code-vs-live.md (crossref) ...")
    cmd = [
        sys.executable,
        str(xref),
        "--columns-csv",
        str(columns_csv),
    ]
    return subprocess.call(cmd, cwd=str(ROOT))


def run_export(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    out_dir: Path,
    charset: str | None = None,
) -> None:
    kw = connect_params(host, port, user, password, database, charset)
    conn = pymysql.connect(**kw)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        export_schema_sql(conn, database, out_dir / "14-mysql-schema.sql")
        export_columns_csv(conn, database, out_dir / "14-mysql-columns.csv")
        export_tables_summary_md(conn, database, out_dir / "14-mysql-tables-summary.md", host)
        print(f"Wrote {out_dir / '14-mysql-schema.sql'}")
        print(f"Wrote {out_dir / '14-mysql-columns.csv'}")
        print(f"Wrote {out_dir / '14-mysql-tables-summary.md'}")
    finally:
        conn.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Check MySQL hosts and optionally export schema.")
    ap.add_argument("--hosts", help="Comma-separated hosts (else MYSQL_HOSTS / MYSQL_HOST)")
    ap.add_argument("--host", help="Single host (else MYSQL_HOST)")
    ap.add_argument("--port", type=int, default=int(os.environ.get("MYSQL_PORT", "3306")))
    ap.add_argument("--user", default=os.environ.get("MYSQL_USER", ""))
    ap.add_argument("--password", default=os.environ.get("MYSQL_PASSWORD", ""))
    ap.add_argument(
        "--password-file",
        type=Path,
        help="Read MySQL password from file (UTF-8, single line; do not commit this file)",
    )
    ap.add_argument("--database", "-d", help="Database for export (else MYSQL_DATABASE)")
    ap.add_argument(
        "--charset",
        default="",
        help="Client charset for PyMySQL (default: MYSQL_CHARSET env or utf8; use utf8mb4 on modern MySQL)",
    )
    ap.add_argument("--export", action="store_true", help="Export schema/columns/summary to docs")
    ap.add_argument(
        "--crossref-only",
        action="store_true",
        help="Only refresh 14-db-code-vs-live.md (requires existing 14-mysql-columns.csv)",
    )
    ap.add_argument(
        "--no-crossref",
        action="store_true",
        help="After successful --export, do not run crossref_schema_vs_code.py",
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=DOCS,
        help=f"Output directory (default: {DOCS})",
    )
    ap.add_argument(
        "--export-on-host",
        help="Run export on this host only (default: first host that passes check)",
    )
    ap.add_argument(
        "--tcp-probe",
        action="store_true",
        help="Only test TCP connectivity to MySQL port (no credentials)",
    )
    ap.add_argument(
        "--probe-timeout",
        type=float,
        default=5.0,
        help="Seconds for TCP probe (default: 5)",
    )
    args = ap.parse_args()

    if args.crossref_only:
        if args.export or args.tcp_probe:
            print("Do not combine --crossref-only with --export or --tcp-probe.", file=sys.stderr)
            return 2
        path_check = args.output_dir / "14-mysql-columns.csv"
        if not path_check.is_file():
            print(
                f"Missing {path_check}. Run with --export --database <db> first (or copy CSV there).",
                file=sys.stderr,
            )
            return 1
        rc = run_crossref_subprocess(path_check)
        if rc != 0:
            print(f"crossref_schema_vs_code.py exited {rc}", file=sys.stderr)
        return rc

    hosts = parse_hosts(args)

    if args.tcp_probe:
        if not hosts:
            print("No hosts: pass --hosts or set MYSQL_HOSTS / MYSQL_HOST", file=sys.stderr)
            return 2
        print(f"TCP probe port={args.port} timeout={args.probe_timeout}s")
        print(f"Hosts ({len(hosts)}): {hosts!r}\n")
        any_open = False
        for h in hosts:
            ok, msg = tcp_probe(h, args.port, args.probe_timeout)
            any_open = any_open or ok
            status = "OPEN" if ok else "CLOSED"
            print(f"  [{status}] {h}:{args.port} ({msg})")
        print(
            "\nIf all CLOSED from outside, use SSH -L local:3306:127.0.0.1:3306 then MYSQL_HOST=127.0.0.1 MYSQL_PORT=<local>."
        )
        return 0 if any_open else 1

    user = args.user
    password = (args.password or "").strip()
    if args.password_file:
        if not args.password_file.is_file():
            print(f"No such file: {args.password_file}", file=sys.stderr)
            return 2
        password = args.password_file.read_text(encoding="utf-8").strip()

    if not hosts:
        print("No hosts: set MYSQL_HOSTS or MYSQL_HOST, or pass --hosts", file=sys.stderr)
        return 2
    if not user:
        print("No user: set MYSQL_USER or pass --user", file=sys.stderr)
        return 2
    if password is None or password == "":
        print("No password: set MYSQL_PASSWORD or pass --password", file=sys.stderr)
        return 2

    charset = (args.charset or "").strip() or None

    print(f"User={user!r} password={mask(password)} port={args.port} charset={charset or default_charset()!r}")
    print(f"Hosts ({len(hosts)}): {hosts!r}\n")

    ok_hosts: list[str] = []
    for h in hosts:
        ok, msg = check_host(h, args.port, user, password, charset)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {h}: {msg}")
        if ok:
            ok_hosts.append(h)

    if not ok_hosts:
        print("\nNo reachable hosts.")
        return 1

    if not args.export:
        print(f"\n{len(ok_hosts)} host(s) reachable. Use --export to write 14-* files.")
        return 0

    db = (args.database or os.environ.get("MYSQL_DATABASE") or "").strip()
    export_host = args.export_on_host
    if export_host:
        if export_host not in ok_hosts:
            print(f"--export-on-host {export_host!r} is not in OK list.", file=sys.stderr)
            return 1
    else:
        export_host = ok_hosts[0]

    if not db:
        if not pymysql:
            print("pymysql required for --export", file=sys.stderr)
            return 1
        kw = connect_params(export_host, args.port, user, password, None, charset)
        conn = pymysql.connect(**kw)
        try:
            dbs = list_databases(conn)
        finally:
            conn.close()
        print("\nMYSQL_DATABASE not set. Non-system databases:")
        for name in dbs[:50]:
            print(f"  - {name}")
        if len(dbs) > 50:
            print(f"  ... ({len(dbs)} total)")
        print("\nRe-run with: --export --database <name>  (or set MYSQL_DATABASE)")
        return 3

    print(f"\nExporting from {export_host!r} database={db!r} -> {args.output_dir}")
    run_export(export_host, args.port, user, password, db, args.output_dir, charset)
    columns_csv = args.output_dir / "14-mysql-columns.csv"
    if not args.no_crossref:
        rc = run_crossref_subprocess(columns_csv)
        if rc != 0:
            print(
                "crossref failed; 14-db-code-vs-live.md may be stale. Run: "
                "python3 debug/check_mysql_hosts.py --crossref-only",
                file=sys.stderr,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
