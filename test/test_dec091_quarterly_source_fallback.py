"""DEC-091 addendum — 분기/청구 원천 폴백 + 손익(청구−입금) 정본 회귀 가드.

- A) T2_Ssub 미집계 시 list_period_summary 가 출고(S1)−반품(R3) 실시간 파생으로 대체,
     source='s1_ssub_live'. 파생 SQL 은 월키 정규화 + Yesno 무필터(DEC-081/085).
- C) get_quarterly_summary 의 손익 = 청구(T2 Sum28) − 입금(T5_Ssub), source 전파.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import settlement_service as ss  # noqa: E402
from app.services import stats_service as stx  # noqa: E402
from app.services import t5_ssub_adapt  # noqa: E402

_NORM = "REPLACE(REPLACE(REPLACE(TRIM("


class PeriodSourceFallbackTests(IsolatedAsyncioTestCase):
    async def test_t2_populated_uses_t2(self) -> None:
        async def fake(server_id, sql, params=()):  # noqa: ARG001
            up = sql.upper()
            if "COUNT(DISTINCT" in up:
                return [{"cnt": 2}]
            if "GSUMX" in up:
                return [
                    {"Gdate": "202601", "GSUMX": 100, "GSUMY": 10, "GSSUM": 110},
                    {"Gdate": "202602", "GSUMX": 200, "GSUMY": 20, "GSSUM": 220},
                ]
            return []

        with patch.object(ss, "execute_query", side_effect=fake):
            res = await ss.list_period_summary(
                server_id="remote_138", hcode="", month_from="202601", month_to="202603",
            )
        self.assertEqual(res["source"], "t2_ssub")
        self.assertEqual(res["total"], 2)
        self.assertEqual(res["totals"]["gssum"], 330)

    async def test_t2_empty_falls_back_to_source(self) -> None:
        captured: list[str] = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            captured.append(sql)
            up = sql.upper()
            if "COUNT(DISTINCT" in up:
                return [{"cnt": 0}]  # T2 비어 있음
            if "FROM S1_SSUB" in up:
                return [{"Gdm": "202601", "Amt": 1000}, {"Gdm": "202602", "Amt": 500}]
            if "FROM R3_SSUB" in up:
                return [{"Gdm": "202601", "Amt": 100}]
            return []  # T2 list

        with patch.object(ss, "execute_query", side_effect=fake):
            res = await ss.list_period_summary(
                server_id="remote_138", hcode="", month_from="202601", month_to="202603",
            )
        self.assertEqual(res["source"], "s1_ssub_live")
        self.assertEqual(res["total"], 2)
        # 202601: 1000-100=900 → Sum26=900, Sum27=90, Sum28=990.
        m1 = next(i for i in res["items"] if i["gdate"] == "202601")
        self.assertEqual(m1["gsumx"], 900)
        self.assertEqual(m1["gsumy"], 90)
        self.assertEqual(m1["gssum"], 990)
        # 파생 SQL: 월키 정규화 + Yesno 무필터.
        src = next(s for s in captured if "FROM S1_Ssub" in s)
        self.assertIn(_NORM, src)
        self.assertNotIn("<> '2'", src)
        self.assertNotIn("Yesno", src)

    async def test_deposits_by_month(self) -> None:
        async def fake(server_id, sql, params=()):  # noqa: ARG001
            if sql.strip().upper().startswith("SHOW COLUMNS"):
                return [{"Field": "Gdate"}, {"Field": "Hcode"}, {"Field": "Gssum"}]
            return [{"Gdm": "202601", "Amt": 700}, {"Gdm": "202602", "Amt": 300}]

        # deposits_by_month 는 t5_ssub_adapt.t5_column_names(SHOW COLUMNS) 를 거치며,
        # 그 어댑터는 자체 import 한 execute_query 를 쓰므로 함께 패치해야 실 DB
        # (servers.yaml 라이브 터널) 접근 없이 fake 의 SHOW COLUMNS 분기가 쓰인다.
        t5_ssub_adapt.clear_t5_column_cache_for_tests()
        try:
            with patch.object(ss, "execute_query", side_effect=fake), \
                 patch.object(t5_ssub_adapt, "execute_query", side_effect=fake):
                dep = await ss.deposits_by_month(
                    "remote_138", month_from="202601", month_to="202603", hcode="",
                )
        finally:
            t5_ssub_adapt.clear_t5_column_cache_for_tests()
        self.assertEqual(dep, {"202601": 700, "202602": 300})


class QuarterlyProfitSemanticsTests(IsolatedAsyncioTestCase):
    async def test_profit_is_billed_minus_deposit(self) -> None:
        # 청구(Sum28) = 990+220 per month via list_period_summary; 입금(T5) via deposits.
        async def fake_period(*, server_id, hcode, month_from, month_to, limit=12, offset=0):  # noqa: ARG001
            return {
                "items": [
                    {"gdate": "202601", "gsumx": 900, "gsumy": 90, "gssum": 990},
                    {"gdate": "202602", "gsumx": 200, "gsumy": 20, "gssum": 220},
                ],
                "totals": {"gsumx": 1100, "gsumy": 110, "gssum": 1210},
                "total": 2,
                "source": "s1_ssub_live",
            }

        async def fake_dep(server_id, *, month_from, month_to, hcode=None):  # noqa: ARG001
            return {"202601": 400, "202602": 100}

        with patch.object(ss, "list_period_summary", new=AsyncMock(side_effect=fake_period)), \
             patch.object(ss, "deposits_by_month", new=AsyncMock(side_effect=fake_dep)):
            res = await stx.get_quarterly_summary(
                server_id="remote_138", hcode=None, year=2026, quarter=1, quarters=1,
            )
        comp = res["comparison"][0]
        # 청구 = 990+220 = 1210, 입금 = 400+100 = 500, 손익 = 710.
        self.assertEqual(comp["gsumx"], 1210)   # 청구
        self.assertEqual(comp["gsumy"], 500)    # 입금
        self.assertEqual(comp["gssum"], 710)    # 잔액
        self.assertEqual(comp["profit"], 710)   # 손익 = 청구 − 입금
        self.assertEqual(res["totals"]["profit"], 710)
        # 월별 items 도 청구/입금/잔액 축으로 재매핑.
        m1 = next(i for i in res["items"] if i["gdate"] == "202601")
        self.assertEqual(m1["gsumx"], 990)      # 청구
        self.assertEqual(m1["gsumy"], 400)      # 입금
        self.assertEqual(m1["gssum"], 590)      # 잔액
        # source 전파(파생본 배지용).
        self.assertEqual(res["metadata"]["source"], "s1_ssub_live")
        self.assertEqual(res["metadata"]["profit_basis"], "billed_minus_deposit")


class QuarterlyMultiQuarterTests(IsolatedAsyncioTestCase):
    async def test_quarters_n_aggregates_billed_minus_deposit(self) -> None:
        """다분기(N) 집계 — 각 분기 청구(Sum28)−입금(T5) 손익 + 합산 (팬아웃 백엔드 계약)."""
        async def fake_period(*, server_id, hcode, month_from, month_to, limit=12, offset=0):  # noqa: ARG001
            return {
                "items": [{"gdate": month_from, "gsumx": 10, "gsumy": 1, "gssum": 11}],
                "totals": {"gsumx": 10, "gsumy": 1, "gssum": 11},
                "total": 1, "source": "t2_ssub",
            }

        async def fake_dep(server_id, *, month_from, month_to, hcode=None):  # noqa: ARG001
            return {month_from: 3}

        with patch.object(ss, "list_period_summary", new=AsyncMock(side_effect=fake_period)), \
             patch.object(ss, "deposits_by_month", new=AsyncMock(side_effect=fake_dep)):
            res = await stx.get_quarterly_summary(
                server_id="remote_138", hcode=None, year=2026, quarter=2, quarters=3,
            )
        self.assertEqual(len(res["comparison"]), 3)
        # 청구=11(Sum28), 입금=3, 손익=8 per 분기.
        self.assertTrue(all(c["profit"] == 8 for c in res["comparison"]))
        self.assertEqual(res["totals"]["profit"], 24)  # 8 × 3


if __name__ == "__main__":
    main()
