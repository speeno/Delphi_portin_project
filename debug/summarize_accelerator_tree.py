#!/usr/bin/env python3
"""Accelerator 산출물(*.tree.json / *.pas_analysis.json) 요약기.

Phase F 누락 3화면(Sobo12/13/15) layout_mappings 작성을 위한 입력 추출용.
- 최상위 패널/그리드 구조 + TabOrder
- DBGrid 컬럼(FieldName/Title.Caption/Width/정렬)
- 입력 위젯(Edit/ComboBox/CheckBox) TabOrder 순
- 이벤트 핸들러 목록(.pas_analysis.json sql_calls 의 테이블도)

사용: python3 debug/summarize_accelerator_tree.py <Subu12> [<Subu13> ...]
인자 없으면 Subu12 Subu13 Subu15 기본.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_GEN = _REPO / "tools" / "delphi_porting_accelerator" / "examples" / "generated" / "legacy_source_root"

_INPUT_CLASSES = {
    "TFlatEdit", "TFlatMaskEdit", "TFlatNumber", "TFlatComboBox",
    "TFlatCheckBox", "TEdit", "TComboBox", "TCheckBox", "TDateEdit", "TMemo",
}
_BUTTON_CLASSES = {"TdxButton", "TFlatButton", "TFlatSpeedButton", "TButton", "TBitBtn"}


def _events(props: dict) -> dict:
    return {k: v for k, v in props.items() if k.startswith("On")}


def _summarize_grid(node: dict) -> dict:
    cols = node["props"].get("Columns") or []
    out_cols = []
    for c in cols:
        out_cols.append({
            "field": c.get("FieldName"),
            "title": c.get("Title.Caption"),
            "width": c.get("Width"),
            "align": c.get("Title.Alignment"),
            "visible": c.get("Visible", True),
        })
    return {
        "name": node["name"],
        "datasource": node["props"].get("DataSource"),
        "events": _events(node["props"]),
        "columns": out_cols,
    }


def _walk(node: dict, depth: int, top_panels: list, grids: list, inputs: list, buttons: list) -> None:
    cls = node.get("class_name", "")
    props = node.get("props", {})
    name = node.get("name", "")
    if cls == "TDBGrid" or cls == "TDBGridEh":
        grids.append(_summarize_grid(node))
    if cls in _INPUT_CLASSES:
        inputs.append({
            "name": name, "class": cls, "tab": props.get("TabOrder"),
            "caption": props.get("Caption"), "maxlen": props.get("MaxLength"),
            "enabled": props.get("Enabled", True), "events": _events(props),
        })
    if cls in _BUTTON_CLASSES:
        buttons.append({
            "name": name, "class": cls, "caption": props.get("Caption"),
            "tab": props.get("TabOrder"), "enabled": props.get("Enabled", True),
            "onclick": props.get("OnClick"),
        })
    for ch in node.get("children") or []:
        _walk(ch, depth + 1, top_panels, grids, inputs, buttons)


def summarize(stem: str) -> dict:
    form = "Sobo" + stem.replace("Subu", "")
    tree = json.loads((_GEN / stem / f"{form}.tree.json").read_text(encoding="utf-8"))
    pas_path = _GEN / stem / f"{form}.pas_analysis.json"
    pas = json.loads(pas_path.read_text(encoding="utf-8")) if pas_path.is_file() else {}

    top_panels = []
    for ch in tree.get("children") or []:
        cls = ch.get("class_name", "")
        if cls in ("TFlatPanel", "TPanel"):
            top_panels.append({
                "name": ch["name"], "tab": ch["props"].get("TabOrder"),
                "caption": ch["props"].get("Caption"),
                "child_classes": sorted({c.get("class_name") for c in ch.get("children") or []}),
            })
        elif cls in ("TDataSource",):
            top_panels.append({"name": ch["name"], "dataset": ch["props"].get("DataSet")})

    grids: list = []
    inputs: list = []
    buttons: list = []
    _walk(tree, 0, top_panels, grids, inputs, buttons)
    inputs.sort(key=lambda x: (x["tab"] is None, x["tab"] or 0))

    tables = sorted({
        t for call in (pas.get("sql_calls") or [])
        for t in ([call.get("table")] if isinstance(call, dict) else [])
        if t
    })

    return {
        "form": form,
        "caption": tree["props"].get("Caption"),
        "top_level": top_panels,
        "grids": grids,
        "inputs": inputs,
        "buttons": buttons,
        "event_handler_count": len(pas.get("event_handlers") or []),
        "sql_tables": tables,
    }


def main() -> None:
    stems = sys.argv[1:] or ["Subu12", "Subu13", "Subu15"]
    for stem in stems:
        print("=" * 70)
        print(json.dumps(summarize(stem), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
