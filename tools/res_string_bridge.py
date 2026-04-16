"""
델파이 리소스 문자열(.rc STRINGTABLE 등)과 폼/코드의 숫자 ID를 잇는 브리지(설계·최소 파서).

DFM 파서는 `.dfm` 안에 **문자열로 적힌** Caption/Text만 본다. `LoadStr(123)` 형태나
리소스 전용 문자열은 이 모듈(또는 후속 확장)으로 ID→문자열 테이블을 만든 뒤
별도 조인 단계에서 매핑한다.

최소 지원: 텍스트 `.rc` 안의 `12345, "문자열"` / `12345, "escaped "" quote"` 패턴을
정수 키 → 문자열 dict 로 추출한다. 바이너리 `.res`는 포함하지 않는다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


_RC_STRINGTABLE_LINE = re.compile(
    r'^\s*(\d+)\s*,\s*"((?:\\.|[^"\\])*)"\s*$',
    re.MULTILINE,
)


def parse_rc_stringtable_entries(rc_text: str) -> dict[int, str]:
    """
    STRINGTABLE 블록 밖의 숫자, "문자열" 줄도 일부 잡을 수 있으므로,
    가능하면 STRINGTABLE … BEGIN … END 사이만 잘라 넣는 것이 안전하다.
    """
    out: dict[int, str] = {}
    for m in _RC_STRINGTABLE_LINE.finditer(rc_text):
        sid = int(m.group(1))
        raw = m.group(2).replace(r"\"", '"').replace(r"\\", "\\")
        out[sid] = raw
    return out


def load_rc_stringtable(path: str | Path) -> dict[int, str]:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    return parse_rc_stringtable_entries(text)


def explain_res_bridge_usage() -> str:
    return (
        "1) Delphi IDE 또는 brcc32 등으로 .rc를 확보한다.\n"
        "2) load_rc_stringtable('.rc') 로 dict 을 만든다.\n"
        "3) PAS/DFM에서 추출한 숫자 ID를 키로 조회해 UI 라벨 후보를 만든다.\n"
        "4) 바이너리 .res 는 외부 도구로 .rc 변환 후 동일 파이프라인을 쓴다."
    )


def extract_resourcestrings_from_pas(path: str | Path) -> dict[str, str]:
    """
    .pas 의 resourcestring 블록을 추출한다 (dfm2html_project 로직, CP949 등은 delphi_source_encoding).
    """
    p = Path(path)
    if not p.is_file():
        return {}
    tools = Path(__file__).resolve().parent
    parsers = tools / "parsers"
    d2h = tools / "dfm2html_project"
    if str(parsers) not in sys.path:
        sys.path.insert(0, str(parsers))
    if str(d2h) not in sys.path:
        sys.path.insert(0, str(d2h))
    from delphi_source_encoding import read_delphi_source  # noqa: PLC0415
    from dfm2html.resources.pas_resourcestring import (  # noqa: PLC0415
        extract_resourcestrings_from_text,
    )

    text = read_delphi_source(str(p))
    return extract_resourcestrings_from_text(text)
