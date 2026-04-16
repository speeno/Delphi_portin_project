#!/usr/bin/env python3
"""
Subu36.dfm 레이아웃 감사: Caption 없는 컨트롤·그리드 컬럼 수 등을 debug/subu36_layout_audit.json 에 기록.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from dfm_parser import parse_dfm_component_tree, parse_dfm_layout  # noqa: E402


def _walk(comp: dict, path: str, out: dict) -> None:
    name = comp.get("name", "")
    typ = comp.get("type", "")
    props = comp.get("properties") or {}
    cap = (props.get("Caption") or "").strip()
    p = f"{path}/{name}" if path else name
    if not cap and typ not in ("TForm", "TSobo36", "TFlatPanel", "TPanel"):
        has_glyph = bool(props.get("Glyph.Data"))
        out["captionless"].append(
            {
                "path": p,
                "type": typ,
                "has_glyph": has_glyph,
                "has_hint": bool((props.get("Hint") or "").strip()),
            }
        )
    cols = props.get("Columns")
    if isinstance(cols, str) and "Title.Caption" in cols:
        out["grids_with_columns_blob"].append(
            {"path": p, "type": typ, "blob_chars": len(cols)}
        )
    for ch in comp.get("children") or []:
        _walk(ch, p, out)


def main() -> None:
    dfm = _REPO / "legacy_delphi_source" / "legacy_source" / "Data" / "Subu36.dfm"
    if not dfm.is_file():
        print("Subu36.dfm not found", file=sys.stderr)
        sys.exit(1)
    root = parse_dfm_component_tree(str(dfm))
    layout_doc = parse_dfm_layout(str(dfm))
    audit: dict = {
        "source": str(dfm.relative_to(_REPO)),
        "captionless": [],
        "grids_with_columns_blob": [],
    }
    if root:
        _walk(root, "", audit)
    gc = []
    lay_root = layout_doc.get("root")

    def walk_layout(node: dict) -> None:
        lay = node.get("layout") or {}
        if lay.get("grid_columns"):
            gc.append(
                {
                    "name": node.get("name"),
                    "type": node.get("type"),
                    "column_count": len(lay["grid_columns"]),
                    "titles": [c.get("title") for c in lay["grid_columns"][:5]],
                }
            )
        for c in node.get("children") or []:
            walk_layout(c)

    if lay_root:
        walk_layout(lay_root)
    audit["layout_grid_columns_preview"] = gc
    out_path = _REPO / "debug" / "subu36_layout_audit.json"
    out_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
