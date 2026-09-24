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

    def test_list_controls_live_in_each_table_header(self) -> None:
        # DEC-321(2026-09-24 「어떤 엑셀저장인지 보기 어렵다」) — 두 창 위 공용 줄 대신 **표마다** 제목 줄(SectionHeader)에
        # 그 표의 내용 전체 보기·컬럼 설정·엑셀 저장(도서별수불원장과 같은 구성).
        for rel, sid in (("reports/book-sales/page.tsx", "Sobo61"), ("reports/customer-sales/page.tsx", "Sobo62")):
            src = _read(rel)
            self.assertNotIn(f'data-legacy-id="{sid}.ShowAll"', src.split("<SplitListPanes")[0], rel)
            left = src.split("top={")[1].split("bottom={")[0]
            self.assertIn("<SectionHeader", left, rel)
            for wid in (f"{sid}.ShowAll", f"{sid}.Button_Export"):
                self.assertIn(wid, left, f"{rel}: {wid} 는 좌측 표 머리")
            right = src.split("bottom={")[1]
            self.assertIn("<SectionHeader", right, rel)
            self.assertIn(f"{sid}.Button_ExportDetail", right, rel)

    def test_book_sales_defaults_to_all_after_search(self) -> None:
        src = _read("reports/book-sales/page.tsx")
        self.assertIn("const effectiveAll = showAll || detail === null;", src)
        self.assertIn("if (!effectiveAll || !sid || bcodes.length === 0) return;", src)


if __name__ == "__main__":
    main()
