"""거래명세서 지사 콤보(Edit106) — FE·BE 정적 회귀."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SalesStatementBranchComboTest(TestCase):
    def test_list_page_uses_branch_select(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("customerBranchList", src)
        self.assertIn('data-legacy-id="Sobo21.Edit106"', src)
        self.assertIn("<select", src)
        self.assertNotIn('placeholder="Gjisa 일치"', src)

    def test_list_page_shows_branch_load_error(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("formatApiError", src)
        self.assertIn("Sobo21.Edit106.Error", src)
        self.assertIn("setBranchError", src)
        self.assertIn("branchLoading", src)
        self.assertIn("Sobo21.Edit106.Loading", src)

    def test_customer_detail_has_branch_collapsible(self) -> None:
        detail = _read(FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx")
        self.assertIn("CustomerBranchCollapsible", detail)
        self.assertIn("customer-branch-panel", _read(
            FRONT / "components" / "master" / "customer-branch-collapsible.tsx"
        ))

    def test_router_exposes_customer_branches(self) -> None:
        router = _read(BACKEND / "app" / "routers" / "masters.py")
        for token in (
            '"/customer/{gcode}/branches"',
            "list_customer_branches",
            "create_customer_branch",
            "update_customer_branch",
            "delete_customer_branch",
        ):
            self.assertIn(token, router)

    def test_list_sales_statements_filters_gjisa(self) -> None:
        svc = _read(BACKEND / "app" / "services" / "transactions_service.py")
        self.assertIn("_append_gjisa_filter", svc)
        self.assertIn("gjisa_lookup_variants", svc)
        self.assertIn("assert_sales_statement_search_allowed", svc)
        self.assertIn("_append_gcode_filter", svc)
        self.assertIn("compute_sales_statement_stock_qty", svc)
        self.assertIn("load_sales_statement_memo_preview", svc)
