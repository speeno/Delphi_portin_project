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
        """특별관리 = 거래처축/도서축 두 패널 동시 표시 + 인라인 자동완성 조회.

        DEC-155(2026-08-13)·DEC-170/171(2026-08-18) 재작성 이후 정본: 모드 라디오
        (`Sobo16.searchAxis.*`)와 팝업 버튼(`Sobo16.Lookup*` / MasterLookupButton) 은
        제거되고, 레거시 Subu16 원형대로 상단=거래처축(`PaneCustomer`/`Edit101`/`DBGrid101`)
        · 하단=도서축(`PaneBook`/`Edit201`/`DBGrid201`) 두 패널 + MasterLookupField
        (인라인 자동완성·빈값 Enter 통과) 로 조회한다.
        """
        src = _read(FRONT / "app" / "(app)" / "master" / "special" / "page.tsx")
        for kw in (
            "Sobo16.PaneCustomer",
            "Sobo16.PaneBook",
            "Sobo16.Edit101",
            "Sobo16.Edit201",
            "Sobo16.DBGrid101",
            "Sobo16.DBGrid201",
            "MasterLookupField",
        ):
            self.assertIn(kw, src)
        # 구 UI(모드 라디오·팝업 버튼)로의 회귀 차단.
        for old_kw in ("Sobo16.searchAxis.", "MasterLookupButton"):
            self.assertNotIn(old_kw, src)
