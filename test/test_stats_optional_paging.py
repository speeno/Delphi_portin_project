"""
통계 화면 옵셔널 필터 + 표준 페이징 회귀.

사용자 요구:
- 통계 화면의 거래처/도서/출판사 필터가 비어 있으면 전체 대상으로 조회한다.
- 대량 데이터에 대비해 기존 목록과 동일한 page 메타 + DataGridPager 패턴을 사용한다.
- 페이징 네비게이션은 그리드 상단에 둔다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"

sys.path.insert(0, str(BACKEND))


class StatsBackendOptionalPaging(IsolatedAsyncioTestCase):
    async def test_customer_analysis_forwards_optional_hcode_and_page(self):
        from app.services import stats_service

        calls: list[dict] = []

        async def fake_customer_sales(**kwargs):
            calls.append(kwargs)
            return {
                "rows": [{"hcode": "H1", "goqut": 2, "gosum": 3000}],
                "total": 12,
                "page": {"limit": 5, "offset": 5, "total": 12, "has_more": True},
            }

        old = stats_service.reports_service.get_customer_sales
        stats_service.reports_service.get_customer_sales = fake_customer_sales
        try:
            res = await stats_service.get_customer_analysis(
                server_id="remote_138",
                hcode="",
                date_from="2026-01-01",
                date_to="2026-01-31",
                limit=5,
                offset=5,
            )
        finally:
            stats_service.reports_service.get_customer_sales = old

        self.assertIsNone(calls[0]["hcode"])
        self.assertEqual(calls[0]["limit"], 5)
        self.assertEqual(calls[0]["offset"], 5)
        self.assertEqual(res["page"]["total"], 12)
        self.assertEqual(res["totals"]["count"], 12)
        self.assertEqual(res["metadata"]["scope"], "all")

    async def test_book_turnover_accepts_empty_hcode_and_returns_page(self):
        from app.services import stats_service

        async def fake_book_sales(**kwargs):
            self.assertIsNone(kwargs["hcode"])
            return {
                "rows": [
                    {"gcode": "B2", "gname": "Book 2", "giqut": 1, "goqut": 5},
                    {"gcode": "B1", "gname": "Book 1", "giqut": 10, "goqut": 1},
                ],
                "total": 2,
            }

        old = stats_service.reports_service.get_book_sales
        stats_service.reports_service.get_book_sales = fake_book_sales
        try:
            res = await stats_service.get_book_turnover(
                server_id="remote_138",
                hcode="",
                date_from="2026-01-01",
                date_to="2026-01-31",
                limit=1,
                offset=0,
            )
        finally:
            stats_service.reports_service.get_book_sales = old

        self.assertEqual(res["page"], {"limit": 1, "offset": 0, "total": 2, "has_more": True})
        self.assertEqual([i["gcode"] for i in res["items"]], ["B2"])

    async def test_publisher_stats_groups_by_hcode_and_pages(self):
        """DEC-082 — 출판사 축 = S1_Ssub.Hcode 그룹(get_publisher_sales_summary 재사용).

        (구 구현은 get_book_sales 행에 없는 pcode 를 읽어 전부 "미분류" 로 합산되던
        버그가 있었다 — 본 테스트는 정본 축/이름 lookup 재사용을 고정한다.)
        """
        from app.services import stats_service

        async def fake_publisher_summary(**kwargs):
            self.assertIsNone(kwargs["hcode"])
            return {
                "rows": [
                    {"hcode": "P1", "book_count": 2, "giqut": 8, "goqut": 9,
                     "gbqut": 1, "gjqut": 12, "gosum": 3000, "gpqut": 0, "gpsum": 0},
                ],
                "truncated": False,
            }

        async def fake_names(server_id, hcodes):
            return {"P1": "Pub"}

        old_summary = stats_service.reports_service.get_publisher_sales_summary
        old_names = stats_service.inbound_service._fetch_publisher_names
        stats_service.reports_service.get_publisher_sales_summary = fake_publisher_summary
        stats_service.inbound_service._fetch_publisher_names = fake_names
        try:
            res = await stats_service.get_publisher_stats(
                server_id="remote_138",
                hcode=None,
                date_from="2026-01-01",
                date_to="2026-01-31",
                limit=100,
                offset=0,
            )
        finally:
            stats_service.reports_service.get_publisher_sales_summary = old_summary
            stats_service.inbound_service._fetch_publisher_names = old_names

        self.assertEqual(res["page"]["total"], 1)
        self.assertEqual(res["items"][0]["publisher_code"], "P1")
        self.assertEqual(res["items"][0]["publisher_name"], "Pub")
        self.assertEqual(res["items"][0]["book_count"], 2)
        self.assertEqual(res["totals"]["sales_total"], 3000)
        self.assertEqual(res["metadata"]["publisher_source"], "s1_ssub_hcode")


class StatsFrontendStaticPaging(TestCase):
    def test_stats_pages_use_top_pager_and_optional_filter(self):
        pages = [
            FE / "app" / "(app)" / "stats" / "monthly" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "customer" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "book" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "sales-period" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "customer-analysis" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "book-turnover" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "quarterly-summary" / "page.tsx",
            FE / "app" / "(app)" / "stats" / "publisher" / "page.tsx",
        ]
        for page in pages:
            src = page.read_text(encoding="utf-8")
            self.assertIn("DataGridPager", src, f"{page} should render top pager")
            self.assertIn("offset: 0", src, f"{page} should reset offset on search")

        book_page = (FE / "app" / "(app)" / "stats" / "book" / "page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("fetchAllPages", book_page)
        self.assertNotIn("hcode)는 필수", book_page)

        publisher_page = (FE / "app" / "(app)" / "stats" / "publisher" / "page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("ScreenPlaceholder", publisher_page)
        self.assertIn("statsApi.publisher", publisher_page)

    def test_reports_book_sales_optional_hcode_top_pager(self):
        """C6 Sobo61 /reports/book-sales — 통계·목록과 동일 정책(DEC-033 f)."""
        p = FE / "app" / "(app)" / "reports" / "book-sales" / "page.tsx"
        src = p.read_text(encoding="utf-8")
        self.assertNotIn("거래처 hcode 는 필수", src)
        self.assertIn('hcode: eHcode.trim() || undefined', src)
        self.assertIn("DataGridPager", src)
        self.assertIn("<DataGridPager", src)
        # DEC-141 — 그리드 행 타입이 파생 필드(매출부수/매출액) 포함 GridRow 로 확장됨.
        dg_idx = src.find("<DataGrid<BookSalesGridRow>")
        pager_idx = src.find("<DataGridPager")
        self.assertGreaterEqual(pager_idx, 0)
        self.assertGreaterEqual(dg_idx, 0)
        self.assertLess(pager_idx, dg_idx, f"{p}: pager must render above DataGrid")


if __name__ == "__main__":
    main(verbosity=2)
