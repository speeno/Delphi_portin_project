"""DEC-323 — 도서별년말집계: 검색 통일·SCode/집계 단위/하단 상세 제거·컬럼명 통일·엑셀 전 필드 (2026-09-24)."""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

from app.routers.reports import _YEAR_END_DERIVED_FIELDS
from app.services.reports_service import _YEAR_END_BOOK_SORT_KEYS

PAGE = (Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
        / "reports" / "year-end-book" / "page.tsx")


class YearEndBookPage(TestCase):
    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")

    def test_columns_in_requested_order(self) -> None:
        block = self.src.split("const columns: DataGridColumn<YearEndBookGridRow>[]")[1].split("],\n    [],")[0]
        labels = re.findall(r'label: "([^"]+)"', block)
        self.assertEqual(labels, ["년도", "코드", "도서명", "ISBN", "정가", "입고수량", "출고수량", "증정수량",
                                  "반품수량", "판매수량", "출고금액", "반품금액", "판매금액"])
        self.assertIn('"reports.year-end-book.v2"', self.src, "종전 숨김/순서 저장을 잇지 않음(전 컬럼 기본 표시)")

    def test_removed_controls(self) -> None:
        for gone in ("Sobo67.CheckBox2", "Sobo67.GrainGroup", "drillDown", "년도 표로", "Sobo67.Edit105\""):
            self.assertNotIn(gone, self.src, gone)

    def test_excel_saves_all_fields(self) -> None:
        self.assertIn("const allColumns = useMemo(() => gridPrefs.orderColumns(columns)", self.src)
        self.assertIn("columns: allColumns.map(", self.src)


class YearEndBookBackend(TestCase):
    def test_sale_fields_sort_and_export(self) -> None:
        self.assertIn("sale_qty", _YEAR_END_BOOK_SORT_KEYS)
        self.assertIn("sale_amt", _YEAR_END_BOOK_SORT_KEYS)
        r = {"goqut": 10, "gbqut": -3, "gosum": 1000, "gbsum": -300}
        self.assertEqual(_YEAR_END_DERIVED_FIELDS["sale_qty"](r), 7)
        self.assertEqual(_YEAR_END_DERIVED_FIELDS["sale_amt"](r), 700)


if __name__ == "__main__":
    main()
