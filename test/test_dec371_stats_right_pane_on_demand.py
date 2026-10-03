"""DEC-371 — 통계 도서별판매 · 거래처별판매: 기본은 좌측 목록 전체 폭, 우측은 필요할 때만.

요청(교문사, 2026-10-03)
-----------------------
"통계관리 화면이 현재 좌/우로 나눠져있는데요. 기본 화면은 좌측화면을 전체화면으로 해주시고,
내용 전체보기를 클릭하면 좌측화면이 줄어들면서 세부 내용이 보여지는걸로 요청드립니다.
내용 전체보기 해지를 하면 좌측화면이 다시 커지는걸루요. 현재, 출고현황, 원장관리 기능과 동일하게."

규칙
----
- 우측 창 = 「내용 전체 보기」 체크 또는 좌측 행 선택 때만(출고현황 · 원장관리와 같은 조건).
- 체크를 풀면 선택도 함께 풀려 좌측이 다시 전체 폭(전체 보기 중 눌러 본 행 때문에 우측이 남지 않게).
- DEC-319 의 «우측 창 항상 표시»는 철회. DEC-343/351(선택 전 우측 공백) · DEC-344(전체 = 검색 결과 전체)는 유지.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

APP = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"


def _read(rel: str) -> str:
    return (APP / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def _show_all_handler(src: str, legacy_id: str) -> str:
    """「내용 전체 보기」 체크박스 input 블록."""
    at = src.index(f'data-legacy-id="{legacy_id}"')
    start = src.rindex("<input", 0, at)
    return src[start : src.index("/>", at)]


class StatsRightPaneOnDemand(TestCase):
    def test_book_sales(self) -> None:
        src = _read("reports/book-sales/page.tsx")
        self.assertIn("secondaryVisible={showAll || detail !== null}", src)
        box = _show_all_handler(src, "Sobo61.ShowAll")
        self.assertIn("setShowAll(e.target.checked);", box)
        self.assertIn("if (!e.target.checked) setDetail(null);", box)

    def test_customer_sales(self) -> None:
        src = _read("reports/customer-sales/page.tsx")
        self.assertIn("secondaryVisible={showAll || selectedKey !== null}", src)
        box = _show_all_handler(src, "Sobo62.ShowAll")
        self.assertIn("setShowAll(e.target.checked);", box)
        for clear in ("setSelectedKey(null);", "setSelectedRow(null);", "setDetail(null);"):
            self.assertIn(clear, box)

    def test_same_rule_as_outbound_status_and_ledger(self) -> None:
        self.assertIn(
            "secondaryVisible={showAll || selectedKey !== null}",
            (APP.parents[1] / "components" / "transactions" / "transaction-status-screen.tsx").read_text(encoding="utf-8"),
        )
        self.assertIn("secondaryVisible={showAll || selKey !== null}", _read("ledger/customer/page.tsx"))


if __name__ == "__main__":
    main()
