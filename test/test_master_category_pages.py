from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MasterCategoryPagesTest(TestCase):
    def test_customer_category_page(self) -> None:
        page = FRONT / "app" / "(app)" / "master" / "customer-category" / "page.tsx"
        self.assertTrue(page.exists(), str(page))
        src = _read(page)
        self.assertIn("CustomerCategoryCollapsible", src)
        self.assertIn("defaultOpen", src)

    def test_book_category_page(self) -> None:
        page = FRONT / "app" / "(app)" / "master" / "book-category" / "page.tsx"
        self.assertTrue(page.exists(), str(page))
        src = _read(page)
        self.assertIn("BookCategoryPanel", src)
        self.assertIn("MasterCategoryCollapsible", src)
        self.assertIn("Sobo14.Panel200", src)

    def test_baebon_page(self) -> None:
        page = FRONT / "app" / "(app)" / "master" / "baebon" / "page.tsx"
        self.assertTrue(page.exists(), str(page))
        src = _read(page)
        for kw in ("배본처관리", "masterApi.specialList", "masterApi.specialPatch"):
            self.assertIn(kw, src)

    def test_master_index_hides_unused_cards(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "master" / "page.tsx")
        for removed in ("출판사·출고거래처(마스터)", "도서코드(마스터)", "할인율(대표)"):
            self.assertNotIn(removed, src)
        for shown in ("거래처관리", "입고처관리", "저자관리", "도서관리", "기타거래처"):
            self.assertIn(shown, src)
        # 배본처관리(Sobo16_baebon)는 운영 요청으로 허브 카드에서 감춤 (2026-05).
        # route(/master/baebon)·페이지·API 는 유지하므로 카드 title 만 제거됐는지 검증.
        self.assertNotIn('title: "배본처관리"', src)

    def test_master_list_keys_are_not_gcode_only(self) -> None:
        customer_src = _read(FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx")
        self.assertIn("`${c.hcode || \"\"}:${c.gcode}", customer_src)
        self.assertIn("`${r.hcode || \"\"}:${r.gcode}", customer_src)

