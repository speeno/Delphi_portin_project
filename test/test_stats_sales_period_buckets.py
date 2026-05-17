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


class SalesPeriodBucketAggregation(IsolatedAsyncioTestCase):
    async def test_daily_calls_once_per_day_and_sums(self):
        from app.services.stats_service import get_sales_period

        calls: list[tuple[str, str]] = []

        async def fake_get_book_sales(**kwargs):
            ds_from = kwargs["date_from"]
            ds_to = kwargs["date_to"]
            calls.append((ds_from, ds_to))
            # 각 일자별로 다른 합계 시뮬레이션
            day = ds_from.replace(".", "")
            q = int(day[-2:]) if len(day) >= 2 else 1
            return {"rows": [{"goqut": q, "gosum": q * 100}], "total": 1}

        with patch("app.services.stats_service.reports_service.get_book_sales", new=fake_get_book_sales):
            out = await get_sales_period(
                server_id="remote_138",
                hcode=None,
                date_from="2026.05.01",
                date_to="2026.05.02",
                group_by="daily",
                limit=100,
                offset=0,
            )

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], ("2026.05.01", "2026.05.01"))
        self.assertEqual(calls[1], ("2026.05.02", "2026.05.02"))
        self.assertEqual(len(out["items"]), 2)
        self.assertEqual(out["items"][0]["group_by"], "daily")

    async def test_weekly_single_slice_same_totals_as_one_call(self):
        from app.services.stats_service import get_sales_period

        async def fake_get_book_sales(**kwargs):
            return {"rows": [{"goqut": 5, "gosum": 500}], "total": 1}

        with patch("app.services.stats_service.reports_service.get_book_sales", new=fake_get_book_sales):
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
        self.assertEqual(out["items"][0]["group_by"], "weekly")


if __name__ == "__main__":
    main(verbosity=2)
