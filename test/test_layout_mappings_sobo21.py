"""Sobo21 layout-mapping data-legacy-id 회귀 가드 — DEC-064 §Idnum 정합 (2026-06-05).

거래명세서 모던 페이지(`page.tsx`) 가 레거시 dfm 위젯 ID 를 `data-legacy-id` 로 surface
하는지 정적으로 확인한다. ID 가 사라지면 layout-mapping 회귀로 즉시 차단.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = (
    ROOT
    / "도서물류관리프로그램"
    / "frontend"
    / "src"
    / "app"
    / "(app)"
    / "transactions"
    / "sales-statement"
    / "page.tsx"
)


# DEC-064 §Idnum 정합 + Sobo21 합성 매핑 — 모두 page.tsx 본문에 1회 이상 등장해야 한다.
REQUIRED_LEGACY_IDS = (
    "Sobo21.Panel001",
    "Sobo21.Panel101",
    "Sobo21.Edit101",
    "Sobo21.Edit102",
    "Sobo21.Edit103",            # Jubun (advanced — hidden by default)
    "Sobo21.Edit104",            # Gcode (advanced)
    "Sobo21.Edit105",            # 거래처명
    "Sobo21.Edit109",            # DEC-064 — 전표번호 입력 (Idnum 5자리)
    "Sobo21.dxButton1",
    "Sobo21.DBGrid101",
    "Sobo21.DBGrid101.GSQUT",
    "Sobo21.DBGrid101.GSSUM",
    "Sobo21.DBGrid101.YESNO",
    "Sobo21.DBGrid101.Lines",
    "Sobo21.DBGrid101.LineRow",
    "Sobo21.RightAside",
    "Sobo21.Layout.Main",
    "Sobo21.LineGrid.BookLookup",
    "Sobo21.Hint.IdnumPrimary",
    "Sobo21.Hint.MultiMatch",
    "Sobo21.Hint.ZeroMatch",
    "Sobo21.Hint.SingleMatch",
)


class Sobo21LayoutMappingTest(TestCase):
    def test_page_exists(self) -> None:
        self.assertTrue(PAGE_PATH.exists(), f"missing: {PAGE_PATH}")

    def test_required_legacy_ids_present(self) -> None:
        text = PAGE_PATH.read_text(encoding="utf-8")
        missing = [legacy_id for legacy_id in REQUIRED_LEGACY_IDS if legacy_id not in text]
        self.assertFalse(
            missing,
            f"Sobo21 page.tsx 에서 다음 data-legacy-id 누락: {missing}\n"
            "DEC-028 (data-legacy-id 의무) + DEC-064 §Idnum 정합 (Edit109) 회귀 차단.",
        )

    def test_idnum_input_uses_max_length_5(self) -> None:
        """Subu21 Edit109 5자리 — DEC-064 §Idnum 정합."""
        text = PAGE_PATH.read_text(encoding="utf-8")
        # Edit109 input 근처에 maxLength={5} 가 명시돼야 한다.
        self.assertIn("Sobo21.Edit109", text)
        # Edit103 (Jubun) 은 차수 2자리 backward-compat 으로 유지.
        self.assertIn("Sobo21.Edit103", text)

    def test_idnum_input_imports_format_helpers(self) -> None:
        text = PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("formatIdnumInput", text)
        self.assertIn("formatIdnumDisplay", text)

    def test_layout_two_column_with_sticky_right_aside(self) -> None:
        """좌·우 한 화면 + 우측 sticky — 거래처참조·메모 동시 노출."""
        text = PAGE_PATH.read_text(encoding="utf-8")
        # tailwind utilities 가 명시돼야 한다 (디자인 토큰 위반 0).
        self.assertIn("lg:grid-cols-[minmax(0,2fr)_minmax(360px,1fr)]", text)
        self.assertIn("lg:sticky", text)
        # 우측 패널은 두 카드(참조·메모) 모두 포함.
        self.assertIn("SalesStatementReferencePanel", text)
        self.assertIn("SalesStatementMemoPanel", text)

    def test_data_grid_keyboard_nav_enabled_for_list(self) -> None:
        """DataGrid opt-in 키보드 네비 — DEC-064 §7a."""
        text = PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("enableKeyboardNav", text)
        self.assertIn("onSelectedRowChange", text)

    def test_slip_no_does_not_fallback_to_jubun(self) -> None:
        """참조 패널 전표번호 — Idnum 만 표시, Jubun 폴백 금지 (DEC-064 §Idnum 상세수정)."""
        text = PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("detailSlipNo", text)
        self.assertIn("slipInternalHint", text)
        # 과거 회귀: selectedKey?.jubun 을 slipNo 로 쓰던 패턴.
        self.assertNotIn("selectedKey?.jubun ||", text)
        self.assertNotIn('selectedKey?.jubun ||\n              jubun', text)

    def test_single_result_auto_selects_detail(self) -> None:
        """거래처 검색 단건 — selectStatementRow 자동 호출."""
        text = PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("if (res.items.length === 1)", text)
        self.assertIn("await selectStatementRow(res.items[0])", text)


if __name__ == "__main__":
    from unittest import main

    main()
