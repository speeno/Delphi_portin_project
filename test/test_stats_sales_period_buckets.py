"""STAT-1 기간별 매출 — 일/주/월 버킷 분할 회귀 (stats_service.get_sales_period)."""

from __future__ import annotations

from datetime import date
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class SalesPeriodSliceHelpers(TestCase):
    def test_day_ranges_counts_three_days(self):
        from app.services.stats_service import _day_ranges

        d1 = date(2026, 5, 1)
        d2 = date(2026, 5, 3)
        rng = _day_ranges(d1, d2)
        self.assertEqual(len(rng), 3)
        self.assertEqual(rng[0], (d1, d1))
        self.assertEqual(rng[2], (d2, d2))

    def test_week_ranges_splits_iso_weeks(self):
        from app.services.stats_service import _week_ranges

        # 월요일~일요일 한 주만 걸친 경우 1구간
        d1 = date(2026, 5, 4)  # Mon
        d2 = date(2026, 5, 10)  # Sun
        rng = _week_ranges(d1, d2)
        self.assertEqual(len(rng), 1)
        self.assertEqual(rng[0], (d1, d2))

    def test_month_ranges_splits_calendar_months(self):
        from app.services.stats_service import _month_ranges

        d1 = date(2026, 4, 28)
        d2 = date(2026, 5, 5)
        rng = _month_ranges(d1, d2)
        self.assertEqual(len(rng), 2)
        self.assertEqual(rng[0][0], d1)
        self.assertEqual(rng[0][1], date(2026, 4, 30))
        self.assertEqual(rng[1][0], date(2026, 5, 1))
        self.assertEqual(rng[1][1], d2)


def _cell(goqut=0, gosum=0, giqut=0, gisum=0):
    return {"giqut": giqut, "gisum": gisum, "gbqut": 0, "gpqut": 0,
            "gjqut": 0, "goqut": goqut, "gosum": gosum, "gpsum": 0}


class SalesPeriodBucketAggregation(IsolatedAsyncioTestCase):
    async def test_daily_single_pass_and_sums(self):
        """DEC-140 — 종전 '일자당 1회 호출(N+1)' 계약 폐기: 기간 전체 1회 호출."""
        from app.services.stats_service import get_sales_period

        calls: list[tuple[str, str]] = []

        async def fake_daily_cells(**kwargs):
            calls.append((kwargs["date_from"], kwargs["date_to"]))
            return {
                "2026.05.01": _cell(goqut=1, gosum=100),
                "2026.05.02": _cell(goqut=2, gosum=200),
            }

        with patch("app.services.stats_service.reports_service.get_daily_sales_cells",
                   new=fake_daily_cells):
            out = await get_sales_period(
                server_id="remote_138",
                hcode=None,
                date_from="2026.05.01",
                date_to="2026.05.02",
                group_by="daily",
                limit=100,
                offset=0,
            )

        self.assertEqual(calls, [("2026.05.01", "2026.05.02")], "단일 패스(N+1 금지)")
        self.assertEqual(len(out["items"]), 2)
        self.assertEqual(out["items"][0]["group_by"], "daily")
        self.assertEqual(out["items"][0]["qut_total"], 1)
        self.assertEqual(out["items"][1]["qut_total"], 2)

    async def test_weekly_single_slice_rolls_up_days(self):
        from app.services.stats_service import get_sales_period

        async def fake_daily_cells(**kwargs):
            return {
                "2026.05.04": _cell(goqut=2, gosum=200),
                "2026.05.06": _cell(goqut=3, gosum=300),
            }

        with patch("app.services.stats_service.reports_service.get_daily_sales_cells",
                   new=fake_daily_cells):
            out = await get_sales_period(
                server_id="remote_138",
                hcode=None,
                date_from="2026.05.04",
                date_to="2026.05.10",
                group_by="weekly",
                limit=100,
                offset=0,
            )

        self.assertEqual(len(out["items"]), 1)
        self.assertEqual(out["items"][0]["qut_total"], 5)
        self.assertEqual(out["items"][0]["qut_total"], 5)
        self.assertEqual(out["items"][0]["group_by"], "weekly")


if __name__ == "__main__":
    main(verbosity=2)
