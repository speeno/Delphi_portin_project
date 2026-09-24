"""DEC-210 — 도서별 판매 「내용 전체 보기」 (2026-08-26 09:25 사용자 요청).

**DEC-288(2026-09-12)로 의미 재정의** — 체크하면 상단 목록에 보이는 **모든 도서**의 거래처별 내역이
하단에 함께 조회된다(상단 표를 펼치던 종전 동작은 폐기, 분할 유지). 화면 배선 가드는
`test_dec288_show_all_detail_extended.py` 로 이관하고, 여기서는 DataGrid `unbounded` 모드
자체(다른 화면이 여전히 쓰는 공용 prop)와 체크박스 존재만 지킨다.
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
        # 배경이 토큰(table-body)으로 바뀌었을 뿐 — unbounded 면 스크롤 컨테이너가 아니어야 한다.
        self.assertRegex(src, r'\(unbounded\n\s+\? "w-full min-w-0 bg-(card|table-body)"')
        self.assertIn(": `${LIST_TABLE_SCROLL_CARD_CLASS} overflow-y-auto ` +", src)


class BookSalesShowAll(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/reports/book-sales/page.tsx")

    def test_checkbox_in_toolbar(self) -> None:
        self.assertIn('data-legacy-id="Sobo61.ShowAll"', self.src)
        self.assertIn("내용 전체 보기", self.src)

    def test_show_all_loads_all_books_detail(self) -> None:
        """DEC-288 — 상단 펼치기(unbounded) 대신 하단 전 도서 상세."""
        # 2026-09 UI 통일 — 분할 제어가 `disabled={!showAll && <선택없음>}` 에서
        # `secondaryVisible={showAll || <선택있음>}` 으로 바뀌었다(전체 보기면 하단 전 건 상세,
        # 선택 없으면 분할 없이 상단만 — 동작 요구는 동일). 두 표현 중 하나면 통과.
        self.assertIn('storageKey="reports.book-sales"', self.src)
        # DEC-319(2026-09-24) — 하단(우측)은 항상 표시, 선택이 없거나 「내용 전체 보기」면 전 도서 상세.
        self.assertIn("const effectiveAll = showAll || detail === null;", self.src)
        self.assertNotIn("secondaryVisible=", self.src)
        self.assertNotIn("unbounded={showAll}", self.src)
        self.assertIn("bookSalesCustomersAll", self.src)


if __name__ == "__main__":
    main()
