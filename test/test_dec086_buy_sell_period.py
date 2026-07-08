"""DEC-086 — 기간별 매입·매출(월/분기/년) + 엑셀 export 회귀 가드.

가드 포인트
-----------
1. get_book_sales 행에 ``gisum``(매입액 — Scode='Y' 입고/반품 행 Gssum 누적) 추가.
2. get_sales_period — groupBy quarterly/yearly 버킷 라벨(YYYY-Qn/YYYY) +
   매입(buy_qut_total/buy_sum_total) 축 동시 집계, 기존 매출 키 하위 호환.
3. 엑셀 export 라우트(/stats/sales-period/export.xlsx) OpenAPI 등록 + 파라미터.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class BookSalesGisumTests(IsolatedAsyncioTestCase):
    async def test_inbound_rows_accumulate_gisum(self) -> None:
        from app.services import reports_service as rpt

        async def fake_exec(server_id: str, sql: str, params: tuple = ()):
            if "Sg_Csum" in sql:
                return []
            return [
                {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "",
                 "Gdate": "2026.07.01", "Gsqut": 5, "Gssum": 5000},
                {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "",
                 "Gdate": "2026.07.05", "Gsqut": 3, "Gssum": 3000},
            ]

        async def no_lookup(server_id: str, *, sql_template: str, keys: Any,
                            prefix_params: tuple = (), chunk_size: int | None = None):
            return []

        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=no_lookup):
            res = await rpt.get_book_sales(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-12-31",
            )
        row = res["rows"][0]
        self.assertEqual(row["giqut"], 5)
        self.assertEqual(row["gisum"], 5000)  # 매입액 (DEC-086)
        self.assertEqual(row["goqut"], 3)
        self.assertEqual(row["gosum"], 3000)
        self.assertEqual(row["gdate"], "2026.07.05")  # 최종거래일 = MAX(Gdate) (DEC-087)


class SalesPeriodBuySellTests(IsolatedAsyncioTestCase):
    async def _run(self, *, group_by: str, date_from: str, date_to: str) -> dict[str, Any]:
        from app.services import stats_service

        async def fake_book_sales(**kwargs):
            return {
                "rows": [
                    {"goqut": 2, "gosum": 200, "giqut": 1, "gisum": 100},
                ],
                "total": 1,
            }

        old = stats_service.reports_service.get_book_sales
        stats_service.reports_service.get_book_sales = fake_book_sales
        try:
            return await stats_service.get_sales_period(
                server_id="srv", hcode=None,
                date_from=date_from, date_to=date_to, group_by=group_by,
            )
        finally:
            stats_service.reports_service.get_book_sales = old

    async def test_quarterly_buckets_and_buy_fields(self) -> None:
        res = await self._run(group_by="quarterly", date_from="2026-01-01", date_to="2026-09-30")
        buckets = [i["bucket"] for i in res["items"]]
        self.assertEqual(buckets, ["2026-Q1", "2026-Q2", "2026-Q3"])
        first = res["items"][0]
        self.assertEqual(first["qut_total"], 2)       # 매출(기존 키 유지)
        self.assertEqual(first["buy_qut_total"], 1)   # 매입 수량
        self.assertEqual(first["buy_sum_total"], 100)  # 매입 금액
        self.assertEqual(res["totals"]["buy_sum_total"], 300)
        self.assertEqual(res["totals"]["sum_total"], 600)

    async def test_yearly_buckets(self) -> None:
        res = await self._run(group_by="yearly", date_from="2025-03-01", date_to="2026-02-28")
        self.assertEqual([i["bucket"] for i in res["items"]], ["2025", "2026"])

    async def test_unknown_group_by_falls_back_to_daily(self) -> None:
        res = await self._run(group_by="__evil__", date_from="2026-01-01", date_to="2026-01-02")
        self.assertEqual(res["items"][0]["group_by"], "daily")


class ExportRouteRegistrationTests(TestCase):
    def test_export_route_in_openapi(self) -> None:
        from app.main import app

        schema = app.openapi()
        path = schema["paths"].get("/api/v1/stats/sales-period/export.xlsx")
        self.assertIsNotNone(path, "엑셀 export 라우트가 등록되어야 한다")
        params = {p["name"] for p in path["get"].get("parameters", [])}
        self.assertLessEqual(
            {"serverId", "dateFrom", "dateTo", "groupBy", "sortBy", "sortDir"}, params
        )

    def test_all_stats_export_routes_registered(self) -> None:
        """DEC-089 — 통계 전 화면 엑셀 export 라우트 8종."""
        from app.main import app

        paths = set(app.openapi()["paths"])
        expected = {
            "/api/v1/stats/sales-period/export.xlsx",
            "/api/v1/stats/customer-analysis/export.xlsx",
            "/api/v1/stats/book-turnover/export.xlsx",
            "/api/v1/stats/publisher/export.xlsx",
            "/api/v1/stats/quarterly-summary/export.xlsx",
            "/api/v1/reports/book-sales/export.xlsx",
            "/api/v1/reports/customer-sales/export.xlsx",
            "/api/v1/reports/year-end-book/export.xlsx",
        }
        self.assertLessEqual(expected, paths)


if __name__ == "__main__":  # pragma: no cover
    main()
