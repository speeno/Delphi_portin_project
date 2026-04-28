#!/usr/bin/env python3
"""거래명세서 ``layout=legacy_triplicate`` 레거시 삼련 샘플 HTML 생성.

실행 (저장소 루트):

  PYTHONPATH=도서물류관리프로그램/backend python3 debug/generate_sales_statement_legacy_triplicate_sample.py

산출:

  ``debug/output/sales_statement_legacy_triplicate_sample.html``
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
            "gdate": "2026.04.28",
            "hcode": "A-0001",
            "jubun": "SO-20260428-001",
            "gjisa": "",
        },
        "customer": {"hcode": "A-0001", "gname": "샘플거래처"},
        "lines": [
            {
                "gcode": "G001",
                "bcode": "BOOK001",
                "product_name": "레거시 삼련 거래명세서 샘플 도서",
                "shelf": "A-1",
                "gsqut": 2,
                "gdang": 15000,
                "grat1": 10,
                "gssum": 30000,
                "gbigo": "",
            },
            {
                "gcode": "G002",
                "bcode": "BOOK002",
                "product_name": "파주 광탄 물류 반품 안내 확인용",
                "shelf": "B-3",
                "gsqut": 1,
                "gdang": 22000,
                "grat1": 0,
                "gssum": 22000,
                "gbigo": "",
            },
        ],
    }


def main() -> int:
    from app.services.transactions_service import render_sales_statement_html

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "sales_statement_legacy_triplicate_sample.html"
    html = render_sales_statement_html(
        _sample_detail(),
        layout="legacy_triplicate",
        server_id="remote_sample",
    )
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
