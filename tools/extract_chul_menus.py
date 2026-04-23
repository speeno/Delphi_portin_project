#!/usr/bin/env python3
"""Extract MainMenu trees + handler -> form mapping for all WeLove Chul builds.

Reads `analysis/welove_chul_builds.json` (build catalog) and emits 3 JSONs:

  1. analysis/welove_chul_menu_trees.json
       Per-build MainMenu1 tree (object_id, caption, onclick, children, separator).

  2. analysis/welove_chul_menu_matrix.json
       Union of all menu captions × per-build presence (true/false), with
       canonical `MENU-*` tracking IDs.

  3. analysis/welove_chul_menu_handlers.json
       Per-build handler -> referenced forms map (T<form>.Create / .Show patterns
       found inside Menu*Click bodies in Chul.pas).

The parser is intentionally lenient: it extracts top-down by tracking
nested `object ... TMenuItem` blocks and pulls Caption / OnClick lines.
CP949 decoding is enforced for all reads (G3-safe — no secrets touched).
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "analysis/welove_chul_builds.json"
OUT_TREES = ROOT / "analysis/welove_chul_menu_trees.json"
OUT_MATRIX = ROOT / "analysis/welove_chul_menu_matrix.json"
OUT_HANDLERS = ROOT / "analysis/welove_chul_menu_handlers.json"


def read_cp949(path: Path) -> str:
    return path.read_bytes().decode("cp949", errors="replace")


# ---------------------------------------------------------------------------
# DFM main-menu parser

_OBJECT_RE = re.compile(r"^(\s*)object\s+(\w+):\s*(\w+)\s*$")
_END_RE = re.compile(r"^(\s*)end\s*$")
_CAPTION_RE = re.compile(r"^\s*Caption\s*=\s*'((?:''|[^'])*)'")
_ONCLICK_RE = re.compile(r"^\s*OnClick\s*=\s*(\w+)")


def find_main_menu_block(dfm_text: str) -> list[str] | None:
    """Locate the `object MainMenu1: TMainMenu` block and return its lines."""
    lines = dfm_text.splitlines()
    start = None
    indent = None
    for i, line in enumerate(lines):
        m = _OBJECT_RE.match(line)
        if m and m.group(3) == "TMainMenu":
            start = i
            indent = len(m.group(1))
            break
    if start is None:
        return None
    depth = 0
    for j in range(start, len(lines)):
        s = lines[j]
        if _OBJECT_RE.match(s):
            depth += 1
        elif _END_RE.match(s) and len(_END_RE.match(s).group(1)) == indent:
            depth -= 1
            if depth == 0:
                return lines[start : j + 1]
    return lines[start:]


def parse_menu_tree(block_lines: list[str]) -> list[dict]:
    """Parse a TMainMenu DFM block into a nested list of menu nodes.

    Node = {object_id, kind, caption, onclick, separator, children}.
    The first level returned represents items DIRECTLY under the TMainMenu
    (i.e. the top menu bar). Sub-popups appear under children[].
    """
    root: dict = {"object_id": "ROOT", "kind": "TMainMenu", "children": []}
    stack: list[dict] = [root]

    for line in block_lines[1:]:  # skip the TMainMenu opener
        m_obj = _OBJECT_RE.match(line)
        m_end = _END_RE.match(line)
        m_cap = _CAPTION_RE.match(line)
        m_clk = _ONCLICK_RE.match(line)

        if m_obj:
            kind = m_obj.group(3)
            node = {
                "object_id": m_obj.group(2),
                "kind": kind,
                "caption": None,
                "onclick": None,
                "separator": False,
                "children": [],
            }
            if kind == "TMenuItem":
                stack[-1]["children"].append(node)
            stack.append(node)
        elif m_end and len(stack) > 1:
            top = stack[-1]
            if top.get("caption") == "-":
                top["separator"] = True
            stack.pop()
        elif m_cap and stack[-1].get("kind") == "TMenuItem":
            stack[-1]["caption"] = m_cap.group(1).replace("''", "'")
        elif m_clk and stack[-1].get("kind") == "TMenuItem":
            stack[-1]["onclick"] = m_clk.group(1)

    return root["children"]


# ---------------------------------------------------------------------------
# Menu union matrix


def _norm_caption(c: str) -> str:
    """Normalize caption for cross-build matching: NFKC + collapse whitespace."""
    if not c:
        return ""
    out = unicodedata.normalize("NFKC", c).strip()
    out = re.sub(r"\s+", " ", out)
    return out


def _menu_id_from_caption(caption: str) -> str:
    """Generate stable MENU-<HASH-of-normalized-caption> id."""
    n = _norm_caption(caption)
    safe = re.sub(r"[^0-9A-Za-z가-힣]+", "_", n).strip("_")
    return f"MENU-{safe[:48]}" if safe else "MENU-EMPTY"


def collect_paths(nodes: list[dict], parent: tuple[str, ...] = ()) -> list[dict]:
    """Flatten the tree into [{path: (...captions), depth, leaf, onclick}]."""
    out: list[dict] = []
    for n in nodes:
        cap = _norm_caption(n.get("caption") or "")
        if n.get("separator") or not cap:
            continue
        path = parent + (cap,)
        leaf = not any(c.get("caption") for c in n.get("children", []))
        out.append(
            {
                "path": path,
                "depth": len(path),
                "leaf": leaf,
                "onclick": n.get("onclick"),
                "object_id": n.get("object_id"),
            }
        )
        if not leaf:
            out.extend(collect_paths(n.get("children", []), path))
    return out


def build_matrix(per_build_paths: dict[str, list[dict]]) -> dict:
    """Build a union matrix of menu paths × per-build presence.

    Each row keyed by tuple-of-captions ("path"). Stable MENU-<slug> id assigned
    by the leaf caption (first occurrence wins; collisions get -2/-3 suffix).
    """
    paths_seen: dict[tuple, dict] = {}
    builds_order = list(per_build_paths.keys())

    for bid, paths in per_build_paths.items():
        for p in paths:
            key = p["path"]
            row = paths_seen.setdefault(
                key,
                {
                    "path": list(key),
                    "depth": p["depth"],
                    "leaf": p["leaf"],
                    "onclick_by_build": {},
                    "presence": {b: False for b in builds_order},
                    "object_id_by_build": {},
                },
            )
            row["presence"][bid] = True
            if p.get("onclick"):
                row["onclick_by_build"][bid] = p["onclick"]
            if p.get("object_id"):
                row["object_id_by_build"][bid] = p["object_id"]

    # Assign stable MENU-* ids by leaf caption (de-duplicated by sequence #)
    rows = list(paths_seen.values())
    rows.sort(key=lambda r: ("/".join(r["path"]),))
    cap_seq: dict[str, int] = {}
    for r in rows:
        leaf_cap = r["path"][-1] if r["path"] else "EMPTY"
        base = _menu_id_from_caption(leaf_cap)
        seq = cap_seq.get(base, 0) + 1
        cap_seq[base] = seq
        r["menu_id"] = base if seq == 1 else f"{base}-{seq}"
        r["leaf_caption"] = leaf_cap

    return {
        "builds": builds_order,
        "rows": rows,
        "summary": {
            "total_unique_paths": len(rows),
            "per_build_path_count": {
                bid: sum(1 for r in rows if r["presence"][bid]) for bid in builds_order
            },
            "per_build_top_bar_count": {
                bid: sum(1 for r in rows if r["depth"] == 1 and r["presence"][bid])
                for bid in builds_order
            },
        },
    }


# ---------------------------------------------------------------------------
# PAS handler scanner


_PROCEDURE_RE = re.compile(
    r"^procedure\s+T\w+\.(Menu\w+Click)\s*\(\s*Sender\s*:\s*TObject\s*\)\s*;",
    re.MULTILINE,
)
_ALL_PROCEDURE_RE = re.compile(
    r"^procedure\s+T\w+\.(\w+)\s*\(",
    re.MULTILINE,
)


def parse_handlers(pas_text: str) -> dict[str, str]:
    matches = list(_PROCEDURE_RE.finditer(pas_text))
    handlers: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(pas_text)
        handlers[name] = pas_text[start:end]
    return handlers


def parse_form_lifecycle(pas_text: str) -> dict[str, str]:
    """Return body of FormShow / FormCreate / FormActivate procedures (if any)."""
    targets = {"FormShow", "FormCreate", "FormActivate", "FormClose"}
    matches = list(_ALL_PROCEDURE_RE.finditer(pas_text))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1)
        if name not in targets:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(pas_text)
        out[name] = pas_text[start:end]
    return out


def _strip_string_literals(body: str) -> str:
    """Remove Pascal single-quoted string literals (defensive: PAS may contain
    hardcoded credentials; we never store literal contents in the JSON).
    """
    return re.sub(r"'(?:''|[^'])*'", "''", body)


_FORM_REF_RE = re.compile(
    r"\b(T(?:Subu|Sobo|Tong|Seak|Seek|Seok|Seep|Base|Subo|Smms|Exls)\w*)\b"
)
_SHOWMODAL_RE = re.compile(r"\b(\w+)\.ShowModal\b")
_CREATE_RE = re.compile(r"\b(\w+)\s*:=\s*(T\w+)\.Create\s*\(", re.IGNORECASE)


_SEEK_USES_RE = re.compile(r"Seek_Uses\s*\(\s*'([^']+)'\s*\)")
_MENU_VIS_RE = re.compile(r"\b(Menu\w+)\.Visible\s*:=\s*(True|False)", re.IGNORECASE)
_TOOLBAR_VIS_RE = re.compile(r"\b(ToolBar\w*)\.Visible\s*:=\s*(True|False)", re.IGNORECASE)
_MENU_ENABLED_RE = re.compile(r"\b(Menu\w+)\.Enabled\s*:=\s*(True|False)", re.IGNORECASE)


def analyze_handler(body: str) -> dict:
    """Analyze a handler body. NB: license keys are matched BEFORE stripping
    literals (Seek_Uses arg is a literal); structural patterns are matched
    AFTER stripping to defensively avoid scraping credential literals.
    """
    seek_uses = sorted(set(_SEEK_USES_RE.findall(body)))
    sanitized = _strip_string_literals(body)
    forms = sorted(set(_FORM_REF_RE.findall(sanitized)))
    shown = sorted(set(_SHOWMODAL_RE.findall(sanitized)))
    creates = [{"var": v, "type": t} for v, t in _CREATE_RE.findall(sanitized)]
    menu_vis = [{"target": t, "value": v} for t, v in _MENU_VIS_RE.findall(sanitized)]
    toolbar_vis = [{"target": t, "value": v} for t, v in _TOOLBAR_VIS_RE.findall(sanitized)]
    menu_en = [{"target": t, "value": v} for t, v in _MENU_ENABLED_RE.findall(sanitized)]
    return {
        "form_types_referenced": forms,
        "showmodal_targets": shown,
        "create_calls": creates,
        "menu_visibility_writes": menu_vis,
        "menu_enabled_writes": menu_en,
        "toolbar_visibility_writes": toolbar_vis,
        "license_keys_checked": seek_uses,
        "byte_size": len(body),
    }


# ---------------------------------------------------------------------------
# Main


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    builds = catalog["builds"]

    trees: dict[str, dict] = {}
    handlers_summary: dict[str, dict] = {}
    per_build_paths: dict[str, list[dict]] = {}

    for b in builds:
        bid = b["build_id"]
        bdir = ROOT / b["path"]
        dfm_path = bdir / "Chul.dfm"
        pas_path = bdir / "Chul.pas"
        if not dfm_path.exists():
            continue
        dfm_text = read_cp949(dfm_path)
        block = find_main_menu_block(dfm_text)
        tree = parse_menu_tree(block) if block else []
        trees[bid] = {
            "build_id": bid,
            "path": b["path"],
            "main_menu_found": block is not None,
            "top_bar": [
                {
                    "object_id": n.get("object_id"),
                    "caption": _norm_caption(n.get("caption") or ""),
                    "onclick": n.get("onclick"),
                    "children_count": len(n.get("children", [])),
                }
                for n in tree
            ],
            "tree": tree,
        }
        per_build_paths[bid] = collect_paths(tree)

        if pas_path.exists():
            pas_text = read_cp949(pas_path)
            hs = parse_handlers(pas_text)
            analyzed = {name: analyze_handler(body) for name, body in hs.items()}
            lifecycle = {
                name: analyze_handler(body)
                for name, body in parse_form_lifecycle(pas_text).items()
            }
            agg_seek = sorted(
                {k for v in analyzed.values() for k in v["license_keys_checked"]}
                | {k for v in lifecycle.values() for k in v["license_keys_checked"]}
            )
            agg_menu_writes = [
                {"source": "menu_handler", "handler": name, **w}
                for name, v in analyzed.items()
                for w in v["menu_visibility_writes"]
            ] + [
                {"source": "form_lifecycle", "handler": name, **w}
                for name, v in lifecycle.items()
                for w in v["menu_visibility_writes"]
            ]
            agg_toolbar_writes = [
                {"source": "menu_handler", "handler": name, **w}
                for name, v in analyzed.items()
                for w in v["toolbar_visibility_writes"]
            ] + [
                {"source": "form_lifecycle", "handler": name, **w}
                for name, v in lifecycle.items()
                for w in v["toolbar_visibility_writes"]
            ]
            handlers_summary[bid] = {
                "build_id": bid,
                "path": b["path"],
                "handler_count": len(hs),
                "form_lifecycle_count": len(lifecycle),
                "build_aggregate": {
                    "license_keys_used": agg_seek,
                    "license_key_count": len(agg_seek),
                    "menu_visibility_writes": agg_menu_writes,
                    "toolbar_visibility_writes": agg_toolbar_writes,
                },
                "handlers": analyzed,
                "form_lifecycle": lifecycle,
            }

    matrix = build_matrix(per_build_paths)

    OUT_TREES.parent.mkdir(parents=True, exist_ok=True)
    OUT_TREES.write_text(
        json.dumps(
            {
                "source_catalog": "analysis/welove_chul_builds.json",
                "secrets_policy": "Per docs/secrets-policy.md (G3): DFM/PAS 본문(메뉴 캡션·핸들러 이름)만 추출. Config.Ini 자격증명 미접근.",
                "builds": list(trees.values()),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    OUT_MATRIX.write_text(
        json.dumps(
            {
                "source_catalog": "analysis/welove_chul_builds.json",
                "secrets_policy": "Per docs/secrets-policy.md (G3): 메뉴 캡션 union (UI 라벨 GREEN 등급).",
                "matrix": matrix,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    OUT_HANDLERS.write_text(
        json.dumps(
            {
                "source_catalog": "analysis/welove_chul_builds.json",
                "secrets_policy": "Per docs/secrets-policy.md (G3): Pascal 핸들러 본문 분석 — 폼 타입·ShowModal·Create·Menu*.Visible 라이트만 추출. SQL/암호 미인용.",
                "builds": list(handlers_summary.values()),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"wrote {OUT_TREES.relative_to(ROOT)}")
    print(f"wrote {OUT_MATRIX.relative_to(ROOT)}")
    print(f"wrote {OUT_HANDLERS.relative_to(ROOT)}")
    print()
    print("Top-bar counts (matrix view):")
    for bid, n in matrix["summary"]["per_build_top_bar_count"].items():
        print(f"  {bid:35s} top_bar={n:>3d}  total_paths={matrix['summary']['per_build_path_count'][bid]}")
    print(f"Total unique menu paths across all builds: {matrix['summary']['total_unique_paths']}")


if __name__ == "__main__":
    main()
