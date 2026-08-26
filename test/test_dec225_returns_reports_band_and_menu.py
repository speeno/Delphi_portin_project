"""DEC-225 — 기간별 재고원장·반품내역서 띠 정합 + 반품재고관리(통합) 메뉴 제거 (2026-08-27)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "도서물류관리프로그램"
FRONT = PRODUCT / "frontend" / "src"


class ReportBandsInline(TestCase):
    def test_filters_are_contents_children_of_band(self) -> None:
        for rel, pid in (("returns/ledger", "Sobo34_4"), ("returns/period-report", "Sobo58")):
            src = (FRONT / "app" / "(app)" / rel / "page.tsx").read_text(encoding="utf-8")
            band = src[src.index("<PageHeader"): src.index("</PageHeader>")]
            self.assertIn(f'data-legacy-id="{pid}.Panel001" className="contents"', band, rel)
            self.assertNotIn('className="flex flex-wrap items-end gap-3"', band, rel)
            self.assertNotIn('<div className="flex items-end">', band, rel)


class IntegratedReturnsMenuRemoved(TestCase):
    def test_registry_page_and_rbac_sources(self) -> None:
        self.assertNotIn("MenuShippingReturnsInventory", (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8"))
        self.assertFalse((FRONT / "app" / "(app)" / "shipping" / "returns-inventory").exists())
        for rel in ("docs/onboarding-rbac-menu-matrix.md", "migration/contracts/rbac_menu_matrix.yaml", "analysis/rbac_menu_matrix.json"):
            self.assertNotIn("ACC-MENU-NAV-12", (ROOT / rel).read_text(encoding="utf-8"), rel)
        self.assertNotIn("NAV-12", (FRONT / "data" / "rbac_menu_matrix.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
