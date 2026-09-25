"""
DEC-331 — 「년/월(통계)」 허브 메뉴 제거(사용자 2026-09-25). 사이드바에서만 감춘다.

- 레지스트리 엔트리·라우트(/year-month-stats)·ACC-MENU-NAV-07 은 보존(직접 링크·즐겨찾기·등가 매트릭스 불변, DEC-309 취지).
- 하위 세분화 판매 6종(DEC-329)은 통계관리 메뉴에 그대로.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class YearMonthHubHidden(TestCase):
    def setUp(self):
        self.reg = (FE / "lib" / "form-registry.ts").read_text(encoding="utf-8")

    def _entry(self, fid: str) -> str:
        m = re.search(r'\{\s*id: "' + re.escape(fid) + r'",.*?\n  \},', self.reg, re.S)
        self.assertIsNotNone(m, fid)
        return m.group(0)

    def test_hub_entry_kept_but_hidden(self):
        hub = self._entry("MenuYearMonthStats")
        # DEC-333 — 중복 플래그 sidebarHidden 을 기존 hiddenFromMenu(2026-09-04 규약)로 통합.
        self.assertIn("hiddenFromMenu: true", hub)
        self.assertIn("hiddenReason:", hub)
        self.assertIn('route: "/year-month-stats"', hub)
        self.assertTrue((FE / "app" / "(app)" / "year-month-stats" / "page.tsx").exists())

    def test_sub_screens_still_in_menu(self):
        for fid in ("Sobo79_1", "Sobo79_2", "Sobo79_3", "Sobo79_4", "Sobo73", "Sobo74"):
            e = self._entry(fid)
            self.assertIn('menuGroup: "statistics"', e)
            self.assertNotIn("hiddenFromMenu", e)

    def test_sidebar_filters_hidden(self):
        sb = (FE / "components" / "app-shell" / "sidebar.tsx").read_text(encoding="utf-8")
        self.assertIn("if (form.hiddenFromMenu) return false;", sb)
        self.assertNotIn("sidebarHidden", self.reg + sb)

    def test_publisher_stats_distributor_only(self):
        """DEC-333 — 출판사통계 메뉴는 물류사(총판) 계정에만."""
        e = self._entry("Sobo43_stats_route")
        self.assertIn("distributorOnly: true", e)
        sb = (FE / "components" / "app-shell" / "sidebar.tsx").read_text(encoding="utf-8")
        self.assertIn("if (form.distributorOnly && !isDistributor) return false;", sb)


if __name__ == "__main__":
    main(verbosity=2)
