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
        # 지사(Edit106)는 DEC-119(2026-07-21)로 네이티브 <select> → LocalComboField(픽 필드,
        # data-legacy-id 는 내부 input 에 `inputLegacyId` 로 보존) 전환 — 자유 입력 회귀 금지.
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("customerBranchList", src)
        self.assertIn('inputLegacyId="Sobo21.Edit106"', src)
        self.assertIn("LocalComboField", src)
        self.assertNotIn('placeholder="Gjisa 일치"', src)

    def test_list_page_shows_branch_load_error(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("formatApiError", src)
        self.assertIn("Sobo21.Edit106.Error", src)
        self.assertIn("setBranchError", src)
        self.assertIn("branchLoading", src)
        self.assertIn("Sobo21.Edit106.Loading", src)

    def test_customer_detail_has_branch_collapsible(self) -> None:
        # DEC-412: 프론트 재설계 M-DEC-4 — 의도적 제거(접이식 지점 패널): 지점(H2_Gbun) 관리는 상세 헤더
        # 「지점 관리」(레거시 Button007) → 팝업(CustomerBranchDialog). 거래명세서 지사 콤보가 읽는 같은 API.
        detail = _read(FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx")
        self.assertIn("<CustomerBranchDialog", detail)
        self.assertIn("onBranch={() => setBranchOpen(true)}", detail)
        form = _read(FRONT / "components" / "master" / "customer-detail-form.tsx")
        self.assertIn('data-legacy-id="Sobo11.Button007"', form)
        dialog = _read(FRONT / "components" / "master" / "customer-branch-dialog.tsx")
        for api in ("customerBranchList", "customerBranchCreate", "customerBranchUpdate", "customerBranchBulkDelete"):
            self.assertIn(f"masterApi.{api}", dialog, api)
        for lid in ("Seok10.Seok10", "Seok10.DBGrid101", "Seok10.BitBtn101", "Seok10.BitBtn102", "Seok10.Edit101"):
            self.assertIn(lid, dialog, lid)

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
        self.assertIn("_append_gjisa_filter_async", svc)
        self.assertIn("gjisa_search_variants", svc)
        self.assertIn("_append_jubun_filter", svc)
        self.assertIn("jubun_lookup_variants", svc)
        self.assertIn("Scode = 'X'", svc)
        self.assertIn("assert_sales_statement_search_allowed", svc)
        self.assertIn("_append_gcode_filter", svc)
        self.assertIn("compute_sales_statement_stock_qty", svc)
        self.assertIn("load_sales_statement_memo_preview", svc)
