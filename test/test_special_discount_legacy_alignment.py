from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SpecialDiscountLegacyAlignmentTest(TestCase):
    def test_discount_caps_uses_sobo39(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "master" / "discount" / "page.tsx")
        self.assertIn('useScreenCaps("Sobo39")', src)
        self.assertIn("normalizeVariant", src)
        self.assertIn('searchParams.get("type")', src)
        self.assertIn("Sobo39.SearchStatus", src)

    def test_special_has_two_search_axes_and_lookup_buttons(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "master" / "special" / "page.tsx")
        for kw in (
            "Sobo16.searchAxis.customer",
            "Sobo16.searchAxis.book",
            "Sobo16.LookupHcode",
            "Sobo16.LookupGcode",
            "Sobo16.LookupBcode",
            "MasterLookupButton",
        ):
            self.assertIn(kw, src)
