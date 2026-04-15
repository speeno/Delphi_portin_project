#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build porting / optimization report from:
  - docs/phase1-structure/13-db-sql-references.csv
  - Optional docs/phase1-structure/14-mysql-columns.csv (live)
  - Chulpan.dpr closure: Pascal patterns (Seek_Name, RunSQL, ClientDataSet, etc.)

Outputs:
  docs/phase1-structure/15-db-porting-and-optimization.md
  docs/phase1-structure/15-db-table-usage.csv

Run: python3 debug/generate_db_porting_report.py
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

_DEBUG = Path(__file__).resolve().parent
if str(_DEBUG) not in sys.path:
    sys.path.insert(0, str(_DEBUG))

from delphi_build_closure import closure_from_dpr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "phase1-structure"
CSV13 = DOCS / "13-db-sql-references.csv"
CSV14 = DOCS / "14-mysql-columns.csv"
OUT_MD = DOCS / "15-db-porting-and-optimization.md"
OUT_CSV = DOCS / "15-db-table-usage.csv"

# (label, regex) \u2014 counted as non-overlapping matches per file, then summed
PAS_ACCESS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Seek_Name", re.compile(r"\.Seek_Name\s*\(", re.I)),
    ("RunSQL", re.compile(r"\.RunSQL\s*\(", re.I)),
    ("Socket API", re.compile(r"\bSocket\.(?:RunSQL|busyloop|MakeData|GetData)\b", re.I)),
    ("Sql.Add", re.compile(r"\.[Ss]ql\.Add\s*\(", re.I)),
    ("SQL.Text assign", re.compile(r"\.SQL\.Text\s*:=", re.I)),
    ("Sqlen assign", re.compile(r"\bSqlen\s*:=", re.I)),
    ("OpenShow", re.compile(r"\bOpenShow\s*\(", re.I)),
    ("ApplyUpdates", re.compile(r"\.ApplyUpdates\s*\(", re.I)),
    ("TClientDataSet", re.compile(r"\bTClientDataSet\b", re.I)),
    ("TZMySqlQuery", re.compile(r"\bTZMySqlQuery\b", re.I)),
    ("TZMySqlTable", re.compile(r"\bTZMySqlTable\b", re.I)),
    ("TDataSource", re.compile(r"\bTDataSource\b", re.I)),
    ("TDBGridEh", re.compile(r"\bTDBGridEh\b", re.I)),
    ("TDBGrid", re.compile(r"\bTDBGrid\b", re.I)),
]


def read_csv_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def load_13_rows() -> list[dict[str, str]]:
    if not CSV13.is_file():
        return []
    f = io.StringIO(read_csv_text(CSV13))
    return list(csv.DictReader(f))


def load_live_tables() -> tuple[set[str], str | None]:
    if not CSV14.is_file():
        return set(), None
    f = io.StringIO(read_csv_text(CSV14))
    tables: set[str] = set()
    schemas: set[str] = set()
    for row in csv.DictReader(f):
        t = (row.get("TABLE_NAME") or row.get("table_name") or "").strip()
        s = (row.get("TABLE_SCHEMA") or row.get("table_schema") or "").strip()
        if t:
            tables.add(t)
        if s:
            schemas.add(s)
    sch = next(iter(schemas)) if len(schemas) == 1 else None
    return tables, sch


def scan_closure_pas() -> tuple[Counter[str], int]:
    """Pattern name -> total count; second return = pas file count."""
    units, _miss = closure_from_dpr()
    pas_paths = [p for _, p in units]
    totals: Counter[str] = Counter()
    for path in pas_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for label, pat in PAS_ACCESS_PATTERNS:
            totals[label] += len(pat.findall(text))
    return totals, len(pas_paths)


def aggregate_tables(rows: list[dict[str, str]]):
    """table -> hits, kinds Counter, units Counter, example files set."""
    hits: dict[str, int] = defaultdict(int)
    kinds: dict[str, Counter[str]] = defaultdict(Counter)
    units: dict[str, Counter[str]] = defaultdict(Counter)
    files: dict[str, set[str]] = defaultdict(set)
    for r in rows:
        t = (r.get("table") or "").strip()
        if not t:
            continue
        hits[t] += 1
        kinds[t][(r.get("kind") or "").strip() or "?"] += 1
        u = (r.get("unit") or "").strip()
        if u:
            units[t][u] += 1
        fn = (r.get("file") or "").strip()
        if fn:
            files[t].add(fn)
    return hits, kinds, units, files


def md_escape_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    rows = load_13_rows()
    if not rows:
        print(f"Missing or empty {CSV13}", file=sys.stderr)
        return 1

    hits, kinds, units, files = aggregate_tables(rows)
    live_tables, live_schema = load_live_tables()
    pas_counts, n_pas = scan_closure_pas()

    code_tables = set(hits.keys())
    only_code = sorted(code_tables - live_tables) if live_tables else []
    only_live = sorted(live_tables - code_tables) if live_tables else []
    both = sorted(code_tables & live_tables) if live_tables else sorted(code_tables)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# DB porting and optimization notes (Chulpan closure)\n\n")
    lines.append(
        "Generated by [`debug/generate_db_porting_report.py`](../../debug/generate_db_porting_report.py). "
        "Refresh after updating [`13-db-sql-references.csv`](13-db-sql-references.csv) "
        "([`debug/extract_db_sql_references.py`](../../debug/extract_db_sql_references.py)) or live export [`14-mysql-columns.csv`](14-mysql-columns.csv).\n\n"
    )

    lines.append("## 1. How data access works in this codebase\n\n")
    lines.append(
        "The Delphi app combines **in-memory `TClientDataSet`** (often via `Base10.OpenShow`), "
        "**string-built SQL** (`Sqlen`, `Sql.Add`), and legacy **middleware-style** calls such as "
        "`Base10.Seek_Name` / socket `RunSQL` (see [`Base01.pas`](../../Base01.pas)). "
        "A modern port typically replaces string SQL with **parameterized queries**, a single **connection pool**, and explicit **repositories** per aggregate.\n\n"
    )
    lines.append(f"- **PAS files in closure**: {n_pas}\n")
    lines.append("- **Pattern counts** (regex hits summed over all closure `.pas`; overlaps possible):\n\n")
    lines.append("| Pattern | Approx. hits |\n|---------|---------------:|\n")
    for label, c in pas_counts.most_common():
        lines.append(f"| {label} | {c} |\n")
    lines.append("\n")

    lines.append("## 2. Tables referenced in SQL strings (static scan)\n\n")
    lines.append(
        f"- **Distinct table names**: {len(hits)}\n"
        f"- **Total SQL token hits** (from/join/into/update/dfm): {sum(hits.values())}\n\n"
    )

    lines.append("### 2.1 Top tables by hit count\n\n")
    lines.append("| table | hits | units | primary `kind` tags |\n")
    lines.append("|-------|-----:|------:|--------------------|\n")
    for t, c in sorted(hits.items(), key=lambda x: (-x[1], x[0]))[:45]:
        nu = len(units[t])
        ktop = ", ".join(f"{k}({v})" for k, v in kinds[t].most_common(3))
        lines.append(f"| `{md_escape_cell(t)}` | {c} | {nu} | {md_escape_cell(ktop)} |\n")
    lines.append("\n")

    lines.append("### 2.2 Per-table unit hotspots (top 3 units per table, sample)\n\n")
    for t, c in sorted(hits.items(), key=lambda x: (-x[1], x[0]))[:20]:
        top_u = units[t].most_common(3)
        u_s = ", ".join(f"`{u}` ({n})" for u, n in top_u)
        f_s = ", ".join(f"`{f}`" for f in sorted(files[t])[:4])
        if len(files[t]) > 4:
            f_s += ", ..."
        lines.append(f"- **`{t}`** ({c} hits): units {u_s}; files {f_s}\n")
    lines.append("\n")

    lines.append("## 3. Live schema cross-check\n\n")
    if not live_tables:
        lines.append(
            "No [`14-mysql-columns.csv`](14-mysql-columns.csv) yet. Export from MySQL with "
            "[`debug/check_mysql_hosts.py`](../../debug/check_mysql_hosts.py) (`--export --database <db>`), then run "
            "[`debug/crossref_schema_vs_code.py`](../../debug/crossref_schema_vs_code.py) and re-run this report.\n\n"
        )
    else:
        lines.append(
            f"Live schema: **{len(live_tables)}** tables"
            + (f" (`{live_schema}`)" if live_schema else "")
            + ".\n\n"
        )
        lines.append("| Category | Count | Notes |\n|----------|------:|-------|\n")
        lines.append(f"| In both code + live | {len(both)} | Safe baseline for porting |\n")
        lines.append(
            f"| Code only | {len(only_code)} | Typo, view, dynamic SQL, or other DB |\n"
        )
        lines.append(
            f"| Live only | {len(only_live)} | Other apps, batch, legacy unused \u2014 **verify before DROP** |\n"
        )
        lines.append("\n")

        lines.append("### 3.1 Code-only table names\n\n")
        if only_code:
            for t in only_code:
                lines.append(f"- `{t}` ({hits[t]} hits)\n")
        else:
            lines.append("*(none)*\n")
        lines.append(
            "\n*Closure note*: these names appear in `Sqlen`/`Sqlon` in units such as "
            "`Subu22_1`, `Subu22_2`, `Subu27`, `Subu97` (`S4_Ssub`), `Subu13_1` (`T0_Gbun`), "
            "`Subu38_2`, `Seek09` (`T8_Gbun`) under repo root. They are absent from "
            "the exported `chul_09_db` snapshot \u2014 treat as schema/tenant mismatch, not typos. "
            "See [`13-db-surface.md`](13-db-surface.md).\n\n"
        )

        lines.append("### 3.2 Live-only tables (not seen in static SQL scan)\n\n")
        lines.append(
            "*May still be used via runtime string SQL or other services. Check logs and grants before archiving.*\n\n"
        )
        if only_live:
            for t in only_live[:200]:
                lines.append(f"- `{t}`\n")
            if len(only_live) > 200:
                lines.append(f"\n... and {len(only_live) - 200} more.\n")
        else:
            lines.append("*(none)*\n")
        lines.append("\n")

    lines.append("## 4. Optimization and modernization playbook\n\n")
    lines.append(
        "1. **Soft delete / visibility**: `Base01` uses `D_Open` / `D_Select` with `` `Check` `` \u2014 ensure every query in the new stack applies the same rule or replace with explicit `deleted_at`.\n"
    )
    lines.append(
        "2. **Hot keys**: Many tables filter on `Hcode`, `Gcode`, dates \u2014 add or verify **composite indexes** matching `WHERE` clauses from [`13-db-sql-references.csv`](13-db-sql-references.csv) snippets.\n"
    )
    lines.append(
        "3. **Dead schema**: `Live only` tables \u2014 trace **MySQL user grants** and **application logs**; candidates for read-only archive or separate schema after sign-off.\n"
    )
    lines.append(
        "4. **Missing tables** (`Code only`): run **integration tests** against live DB; fix synonyms or split multi-tenant DBs.\n"
    )
    lines.append(
        "5. **Replace `Seek_Name` / socket SQL** with a typed API + transactions to simplify pooling and error handling.\n"
    )
    lines.append(
        "6. **Security**: move from shared `root` to **least-privilege** users per service; rotate passwords exposed outside secret stores.\n\n"
    )

    lines.append("## 5. Machine-readable usage CSV\n\n")
    lines.append(
        f"- [`15-db-table-usage.csv`](15-db-table-usage.csv): per-table hits, unit count, kinds, live presence.\n"
    )

    OUT_MD.write_text("".join(lines), encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "table",
                "sql_hits",
                "distinct_units",
                "kind_from",
                "kind_join",
                "kind_into",
                "kind_update",
                "kind_dfm_TableName",
                "in_live_schema",
            ]
        )
        for t in sorted(hits.keys(), key=lambda x: (-hits[x], x)):
            kt = kinds[t]
            w.writerow(
                [
                    t,
                    hits[t],
                    len(units[t]),
                    kt.get("from", 0) + kt.get("from_bt", 0),
                    kt.get("join", 0),
                    kt.get("into", 0),
                    kt.get("update", 0),
                    kt.get("dfm_TableName", 0),
                    "yes" if (live_tables and t in live_tables) else ("no" if live_tables else ""),
                ]
            )

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
