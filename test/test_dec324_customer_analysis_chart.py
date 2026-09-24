"""DEC-324 — 거래처별 판매 분석: 차트 = 표 순서·상위 N 선택·수량/금액 이중 축·막대별 라벨 (2026-09-24)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

SRC = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class CustomerAnalysisChart(TestCase):
    def setUp(self) -> None:
        self.page = (SRC / "app" / "(app)" / "stats" / "customer-analysis" / "page.tsx").read_text(encoding="utf-8")
        self.charts = (SRC / "components" / "stats" / "charts.tsx").read_text(encoding="utf-8")

    def test_bars_follow_table_order_and_top_n_is_selectable(self) -> None:
        self.assertIn("const TOP_N_OPTIONS = [10, 20, 30, 50, 0] as const;", self.page)
        self.assertIn("data.items.slice(0, topN)", self.page, "막대 = 표(서버 정렬) 앞 N행")
        self.assertNotIn(".sort((a, b) => Number(b.gosum", self.page, "차트만 따로 재정렬 금지")
        self.assertIn('{ key: "gosum", dir: "desc" }', self.page, "기본 정렬 = 출고금액 내림차순")
        self.assertIn(".Combo_TopN", self.page)

    def test_quantity_visible_on_own_axis_and_all_labels(self) -> None:
        self.assertIn("secondaryAxisThousand", self.page)
        self.assertIn("showAllLabels", self.page)
        self.assertIn('orientation="right"', self.charts)
        self.assertIn("interval={0}", self.charts)
        # recharts 3 — 재렌더가 잦은 화면에서 막대 애니메이션이 끝나지 않아 막대가 비던 문제.
        self.assertIn("isAnimationActive={false}", self.charts)


if __name__ == "__main__":
    main()
