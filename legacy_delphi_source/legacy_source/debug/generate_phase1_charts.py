#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate SVG charts for phase1 stakeholder docs from existing CSV/MD inputs.

Outputs under docs/phase1-structure/figures/:
  - chart-top-sql-tables.svg
  - chart-sql-kind-mix.svg
  - chart-code-vs-live-tables.svg
  - chart-top-forms-by-components.svg  (optional, if 12-screen-specification.csv exists)

Run: pip install -r debug/requirements-charts.txt
     python3 debug/generate_phase1_charts.py
"""
from __future__ import annotations

import csv
import io
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "phase1-structure"
FIG = DOCS / "figures"
CSV13 = DOCS / "13-db-sql-references.csv"
CSV12 = DOCS / "12-screen-specification.csv"
CSV15 = DOCS / "15-db-table-usage.csv"
CROSS = DOCS / "14-db-code-vs-live.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            text = None
    else:
        text = raw.decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def parse_crossref_counts(md_path: Path) -> tuple[int, int, int] | None:
    """Return (both, code_only, live_only) from 14-db-code-vs-live.md summary table."""
    if not md_path.is_file():
        return None
    text = md_path.read_text(encoding="utf-8", errors="replace")
    both = code_only = live_only = None
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        label, val = parts[1], parts[2]
        if not val.isdigit():
            continue
        n = int(val)
        if label.startswith("In both"):
            both = n
        elif "Code only" in label:
            code_only = n
        elif "Live only" in label:
            live_only = n
    if both is None or code_only is None or live_only is None:
        return None
    return both, code_only, live_only


def main() -> int:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Install: pip install -r debug/requirements-charts.txt", file=sys.stderr)
        return 1

    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["figure.dpi"] = 120

    # --- 1) Top tables by sql_hits (15 CSV) ---
    rows15 = read_csv_rows(CSV15)
    if rows15:
        pairs: list[tuple[str, int]] = []
        for r in rows15:
            t = (r.get("table") or "").strip()
            try:
                h = int(r.get("sql_hits") or 0)
            except ValueError:
                continue
            if t:
                pairs.append((t, h))
        pairs.sort(key=lambda x: -x[1])
        top = pairs[:12]
        if top:
            fig, ax = plt.subplots(figsize=(10, 5))
            names = [p[0] for p in top]
            vals = [p[1] for p in top]
            ax.barh(names[::-1], vals[::-1], color="#2c5282")
            ax.set_xlabel("SQL reference hits (static scan)")
            ax.set_title("Top tables by SQL string hits (Chulpan closure)")
            fig.tight_layout()
            fig.savefig(FIG / "chart-top-sql-tables.svg", format="svg", bbox_inches="tight")
            plt.close(fig)

    # --- 2) SQL kind mix from 13 ---
    rows13 = read_csv_rows(CSV13)
    if rows13:
        kinds = Counter((r.get("kind") or "").strip() or "unknown" for r in rows13)
        # collapse minor
        labels = list(kinds.keys())
        sizes = [kinds[k] for k in labels]
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("SQL token kinds (from / join / update / ...)")
        fig.tight_layout()
        fig.savefig(FIG / "chart-sql-kind-mix.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

    # --- 3) Code vs live ---
    counts = parse_crossref_counts(CROSS)
    if counts:
        both, co, lo = counts
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            [both, co, lo],
            labels=["In both (code + live)", "Code only", "Live only"],
            autopct="%1.1f%%",
            colors=["#276749", "#c05621", "#718096"],
            startangle=140,
        )
        ax.set_title("Table names: static code vs live MySQL (chul_09_db)")
        fig.tight_layout()
        fig.savefig(FIG / "chart-code-vs-live-tables.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

    # --- 4) Top forms by component sum (optional) ---
    rows12 = read_csv_rows(CSV12)
    if rows12:
        numeric_cols = [
            "TDBGrid",
            "TClientDataSet",
            "TEdit",
            "TPanel",
            "TButton",
            "TWebBrowser",
        ]
        scores: list[tuple[str, int]] = []
        for r in rows12:
            inst = (r.get("instance") or "").strip()
            if not inst:
                continue
            s = 0
            for c in numeric_cols:
                try:
                    s += int((r.get(c) or "0").strip() or 0)
                except ValueError:
                    pass
            scores.append((inst, s))
        scores.sort(key=lambda x: -x[1])
        topf = scores[:15]
        if topf:
            fig, ax = plt.subplots(figsize=(10, 6))
            names = [p[0] for p in topf]
            vals = [p[1] for p in topf]
            ax.barh(names[::-1], vals[::-1], color="#553c9a")
            ax.set_xlabel("Sum of key controls (grid, CDS, edit, ??)")
            ax.set_title("Heavier screens by control counts (DFM/CSV spec)")
            fig.tight_layout()
            fig.savefig(FIG / "chart-top-forms-by-components.svg", format="svg", bbox_inches="tight")
            plt.close(fig)

    # --- 5) Wireframe SVG coverage (Form rows vs wireframes/{instance}.svg) ---
    wf_dir = DOCS / "wireframes"
    stems = {p.stem for p in wf_dir.glob("*.svg")}
    rows12b = read_csv_rows(CSV12)
    forms = [r for r in rows12b if (r.get("kind") or "").strip() == "Form"]
    if forms:
        with_svg = sum(1 for r in forms if (r.get("instance") or "").strip() in stems)
        without_svg = len(forms) - with_svg
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            [with_svg, without_svg],
            labels=["Form with wireframe SVG", "Form without SVG"],
            autopct="%1.1f%%",
            colors=["#2b6cb0", "#e2e8f0"],
            startangle=90,
        )
        ax.set_title("Screen spec Form rows vs wireframes/*.svg match")
        fig.tight_layout()
        fig.savefig(FIG / "chart-wireframe-coverage.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

    print(f"Wrote charts under {FIG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
