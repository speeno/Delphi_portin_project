"""DEC-343/344/345 — 도서별판매·거래처별판매 우측 표 (2026-09-30, 교문사 경리부 요청 문서).

- DEC-343 도서별판매: 검색 직후 우측(도서별 거래처 상세 내역)은 **공백** — 도서를 고른 뒤에만 채운다.
- DEC-344 도서별판매: 「내용 전체 보기」 = 그 쪽(100종)이 아니라 **검색 결과 전체** 도서의 거래처별 내역.
  (캡처: 좌측 합계 출고 15,325 인데 우측은 첫 쪽 100종의 420 부)
- DEC-345 거래처별판매: 우측 거래처명이 **다른 계정의 같은 코드** 이름으로 나오던 오류
  (3313: 좌 「한밭대[대전s]원각서점」 / 우 「대구)영남기술교육원」) + 검색칸에는 코드가 아니라 거래처명.
"""

import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from app.services import reports_service as rs

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


# ── DEC-343 ────────────────────────────────────────────────────────────────
class BookSalesRightPaneBlankAfterSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/reports/book-sales/page.tsx")

    def test_idle_state_shows_no_rows(self) -> None:
        self.assertIn("const detailIdle = !showAll && detail === null;", self.src)
        self.assertIn("detailIdle ? NO_DETAIL_ROWS : effectiveAll ? allRowsArr : detailRows", self.src)
        self.assertIn("왼쪽 목록에서 도서를 선택하면 그 도서의 거래처별 내역이 표시됩니다.", self.src)

    def test_all_books_detail_not_requested_unless_checked(self) -> None:
        effect = self.src.split("reportsApi.bookSalesCustomersAll(")[0].rsplit("useEffect(", 1)[1]
        self.assertIn("if (!effectiveAll ||", effect)
        self.assertIn("const effectiveAll = showAll;", self.src)

    def test_right_pane_opens_on_demand(self) -> None:
        # DEC-371 — 우측 창은 「내용 전체 보기」 또는 도서 선택 때만 연다(종전 «항상 표시» 철회).
        self.assertIn("secondaryVisible={showAll || detail !== null}", self.src)
        self.assertIn("선택 해제", self.src)


# ── DEC-344 ────────────────────────────────────────────────────────────────
class BookSalesShowAllCoversWholeResult(unittest.IsolatedAsyncioTestCase):
    ROWS = [
        {"Bcode": "B2", "Gcode": "C1", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gsqut": 7, "Gssum": 700},
        {"Bcode": "B1", "Gcode": "C2", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gsqut": 5, "Gssum": 500},
        {"Bcode": "B1", "Gcode": "C1", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gsqut": 10, "Gssum": 1000},
        {"Bcode": "B3", "Gcode": "C1", "Scode": "X", "Gubun": "반품", "Pubun": "반품", "Gsqut": -2, "Gssum": -200},
    ]

    async def _run(self, *, cap: int | None = None, **kw):
        seen: dict = {}

        async def fake_query(server_id, sql, params=()):
            seen["sql"], seen["params"] = sql, tuple(params)
            return self.ROWS

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            seen.setdefault("lookups", []).append(sql_template)
            if "G1_Ggeo" in sql_template:
                return [{"gcode": "C1", "gname": "거래처1"}, {"gcode": "C2", "gname": "거래처2"}]
            raise AssertionError("전체 모드는 도서코드 IN 조회를 쓰지 않는다")

        patches = [
            patch.object(rs, "execute_query", AsyncMock(side_effect=fake_query)),
            patch.object(rs, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)),
            patch.object(rs, "fetch_book_meta", AsyncMock(return_value={"B1": {"gname": "도서1"}})),
        ]
        if cap is not None:
            patches.append(patch.object(rs, "BOOK_SALES_CUSTOMERS_ALL_MAX", cap))
        for p in patches:
            p.start()
        try:
            res = await rs.get_book_sales_customers_all(
                server_id="remote_153", hcode="5019",
                date_from="2026-09-01", date_to="2026-09-29",
                bcodes=[], all_books=True, **kw,
            )
        finally:
            for p in patches:
                p.stop()
        return res, seen

    async def test_no_book_code_list_needed(self) -> None:
        res, seen = await self._run()
        self.assertNotIn("Bcode IN", seen["sql"])
        self.assertIn("GROUP BY Bcode, Gcode", seen["sql"])
        self.assertIn("Hcode = %s", seen["sql"], "계정 스코프 유지")
        self.assertEqual(seen["params"], ("2026.09.01", "2026.09.29", "5019"))
        self.assertEqual(res["books"], 3)
        self.assertEqual(res["total_rows"], 4)

    async def test_rows_sorted_by_book_then_customer(self) -> None:
        res, _ = await self._run()
        self.assertEqual(
            [(r["bcode"], r["gcode"]) for r in res["rows"]],
            [("B1", "C1"), ("B1", "C2"), ("B2", "C1"), ("B3", "C1")],
        )
        self.assertEqual(res["rows"][0]["gname"], "거래처1")
        self.assertEqual(res["rows"][0]["bname"], "도서1")

    async def test_totals_cover_whole_result_even_when_rows_are_capped(self) -> None:
        res, _ = await self._run(cap=2)
        self.assertTrue(res["truncated"])
        self.assertEqual(len(res["rows"]), 2)
        self.assertEqual(res["total_rows"], 4)
        self.assertEqual(res["books"], 3, "도서 수도 전체 기준")
        self.assertEqual(res["totals"]["goqut"], 22)   # 10 + 5 + 7 — 잘린 행 포함
        self.assertEqual(res["totals"]["gosum"], 2200)
        self.assertEqual(res["totals"]["gbqut"], -2)

    async def test_single_book_filter_follows_list_query(self) -> None:
        _, seen = await self._run(bcode="B1")
        self.assertIn("Bcode = %s", seen["sql"])
        self.assertEqual(seen["params"][-1], "B1")

    async def test_page_scoped_mode_unchanged(self) -> None:
        res = await rs.get_book_sales_customers_all(
            server_id="remote_153", hcode="5019",
            date_from="2026-09-01", date_to="2026-09-29", bcodes=[],
        )
        self.assertEqual(res, {"rows": [], "books": 0})


class BookSalesShowAllWiring(unittest.TestCase):
    def test_router_exposes_all_books(self) -> None:
        src = (BACK / "routers" / "reports.py").read_text(encoding="utf-8")
        block = src.split('@router.get("/book-sales/customers-all")')[1].split("@router.get(")[0]
        self.assertIn('alias="allBooks"', block)
        self.assertIn("all_books=all_books", block)
        self.assertIn("enforce_hcode_isolation(hcode, current)", block)

    def test_screen_asks_for_whole_result_with_search_snapshot(self) -> None:
        src = _read("app/(app)/reports/book-sales/page.tsx")
        call = src.split("reportsApi.bookSalesCustomersAll(")[1].split("});")[0]
        self.assertIn("allBooks: true", call)
        self.assertNotIn("bcodes", call, "그 쪽 도서코드 목록을 보내지 않는다")
        self.assertIn("dateFrom: snap.dateFrom", call, "목록을 조회한 조건 그대로")
        # 합계·도서 수·행 수는 서버(전체 기준)
        self.assertIn("effectiveAll && allMeta?.totals", src)
        self.assertIn("allMeta?.books", src)

    def test_probe_matrix_has_all_books_case(self) -> None:
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("reports.book_sales_customers_all_books", probe)


# ── DEC-345 ────────────────────────────────────────────────────────────────
class CustomerNamesAreAccountScoped(unittest.IsolatedAsyncioTestCase):
    MASTER = [
        {"hcode": "7001", "gcode": "3313", "gname": "대구)영남기술교육원"},   # 다른 계정
        {"hcode": "5019", "gcode": "3313", "gname": "한밭대[대전s]원각서점"},  # 자사
        {"hcode": "7001", "gcode": "4001", "gname": "타계정 거래처"},
        {"hcode": "", "gcode": "4001", "gname": "공용 거래처"},
        {"hcode": "7001", "gcode": "5005", "gname": "타계정 전용"},
    ]

    def test_own_row_wins_regardless_of_row_order(self) -> None:
        for rows in (self.MASTER, list(reversed(self.MASTER))):
            names = rs._pick_customer_names(rows, "5019")
            self.assertEqual(names["3313"], "한밭대[대전s]원각서점")

    def test_falls_back_to_shared_row_never_other_account(self) -> None:
        names = rs._pick_customer_names(self.MASTER, "5019")
        self.assertEqual(names["4001"], "공용 거래처")
        self.assertEqual(names["5005"], "", "다른 계정 이름은 쓰지 않는다")

    def test_without_account_ambiguous_names_stay_blank(self) -> None:
        names = rs._pick_customer_names(self.MASTER, None)
        self.assertEqual(names["3313"], "", "계정마다 이름이 다르면 임의로 고르지 않는다")
        self.assertEqual(names["5005"], "타계정 전용")

    async def test_books_all_uses_scoped_names(self) -> None:
        rows = [
            {"Gcode": "3313", "Gjisa": "", "Bcode": "B1", "Gubun": "출고", "Pubun": "",
             "Gsqut": 10, "Gssum": 1000},
        ]

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            if "G1_Ggeo" in sql_template:
                self.assertIn("Hcode AS hcode", sql_template, "계정 컬럼을 함께 읽어야 고를 수 있다")
                return self.MASTER
            if "G4_Book" in sql_template:
                return [{"bcode": "B1", "gname": "도서1"}]
            return rows

        with patch.object(rs, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)), \
             patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)):
            res = await rs.get_customer_sales_books_all(
                server_id="remote_153", hcode="5019",
                date_from="2026-01-01", date_to="2026-09-29", pairs=["3313|"],
            )
        self.assertEqual([r["gname"] for r in res["rows"]], ["한밭대[대전s]원각서점"])


class CustomerSearchFieldShowsName(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/reports/customer-sales/page.tsx")
        self.field = self.src.split('inputLegacyId="Sobo62.Edit103"')[0].rsplit("<MasterLookupField", 1)[1]

    def test_field_displays_name_and_keeps_code_as_query_key(self) -> None:
        self.assertIn("value={custQuery}", self.field)
        self.assertIn("setCustQuery(selection.name || code);", self.field)
        self.assertIn("setCustQuery(it.gname || code);", self.field)
        self.assertIn("gcode: eGcode.trim() || undefined", self.src, "조회 키는 코드")

    def test_confirmed_name_does_not_reopen_search(self) -> None:
        self.assertIn(
            'confirmed={gcode.trim() !== "" && custQuery.trim() !== "" && custQuery !== gcode}', self.field
        )

    def test_name_survives_reload_and_typed_code_resolves_to_name(self) -> None:
        self.assertIn("gname: eGname,", self.src)
        self.assertIn("snap.gname || snap.gcode", self.src)
        self.assertIn("res.rows.find((r) => r.gcode === eGcode.trim())?.gname", self.src)


# ── DEC-351 — 거래처별판매 우측 표도 도서별판매와 같은 규칙 ─────────────────────
class CustomerSalesRightPaneOnlyWhenSelected(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/reports/customer-sales/page.tsx")

    def test_blank_after_search_and_after_clear(self) -> None:
        self.assertNotIn("loadDetail(undefined", self.src, "선택 없이 «전체 거래처»를 부르지 않는다")
        load_body = self.src.split("async function load(")[1].split("async function loadDetail(")[0]
        self.assertIn("setDetail(null);", load_body)
        clear = self.src.split("선택 해제 = 우측을 다시 비운다")[1].split("선택 해제\n")[0]
        self.assertIn("setDetail(null);", clear)
        self.assertIn("왼쪽 목록에서 거래처를 선택하면 그 거래처의 도서별 내역이 표시됩니다.", self.src)

    def test_detail_requires_a_row(self) -> None:
        self.assertIn("row: CustomerSalesRow,\n", self.src)
        self.assertIn("gcode: row.gcode,", self.src)

    def test_show_all_asks_for_whole_result(self) -> None:
        call = self.src.split("reportsApi.customerSalesBooksAll(")[1].split("});")[0]
        self.assertIn("allCustomers: true", call)
        self.assertNotIn("pairs", call, "그 쪽 거래처 목록을 보내지 않는다")
        self.assertIn("dateFrom: snap.dateFrom", call, "목록을 조회한 조건 그대로")


class CustomerSalesBooksAllWholeResult(unittest.IsolatedAsyncioTestCase):
    ROWS = [
        {"Gcode": "C2", "Gjisa": "", "Bcode": "B1", "Gubun": "출고", "Pubun": "", "Gsqut": 5, "Gssum": 500},
        {"Gcode": "C1", "Gjisa": "", "Bcode": "B2", "Gubun": "출고", "Pubun": "", "Gsqut": 7, "Gssum": 700},
        {"Gcode": "C1", "Gjisa": "", "Bcode": "B1", "Gubun": "출고", "Pubun": "", "Gsqut": 10, "Gssum": 1000},
        {"Gcode": "C3", "Gjisa": "", "Bcode": "B1", "Gubun": "반품", "Pubun": "", "Gsqut": -2, "Gssum": -200},
    ]

    async def _run(self, *, cap: int | None = None, **kw):
        seen: dict = {}

        async def fake_query(server_id, sql, params=()):
            seen["sql"], seen["params"] = sql, tuple(params)
            return self.ROWS

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            if "G1_Ggeo" in sql_template:
                return [{"hcode": "5019", "gcode": "C1", "gname": "거래처1"}]
            if "G4_Book" in sql_template:
                return [{"bcode": "B1", "gname": "도서1"}]
            raise AssertionError("전체 모드는 거래처코드 IN 조회를 쓰지 않는다")

        patches = [
            patch.object(rs, "execute_query", AsyncMock(side_effect=fake_query)),
            patch.object(rs, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)),
            patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)),
        ]
        if cap is not None:
            patches.append(patch.object(rs, "BOOK_SALES_CUSTOMERS_ALL_MAX", cap))
        for p in patches:
            p.start()
        try:
            res = await rs.get_customer_sales_books_all(
                server_id="remote_153", hcode="5019",
                date_from="2026-08-30", date_to="2026-09-30",
                pairs=[], all_customers=True, **kw,
            )
        finally:
            for p in patches:
                p.stop()
        return res, seen

    async def test_no_customer_list_needed_and_scoped(self) -> None:
        res, seen = await self._run()
        self.assertNotIn("Gcode IN", seen["sql"])
        self.assertIn("Hcode = %s", seen["sql"], "계정 스코프 유지")
        self.assertIn("Scode = %s", seen["sql"], "목록과 같은 판매 구분")
        self.assertEqual(seen["params"], ("2026.08.30", "2026.09.30", "X", "5019"))
        self.assertEqual(res["customers"], 3)
        self.assertEqual(res["total_rows"], 4)
        self.assertEqual(
            [(r["gcode"], r["bcode"]) for r in res["rows"]],
            [("C1", "B1"), ("C1", "B2"), ("C2", "B1"), ("C3", "B1")],
        )
        self.assertEqual(res["rows"][0]["gname"], "거래처1")

    async def test_totals_cover_whole_result_even_when_capped(self) -> None:
        res, _ = await self._run(cap=2)
        self.assertTrue(res["truncated"])
        self.assertEqual(len(res["rows"]), 2)
        self.assertEqual(res["customers"], 3, "거래처 수도 전체 기준")
        self.assertEqual(res["totals"]["goqut"], 22)
        self.assertEqual(res["totals"]["gbqut"], -2)

    async def test_single_customer_filter_follows_list_query(self) -> None:
        _, seen = await self._run(gcode="C1")
        self.assertIn("Gcode = %s", seen["sql"])
        self.assertEqual(seen["params"][-1], "C1")

    async def test_page_scoped_mode_unchanged(self) -> None:
        res = await rs.get_customer_sales_books_all(
            server_id="remote_153", hcode="5019",
            date_from="2026-08-30", date_to="2026-09-30", pairs=[],
        )
        self.assertEqual(res, {"rows": [], "customers": 0, "totals": {}, "truncated": False})

    def test_router_and_probe(self) -> None:
        src = (BACK / "routers" / "reports.py").read_text(encoding="utf-8")
        block = src.split('@router.get("/customer-sales/books-all")')[1].split("@router.get(")[0]
        self.assertIn('alias="allCustomers"', block)
        self.assertIn("all_customers=all_customers", block)
        self.assertIn("enforce_hcode_isolation(hcode, current)", block)
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("reports.customer_sales_books_all_customers", probe)


if __name__ == "__main__":
    unittest.main()
