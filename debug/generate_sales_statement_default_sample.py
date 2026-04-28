#!/usr/bin/env python3
"""거래명세서 ``layout=default`` (현재 운영 기본: 수동 2단 빌더) 샘플 HTML 생성.

IR ``sales_statement_base`` 는 ``auto_enabled: false`` 이므로 일반적으로
``try_render_with_ir`` 는 건너뛰고 ``transactions_service`` 의 수동 템플릿이 사용된다.

실행 (저장소 루트):

  PYTHONPATH=도서물류관리프로그램/backend python3 debug/generate_sales_statement_default_sample.py

산출:

  ``debug/output/sales_statement_default_sample.html``
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

OUT_DIR = ROOT / "debug" / "output"


def _sample_detail() -> dict:
    return {
        "order_key": {
            "gdate": "2026.04.27",
            "hcode": "H12345",
            "jubun": "SO-20260427-001",
            "gjisa": "본점",
        },
        "customer": {"hcode": "H12345", "gname": "샘플도서관(주)"},
        "lines": [
            {
                "gcode": "G001",
                "bcode": "9788936434267",
                "product_name": "한글시대의 시작",
                "pubun": "단행본",
                "gsqut": 5,
                "gssum": 67500,
                "gbigo": "",
            },
            {
                "gcode": "G002",
                "bcode": "9788937473302",
                "product_name": "모던 클래식 에세이",
                "pubun": "단행본",
                "gsqut": 2,
                "gssum": 25600,
                "gbigo": "특가",
            },
            {
                "gcode": "G003",
                "bcode": "8801234567890",
                "product_name": "잡지 구독 — 2026년 5월호",
                "pubun": "정간",
                "gsqut": 12,
                "gssum": 144000,
                "gbigo": "",
            },
        ],
    }


def main() -> int:
    from app.services.transactions_service import render_sales_statement_html

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "sales_statement_default_sample.html"
    html = render_sales_statement_html(_sample_detail(), layout="default")
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
