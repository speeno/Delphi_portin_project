"""
텍스트 DFM 줄 목록에서 속성 값이 여러 줄에 걸친 블록을 한 논리 줄로 합친다.

- `Prop = (` … `)`  (예: Items.Strings)
- `Prop = {` … `}`  (예: Glyph.Data, Picture.Data 등 바이너리/16진 덤프)
- `Prop = <` … `>`  (예: Columns = < item … end … >)

object/inherited/end 줄은 변경하지 않는다.
"""

from __future__ import annotations

import re
from typing import List


_OBJ = re.compile(r"^(object|inherited)\s", re.I)
_END = re.compile(r"^end\s*(\.|$)", re.I)


def _paren_depth_delta(s: str) -> int:
    return s.count("(") - s.count(")")


def _brace_depth_delta(s: str) -> int:
    return s.count("{") - s.count("}")


def _angle_depth_delta(s: str) -> int:
    return s.count("<") - s.count(">")


def merge_property_blocks(lines: List[str]) -> List[str]:
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if _OBJ.match(stripped) or stripped == "end" or _END.match(stripped):
            out.append(raw)
            i += 1
            continue

        # Prop = ( … ) — Items.Strings 등
        if "=" in raw and "(" in raw:
            idx = raw.index("=")
            tail = raw[idx + 1 :]
            if "(" in tail:
                depth = _paren_depth_delta(tail)
                if depth > 0:
                    buf = [raw.rstrip("\r\n")]
                    i += 1
                    while i < n and depth > 0:
                        nxt = lines[i]
                        buf.append(nxt.rstrip("\r\n"))
                        depth += _paren_depth_delta(nxt)
                        i += 1
                    out.append("\n".join(buf))
                    continue

        # Prop = { … } — Glyph.Data 등
        if "=" in raw and "{" in raw:
            idx = raw.index("=")
            tail = raw[idx + 1 :]
            depth = _brace_depth_delta(tail)
            if depth > 0:
                buf = [raw.rstrip("\r\n")]
                i += 1
                while i < n and depth > 0:
                    nxt = lines[i]
                    buf.append(nxt.rstrip("\r\n"))
                    depth += _brace_depth_delta(nxt)
                    i += 1
                out.append("\n".join(buf))
                continue

        # Prop = < … > — Columns = < item … end … > 등
        if "=" in raw and "<" in raw:
            idx = raw.index("=")
            tail = raw[idx + 1 :]
            if "<" in tail:
                depth = _angle_depth_delta(tail)
                if depth > 0:
                    buf = [raw.rstrip("\r\n")]
                    i += 1
                    while i < n and depth > 0:
                        nxt = lines[i]
                        buf.append(nxt.rstrip("\r\n"))
                        depth += _angle_depth_delta(nxt)
                        i += 1
                    out.append("\n".join(buf))
                    continue

        out.append(raw)
        i += 1

    return out
