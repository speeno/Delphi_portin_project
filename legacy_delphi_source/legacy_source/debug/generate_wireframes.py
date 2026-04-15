#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wireframe SVGs from text DFM layout (+ CSV fallback from 12-screen-specification).

Usage:
  python3 debug/generate_wireframes.py              # priority screens only
  python3 debug/generate_wireframes.py --all        # all forms with text DFM
  python3 debug/generate_wireframes.py --max 20     # cap output count
"""
from __future__ import annotations

import argparse
import csv
import html
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "docs" / "phase1-structure" / "12-screen-specification.csv"
OUT_DIR = ROOT / "docs" / "phase1-structure" / "wireframes"

# Draw rects with this min area, or if type matches
MIN_AREA = 2800
DRAW_TYPES = frozenset(
    {
        "TPanel",
        "TDBGrid",
        "TDBGridEh",
        "TGroupBox",
        "TPageControl",
        "TTabSheet",
        "TScrollBox",
        "TSplitter",
        "TToolBar",
        "TStatusBar",
        "TStringGrid",
        "TMemo",
        "TRichEdit",
    }
)
SKIP_TYPES = frozenset(
    {
        "TLabel",
        "TEdit",
        "TButton",
        "TSpeedButton",
        "TCheckBox",
        "TRadioButton",
        "TComboBox",
        "TDateTimePicker",
        "TCornerButton",
    }
)

# Draw small controls when DFM has Caption (field labels, buttons)
LABEL_LIKE_TYPES = frozenset(
    {
        "TLabel",
        "TStaticText",
        "TmyLabel3d",
    }
)
BUTTON_CAPTION_TYPES = frozenset(
    {
        "TButton",
        "TBitBtn",
        "TSpeedButton",
        "TFlatButton",
    }
)


def read_text_maybe_cp949(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def is_probably_text_dfm(path: Path) -> bool:
    try:
        b = path.read_bytes()[:4096]
    except OSError:
        return False
    if b.startswith(b"TPF0") or b"\x00" in b[:200]:
        return False
    return True


def int_prop(props: dict[str, str], key: str, default: int = 0) -> int:
    v = props.get(key)
    if not v:
        return default
    m = re.search(r"-?\d+", v)
    return int(m.group(0)) if m else default


@dataclass
class DfmNode:
    name: str
    typ: str
    props: dict[str, str] = field(default_factory=dict)
    children: list[DfmNode] = field(default_factory=list)


def parse_dfm_tree(text: str) -> DfmNode | None:
    lines = text.splitlines()
    root: DfmNode | None = None
    stack: list[DfmNode] = []
    prop_re = re.compile(r"^(\s+)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")

    for raw in lines:
        line = raw.rstrip("\n\r")
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("object ") and ":" in stripped:
            m = re.match(r"object (\w+): (\w+)", stripped)
            if not m:
                continue
            name, typ = m.group(1), m.group(2)
            node = DfmNode(name, typ)
            if root is None:
                root = node
                stack = [node]
            else:
                stack[-1].children.append(node)
                stack.append(node)
        elif stripped == "end":
            if len(stack) > 1:
                stack.pop()
        else:
            if not stack:
                continue
            pm = prop_re.match(line)
            if pm:
                spaces, key, val = pm.group(1), pm.group(2), pm.group(3).strip()
                if len(spaces) >= 2 and key not in ("object", "inherited", "inline"):
                    stack[-1].props[key] = val
    return root


def collect_rects(
    node: DfmNode,
    ax: int,
    ay: int,
    out: list[tuple[str, str, int, int, int, int, str]],
) -> None:
    l = int_prop(node.props, "Left", 0)
    t = int_prop(node.props, "Top", 0)
    w = int_prop(node.props, "Width", 0)
    h = int_prop(node.props, "Height", 0)
    nx, ny = ax + l, ay + t
    area = max(0, w) * max(0, h)
    if w > 0 and h > 0:
        drew_main = False
        if node.typ in SKIP_TYPES and area < MIN_AREA * 3:
            pass
        elif node.typ in DRAW_TYPES or area >= MIN_AREA:
            if node.typ not in SKIP_TYPES or area >= MIN_AREA:
                lbl = display_label_for_node(node)
                out.append((node.name, node.typ, nx, ny, w, h, lbl))
                drew_main = True
        if not drew_main and node.typ in LABEL_LIKE_TYPES and area >= 40:
            cap = parse_dfm_string_value(node.props.get("Caption", ""))
            if cap:
                out.append((node.name, node.typ, nx, ny, w, h, cap))
        elif not drew_main and node.typ in BUTTON_CAPTION_TYPES and area >= 160:
            cap = parse_dfm_string_value(node.props.get("Caption", ""))
            if cap:
                out.append((node.name, node.typ, nx, ny, w, h, cap))
    for child in node.children:
        collect_rects(child, nx, ny, out)


def root_client_size(root: DfmNode) -> tuple[int, int]:
    cw = int_prop(root.props, "ClientWidth", 0)
    ch = int_prop(root.props, "ClientHeight", 0)
    if cw <= 0:
        cw = int_prop(root.props, "Width", 640)
    if ch <= 0:
        ch = int_prop(root.props, "Height", 480)
    return cw, ch


def strip_caption(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    return s


def parse_dfm_string_value(raw: str) -> str:
    """
    Parse right-hand side of DFM property: 'a'#13#10'b' or 'x''y' (escaped quote).
    Returns a single-line display string (newlines -> space).
    """
    raw = raw.strip()
    if not raw:
        return ""
    parts: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        if raw[i] == "'":
            i += 1
            chunk: list[str] = []
            while i < n:
                if raw[i] == "'" and i + 1 < n and raw[i + 1] == "'":
                    chunk.append("'")
                    i += 2
                elif raw[i] == "'":
                    break
                else:
                    chunk.append(raw[i])
                    i += 1
            parts.append("".join(chunk))
            i += 1
            continue
        m = re.match(r"#(\d+)", raw[i:])
        if m:
            c = int(m.group(1))
            if c in (13, 10):
                parts.append(" ")
            elif 32 <= c < 127:
                parts.append(chr(c))
            i += len(m.group(0))
            continue
        i += 1
    s = "".join(parts)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def display_label_for_node(node: DfmNode) -> str:
    """Prefer user-visible Caption/Text; else short type or object name."""
    for key in ("Caption", "Text", "SimpleText"):
        raw = node.props.get(key)
        if not raw:
            continue
        text = parse_dfm_string_value(raw)
        if text:
            return text
    # Grids / data areas often have no caption in DFM
    if "Grid" in node.typ or node.typ in ("TMemo", "TRichEdit", "TStringGrid"):
        return node.typ
    return node.typ


def svg_escape(s: str) -> str:
    return html.escape(s, quote=True)


def build_svg_from_dfm(
    root: DfmNode,
    title: str,
    subtitle: str,
    max_side: float = 1100.0,
) -> str:
    cw, ch = root_client_size(root)
    cw, ch = max(cw, 200), max(ch, 150)
    rects: list[tuple[str, str, int, int, int, int, str]] = []
    for child in root.children:
        collect_rects(child, 0, 0, rects)
    scale = min(1.0, max_side / max(cw, ch))
    sw, sh = cw * scale, ch * scale
    title_h = 36
    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw + 20:.0f}" height="{sh + title_h + 16:.0f}" viewBox="0 0 {sw + 20:.0f} {sh + title_h + 16:.0f}">',
        '  <rect x="0" y="0" width="100%" height="100%" fill="#f4f4f4"/>',
        f'  <text x="10" y="22" font-family="system-ui,sans-serif" font-size="13" font-weight="bold">{svg_escape(title)}</text>',
        f'  <text x="10" y="38" font-family="system-ui,sans-serif" font-size="10" fill="#444">{svg_escape(subtitle)}</text>',
        f'  <g transform="translate(10 {title_h})">',
        f'    <rect x="0" y="0" width="{sw}" height="{sh}" fill="#fff" stroke="#333" stroke-width="1"/>',
    ]
    colors = ["#cfe8fc", "#e8f5e9", "#fff3e0", "#f3e5f5", "#eceff1", "#d7ccc8"]
    for i, (_name, typ, x, y, w, h, label) in enumerate(rects):
        if w <= 0 or h <= 0:
            continue
        rx = x * scale
        ry = y * scale
        rw = max(1, w * scale)
        rh = max(1, h * scale)
        if rx + rw > sw + 1:
            rw = max(1, sw - rx)
        if ry + rh > sh + 1:
            rh = max(1, sh - ry)
        c = colors[i % len(colors)]
        lines.append(
            f'    <rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" '
            f'fill="{c}" stroke="#666" stroke-width="0.6" opacity="0.95"/>'
        )
        show = label.strip() or typ
        max_chars = max(12, int((rw - 6) / 5)) if rw > 30 else 10
        show = show[: max(10, min(max_chars, 72))]
        if rw > 40 and rh > 12:
            lines.append(
                f'    <text x="{rx + 3:.1f}" y="{ry + 11:.1f}" font-family="system-ui,sans-serif" '
                f'font-size="9" fill="#222">{svg_escape(show)}</text>'
            )
        if rw > 40 and rh > 26 and show != typ:
            lines.append(
                f'    <text x="{rx + 3:.1f}" y="{ry + 22:.1f}" font-family="system-ui,sans-serif" '
                f'font-size="7" fill="#666">{svg_escape(typ[:32])}</text>'
            )
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines)


def fallback_svg_from_csv_row(row: dict[str, str], title: str, subtitle: str) -> str:
    cw_s, ch_s = row.get("client_w", ""), row.get("client_h", "")
    try:
        cw = int(cw_s) if cw_s else 640
        ch = int(ch_s) if ch_s else 400
    except ValueError:
        cw, ch = 640, 400
    cw, ch = max(200, cw), max(150, ch)
    scale = min(1.0, 1000.0 / max(cw, ch))
    sw, sh = cw * scale, ch * scale
    title_h = 36
    try:
        g = int(row.get("TDBGrid", "0") or 0)
        p = int(row.get("TPanel", "0") or 0)
        e = int(row.get("TEdit", "0") or 0)
    except ValueError:
        g, p, e = 0, 0, 0
    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw + 20:.0f}" height="{sh + title_h + 16:.0f}">',
        '  <rect width="100%" height="100%" fill="#fafafa"/>',
        f'  <text x="10" y="22" font-family="system-ui,sans-serif" font-size="13" font-weight="bold">{svg_escape(title)}</text>',
        f'  <text x="10" y="38" font-family="system-ui,sans-serif" font-size="10" fill="#444">{svg_escape(subtitle)}</text>',
        f'  <text x="10" y="{title_h + 14}" font-family="system-ui,sans-serif" font-size="10" fill="#666">(DFM \uc5c6\uc74c/\uc774\uc9c4: \ucef4\ud3ec\ub10c\ud2b8 \uac1c\uc218 \uae30\ubc18 \uc640\uc774\uc5b4)</text>',
        f'  <g transform="translate(10 {title_h + 24})">',
        f'    <rect x="0" y="0" width="{sw}" height="{sh}" fill="#fff" stroke="#333"/>',
    ]
    y0 = 8.0
    h_band = max(24.0, (sh - 16) / max(3, 1 + min(g, 5)))
    lines.append(
        f'    <rect x="4" y="{y0}" width="{sw - 8}" height="{min(h_band, sh * 0.15):.1f}" fill="#e3f2fd" stroke="#666"/>'
    )
    lines.append(
        f'    <text x="8" y="{y0 + 14}" font-size="9">Panel-like x{p}</text>'
    )
    y0 += h_band + 4
    gh = min((sh - y0 - 8) / max(g, 1), sh * 0.5) if g else sh * 0.35
    for i in range(min(g, 6) if g else 1):
        yy = y0 + i * (gh + 4)
        lines.append(
            f'    <rect x="4" y="{yy:.1f}" width="{sw - 8}" height="{gh:.1f}" fill="#e8f5e9" stroke="#666"/>'
        )
        lines.append(
            f'    <text x="8" y="{yy + 14:.1f}" font-size="9">TDBGrid ({i + 1})</text>'
        )
    lines.append(f'    <text x="4" y="{sh - 8}" font-size="8" fill="#888">TEdit x{e}</text>')
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines)


def row_priority(row: dict[str, str]) -> bool:
    if row.get("kind") != "Form":
        return False
    mp = (row.get("menu_paths") or "").strip()
    if mp and mp != "\u2014" and mp != "-":
        return True
    try:
        if int(row.get("TDBGrid", "0") or 0) >= 2:
            return True
    except ValueError:
        pass
    su = (row.get("startup_createform") or "").lower()
    if su.startswith("yes"):
        return True
    inst = row.get("instance", "")
    if inst in ("Subu00", "Sobo10"):
        return True
    return False


def load_csv_rows() -> list[dict[str, str]]:
    if not CSV_PATH.is_file():
        raise SystemExit(f"Missing {CSV_PATH} ? run: python3 debug/generate_screen_specification.py")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--all",
        action="store_true",
        help="Generate for all forms with text DFM (or fallback)",
    )
    ap.add_argument("--max", type=int, default=0, help="Max number of SVG files (0=no limit)")
    args = ap.parse_args()
    use_priority = not args.all

    rows = load_csv_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for row in rows:
        if use_priority and not row_priority(row):
            continue
        if row.get("kind") not in ("Form", "Frame"):
            continue
        inst = row.get("instance", "unknown")
        rel = row.get("dpr_in_path", "").replace("\\", "/")
        if not rel:
            continue
        pas = ROOT / rel
        dfm = pas.with_suffix(".dfm")
        caption = strip_caption(row.get("caption_dfm", "") or inst)
        subtitle = f"{row.get('unit', '')} | {inst} | {row.get('form_class', '')}"

        svg: str | None = None
        if dfm.is_file() and is_probably_text_dfm(dfm):
            text = read_text_maybe_cp949(dfm)
            tree = parse_dfm_tree(text)
            if tree:
                svg = build_svg_from_dfm(tree, caption or inst, subtitle)

        if svg is None:
            svg = fallback_svg_from_csv_row(row, caption or inst, subtitle)

        out = OUT_DIR / f"{inst}.svg"
        out.write_text(svg, encoding="utf-8")
        n += 1
        if args.max and n >= args.max:
            break

    print(f"Wrote {n} SVG(s) under {OUT_DIR}")


if __name__ == "__main__":
    main()
