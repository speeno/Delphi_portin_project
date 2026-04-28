#!/usr/bin/env python3
"""구현된 ``barcode_svg_service`` 로 심볼로지별 샘플 바코드를 SVG·PNG로 저장.

실행 (저장소 루트):
  PYTHONPATH=도서물류관리프로그램/backend python3 debug/generate_barcode_sample_images.py

산출:
  - ``debug/output/barcode_samples/*.svg`` · ``*.png``
  - ``debug/output/barcode_samples/index.html`` — 브라우저에서 유형별 미리보기
"""
from __future__ import annotations

import html as html_lib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

OUT = ROOT / "debug" / "output" / "barcode_samples"
OUT.mkdir(parents=True, exist_ok=True)


def _mm_to_px(mm: float, dpi: float = 144.0) -> int:
    return max(32, int(round(mm * dpi / 25.4)))


def _png_via_rsvg(svg_path: Path, png_path: Path, w_mm: float, h_mm: float) -> bool:
    exe = shutil.which("rsvg-convert")
    if not exe:
        return False
    w_px = _mm_to_px(w_mm)
    h_px = _mm_to_px(h_mm)
    try:
        subprocess.run(
            [exe, "-w", str(w_px), "-h", str(h_px), str(svg_path), "-o", str(png_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return png_path.is_file()
    except (subprocess.CalledProcessError, OSError):
        return False


# (파일 접두사, symbology, 페이로드, 폭mm, 높이mm, 설명)
SAMPLES: list[tuple[str, str, str, float, float, str]] = [
    ("s01_code128_isbn", "code128", "9788936434260", 55.0, 16.0, "Code128 ISBN"),
    ("s02_code128_ship", "code128", "SHIP-2026-0001", 65.0, 14.0, "Code128 알파넘"),
    ("s03_code39", "code39", "ABC-123", 48.0, 14.0, "Code39"),
    ("s04_ean13", "ean13", "590123412345", 42.0, 16.0, "EAN-13 (12자리+체크)"),
    ("s05_ean8", "ean8", "1234567", 32.0, 14.0, "EAN-8"),
    ("s06_upca", "upca", "01234567890", 42.0, 18.0, "UPC-A"),
    ("s07_itf", "itf", "00123456", 50.0, 14.0, "ITF Interleaved 2 of 5"),
    ("s08_isbn13", "isbn13", "9780306405731", 50.0, 16.0, "ISBN-13 심볼"),
    ("s09_codabar", "codabar", "A123456A", 52.0, 14.0, "Codabar"),
    ("s10_qr_url", "qr", "https://example.com/books/9788936434260", 28.0, 28.0, "QR URL"),
    ("s11_qr_utf8", "qr", "도서물류 샘플 QR", 30.0, 30.0, "QR UTF-8"),
]


def _write_gallery_html(out_dir: Path) -> None:
    """유형별 PNG 를 한 페이지에서 볼 수 있는 정적 갤러리."""
    cards: list[str] = []
    for prefix, sym, payload, w_mm, h_mm, desc in SAMPLES:
        png = out_dir / f"{prefix}.png"
        if not png.is_file():
            continue
        cards.append(
            "<section class='card'>"
            f"<h2>{html_lib.escape(prefix)} — <code>{html_lib.escape(sym)}</code></h2>"
            f"<p class='desc'>{html_lib.escape(desc)}</p>"
            "<p class='meta'>"
            f"페이로드: <code>{html_lib.escape(payload)}</code> · "
            f"박스: {html_lib.escape(str(w_mm))}×{html_lib.escape(str(h_mm))} mm · "
            f"<a href='{html_lib.escape(prefix)}.svg'>SVG</a>"
            "</p>"
            f"<div class='imgwrap'><img src='{html_lib.escape(prefix)}.png' alt=''/></div>"
            "</section>"
        )
    body = "\n".join(cards)
    doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>바코드 유형별 샘플</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 52rem; margin: 1.5rem auto; padding: 0 1rem; color: #111; }}
h1 {{ font-size: 1.35rem; }}
.note {{ color: #444; font-size: 0.9rem; margin-bottom: 1.5rem; }}
.card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0; background: #fafafa; }}
.card h2 {{ font-size: 1rem; margin: 0 0 0.5rem 0; }}
.desc {{ margin: 0.25rem 0; }}
.meta {{ font-size: 0.85rem; color: #555; margin: 0 0 0.75rem 0; }}
.meta code {{ background: #eee; padding: 0.1em 0.35em; border-radius: 4px; }}
.imgwrap {{ background: #fff; border: 1px solid #e0e0e0; padding: 12px; border-radius: 6px; text-align: center; }}
img {{ max-width: 100%; height: auto; vertical-align: middle; }}
</style></head><body>
<h1>바코드 유형별 샘플 이미지</h1>
<p class="note">생성 스크립트: <code>debug/generate_barcode_sample_images.py</code><br/>
이 폴더를 브라우저로 열거나, VS Code Live Server 등으로 <code>index.html</code> 을 여세요.</p>
{body}
</body></html>
"""
    (out_dir / "index.html").write_text(doc, encoding="utf-8")


def main() -> int:
    from app.services import barcode_svg_service as bsvc

    if not bsvc.is_barcode_engine_available():
        print("python-barcode 미설치 — pip install python-barcode 후 재실행")
        return 1

    png_ok = False
    HTML = None  # type: ignore[assignment]
    try:
        from weasyprint import HTML as _HTML  # type: ignore[import-not-found]

        HTML = _HTML
        png_ok = True
    except Exception as exc:
        print(f"WeasyPrint PNG 스킵: {exc}")

    lines = [
        "샘플 바코드 (barcode_svg_service — 다중 심볼로지)",
        "갤러리(미리보기): debug/output/barcode_samples/index.html",
        "생성: debug/generate_barcode_sample_images.py",
        "지원: " + ", ".join(bsvc.list_supported_symbologies()),
        "",
    ]

    for prefix, sym, payload, w_mm, h_mm, desc in SAMPLES:
        if sym == "qr" and not bsvc.is_qr_engine_available():
            print(f"[skip] {prefix}: segno 미설치 (pip install segno)")
            lines.append(f"[skip] {prefix} ({sym}) — segno 없음")
            continue
        svg = bsvc.render_barcode_svg_for_print(payload, w_mm, h_mm, symbology=sym)
        if not svg:
            print(f"[skip] {prefix}: 인코딩 실패 sym={sym} payload={payload!r}")
            lines.append(f"[skip] {prefix} ({sym}) — 인코딩 실패")
            continue
        svg_path = OUT / f"{prefix}.svg"
        svg_path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {svg_path} ({desc})")
        lines.append(f"{prefix}.svg / .png — {sym} — {desc}")

        png_path = OUT / f"{prefix}.png"
        wrote_png = False
        if png_ok and HTML is not None:
            page_w, page_h = w_mm, h_mm
            html_doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"/>
<style>
@page {{ size: {page_w}mm {page_h}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; width: {page_w}mm; height: {page_h}mm; }}
body > svg {{ display: block; width: {page_w}mm; height: {page_h}mm; }}
</style></head><body>{svg}</body></html>"""
            try:
                HTML(string=html_doc, base_url=str(OUT)).write_png(
                    str(png_path),
                    resolution=144,
                )
                wrote_png = png_path.is_file()
            except Exception as exc:
                print(f"[warn] WeasyPrint PNG 실패 {prefix}: {exc}")
        if not wrote_png:
            if _png_via_rsvg(svg_path, png_path, w_mm, h_mm):
                print(f"Wrote {png_path} (rsvg-convert)")
            else:
                print(f"[warn] PNG 미생성 {prefix} (WeasyPrint·rsvg-convert 불가)")
        else:
            print(f"Wrote {png_path} (WeasyPrint)")

    (OUT / "README.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    _write_gallery_html(OUT)
    print(f"Wrote {OUT / 'index.html'} (갤러리)")
    print(f"\n완료: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
