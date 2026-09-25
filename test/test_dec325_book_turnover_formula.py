"""DEC-325 — 도서 회전율(회) = 판매수량 ÷ 평균재고((기초+기말)/2) + 판매 컬럼 + 차트=표 순서 (2026-09-25)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

from app.services import stats_service as ss

PAGE = (Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
        / "stats" / "book-turnover" / "page.tsx")


def _run(rows, stock):
    async def fake_sales(**_):
        return {"rows": rows, "total": len(rows)}

    async def fake_stock(server_id, *, hcode, asof, axis_like, bcodes):
        return stock(asof)

    with patch.object(ss.reports_service, "get_book_sales", side_effect=fake_sales), \
            patch.object(ss.reports_service, "_fetch_stock_asof", side_effect=fake_stock):
        return asyncio.run(ss.get_book_turnover(
            server_id="s", hcode="5019", date_from="2026-08-25", date_to="2026-09-24",
        ))


class Formula(TestCase):
    def test_sale_over_average_stock(self) -> None:
        # 판매 = 출고 170 + 반품 −20 = 150, 기초 200·기말 100 → 평균 150 → 1.00회. 입고 0 이어도 계산된다(종전 0).
        res = _run(
            [{"gcode": "A", "gname": "a", "giqut": 0, "goqut": 170, "gbqut": -20, "gosum": 1700, "gbsum": -200}],
            lambda asof: {"A": 200 if asof == "2026.08.24" else 100},
        )
        it = res["items"][0]
        self.assertEqual((it["sale_qut"], it["sale_amt"]), (150, 1500))
        self.assertEqual((it["opening_stock"], it["closing_stock"]), (200, 100))
        self.assertEqual(it["turnover_ratio"], 1.0)
        self.assertEqual(res["totals"]["overall_turnover"], 1.0)

    def test_non_positive_average_is_blank_and_sorted_last(self) -> None:
        res = _run(
            [{"gcode": "A", "gname": "a", "goqut": 5}, {"gcode": "B", "gname": "b", "goqut": 5}],
            lambda asof: {"A": 0, "B": 10},
        )
        self.assertEqual([i["gcode"] for i in res["items"]], ["B", "A"])
        self.assertIsNone(res["items"][1]["turnover_ratio"])


class Page(TestCase):
    def test_columns_chart_and_default_sort(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        for label in ("판매수량", "판매금액", "기초재고", "기말재고", "회전율(회)"):
            self.assertIn(f'label: "{label}"', src)
        self.assertIn('{ key: "turnover_ratio", dir: "desc" }', src)
        self.assertIn("data.items.slice(0, topN)", src, "막대 = 표 앞 N행")
        self.assertIn("secondaryAxisRaw", src)
        self.assertNotIn("toFixed(4)", src, "종전 0.0000 표기 제거")


if __name__ == "__main__":
    main()
