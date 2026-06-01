"""거래명세서 목록 — 참조·메모 패널·customer-preview 회귀."""

from __future__ import annotations

from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys_path_added = False


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SalesStatementListPanelsStaticTest(TestCase):
    def test_list_page_has_bottom_panels(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("SalesStatementReferencePanel", src)
        self.assertIn("SalesStatementMemoPanel", src)
        self.assertIn("loadCustomerPreview", src)
        self.assertIn("selectStatementRow", src)
        self.assertIn("Sobo21.Link.Detail", src)
        self.assertIn("refError", src)
        self.assertIn("memoPreview", src)

    def test_shared_panel_components_exist(self) -> None:
        ref = _read(FRONT / "components" / "transactions" / "sales-statement-reference-panel.tsx")
        self.assertIn("Sobo21.Label104", ref)
        self.assertIn("Sobo21.Edit203", ref)
        self.assertIn("memoPreview", ref)
        self.assertIn("Sobo21.Panel007.Error", ref)
        self.assertIn(
            "Sobo21.Button801",
            _read(FRONT / "components" / "transactions" / "sales-statement-memo-panel.tsx"),
        )

    def test_router_customer_preview_before_detail(self) -> None:
        router = _read(BACKEND / "app" / "routers" / "transactions.py")
        prev = router.find("/sales-statement/customer-preview")
        detail = router.find('"/sales-statement/{order_key}"')
        self.assertGreater(prev, 0)
        self.assertGreater(detail, 0)
        self.assertLess(prev, detail)
        fn = router[prev : prev + 800]
        self.assertIn("jubun", fn)

    def test_inquiry_api_memo_preview(self) -> None:
        src = _read(FRONT / "lib" / "inquiry-api.ts")
        self.assertIn("memo_preview", src)
        self.assertIn("jubun:", src)


class SalesStatementStockQtyTest(IsolatedAsyncioTestCase):
    async def test_compute_stock_uses_gcode_in(self) -> None:
        import sys

        global sys_path_added
        if not sys_path_added:
            sys.path.insert(0, str(BACKEND))
            sys_path_added = True

        from app.services import transactions_service

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            return [{"stock_qty": 694}]

        old = transactions_service.execute_query
        transactions_service.execute_query = fake_query
        try:
            qty = await transactions_service.compute_sales_statement_stock_qty(
                "remote_138",
                gcode="00001",
                date_from="2026-01-01",
                date_to="2026-01-31",
                gjisa="01|광화문점",
            )
        finally:
            transactions_service.execute_query = old

        self.assertEqual(qty, 694)
        sql, params = captured[0]
        self.assertIn("Gcode IN", sql)
        self.assertIn("COALESCE(Gjisa,'') IN", sql)
        self.assertIn("00001", params)

    async def test_list_sales_statements_gcode_in_filter(self) -> None:
        import sys

        if str(BACKEND) not in sys.path:
            sys.path.insert(0, str(BACKEND))

        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "COUNT" in sql or "row_count" in sql.lower():
                return [{"row_count": 0}]
            return []

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        transactions_service.execute_query = fake_query

        async def fake_count(*_a, **_k):
            return 0

        transactions_service.count_grouped = fake_count
        old_assert = h2bl.assert_sales_statement_search_allowed
        h2bl.assert_sales_statement_search_allowed = noop_assert
        try:
            await transactions_service.list_sales_statements(
                server_id="remote_138",
                date_from="2026-01-01",
                date_to="2026-01-31",
                gcode="00001",
                gjisa="2|부곡리(매장)",
                limit=10,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            h2bl.assert_sales_statement_search_allowed = old_assert

        list_sql = next(
            (s for s, _ in captured if "FROM S1_Ssub" in s and "GROUP BY" in s),
            "",
        )
        self.assertIn("Gcode IN", list_sql)
        self.assertIn("COALESCE(Gjisa,'') IN", list_sql)
