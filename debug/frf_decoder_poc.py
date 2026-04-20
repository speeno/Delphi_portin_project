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
# v0.5.0 (2026-04-20)
#   + Memo 속성 블록 디코드: FrameTyp(byte@2), FrameWidth(i32@4),
#     FrameColor(i32@8), FillColor(i32@14) — debug/frf_property_probe.py
#     1,629 sample 통계로 오프셋 검증.
#   + Delphi TColor (0x00BBGGRR + flag) → '#RRGGBB' / 투명 / 시스템색 분류
#     (_decode_tcolor).
#   + IR.object.border / fill / style.color 를 추출값으로 채움 (실패-허용
#     fallback 은 종전 기본값 유지).
#
# v0.5.1 (2026-04-20) — Phase 0 회귀 봉합
#   ! v0.5.0 의 ``FillColor=i32@base+14`` 가 일부 양식(계산서, Report_4_96 등)
#     에서 *clWhite (0x00FFFFFF)* 를 잘못 잡아 1,744건 중 다수 셀에
#     ``fill={'color':'#FFFFFF','transparent':False}`` 가 박혔다.
#     컴파일러가 이를 ``background:#FFFFFF`` 로 inline 하면서 배경 라인/표가
#     가려져 시각상 *v0.4.x 이전* 형태로 회귀.
#   * 보수적 룰 추가 (Phase A 정밀 offset 결정 전 임시):
#       - fill_color_hex == '#FFFFFF' → fill_transparent=True 로 폴백.
#         (사유: FreeReport 기본 FillColor 는 clNone(0x1FFFFFFF) 이며 명시적
#          clWhite 는 운영 양식에서 사실상 0%; v0.4.x 에서도 transparent 였음.)
#
# v0.6.0 (2026-04-20) — Font/Adjust 디코드 + Phase A probe 데이터 정합
#   Phase A: ``debug/frf_property_probe.py`` 가 553 파일·41,490 windows 스캔.
#   결과 (debug/output/frf_property_probe.{md,json}):
#     - FillColor 정확 위치: base+14 (clNone hits=29,641, 압도적)
#     - FrameColor 정확 위치: base+8 (4-byte aligned, hits=33,498)
#     - Font.Name *기본* 위치: base+46 (length WORD), 내용 base+48~. 본문이 빈
#       Memo 의 경우 고정 offset; 본문이 있으면 Font block 이 (text_length+N)
#       만큼 뒤로 밀린다 → *동적 스캔* 으로 회수.
#     - Font.Size 위치: Font.Name 종료 직후 (probe 최빈 = base+55, "Arial" 의
#       경우)
#     - Font.Color 위치: Font.Size 직후 i32 (4 byte)
#   v0.6.0 의 추가 사항:
#     + ``try_extract_font_block_after`` 헬퍼 신설 — 동적 스캔으로 Font.Name/
#       Size/Color/Style/Charset 회수.
#     + ``try_extract_memo_props_after`` 가 위 헬퍼 결과를 부착해 반환.
#     + IR.style.font_family/font_size_pt/font_weight/font_italic/color 를
#       추출값으로 채움; 추정 fallback 은 v0.5.1 때와 동일 보존 (LSP).
#     + 한글 코드페이지 (CP949) 폰트 이름 ('굴림', '바탕', '돋움', '궁서')
#       사전 매핑 테이블.
#   운영 참고 (``계산서.frf``):
#     - 동일 셀 (예: ``Memo204_1`` / ``Memo204_2``) 이 밴드(_1=공급자, _2=공급받는자)
#       마다 *가로 폭 raw px* 가 다르게 저장될 수 있다 (예: 112px vs 132px). 이는
#       소스 FRF 제작 시 세로 2단 복사 본이 *서로 다른 격자* 가 박힌 것이지
#       디코더 rect 오탐이 아니다. 맞춤이 필요하면 IR 후처리/에디터로 별도 정합.
DECODER_VERSION = "0.6.0"

# ---------------------------------------------------------------------------
# 좌표 단위 — 데이터 기반 결정 (debug/frf_unit_probe.py, 2026-04-20)
#
# 진단 결과 7 종 양식 (Report_1_11/_21/_22/_61/_71, Report_2_12, 계산서.frf)
# 모두에서 px_96 (96 DPI 픽셀) 단위가 paper_match_score 1 위. bbox 가 ISO 표준
# 양식 (Receipt 182×128, A5 portrait/landscape, B5 portrait) 와 정확히 일치.
#
#   - twips (1440/inch) → bbox 7~17mm  ❌ (페이지 1cm 띠에 모든 객체 뭉침)
#   - px_96 (96/inch)   → bbox 150~200mm ✅ (실제 양식 크기)
#   - mm_100 (1/100mm)  → bbox 6~10mm  ❌
#   - mm_10  (1/10mm)   → bbox 50~100mm (영수증 양식에는 맞으나 A5/B5 미달)
#
# 결론: FastReport VCL 4.x ANSI 한국어 양식의 좌표 단위는 **96 DPI 픽셀**.
#       1 mm = 96 / 25.4 ≈ 3.7795 px.
# ---------------------------------------------------------------------------
UNITS_PER_MM = 96.0 / 25.4

# v0.2 호환 별칭 — rect_raw_twips 키는 *raw int32* 이므로 의미는 그대로.
TWIPS_PER_MM = UNITS_PER_MM


def units_to_mm(units: int) -> float:
    """raw int32 좌표 → mm 환산 (단위는 96 DPI 픽셀, frf_unit_probe.py 결정)."""
    return round(units / UNITS_PER_MM, 4)


# v0.2 호환 별칭 — 외부 import 호출자 보호 (테스트/진단 스크립트).
twips_to_mm = units_to_mm


# 좌표 plausibility 한도 (px_96 기준 합리 범위 — 단일 정의).
# X/W 는 가장 넓은 양식 (A4 landscape 297mm + 여유) 까지, Y/H 는 다중 페이지 보고서
# 가능성 (장표 1m+) 까지 허용하되 outlier 거부 위해 v0.2 보다 좁힘.
_RECT_X_RANGE_MM = (-20.0, 320.0)
_RECT_Y_RANGE_MM = (-20.0, 1200.0)
_RECT_W_RANGE_MM = (0.1, 320.0)
_RECT_H_RANGE_MM = (0.1, 1200.0)


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


def _is_printable_ascii_or_korean(data: bytes) -> bool:
    """문자열 후보가 ASCII printable 또는 CP949(EUC-KR) 한글 / 공백/탭/CR/LF 만으로 구성되는지.

    FastReport VCL 4.x 한국어 양식은 binding 텍스트가 ANSI(CP949) 로 저장된다. 본 검증은
    (a) ASCII printable + 공백/탭/CR/LF, 또는 (b) lead byte 0x81-0xFE + trail byte
    0x40-0x7E/0x80-0xFE 의 2 바이트 시퀀스 — KS_C_5601 EUC-KR 더블바이트 — 를 허용한다.
    """
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        if 0x20 <= b < 0x7F or b in (0x09, 0x0D, 0x0A):
            i += 1
            continue
        if 0x81 <= b <= 0xFE and i + 1 < n:
            b2 = data[i + 1]
            if 0x40 <= b2 <= 0x7E or 0x80 <= b2 <= 0xFE:
                i += 2
                continue
        return False
    return True


def _decode_pascal_string(data: bytes) -> str | None:
    """ASCII 우선, 실패 시 CP949 로 디코딩 시도. 마지막 폴백은 latin-1 (lossless byte→char)."""
    try:
        return data.decode("ascii")
    except UnicodeDecodeError:
        pass
    try:
        return data.decode("cp949")
    except (UnicodeDecodeError, LookupError):
        pass
    return data.decode("latin-1", errors="replace")


def scan_word_strings(buf: bytes, min_len: int = 3, max_len: int = 128) -> list[StringHit]:
    """버퍼 전역에서 WORD-prefixed string 후보를 *모두* 수집한다.

    ASCII printable + CP949 한글 modeller 까지 허용 (FastReport VCL 4.x 한국어 양식).
    """
    hits: list[StringHit] = []
    i = 0
    n = len(buf)
    while i + 2 <= n:
        ln = buf[i] | (buf[i + 1] << 8)
        if min_len <= ln <= max_len and i + 2 + ln <= n:
            data = buf[i + 2 : i + 2 + ln]
            if _is_printable_ascii_or_korean(data):
                txt = _decode_pascal_string(data)
                if txt is not None:
                    hits.append(StringHit(offset=i, text=txt))
                    i += 2 + ln
                    continue
        i += 1
    return hits


# ---------------------------------------------------------------------------
# Object type guesser
# ---------------------------------------------------------------------------


# Object name 패턴 — 변형 suffix (`Memo10_1`, `Memo107_2`) / 대소문자 / FreeReport 클래스명
# (`TfrMemoView`) 까지 모두 일반화 (사용자 규칙: 케이스가 아닌 일반화).
_PAGE_PAT = re.compile(r"^Page\d+(?:[_-]\d+)?$")
_BAND_PAT = re.compile(r"^Band\d+(?:[_-]\d+)?$")
_MEMO_PAT = re.compile(r"^Memo\d+(?:[_-]\d+)?$|^Text\d+(?:[_-]\d+)?$")
_PIC_PAT = re.compile(r"^(?:Picture|Pic|Image|Img)\d+(?:[_-]\d+)?$")
_LINE_PAT = re.compile(r"^Line\d+(?:[_-]\d+)?$")
_RECT_PAT = re.compile(r"^(?:Rect|Shape)\d+(?:[_-]\d+)?$")
_BARCODE_PAT = re.compile(r"^(?:Barcode|BarCode|BC)\d+(?:[_-]\d+)?$")
_SUBREPORT_PAT = re.compile(r"^(?:SubReport|Subreport|Sub)\d+(?:[_-]\d+)?$")
# 데이터 토큰 — 한글/공백/포맷 spec 포함 가능
_DATA_TOKEN_PAT = re.compile(r"^\[[^\[\]]+\]")
# FreeReport 직렬화 클래스명 (`TfrMemoView`, `TfrLineView` 등) — 객체 *유형 마커*
_FR_CLASS_PAT = re.compile(r"^Tfr(Memo|Text|Line|Rect|Shape|Picture|Bar[Cc]ode|SubReport)View$")


# 메타 노이즈 — binding literal 후보에서 제외할 알려진 ASCII 키워드들.
_META_NOISE_WORDS = {
    "Form", "TFont", "Color", "Charset", "Style", "Height", "Width",
    "DEFAULT_CHARSET", "HANGEUL_CHARSET", "Times New Roman",
    "MasterData", "PageHeader", "PageFooter", "ReportTitle", "ReportSummary",
    "ColumnHeader", "ColumnFooter", "MasterHeader", "MasterFooter",
    "Child", "Overlay", "GroupHeader", "GroupFooter",
}

_KNOWN_FONT_NAMES = {
    "굴림", "굴림체", "돋움", "돋움체", "바탕", "바탕체", "궁서", "궁서체",
    "맑은 고딕", "Malgun Gothic", "Arial", "Tahoma", "Verdana", "Times New Roman",
}
_META_LITERAL_PAT = re.compile(
    r"(?:^|[\s:._-])(Font|TitleFont|Charset|DEFAULT_CHARSET|HANGEUL_CHARSET|Style|Color)(?:$|[\s:._-])",
    re.I,
)


def _has_korean(text: str) -> bool:
    return any("\uAC00" <= c <= "\uD7A3" or "\u3130" <= c <= "\u318F" for c in text)


def _sanitize_literal_text(text: str) -> str | None:
    """한글 literal 후보에서 폰트/메타 노이즈를 제거한다.

    예:
      - `출판사명굴림` -> `출판사명`
      - `입 고 일:굴림` -> `입 고 일:`
      - `굴림` / `HANGEUL_CHARSET` / `TitleFont` -> None
    """
    s = text.strip()
    if not s:
        return None
    if s in _META_NOISE_WORDS or s in _KNOWN_FONT_NAMES:
        return None
    if _META_LITERAL_PAT.search(s):
        return None
    # 알려진 폰트명이 앞/뒤에 붙는 경우 반복 제거.
    changed = True
    while changed and s:
        changed = False
        for name in sorted(_KNOWN_FONT_NAMES, key=len, reverse=True):
            if s.startswith(name):
                s = s[len(name):].lstrip(" :._-/")
                changed = True
            if s.endswith(name):
                s = s[:-len(name)].rstrip(" ._-/")
                changed = True
    s = s.strip()
    if not s:
        return None
    if s in _KNOWN_FONT_NAMES or s in _META_NOISE_WORDS:
        return None
    # 메타 성 문자열만 남은 경우도 제거.
    if _META_LITERAL_PAT.search(s):
        return None
    return s


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
    if _SUBREPORT_PAT.match(text):
        return "subreport_obj"
    if _DATA_TOKEN_PAT.match(text):
        return "data_token"
    if _FR_CLASS_PAT.match(text):
        return "class_marker"
    # 한글 포함 일반 텍스트 → 라벨 literal 후보 (메타 노이즈 제외).
    if _has_korean(text) and text not in _META_NOISE_WORDS:
        return "literal_text"
    return None


# ---------------------------------------------------------------------------
# Coordinate extractor — try to read 4 little-endian int32 right after a
# scanned object name; treat as (Left, Top, Width, Height) in TWIPs.
# ---------------------------------------------------------------------------


def _is_plausible_rect(rect: dict) -> bool:
    """rect_mm 4 값이 *현실적* 범위 (단일 한도 정의) 안에 들어오는지 검증."""
    x, y, w, h = rect["x_mm"], rect["y_mm"], rect["w_mm"], rect["h_mm"]
    if not (_RECT_X_RANGE_MM[0] <= x <= _RECT_X_RANGE_MM[1]):
        return False
    if not (_RECT_Y_RANGE_MM[0] <= y <= _RECT_Y_RANGE_MM[1]):
        return False
    if not (_RECT_W_RANGE_MM[0] <= w <= _RECT_W_RANGE_MM[1]):
        return False
    if not (_RECT_H_RANGE_MM[0] <= h <= _RECT_H_RANGE_MM[1]):
        return False
    return True


def _rect_score(rect: dict) -> float:
    """rect 후보의 "선호 점수" (작을수록 우수). 동률일 때 첫 매치 우선.

    px_96 단위 결정 후 양식 좌표 분포는 0~300mm 가 일반적 (라벨/영수증/A5/B5).
    너무 작거나 너무 큰 좌표·치수는 감점한다.
    """
    x, y, w, h = rect["x_mm"], rect["y_mm"], rect["w_mm"], rect["h_mm"]
    score = 0.0
    if w < 1.0 or h < 1.0:
        score += 5.0
    if w > 250.0 or h > 600.0:
        score += 3.0
    if x < 0 or y < 0:
        score += 1.0
    # 페이지 안쪽 좌표 (≤300mm) 가산 — 동일 객체에서 안쪽 후보를 우선시.
    if x > 320 or y > 1200:
        score += 4.0
    return score


def try_extract_rect_after(
    buf: bytes,
    after_offset: int,
    search_window: int = 32,
    skip_min: int = 0,
) -> dict | None:
    """객체 이름 직후의 가까운 위치에서 (Left,Top,Width,Height) TWIPs 추출 시도.

    FreeReport 직렬화 규칙: 객체명 직후 *3 바이트 헤더* (`00 02 00`) → 4×LE int32 좌표.
    본 함수는 `skip_min..search_window` 모든 위치에서 4 i32 를 시도해 plausibility 검증을
    통과한 후보 중 점수가 가장 좋은 것을 반환한다 (best-fit). 단, 동률일 때는 가장
    이른 위치 (skip 작은 쪽) 가 우선 — 직렬화 규칙에 더 가까움.
    """
    n = len(buf)
    candidates: list[tuple[float, int, dict]] = []
    for skip in range(skip_min, search_window):
        base = after_offset + skip
        if base + 16 > n:
            break
        try:
            l, t, w, h = struct.unpack_from("<iiii", buf, base)
        except struct.error:
            continue
        rect = {
            "x_mm": units_to_mm(l),
            "y_mm": units_to_mm(t),
            "w_mm": units_to_mm(w),
            "h_mm": units_to_mm(h),
            # v0.2 호환: 키는 raw_twips 유지하지만 실제 단위는 px@96DPI raw int.
            "raw_twips": {"left": l, "top": t, "width": w, "height": h},
            "offset": base,
        }
        if not _is_plausible_rect(rect):
            continue
        candidates.append((_rect_score(rect), skip, rect))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1]))
    return candidates[0][2]


# ---------------------------------------------------------------------------
# Memo 속성 블록 (Frame/Fill) 추출 — v0.5.0
#
# debug/frf_property_probe.py 가 1,629 Memo 샘플로 검증한 byte 레이아웃:
#
#     0-1   WORD   Stretched/Adjust 비트 (현재 미사용)
#     2     u8    FrameTyp (1=Left, 2=Top, 4=Right, 8=Bottom; 0x0F=all)
#     3     u8    reserved/padding
#     4-7   i32   FrameWidth (px@96DPI; 통상 1 또는 2)
#     8-11  i32   FrameColor (Delphi TColor)
#     12-13 WORD  ShadowSize (현재 미사용)
#     14-17 i32   FillColor  (Delphi TColor)
#     18+   variable  Adjust/Font/Memo content (본 PoC 미해석)
#
# 본 함수는 *위 18 byte 만* 해석한다. 실패 시 None 반환 (호출측에서 IR 기본값
# 유지). FrameTyp 가 합법 비트마스크 (0x00..0x0F) 가 아니거나 FrameWidth 가
# 0..16 범위를 벗어나면 디코드 거부.
# ---------------------------------------------------------------------------


# Delphi TColor 분류 — frame/fill 양쪽 공용.
#   - direct: 0x00000000..0x00FFFFFF 사이 (high byte == 0)
#   - clNone: 0x1FFFFFFF (특수 transparent 마커)
#   - system: high byte == 0xFF (clBtnFace 등)
#   - 그 외 (e.g. 0xFFFFnnnn 음수 i32) → 시스템색으로 간주
def _decode_tcolor(value: int | None) -> tuple[str | None, bool]:
    """Delphi TColor → (#RRGGBB, transparent_flag).

    Returns
    -------
    (hex, transparent)
        - hex: ``"#RRGGBB"`` 또는 ``None`` (시스템색/clNone 등 상수 → 호출측 기본값).
        - transparent: ``True`` 면 fill 이 그려지지 않음 (clNone).
    """
    if value is None:
        return None, False
    v = value & 0xFFFFFFFF
    if v == 0x1FFFFFFF:
        return None, True
    high = (v >> 24) & 0xFF
    if high != 0:
        # 시스템색 (0xFFnnnnnn) 또는 미지정 — 호출측이 기본값 유지하도록 None.
        return None, False
    rr = v & 0xFF
    gg = (v >> 8) & 0xFF
    bb = (v >> 16) & 0xFF
    return f"#{rr:02X}{gg:02X}{bb:02X}", False


# FreeReport TfrFrameBorder bit 정의 (frtypes.pas).
_FRAME_BIT_LEFT = 0x01
_FRAME_BIT_TOP = 0x02
_FRAME_BIT_RIGHT = 0x04
_FRAME_BIT_BOTTOM = 0x08
_FRAME_BITS_ALL = 0x0F


def try_extract_memo_props_after(buf: bytes, rect_offset: int) -> dict | None:
    """rect 16 byte 직후의 Frame/Fill 속성 블록을 디코드.

    Parameters
    ----------
    buf : 바이너리 전체.
    rect_offset : rect (4×i32) 의 *시작* 오프셋. 본 함수는 ``rect_offset+16`` 부터
        18 byte 를 읽는다.

    Returns
    -------
    dict | None
        ``{ "frame_typ": int, "frame_width_px": int, "frame_color": int|None,
            "fill_color": int|None, "frame_color_hex": str|None,
            "fill_color_hex": str|None, "fill_transparent": bool }``
        또는 None (오프셋 부족/속성 비합법).
    """
    base = rect_offset + 16
    if base + 18 > len(buf):
        return None
    try:
        frame_typ = buf[base + 2]
        frame_width = struct.unpack_from("<i", buf, base + 4)[0]
        frame_color = struct.unpack_from("<i", buf, base + 8)[0]
        fill_color = struct.unpack_from("<i", buf, base + 14)[0]
    except struct.error:
        return None
    if not (0 <= frame_typ <= _FRAME_BITS_ALL):
        return None
    if not (0 <= frame_width <= 16):
        return None
    fc_hex, _fc_trans = _decode_tcolor(frame_color)
    fill_hex, fill_trans = _decode_tcolor(fill_color)
    # v0.5.1 Phase 0 — clWhite 회귀 봉합:
    # 본 PoC 의 base+14 offset 은 일부 양식에서 ShadowColor/FillStyle 영역을
    # 잘못 잡아 *항상* 0x00FFFFFF 가 회수된다. FreeReport 기본 FillColor 는
    # clNone 이고 명시적 clWhite 는 운영 양식에서 0% 에 가깝기 때문에,
    # *clWhite 회수* 는 회귀로 간주하고 transparent 로 폴백한다.
    # (Phase A probe 결과 base+14 = clNone 이 29,641 hits 로 압도적 = 정합 위치
    #  확인 OK. v0.6.0 도 동일 offset 유지.)
    if fill_hex == "#FFFFFF" and not fill_trans:
        fill_hex = None
        fill_trans = True
    # v0.6.0 — Adjust(halign/valign) byte (base+18) 추출.
    halign, valign = try_extract_adjust(buf, base)
    # v0.6.0 — Font 블록 동적 스캔 (base+22..base+128).
    font_block = try_extract_font_block_after(buf, base, scan_window=128)
    return {
        "frame_typ": frame_typ,
        "frame_width_px": frame_width,
        "frame_color": frame_color & 0xFFFFFFFF,
        "fill_color": fill_color & 0xFFFFFFFF,
        "frame_color_hex": fc_hex,
        "fill_color_hex": fill_hex,
        "fill_transparent": fill_trans,
        "halign": halign,
        "valign": valign,
        "font": font_block,  # None 가능 — 호출측 fallback.
    }


def _frame_typ_to_sides(frame_typ: int) -> dict:
    """FrameTyp 비트마스크 → IR border 4-측면 boolean."""
    return {
        "left": bool(frame_typ & _FRAME_BIT_LEFT),
        "top": bool(frame_typ & _FRAME_BIT_TOP),
        "right": bool(frame_typ & _FRAME_BIT_RIGHT),
        "bottom": bool(frame_typ & _FRAME_BIT_BOTTOM),
    }


# ---------------------------------------------------------------------------
# v0.6.0 — Font 블록 디코드
# ---------------------------------------------------------------------------
#
# Phase A probe 데이터로 결정한 정합 byte 레이아웃 (Memo 객체 base 기준):
#
#   base+44.+45  WORD     padding (보통 00 00) — Font 블록 직전
#   base+46.+47  WORD     Font.Name length n (1..32)
#   base+48..   bytes(n) Font.Name (ASCII or CP949)
#   base+48+n   byte     null terminator (ASCII strings 만; 항상 존재 X)
#   base+48+n+? i32      Font.Size (positive pt, 6..72)
#   직후         i32      Font.Color (Delphi TColor)
#   직후         WORD     Font.Charset (0=ANSI, 129=Hangeul, 134=Chinese)
#   직후         byte     Font.Style 비트마스크 (0x01=Bold, 0x02=Italic,
#                          0x04=Underline, 0x08=StrikeOut)
#
# *Memo 본문* 이 Font 블록 *이전* 에 변길이로 등장하는 양식이 있으므로 (예:
# Memo216_2 "상호" 의 경우 Font 블록이 base+~74 로 밀림), 본 함수는 base+22
# 부터 base+128 사이 *동적 스캔* 을 수행한다.
# ---------------------------------------------------------------------------

# CP949 한글 폰트 (raw bytes → Unicode 정규화).
_CP949_FONT_MAP = {
    b"\xb1\xbc\xb8\xb2": "굴림",
    b"\xb9\xcc\xc5\xc1": "바탕",
    b"\xb5\xcb\xbf\xf2": "돋움",
    b"\xb1\xc3\xbc\xad": "궁서",
}

# 운영에서 빈번한 ASCII 폰트 (문자열 검증 화이트리스트).
_KNOWN_ASCII_FONTS = {
    b"Arial",
    b"MS Sans Serif",
    b"Times New Roman",
    b"Courier New",
    b"Tahoma",
    b"Helvetica",
    b"Verdana",
    b"Wingdings",
    b"Symbol",
}

# Font.Style 비트 (TFontStyle bit set).
_FONT_STYLE_BOLD = 0x01
_FONT_STYLE_ITALIC = 0x02
_FONT_STYLE_UNDERLINE = 0x04
_FONT_STYLE_STRIKEOUT = 0x08
_FONT_STYLE_VALID_MASK = 0x0F


def _decode_font_name_bytes(raw_name: bytes) -> tuple[str, str] | None:
    """raw bytes → (font_family, decoded_name).

    family 는 한글 이름이면 그대로 ('굴림' 등), ASCII 면 그대로.
    decoded_name 은 IR 직렬화용 (사람이 읽을 수 있는 형태).
    실패 시 None.
    """
    if raw_name in _CP949_FONT_MAP:
        name = _CP949_FONT_MAP[raw_name]
        return name, name
    if raw_name in _KNOWN_ASCII_FONTS:
        s = raw_name.decode("ascii")
        return s, s
    # 일반 ASCII (화이트리스트 외) — 1..32 길이의 순수 ASCII 만 허용.
    if all(0x20 <= b < 0x7F for b in raw_name) and 1 <= len(raw_name) <= 32:
        s = raw_name.decode("ascii")
        return s, s
    # CP949 임의 한글 (B0..C8 / A1..FE 더블바이트 시퀀스) — 보수적으로 허용.
    try:
        s = raw_name.decode("cp949")
        if 1 <= len(s) <= 16 and all(c.isprintable() for c in s):
            return s, s
    except UnicodeDecodeError:
        pass
    return None


def try_extract_font_block_after(
    buf: bytes, base: int, *, scan_window: int = 128
) -> dict | None:
    """base+22 ~ base+scan_window 영역에서 Font 블록을 동적 스캔.

    Returns
    -------
    dict | None
        ``{ "font_name": str, "font_family": str, "font_size_pt": float|None,
            "font_color_hex": str|None, "font_color": int|None,
            "font_style_byte": int|None, "font_bold": bool, "font_italic": bool,
            "font_underline": bool, "font_strikeout": bool,
            "font_charset": int|None, "font_offset": int }`` 또는 None.
    """
    end = min(base + scan_window, len(buf))
    # base+22 부터 시작 (속성 블록 18 byte + 4 byte 패딩 보수적 회피).
    for off in range(base + 22, end - 6):
        n = struct.unpack_from("<H", buf, off)[0]
        if not (1 <= n <= 32):
            continue
        name_start = off + 2
        name_end = name_start + n
        if name_end > end:
            continue
        raw_name = buf[name_start:name_end]
        decoded = _decode_font_name_bytes(raw_name)
        if decoded is None:
            continue
        font_family, font_name = decoded
        # Font.Name 다음에 ``\x00`` terminator 가 1 byte 더 있는 양식이 있다.
        # i32 정합을 위해 +1 전후 모두 시도.
        for term_pad in (0, 1):
            size_off = name_end + term_pad
            # Font.Size i32 (4) + Font.Color i32 (4) = 최소 8 byte 필요.
            if size_off + 8 > end:
                continue
            try:
                font_size = struct.unpack_from("<i", buf, size_off)[0]
                font_color_int = struct.unpack_from("<i", buf, size_off + 4)[0]
            except struct.error:
                continue
            # Font.Size 합리 범위 검증 (positive pt 6..72, or negative px -200..-6).
            if not (6 <= font_size <= 72 or -200 <= font_size <= -6):
                continue
            font_size_pt: float | None
            if font_size > 0:
                font_size_pt = float(font_size)
            else:
                # Delphi negative-px height: -px → pt = px * 72 / 96.
                font_size_pt = abs(font_size) * 0.75
            color_hex, _color_trans = _decode_tcolor(font_color_int)
            # Style/Charset — 다음 6 byte 안에서 합법 비트마스크 조회.
            style_byte = 0
            charset = None
            for so in range(size_off + 8, min(size_off + 18, end)):
                b = buf[so]
                if 0 <= b <= _FONT_STYLE_VALID_MASK:
                    # 0 도 합법 (no style) — 스캔 우선순위는 가장 가까운 byte.
                    style_byte = b
                    break
            # Charset 탐색 — 보통 0 (ANSI) / 129 (Hangeul) / 134 (Chinese)
            for so in range(size_off + 8, min(size_off + 16, end)):
                b = buf[so]
                if b in (0, 1, 128, 129, 134, 136, 161, 162, 178):
                    charset = b
                    break
            return {
                "font_name": font_name,
                "font_family": font_family,
                "font_size_pt": font_size_pt,
                "font_color": font_color_int & 0xFFFFFFFF,
                "font_color_hex": color_hex,
                "font_style_byte": style_byte,
                "font_bold": bool(style_byte & _FONT_STYLE_BOLD),
                "font_italic": bool(style_byte & _FONT_STYLE_ITALIC),
                "font_underline": bool(style_byte & _FONT_STYLE_UNDERLINE),
                "font_strikeout": bool(style_byte & _FONT_STYLE_STRIKEOUT),
                "font_charset": charset,
                "font_offset": off,
            }
    return None


# Adjust(halign/valign) 비트 (TfrAlignment bit-encoded byte at base+18 or base+19).
# FastReport VCL 4.x: low nibble = HAlign (0=Left,1=Right,2=Center), high nibble
# = VAlign (0=Top,1=Bottom,2=Center). Phase A probe 결과 base+18 의 byte 가
# 0x00..0x22 분포를 보임 (실측 제공: Memo107_2 base+18 = 0x2C 인 양식도 존재
# → 0x2C = 0b0010_1100 은 high=2(VCenter), low=0xC(invalid) → fallback default).
_HALIGN_MAP = {0: "left", 1: "right", 2: "center", 3: "justify"}
_VALIGN_MAP = {0: "top", 1: "bottom", 2: "center"}


def try_extract_adjust(buf: bytes, base: int) -> tuple[str | None, str | None]:
    """Adjust byte → (halign, valign) 또는 (None, None) (실패-허용)."""
    if base + 19 > len(buf):
        return None, None
    b = buf[base + 18]
    halign = _HALIGN_MAP.get(b & 0x0F)
    valign = _VALIGN_MAP.get((b >> 4) & 0x0F)
    return halign, valign


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

        if kind == "class_marker":
            # FreeReport 직렬화 클래스명 마커는 *부모 객체의 type 힌트* — 직전 객체에 적용.
            if last_object is not None:
                tname = hit.text  # e.g. "TfrMemoView"
                last_object.setdefault("unsupported_props", {})["fr_class_marker"] = tname
            continue

        if kind in (
            "text_obj",
            "picture_obj",
            "line_obj",
            "rect_obj",
            "barcode_obj",
            "subreport_obj",
        ):
            ir_type_map = {
                "text_obj": "Text",
                "picture_obj": "Picture",
                "line_obj": "Line",
                "rect_obj": "Rect",
                "barcode_obj": "Barcode",
                "subreport_obj": "SubReport",
            }
            rect = try_extract_rect_after(raw, end_offset, search_window=32)
            # v0.5.0 — rect 직후 18 byte Memo 속성 블록 (Frame/Fill) 디코드.
            # text_obj 외에도 line/rect/picture 등은 동일 base class 직렬화 규칙
            # (TfrView.LoadFromStream) 을 따르므로 frame/fill 추출은 모든 객체에서 시도.
            props = (
                try_extract_memo_props_after(raw, rect["offset"]) if rect else None
            )
            border_default = {
                "left": False,
                "top": False,
                "right": False,
                "bottom": False,
                "color": "#888888",
                "width_pt": 1.0,
                "style": "solid",
            }
            fill_default = {"color": "#FFFFFF", "transparent": True}
            style_default = {
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
            }
            if props is not None:
                sides = _frame_typ_to_sides(props["frame_typ"])
                # FreeReport FrameWidth 단위는 px@96DPI; 1 px ≈ 0.75 pt.
                width_pt = max(0.5, round(props["frame_width_px"] * 0.75, 2))
                fc_hex = props["frame_color_hex"] or border_default["color"]
                border_default = {
                    **sides,
                    "color": fc_hex,
                    "width_pt": width_pt,
                    "style": "solid",
                }
                if props["fill_transparent"]:
                    fill_default = {"color": "#FFFFFF", "transparent": True}
                elif props["fill_color_hex"] is not None:
                    fill_default = {
                        "color": props["fill_color_hex"],
                        "transparent": False,
                    }
                # v0.6.0 — Font 블록 디코드 결과 부착 (있으면 추정 fallback 대체).
                font_block = props.get("font")
                if font_block:
                    style_default = {
                        **style_default,
                        "font_family": font_block["font_family"],
                        "font_size_pt": font_block["font_size_pt"]
                        or style_default["font_size_pt"],
                        "font_weight": "bold" if font_block["font_bold"] else "normal",
                        "font_italic": font_block["font_italic"],
                        "font_underline": font_block["font_underline"],
                        "color": font_block["font_color_hex"]
                        or style_default["color"],
                        "_font_extracted": True,
                        "_font_charset": font_block["font_charset"],
                    }
                # v0.6.0 — Adjust(halign/valign) 추출.
                if props.get("halign"):
                    style_default = {**style_default, "halign": props["halign"]}
                if props.get("valign"):
                    style_default = {**style_default, "valign": props["valign"]}
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
                "border": border_default,
                "fill": fill_default,
                "style": style_default if kind == "text_obj" else {},
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
            if kind == "picture_obj":
                # v0.4.0 — 이미지 매칭(_extract_and_attach_images) 시 사용할 임시 오프셋.
                # IR 직렬화 직전에 _attach_pictures 가 obj 에 image 부여하고 _offset 키는
                # _ir_to_dict 단계에서 제거된다.
                obj["_decoder_offset"] = hit.offset
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
            continue

        if kind == "literal_text":
            # 한글 라벨 literal — 직전 Text 객체의 binding 이 비어있을 때만 채택 (보수적).
            sanitized = _sanitize_literal_text(hit.text)
            if (
                sanitized is not None
                and
                last_object is not None
                and last_object["type"] == "Text"
                and not (last_object.get("binding") or {}).get("raw")
            ):
                last_object["binding"] = {
                    "kind": "literal",
                    "value": sanitized,
                    "raw": sanitized,
                }

    _post_process(ir)
    # v0.4.0 — Picture 객체에 임베디드 이미지(JPG/PNG/BMP) 매칭 + base64 부여.
    img_summary = _extract_and_attach_images(ir, raw)
    if img_summary:
        ir.source["image_extraction"] = img_summary
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
# 단일 토큰 — ASCII 식별자 + 한글/숫자/언더스코어 모두 허용 (CP949 양식 호환).
_TOKEN_SIMPLE_PAT = re.compile(r"^\[([^\[\]\s\.]+)\]$")
# 인라인 단일 토큰 — `라벨 [Squt1] 단위` 처럼 literal 사이에 끼는 단일 식별자.
_TOKEN_INLINE_PAT = re.compile(r"\[([^\[\]\s\.]+)\]")
_RESERVED_FUNCTION_NAMES = {
    "PageN", "TotalPages", "Date", "Time", "DateTime", "Page",
    "Line", "Line#", "RowNo", "PageNum",
}


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
        # 단일 anchored 토큰이면 그대로 처리.
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
        # literal 사이에 끼는 인라인 [Token] 도 모두 잡아낸다 — `[Squt1] [Squt2]` 처럼
        # 단일 식별자가 표 셀에 그대로 흘러나오던 문제를 일반화해 해결한다.
        for m in _TOKEN_INLINE_PAT.finditer(text):
            if m.start() > cursor:
                tokens.append({"type": "literal", "value": text[cursor : m.start()]})
            inner = m.group(1)
            if inner in _RESERVED_FUNCTION_NAMES:
                tokens.append({"type": "function", "name": inner, "args": [], "format": None})
            elif inner == "None":
                pass
            else:
                tokens.append({
                    "type": "field",
                    "table": None,
                    "column": inner,
                    "format": None,
                    "format_spec": None,
                })
            cursor = m.end()
    if cursor < len(text):
        tokens.append({"type": "literal", "value": text[cursor:]})
    if not tokens:
        tokens.append({"type": "literal", "value": text})
    return tokens


# ---------------------------------------------------------------------------
# v0.4.0 — Picture 임베디드 이미지(JPG/PNG/BMP) 추출 + Picture 객체 매칭
# ---------------------------------------------------------------------------
#
# 데이터 기반 결정 (debug/frf_batch_convert_all.py 1,744 스캔 + Picture/이미지
# offset 차이 측정):
#
#   - 1,744 frf 중 215 (12.33%) 가 임베디드 이미지를 가짐
#   - JPG: 211, BMP: 6, PNG: 0
#   - Picture 객체 hit offset 다음 +82 byte 위치에 이미지 magic byte 가 일관되게
#     등장 (FastReport VCL 4.x 가 ObjectName 다음 *fixed-size header* 로 메타를
#     기록한 뒤 BLOB 시작). 그래서 매칭 휴리스틱은 단순:
#         "Picture 객체의 hit offset 보다 큰 첫 image magic"
#     매칭 거리 (Δ) 는 64~256 범위면 신뢰. 1024 초과면 매칭 실패로 간주.
#
# 이미지 종료 위치 결정:
#   - JPG: SOI(\xff\xd8) → 가장 마지막 EOI(\xff\xd9) 까지. 다음 magic/EOF 이전.
#   - BMP: 헤더 +2 offset 의 LE int32 = 파일 전체 길이.
#   - PNG: IEND chunk(``\x00\x00\x00\x00IEND\xaeB\x60\x82``) + chunk CRC(8 byte 포함).
# ---------------------------------------------------------------------------

_IMG_MAGICS = {
    "image/jpeg": b"\xff\xd8\xff",
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/bmp": b"BM",
}
# 매칭 거리(Picture 객체 → 이미지 매직) 합리 한도 — false positive 방지.
# v0.4.0: 1,024 사용 → 211 매칭. v0.4.1: 4,096 으로 완화 (Report_4_94 등 다중
# Picture/이미지가 분산된 양식의 매칭률 회복). Δ 가 4,096 초과면 매핑 거부.
_IMG_MATCH_MAX_DELTA = 4096
# BMP magic 은 너무 짧아 false positive 가 잦으므로 size 헤더 sanity 체크 범위.
_IMG_BMP_SIZE_RANGE = (100, 5_000_000)
_IMG_PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB\x60\x82"


def _scan_image_blobs(raw: bytes) -> list[dict]:
    """파일 전체에서 이미지 BLOB 후보를 (offset, end, format, data) 리스트로 반환.

    BLOB 들은 파일 내 등장 순서로 정렬돼 있고, *서로 겹치지 않는다*. (이전 BLOB 이
    가지는 [offset, end) 안에 들어오는 다음 magic 은 우연의 false positive 로 보고
    버린다 — 예: BMP 픽셀 데이터 안의 JPG SOI 패턴.)
    """
    candidates: list[dict] = []
    for fmt, magic in _IMG_MAGICS.items():
        pos = 0
        while True:
            i = raw.find(magic, pos)
            if i < 0:
                break
            end = _image_end(raw, i, fmt)
            if end is not None and end > i:
                candidates.append({"offset": i, "end": end, "format": fmt})
            # BMP/JPG magic 짧음 — 반복 검색 위해 +2 진행
            pos = i + max(2, len(magic))
    candidates.sort(key=lambda c: c["offset"])

    # 이전 BLOB 안에 끼는 후보 제거 (BMP/JPG 데이터 내부의 우연 magic).
    pruned: list[dict] = []
    cur_end = -1
    for c in candidates:
        if c["offset"] < cur_end:
            continue
        pruned.append(c)
        cur_end = c["end"]

    # 각 BLOB 의 실제 byte payload 부착.
    for c in pruned:
        c["data"] = raw[c["offset"]:c["end"]]
    return pruned


def _image_end(raw: bytes, start: int, fmt: str) -> int | None:
    """``start`` 부터 시작하는 이미지의 *exclusive end offset* 추정."""
    n = len(raw)
    if fmt == "image/bmp":
        if start + 14 > n:
            return None
        size = struct.unpack_from("<I", raw, start + 2)[0]
        if not (_IMG_BMP_SIZE_RANGE[0] < size < _IMG_BMP_SIZE_RANGE[1]):
            return None
        end = start + size
        return min(end, n)
    if fmt == "image/png":
        idx = raw.find(_IMG_PNG_IEND, start)
        if idx < 0:
            return None
        return idx + len(_IMG_PNG_IEND)
    if fmt == "image/jpeg":
        # SOI ~ 마지막 EOI(\xff\xd9). 진정한 JPG 는 segment 파싱이 정석이지만
        # 1,744 양식 휴리스틱: SOI 다음 *4096~파일 끝* 사이의 마지막 EOI 사용.
        # 다음 image magic (다른 SOI/IHDR/BM) 이전까지로 한도.
        next_boundary = n
        for other_magic in _IMG_MAGICS.values():
            j = raw.find(other_magic, start + 3)
            if 0 < j < next_boundary:
                next_boundary = j
        # 마지막 EOI 검색
        eoi = raw.rfind(b"\xff\xd9", start + 4, next_boundary + 2)
        if eoi < 0:
            return None
        return eoi + 2
    return None


def _extract_and_attach_images(ir: "IR", raw: bytes) -> dict | None:
    """Picture 객체에 임베디드 이미지 BLOB 매칭 + IR.Object.image 부여 (v0.4.0).

    매칭 규칙: Picture 객체의 hit offset 보다 큰 첫 image BLOB. 거리 Δ 가
    ``_IMG_MATCH_MAX_DELTA`` 이내일 때만 신뢰. 매칭 실패 Picture 는 image 필드를
    부여하지 않고 (컴파일러가 placeholder 박스로 fallback).

    Returns
    -------
    summary 또는 None — IR.source.image_extraction 으로 노출.
    """
    import base64
    import hashlib

    blobs = _scan_image_blobs(raw)
    matched = 0
    skipped_picture = 0
    used_blob_offsets: set[int] = set()
    pictures: list[dict] = []
    for page in ir.pages:
        for band in page.get("bands", []):
            for obj in band.get("objects", []):
                if obj.get("type") == "Picture":
                    pictures.append(obj)

    for pic in pictures:
        offset = pic.pop("_decoder_offset", None)
        if offset is None:
            skipped_picture += 1
            continue
        # Picture 다음 가장 가까운 미사용 BLOB
        candidate = None
        for b in blobs:
            if b["offset"] <= offset:
                continue
            if b["offset"] in used_blob_offsets:
                continue
            candidate = b
            break
        if candidate is None:
            skipped_picture += 1
            continue
        delta = candidate["offset"] - offset
        if delta > _IMG_MATCH_MAX_DELTA:
            skipped_picture += 1
            continue
        used_blob_offsets.add(candidate["offset"])
        data = candidate["data"]
        sha1 = hashlib.sha1(data).hexdigest()
        pic["image"] = {
            "format": candidate["format"],
            "size_bytes": len(data),
            "sha1": sha1,
            "data_b64": base64.b64encode(data).decode("ascii"),
            "decoder_match_delta": delta,
        }
        matched += 1

    # Picture 객체 없이 발견된 BLOB 도 진단으로 노출 (Report_2_11 케이스 등).
    unmatched_blobs = [
        {"offset": b["offset"], "format": b["format"], "size_bytes": b["end"] - b["offset"]}
        for b in blobs if b["offset"] not in used_blob_offsets
    ]
    if not pictures and not blobs:
        return None
    return {
        "image_blobs_total": len(blobs),
        "pictures_total": len(pictures),
        "pictures_matched": matched,
        "pictures_unmatched": skipped_picture,
        "blobs_unmatched": unmatched_blobs[:10],
    }


def _post_process(ir: IR) -> None:
    """Page/Band 의 size/height 를 객체 bbox union 으로 추정 보정 (v0.3).

    v0.2 에서는 *Y-축 max 만* 페이지 높이로 보정했으나, 좌표 단위 교정 (px_96)
    이후에는 X-축 max 도 페이지 폭 보정에 활용해 SVG/HTML viewBox 가 실제
    양식 크기에 맞춰진다. 비현실 좌표 (PLAUSIBLE_LIMIT_MM 초과) 는 계속 제외.

    페이지 폭 후보 (PageW) 는 다음 우선순위로 결정한다:
      1. 객체 bbox union 의 right (max_x) + 작은 margin (8mm)
      2. 디코더 기본 (라벨 100mm)
    페이지 높이 (PageH) 도 동일.
    """
    PLAUSIBLE_LIMIT_MM = 1200.0
    for page in ir.pages:
        max_x = 0.0
        max_y = 0.0
        for band in page["bands"]:
            band_max_y = 0.0
            for obj in band["objects"]:
                rect = obj["rect_mm"]
                right = rect["x"] + rect["w"]
                bottom = rect["y"] + rect["h"]
                if 0.0 < right <= PLAUSIBLE_LIMIT_MM and right > max_x:
                    max_x = right
                if 0.0 < bottom <= PLAUSIBLE_LIMIT_MM:
                    if bottom > band_max_y:
                        band_max_y = bottom
                    if bottom > max_y:
                        max_y = bottom
            band["height_mm"] = round(band_max_y, 4)
        if 0.0 < max_x <= PLAUSIBLE_LIMIT_MM and max_x > page["size_mm"]["width"]:
            page["size_mm"]["width"] = round(max_x + 8.0, 4)
        if 0.0 < max_y <= PLAUSIBLE_LIMIT_MM and max_y > page["size_mm"]["height"]:
            page["size_mm"]["height"] = round(max_y + 8.0, 4)
    _infer_text_font_sizes(ir)


def _infer_text_font_sizes(ir: IR) -> None:
    """Text 객체의 font_size_pt 를 rect 크기 기반으로 추정 보정 (v0.3.2).

    v0.3.1 까지는 *높이만* 기준으로 추정해 셀이 *세로로 길쭉할 때* (예: w=5mm, h=30mm)
    폰트가 16pt 까지 부풀어, 한 줄에 1글자만 들어가 세로로 쌓이는 현상이 나타났다.
    v0.3.2 부터는:

      1. 가로 텍스트로 가정해 line-height ≈ 1.2 → ``font_mm = h / 1.2`` 로 시작하고,
      2. ``w < h`` 인 셀은 폭으로도 추가 캡 (≈ 1자가 들어가는 폭) 을 적용해 폰트가
         셀 폭을 넘어 세로 1글자 wrap 으로 떨어지는 현상을 차단하며,
      3. 라벨 폼에서 일반적으로 쓰는 범위 (``6 ~ 12pt``) 로 클램프해 인접 셀과
         겹치지 않도록 상한을 한 단계 더 낮췄다.
    """
    MM_PER_PT = 25.4 / 72.0
    for page in ir.pages:
        for band in page["bands"]:
            for obj in band["objects"]:
                if obj.get("type") != "Text":
                    continue
                style = obj.get("style") or {}
                rect = obj.get("rect_mm") or {}
                w_mm = float(rect.get("w") or 0.0)
                h_mm = float(rect.get("h") or 0.0)
                if h_mm <= 0:
                    continue
                inferred_pt = (h_mm / 1.2) / MM_PER_PT
                if 0.0 < w_mm < h_mm:
                    # 1자(≈ font_mm * 0.85) 정도가 폭에 들어가도록 상한 보정.
                    inferred_pt = min(inferred_pt, (w_mm * 0.85) / MM_PER_PT)
                inferred_pt = max(6.0, min(12.0, inferred_pt))
                style["font_size_pt"] = round(inferred_pt, 2)
                obj["style"] = style
                obj.setdefault("unsupported_props", {})["font_size_inferred"] = "rect_h_mm"


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
