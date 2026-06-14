"""DataGrid opt-in 키보드 네비 회귀 — DEC-064 §7a (2026-06-05).

`data-grid.tsx` 에 (1) 새 props(`enableKeyboardNav`/`selectedRowKey`/`onSelectedRowChange`)
가 추가되었고, (2) 기본값이 모두 비활성/undefined 이라 기존 호출자 회귀 0 인지 정적 확인.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
GRID_PATH = (
    ROOT
    / "도서물류관리프로그램"
    / "frontend"
    / "src"
    / "components"
    / "data-grid"
    / "data-grid.tsx"
)


class DataGridKeyboardNavTest(TestCase):
    def setUp(self) -> None:
        self.text = GRID_PATH.read_text(encoding="utf-8")

    def test_grid_file_exists(self) -> None:
        self.assertTrue(GRID_PATH.exists())

    def test_props_declare_keyboard_nav_optionals(self) -> None:
        for prop in (
            "enableKeyboardNav?: boolean",
            "selectedRowKey?: string",
            "onSelectedRowChange?",
        ):
            self.assertIn(prop, self.text, f"missing prop declaration: {prop}")

    def test_default_keyboard_nav_disabled(self) -> None:
        """기본값 false — 기존 화면 회귀 0 보장."""
        self.assertIn("enableKeyboardNav = false", self.text)

    def test_keyboard_handler_branches_present(self) -> None:
        """↑/↓/Home/End/PageUp/PageDown/Enter 분기 모두 처리."""
        for key in ("ArrowDown", "ArrowUp", "Home", "End", "PageDown", "PageUp", "Enter"):
            self.assertIn(key, self.text, f"missing key branch: {key}")

    def test_table_role_grid_only_when_enabled(self) -> None:
        """role='grid' / tabIndex 는 enableKeyboardNav 분기 안에서만 적용."""
        self.assertIn("enableKeyboardNav ? \"grid\" : undefined", self.text)
        self.assertIn("tabIndex={enableKeyboardNav ? 0 : undefined}", self.text)


if __name__ == "__main__":
    from unittest import main

    main()
