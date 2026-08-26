"""DEC-210 — 도서별 판매 「내용 전체 보기」 (2026-08-26 09:25 사용자 요청).

체크하면 상단 도서 표가 **스크롤 없이 현재 페이지 행을 모두** 펼치고(뷰포트 상한·내부 스크롤 해제)
2단 분할은 해제되어 하단 거래처별 상세가 아래에 이어진다(페이지 스크롤). 재고현황/원장 화면과 같은 의미.
DataGrid 에 `unbounded` 모드를 두어 다른 DataGrid 화면도 같은 방식으로 붙일 수 있다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class DataGridUnbounded(TestCase):
    def test_prop_removes_height_cap_and_inner_scroll(self) -> None:
        src = _read("components/data-grid/data-grid.tsx")
        self.assertIn("unbounded?: boolean;", src)
        self.assertIn("unbounded = false,", src)
        # DEC-213 — unbounded 면 카드가 스크롤 컨테이너가 아니어야 th/tfoot sticky 가 페이지 스크롤에 붙는다
        self.assertIn('(unbounded\n            ? "w-full min-w-0 bg-card"', src)
        self.assertIn(": `${LIST_TABLE_SCROLL_CARD_CLASS} overflow-y-auto ` +", src)


class BookSalesShowAll(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/reports/book-sales/page.tsx")

    def test_checkbox_in_toolbar(self) -> None:
        self.assertIn('data-legacy-id="Sobo61.ShowAll"', self.src)
        self.assertIn("내용 전체 보기", self.src)

    def test_show_all_unbounds_top_grid_and_disables_split(self) -> None:
        self.assertIn('storageKey="reports.book-sales"\n        disabled={showAll}', self.src)
        self.assertIn("fillHeight={!showAll}\n        unbounded={showAll}", self.src)


if __name__ == "__main__":
    main()
