#!/usr/bin/env python3
"""
frf_unit_probe — `.frf` 좌표 단위 진단 스크립트.

배경:
  현 디코더 (`frf_decoder_poc.py` v0.2.x) 는 객체 직후 4×LE int32 를 *항상*
  TWIPS (1/1440 inch) 로 가정해 mm 로 환산한다. 그러나 실제 산출 IR/SVG 가
  페이지 상단 ~1cm 좁은 띠에 모든 객체가 뭉치는 현상을 보여, 좌표 단위 가정
  자체가 틀렸을 가능성이 매우 높다.

목적:
  *코드 변경 없이* 동일 .frf 입력에 대해 4 가지 단위 후보를 적용했을 때
  "plausible 한 mm 좌표" 가 얼마나 회수되는지 통계 비교 → 단위를 데이터로 결정.

평가 단위 후보:
  - twips_1440 : 1440/inch  → ÷56.6929 / mm
  - px_96      :   96/inch  → ÷ 3.7795 / mm
  - mm_100     :  100/mm    → ÷100      / mm
  - mm_10      :   10/mm    → ÷10       / mm

평가 메트릭 (각 단위별):
  - n_candidates      : 4×i32 후보 추출에 성공한 객체 수
  - n_plausible       : 좌표 4 값이 합리 범위 안인 객체 수
                        (0 ≤ x ≤ 600mm, 0 ≤ y ≤ 1500mm, 0 < w ≤ 600mm, 0 < h ≤ 1500mm)
  - plausible_ratio   : n_plausible / n_candidates
  - x_range/y_range   : 좌표 분포 (min .. p50 .. p95 .. max)
  - bbox_mm           : 모든 plausible 객체의 union bbox
  - aspect_ratio      : bbox.w / bbox.h
  - paper_match_score : ISO 표준 양식 (A4/A5/B4/B5/영수증류) bbox 와의 근사 정도

사용:
  python3 debug/frf_unit_probe.py <path/to/file.frf> [<path/to/file2.frf> ...]
  python3 debug/frf_unit_probe.py  # 기본 샘플 2종 자동 평가

본 스크립트는 *읽기 전용 진단* — 디코더/IR/HTML 산출물에 영향을 주지 않는다.
"""
from __future__ import annotations

import argparse
import importlib.util
import statistics
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_decoder():
    """frf_decoder_poc 를 dynamic import — sys.modules 등록 필수 (dataclasses)."""
    p = REPO_ROOT / "debug" / "frf_decoder_poc.py"
    spec = importlib.util.spec_from_file_location("frf_decoder_poc", p)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load decoder: {p}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name or "frf_decoder_poc"] = mod
    spec.loader.exec_module(mod)
    return mod


# 단위 후보 — (이름, divisor: raw_int / divisor = mm)
UNIT_CANDIDATES: list[tuple[str, float]] = [
    ("twips_1440", 1440.0 / 25.4),
    ("px_96", 96.0 / 25.4),
    ("mm_100", 100.0),
    ("mm_10", 10.0),
]

# 합리 범위 (단위와 무관 — mm 환산 후 검사)
X_RANGE_MM = (-50.0, 600.0)
Y_RANGE_MM = (-50.0, 1500.0)
W_RANGE_MM = (0.1, 600.0)
H_RANGE_MM = (0.1, 1500.0)

# 알려진 인쇄 양식 (mm) — paper_match_score 용
KNOWN_PAPERS = [
    ("A4_portrait", 210.0, 297.0),
    ("A4_landscape", 297.0, 210.0),
    ("A5_portrait", 148.0, 210.0),
    ("A5_landscape", 210.0, 148.0),
    ("B4_portrait", 250.0, 353.0),
    ("B5_portrait", 176.0, 250.0),
    ("Letter_portrait", 215.9, 279.4),
    ("Receipt_182x128", 182.0, 128.0),
    ("Receipt_128x182", 128.0, 182.0),
]


@dataclass
class RawHit:
    object_name: str
    offset_after: int
    raw_l: int
    raw_t: int
    raw_w: int
    raw_h: int


def collect_raw_candidates(decoder, raw: bytes) -> list[RawHit]:
    """객체 hit 직후의 첫 번째 4×i32 후보를 단순 추출 (단위 환산 *전*).

    디코더 v0.2 의 try_extract_rect_after 가 best-fit + plausibility 까지 묶어
    수행하지만, 본 진단은 raw int 만 필요하므로 *3 바이트 헤더 다음 위치* 를
    1순위로 고정 (skip=3) 하고 실패 시 0..16 윈도우에서 첫 매칭만 사용.
    """
    hits = decoder.scan_word_strings(raw)
    classified = [(h, decoder.classify(h.text)) for h in hits]
    object_kinds = {
        "text_obj", "picture_obj", "line_obj", "rect_obj",
        "barcode_obj", "subreport_obj",
    }
    out: list[RawHit] = []
    n = len(raw)
    for h, kind in classified:
        if kind not in object_kinds:
            continue
        end = h.offset + 2 + len(h.text)
        for skip in (3, 0, 1, 2, 4, 5, 6, 7, 8):
            base = end + skip
            if base + 16 > n:
                break
            try:
                l, t, w, h_int = struct.unpack_from("<iiii", raw, base)
            except struct.error:
                continue
            out.append(RawHit(
                object_name=h.text,
                offset_after=base,
                raw_l=l, raw_t=t, raw_w=w, raw_h=h_int,
            ))
            break
    return out


def evaluate_unit(raw_hits: list[RawHit], divisor: float) -> dict:
    plausible: list[tuple[float, float, float, float]] = []
    for r in raw_hits:
        x = r.raw_l / divisor
        y = r.raw_t / divisor
        w = r.raw_w / divisor
        hh = r.raw_h / divisor
        if not (X_RANGE_MM[0] <= x <= X_RANGE_MM[1]):
            continue
        if not (Y_RANGE_MM[0] <= y <= Y_RANGE_MM[1]):
            continue
        if not (W_RANGE_MM[0] <= w <= W_RANGE_MM[1]):
            continue
        if not (H_RANGE_MM[0] <= hh <= H_RANGE_MM[1]):
            continue
        plausible.append((x, y, w, hh))

    n_candidates = len(raw_hits)
    n_plausible = len(plausible)
    if n_plausible == 0:
        return {
            "n_candidates": n_candidates,
            "n_plausible": 0,
            "plausible_ratio": 0.0,
            "bbox_mm": None,
            "aspect_ratio": None,
            "x_distribution": None,
            "y_distribution": None,
            "paper_match_score": 0.0,
            "best_paper": None,
        }

    xs = [p[0] for p in plausible]
    ys = [p[1] for p in plausible]
    rights = [p[0] + p[2] for p in plausible]
    bottoms = [p[1] + p[3] for p in plausible]
    bbox = {
        "x0": min(xs), "y0": min(ys),
        "x1": max(rights), "y1": max(bottoms),
    }
    bw = bbox["x1"] - bbox["x0"]
    bh = bbox["y1"] - bbox["y0"]
    aspect = bw / bh if bh > 0 else None

    best_paper = None
    best_score = 0.0
    for name, pw, ph in KNOWN_PAPERS:
        # 양식이 페이지 안에 들어맞는 정도: bbox 가 papers 안 + bbox 면적 / paper 면적
        if bw <= pw * 1.05 and bh <= ph * 1.05:
            fill = (bw * bh) / (pw * ph) if pw * ph > 0 else 0
            if fill > best_score:
                best_score = fill
                best_paper = name

    return {
        "n_candidates": n_candidates,
        "n_plausible": n_plausible,
        "plausible_ratio": n_plausible / n_candidates if n_candidates else 0.0,
        "bbox_mm": {k: round(v, 2) for k, v in bbox.items()},
        "bbox_size_mm": {"w": round(bw, 2), "h": round(bh, 2)},
        "aspect_ratio": round(aspect, 3) if aspect else None,
        "x_distribution": {
            "min": round(min(xs), 2),
            "p50": round(statistics.median(xs), 2),
            "p95": round(statistics.quantiles(xs, n=20)[-1] if len(xs) >= 20 else max(xs), 2),
            "max": round(max(xs), 2),
        },
        "y_distribution": {
            "min": round(min(ys), 2),
            "p50": round(statistics.median(ys), 2),
            "p95": round(statistics.quantiles(ys, n=20)[-1] if len(ys) >= 20 else max(ys), 2),
            "max": round(max(ys), 2),
        },
        "paper_match_score": round(best_score, 3),
        "best_paper": best_paper,
    }


def probe_file(decoder, path: Path) -> dict:
    raw = path.read_bytes()
    raw_hits = collect_raw_candidates(decoder, raw)
    units = {}
    for name, divisor in UNIT_CANDIDATES:
        units[name] = evaluate_unit(raw_hits, divisor)
    return {
        "file": str(path),
        "size_bytes": len(raw),
        "raw_hits": len(raw_hits),
        "units": units,
    }


def render_report(reports: list[dict]) -> str:
    lines: list[str] = []
    for rep in reports:
        lines.append("")
        lines.append(f"=== {Path(rep['file']).name}  ({rep['size_bytes']:,} bytes, raw_hits={rep['raw_hits']}) ===")
        header = f"  {'unit':<12} | {'plausible':>10} | {'fill%':>6} | {'bbox(mm)':>16} | {'aspect':>6} | {'paper':>20}"
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        # 점수 기반 정렬 — paper_match_score, plausible_ratio
        sorted_units = sorted(
            rep["units"].items(),
            key=lambda kv: (kv[1].get("paper_match_score") or 0, kv[1].get("plausible_ratio") or 0),
            reverse=True,
        )
        for name, ev in sorted_units:
            ratio_txt = f"{ev['n_plausible']}/{ev['n_candidates']}"
            fill_txt = f"{(ev['plausible_ratio'] or 0) * 100:5.1f}%"
            bbox = ev.get("bbox_size_mm") or {}
            bbox_txt = (
                f"{bbox.get('w', 0):>5.0f}×{bbox.get('h', 0):<5.0f}"
                if bbox else "-"
            )
            ar = ev.get("aspect_ratio")
            ar_txt = f"{ar:5.2f}" if ar is not None else "  -  "
            paper_txt = (ev.get("best_paper") or "-")
            lines.append(
                f"  {name:<12} | {ratio_txt:>10} | {fill_txt:>6} | "
                f"{bbox_txt:>16} | {ar_txt:>6} | {paper_txt:>20}"
            )
    return "\n".join(lines)


_DEFAULT_SAMPLES = [
    REPO_ROOT / "legacy_delphi_source/legacy_source/Report/Report_1_21.frf",
    REPO_ROOT / "legacy_delphi_source/legacy_source/Report/계산서.frf",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FRF 좌표 단위 진단 (read-only)")
    parser.add_argument("files", nargs="*", type=Path,
                        help="진단할 .frf 파일 경로들 (생략 시 기본 샘플 2종)")
    args = parser.parse_args(argv)

    decoder = _load_decoder()
    targets = args.files or [p for p in _DEFAULT_SAMPLES if p.is_file()]
    if not targets:
        print("[probe] 평가할 .frf 가 없음", file=sys.stderr)
        return 2

    reports = [probe_file(decoder, p) for p in targets]
    print(render_report(reports))

    # 종합 요약 — 단위별 paper_match_score + plausible_ratio 가산점
    overall: dict[str, list[float]] = {n: [] for n, _ in UNIT_CANDIDATES}
    for rep in reports:
        for unit_name, ev in rep["units"].items():
            score = (ev.get("paper_match_score") or 0) * 0.7 + (ev.get("plausible_ratio") or 0) * 0.3
            overall[unit_name].append(score)
    print("\n=== Overall ranking (mean of paper_match_score×0.7 + plausible_ratio×0.3) ===")
    ranked = sorted(
        overall.items(),
        key=lambda kv: statistics.mean(kv[1]) if kv[1] else 0,
        reverse=True,
    )
    for name, scores in ranked:
        m = statistics.mean(scores) if scores else 0
        print(f"  {name:<12} mean={m:.3f}  per-file={[round(s, 3) for s in scores]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
