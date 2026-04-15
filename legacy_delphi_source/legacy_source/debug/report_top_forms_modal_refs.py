#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rank Form rows in 12-screen-specification.csv by showmodal_refs proxy
((+N) suffix or ;;-separated ref count). Phase1 proxy for modal-heavy screens.

Run from project root:
  python3 debug/report_top_forms_modal_refs.py
  python3 debug/report_top_forms_modal_refs.py --top 15
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV12 = ROOT / "docs" / "phase1-structure" / "12-screen-specification.csv"


def modal_score(cell: str) -> int:
    if not cell or not cell.strip():
        return 0
    m = re.search(r"\(\+(\d+)\)\s*$", cell.strip())
    if m:
        return int(m.group(1))
    return cell.count(";;") + 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=20, help="number of rows to print")
    args = ap.parse_args()

    if not CSV12.is_file():
        print("Missing:", CSV12, file=sys.stderr)
        return 1

    raw = CSV12.read_bytes()
    text = None
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode("utf-8", errors="replace")

    rows = list(csv.DictReader(io.StringIO(text)))
    forms = [r for r in rows if (r.get("kind") or "").strip() == "Form"]
    scored = []
    for r in forms:
        inst = (r.get("instance") or "").strip()
        cap = (r.get("caption_dfm") or "").strip()
        sm = modal_score(r.get("showmodal_refs") or "")
        scored.append((sm, inst, cap))
    scored.sort(key=lambda x: -x[0])

    print(f"Forms: {len(forms)}  (from {CSV12.name})\n")
    print(f"{'score':>6}  {'instance':<12}  caption")
    for sm, inst, cap in scored[: args.top]:
        cap_short = (cap[:40] + "...") if len(cap) > 41 else cap
        print(f"{sm:6d}  {inst:<12}  {cap_short}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
