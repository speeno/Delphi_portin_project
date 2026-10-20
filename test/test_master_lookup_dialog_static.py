from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MasterLookupDialogStaticTest(TestCase):
    def test_lookup_config_has_required_kinds(self) -> None:
        src = _read(FRONT / "lib" / "master-lookup-config.ts")
        for kind in ('customer', 'book', 'inboundVendor'):
            self.assertIn(f'{kind}: {{', src)
        self.assertIn("MASTER_LOOKUP_CONFIGS", src)
        self.assertIn("rowKey: (row, index)", src)
        self.assertIn(":${index}`", src)

    def test_dialog_contains_core_elements(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-lookup-dialog.tsx")
        for kw in ("DataGrid<MasterLookupRow>", "Input", "Button", 'event.key === "Escape"', "onSelect"):
            self.assertIn(kw, src)
        self.assertIn("CommonLookupDialog.SearchInput", src)
        self.assertIn("CommonLookupDialog.SelectButton", src)

    def test_dialog_has_mobile_responsive_classes(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-lookup-dialog.tsx")
        # DEC-110(2026-07-19 팝업 리사이즈) 이후 데스크톱 높이는 sm:h-[80vh]+sm:max-h-[92vh]
        # (+sm:resize) — 정확한 vh 값은 UI 조정 대상이라 max-h 유틸 존재만 가드한다.
        for cls in ("fixed inset-x-2 top-8 bottom-2", "sm:w-[min(960px,96vw)]", "overflow-auto"):
            self.assertIn(cls, src)
        self.assertRegex(src, r"sm:max-h-\[\d+vh\]")

    def test_master_lookup_field_exists(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-lookup-field.tsx")
        for kw in ("MasterLookupButton", "useInlineAutocomplete", "mastersApi.customers", "mastersApi.products"):
            self.assertIn(kw, src)

    def test_representative_pages_use_lookup_button(self) -> None:
        """DEC-412: 프론트 재설계 M-DEC-17 — 의도적 제거: 기초관리 목록(거래처·도서·입고처) 머리의 검색 팝업
        (MasterLookupButton). 피그마 머리의 검색 기준 선택 + 입력칸(MasterSearchQueryField · X 지우기)으로 찾는다.
        공용 팝업(MasterLookupDialog/Field)은 전표·현황 화면에서 그대로 쓴다(아래 테스트).
        """
        pages = {
            "customer": "components/master/customer-master-list-header.tsx",
            "book": "components/master/book-master-chrome.tsx",
            "inbound-vendor": "components/master/inbound-vendor-master-chrome.tsx",
        }
        for route, chrome_rel in pages.items():
            page = _read(FRONT / "app" / "(app)" / "master" / route / "page.tsx")
            self.assertNotIn("MasterLookupButton", page, route)
            self.assertRegex(page, r"<(Customer|Book|InboundVendor)MasterListHeader\b", route)
            chrome = _read(FRONT / chrome_rel)
            self.assertIn("<MasterSearchQueryField", chrome, chrome_rel)
            self.assertIn('aria-label="검색 기준"', chrome, chrome_rel)

    def test_shipment_transactions_pages_use_lookup_field(self) -> None:
        shipment_orders = _read(FRONT / "app" / "(app)" / "outbound" / "orders" / "page.tsx")
        tx_status = _read(FRONT / "app" / "(app)" / "transactions" / "status" / "page.tsx")
        tx_inbound = _read(FRONT / "app" / "(app)" / "transactions" / "inbound-statement" / "page.tsx")

        self.assertIn("MasterLookupField", shipment_orders)
        # 출고 목록 필터는 거래처(G1_Ggeo) 코드 기준 → customer lookup.
        # (회사 Hcode 격리는 서버 scope 가 강제; 팝업은 거래처 목록이어야 함 — 사용자 요청.)
        self.assertIn('lookupKind="customer"', shipment_orders)
        self.assertIn("applyCustomerToHcode", shipment_orders)

        self.assertIn("MasterLookupField", tx_status)
        self.assertIn('lookupKind="publisher"', tx_status)

        self.assertIn("MasterLookupField", tx_inbound)
        self.assertIn('lookupKind="inboundVendor"', tx_inbound)
