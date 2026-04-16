"""
dfm2html_project 의 DfmParser 로 .dfm 을 읽어 기존 parse_dfm_layout 과 호환되는 JSON 을 만든다.

- 인코딩: delphi_source_encoding.read_delphi_source
- IR: dfm_layout_ir.enrich_layout_document
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_TOOLS = Path(__file__).resolve().parent
_PARSERS = _TOOLS / "parsers"
_DFM2HTML = _TOOLS / "dfm2html_project"

if str(_PARSERS) not in sys.path:
    sys.path.insert(0, str(_PARSERS))
if str(_DFM2HTML) not in sys.path:
    sys.path.insert(0, str(_DFM2HTML))

from delphi_source_encoding import read_delphi_source  # noqa: E402
from dfm_grid_columns import extract_grid_columns  # noqa: E402
from dfm_layout_ir import enrich_layout_document  # noqa: E402
from dfm_parser import LAYOUT_EXPORT_KEYS, is_binary_dfm_text  # noqa: E402
from delphi_string_normalize import normalize_delphi_display_string  # noqa: E402
from delphi_scalar import layout_value_as_str  # noqa: E402


def _props_to_layout(props: dict[str, Any]) -> dict[str, Any]:
    lay: dict[str, Any] = {}
    for k, v in props.items():
        if k.startswith("On"):
            continue
        if k in LAYOUT_EXPORT_KEYS:
            if k in ("Caption", "Text", "Hint") and isinstance(v, str):
                lay[k] = normalize_delphi_display_string(v)
            else:
                lay[k] = layout_value_as_str(v)
        elif k.startswith("Font."):
            lay[k] = layout_value_as_str(v)
        elif k.startswith("Items"):
            if isinstance(v, list):
                lay[k] = "\n".join(layout_value_as_str(x) for x in v)
            else:
                lay[k] = layout_value_as_str(v)
        elif k.endswith(".Data"):
            lay[k] = layout_value_as_str(v)

    cols = props.get("Columns")
    if isinstance(cols, list):
        gc: list[dict[str, Any]] = []
        for it in cols:
            if not isinstance(it, dict):
                continue
            fn = it.get("FieldName")
            tc = it.get("Title.Caption")
            gc.append(
                {
                    "field_name": None if fn is None else layout_value_as_str(fn),
                    "title": None if tc is None else layout_value_as_str(tc),
                }
            )
        if gc:
            lay["grid_columns"] = gc
    elif isinstance(cols, str) and "item" in cols.lower():
        ec = extract_grid_columns(cols)
        if ec:
            lay["grid_columns"] = ec
    return lay


def _events_from_props(props: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in props.items():
        if not k.startswith("On"):
            continue
        if v is None or v is False or v == "":
            continue
        out[k] = layout_value_as_str(v)
    return out


def _conv(node: Any, depth: int) -> dict[str, Any]:
    props = node.props
    return {
        "name": node.name,
        "type": node.class_name,
        "depth": depth,
        "layout": _props_to_layout(props),
        "events": _events_from_props(props),
        "children": [_conv(ch, depth + 1) for ch in node.children],
    }


def parse_dfm_layout_via_dfm2html(filepath: str) -> dict[str, Any]:
    """dfm2html DfmParser 기반 레이아웃 문서(레거리 스키마 + engine 필드)."""
    content = read_delphi_source(filepath)

    if is_binary_dfm_text(content):
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "binary_dfm_unsupported",
            "root": None,
            "parse_error": "binary TPF0 DFM — 텍스트 변환 후 파싱하세요",
            "engine": "dfm2html",
        }

    from dfm2html.parser.dfm_parser import DfmParser  # noqa: PLC0415

    parser = DfmParser()
    try:
        root_node = parser.parse(content)
    except ValueError as e:
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "unknown",
            "root": None,
            "parse_error": str(e),
            "engine": "dfm2html",
        }

    doc: dict[str, Any] = {
        "file": filepath,
        "form_name": root_node.name,
        "form_class": root_node.class_name,
        "root": _conv(root_node, 0),
        "engine": "dfm2html",
    }
    if doc.get("root") is not None:
        enrich_layout_document(doc)
    return doc
