from __future__ import annotations

import re
from typing import Any


BOOL_MAP = {'True': True, 'False': False}
SET_RE = re.compile(r'^\[(.*)\]$')
INT_RE = re.compile(r'^-?\d+$')
FLOAT_RE = re.compile(r'^-?\d+\.\d+$')


def decode_delphi_string_expr(raw: str) -> str:
    if "'" not in raw and '#' not in raw:
        return raw

    parts: list[str] = []
    i = 0
    while i < len(raw):
        ch = raw[i]
        if ch == "'":
            j = i + 1
            buf = []
            while j < len(raw):
                if raw[j] == "'":
                    if j + 1 < len(raw) and raw[j + 1] == "'":
                        buf.append("'")
                        j += 2
                        continue
                    break
                buf.append(raw[j])
                j += 1
            parts.append(''.join(buf))
            i = j + 1
            continue
        if ch == '#':
            j = i + 1
            while j < len(raw) and raw[j].isdigit():
                j += 1
            try:
                parts.append(chr(int(raw[i + 1:j])))
            except ValueError:
                parts.append(raw[i:j])
            i = j
            continue
        i += 1
    return ''.join(parts)


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw in BOOL_MAP:
        return BOOL_MAP[raw]
    if INT_RE.match(raw):
        return int(raw)
    if FLOAT_RE.match(raw):
        return float(raw)
    set_match = SET_RE.match(raw)
    if set_match:
        body = set_match.group(1).strip()
        if not body:
            return []
        return [x.strip() for x in body.split(',')]
    if raw.startswith("'") or '#' in raw:
        return decode_delphi_string_expr(raw)
    return raw
