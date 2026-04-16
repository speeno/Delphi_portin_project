"""
델파이 DFM 스칼라/색 리터럴 처리 (dfm2html_project/dfm2html/parser/values.py 에서 이식).

HTML·레이아웃 JSON 문자열화 시 참고한다.
"""

from __future__ import annotations

import re
from typing import Any, List

# dfm2html COLOR_MAP 과 동기
COLOR_MAP = {
    "clBtnFace": "#f0f0f0",
    "clWindowText": "#000000",
    "clWindow": "#ffffff",
    "clBtnText": "#000000",
    "clWhite": "#ffffff",
    "clBlack": "#000000",
    "clRed": "#ff0000",
    "clBlue": "#0000ff",
    "clGreen": "#008000",
    "clGray": "#808080",
    "clSilver": "#c0c0c0",
    "clYellow": "#ffff00",
    "clInfoBk": "#ffffe1",
}


def decode_delphi_string(value: str) -> str:
    """작은따옴표·#NNN 이스케이프를 풀어 표시용 문자열로 만든다."""
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")

    parts = re.findall(r"'[^']*(?:''[^']*)*'|#\d+", value)
    if parts:
        out: List[str] = []
        for part in parts:
            if part.startswith("#"):
                try:
                    out.append(chr(int(part[1:])))
                except ValueError:
                    out.append(part)
            else:
                out.append(part[1:-1].replace("''", "'"))
        return "".join(out)
    return value


def layout_value_as_str(v: Any) -> str:
    """dfm2html 파서가 만든 파이썬 값을 레이아웃 JSON 문자열 필드로 직렬화."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return str(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        if not v:
            return "[]"
        return "[" + ", ".join(str(x) for x in v) + "]"
    return str(v)
