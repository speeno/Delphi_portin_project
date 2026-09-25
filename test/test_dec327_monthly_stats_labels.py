"""
DEC-327 — 월별통계 컬럼 용어 직관화(사용자 2026-09-25 「트렌드는 어떤 의미?」 → 「직관적 용어로 변경」).

- 수량합/금액합 → 매출수량 합계/매출금액 합계(표 머리·하단 합계 동일).
- 「트렌드」(증감 추세가 아닌 금액 비교 막대) → 「매출 비교 (최고 월=100%)」 + 비율(%) 표시.
- 막대 열은 화면 보조 표시라 엑셀 저장 컬럼에서 제외.
- 차트(사용자 「다양한 차트 형식과 함께」): 금액·수량 막대 / 추세선 / 전월 대비 증감 / 누적 면적 / 월별 비중 원형(상위 7 + 기타).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

PAGE = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "stats" / "monthly" / "page.tsx"
)


class MonthlyStatsLabels(TestCase):
    def setUp(self):
        self.src = PAGE.read_text(encoding="utf-8")

    def test_intuitive_labels(self):
        self.assertIn('label: "매출수량 합계"', self.src)
        self.assertIn('label: "매출금액 합계"', self.src)
        self.assertIn('label: "매출 비교 (최고 월=100%)"', self.src)
        for old in ('label: "트렌드"', 'label: "수량합"', 'label: "금액합"', "<span>수량합 ", "<span>금액합 "):
            self.assertNotIn(old, self.src)

    def test_bar_shows_percent_and_excluded_from_export(self):
        self.assertIn("{Math.round(pct)}%", self.src)
        export = self.src.split("salesPeriodExportBlob(")[1].split("groupBy")[0]
        self.assertIn('.filter((c) => c.id !== "trend")', export)

    def test_chart_kinds(self):
        for kind in ('"bar"', '"trend"', '"delta"', '"cumulative"', '"share"'):
            self.assertIn(f"value: {kind}", self.src)
        self.assertIn('legacyId="StatsMonthly.Chart_Monthly"', self.src)
        self.assertIn('data-legacy-id="StatsMonthly.Combo_ChartKind"', self.src)
        self.assertIn("<StatsCumulativeAreaChart", self.src)
        self.assertIn('labelKind="name"', self.src)
        self.assertIn("PIE_TOP", self.src)

    def test_cumulative_chart_component(self):
        charts = (PAGE.parents[4] / "components" / "stats" / "charts.tsx").read_text(encoding="utf-8")
        body = charts.split("export function StatsCumulativeAreaChart")[1].split("export function")[0]
        self.assertIn("acc += Number(d.value ?? 0)", body)
        self.assertIn("isAnimationActive={false}", body)


if __name__ == "__main__":
    main(verbosity=2)
