"""DEC-313 — 도서별수불원장: 도서명 우선 표시·정가/ISBN 정돈·판매부수·엑셀 전 컬럼(=화면 모양) (2026-09-24)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

FRONT = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class BookLedgerPage(TestCase):
    def setUp(self) -> None:
        self.src = (FRONT / "app" / "(app)" / "inventory" / "ledger" / "page.tsx").read_text("utf-8").replace("\r\n", "\n")

    def test_sale_qty_column_after_returns_in_both_grids(self) -> None:
        self.assertIn("(r.out_qty || 0) + (r.rtn_qty || 0)", self.src, "판매부수 = 출고 + 반품(음수)")
        for name in ("const TOP_COLUMNS", "const DETAIL_COLUMNS"):
            block = self.src.split(name)[1].split("];")[0]
            self.assertLess(block.index('label: "반품"'), block.index('label: "판매부수"'), name)
        self.assertIn("sale_qty: saleQty(data.totals)", self.src, "합계에도 판매부수")

    def test_search_box_shows_book_name(self) -> None:
        self.assertIn("value={bookQuery}", self.src)
        self.assertIn("setBookQuery(sel.name || sel.code);", self.src)
        self.assertIn("setBookQuery(it.gname || it.bcode);", self.src)

    def test_price_isbn_in_section_header(self) -> None:
        self.assertIn('data-legacy-id="Sobo32.BookInfo"', self.src)
        for label in ('label: "코드"', 'label: "정가"', 'label: "ISBN"', 'label: "기간"'):
            self.assertIn(label, self.src)

    def test_excel_exports_all_columns_like_screen(self) -> None:
        self.assertIn("topPrefs.orderColumns(TOP_COLUMNS)", self.src, "숨긴 칸 포함 전 컬럼")
        self.assertIn("detailPrefs.orderColumns(DETAIL_COLUMNS)", self.src)
        self.assertIn("screenLikeExport(columns, rows,", self.src, "본문만 빈칸 처리")
        self.assertIn('rows: totals ? [...xRows, { ...totals, [columns[0].key]: "합계" }] : xRows', self.src,
                      "합계 행은 화면처럼 0 도 표시")
        self.assertIn("도서별수불원장_${fileBook}", self.src, "파일명 도서명 우선")


class SharedHelper(TestCase):
    def test_screen_like_export_helper(self) -> None:
        src = (FRONT / "lib" / "table-export.ts").read_text("utf-8")
        self.assertIn("export function screenLikeExport(", src)
        self.assertIn('numFmt: "#,##0"', src)


if __name__ == "__main__":
    main()
