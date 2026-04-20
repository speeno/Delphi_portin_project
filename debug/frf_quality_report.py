#!/usr/bin/env python3
"""
frf_quality_report — 배치 변환 산출물의 IR/HTML 을 정량 평가하고 우선순위 리포트를 생성한다.

설계 근거
---------
- 사용자 규칙: "기존 코드를 우선 활용" — 본 모듈은 디코더/컴파일러를 *재호출하지 않고*,
  이미 산출된 `.ir.json` 만 읽어 통계만 만든다 (READ-ONLY 분석기).
- 일반화 규칙: 특정 양식의 케이스가 아니라 **모든 IR 에 동일 지표 적용** — 4 차원 점수.
- IR 스키마 정본: `analysis/print_specs/frf_ir_schema.md` v0.1.0.

산출 지표 (per-IR)
------------------
- `coord_recovery`     : 객체의 `rect_mm` 가 (0,0,0,0) 이 *아닌* 비율 — 좌표 복원률.
- `binding_fill`       : `binding.kind != literal` 또는 literal 이면서 value 가 비어있지
                         않은 객체 비율 — 텍스트/식 채움률.
- `object_coverage`    : 1 - (`unsupported_objects` 수 / 전체 객체 수) — 객체 인식률.
- `token_recovery`     : `expressions_dictionary` 가 비어있지 않은 비율 (IR 1건당 0/1).
- `priority_score`     : (1 - coord_recovery) + (1 - binding_fill) + (1 - object_coverage)
                         + 0.25 × (1 - token_recovery)
                         → **클수록 개선 우선순위 높음** (시각·데이터 둘 다 비어있을수록 ↑).

CLI:
  python3 debug/frf_quality_report.py
  python3 debug/frf_quality_report.py --batch-root debug/output/frf_converted_all
  python3 debug/frf_quality_report.py --top 30 --csv debug/output/frf_quality_topN.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# v0.3.0 (2026-04-20)
#   + Phase B/C 산출 IR 의 *Font 추출 회복률* 과 *opaque-white fill 회귀 카운트*
#     를 추적해 v0.5.0 회귀 (계산서 등에서 248/260 셀이 #FFFFFF 로 채워지던
#     문제) 의 영구 차단을 정량 검증한다.
REPORT_VERSION = "0.3.0"

# v0.3 디코더 (px_96 단위 교정) 이후 도입된 합리적 페이지 크기 범위 — mm
_PAGE_W_OK = (60.0, 320.0)
_PAGE_H_OK = (40.0, 600.0)


@dataclass
class IRMetrics:
    rel_path: str
    pages: int = 0
    bands: int = 0
    objects: int = 0
    objects_with_rect: int = 0
    objects_with_binding: int = 0
    text_objects: int = 0
    unsupported_objects: int = 0
    decoder_warnings: int = 0
    expressions: int = 0
    decoder_version: str = ""
    schema_version: str = ""
    raw_size_bytes: int = 0
    page_size_mm: tuple[float, float] = (0.0, 0.0)
    page_size_ok: bool = False
    coord_outliers: int = 0  # 좌표가 plausibility 한도를 살짝 벗어난 객체 수
    # v0.3.0 — Phase B/C 폰트/Fill 정량 메트릭.
    font_extracted_count: int = 0       # style._font_extracted=True 텍스트 객체 수
    fill_opaque_white_count: int = 0    # fill.color=#FFFFFF AND transparent=False (회귀 추적)
    fill_transparent_count: int = 0
    fill_colored_count: int = 0
    extras: dict = field(default_factory=dict)

    @property
    def coord_recovery(self) -> float:
        return _safe_div(self.objects_with_rect, self.objects)

    @property
    def binding_fill(self) -> float:
        return _safe_div(self.objects_with_binding, self.objects)

    @property
    def object_coverage(self) -> float:
        denom = self.objects + self.unsupported_objects
        return 1.0 - _safe_div(self.unsupported_objects, denom)

    @property
    def token_recovery(self) -> float:
        return 1.0 if self.expressions > 0 else 0.0

    @property
    def priority_score(self) -> float:
        return round(
            (1.0 - self.coord_recovery)
            + (1.0 - self.binding_fill)
            + (1.0 - self.object_coverage)
            + 0.25 * (1.0 - self.token_recovery),
            6,
        )

    @property
    def font_recovery(self) -> float:
        return _safe_div(self.font_extracted_count, self.text_objects)

    def to_row(self) -> dict[str, Any]:
        return {
            "rel": self.rel_path,
            "objects": self.objects,
            "coord_recovery": round(self.coord_recovery, 4),
            "binding_fill": round(self.binding_fill, 4),
            "object_coverage": round(self.object_coverage, 4),
            "token_recovery": round(self.token_recovery, 4),
            "font_recovery": round(self.font_recovery, 4),
            "fill_opaque_white": self.fill_opaque_white_count,
            "fill_transparent": self.fill_transparent_count,
            "fill_colored": self.fill_colored_count,
            "page_w_mm": round(self.page_size_mm[0], 2),
            "page_h_mm": round(self.page_size_mm[1], 2),
            "page_size_ok": int(self.page_size_ok),
            "coord_outliers": self.coord_outliers,
            "decoder_warnings": self.decoder_warnings,
            "unsupported_objects": self.unsupported_objects,
            "expressions": self.expressions,
            "raw_size_bytes": self.raw_size_bytes,
            "decoder_version": self.decoder_version,
            "priority_score": self.priority_score,
        }


def _safe_div(num: float, den: float) -> float:
    if den <= 0:
        return 0.0
    return float(num) / float(den)


def evaluate_ir(ir: dict, *, rel_path: str) -> IRMetrics:
    m = IRMetrics(
        rel_path=rel_path,
        decoder_version=str((ir.get("source") or {}).get("decoder_version", "")),
        schema_version=str(ir.get("schema_version", "")),
        raw_size_bytes=int((ir.get("source") or {}).get("raw_size_bytes", 0) or 0),
        decoder_warnings=len(ir.get("decoder_warnings") or []),
        unsupported_objects=len(ir.get("unsupported_objects") or []),
        expressions=len(ir.get("expressions_dictionary") or {}),
    )
    pages = ir.get("pages") or []
    m.pages = len(pages)
    if pages:
        size = (pages[0].get("size_mm") or {})
        pw = float(size.get("width", 0.0) or 0.0)
        ph = float(size.get("height", 0.0) or 0.0)
        m.page_size_mm = (pw, ph)
        m.page_size_ok = (
            _PAGE_W_OK[0] <= pw <= _PAGE_W_OK[1]
            and _PAGE_H_OK[0] <= ph <= _PAGE_H_OK[1]
        )
    for page in pages:
        bands = page.get("bands") or []
        m.bands += len(bands)
        for band in bands:
            for obj in band.get("objects") or []:
                m.objects += 1
                otype = obj.get("type")
                if otype == "Text":
                    m.text_objects += 1
                rect = obj.get("rect_mm") or {}
                w = float(rect.get("w", 0.0) or 0.0)
                h = float(rect.get("h", 0.0) or 0.0)
                x = float(rect.get("x", 0.0) or 0.0)
                y = float(rect.get("y", 0.0) or 0.0)
                if w > 0.0 and h > 0.0:
                    m.objects_with_rect += 1
                    # plausibility 한도 *살짝* 벗어남 (디코더가 통과시켰지만 의심스러운 후보)
                    if x < -10 or x > 320 or y < -10 or y > 1200:
                        m.coord_outliers += 1
                binding = obj.get("binding") or {}
                bkind = binding.get("kind")
                if bkind == "expression":
                    m.objects_with_binding += 1
                elif bkind == "literal":
                    val = binding.get("value") or binding.get("raw") or ""
                    if str(val).strip():
                        m.objects_with_binding += 1
                # v0.3.0 — font/fill 메트릭.
                style = obj.get("style") or {}
                if otype == "Text" and style.get("_font_extracted"):
                    m.font_extracted_count += 1
                fill = obj.get("fill") or {}
                if fill.get("transparent"):
                    m.fill_transparent_count += 1
                else:
                    color = (fill.get("color") or "").upper()
                    if color in ("#FFFFFF", "#FFF"):
                        m.fill_opaque_white_count += 1
                    elif color:
                        m.fill_colored_count += 1
    return m


def collect_ir_paths(root: Path) -> list[Path]:
    return sorted(root.rglob("*.ir.json"))


def aggregate(metrics: list[IRMetrics]) -> dict[str, Any]:
    total = len(metrics) or 1
    obj_total = sum(m.objects for m in metrics) or 1
    rect_total = sum(m.objects_with_rect for m in metrics)
    bind_total = sum(m.objects_with_binding for m in metrics)
    unsup_total = sum(m.unsupported_objects for m in metrics)
    warn_total = sum(m.decoder_warnings for m in metrics)
    expr_files = sum(1 for m in metrics if m.expressions > 0)

    buckets = {"empty_layout": 0, "low": 0, "mid": 0, "ok": 0}
    for m in metrics:
        cr = m.coord_recovery
        if cr <= 0.05:
            buckets["empty_layout"] += 1
        elif cr <= 0.5:
            buckets["low"] += 1
        elif cr <= 0.85:
            buckets["mid"] += 1
        else:
            buckets["ok"] += 1

    page_ok_count = sum(1 for m in metrics if m.page_size_ok)
    outlier_total = sum(m.coord_outliers for m in metrics)
    decoder_versions = sorted({m.decoder_version for m in metrics if m.decoder_version})

    text_total = sum(m.text_objects for m in metrics) or 1
    font_extracted_total = sum(m.font_extracted_count for m in metrics)
    opaque_white_total = sum(m.fill_opaque_white_count for m in metrics)
    fill_transparent_total = sum(m.fill_transparent_count for m in metrics)
    fill_colored_total = sum(m.fill_colored_count for m in metrics)

    return {
        "files": len(metrics),
        "objects_total": obj_total,
        "text_objects_total": text_total,
        "coord_recovery_overall": round(rect_total / obj_total, 4),
        "binding_fill_overall": round(bind_total / obj_total, 4),
        "font_recovery_overall": round(font_extracted_total / text_total, 4),
        "font_extracted_total": font_extracted_total,
        "fill_opaque_white_total": opaque_white_total,
        "fill_transparent_total": fill_transparent_total,
        "fill_colored_total": fill_colored_total,
        "unsupported_objects_total": unsup_total,
        "decoder_warnings_total": warn_total,
        "files_with_expressions": expr_files,
        "files_with_expressions_ratio": round(expr_files / total, 4),
        "page_size_ok_files": page_ok_count,
        "page_size_ok_ratio": round(page_ok_count / total, 4),
        "coord_outliers_total": outlier_total,
        "coord_outliers_ratio": round(outlier_total / obj_total, 4),
        "decoder_versions": decoder_versions,
        "buckets_by_coord_recovery": buckets,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Batch FRF quality report")
    ap.add_argument(
        "--batch-root",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "debug/output/frf_converted_all",
        help="배치 변환 산출 루트 (recursive *.ir.json 검색)",
    )
    ap.add_argument(
        "--top",
        type=int,
        default=20,
        help="우선순위 상위 N 개를 stdout 에 출력",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="JSON 리포트 저장 경로 (기본: <batch-root>/_quality_report.json)",
    )
    ap.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="파일별 지표를 CSV 로도 저장 (옵션)",
    )
    args = ap.parse_args(argv)

    root: Path = args.batch_root
    if not root.is_dir():
        print(f"batch root not found: {root}", file=sys.stderr)
        return 2

    paths = collect_ir_paths(root)
    if not paths:
        print(f"no *.ir.json under {root}", file=sys.stderr)
        return 1

    metrics: list[IRMetrics] = []
    fail_files: list[dict] = []
    for p in paths:
        rel = str(p.relative_to(root))
        try:
            ir = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            fail_files.append({"rel": rel, "error": f"{type(e).__name__}: {e}"})
            continue
        metrics.append(evaluate_ir(ir, rel_path=rel))

    metrics.sort(key=lambda m: (-m.priority_score, m.rel_path))
    agg = aggregate(metrics)

    payload = {
        "report_version": REPORT_VERSION,
        "batch_root": str(root),
        "scanned": len(paths),
        "ok": len(metrics),
        "fail": len(fail_files),
        "summary": agg,
        "fail_files": fail_files,
        "top_priority": [m.to_row() for m in metrics[: max(0, args.top)]],
        "all_files": [m.to_row() for m in metrics],
    }

    out_path = args.out or (root / "_quality_report.json")
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.csv is not None:
        with args.csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "rel",
                    "objects",
                    "coord_recovery",
                    "binding_fill",
                    "object_coverage",
                    "token_recovery",
                    "font_recovery",
                    "fill_opaque_white",
                    "fill_transparent",
                    "fill_colored",
                    "page_w_mm",
                    "page_h_mm",
                    "page_size_ok",
                    "coord_outliers",
                    "decoder_warnings",
                    "unsupported_objects",
                    "expressions",
                    "raw_size_bytes",
                    "decoder_version",
                    "priority_score",
                ],
            )
            w.writeheader()
            for m in metrics:
                w.writerow(m.to_row())

    print(
        json.dumps(
            {
                "scanned": len(paths),
                "ok": len(metrics),
                "fail": len(fail_files),
                "summary": agg,
                "report": str(out_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
