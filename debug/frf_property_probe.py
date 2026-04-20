#!/usr/bin/env python3
"""
frf_property_probe — `.frf` Memo 속성/Font 블록 byte layout 실측.

목적:
  v0.5.x 디코더 ([`debug/frf_decoder_poc.py`](debug/frf_decoder_poc.py)) 의
  ``try_extract_memo_props_after`` 가 ``i32@base+14`` 를 FillColor 로 잘못
  단정했고, 결과적으로 일부 양식 (계산서, Report_4_96 등) 에서 시각 회귀가
  발생했다. v0.5.1 Phase 0 에서 보수적으로 transparent 폴백했지만, *정확한*
  FillColor / Font.Name / Font.Size / Font.Color / Font.Style / Adjust(halign,
  valign) offset 을 데이터로 결정해야 v0.6.0 에서 정밀 디코드가 가능하다.

방법론 (READ-ONLY):
  1. 1,744 .frf + Tong06.dfm 의 frReportXX_YY.ReportForm BLOB 전수 스캔.
  2. Memo*_* 객체 직후 *128 byte* 윈도우를 추출.
  3. 각 윈도우에서 다음을 통계 추출:
     - 알려진 RGB 색 상수 (clNone=0x1FFFFFFF, clBlack=0, clWhite=0x00FFFFFF,
       clRed=0xFF, clBlue=0xFF0000, clGreen=0x008000, clTeal=0x008080,
       clSilver=0xC0C0C0, clGray=0x808080, clNavy=0x800000, clMaroon=0x80) 가
       어느 byte offset 에서 i32 LE 로 등장하는가 (FillColor / Font.Color
       후보).
     - WORD-prefixed 짧은 문자열 (length 1..32) 이 등장하는 위치 — 후보:
       'Arial', 'MS Sans Serif', 'Times New Roman', '굴림' (CP949 B1BCB8B2),
       '바탕' (CP949 B9CCC5C1), '돋움' (CP949 B5CBBFF2). Font.Name 후보.
     - Font.Size 후보: i32 in [6..72] (logical pt 또는 -px 음수).
     - Font.Style bit byte 후보 (0x00..0x0F = B/I/U/StrikeOut 조합).
     - Adjust 후보: byte = 0..15 (FreeReport `TfrAdjust`: 0=center 등).

산출:
  ``debug/output/frf_property_probe.{md,json}`` — 권장 offset 표 + 빈도/근거.

사용:
  python3 debug/frf_property_probe.py            # 1,744 전수 + Tong06 BLOB
  python3 debug/frf_property_probe.py --limit 50 # 빠른 sanity 모드
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import struct
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# 데이터 수집 — 1,744 .frf + Tong06 .dfm BLOB
# ---------------------------------------------------------------------------

MEMO_NAME_RE = re.compile(rb"Memo\d+_\d+(?=[\x00\x02])")
WINDOW_BYTES = 128

# Tong06.dfm 의 ReportForm = { … } 안의 hex 를 BLOB 으로 복원하기 위한 패턴.
DFM_REPORTFORM_RE = re.compile(
    r"ReportForm\s*=\s*\{([^}]*)\}", flags=re.DOTALL
)

# Delphi TColor 상수 (LE i32) — 0x00BBGGRR.
KNOWN_COLORS = {
    "clBlack":   0x00000000,
    "clWhite":   0x00FFFFFF,
    "clRed":     0x000000FF,
    "clBlue":    0x00FF0000,
    "clGreen":   0x00008000,
    "clTeal":    0x00808000,
    "clSilver":  0x00C0C0C0,
    "clGray":    0x00808080,
    "clYellow":  0x0000FFFF,
    "clNavy":    0x00800000,
    "clMaroon":  0x00000080,
    "clNone":    0x1FFFFFFF,
}

# 후보 Font.Name (ASCII / CP949).
FONT_NAME_CANDIDATES = [
    b"Arial",
    b"MS Sans Serif",
    b"Times New Roman",
    b"Courier New",
    b"Tahoma",
    b"Helvetica",
    b"\xb1\xbc\xb8\xb2",       # 굴림 CP949
    b"\xb9\xcc\xc5\xc1",       # 바탕 CP949 (= 0xB9CC + 0xC5C1)
    b"\xb5\xcb\xbf\xf2",       # 돋움 CP949
    b"\xb1\xc3\xbc\xad",       # 궁서 CP949 (변형)
]


def iter_frf_bytes(repo: Path, limit: int | None) -> Iterable[tuple[str, bytes]]:
    files = sorted(repo.rglob("*.frf"))
    if limit:
        files = files[:limit]
    for f in files:
        try:
            yield (str(f.relative_to(repo)), f.read_bytes())
        except OSError:
            continue


def iter_tong06_blobs(repo: Path) -> Iterable[tuple[str, bytes]]:
    dfm = repo / "legacy_delphi_source" / "legacy_source" / "Tong06.dfm"
    if not dfm.exists():
        return
    text = dfm.read_text(errors="replace")
    for i, m in enumerate(DFM_REPORTFORM_RE.finditer(text)):
        hex_lines = m.group(1)
        cleaned = re.sub(r"[^0-9A-Fa-f]", "", hex_lines)
        try:
            blob = bytes.fromhex(cleaned)
        except ValueError:
            continue
        yield (f"Tong06.dfm#blob{i}", blob)


# ---------------------------------------------------------------------------
# Memo property window 분석
# ---------------------------------------------------------------------------

def find_memo_windows(buf: bytes) -> list[tuple[int, bytes]]:
    """Memo*_* 이름이 등장하는 위치마다 (rect_offset 으로 가정되는 위치, 128 byte) 반환.

    base 위치 결정 규칙:
      - name 끝 직후 ``\\x00`` (null) + ``\\x02\\x00`` (separator) 다음의 4 i32 가
        rect (l,t,w,h). 그러므로 rect_offset = name_start + len(name) + 1 + 2
        = name_start + len(name) + 3, base = rect_offset + 16.
    """
    out: list[tuple[int, bytes]] = []
    for m in MEMO_NAME_RE.finditer(buf):
        name = m.group(0)
        rect_offset = m.start() + len(name) + 3
        base = rect_offset + 16
        if base + WINDOW_BYTES > len(buf):
            continue
        # rect plausibility — 우리는 이미 rect_offset 가설을 적용했으므로 거기서
        # 4 i32 를 unpack 해 합리 범위인지 검사 (false positive 거름).
        try:
            l, t, w, h = struct.unpack_from("<iiii", buf, rect_offset)
        except struct.error:
            continue
        if not (0 <= l < 5000 and 0 <= t < 5000 and 0 < w < 5000 and 0 < h < 1000):
            continue
        window = buf[base:base + WINDOW_BYTES]
        out.append((base, window))
    return out


def scan_known_colors(window: bytes, hits: collections.Counter) -> None:
    """window 내 모든 4-byte aligned 위치를 i32 LE 로 읽어 알려진 TColor 와 매칭."""
    for off in range(0, len(window) - 3):
        v = struct.unpack_from("<I", window, off)[0]
        for name, magic in KNOWN_COLORS.items():
            if v == magic:
                hits[(name, off)] += 1


def scan_font_names(window: bytes, hits: collections.Counter) -> None:
    """WORD-prefixed string 이면서 font name 후보와 일치하는 위치 회수."""
    for off in range(0, len(window) - 2):
        n = struct.unpack_from("<H", window, off)[0]
        if not (1 <= n <= 32):
            continue
        s = window[off + 2:off + 2 + n]
        if len(s) != n:
            continue
        for cand in FONT_NAME_CANDIDATES:
            if s == cand:
                hits[(cand.decode("cp949", errors="replace"), off)] += 1


def scan_font_size(window: bytes, hits: collections.Counter) -> None:
    """i32 in [-200..-6] (Delphi negative-px height) 또는 [6..72] (pt) 회수."""
    for off in range(0, len(window) - 3):
        v = struct.unpack_from("<i", window, off)[0]
        if 6 <= v <= 72 or -200 <= v <= -6:
            hits[("font_size_int", off, v)] += 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None,
                        help="처리할 .frf 파일 수 (디버그). 없음 → 전수.")
    parser.add_argument("--out-dir", type=Path,
                        default=REPO_ROOT / "debug" / "output",
                        help="결과 파일 저장 디렉토리.")
    args = parser.parse_args()

    color_hits: collections.Counter = collections.Counter()
    fontname_hits: collections.Counter = collections.Counter()
    fontsize_hits: collections.Counter = collections.Counter()
    total_windows = 0
    file_count = 0

    sources = list(iter_frf_bytes(REPO_ROOT, args.limit))
    sources += list(iter_tong06_blobs(REPO_ROOT))

    for label, buf in sources:
        windows = find_memo_windows(buf)
        if not windows:
            continue
        file_count += 1
        for _base, win in windows:
            total_windows += 1
            scan_known_colors(win, color_hits)
            scan_font_names(win, fontname_hits)
            scan_font_size(win, fontsize_hits)

    # ---- 권장 offset 결정 (최빈값) ----
    # FillColor 후보: 자주 나오는 0x1FFFFFFF (clNone) 의 가장 빈번한 offset.
    fill_offsets = collections.Counter()
    for (name, off), c in color_hits.items():
        if name == "clNone":
            fill_offsets[off] += c

    # FrameColor 후보: clBlack 의 최빈 offset (or 그냥 0).
    frame_offsets = collections.Counter()
    for (name, off), c in color_hits.items():
        if name in ("clBlack", "clBlue", "clRed"):
            frame_offsets[off] += c

    # FontColor 후보: clBlack 위치 중 FrameColor 와 다른 위치.
    fontcolor_offsets = collections.Counter()
    for (name, off), c in color_hits.items():
        if name == "clBlack":
            fontcolor_offsets[off] += c

    # FontName 후보: 각 후보별 최빈 offset.
    fontname_offsets: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    for (cand, off), c in fontname_hits.items():
        fontname_offsets[cand][off] += c

    # FontSize 후보: 가장 자주 등장하는 offset.
    fontsize_offsets: collections.Counter = collections.Counter()
    for (_kind, off, _v), c in fontsize_hits.items():
        fontsize_offsets[off] += c

    args.out_dir.mkdir(parents=True, exist_ok=True)
    md = args.out_dir / "frf_property_probe.md"
    js = args.out_dir / "frf_property_probe.json"

    summary = {
        "file_count": file_count,
        "total_windows": total_windows,
        "fill_color_offset_top": fill_offsets.most_common(8),
        "frame_color_offset_top": frame_offsets.most_common(8),
        "font_color_offset_top": fontcolor_offsets.most_common(8),
        "font_name_offset_per_candidate": {
            cand: oct.most_common(6) for cand, oct in fontname_offsets.items()
        },
        "font_size_offset_top": fontsize_offsets.most_common(8),
    }
    js.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                  encoding="utf-8")

    lines = ["# FRF Property/Font Probe Result", ""]
    lines.append(f"- file_count: {file_count}")
    lines.append(f"- total_windows: {total_windows}")
    lines.append("")
    lines.append("## FillColor offset (clNone 분포 = 최빈 위치가 정답)")
    for off, c in summary["fill_color_offset_top"]:
        lines.append(f"  - base+{off:3d}: {c}")
    lines.append("")
    lines.append("## FrameColor offset (clBlack/Blue/Red 합계 분포)")
    for off, c in summary["frame_color_offset_top"]:
        lines.append(f"  - base+{off:3d}: {c}")
    lines.append("")
    lines.append("## FontColor offset (clBlack 분포)")
    for off, c in summary["font_color_offset_top"]:
        lines.append(f"  - base+{off:3d}: {c}")
    lines.append("")
    lines.append("## Font.Name offset per candidate")
    for cand, top in summary["font_name_offset_per_candidate"].items():
        lines.append(f"  ### {cand}")
        for off, c in top:
            lines.append(f"  - base+{off:3d}: {c}")
    lines.append("")
    lines.append("## Font.Size offset")
    for off, c in summary["font_size_offset_top"]:
        lines.append(f"  - base+{off:3d}: {c}")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[probe] wrote {md} and {js}")
    print(f"[probe] file_count={file_count} total_windows={total_windows}")
    print(f"[probe] FillColor top offset = {fill_offsets.most_common(3)}")
    print(f"[probe] FrameColor top offset = {frame_offsets.most_common(3)}")
    print(f"[probe] FontColor top offset = {fontcolor_offsets.most_common(3)}")
    print(f"[probe] FontSize top offset = {fontsize_offsets.most_common(3)}")
    for cand, top in fontname_offsets.items():
        print(f"[probe] FontName {cand!r}: top offset = {top.most_common(3)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
