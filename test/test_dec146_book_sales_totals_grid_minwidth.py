"""DEC-146 — 도서별판매 전체 결과 합계 + DataGrid 컬럼 최소폭·합계행 회귀 가드.

2026-08-13 사용자 보고 3건:
- 도서별판매 "합계가 나올 수 있을까요?" → 합계는 **전체 검색 결과**(페이지·상한
  무관) 기준으로 서버 계산(get_book_sales_daily totals) 후 tfoot 합계행 표시.
- 2분할 화면에서 컬럼 과압축 — 헤더가 한 글자씩 세로로 꺾이고 숫자가 표 밖으로
  넘침 → DataGrid 공통 컬럼 최소폭 + 카드 가로 스크롤.
- 거래처판매 우측 상세 패널 — 행 선택 시에만 표시(평소 목록 전체 폭).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import reports_service as rpt  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

S1_DAILY_ROWS = [
    {"Gdate": "2026.07.20", "Bcode": "91184", "Scode": "X", "Gubun": "출고",
     "Pubun": "위탁", "Gsqut": 1, "Gssum": 33440},
    {"Gdate": "2026.07.22", "Bcode": "91184", "Scode": "X", "Gubun": "출고",
     "Pubun": "위탁", "Gsqut": 14, "Gssum": 468160},
    {"Gdate": "2026.07.23", "Bcode": "91184", "Scode": "X", "Gubun": "반품",
     "Pubun": "정품", "Gsqut": -2, "Gssum": -66880},
]


class BookSalesDailyTotalsTests(IsolatedAsyncioTestCase):
    async def _run(self, **kw):
        async def fake_exec(server_id, sql, params=()):
            if "FROM S1_Ssub" in sql:
                return S1_DAILY_ROWS
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            return []

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            return await rpt.get_book_sales_daily(
                server_id="remote_1", hcode="5019",
                date_from="2026.07.11", date_to="2026.08.11", **kw,
            )

    async def test_totals_cover_all_rows_not_just_page(self) -> None:
        # limit=1 로 1행만 페이징해도 합계는 전체 3행(일자 3개) 기준.
        res = await self._run(limit=1, offset=0)
        self.assertEqual(len(res["rows"]), 1)
        t = res["totals"]
        self.assertEqual(t["goqut"], 15, "출고수 = 1 + 14 (전체)")
        self.assertEqual(t["gosum"], 501600)
        self.assertEqual(t["gbqut"], -2, "반품수 음수 관례 그대로")
        self.assertEqual(t["gbsum"], -66880)

    async def test_totals_keys_match_measure_whitelist(self) -> None:
        res = await self._run()
        self.assertEqual(
            set(res["totals"].keys()), set(rpt._BOOK_SALES_MEASURE_KEYS),
            "합계는 흐름 측정치만 — 재고 3종·정가 미포함",
        )


class ResponseModelGuard(TestCase):
    def test_book_sales_response_carries_totals(self) -> None:
        from app.models.inquiry import BookSalesResponse, BookSalesTotals

        fields = BookSalesResponse.model_fields
        self.assertIn("totals", fields)
        t = BookSalesTotals(goqut=15, gosum=501600)
        self.assertEqual(t.goqut, 15)
        self.assertEqual(t.giqut, 0, "미지정 측정치 0 기본값")


class DataGridMinWidthAndTotalsGuard(TestCase):
    GRID = FRONTEND / "components" / "data-grid" / "data-grid.tsx"

    def test_table_enforces_min_width_for_horizontal_scroll(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("tableMinWidth", src)
        self.assertIn("minWidth: tableMinWidth", src, "표 최소폭 → 카드 가로 스크롤")
        self.assertNotIn(
            '"w-full min-w-0 table-fixed', src,
            "min-w-0 테이블은 최소폭을 무력화해 컬럼 과압축을 재발시킨다",
        )

    def test_totals_footer_row_supported(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("<tfoot>", src)
        self.assertIn("totals?", src)
        self.assertIn("totalsLabel", src)


class ScreenWiringGuard(TestCase):
    def test_book_sales_page_passes_totals(self) -> None:
        src = (FRONTEND / "app" / "(app)" / "reports" / "book-sales"
               / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("totals={gridTotals}", src)
        # 파생 합계 = 행과 동일식 (반품 음수 관례라 합산=차감).
        self.assertIn("totals.goqut + totals.gbqut", src)
        self.assertIn("totals.gosum + totals.gbsum", src)

    def test_customer_sales_detail_panel_renders_only_when_selected(self) -> None:
        src = (FRONTEND / "app" / "(app)" / "reports" / "customer-sales"
               / "page.tsx").read_text(encoding="utf-8")
        panel_at = src.index('data-legacy-id="Sobo62.DBGrid201"')
        guard_at = src.rindex("selectedKey !== null && (", 0, panel_at)
        self.assertGreater(guard_at, 0, "상세 패널은 행 선택 시에만 렌더")
        self.assertNotIn("좌측 거래처 행을 선택하면", src, "빈 안내 패널 제거")


if __name__ == "__main__":
    main()
