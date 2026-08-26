"""DEC-220 — 입고명세서 하단 라인 표 DataGrid + 「내용 전체 보기」 (2026-08-27 사용자 지적)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "transactions" / "inbound-statement" / "page.tsx"


class InboundStatementLinesGrid(TestCase):
    def setUp(self) -> None:
        self.src = SRC.read_text(encoding="utf-8")

    def test_bottom_lines_are_data_grid(self) -> None:
        self.assertNotIn("<table", self.src)
        i = self.src.index('legacyId="Sobo22.DBGrid101"')
        block = self.src[self.src.rindex("<DataGrid<ReceiptLineDetail>", 0, i): self.src.index("/>", i)]
        for tok in ("sort={lineSort.sort}", "onSortChange=", "columnWidths=", "onColumnResize=", "onColumnReorder=", "totals=", "enableKeyboardNav"):
            self.assertIn(tok, block, tok)
        self.assertIn('"transactions.inbound-statement.lines"', self.src)
        self.assertIn("hidden={linePrefs.hidden}", self.src, "하단 표 컬럼 설정")
        for fld in ("PUBUN", "BCODE", "BNAME", "GSQUT", "GDANG", "GRAT1", "GSSUM", "GBIGO", "YESNO"):
            self.assertIn(f'legacyId: "Sobo22.DBGrid101.{fld}"', self.src, fld)

    def test_show_all_checkbox(self) -> None:
        self.assertIn('data-legacy-id="Sobo22.ShowAll"', self.src)
        self.assertIn("내용 전체 보기", self.src)
        self.assertIn("disabled={!selectedKey || showAll}", self.src, "전체 보기면 분할 해제")
        self.assertIn("fillHeight={!showAll}\n        unbounded={showAll}", self.src)


if __name__ == "__main__":
    main()
