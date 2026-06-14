"""전표번호(jubun) 단독 LIST — Subu21 자동채움 UX 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class JubunPrimaryListTest(IsolatedAsyncioTestCase):
    async def test_list_jubun_only_without_gcode_returns_rows(self) -> None:
        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl

        async def noop_assert(**_kwargs):
            return None

        old_assert = h2bl.assert_sales_statement_search_allowed
        h2bl.assert_sales_statement_search_allowed = noop_assert
        try:
            items, total = await transactions_service.list_sales_statements(
                server_id="remote_153",
                hcode="5019",
                date_from="2026-05-25",
                date_to="2026-06-04",
                jubun="11",
                gcode=None,
                limit=5,
                offset=0,
            )
        finally:
            h2bl.assert_sales_statement_search_allowed = old_assert

        self.assertGreater(total, 0)
        self.assertGreater(len(items), 0)
        self.assertEqual(items[0].get("order_key", {}).get("jubun"), "11")

    async def test_customer_preview_stock_uses_bcode(self) -> None:
        from app.services import transactions_service

        captured: list[tuple[str, str, str]] = []

        async def fake_stock(_server_id, *, bcode, hcode, ocode="B"):
            captured.append((bcode, hcode, ocode))
            return 42

        async def fake_profile(*_a, **_k):
            return {"gname": "테스트"}

        async def fake_memo(*_a, **_k):
            return {}

        old_stock = transactions_service.compute_sales_statement_stock_qty
        old_prof = transactions_service.fetch_g1_customer_profile
        old_memo = transactions_service.load_sales_statement_memo_preview
        transactions_service.compute_sales_statement_stock_qty = fake_stock
        transactions_service.fetch_g1_customer_profile = fake_profile
        transactions_service.load_sales_statement_memo_preview = fake_memo
        try:
            out = await transactions_service.get_sales_statement_customer_preview(
                server_id="remote_138",
                gcode="00004",
                date_from="2026-05-14",
                date_to="2026-05-14",
                hcode="5019",
                bcode="BK99",
                ocode="B",
                g1_fallback_hcodes=("5019",),
            )
        finally:
            transactions_service.compute_sales_statement_stock_qty = old_stock
            transactions_service.fetch_g1_customer_profile = old_prof
            transactions_service.load_sales_statement_memo_preview = old_memo

        self.assertEqual(captured, [("BK99", "5019", "B")])
        self.assertEqual(out.get("stock_qty"), 42)


if __name__ == "__main__":
    from unittest import main

    main()
