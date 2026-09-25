"""
DEC-326 — 분기/반기 손익 점검(사용자 2026-09-25).

- 청구: 월 단위로 T2_Ssub 확정값(≠0) 우선, 없거나 0 이면 출고−반품 실시간 파생.
- 입금: T5_Ssub 값이 있는 달은 T5, 없으면 H1_Ssub 수금(입금−출금).
- 도서별 판매 기여도: 판매금액(출고+반품) 비중·누적 비중, 별도 엔드포인트 1회 조회.
- 화면: 분기 추세 선그래프(최소제곱 추세선), 청구 구성 파이(입금·잔액, 중복 조각 없음), 파이 애니메이션 off.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "도서물류관리프로그램"
BACKEND = PRODUCT / "backend"
FE = PRODUCT / "frontend" / "src"
sys.path.insert(0, str(BACKEND))


class QuarterSourceMerge(IsolatedAsyncioTestCase):
    async def _run(self, *, t2, live, t5, h1):
        from app.services import stats_service

        ss = stats_service.settlement_service

        async def f_t2(**kw):
            return t2

        async def f_live(server_id, **kw):
            return live

        async def f_t5(server_id, **kw):
            return t5

        async def f_h1(server_id, **kw):
            return h1

        olds = (ss.list_period_summary, ss.live_period_summary, ss.deposits_by_month, ss.receipts_by_month_h1)
        ss.list_period_summary, ss.live_period_summary = f_t2, f_live
        ss.deposits_by_month, ss.receipts_by_month_h1 = f_t5, f_h1
        try:
            return await stats_service._compute_quarter("remote_153", 2026, 1, "5019")
        finally:
            (ss.list_period_summary, ss.live_period_summary,
             ss.deposits_by_month, ss.receipts_by_month_h1) = olds

    async def test_billed_uses_t2_when_nonzero_else_live(self):
        res = await self._run(
            t2={"source": "t2_ssub", "items": [
                {"gdate": "202601", "gssum": 1000},   # 확정값
                {"gdate": "202603", "gssum": 0},      # 자리표시 행(0) → 실시간
            ]},
            live={"202601": {"gssum": 9}, "202602": {"gssum": 200}, "202603": {"gssum": 300}},
            t5={}, h1={},
        )
        self.assertEqual([m["gsumx"] for m in res["month_items"]], [1000, 200, 300])
        self.assertEqual(res["billed"], 1500)
        self.assertTrue(res["source_live"])

    async def test_deposit_t5_first_then_h1(self):
        res = await self._run(
            t2={"source": "t2_ssub", "items": []},
            live={},
            t5={"202601": 50},
            h1={"202601": 7, "202602": 70, "202603": -5},
        )
        self.assertEqual([m["gsumy"] for m in res["month_items"]], [50, 70, -5])
        self.assertEqual(res["deposit"], 115)
        self.assertEqual(res["balance"], res["billed"] - 115)


class BookContribution(IsolatedAsyncioTestCase):
    async def test_share_and_cumulative(self):
        from app.services import stats_service

        seen = {}

        async def fake_book_sales(**kw):
            seen.update(kw)
            return {"rows": [
                {"gcode": "B1", "gname": "A", "goqut": 10, "gbqut": -2, "gosum": 1000, "gbsum": -200},
                {"gcode": "B2", "gname": "B", "goqut": 3, "gbqut": 0, "gosum": 200, "gbsum": 0},
            ]}

        old = stats_service.reports_service.get_book_sales
        stats_service.reports_service.get_book_sales = fake_book_sales
        try:
            res = await stats_service.get_book_contribution(
                server_id="remote_153", hcode="5019", month_from="202601", month_to="202602",
            )
        finally:
            stats_service.reports_service.get_book_sales = old

        self.assertEqual(seen["date_from"], "2026.01.01")
        self.assertEqual(seen["date_to"], "2026.02.28")
        self.assertEqual(res["total_sale_amt"], 1000)
        b1, b2 = res["items"]
        self.assertEqual((b1["rank"], b1["sale_qty"], b1["sale_amt"], b1["share"], b1["cum_share"]),
                         (1, 8, 800, 80.0, 80.0))
        self.assertEqual((b2["rank"], b2["share"], b2["cum_share"]), (2, 20.0, 100.0))

    async def test_invalid_range_rejected(self):
        from app.services import stats_service

        with self.assertRaises(stats_service.StatsValidationError):
            await stats_service.get_book_contribution(
                server_id="remote_153", hcode=None, month_from="202603", month_to="202601",
            )


class QuarterlyStatic(TestCase):
    def test_router_and_probe(self):
        router = (BACKEND / "app" / "routers" / "stats.py").read_text(encoding="utf-8")
        self.assertIn('"/book-contribution"', router)
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("/api/v1/stats/book-contribution", probe)

    def test_charts_trend_and_pie(self):
        charts = (FE / "components" / "stats" / "charts.tsx").read_text(encoding="utf-8")
        self.assertIn("export function StatsTrendLineChart", charts)
        self.assertIn("__trend", charts)
        pie = charts.split("export function StatsPieChart")[1]
        self.assertIn("isAnimationActive={false}", pie)

    def test_page_wiring(self):
        src = (FE / "app" / "(app)" / "stats" / "quarterly-summary" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("<StatsTrendLineChart", src)
        self.assertIn("statsApi.bookContribution", src)
        self.assertIn(".Grid_BookContribution", src)
        self.assertIn("청구 구성", src)
        self.assertNotIn('"손익(+)"', src)  # 잔액과 같은 값 — 중복 조각 금지
        self.assertIn("showAllLabels", src)


if __name__ == "__main__":
    main(verbosity=2)
