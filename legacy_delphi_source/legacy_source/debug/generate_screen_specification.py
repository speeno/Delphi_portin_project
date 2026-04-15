#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate detailed screen specification from root Chulpan.dpr + DFM + Chul menu/showmodal scan.
Outputs: docs/phase1-structure/12-screen-specification.md, 12-screen-specification.csv
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "docs" / "phase1-structure" / "12-screen-specification.md"
OUT_CSV = ROOT / "docs" / "phase1-structure" / "12-screen-specification.csv"
DPR = ROOT / "Chulpan.dpr"
CHUL_PAS = ROOT / "Chul.pas"
CHUL_DFM = ROOT / "Chul.dfm"

L_MAIN = "\uba54\uc778 \uba54\ub274"
L_POPUP = "\uadf8\ub9ac\ub4dc \ud31d\uc5c5"


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


def form_name_from_dpr_brace(inner: str) -> str:
    inner = inner.strip()
    if ":" in inner:
        return inner.split(":", 1)[0].strip()
    return inner


def parse_dpr_entries(dpr: Path) -> list[tuple[str, str, str, str]]:
    """(unit, rel_path, form_instance, kind) kind = DataModule|Frame|Form"""
    text = read_text_maybe_cp949(dpr)
    entries: list[tuple[str, str, str, str]] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("//"):
            continue
        m = re.match(
            r"^(\w+)\s+in\s+'([^']+)'\s+\{([^}]+)\}\s*,?\s*$", s
        )
        if not m:
            continue
        unit, rel, brace = m.group(1), m.group(2), m.group(3)
        rel = rel.replace("\\", "/")
        inst = form_name_from_dpr_brace(brace)
        b = brace.strip()
        if "TDataModule" in b:
            kind = "DataModule"
        elif "TFrame" in b:
            kind = "Frame"
        else:
            kind = "Form"
        entries.append((unit, rel, inst, kind))
    return entries


def resolve_pas(rel: str) -> Path:
    p = Path(rel)
    if not p.is_absolute():
        p = ROOT / p
    return p.resolve()


def parse_dfm_root(dfm_path: Path) -> dict[str, str]:
    if not dfm_path.is_file() or not is_probably_text_dfm(dfm_path):
        return {}
    text = read_text_maybe_cp949(dfm_path)
    lines = text.splitlines()
    root_m = None
    start = 0
    for i, line in enumerate(lines):
        m = re.match(r"^object\s+(\w+)\s*:\s*(T\w+)\s*$", line.strip())
        if m:
            root_m = (m.group(1), m.group(2))
            start = i + 1
            break
    if not root_m:
        return {}
    props: dict[str, str] = {"dfm_object": root_m[0], "dfm_class": root_m[1]}
    prop_re = re.compile(r"^\s{2}([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")
    for j in range(start, len(lines)):
        line = lines[j]
        if re.match(r"^\s{2}object\s+\w+", line):
            break
        pm = prop_re.match(line)
        if pm:
            k, v = pm.group(1), pm.group(2).strip()
            if k in (
                "Caption",
                "FormStyle",
                "BorderStyle",
                "BorderIcons",
                "Position",
                "WindowState",
                "ClientWidth",
                "ClientHeight",
                "Width",
                "Height",
                "Color",
                "Font",
                "Visible",
                "Scaled",
                "PixelsPerInch",
                "TextHeight",
            ):
                props[k] = v
    return props


def count_components(text: str) -> dict[str, int]:
    t = text
    return {
        "TDBGrid": len(re.findall(r":\s*TDBGrid\b", t)),
        "TClientDataSet": len(re.findall(r":\s*TClientDataSet\b", t)),
        "TEdit": len(re.findall(r":\s*TEdit\b", t)),
        "TButton": len(re.findall(r":\s*TButton\b", t)),
        "TPanel": len(re.findall(r":\s*TPanel\b", t)),
        "TComboBox": len(re.findall(r":\s*TComboBox\b", t)),
        "TDateTimePicker": len(re.findall(r":\s*TDateTimePicker\b", t)),
        "TWebBrowser": len(re.findall(r":\s*TWebBrowser\b", t)),
        "TImage": len(re.findall(r":\s*TImage\b", t)),
    }


def extract_object_block(lines: list[str], start: int) -> tuple[list[str], int]:
    depth = 0
    for i in range(start, len(lines)):
        s = lines[i].strip()
        if s.startswith("object "):
            depth += 1
        elif s.startswith("end"):
            depth -= 1
            if depth == 0:
                return lines[start : i + 1], i + 1
    return lines[start:], len(lines)


def find_menu_block(text: str, marker: str) -> list[str] | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if marker in line:
            block, _ = extract_object_block(lines, i)
            return block
    return None


@dataclass
class _MN:
    caption: str | None = None
    onclick: str | None = None


def parse_menu_onclick_paths(dfm_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    stack: list[_MN] = []
    for block_marker, root_lbl in (
        ("object MainMenu1: TMainMenu", L_MAIN),
        ("object PopupMenu1: TPopupMenu", L_POPUP),
    ):
        blk = find_menu_block(dfm_text, block_marker)
        if not blk:
            continue
        for line in blk:
            s = line.strip()
            if s.startswith("object ") and "TMenuItem" in s:
                stack.append(_MN())
            elif s.startswith("end") and stack:
                n = stack.pop()
                if n.onclick:
                    parts = [root_lbl]
                    for p in stack:
                        if p.caption and p.caption != "-":
                            parts.append(p.caption)
                    if n.caption and n.caption != "-":
                        parts.append(n.caption)
                    out[n.onclick] = " / ".join(parts)
            elif "Caption =" in s and stack:
                m = re.search(r"Caption\s*=\s*'((?:''|[^'])*)'", s)
                if m:
                    stack[-1].caption = m.group(1).replace("''", "'")
            elif "OnClick =" in s and stack:
                m = re.search(r"OnClick\s*=\s*(\w+)", s)
                if m:
                    stack[-1].onclick = m.group(1)
    return out


def parse_menu_handlers(pas_text: str) -> dict[str, str]:
    handlers: dict[str, str] = {}
    pat = re.compile(
        r"^procedure\s+TSubu00\.(Menu\w+Click)\s*\(\s*Sender:\s*TObject\s*\)\s*;",
        re.MULTILINE,
    )
    matches = list(pat.finditer(pas_text))
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(pas_text)
        handlers[name] = pas_text[start:end]
    return handlers


def handler_primary_tform(body: str) -> str | None:
    creates = re.findall(r"\b\w+\s*:=\s*(T\w+)\.Create\s*\(\s*self\s*\)", body, re.I)
    prefixes = ("TSobo", "TSeok", "TSeak", "TSeek", "TTong")
    for rhs in creates:
        if any(rhs.startswith(p) for p in prefixes):
            return rhs
    mdi = re.findall(r"MDIChildren\[I\]\s+is\s+(T\w+)", body)
    for t in mdi:
        if any(t.startswith(p) for p in prefixes):
            return t
    return None


def build_menu_paths_for_tform(
    onclick_paths: dict[str, str], handlers: dict[str, str]
) -> dict[str, list[str]]:
    """TFormClass e.g. TSobo21 -> list of menu paths"""
    rev: dict[str, list[str]] = defaultdict(list)
    for hname, path in onclick_paths.items():
        body = handlers.get(hname, "")
        if not body.strip():
            continue
        tf = handler_primary_tform(body)
        if tf:
            rev[tf].append(path)
    return dict(rev)


def scan_showmodal_in_file(text: str) -> list[tuple[str, str]]:
    """(identifier, line snippet)"""
    out: list[tuple[str, str]] = []
    for m in re.finditer(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\.ShowModal\b", text
    ):
        ident = m.group(1)
        if ident in ("Application", "Self"):
            continue
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        snippet = text[line_start : line_end if line_end != -1 else len(text)].strip()[:120]
        out.append((ident, snippet))
    return out


def datamodule_class_from_pas(pas_path: Path) -> str | None:
    if not pas_path.is_file():
        return None
    t = read_text_maybe_cp949(pas_path)
    m = re.search(
        r"^\s*(T\w+)\s*=\s*class\s*\(\s*TDataModule\s*\)", t, re.MULTILINE
    )
    return m.group(1) if m else None


def parse_dpr_startup_createforms(dpr_text: str) -> list[tuple[str, str]]:
    """Application.CreateForm(TClass, Var) after begin block."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(
        r"Application\.CreateForm\s*\(\s*(T\w+)\s*,\s*(\w+)\s*\)", dpr_text
    ):
        out.append((m.group(1), m.group(2)))
    return out


def strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    return s


def classify_ui_role(
    kind: str, form_style: str | None, border: str | None
) -> str:
    if kind == "DataModule":
        return "non-visual DataModule"
    if kind == "Frame":
        return "embeddable Frame"
    fs = (form_style or "").lower()
    bs = (border or "").lower()
    if "fsmdichild" in fs or "mdichild" in fs:
        return "MDI child"
    if "fsmdiform" in fs or "mdiform" in fs:
        return "MDI parent"
    if "bsdialog" in bs or "dialog" in bs:
        return "dialog-style border"
    if kind == "Form":
        return "typical Form (check ShowModal vs Show in code)"
    return "unknown"


def main() -> None:
    entries = parse_dpr_entries(DPR)
    dpr_full = read_text_maybe_cp949(DPR)
    startup_forms = parse_dpr_startup_createforms(dpr_full)
    startup_vars = {var for _tcls, var in startup_forms}

    form_map: dict[str, tuple[str, str, str]] = {}
    for unit, rel, inst, kind in entries:
        form_map[inst] = (unit, rel, kind)

    dfm_text = read_text_maybe_cp949(CHUL_DFM)
    pas_text = read_text_maybe_cp949(CHUL_PAS)
    onclick_paths = parse_menu_onclick_paths(dfm_text)
    handlers = parse_menu_handlers(pas_text)
    tform_menus = build_menu_paths_for_tform(onclick_paths, handlers)

    # ShowModal: each unit's .pas from DPR (includes Chul.pas)
    showmodal_by_ident: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for unit, rel, inst, _kind in entries:
        p = resolve_pas(rel)
        if not p.is_file():
            continue
        t = read_text_maybe_cp949(p)
        rel_s = str(p.relative_to(ROOT))
        for ident, snip in scan_showmodal_in_file(t):
            showmodal_by_ident[ident].append((rel_s, snip))

    rows: list[dict[str, str]] = []
    for unit, rel, inst, kind in entries:
        pas_path = resolve_pas(rel)
        dfm_path = pas_path.with_suffix(".dfm")
        root = parse_dfm_root(dfm_path)
        dfm_exists = dfm_path.is_file() and is_probably_text_dfm(dfm_path)
        full_dfm = read_text_maybe_cp949(dfm_path) if dfm_exists else ""
        counts = count_components(full_dfm) if full_dfm else {}

        t_cls = f"T{inst}" if not inst.startswith("T") else inst
        if kind == "Form":
            t_cls = root.get("dfm_class", t_cls)
        elif kind == "DataModule":
            dm = datamodule_class_from_pas(pas_path)
            if dm:
                t_cls = dm

        menus = tform_menus.get(t_cls, [])
        menu_cell = "; ".join(sorted(set(menus))[:8])
        if len(set(menus)) > 8:
            menu_cell += f" (+{len(set(menus)) - 8})"

        modal_refs = showmodal_by_ident.get(inst, [])
        modal_cell = ""
        if modal_refs:
            modal_cell = "; ".join({f"{a}: {b[:60]}" for a, b in modal_refs[:5]})
            if len(modal_refs) > 5:
                modal_cell += f" (+{len(modal_refs) - 5})"

        caption = strip_quotes(root.get("Caption", "").strip())
        fs = root.get("FormStyle", "")
        bs = root.get("BorderStyle", "")
        role = classify_ui_role(kind, fs or None, bs or None)
        startup = "yes" if inst in startup_vars else "no"
        if inst == "Sobo10":
            startup = "yes (pre-CreateForm login)"

        row = {
            "instance": inst,
            "form_class": t_cls,
            "unit": unit,
            "dpr_in_path": rel,
            "kind": kind,
            "ui_role": role,
            "caption_dfm": caption,
            "form_style": fs,
            "border_style": bs,
            "position": root.get("Position", ""),
            "client_w": root.get("ClientWidth", ""),
            "client_h": root.get("ClientHeight", ""),
            "dfm_found": "yes" if dfm_exists else "no",
            "startup_createform": startup,
            "menu_paths": menu_cell,
            "showmodal_refs": modal_cell,
            "TDBGrid": str(counts.get("TDBGrid", 0)),
            "TClientDataSet": str(counts.get("TClientDataSet", 0)),
            "TEdit": str(counts.get("TEdit", 0)),
            "TPanel": str(counts.get("TPanel", 0)),
            "TButton": str(counts.get("TButton", 0)),
            "TWebBrowser": str(counts.get("TWebBrowser", 0)),
        }
        rows.append(row)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    # CSV
    fieldnames = list(rows[0].keys()) if rows else []
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Markdown
    md: list[str] = []
    md.append("# \ud654\uba74 \uc815\uc758\uc11c (\ub8e8\ud2b8 Chulpan.dpr \uae30\uc900)\n\n")
    md.append(
        "\uc0dd\uc131: [`debug/generate_screen_specification.py`](../../debug/generate_screen_specification.py) "
        "\uc7ac\uc2e4\ud589.\n\n"
    )
    md.append("## \ubc94\uc704\n\n")
    md.append(
        "- **\uae30\uc900 DPR**: [`Chulpan.dpr`](../Chulpan.dpr) `uses` \uc5d0 \uba85\uc2dc\ub41c \uc720\ub2db\ub9cc.\n"
        "- **DFM**: \uac01 `.pas` \uc640 \ub3d9\uc77c \uacbd\ub85c\uc758 `.dfm` (\ud14d\uc2a4\ud2b8 DFM\ub9cc; \uc774\uc9c4\ud615 DFM\uc740 \uc2a4\ud0b5).\n"
        "- **\uba54\ub274 \uacbd\ub85c**: `Chul.dfm` \uba54\ub274 + `Chul.pas` `Menu*Click`\uc5d0\uc11c **\uc5f4\ub9ac\ub294 \uc8fc \ud3fc \ud074\ub798\uc2a4**\uc640 \ub9e4\uce6d (\ud234\ubc14/\ub2e4\ub978 \uacbd\ub85c\ub294 \ubbf8\ud3ec\ud568).\n"
        "- **ShowModal**: DPR `uses`\uc5d0 \ud3ec\ud568\ub41c \uac01 `.pas`\uc5d0\uc11c `*.ShowModal` \uac80\uc0c9 (\ub3d9\uc77c \uc2dd\ubcc4\uc790\uac00 \uc5ec\ub7ec \ud30c\uc77c\uc5d0\uc11c \uc4f0\uc774\uba74 \ubaa8\ub450 \ub098\uc5f4).\n\n"
    )
    md.append("## \uc694\uc57d\n\n")
    n_form = sum(1 for r in rows if r["kind"] == "Form")
    n_dm = sum(1 for r in rows if r["kind"] == "DataModule")
    n_fr = sum(1 for r in rows if r["kind"] == "Frame")
    n_dfm = sum(1 for r in rows if r["dfm_found"] == "yes")
    md.append(
        f"| \ud56d\ubaa9 | \uac1c\uc218 |\n|------|------:|\n"
        f"| Form (\ucd94\uc815) | {n_form} |\n"
        f"| DataModule | {n_dm} |\n"
        f"| Frame | {n_fr} |\n"
        f"| \ud14d\uc2a4\ud2b8 DFM \ubc1c\uacac | {n_dfm} |\n"
        f"| \ucd1d DPR \uc5d4\ud2b8\ub9ac | {len(rows)} |\n\n"
    )

    md.append("## \ubd80\ud305 \uc2dc `Application.CreateForm` (\ub85c\uadf8\uc778 \uc774\ud6c4)\n\n")
    md.append("| \uc21c\uc11c | \ud074\ub798\uc2a4 | \ubcc0\uc218(\uc778\uc2a4\ud134\uc2a4) |\n")
    md.append("|------|----------|-------------|\n")
    for i, (tcls, var) in enumerate(startup_forms, 1):
        md.append(f"| {i} | `{tcls}` | `{var}` |\n")
    md.append(
        "\n\ub85c\uadf8\uc778: `Sobo10 := TSobo10.Create(Application);` \ud6c4 `ShowModal` \uc131\uacf5 \uc2dc\uc5d0\ub9cc "
        "\uc704 `CreateForm`\uc774 \uc2e4\ud589\ub429\ub2c8\ub2e4.\n\n"
    )

    md.append("## \uc804\uccb4 \ud45c (\uba54\ub274 / \ubaa8\ub2ec / \ubd80\ud305 / \ucef4\ud3ec\ub10c\ud2b8 \uac1c\uc218)\n\n")
    md.append(
        "| \uc778\uc2a4\ud134\uc2a4 | \ud3fc \ud074\ub798\uc2a4 | \uc720\ub2db | DPR `in` | \uc885\ub958 | "
        "\ubd80\ud305 CreateForm | UI \uc5ed\ud560 | DFM Caption | FormStyle | "
        "BorderStyle | ClientWxH | \uba54\ub274 \uacbd\ub85c(\uc77c\ubd80) | ShowModal \uc5f0\uc18d | "
        "Grid | CDS | Panel | Edit |\n"
    )
    md.append(
        "|-----------|----------|------|----------|------|----------------|----------|-------------|-----------|"
        "------------|---------|----------------|---------------|-----|-----|-------|------|\n"
    )
    for r in sorted(rows, key=lambda x: (x["kind"], x["unit"])):
        cw, ch = r["client_w"], r["client_h"]
        wh = f"{cw}x{ch}" if cw or ch else "\u2014"
        cap = (r["caption_dfm"] or "\u2014").replace("|", "\\|")[:80]
        menu = (r["menu_paths"] or "\u2014").replace("|", "\\|")[:100]
        sm = (r["showmodal_refs"] or "\u2014").replace("|", "\\|")[:120]
        su = r.get("startup_createform", "\u2014")
        md.append(
            f"| `{r['instance']}` | `{r['form_class']}` | `{r['unit']}` | `{r['dpr_in_path']}` | {r['kind']} | "
            f"{su} | {r['ui_role']} | {cap} | {r['form_style'] or '\u2014'} | {r['border_style'] or '\u2014'} | {wh} | "
            f"{menu} | {sm} | {r['TDBGrid']} | {r['TClientDataSet']} | {r['TPanel']} | {r['TEdit']} |\n"
        )

    md.append("\n## CSV\n\n")
    md.append(
        f"\ub3d9\uc77c \ub0b4\uc6a9\uc744 \uc2a4\ud504\ub808\ub4dc\uc2dc\ud2b8\uc6a9\uc73c\ub85c: "
        f"[12-screen-specification.csv](12-screen-specification.csv) (UTF-8 BOM).\n\n"
    )
    md.append("## \uad00\ub828 \ubb38\uc11c\n\n")
    md.append(
        "- [11-screen-business-flows.md](11-screen-business-flows.md) \uba54\ub274 \ud50c\ub85c\uc6b0 \uc0c1\uc138\n"
        "- [06-forms-runtime-graph.md](06-forms-runtime-graph.md)\n"
    )

    OUT_MD.write_text("".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}\nWrote {OUT_CSV}")


if __name__ == "__main__":
    main()
