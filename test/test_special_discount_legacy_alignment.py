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

        DEC-412: 프론트 재설계 M-DEC-13/18/19 — 의도적 제거: 두 축 패널(PaneCustomer/PaneBook ·
        DBGrid201)과 MasterLookupField. 피그마 1:1351 목록 한 장(DBGrid101)에서 거래처·도서의 코드/명
        4기준으로 찾고, 신규/상세 폼에서 거래처(Edit101)·도서(Edit201)를 자동완성 콤보로 고른다.
        두 축 검색 의미(거래처로 찾기 / 도서로 찾기)는 검색 기준으로 남는다.
        """
        page = _read(FRONT / "app" / "(app)" / "master" / "special" / "page.tsx")
        chrome = _read(FRONT / "components" / "master" / "special-master-chrome.tsx")
        form = _read(FRONT / "components" / "master" / "special-detail-form.tsx")
        self.assertIn('legacyId="Sobo16.DBGrid101"', page)
        for col in ("GCODE", "GNAME", "BCODE", "BNAME", "GRAT1", "GSSUM"):
            self.assertIn(f'legacyId: "Sobo16.DBGrid101.{col}"', page, col)
        # 거래처축·도서축 검색 = 검색 기준 4개(코드/명)
        for fid in ('id: "gcode"', 'id: "gname"', 'id: "bcode"', 'id: "bname"'):
            self.assertIn(fid, chrome)
        self.assertIn("if (field === \"bcode\") return { bcode: text };", page)
        # 폼: 거래처·도서 자동완성 콤보(레거시 Edit101/Edit201) · 비율(Edit301) · 정가(Edit302)
        for lid in ("Sobo16.Edit101", "Sobo16.Edit201", "Sobo16.Edit301", "Sobo16.Edit302", "Sobo16.Panel002"):
            self.assertIn(lid, form, lid)
        self.assertIn('kind="customer"', form)
        self.assertIn('kind="book"', form)
        # 구 UI(모드 라디오·팝업 버튼)로의 회귀 차단.
        for old_kw in ("Sobo16.searchAxis.", "MasterLookupButton"):
            self.assertNotIn(old_kw, page)
            self.assertNotIn(old_kw, form)
