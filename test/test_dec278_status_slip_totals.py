"""DEC-278 — 현황(전표 목록) 하단 합계 행 (2026-09-12, 교문사 「반품현황 하단에 합계」).

공용 `TransactionStatusScreen`(출고·입고·반품·폐기·신간발행 현황)의 전표 목록(상세·요약)에는
합계 행이 없었다. `DataGrid` 의 `totals`(DEC-146, `tfoot` + `sticky bottom-0`)로 항목수·수량·금액을
붙인다. 합계는 **화면에 보이는 행 기준**(접수유형 필터 반영, 상세 라인 합계와 같은 관례)이고,
결과가 여러 페이지면 라벨을 「합계(이 페이지)」로 바꿔 부분합임을 드러낸다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

_HUB = Path(__file__).resolve().parents[1]
_SRC = _HUB / "도서물류관리프로그램" / "frontend" / "src" / "components" / "transactions" / "transaction-status-screen.tsx"


class StatusSlipTotalsTests(TestCase):
    def setUp(self) -> None:
        self.src = _SRC.read_text(encoding="utf-8")

    def test_totals_sum_the_slip_measure_columns(self) -> None:
        self.assertIn("slipTotalsOf", self.src)
        for key in ("item_count", "qty", "amount"):
            self.assertRegex(
                self.src,
                re.compile(rf"{key}: rows\.reduce\("),
                f"{key} 합계 누락 — 전표 목록 컬럼과 키가 맞아야 tfoot 에 찍힌다",
            )

    def test_both_slip_grids_get_totals(self) -> None:
        """상세(DBGrid101) · 요약(DBGrid201) 두 전표 목록 모두."""
        self.assertIn("totals={filteredSlips.length > 0 ? slipTotalsOf(filteredSlips) : undefined}", self.src)
        self.assertIn("totals={slips.length > 0 ? slipTotalsOf(slips) : undefined}", self.src)

    def test_totals_follow_the_visible_rows(self) -> None:
        """접수유형 필터로 좁힌 상세 목록은 그 부분합이 맞다(보이는 행 = 더하는 행)."""
        self.assertIn("slipTotalsOf(filteredSlips)", self.src)
        self.assertNotIn("slipTotalsOf(slips.filter", self.src)

    def test_multi_page_totals_are_labelled(self) -> None:
        """조용한 부분합 금지 — 여러 페이지면 「합계(이 페이지)」."""
        self.assertIn('page.total > shown ? "합계(이 페이지)" : "합계"', self.src)
        self.assertIn("totalsLabel={slipTotalsLabel(", self.src)


if __name__ == "__main__":
    main()
