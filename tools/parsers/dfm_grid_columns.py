"""
TDBGridEh 등 `Columns = < ... >` 블롭에서 FieldName·Title.Caption 목록 추출.
"""

from __future__ import annotations

import re
from typing import Any


def extract_grid_columns(columns_blob: str | None) -> list[dict[str, Any]]:
    if not columns_blob or not isinstance(columns_blob, str):
        return []
    s = columns_blob.strip()
    if not s.startswith("<"):
        return []

    parts = re.split(r"(?m)^\s*item\s*$", s)
    out: list[dict[str, Any]] = []
    for part in parts[1:]:
        if "end" not in part and "Title.Caption" not in part:
            continue
        fm = re.search(
            r"FieldName\s*=\s*(?:'((?:[^']|'')*)'|(\w+))",
            part,
            re.I,
        )
        tm = re.search(
            r"Title\.Caption\s*=\s*'((?:[^']|'')*)'",
            part,
            re.I,
        )
        if not tm and not fm:
            continue
        field_val = None
        if fm:
            field_val = (fm.group(1) or fm.group(2) or "").replace("''", "'")
        out.append(
            {
                "field_name": field_val or None,
                "title": tm.group(1).replace("''", "'") if tm else None,
            }
        )
    return out
