"""DEC-085 — 분기/반기 손익 0건 사고: T2_Ssub.Gdate 월키 정규화 회귀 가드.

배경
----
레거시 Subu45(정산 입력)는 T2_Ssub.Gdate 에 ``FormatDateTime('yyyy"."mm"')`` =
점 구분 월('2026.07') 을 기록한다. ``Gdate BETWEEN 'YYYYMM'..`` 직접 비교는
문자열 정렬상('.' < '0') 전 행이 하한에서 탈락 → 분기/반기 손익(Sobo53)·
청구금액(년월)(Sobo47) 이 항상 0건이 되던 원인.

가드 포인트
-----------
1. ``_SQL_PERIOD_SUMMARY``(+COUNT) 는 숫자만 남긴 6자리 월키
   (REPLACE/TRIM/LEFT — t5_ssub_adapt 동일 패턴)로 비교·그룹·정렬한다.
2. 원컬럼 ``Gdate BETWEEN`` 직접 비교로의 회귀 금지.
3. 파라미터는 정규화된 'YYYYMM' 6자리.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

_MONTH_KEY = "LEFT(REPLACE(REPLACE(REPLACE(TRIM(Gdate),'-',''),'.',''),'/',''),6)"


class PeriodSummaryMonthKeyTests(IsolatedAsyncioTestCase):
    async def _run(self, **kwargs: Any) -> list[tuple[str, tuple[Any, ...]]]:
        from app.services import settlement_service as st

        calls: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            calls.append((sql, tuple(params)))
            if "COUNT(DISTINCT" in sql:
                return [{"cnt": 0}]
            return []

        with patch("app.services.settlement_service.execute_query", new=fake_exec):
            await st.list_period_summary(
                server_id="srv", hcode="5019",
                month_from=kwargs.get("month_from", "2026-01"),
                month_to=kwargs.get("month_to", "2026-03"),
            )
        return calls

    async def test_sql_uses_normalized_month_key(self) -> None:
        calls = await self._run()
        paged_sql = calls[0][0]
        count_sql = calls[1][0]
        for sql in (paged_sql, count_sql):
            self.assertIn(_MONTH_KEY, sql)
            # 원컬럼 직접 BETWEEN 회귀 금지 — 'Gdate BETWEEN' 은 월키 표현식
            # 안(TRIM(Gdate))에만 존재해야 한다.
            self.assertNotIn(" Gdate BETWEEN", sql)
            # DEC-089 — 레거시 Subu47 원문에 없는 Yesno 필터 재도입 금지
            # (마감 데이터 제외 → 분기 손익 0원 사고).
            self.assertNotIn("Yesno", sql)
        self.assertIn(f"GROUP BY {_MONTH_KEY}", paged_sql)
        self.assertIn(f"ORDER BY {_MONTH_KEY}", paged_sql)

    async def test_month_params_normalized_to_yyyymm(self) -> None:
        calls = await self._run(month_from="2026-01", month_to="2026.03")
        _, params = calls[0]
        self.assertEqual(params[0], "202601")
        self.assertEqual(params[1], "202603")

    async def test_quarterly_summary_delegates_quarter_bounds(self) -> None:
        from app.services import stats_service

        captured: dict[str, Any] = {}

        async def fake_period_summary(**kwargs):
            captured.update(kwargs)
            return {"items": [], "totals": {"gsumx": 0, "gsumy": 0, "gssum": 0}, "total": 0}

        async def fake_deposits(server_id, *, month_from, month_to, hcode=None):
            return {}

        old = stats_service.settlement_service.list_period_summary
        old_dep = stats_service.settlement_service.deposits_by_month
        stats_service.settlement_service.list_period_summary = fake_period_summary
        stats_service.settlement_service.deposits_by_month = fake_deposits
        try:
            await stats_service.get_quarterly_summary(
                server_id="srv", hcode="5019", year=2026, quarter=3,
            )
        finally:
            stats_service.settlement_service.list_period_summary = old
            stats_service.settlement_service.deposits_by_month = old_dep

        self.assertEqual(captured["month_from"], "202607")
        self.assertEqual(captured["month_to"], "202609")
        self.assertEqual(captured["hcode"], "5019")

    async def test_quarterly_summary_n_quarter_comparison(self) -> None:
        """DEC-088 — quarters=N: 기준 분기에서 과거 방향 N개 분기 집계·비교."""
        from app.services import stats_service

        calls: list[tuple[str, str]] = []

        async def fake_period_summary(**kwargs):
            calls.append((kwargs["month_from"], kwargs["month_to"]))
            # gssum(Sum28)=60 = 청구. DEC-091 — 손익=청구−입금(T5).
            return {
                "items": [{"gdate": kwargs["month_from"], "gsumx": 100, "gsumy": 40, "gssum": 60}],
                "totals": {"gsumx": 100, "gsumy": 40, "gssum": 60},
                "total": 1,
            }

        async def fake_deposits(server_id, *, month_from, month_to, hcode=None):
            # 각 분기 첫 달에 입금 10 → 손익 = 청구(60) − 입금(10) = 50.
            return {month_from: 10}

        old = stats_service.settlement_service.list_period_summary
        old_dep = stats_service.settlement_service.deposits_by_month
        stats_service.settlement_service.list_period_summary = fake_period_summary
        stats_service.settlement_service.deposits_by_month = fake_deposits
        try:
            res = await stats_service.get_quarterly_summary(
                server_id="srv", hcode="5019", year=2026, quarter=1, quarters=3,
            )
        finally:
            stats_service.settlement_service.list_period_summary = old
            stats_service.settlement_service.deposits_by_month = old_dep

        # 과거 → 기준 순: 2025-Q3, 2025-Q4, 2026-Q1.
        self.assertEqual(calls, [("202507", "202509"), ("202510", "202512"), ("202601", "202603")])
        comp = res["comparison"]
        self.assertEqual([c["label"] for c in comp], ["2025-Q3", "2025-Q4", "2026-Q1"])
        # DEC-091 — 청구=Sum28(60), 입금=T5(10), 손익=청구−입금=50.
        self.assertTrue(all(c["gsumx"] == 60 for c in comp), "청구=Sum28")
        self.assertTrue(all(c["gsumy"] == 10 for c in comp), "입금=T5")
        self.assertTrue(all(c["profit"] == 50 for c in comp), "손익=청구−입금")
        self.assertEqual(res["totals"]["gsumx"], 180)   # 청구 3분기 합 = 60×3
        self.assertEqual(res["totals"]["profit"], 150)  # (60−10)×3
        self.assertEqual(res["metadata"]["quarters"], 3)
        # 월별 items 는 N개 분기 병합 + 월 오름차순.
        self.assertEqual([i["gdate"] for i in res["items"]], ["202507", "202510", "202601"])


class PublisherRowScopeTests(IsolatedAsyncioTestCase):
    """DEC-090 — T2 정산(행=출판사 코드) 도메인 hcode 해석 가드."""

    def _resolve(self, request_hcode, ctx):
        from app.core.hcode_isolation import resolve_publisher_row_scope
        return resolve_publisher_row_scope(request_hcode, ctx)

    async def test_operator_account_defaults_to_all(self) -> None:
        # 물류/총판(T1) 운영 계정 — 로그인 코드 주입 금지, 미지정=전체(None).
        ctx = {"hcode": "5019", "account_type": "T1", "account_family": "chul_09",
               "role": "operator", "permissions": ["admin.stats.quarterly"]}
        self.assertIsNone(self._resolve(None, ctx))
        self.assertIsNone(self._resolve("", ctx))

    async def test_operator_optional_filter_passthrough(self) -> None:
        ctx = {"hcode": "5019", "account_type": "T2_DIST", "account_family": "chul_09",
               "role": "operator", "permissions": []}
        self.assertEqual(self._resolve("P001", ctx), "P001")

    async def test_isolated_publisher_forced_to_own_code(self) -> None:
        # 출판사 계정(T2_PUB) — 타 코드 요청해도 본인 코드 강제.
        ctx = {"hcode": "P777", "account_type": "T2_PUB", "account_family": "chul_09",
               "role": "operator", "permissions": []}
        self.assertEqual(self._resolve(None, ctx), "P777")
        self.assertEqual(self._resolve("P001", ctx), "P777")


if __name__ == "__main__":  # pragma: no cover
    main()
