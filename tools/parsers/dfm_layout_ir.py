"""
레이아웃 JSON(parse_dfm_layout) 노드에 Anchors·Align·TabOrder 기반 layout_ir 보강.
"""

from __future__ import annotations

import re
from typing import Any


def parse_anchors(val: str | None) -> list[str]:
    if not val:
        return []
    return re.findall(r"\bak\w+", val)


def enrich_layout_document(doc: dict[str, Any]) -> dict[str, Any]:
    root = doc.get("root")
    if root is None:
        return doc

    def walk(node: dict[str, Any]) -> None:
        children: list[dict[str, Any]] = list(node.get("children") or [])
        indexed: list[tuple[int, int, dict[str, Any]]] = []
        for i, c in enumerate(children):
            layout = c.get("layout") or {}
            raw = (layout.get("TabOrder") or "").strip()
            try:
                ti = int(raw)
            except ValueError:
                ti = 10**9 + i
            indexed.append((ti, i, c))
        indexed.sort(key=lambda x: (x[0], x[1]))
        for z, (_, __, c) in enumerate(indexed):
            ir = c.setdefault("layout_ir", {})
            ir["z_index"] = z

        for c in children:
            layout = c.get("layout") or {}
            ir = c.setdefault("layout_ir", {})
            ir["anchors"] = parse_anchors(layout.get("Anchors"))
            raw = (layout.get("TabOrder") or "").strip()
            try:
                ir["tab_order"] = int(raw)
            except ValueError:
                ir["tab_order"] = None
            al = (layout.get("Align") or "").strip()
            ir["align"] = al or None
            walk(c)

    walk(root)
    return doc
