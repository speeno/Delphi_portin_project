#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compare live MySQL tables (from 14-mysql-columns.csv) with code references (13-db-sql-references.csv).

Writes docs/phase1-structure/14-db-code-vs-live.md

Run after: debug/check_mysql_hosts.py --export --database <db>
"""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "phase1-structure"
DEFAULT_CODE = DOCS / "13-db-sql-references.csv"
DEFAULT_COLS = DOCS / "14-mysql-columns.csv"
DEFAULT_OUT = DOCS / "14-db-code-vs-live.md"


def read_csv_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def load_code_tables(path: Path) -> set[str]:
    tables: set[str] = set()
    f = io.StringIO(read_csv_text(path))
    r = csv.DictReader(f)
    for row in r:
        t = (row.get("table") or "").strip()
        if t:
            tables.add(t)
    return tables


def load_live_tables(path: Path) -> tuple[set[str], str | None]:
    """Return (table names, TABLE_SCHEMA if uniform)."""
    tables: set[str] = set()
    schemas: set[str] = set()
    if not path.is_file():
        return tables, None
    f = io.StringIO(read_csv_text(path))
    r = csv.DictReader(f)
    for row in r:
        t = (row.get("TABLE_NAME") or row.get("table_name") or "").strip()
        s = (row.get("TABLE_SCHEMA") or row.get("table_schema") or "").strip()
        if t:
            tables.add(t)
        if s:
            schemas.add(s)
    schema = next(iter(schemas)) if len(schemas) == 1 else None
    return tables, schema


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-csv", type=Path, default=DEFAULT_CODE)
    ap.add_argument("--columns-csv", type=Path, default=DEFAULT_COLS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    if not args.code_csv.is_file():
        print(f"Missing {args.code_csv}")
        return 1

    code_tables = load_code_tables(args.code_csv)
    live_tables, live_schema = load_live_tables(args.columns_csv)

    lines: list[str] = []
    lines.append("# Code vs live DB tables\n\n")
    lines.append(
        "*When live MySQL is available, run `python3 debug/check_mysql_hosts.py --export --database <db>`; "
        "this file is refreshed automatically after export (use `--no-crossref` to skip). "
        "To regenerate only this doc from an existing CSV: `python3 debug/check_mysql_hosts.py --crossref-only`.*\n\n"
    )
    lines.append(
        f"- **Code inventory**: [`13-db-sql-references.csv`](13-db-sql-references.csv) "
        f"({len(code_tables)} unique `table` values).\n"
    )
    if not args.columns_csv.is_file() or not live_tables:
        lines.append(
            "- **Live DB**: *(no [`14-mysql-columns.csv`](14-mysql-columns.csv); run "
            "`python3 debug/check_mysql_hosts.py --export --database <db>` first.)*\n\n"
        )
        lines.append("## Result\n\n")
        lines.append("Cannot compare until live export exists.\n")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(lines), encoding="utf-8")
        print(f"Wrote {args.out} (placeholder)")
        return 0

    lines.append(
        f"- **Live DB**: [`14-mysql-columns.csv`](14-mysql-columns.csv) "
        f"({len(live_tables)} tables"
        + (f", schema `{live_schema}`" if live_schema else "")
        + ").\n\n"
    )

    only_code = sorted(code_tables - live_tables)
    only_live = sorted(live_tables - code_tables)
    both = sorted(code_tables & live_tables)

    lines.append("## Summary\n\n")
    lines.append(f"| Metric | Count |\n|--------|------:|\n")
    lines.append(f"| In both | {len(both)} |\n")
    lines.append(f"| Code only (not in live export) | {len(only_code)} |\n")
    lines.append(f"| Live only (not in code heuristic) | {len(only_live)} |\n\n")

    lines.append("## In both\n\n")
    if both:
        lines.append(", ".join(f"`{t}`" for t in both[:200]))
        if len(both) > 200:
            lines.append(f"\n\n... and {len(both) - 200} more.\n")
    else:
        lines.append("*(none)*\n")
    lines.append("\n")

    lines.append("## Code only\n\n")
    lines.append(
        "*Referenced in Delphi closure scan but no matching `TABLE_NAME` in live export.*\n\n"
    )
    if only_code:
        for t in only_code:
            lines.append(f"- `{t}`\n")
    else:
        lines.append("*(none)*\n")
    lines.append("\n")

    lines.append("## Live only\n\n")
    lines.append(
        "*Present in MySQL but not captured as a table token in [`extract_db_sql_references.py`](../../debug/extract_db_sql_references.py) scan.*\n\n"
    )
    if only_live:
        for t in only_live:
            lines.append(f"- `{t}`\n")
    else:
        lines.append("*(none)*\n")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
