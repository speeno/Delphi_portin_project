from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ShipmentTransactionsLookupApplyTest(TestCase):
    def test_shipment_filters_have_lookup_field(self) -> None:
        orders = _read(FRONT / "app" / "(app)" / "outbound" / "orders" / "page.tsx")
        # 출고현황은 `/outbound/status` 중복 스텁이 제거되고 `Sobo67_status`
        # (`/transactions/outbound-status`) 한 건으로 통합됐다(form-registry 주석).
        status = _read(
            FRONT / "components" / "transactions" / "transaction-status-screen.tsx"
        )
        receipts = _read(FRONT / "app" / "(app)" / "inbound" / "receipts" / "page.tsx")
        new_orders = _read(
            FRONT / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
        )
        new_receipts = _read(
            FRONT / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
        )

        for src in (orders, status, receipts, new_orders, new_receipts):
            self.assertIn("MasterLookupField", src)

        # 출고접수/출고현황 목록 필터 = 거래처(G1_Ggeo.Gcode) 룩업. 회사(Hcode) 격리는
        # 서버 enforce_hcode_isolation 이 강제하고(ACC-DATA-03), 화면은 그 안에서 거래처로
        # 좁힌다(applyCustomerToHcode 2026-06-20 회귀 주의 + DEC-137 Gcode=거래처 축).
        self.assertIn('lookupKind="customer"', orders)
        self.assertIn("applyCustomerToHcode", orders)
        self.assertIn('lookupKind="customer"', status)
        # receipts 출판사코드 필터 — 불필요 항목으로 제거 (R11)
        self.assertIn('lookupKind="inboundVendor"', receipts)
        self.assertIn('lookupKind="book"', new_receipts)

    def test_transactions_filters_have_lookup_field(self) -> None:
        pages = {
            "sales": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "sales-statement"
            / "page.tsx",
            "inbound_statement": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "inbound-statement"
            / "page.tsx",
            "status": FRONT / "app" / "(app)" / "transactions" / "status" / "page.tsx",
            "inbound_status": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "inbound-status"
            / "page.tsx",
            "verification": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "verification"
            / "page.tsx",
            "prod_statement": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "production"
            / "statement"
            / "page.tsx",
            "prod_status": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "production"
            / "status"
            / "page.tsx",
            "withholding": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "withholding"
            / "page.tsx",
            "author_history": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "author-history"
            / "page.tsx",
            "new_release": FRONT
            / "app"
            / "(app)"
            / "transactions"
            / "new-release"
            / "page.tsx",
            "other": FRONT / "app" / "(app)" / "transactions" / "other" / "page.tsx",
        }

        for src in (_read(path) for path in pages.values()):
            self.assertIn("MasterLookupField", src)

        self.assertIn('lookupKind="customer"', _read(pages["sales"]))
        self.assertIn("Sobo21.Edit104", _read(pages["sales"]))
        self.assertIn("Sobo21.Edit102", _read(pages["sales"]))
        self.assertIn('lookupKind="inboundVendor"', _read(pages["inbound_statement"]))
        self.assertIn('lookupKind="publisher"', _read(pages["status"]))
        self.assertIn('lookupKind="publisher"', _read(pages["verification"]))
        self.assertIn('lookupKind="customer"', _read(pages["prod_statement"]))
        self.assertIn('lookupKind="author"', _read(pages["withholding"]))
        self.assertIn('lookupKind="book"', _read(pages["new_release"]))

    def test_g7_filter_pages_do_not_use_customer_lookup_kind(self) -> None:
        # Sobo21 거래명세서는 Edit104=Gcode(거래처) — customer lookup 예외 (DEC-028 §3).
        # 출고접수(/outbound/orders)·출고현황(/transactions/outbound-status)도 거래처
        # (G1_Ggeo.Gcode) 필터가 정본이 되어(위 테스트 참조) G7(출판사) 룩업 대상에서 제외.
        g7_pages = [
            FRONT / "app" / "(app)" / "transactions" / "status" / "page.tsx",
            FRONT / "app" / "(app)" / "transactions" / "verification" / "page.tsx",
        ]
        for page in g7_pages:
            with self.subTest(page=page.name):
                self.assertNotIn('lookupKind="customer"', _read(page))
