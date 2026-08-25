"""DEC-197 — 거래처별판매 상단 합계 행 + 검색 직후 하단 = 전체 거래처 도서별.

레거시 엑셀 「통계관리_거래처판매(260824)」 대조(2026-07-24~08-24, 교문사 5019)에서 확인한
레거시 형상: 상단 DBGrid101 Footer(fvtSum) 합계 행, 하단 DBGrid201 은 검색 직후 **전체
거래처**의 도서별(T00=1)이고 거래처를 고르면 좁혀진다. 대조 결과 상단 140/140·하단 682/682
일치(차이 8건은 전부 export 이후 입력분).

사용자 요청 2026-08-25: "각각 레거시 화면처럼 하단에 합계가 보이도록".

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.models.inquiry import CustomerSalesResponse  # noqa: E402
from app.services import reports_service as rpt  # noqa: E402

S1_ROWS = [
    {"Hcode": "5019", "Gcode": "00001", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "", "Gdate": "2026.08.10", "Gsqut": 30, "Gssum": 834_090},
    {"Hcode": "5019", "Gcode": "00004", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "", "Gdate": "2026.08.11", "Gsqut": 57, "Gssum": 1_182_275},
    {"Hcode": "5019", "Gcode": "00004", "Scode": "X", "Gubun": "반품", "Pubun": "정품",
     "Gjisa": "", "Gdate": "2026.08.12", "Gsqut": -1, "Gssum": -21_250},
]
H1_ROWS = [{"Hcode": "5019", "Gcode": "00001", "Gubun": "입금", "Gdate": "2026.08.15", "Gssum": 85_629_320}]


def _patches():
    async def fake_exec(server_id, sql, params=()):
        if "FROM S1_Ssub" in sql:
            return S1_ROWS
        if "FROM H1_Ssub" in sql:
            return H1_ROWS
        return []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
        return []

    async def fake_class(server_id, hcode, rows, table="G1_Ggeo"):
        return None

    return (patch.object(rpt, "execute_query", fake_exec),
            patch.object(rpt, "in_clause_lookup", fake_in),
            patch.object(rpt, "_attach_customer_class_soft", fake_class))


class TopTotalsTests(IsolatedAsyncioTestCase):
    async def test_totals_cover_whole_result_not_page(self) -> None:
        p1, p2, p3 = _patches()
        with p1, p2, p3:
            res = await rpt.get_customer_sales(
                server_id="remote_1", hcode="5019", date_from="2026.07.24", date_to="2026.08.24",
                scope="X", limit=1, offset=0,
            )
        self.assertEqual(len(res["rows"]), 1, "페이지는 1행")
        t = res["totals"]
        # 합계는 페이지가 아니라 결과 전체(2거래처) 기준 — 레거시 Footer fvtSum.
        self.assertEqual(t["goqut"], 87)
        self.assertEqual(t["gbqut"], -1)
        self.assertEqual(t["gsusu"], 86)
        self.assertEqual(t["gjsum"], 85_629_320)
        self.assertEqual(t["gssum"], 834_090 + 1_182_275 - 21_250)
        self.assertEqual(set(t), {"goqut", "gosum", "gjqut", "gbqut", "gbsum", "gsusu", "gjsum", "gssum"})

    def test_response_model_carries_totals(self) -> None:
        self.assertIn("totals", CustomerSalesResponse.model_fields)


class BookSalesListTotalsTests(IsolatedAsyncioTestCase):
    """도서별판매 **목록** API 도 합계를 돌려준다 — 종전엔 일별(get_book_sales_daily)에만 있어
    화면 합계 행(totals={gridTotals})이 비어 있었다(2026-08-25 사용자 요청)."""

    async def test_book_sales_returns_totals_over_all_rows(self) -> None:
        rows = [
            {"Bcode": "0001", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "Gdate": "2026.08.01",
             "Gsqut": 3, "Gssum": 30_000},
            {"Bcode": "0002", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "Gdate": "2026.08.02",
             "Gsqut": 5, "Gssum": 50_000},
            {"Bcode": "0002", "Scode": "X", "Gubun": "반품", "Pubun": "정품", "Gdate": "2026.08.03",
             "Gsqut": -1, "Gssum": -10_000},
        ]

        async def fake_exec(server_id, sql, params=()):
            return rows if "FROM S1_Ssub" in sql else []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            return []

        with patch.object(rpt, "execute_query", fake_exec), patch.object(rpt, "in_clause_lookup", fake_in):
            res = await rpt.get_book_sales(
                server_id="remote_1", hcode="5019", date_from="2026.08.01", date_to="2026.08.24",
                limit=1, offset=0,
            )
        self.assertEqual(len(res["rows"]), 1, "페이지 1행")
        t = res["totals"]
        self.assertEqual(t["goqut"], 8, "합계는 전체 결과")
        self.assertEqual(t["gbqut"], -1)
        self.assertEqual(t["gosum"], 80_000)
        self.assertEqual(t["gbsum"], -10_000)
        self.assertEqual(set(t), set(rpt._BOOK_SALES_MEASURE_KEYS))


class AllCustomersDetailTests(IsolatedAsyncioTestCase):
    async def _sql(self, **kw):
        exec_mock = AsyncMock(return_value=[])
        with patch.object(rpt, "execute_query", new=exec_mock):
            await rpt.get_customer_sales_detail(
                server_id="srv", hcode="5019", date_from="2026-07-24", date_to="2026-08-24", **kw,
            )
        return exec_mock.await_args.args[1], exec_mock.await_args.args[2]

    async def test_omitted_gcode_means_all_customers(self) -> None:
        """레거시 T00=1 — 검색 직후 하단은 전체 거래처의 도서별(엑셀 「내용 전체」 시트)."""
        sql, params = await self._sql()
        self.assertNotIn("Gcode = %s", sql)
        self.assertNotIn("Gjisa", sql)
        self.assertIn("Hcode = %s", sql)

    async def test_gcode_narrows_to_customer(self) -> None:
        sql, params = await self._sql(gcode="00001")
        self.assertIn("Gcode = %s", sql)
        self.assertIn("00001", params)

    async def test_by_branch_without_gcode_has_no_branch_filter(self) -> None:
        sql, _ = await self._sql(by_branch=True)
        self.assertNotIn("Gjisa", sql)


class ScreenTests(TestCase):
    PAGE = FRONT / "app" / "(app)" / "reports" / "customer-sales" / "page.tsx"

    def test_top_grid_gets_totals_and_all_detail_after_search(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn("totals={topTotals}", src)
        self.assertIn("totals={detailTotals}", src)
        # 검색 직후 전체 거래처 도서별을 자동 조회(레거시 T00=1).
        self.assertIn("loadDetail(", src)
        self.assertIn("전체 거래처", src)


if __name__ == "__main__":
    main()
