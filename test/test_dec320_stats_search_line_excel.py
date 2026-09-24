"""DEC-320 — 통계관리 하위 화면 한 줄 검색 통일 + 모든 목록표 「엑셀 저장」 (2026-09-24)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

SRC = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"

# (화면, 한 줄 검색을 직접 쓰는가/공용 필터 바를 쓰는가, 목록표 수)
SCREENS = (
    ("app/(app)/reports/book-sales/page.tsx", "direct", 2),
    ("app/(app)/reports/customer-sales/page.tsx", "direct", 2),
    ("app/(app)/reports/year-end-book/page.tsx", "direct", 1),
    ("app/(app)/stats/monthly/page.tsx", "direct", 1),
    ("app/(app)/stats/customer/page.tsx", "direct", 1),
    ("app/(app)/stats/book/page.tsx", "direct", 1),
    ("app/(app)/stats/sales-period/page.tsx", "bar", 1),
    ("app/(app)/stats/customer-analysis/page.tsx", "bar", 1),
    ("app/(app)/stats/book-turnover/page.tsx", "bar", 1),
    ("app/(app)/stats/quarterly-summary/page.tsx", "bar", 2),
    ("app/(app)/stats/publisher/page.tsx", "bar", 1),
)


class StatsScreens(TestCase):
    def test_one_line_search_on_title_row(self) -> None:
        for rel, kind, _n in SCREENS:
            src = (SRC / rel).read_text(encoding="utf-8")
            self.assertIn("filtersBelow={false}", src, rel)
            if kind == "direct":
                self.assertIn("<LedgerSearchLine", src, rel)
                self.assertIn("<LedgerSearchButton", src, rel)
            else:
                header = src.split("<PageHeader")[1].split("</PageHeader>")[0]
                self.assertIn("<StatsFilterBar", header, f"{rel}: 필터 바는 제목 줄 안")

    def test_shared_filter_bar_uses_pills(self) -> None:
        bar = (SRC / "components" / "stats" / "stats-filter-bar.tsx").read_text(encoding="utf-8")
        for piece in ("<LedgerSearchLine", "<LedgerDatePill", "<LedgerSearchButton"):
            self.assertIn(piece, bar)
        stops = bar.split("const filterStopIds")[1].split("return ids")[0]
        self.assertLess(stops.index("Edit_DateFrom"), stops.index("Edit_GcodeFrom"), "Enter 순서 = 화면 순서")

    def test_every_list_table_has_excel_save(self) -> None:
        for rel, _kind, n in SCREENS:
            src = (SRC / rel).read_text(encoding="utf-8")
            self.assertGreaterEqual(src.count('"엑셀 저장"'), n, f"{rel}: 목록표마다 「엑셀 저장」")
            self.assertNotIn("엑셀 다운로드", src, f"{rel}: 라벨은 「엑셀 저장」으로 통일")


if __name__ == "__main__":
    main()
