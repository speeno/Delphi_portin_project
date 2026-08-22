"""검색 팝업 자동 선택 제거 회귀 — 2026-08-22 사용자 요청.

요청 원문
--------
"검색을 위한 다양한 팝업 창이 뜬다. 이때 사용자가 명시적으로 항목 선택을 하지 않고
초기에 자동으로 선택되어 있어서 사용자가 무의식적으로 엔터를 입력하면 무조건 첫번째
검색 항목이 입력이 된다. 사용자는 팝업상태에서 명시적으로 키보드나 값을 입력해서 항목
선택을 하지 않은 경우 엔터를 처도 자동 선택이 되지 않도록 해달라"

정합
----
- `master-lookup-dialog` 는 검색 직후 첫 행(rows[0])을 자동 강조했고, 같은 키워드로
  Enter 를 다시 치면 그 행을 확정했다 → 검색만 하려던 Enter 가 1번째 결과를 입력.
- 이제 자동 강조는 **정확 코드 일치 행**에만 남긴다(DEC-134 — 전체 코드를 입력한
  사용자의 Enter 1회 확정은 "값을 입력해서 선택한" 명시적 행동이므로 유지).
- 그 외 팝업/자동완성은 원래부터 미선택(-1) 시작 — 회귀로 굳힌다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
DIALOG = SRC / "components" / "master" / "master-lookup-dialog.tsx"
FIELD = SRC / "components" / "master" / "master-lookup-field.tsx"
SLIP_DIALOG = SRC / "components" / "transactions" / "sales-statement-search-dialog.tsx"
GRID = SRC / "components" / "data-grid" / "data-grid.tsx"


class LookupDialogAutoSelectTests(TestCase):
    def setUp(self) -> None:
        self.src = DIALOG.read_text(encoding="utf-8")

    def test_no_first_row_fallback_after_search(self) -> None:
        """검색 결과의 첫 행을 자동 선택하는 폴백이 없어야 한다."""
        # 종전 코드: const initIdx = exactIdx >= 0 ? exactIdx : 0;
        self.assertNotIn("exactIdx >= 0 ? exactIdx : 0", self.src)
        self.assertNotIn("res.rows.length > 0 ? config.rowKey(res.rows[initIdx]", self.src)

    def test_selection_only_on_exact_code_match(self) -> None:
        """자동 선택은 정확 코드 일치일 때만 — 아니면 빈 문자열(미선택)."""
        m = re.search(
            r"const exactIdx = res\.rows\.findIndex\([\s\S]{0,220}?"
            r"setSelectedKey\(\s*([\s\S]{0,160}?)\);",
            self.src,
        )
        self.assertIsNotNone(m, "검색 후 setSelectedKey 블록을 찾지 못했다")
        expr = m.group(1)
        self.assertIn("exactIdx >= 0", expr, "정확 일치 조건이 사라졌다")
        self.assertIn('""', expr, "미일치 시 선택 해제('')가 되어야 한다")

    def test_arrow_down_still_selects_explicitly(self) -> None:
        """↓ 는 명시적 행동 — 첫 행 선택 + 그리드 진입을 유지한다."""
        self.assertIn('if (e.key === "ArrowDown")', self.src)
        self.assertIn("setSelectedKey(config.rowKey(rows[0], 0))", self.src)

    def test_enter_confirm_requires_a_selected_row(self) -> None:
        """같은 키워드 재-Enter 확정은 selectedRow 가 있을 때만."""
        self.assertIn("term === lastTermRef.current && selectedRow", self.src)


class OtherPopupsStartUnselectedTests(TestCase):
    """다른 검색 UI 는 원래 미선택 시작 — 회귀 방지로 고정."""

    def test_inline_autocomplete_starts_unselected(self) -> None:
        src = FIELD.read_text(encoding="utf-8")
        self.assertIn("useState(-1)", src, "activeIdx 는 -1(미선택) 로 시작해야 한다")
        self.assertIn("activeIdx >= 0 && activeIdx < inlineItems.length", src)

    def test_slip_search_dialog_starts_unselected(self) -> None:
        src = SLIP_DIALOG.read_text(encoding="utf-8")
        self.assertIn("useState(-1)", src)
        self.assertIn('e.key === "Enter" && selectedIdx >= 0', src)

    def test_data_grid_has_no_row_when_key_empty(self) -> None:
        """selectedRowKey 가 비면 강조 행 없음(-1) — 팝업 미선택 상태가 시각적으로도 유지."""
        src = GRID.read_text(encoding="utf-8")
        self.assertIn("if (!enableKeyboardNav || !selectedRowKey) return -1;", src)


if __name__ == "__main__":
    main()
