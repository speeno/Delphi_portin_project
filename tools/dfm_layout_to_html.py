#!/usr/bin/env python3
"""
레이아웃 JSON(parse_dfm_layout / dfm_layout_export 출력)을 단순 절대 배치 HTML로 변환한다.

Delphi 좌표는 부모 클라이언트 기준 — 중첩 div + position:relative/absolute 로 근사한다.
layout_ir(Anchors·Align·TabOrder)가 있으면 z-index·정렬·앵커 힌트를 반영한다.
컴포넌트 종류 → HTML 매핑은 dfm_component_registry.json 에서 로드한다.

사용법:
  python3 tools/dfm_layout_to_html.py <layout.json> <out.html>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PARSERS = _ROOT / "parsers"
if str(_PARSERS) not in sys.path:
    sys.path.insert(0, str(_PARSERS))

from delphi_scalar import COLOR_MAP  # noqa: E402
from delphi_string_normalize import normalize_delphi_display_string  # noqa: E402
from dfm_layout_ir import enrich_layout_document, parse_anchors  # noqa: E402


def _load_registry() -> dict:
    p = _ROOT / "dfm_component_registry.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


_REGISTRY: dict | None = None


def _registry() -> dict:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _load_registry()
    return _REGISTRY


def _type_kind(typ: str) -> str | None:
    kinds = _registry().get("kinds") or {}
    for kind, names in kinds.items():
        if typ in names:
            return kind
    return None


def delphi_px(val: str | None) -> str | None:
    """숫자 리터럴만 px로 취급(식은 무시)."""
    if val is None:
        return None
    v = val.strip().strip("'\"")
    m = re.match(r"^-?\d+", v)
    if not m:
        return None
    return f"{m.group()}px"


def delphi_caption(val: str | None) -> str:
    """레이아웃 JSON 값을 HTML 안전 문자열로(델파이 문자열 연결·#NNN 정규화)."""
    return html.escape(normalize_delphi_display_string(val))


def cmp_style(layout: dict, layout_ir: dict | None = None) -> str:
    layout_ir = layout_ir or {}
    parts = ["position:absolute", "box-sizing:border-box"]

    align = (layout_ir.get("align") or layout.get("Align") or "").strip().lower()
    anchors = list(layout_ir.get("anchors") or [])
    if not anchors and layout.get("Anchors"):
        anchors = parse_anchors(layout.get("Anchors"))

    pos: dict[str, str] = {}
    for key, css in (("Left", "left"), ("Top", "top"), ("Width", "width"), ("Height", "height")):
        px = delphi_px(layout.get(key))
        if px:
            pos[css] = px

    if align == "alclient":
        pos = {"left": "0", "top": "0", "width": "100%", "height": "100%"}
    elif align == "altop":
        pos["left"] = pos.get("left", "0")
        pos["top"] = pos.get("top", "0")
        pos["width"] = pos.get("width", "100%")
    elif align == "albottom":
        pos["left"] = pos.get("left", "0")
        pos["bottom"] = "0"
        pos["width"] = pos.get("width", "100%")
    elif align == "alleft":
        pos["left"] = pos.get("left", "0")
        pos["top"] = pos.get("top", "0")
        pos["height"] = pos.get("height", "100%")

    if "akLeft" in anchors and "akRight" in anchors:
        pos.pop("width", None)
        pos["left"] = "0"
        pos["right"] = "0"
        pos["width"] = "auto"
    elif "akRight" in anchors and "akLeft" not in anchors:
        pos.pop("left", None)
        pos["right"] = "0"

    if "akTop" in anchors and "akBottom" in anchors:
        pos.pop("height", None)
        pos["top"] = "0"
        pos["bottom"] = "0"
        pos["height"] = "auto"
    elif "akBottom" in anchors and "akTop" not in anchors:
        pos.pop("top", None)
        pos["bottom"] = "0"

    for css, val in pos.items():
        parts.append(f"{css}:{val}")

    vis = layout.get("Visible", "").strip().lower()
    if vis == "false":
        parts.append("visibility:hidden")

    col = (layout.get("Color") or "").strip()
    if col in COLOR_MAP:
        parts.append(f"background:{COLOR_MAP[col]}")

    zi = layout_ir.get("z_index")
    if zi is not None:
        parts.append(f"z-index:{10 + int(zi)}")

    return ";".join(parts)


def _node_display_label(
    layout: dict,
    node_name_plain: str,
    typ: str,
    kind: str | None,
) -> str:
    """Caption→Text→Hint→(버튼 등)컴포넌트 이름→타입명 순으로 HTML 조각을 만든다."""
    for key in ("Caption", "Text", "Hint"):
        frag = delphi_caption(layout.get(key))
        if frag:
            return frag
    nm = (node_name_plain or "").strip()
    if kind == "button":
        return html.escape(nm) if nm else ""
    if kind in ("label", "checkbox") and nm:
        return html.escape(nm)
    return html.escape(typ)


def _render_pagecontrol_sheets(sheets: list[dict], parent_typ: str) -> str:
    tabs: list[str] = []
    panels: list[str] = []
    for i, sheet in enumerate(sheets):
        lay = sheet.get("layout") or {}
        cap = delphi_caption(lay.get("Caption"))
        label = cap or html.escape(sheet.get("name", ""))
        tabs.append(
            f'<button type="button" class="delphi-tab" role="tab" data-idx="{i}">{label}</button>'
        )
        body = "".join(render_node(c, False, parent_typ) for c in (sheet.get("children") or []))
        panels.append(
            '<div class="delphi-tabpanel" role="tabpanel" data-idx="'
            f'{i}" style="position:relative;min-height:48px;border:1px solid #bbb;margin-top:4px">'
            f'<div class="delphi-panel" style="width:100%;height:100%;border:1px dashed #888;background:#fafafa">'
            f"{body}</div></div>"
        )
    return (
        '<div class="delphi-pagecontrol" style="display:flex;flex-direction:column;'
        'width:100%;height:100%">'
        '<div class="delphi-tabstrip" role="tablist" style="display:flex;gap:4px;flex-wrap:wrap">'
        f'{"".join(tabs)}</div>'
        '<div class="delphi-tabpanels" style="flex:1;min-height:0">'
        f'{"".join(panels)}</div></div>'
    )


def render_node(node: dict, is_root: bool = False, parent_typ: str = "") -> str:
    name_plain = node.get("name") or ""
    name = html.escape(name_plain)
    typ = node.get("type", "")
    layout = node.get("layout") or {}
    layout_ir = node.get("layout_ir") or {}
    typ_esc = html.escape(typ)
    children: list[dict] = list(node.get("children") or [])
    kind = _type_kind(typ)
    label = _node_display_label(layout, name_plain, typ, kind)

    if kind == "pagecontrol":
        sheets = [c for c in children if c.get("type") == "TTabSheet"]
        rest = [c for c in children if c.get("type") != "TTabSheet"]
        inner_pc = _render_pagecontrol_sheets(sheets, typ)
        inner_rest = "".join(render_node(c, False, typ) for c in rest)
        inner_children = inner_pc + inner_rest
    else:
        inner_children = "".join(render_node(c, False, typ) for c in children)

    container_style = cmp_style(layout, layout_ir) + ";position:relative;overflow:visible"
    inner = ""

    if is_root and layout.get("ClientWidth") and layout.get("ClientHeight"):
        cw = delphi_px(layout.get("ClientWidth"))
        ch = delphi_px(layout.get("ClientHeight"))
        wh = ""
        if cw and ch:
            wh = f"width:{cw};height:{ch};"
        inner = (
            f'<div class="delphi-form-root" style="{wh}position:relative;'
            f'border:1px solid #444;background:var(--delphi-form-bg,#f0f0f0)">'
        )
        inner += inner_children
        inner += "</div>"
    elif kind == "button":
        inner = f'<button type="button" class="delphi-btn" style="min-width:40px">{label}</button>'
    elif kind == "edit":
        inner = f'<input type="text" class="delphi-edit" placeholder="{name}" style="width:100%;height:100%" readonly />'
    elif kind == "label":
        inner = f'<span class="delphi-label" style="white-space:pre-wrap;font-size:12px">{label}</span>'
    elif kind == "checkbox":
        inner = f'<label class="delphi-checkbox"><input type="checkbox" disabled /> {label}</label>'
    elif kind == "memo":
        inner = '<textarea class="delphi-memo" readonly style="width:100%;height:100%"></textarea>'
    elif kind == "panel":
        inner = f'<div class="delphi-panel" style="border:1px dashed #888;background:#fafafa;width:100%;height:100%">{inner_children}</div>'
    elif kind == "grid":
        cols = layout.get("grid_columns") or []
        hdr_cells: list[str] = []
        if cols:
            for idx, c in enumerate(cols):
                raw_t = c.get("title") or c.get("field_name") or ""
                cell = delphi_caption(str(raw_t) if raw_t is not None else "")
                br = "" if idx == len(cols) - 1 else "border-right:1px solid #bbb;"
                hdr_cells.append(
                    f'<div style="flex:1;min-width:40px;padding:2px 6px;{br}">{cell or "&nbsp;"}</div>'
                )
        else:
            hdr_cells = [
                '<div style="flex:1;padding:2px 6px;border-right:1px solid #bbb">A</div>',
                '<div style="flex:1;padding:2px 6px;border-right:1px solid #bbb">B</div>',
                '<div style="flex:1;padding:2px 6px">C</div>',
            ]
        inner = (
            '<div class="delphi-grid-inner" style="display:flex;flex-direction:column;'
            'height:100%;font-size:11px;color:#333">'
            '<div class="delphi-grid-header" style="display:flex;border-bottom:1px solid #999;'
            'background:#dde">'
            f'{"".join(hdr_cells)}'
            "</div>"
            '<div class="delphi-grid-body" style="flex:1;overflow:auto;background:#eee;padding:4px">'
            f"[{typ_esc}]</div></div>"
        )
    else:
        inner = (
            f'<div class="delphi-unknown" style="border:1px dotted #aaa;background:#fff;'
            f'width:100%;height:100%;font-size:10px">{typ_esc}<br/>{name}{inner_children}</div>'
        )

    return (
        f'<div class="delphi-node" data-type="{html.escape(typ)}" data-name="{name}" '
        f'style="{container_style}">{inner}</div>'
    )


def build_html(doc: dict) -> str:
    enrich_layout_document(doc)
    root = doc.get("root")
    title = html.escape(doc.get("form_name", "Form"))
    body = "<p>root 없음</p>" if not root else render_node(root, is_root=True)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      --delphi-form-bg: #f0f0f0;
      --delphi-btn-face: #f0f0f0;
      --delphi-grid-header: #ddeeee;
    }}
    body {{ margin: 16px; font-family: system-ui, sans-serif; }}
    .delphi-node {{ font-size: 12px; }}
    .delphi-form-root .delphi-node {{ font-size: 12px; }}
    .delphi-btn {{ background: var(--delphi-btn-face); border: 1px solid #888; border-radius: 2px; }}
  </style>
</head>
<body>
  <h1 style="font-size:14px">{title} <small>({html.escape(doc.get("form_class", ""))})</small></h1>
  {body}
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <layout.json> <out.html>", file=sys.stderr)
        sys.exit(1)
    layout_path = sys.argv[1]
    out_path = sys.argv[2]
    doc = json.loads(Path(layout_path).read_text(encoding="utf-8"))
    html_out = build_html(doc)
    Path(out_path).write_text(html_out, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
