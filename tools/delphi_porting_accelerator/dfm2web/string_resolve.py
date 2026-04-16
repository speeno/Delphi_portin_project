"""Resolve integer resource IDs in normalized DFM trees to human-readable strings.

Uses .rc STRINGTABLE maps and PAS resourcestring blocks as lookup sources.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_STRING_FIELDS = ('caption', 'text', 'hint')


def _load_rc(path: Path) -> dict[int, str]:
    tools_root = Path(__file__).resolve().parents[2]
    bridge = tools_root / 'res_string_bridge.py'
    if str(bridge.parent) not in sys.path:
        sys.path.insert(0, str(bridge.parent))
    from res_string_bridge import load_rc_stringtable  # noqa: PLC0415
    return load_rc_stringtable(path)


def build_string_id_map(rc_paths: list[Path]) -> dict[int, str]:
    merged: dict[int, str] = {}
    for p in rc_paths:
        merged.update(_load_rc(p))
    return merged


def _is_numeric_id(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit() and len(stripped) <= 10:
            return int(stripped)
    return None


def _resolve_field(value: Any, id_map: dict[int, str]) -> tuple[Any, bool]:
    rid = _is_numeric_id(value)
    if rid is not None and rid in id_map:
        return id_map[rid], True
    return value, False


def apply_resource_strings(
    node: dict[str, Any],
    id_map: dict[int, str],
    pas_rs: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Walk *node* in-place, replacing resource IDs with strings.

    Returns a list of unresolved entries for reporting.
    """
    unresolved: list[dict[str, Any]] = []
    _walk(node, id_map, pas_rs or {}, unresolved)
    return unresolved


def _walk(
    node: dict[str, Any],
    id_map: dict[int, str],
    pas_rs: dict[str, str],
    unresolved: list[dict[str, Any]],
) -> None:
    for field in _STRING_FIELDS:
        original = node.get(field)
        if original is None or original == '':
            continue
        resolved, ok = _resolve_field(original, id_map)
        if ok:
            node[field] = resolved
        elif _is_numeric_id(original) is not None:
            unresolved.append({
                'node': node.get('name', ''),
                'field': field,
                'value': original,
            })

    for col in node.get('gridColumns') or []:
        cap = col.get('caption')
        if cap is not None:
            resolved, ok = _resolve_field(cap, id_map)
            if ok:
                col['caption'] = resolved

    for child in node.get('children') or []:
        _walk(child, id_map, pas_rs, unresolved)
