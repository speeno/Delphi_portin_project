"""DEC-319 — 통계 도서별판매·거래처별판매 「내용 전체 보기」 공통 동작 통일 (2026-09-24)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

APP = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"


def _read(rel: str) -> str:
    return (APP / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class StatsShowAll(TestCase):
    def test_both_keep_right_pane_and_offer_clear_selection(self) -> None:
        for rel in ("reports/book-sales/page.tsx", "reports/customer-sales/page.tsx"):
            src = _read(rel)
            self.assertNotIn("secondaryVisible=", src, f"{rel}: 우측 창은 항상 표시(열렸다 닫혔다 금지)")
            self.assertIn("선택 해제", src, rel)
            self.assertIn("내용 전체 보기", src, rel)

    def test_customer_sales_toolbar_is_above_panes_like_book_sales(self) -> None:
        src = _read("reports/customer-sales/page.tsx")
        before_split = src.split("<SplitListPanes")[0]
        self.assertIn('data-legacy-id="Sobo62.ShowAll"', before_split, "체크박스는 두 창 위 한 줄(표 도구줄 아님)")
        grid = src.split("<SplitListPanes")[1].split("bottom={")[0]
        self.assertNotIn("toolbarTop=", grid)

    def test_book_sales_defaults_to_all_after_search(self) -> None:
        src = _read("reports/book-sales/page.tsx")
        self.assertIn("const effectiveAll = showAll || detail === null;", src)
        self.assertIn("if (!effectiveAll || !sid || bcodes.length === 0) return;", src)


if __name__ == "__main__":
    main()
