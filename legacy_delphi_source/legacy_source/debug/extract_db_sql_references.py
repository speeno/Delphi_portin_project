#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Chulpan.dpr build closure (.pas + sibling .dfm) for SQL table-like tokens.

Writes:
  docs/phase1-structure/13-db-sql-references.csv
  docs/phase1-structure/13-db-surface.md

Depends on debug/delphi_build_closure.py (same directory).
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

_DEBUG = Path(__file__).resolve().parent
if str(_DEBUG) not in sys.path:
    sys.path.insert(0, str(_DEBUG))

from delphi_build_closure import ROOT, closure_from_dpr  # noqa: E402

OUT_DIR = ROOT / "docs" / "phase1-structure"
CSV_PATH = OUT_DIR / "13-db-sql-references.csv"
MD_PATH = OUT_DIR / "13-db-surface.md"

# SQL clause -> (regex for identifier after keyword, kind tag)
SQL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)\bfrom\s+([A-Za-z_][A-Za-z0-9_]*)"), "from"),
    (re.compile(r"(?i)\bjoin\s+([A-Za-z_][A-Za-z0-9_]*)"), "join"),
    (re.compile(r"(?i)\binto\s+([A-Za-z_][A-Za-z0-9_]*)"), "into"),
    (re.compile(r"(?i)\bupdate\s+([A-Za-z_][A-Za-z0-9_]*)"), "update"),
]

# Backtick-wrapped MySQL identifiers on same line as From
BACKTICK_FROM = re.compile(r"(?i)\bfrom\s+`([A-Za-z0-9_]+)`")

# Zeos / VCL DFM
DFM_TABLE = re.compile(r"^\s*TableName\s*=\s*'([^']+)'", re.MULTILINE)

# Skip obvious non-table tokens (Delphi / SQL noise)
SKIP_NAMES = frozenset(
    {
        "string",
        "integer",
        "boolean",
        "true",
        "false",
        "nil",
        "null",
        "asc",
        "desc",
        "and",
        "or",
        "not",
        "as",
        "on",
        "is",
        "in",
        "like",
        "between",
        "case",
        "when",
        "then",
        "else",
        "end",
        "begin",
        "select",
        "where",
        "group",
        "order",
        "having",
        "limit",
        "union",
        "all",
        "distinct",
        "values",
        "set",
        "dual",
    }
)


def strip_brace_comments(text: str) -> str:
    """Remove Pascal { ... } comments (non-nested, greedy per segment)."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if text[i] == "{":
            j = text.find("}", i + 1)
            if j == -1:
                out.append(text[i:])
                break
            i = j + 1
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def scan_pas(path: Path) -> list[tuple[str, str, int, str, str]]:
    """Yield (table, kind, line_no, rel_path, snippet)."""
    try:
        raw = path.read_bytes()
    except OSError:
        return []
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")

    text = strip_brace_comments(text)
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    hits: list[tuple[str, str, int, str, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("//") or not stripped:
            continue
        for pat, kind in SQL_PATTERNS:
            for m in pat.finditer(line):
                name = m.group(1)
                if len(name) < 2 or name.lower() in SKIP_NAMES:
                    continue
                snip = line.strip()
                if len(snip) > 160:
                    snip = snip[:157] + "..."
                hits.append((name, kind, line_no, rel, snip))
        for m in BACKTICK_FROM.finditer(line):
            name = m.group(1)
            if len(name) < 2:
                continue
            snip = line.strip()
            if len(snip) > 160:
                snip = snip[:157] + "..."
            hits.append((name, "from_bt", line_no, rel, snip))
    return hits


def scan_dfm(path: Path) -> list[tuple[str, str, int, str, str]]:
    if not path.is_file():
        return []
    try:
        b = path.read_bytes()[:8192]
    except OSError:
        return []
    if b.startswith(b"TPF0") or b"\x00" in b[:200]:
        return []
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return []
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    hits: list[tuple[str, str, int, str, str]] = []
    for m in DFM_TABLE.finditer(text):
        name = m.group(1).strip()
        if not name or len(name) < 1:
            continue
        line_no = text[: m.start()].count("\n") + 1
        hits.append((name, "dfm_TableName", line_no, rel, f"TableName='{name}'"))
    return hits


def main() -> None:
    units, missing = closure_from_dpr()
    pas_paths = [p for _, p in units]

    all_rows: list[tuple[str, str, str, int, str, str]] = []
    # table -> set of units
    table_units: defaultdict[str, set[str]] = defaultdict(set)

    for pas in pas_paths:
        unit_stem = pas.stem
        for table, kind, line_no, rel, snip in scan_pas(pas):
            all_rows.append((table, kind, rel, line_no, unit_stem, snip))
            table_units[table].add(unit_stem)
        dfm = pas.with_suffix(".dfm")
        for table, kind, line_no, rel, snip in scan_dfm(dfm):
            all_rows.append((table, kind, rel, line_no, unit_stem, snip))
            table_units[table].add(unit_stem)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["table", "kind", "file", "line", "unit", "snippet"])
        for table, kind, rel, line_no, unit_stem, snip in sorted(
            all_rows, key=lambda x: (x[0].lower(), x[2], x[3])
        ):
            w.writerow([table, kind, rel, line_no, unit_stem, snip])

    counts = Counter(r[0] for r in all_rows)
    top = counts.most_common(40)

    md: list[str] = []
    md.append("# DB SQL surface (Chulpan.dpr build closure)\n\n")
    md.append("Generated by [`debug/extract_db_sql_references.py`](../../debug/extract_db_sql_references.py).\n\n")
    md.append("## Scope\n\n")
    md.append(
        f"- **PAS files scanned**: {len(pas_paths)} (recursive `uses` closure from [`Chulpan.dpr`](../../Chulpan.dpr), same as [`01-build-closure.md`](01-build-closure.md)).\n"
    )
    md.append(
        "- **Heuristics**: case-insensitive `FROM` / `JOIN` / `INTO` / `UPDATE` + identifier; `FROM \\`name\\``; DFM `TableName='...'` next to each unit when the `.dfm` is text.\n"
    )
    md.append(
        "- **Not detected**: table names built at runtime (string concatenation); dynamic placeholders (`@F11`); comments or binary DFMs.\n"
    )
    md.append(
        "- **Ground truth**: validate against a live MySQL schema or `mysqldump`; this inventory is **code reference only**.\n\n"
    )
    if missing:
        md.append("## DPR path warnings\n\n")
        for m in missing[:20]:
            md.append(f"- {m}\n")
        md.append("\n")

    md.append("## Row file\n\n")
    md.append(
        f"- [`13-db-sql-references.csv`](13-db-sql-references.csv) ({len(all_rows)} rows).\n\n"
    )

    md.append("## Tables by hit count (top 40)\n\n")
    md.append("| table | hits | units (count) |\n")
    md.append("|-------|-----:|----------------:|\n")
    for name, c in top:
        u_n = len(table_units.get(name, ()))
        md.append(f"| `{name}` | {c} | {u_n} |\n")
    md.append("\n")

    md.append("## Examples (known core tables)\n\n")
    for t in ("Id_Logn", "G1_Ggeo", "G2_Ggwo", "G4_Book", "G7_Ggeo"):
        if t in counts:
            md.append(f"- `{t}`: **{counts[t]}** hit(s) in closure.\n")
        else:
            md.append(f"- `{t}`: *(not found by heuristic ? check spelling or dynamic SQL)*\n")
    md.append("\n")

    MD_PATH.write_text("".join(md), encoding="utf-8")
    print(f"Wrote {CSV_PATH} rows={len(all_rows)}")
    print(f"Wrote {MD_PATH}")


if __name__ == "__main__":
    main()
