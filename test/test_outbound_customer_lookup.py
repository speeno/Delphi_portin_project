"""C2 출고 접수 — 거래처 lookup 종류 정적 회귀.

- orders/page.tsx (목록 필터): S1_Ssub.Hcode = G7_Ggeo 출판사 코드 → publisher lookup.
- orders/new/page.tsx (신규 등록): G1 거래처 선택 후 applyCustomerToHcode 로
  거래처의 부모 Hcode(출판사 코드)를 폼에 주입 → customer lookup.
"""
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class OutboundCustomerLookupStaticTest(TestCase):
    def test_orders_list_uses_customer_lookup(self) -> None:
        """출고 목록 거래처 필터는 G1_Ggeo(거래처) 코드 기준 → customer lookup 사용.

        2026-06-20 모델 정합: S1_Ssub.Hcode=회사(로그인 scope), Gcode=거래처. 목록은
        거래처(Gcode)로 좁히므로 검색 팝업도 거래처관리(G1_Ggeo) lookup 이어야 한다
        (직전엔 publisher lookup 이라 로그인 출판사 1건만 노출되던 회귀).
        """
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

    def test_apply_customer_to_hcode_prefers_customer_code(self) -> None:
        # 회귀(2026-06-20): customerList(G1_Ggeo)의 selection.hcode 는 소유 계정(로그인
        # hcode)이라, 이를 우선하면 어떤 거래처를 골라도 로그인 hcode 가 들어갔다.
        # 거래처 코드(selection.code = G1_Ggeo.Gcode)를 우선해야 한다.
        apply_src = (FE / "lib" / "master-lookup-apply.ts").read_text(encoding="utf-8")
        self.assertIn("selection.code || selection.hcode", apply_src)
        self.assertNotIn("selection.hcode || selection.code", apply_src)


if __name__ == "__main__":
    main(verbosity=2)
