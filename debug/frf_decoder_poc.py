"""
frf_decoder — `.frf` (FastReport VCL 4.x 바이너리) → Canonical IR (JSON) PoC v0.1.0

원본 알고리즘 출처:
  - FastReports/FreeReport (BSD-2-Clause) — `Source/FR_Class.pas` 의 `LoadFromStream`
    Copyright (c) 1998-2008, Fast Reports Inc.
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

스키마 정본:
  - analysis/print_specs/frf_ir_schema.md (v0.1.0)
  - analysis/research/c7_oss_shortlist.md (F-01 / F-03 즉시 재사용)

본 PoC 의 한계:
  - `.frf` 바이너리의 *완전한* TStream RTTI 디시리얼라이저는 운영급 1차 PoC 범위 밖이다.
  - 본 v0 는 **휴리스틱 스캐너**: Pascal-style `WORD-prefixed string` (length 2-byte LE
    + ASCII bytes) 를 따라 Page/Band/Object 트리를 *형태적으로* 식별하고, 인접한
    32-bit LE int 4 개를 좌표 (Left/Top/Width/Height TWIPs) 로 가설 추출한다.
  - 실패한 객체는 IR 의 `unsupported_objects[]` 에 *수집* 한다 (실패-허용).
  - 본 PoC 의 목적은 (a) `Report_1_21.frf` 1 양식이 본 디코더로 부분 IR 생성 가능함을
    입증, (b) IR→HTML 컴파일러의 입력 데이터를 PoC 단계에서 공급하는 것 — 운영 도입
    이전 단계.

CLI:
  python -m debug.frf_decoder_poc <path/to/file.frf> [--out path/to/ir.json]

라이선스 의무 (BSD-2 / MIT):
  본 디코더가 운영에 incorporate 될 경우 NOTICE 파일 + 헤더 주석에 위 저작권
  표시를 *필수* 로 보존한다 (analysis/research/c7_oss_license_matrix.md §2.1).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1.0"
DECODER_VERSION = "0.1.0"

TWIPS_PER_MM = 1440.0 / 25.4


def twips_to_mm(twips: int) -> float:
    return round(twips / TWIPS_PER_MM, 4)


# ---------------------------------------------------------------------------
# Low-level binary reader
# ---------------------------------------------------------------------------


class BinReader:
    """단순 byte buffer 위의 little-endian 리더 (최소한)."""

    def __init__(self, data: bytes) -> None:
        self.buf = data
        self.size = len(data)
        self.pos = 0

    def remaining(self) -> int:
        return self.size - self.pos

    def read(self, n: int) -> bytes:
        if self.pos + n > self.size:
            raise EOFError(f"read past end at {self.pos} (+{n})")
        chunk = self.buf[self.pos : self.pos + n]
        self.pos += n
        return chunk

    def read_u8(self) -> int:
        return self.read(1)[0]

    def read_u16_le(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def read_i32_le(self) -> int:
        return struct.unpack("<i", self.read(4))[0]

    def peek_word_str(self, max_len: int = 64) -> str | None:
        """현재 위치에서 `WORD length + ASCII bytes` 형식 문자열을 시도 read."""
        if self.remaining() < 2:
            return None
        ln = struct.unpack_from("<H", self.buf, self.pos)[0]
        if ln == 0 or ln > max_len:
            return None
        if self.pos + 2 + ln > self.size:
            return None
        candidate = self.buf[self.pos + 2 : self.pos + 2 + ln]
        if not all(0x20 <= b < 0x7F or b in (0x09, 0x0D, 0x0A) for b in candidate):
            return None
        return candidate.decode("ascii", errors="replace")


# ---------------------------------------------------------------------------
# Heuristic scanner — extracts (offset, name) pairs of Pascal-style strings
# ---------------------------------------------------------------------------


@dataclass
class StringHit:
    offset: int
    text: str


def scan_word_strings(buf: bytes, min_len: int = 3, max_len: int = 64) -> list[StringHit]:
    """버퍼 전역에서 WORD-prefixed ASCII string 후보를 *모두* 수집한다.

    ASCII printable (또는 한글 EUC-KR 일부 포함 가능 — 본 PoC 는 ASCII 우선) 만 채택.
    """
    hits: list[StringHit] = []
    i = 0
    n = len(buf)
    while i + 2 <= n:
        ln = buf[i] | (buf[i + 1] << 8)
        if min_len <= ln <= max_len and i + 2 + ln <= n:
            data = buf[i + 2 : i + 2 + ln]
            if all(0x20 <= b < 0x7F for b in data):
                try:
                    txt = data.decode("ascii")
                except UnicodeDecodeError:
                    txt = None
                if txt is not None:
                    hits.append(StringHit(offset=i, text=txt))
                    i += 2 + ln
                    continue
        i += 1
    return hits


# ---------------------------------------------------------------------------
# Object type guesser
# ---------------------------------------------------------------------------


_PAGE_PAT = re.compile(r"^Page\d+$")
_BAND_PAT = re.compile(r"^Band\d+$")
_MEMO_PAT = re.compile(r"^Memo\d+$")
_PIC_PAT = re.compile(r"^Picture\d+$|^Pic\d+$")
_LINE_PAT = re.compile(r"^Line\d+$")
_RECT_PAT = re.compile(r"^Rect\d+$|^Shape\d+$")
_BARCODE_PAT = re.compile(r"^Barcode\d+$|^BarCode\d+$|^BC\d+$")
_DATA_TOKEN_PAT = re.compile(r"^\[[A-Za-z_][\w\.]*\]$")


def classify(text: str) -> str | None:
    if _PAGE_PAT.match(text):
        return "page"
    if _BAND_PAT.match(text):
        return "band"
    if _MEMO_PAT.match(text):
        return "text_obj"
    if _PIC_PAT.match(text):
        return "picture_obj"
    if _LINE_PAT.match(text):
        return "line_obj"
    if _RECT_PAT.match(text):
        return "rect_obj"
    if _BARCODE_PAT.match(text):
        return "barcode_obj"
    if _DATA_TOKEN_PAT.match(text):
        return "data_token"
    return None


# ---------------------------------------------------------------------------
# Coordinate extractor — try to read 4 little-endian int32 right after a
# scanned object name; treat as (Left, Top, Width, Height) in TWIPs.
# ---------------------------------------------------------------------------


def _is_plausible_rect(rect: dict) -> bool:
    """rect_mm 4 값이 *현실적* (0 ≤ 좌표 ≤ 600 mm, 0 < 크기 ≤ 600 mm) 인지 검증."""
    x, y, w, h = rect["x_mm"], rect["y_mm"], rect["w_mm"], rect["h_mm"]
    if not (-50.0 <= x <= 600.0 and -50.0 <= y <= 1500.0):
        return False
    if not (0.1 <= w <= 600.0 and 0.1 <= h <= 1500.0):
        return False
    return True


def try_extract_rect_after(buf: bytes, after_offset: int, search_window: int = 16) -> dict | None:
    """객체 이름 직후의 가까운 위치에서 (Left,Top,Width,Height) TWIPs 추출 시도.

    FreeReport 2.3 의 직렬화 규칙은 클래스명 직후 마커 → 좌표 4 개. 본 PoC 는 마커
    바이트 0~`search_window` 만큼 스캔하면서 4 개 LE int32 가 *합리적 범위* (절대값
    ≤ 65535 TWIPs ≈ 1156 mm) 에 들면 채택.
    """
    n = len(buf)
    for skip in range(0, search_window):
        base = after_offset + skip
        if base + 16 > n:
            return None
        try:
            l, t, w, h = struct.unpack_from("<iiii", buf, base)
        except struct.error:
            continue
        if all(-65535 <= v <= 100000 for v in (l, t, w, h)) and 0 < w <= 100000 and 0 < h <= 100000:
            return {
                "x_mm": twips_to_mm(l),
                "y_mm": twips_to_mm(t),
                "w_mm": twips_to_mm(w),
                "h_mm": twips_to_mm(h),
                "raw_twips": {"left": l, "top": t, "width": w, "height": h},
                "offset": base,
            }
    return None


# ---------------------------------------------------------------------------
# Decoder main
# ---------------------------------------------------------------------------


@dataclass
class IR:
    schema_version: str = SCHEMA_VERSION
    source: dict = field(default_factory=dict)
    report: dict = field(default_factory=dict)
    pages: list = field(default_factory=list)
    data_sources: list = field(default_factory=list)
    expressions_dictionary: dict = field(default_factory=dict)
    variant_profile: Any = None
    unsupported_objects: list = field(default_factory=list)
    decoder_warnings: list = field(default_factory=list)


def decode_frf(path: str | os.PathLike) -> dict:
    p = Path(path)
    raw = p.read_bytes()
    n = len(raw)

    ir = IR(
        source={
            "kind": "frf",
            "signature": _detect_signature(raw),
            "filename": p.name,
            "decoded_at": datetime.now(timezone.utc).isoformat(),
            "decoder_version": DECODER_VERSION,
            "raw_size_bytes": n,
        },
        report={
            "name": p.stem,
            "title": p.stem,
            "author": "(unknown)",
            "creator_version": "FastReport VCL 4.x (assumed)",
            "page_count_hint": 1,
        },
    )

    hits = scan_word_strings(raw)
    if not hits:
        ir.decoder_warnings.append({
            "code": "FRF_W_010",
            "message": "WORD-prefixed string 미발견 — 시그니처/엔코딩 차이 가능성",
        })
        return _ir_to_dict(ir)

    classified = [(h, classify(h.text)) for h in hits]
    classified = [(h, k) for h, k in classified if k is not None]

    current_page: dict | None = None
    current_band: dict | None = None
    last_object: dict | None = None

    for hit, kind in classified:
        end_offset = hit.offset + 2 + len(hit.text)

        if kind == "page":
            current_page = {
                "name": hit.text,
                "size_mm": {"width": 100.0, "height": 148.0},
                "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                "orientation": "portrait",
                "columns": 1,
                "background": None,
                "bands": [],
            }
            ir.pages.append(current_page)
            current_band = None
            last_object = None
            continue

        if current_page is None:
            current_page = {
                "name": "Page1_inferred",
                "size_mm": {"width": 100.0, "height": 148.0},
                "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                "orientation": "portrait",
                "columns": 1,
                "background": None,
                "bands": [],
            }
            ir.pages.append(current_page)
            ir.decoder_warnings.append({
                "code": "FRF_W_011",
                "message": "Page 마커 없이 객체 발견 — Page1_inferred 자동 생성",
            })

        if kind == "band":
            current_band = {
                "name": hit.text,
                "type": "MasterData",
                "y_mm": 0.0,
                "height_mm": 0.0,
                "data_source_ref": None,
                "objects": [],
            }
            current_page["bands"].append(current_band)
            last_object = None
            continue

        if current_band is None:
            current_band = {
                "name": "Band1_inferred",
                "type": "MasterData",
                "y_mm": 0.0,
                "height_mm": 0.0,
                "data_source_ref": None,
                "objects": [],
            }
            current_page["bands"].append(current_band)
            ir.decoder_warnings.append({
                "code": "FRF_W_012",
                "message": "Band 마커 없이 객체 발견 — Band1_inferred 자동 생성",
            })

        if kind in ("text_obj", "picture_obj", "line_obj", "rect_obj", "barcode_obj"):
            ir_type_map = {
                "text_obj": "Text",
                "picture_obj": "Picture",
                "line_obj": "Line",
                "rect_obj": "Rect",
                "barcode_obj": "Barcode",
            }
            rect = try_extract_rect_after(raw, end_offset, search_window=24)
            obj = {
                "name": hit.text,
                "type": ir_type_map[kind],
                "rect_mm": (
                    {
                        "x": rect["x_mm"],
                        "y": rect["y_mm"],
                        "w": rect["w_mm"],
                        "h": rect["h_mm"],
                    }
                    if rect and _is_plausible_rect(rect)
                    else {"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}
                ),
                "z_order": len(current_band["objects"]),
                "visible": True,
                "rotation_deg": 0,
                "border": {
                    "left": False,
                    "top": False,
                    "right": False,
                    "bottom": False,
                    "color": "#888888",
                    "width_pt": 1.0,
                    "style": "solid",
                },
                "fill": {"color": "#FFFFFF", "transparent": True},
                "style": {
                    "font_family": "NanumGothic",
                    "font_size_pt": 12.0,
                    "font_weight": "normal",
                    "font_italic": False,
                    "font_underline": False,
                    "color": "#222222",
                    "halign": "left",
                    "valign": "top",
                    "wordwrap": True,
                    "padding_pt": {"top": 1.0, "right": 1.0, "bottom": 1.0, "left": 1.0},
                    "format": None,
                } if kind == "text_obj" else {},
                "binding": {
                    "kind": "literal",
                    "value": "",
                    "raw": "",
                },
                "unsupported_props": (
                    {}
                    if rect and _is_plausible_rect(rect)
                    else {"rect_extraction": "failed_v0" if not rect else "out_of_range_v0",
                          "rect_raw_twips": rect["raw_twips"] if rect else None}
                ),
            }
            current_band["objects"].append(obj)
            last_object = obj
            continue

        if kind == "data_token":
            token_text = hit.text
            tokens = _tokenize_frf_text(token_text)
            if last_object is not None and last_object["type"] in ("Text", "Picture", "Barcode"):
                last_object["binding"] = {
                    "kind": "expression" if any(t["type"] != "literal" for t in tokens) else "literal",
                    "value": None if any(t["type"] != "literal" for t in tokens) else token_text,
                    "raw": token_text,
                    "tokens": tokens,
                }
                for tok in tokens:
                    if tok["type"] == "field":
                        if tok["table"] is None:
                            key = f"[{tok['column']}]"
                        else:
                            key = f"[{tok['table']}.{tok['column']}]"
                        ir.expressions_dictionary[key] = {
                            "table": tok["table"],
                            "column": tok["column"],
                        }
            else:
                ir.decoder_warnings.append({
                    "code": "FRF_W_020",
                    "message": f"binding 토큰 발견 그러나 직전 객체 없음: {token_text}",
                })

    _post_process(ir)
    return _ir_to_dict(ir)


def _detect_signature(raw: bytes) -> str:
    """첫 일부 바이트에서 'FRF' / 'FRF15' / 'FRF20' 패턴을 탐색."""
    for tag in (b"FRF20", b"FRF15", b"FRF"):
        idx = raw.find(tag, 0, 64)
        if idx >= 0:
            return tag.decode("ascii")
    head = raw[:8].hex()
    return f"unknown:{head}"


_TOKEN_FIELD_PAT = re.compile(r"\[([A-Za-z_][\w]*)\.([A-Za-z_][\w]*)(?:\s+\"([^\"]*)\")?\]")
_TOKEN_SIMPLE_PAT = re.compile(r"^\[([A-Za-z_][\w]*)\]$")
_RESERVED_FUNCTION_NAMES = {"PageN", "TotalPages", "Date", "Time", "DateTime", "Page"}


def _tokenize_frf_text(text: str) -> list[dict]:
    """`[Table.Column]` / `[Table.Column "fmt"]` / 단일 `[Token]` 패턴을 토크나이즈.

    레거시 `.frf` 양식은 `[Table.Column]` 형식보다 *단일 식별자* `[Gname]`/`[Gadd1]` 을
    더 많이 사용한다 (Pascal Sg_Csum 데이터셋). 본 토크나이저는 함수 예약명
    (`PageN`/`Date` 등) 외 모든 단일 토큰을 *암시적 field* (`table=None`, `column=…`)
    로 분류해 expressions_dictionary 에 등록한다.
    """
    tokens: list[dict] = []
    cursor = 0
    for m in _TOKEN_FIELD_PAT.finditer(text):
        if m.start() > cursor:
            tokens.append({"type": "literal", "value": text[cursor : m.start()]})
        tokens.append({
            "type": "field",
            "table": m.group(1),
            "column": m.group(2),
            "format": None,
            "format_spec": m.group(3),
        })
        cursor = m.end()
    if cursor == 0:
        m_simple = _TOKEN_SIMPLE_PAT.match(text.strip())
        if m_simple is not None:
            inner = m_simple.group(1)
            if inner in _RESERVED_FUNCTION_NAMES:
                tokens.append({"type": "function", "name": inner, "args": [], "format": None})
            elif inner == "None":
                tokens.append({"type": "literal", "value": ""})
            else:
                tokens.append({
                    "type": "field",
                    "table": None,
                    "column": inner,
                    "format": None,
                    "format_spec": None,
                })
            return tokens
    if cursor < len(text):
        tokens.append({"type": "literal", "value": text[cursor:]})
    if not tokens:
        tokens.append({"type": "literal", "value": text})
    return tokens


def _post_process(ir: IR) -> None:
    """Page/Band 의 size/height 를 객체 max y/h 로 추정 보정.

    비현실 좌표 (≥ 600mm) 는 PoC 단계 한계로 제외하고, 페이지 기본 사이즈
    (라벨 100×148mm) 를 유지한다.
    """
    PLAUSIBLE_LIMIT_MM = 600.0
    for page in ir.pages:
        max_y = 0.0
        for band in page["bands"]:
            band_max = 0.0
            for obj in band["objects"]:
                bottom = obj["rect_mm"]["y"] + obj["rect_mm"]["h"]
                if 0.0 < bottom <= PLAUSIBLE_LIMIT_MM and bottom > band_max:
                    band_max = bottom
            band["height_mm"] = round(band_max, 4)
            if band_max > max_y:
                max_y = band_max
        if 0.0 < max_y <= PLAUSIBLE_LIMIT_MM and max_y > page["size_mm"]["height"]:
            page["size_mm"]["height"] = round(max_y + 8.0, 4)


def _ir_to_dict(ir: IR) -> dict:
    return {
        "schema_version": ir.schema_version,
        "source": ir.source,
        "report": ir.report,
        "pages": ir.pages,
        "data_sources": ir.data_sources,
        "expressions_dictionary": ir.expressions_dictionary,
        "variant_profile": ir.variant_profile,
        "unsupported_objects": ir.unsupported_objects,
        "decoder_warnings": ir.decoder_warnings,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FRF → Canonical IR (PoC v0)")
    parser.add_argument("input", help=".frf file path")
    parser.add_argument("--out", help="IR JSON output path (default: stdout)", default=None)
    args = parser.parse_args(argv)

    ir = decode_frf(args.input)
    payload = json.dumps(ir, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"[frf_decoder] wrote IR → {args.out}")
    else:
        sys.stdout.write(payload)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
