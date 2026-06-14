"""C2 출고 접수 — 거래처 lookup 이 출판사가 아닌 G1 거래처 검색을 사용하는지 정적 회귀."""
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class OutboundCustomerLookupStaticTest(TestCase):
    def test_orders_list_uses_customer_lookup_with_hcode_apply(self) -> None:
        src = (FE / "app" / "(app)" / "outbound" / "orders" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn('lookupKind="customer"', src)
        self.assertIn("applyCustomerToHcode", src)
        self.assertNotIn('lookupKind="publisher"', src)

    def test_orders_new_uses_customer_lookup_with_hcode_apply(self) -> None:
        src = (FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn('lookupKind="customer"', src)
        self.assertIn("applyCustomerToHcode", src)
        self.assertNotIn('lookupKind="publisher"', src)

    def test_apply_customer_to_hcode_prefers_branch_hcode(self) -> None:
        apply_src = (FE / "lib" / "master-lookup-apply.ts").read_text(encoding="utf-8")
        self.assertIn("selection.hcode || selection.code", apply_src)


if __name__ == "__main__":
    main(verbosity=2)
