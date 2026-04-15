#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse Chul.dfm (menus) + Chul.pas (Menu*Click) -> 11-screen-business-flows.md + 11-screen-business-flows-graphs.md (Mermaid)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "phase1-structure" / "11-screen-business-flows.md"
OUT_GRAPHS = ROOT / "docs" / "phase1-structure" / "11-screen-business-flows-graphs.md"

# Korean UI strings (avoid non-ASCII in .py source bytes)
L_MAIN = "\uba54\uc778 \uba54\ub274"  # Main menu
L_POPUP = "\uadf8\ub9ac\ub4dc \ud31d\uc5c5"  # Grid popup
L_TITLE = "\ud654\uba74\u00b7\ube44\uc988\ub2c8\uc2a4 \ud50c\ub85c\uc6b0 \uc815\ub9ac (\ub8e8\ud2b8 \uc815\ubcf8)"
L_NO_HANDLER = "(\ud578\ub4e4\ub7ec \ubcf8\ubb38 \uc5c6\uc74c \ub610\ub294 \ube44\uba54\ub274)"
L_DASH = "\u2014"
L_GRAPH_TITLE = (
    "\ube44\uc988\ub2c8\uc2a4 \ud50c\ub85c\uc6b0 \ub2e4\uc774\uc5b4\uadf8\ub7a8 (Mermaid)"
)
L_GRAPH_INTRO = (
    "\uba54\uc778/\ud31d\uc5c5 \uba54\ub274\uc5d0\uc11c `Menu*Click`\uc73c\ub85c \uc5f4\ub9ac\ub294 "
    "\ud654\uba74\uc744 **Subu00(MDI)**\uc5d0\uc11c \uc5f0\uacb0\ud55c \uadf8\ub798\ud504\uc785\ub2c8\ub2e4. "
    "\ud234\ubc14\ub098 `nForm` \ub2e8\ucd94 \uacbd\ub85c\ub294 \ud3ec\ud568\ub418\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4."
)


def _mermaid_escape_label(s: str) -> str:
    s = s.replace('"', "'").replace("\n", " ").replace("]", " ")
    if len(s) > 118:
        s = s[:115] + "..."
    return s


def write_flow_graphs(by_flow: dict[str, list[tuple]], dash: str) -> None:
    lines: list[str] = []
    lines.append(f"# {L_GRAPH_TITLE}\n\n")
    lines.append(f"{L_GRAPH_INTRO}\n\n")
    lines.append(
        "\uad00\ub828: [11-screen-business-flows.md](11-screen-business-flows.md) "
        "(\ud45c \ubc84\uc804).\n\n"
    )

    flows = sorted(by_flow.keys())
    for fi, flow in enumerate(flows):
        rows = sorted(by_flow[flow], key=lambda x: x[0])
        lines.append(f"## {flow}\n\n")
        lines.append("```mermaid\n")
        lines.append("flowchart TB\n")
        lines.append('  root00["Subu00 MDI"]\n')
        sg = f"sg_{fi}"
        lines.append(f'  subgraph {sg} ["{_mermaid_escape_label(flow)}"]\n')
        for ri, r in enumerate(rows):
            path, hname, fc, un, _rel, fk, _note = r
            tail = path.split(" / ")[-1] if " / " in path else path
            unit_guess = ""
            if un:
                unit_guess = un.strip("`").replace(".pas", "")
            parts: list[str] = []
            if unit_guess:
                parts.append(unit_guess)
            parts.append(tail)
            if fc:
                parts.append(fc.strip("`"))
            else:
                parts.append(f"`{hname}`")
            lbl = " - ".join(p for p in parts if p)
            if fk and fk != dash:
                fkeys = re.findall(r"F\d+", fk)
                if fkeys:
                    lbl += " (" + ",".join(dict.fromkeys(fkeys)) + ")"
            nid = f"n_{fi}_{ri}"
            lines.append(f'    {nid}[\"{_mermaid_escape_label(lbl)}\"]\n')
        lines.append("  end\n")
        for ri, r in enumerate(rows):
            _path, _h, _fc, _un, _rel, fk, _note = r
            nid = f"n_{fi}_{ri}"
            fkeys = re.findall(r"F\d+", fk) if fk and fk != dash else []
            if fkeys:
                el = ",".join(dict.fromkeys(fkeys))
                el = _mermaid_escape_label(el)
                lines.append(f"  root00 -->|{el}| {nid}\n")
            else:
                lines.append(f"  root00 --> {nid}\n")
        lines.append("```\n\n")

    OUT_GRAPHS.parent.mkdir(parents=True, exist_ok=True)
    OUT_GRAPHS.write_text("".join(lines), encoding="utf-8")


def read_text_maybe_cp949(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def form_name_from_dpr_brace(inner: str) -> str:
    inner = inner.strip()
    if ":" in inner:
        return inner.split(":", 1)[0].strip()
    return inner


def parse_dpr_forms(dpr: Path) -> dict[str, tuple[str, str]]:
    text = read_text_maybe_cp949(dpr)
    out: dict[str, tuple[str, str]] = {}
    for m in re.finditer(
        r"^\s*(\w+)\s+in\s+'([^']+)'\s+\{([^}]+)\}\s*,?\s*$", text, re.MULTILINE
    ):
        unit, rel, brace = m.group(1), m.group(2), m.group(3)
        fname = form_name_from_dpr_brace(brace)
        out[fname] = (unit, rel.replace("\\", "/"))
    return out


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


@dataclass
class _MenuNode:
    caption: str | None = None
    onclick: str | None = None


def parse_menu_items(block_lines: list[str], root_label: str) -> dict[str, str]:
    onclick_paths: dict[str, str] = {}
    stack: list[_MenuNode] = []

    for line in block_lines:
        s = line.strip()
        if s.startswith("object ") and "TMenuItem" in s:
            stack.append(_MenuNode())
        elif s.startswith("end") and stack:
            n = stack.pop()
            if n.onclick:
                parts: list[str] = [root_label]
                for p in stack:
                    c = p.caption
                    if c and c != "-":
                        parts.append(c)
                if n.caption and n.caption != "-":
                    parts.append(n.caption)
                onclick_paths[n.onclick] = " / ".join(parts)
        elif "Caption =" in s and stack:
            m = re.search(r"Caption\s*=\s*'((?:''|[^'])*)'", s)
            if m:
                stack[-1].caption = m.group(1).replace("''", "'")
        elif "OnClick =" in s and stack:
            m = re.search(r"OnClick\s*=\s*(\w+)", s)
            if m:
                stack[-1].onclick = m.group(1)
    return onclick_paths


def find_menu_block(text: str, marker: str) -> list[str] | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if marker in line:
            block, _ = extract_object_block(lines, i)
            return block
    return None


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


def analyze_body(body: str) -> dict[str, object]:
    f_keys = re.findall(r"Seek_Uses\s*\(\s*'([^']+)'\s*\)", body)
    creates = re.findall(r"\b(\w+)\s*:=\s*(T\w+)\.Create\s*\(\s*self\s*\)", body, re.I)
    creates_app = re.findall(
        r"\b(\w+)\s*:=\s*(T\w+)\.Create\s*\(\s*Application\s*\)", body, re.I
    )
    mdi_types = sorted(set(re.findall(r"MDIChildren\[I\]\s+is\s+(T\w+)", body)))
    flags: list[str] = []
    if re.search(r"Sobo40\.ShowModal", body):
        flags.append("password modal Subu40")
    if re.search(r"Seok80\.ShowModal", body):
        flags.append("info modal Seok80")
    if re.search(r"Sobo10\.ShowModal", body):
        flags.append("login/register modal Subu10")
    sub_hints = re.findall(r"nUse1\s*\+\s*'([^']+)'", body)
    grid_ops: list[str] = []
    if re.search(r"\bnSqry\.Append\b", body):
        grid_ops.append("nSqry.Append")
    if re.search(r"\bnSqry\.Post\b", body):
        grid_ops.append("nSqry.Post")
    if re.search(r"\bmSqry\.Append\b", body):
        grid_ops.append("mSqry.Append")
    if re.search(r"\bmSqry\.Post\b", body):
        grid_ops.append("mSqry.Post")
    if re.search(r"Keybd_event\s*\(\s*VK_DELETE", body):
        grid_ops.append("Delete key (grid row)")
    return {
        "f_keys": f_keys,
        "creates": creates + creates_app,
        "mdi_types": mdi_types,
        "flags": flags,
        "sub_hints": sub_hints,
        "grid_ops": grid_ops,
    }


def primary_form(
    analysis: dict[str, object], form_map: dict[str, tuple[str, str]]
) -> tuple[str | None, str | None, str | None]:
    creates = analysis["creates"]
    mdi_types: list[str] = analysis["mdi_types"]  # type: ignore
    prefixes = ("TSobo", "TSeok", "TSeak", "TSeek", "TTong")
    for _lhs, rhs in creates:
        if not rhs.startswith("T") or len(rhs) < 2:
            continue
        if any(rhs.startswith(p) for p in prefixes):
            key = rhs[1:]
            if key in form_map:
                u, p = form_map[key]
                return rhs, u, p
    for t in mdi_types:
        if t.startswith("T") and len(t) > 1 and t[1:] in form_map:
            key = t[1:]
            u, p = form_map[key]
            return t, u, p
    return None, None, None


def main() -> None:
    dfm_path = ROOT / "Chul.dfm"
    pas_path = ROOT / "Chul.pas"
    dpr_path = ROOT / "Chulpan.dpr"
    dfm = read_text_maybe_cp949(dfm_path)
    pas = read_text_maybe_cp949(pas_path)
    form_map = parse_dpr_forms(dpr_path)

    onclick_paths: dict[str, str] = {}
    mm = find_menu_block(dfm, "object MainMenu1: TMainMenu")
    if mm:
        onclick_paths.update(parse_menu_items(mm, L_MAIN))
    pm = find_menu_block(dfm, "object PopupMenu1: TPopupMenu")
    if pm:
        onclick_paths.update(parse_menu_items(pm, L_POPUP))

    handlers = parse_menu_handlers(pas)

    intro_scope = (
        "**\ubc94\uc704**: \uc6cc\ud06c\uc2a4\ud398\uc774\uc2a4 \ub8e8\ud2b8 [`Chul.pas`](../Chul.pas) "
        "MDI `Subu00`\uc758 **\uba54\uc778 \uba54\ub274\u00b7\ud31d\uc5c5 \uba54\ub274**"
        "\uc5d0 \uc5f0\uacb0\ub41c `Menu*Click` \ud578\ub4e4\ub7ec\ub97c \uae30\uc900\uc73c\ub85c "
        "\uc790\ub3d9 \ucd94\ucd9c\ud588\uc2b5\ub2c8\ub2e4.\n\n"
    )
    intro_limit = (
        "**\ud55c\uacc4**: \ud234\ubc14(`ToolButton*Click`), `nForm` \ubb38\uc790\uc5f4\ub85c "
        "\uc5ec\ub294 `Sobo*` \ub2e8\ucd94(\ubc30\uacbd \uc774\ubbf8\uc9c0 \ub4f1)\ub294 "
        "\uc774 \ud45c\uc5d0 **\ud3ec\ud568\ub418\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4**.\n\n"
    )
    intro_perm = (
        "**\uad8c\ud55c**: `Base10.Seek_Uses('Fxx')` \uacb0\uacfc\uac00 `X`\uc774\uba74 "
        "`E_Connect`\ub85c \ub9c9\ud799\ub2c8\ub2e4. \uc2e4\uc81c \ud45c\uc2dc \uc5ec\ubd80\ub294 "
        "DB \uad8c\ud55c \ud14c\uc774\ube14\uc5d0 \ub530\ub985\ub2c8\ub2e4.\n\n"
    )
    rel_docs = (
        "\uad00\ub828: [06-forms-runtime-graph.md](06-forms-runtime-graph.md), "
        "[08-base01-inventory.md](08-base01-inventory.md), "
        "[09-settings-external.md](09-settings-external.md).\n\n"
    )
    flow_h = "## \ube44\uc988\ub2c8\uc2a4 \ud50c\ub85c\uc6b0(\ub300\uba54\ub274) \uac1c\uc694\n\n"
    sub_popup_h = "## \ubcf4\uc870: \ud31d\uc5c5 \uba54\ub274(\uadf8\ub9ac\ub4dc)\n\n"

    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for hname, path in sorted(onclick_paths.items(), key=lambda x: x[1]):
        body = handlers.get(hname, "")
        if not body.strip():
            rows.append((path, hname, "", "", "", "", L_NO_HANDLER))
            continue
        an = analyze_body(body)
        f_keys = ", ".join(dict.fromkeys(an["f_keys"]))  # type: ignore
        tform, unit, rel = primary_form(an, form_map)
        form_s = f"`{tform}`" if tform else ""
        unit_s = f"`{unit}.pas`" if unit else ""
        rel_s = f"`{rel}`" if rel else ""
        notes: list[str] = []
        if an["flags"]:  # type: ignore
            notes.extend(an["flags"])  # type: ignore
        if an["creates"] and not tform:  # type: ignore
            notes.append(f"Create: {an['creates'][:2]}")  # type: ignore
        gops = an.get("grid_ops", [])
        if gops and not tform:  # type: ignore
            notes.append("popup grid: " + ", ".join(gops))  # type: ignore
        rows.append(
            (
                path,
                hname,
                form_s,
                unit_s,
                rel_s,
                f_keys or L_DASH,
                "; ".join(notes) if notes else L_DASH,
            )
        )

    by_flow: dict[str, list[tuple]] = {}
    for r in rows:
        parts = r[0].split(" / ")
        # parts[0] is root label (main vs popup); parts[1] is top-level menu caption
        flow = parts[1] if len(parts) > 2 else (parts[1] if len(parts) == 2 else parts[0])
        by_flow.setdefault(flow, []).append(r)

    write_flow_graphs(by_flow, L_DASH)

    lines: list[str] = []
    lines.append(f"# {L_TITLE}\n\n")
    lines.append(intro_scope)
    lines.append(intro_limit)
    lines.append(intro_perm)
    lines.append(rel_docs)
    lines.append(flow_h)
    lines.append(
        "\uc544\ub798\ub294 **\ub300\uba54\ub274 \uc139\uc158**\ubcc4\ub85c "
        "\ud558\uc704 \uba54\ub274 \uacbd\ub85c\uc640 \uc5f4\ub9ac\ub294 "
        "\ud3fc/\uad8c\ud55c \ud0a4\ub97c \uc815\ub9ac\ud55c \ud45c\uc785\ub2c8\ub2e4.\n\n"
    )

    for flow in sorted(by_flow.keys()):
        lines.append(f"## \ud50c\ub85c\uc6b0: {flow}\n\n")
        lines.append(
            "| \uba54\ub274 \uacbd\ub85c | \ud578\ub4e4\ub7ec | \uc8fc \ud3fc \ud074\ub798\uc2a4 | "
            "\uc720\ub2db | DPR `in` \uacbd\ub85c | `Seek_Uses` | \ube44\uace0 |\n"
        )
        lines.append(
            "|-----------|--------|-------------|------|---------------|-------------|------|\n"
        )
        for r in sorted(by_flow[flow], key=lambda x: x[0]):
            path, hname, fc, un, rel, fk, note = r
            lines.append(
                f"| {path} | `{hname}` | {fc} | {un} | {rel} | {fk} | {note} |\n"
            )
        lines.append("\n")

    lines.append(sub_popup_h)
    lines.append("| \uba54\ub274 \uacbd\ub85c | \ud578\ub4e4\ub7ec | \ube44\uace0 |\n")
    lines.append("|-----------|--------|------|\n")
    for r in sorted(rows, key=lambda x: x[0]):
        if not r[0].startswith(L_POPUP):
            continue
        lines.append(f"| {r[0]} | `{r[1]}` | {r[6]} |\n")
    lines.append("\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_GRAPHS}")


if __name__ == "__main__":
    main()
