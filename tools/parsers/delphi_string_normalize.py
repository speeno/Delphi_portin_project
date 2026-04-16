"""
델파이 DFM 문자열 속성용 표시 정규화.

- `#13#10` 등 숫자 이스케이프 → 문자
- `''` → `'`
- 인접한 작은따옴표 문자열 리터럴(`'a'#13#10'b'`)을 구분자(이미 확장된 제어문자)를 유지하며 이어붙임
"""

from __future__ import annotations

import re


def normalize_delphi_display_string(val: str | None) -> str:
    if not val:
        return ""
    v = val.strip()
    v = re.sub(r"#(\d+)", lambda m: chr(int(m.group(1))), v)
    one = re.fullmatch(r"'((?:[^']|'')*)'", v)
    if one:
        return one.group(1).replace("''", "'")
    chunks = list(re.finditer(r"'((?:[^']|'')*)'", v))
    if not chunks:
        return v.strip().strip("'")

    out: list[str] = []
    prev = 0
    for m in chunks:
        out.append(v[prev : m.start()])
        out.append(m.group(1).replace("''", "'"))
        prev = m.end()
    out.append(v[prev:])
    return "".join(out)
