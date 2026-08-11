"""DEC-140 — 기간별 매출분석 단일 패스 + 필터바 개선 회귀 가드.

2026-08-11 교문사-경리부: ① "서버 응답이 30000ms 를 초과했습니다" — 일 단위
장기간 조회 시 슬라이스마다 get_book_sales 를 반복 호출(N+1, 222일=222회)하던
것을 S1_Ssub 단일 쿼리 + 파이썬 버킷으로 교정(라이브: 30s 타임아웃 → 1.1s).
② 도서명 표기, ③ 도서 선택 후 Enter 다음 이동 — StatsFilterBar 공용 반영.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import stats_service  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class SalesPeriodBucketTests(IsolatedAsyncioTestCase):
    async def _run(self, s1_rows, **kw):
        async def fake_exec(server_id, sql, params=()):
            if "FROM S1_Ssub" in sql:
                return s1_rows
            return []

        with patch("app.services.reports_service.execute_query", new=fake_exec):
            return await stats_service.get_sales_period(
                server_id="srv", hcode="5019",
                date_from="2026-07-01", date_to="2026-07-14", **kw,
            )

    async def test_daily_buckets_and_totals(self) -> None:
        rows = [
            {"Gdate": "2026.07.06", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 6, "Gssum": 9000},
            {"Gdate": "2026.07.06", "Scode": "Y", "Gubun": "입고", "Pubun": "",
             "Gsqut": 100, "Gssum": 50000},
            {"Gdate": "2026.07.07", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 1, "Gssum": 1500},
            # 비정형 일자 — 스킵(warn)하고 죽지 않아야 한다.
            {"Gdate": "잘못된값", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 9, "Gssum": 999},
        ]
        res = await self._run(rows, group_by="daily")
        by = {i["bucket"]: i for i in res["items"]}
        self.assertEqual(by["2026-07-06"]["qut_total"], 6)
        self.assertEqual(by["2026-07-06"]["buy_qut_total"], 100)
        self.assertEqual(by["2026-07-07"]["qut_total"], 1)
        self.assertEqual(res["totals"]["qut_total"], 7)
        self.assertEqual(res["totals"]["buy_sum_total"], 50000)
        # 빈 일자 구간도 0 으로 채워져 존재(차트 연속성).
        self.assertEqual(by["2026-07-05"]["qut_total"], 0)

    async def test_weekly_bucket_rollup(self) -> None:
        rows = [
            {"Gdate": "2026.07.06", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 2, "Gssum": 100},
            {"Gdate": "2026.07.08", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 3, "Gssum": 200},
        ]
        res = await self._run(rows, group_by="weekly")
        nz = [i for i in res["items"] if i["qut_total"]]
        self.assertEqual(len(nz), 1, "같은 주(07.06~07.08)는 한 버킷")
        self.assertEqual(nz[0]["qut_total"], 5)

    async def test_single_bcode_filter_clause(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            return []

        with patch("app.services.reports_service.execute_query", new=fake_exec):
            await stats_service.get_sales_period(
                server_id="srv", hcode="5019",
                date_from="2026-07-01", date_to="2026-07-14",
                group_by="daily", bcode_from="90008", bcode_to="",
            )
        sql, params = next(c for c in captured if "FROM S1_Ssub" in c[0])
        self.assertIn("Bcode = %s", sql, "한쪽만 지정 시 단일 도서 필터(종전 무시)")
        self.assertIn("90008", params)
        self.assertIn("Hcode = %s", sql)


class FilterBarSourceGuards(TestCase):
    def test_enter_flow_and_book_name(self) -> None:
        src = (FRONT / "components" / "stats" / "stats-filter-bar.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn("advanceFilterOnEnter", src, "필터 Enter 이동 회귀 — DEC-140")
        self.assertIn("data-enter-scope", src)
        self.assertIn("bcodeFromName", src, "선택 도서명 표기 회귀 — DEC-140")
        self.assertIn("Button_Search", src.split("filterStopIds")[1].split("return ids")[0],
                      "Enter 흐름 마지막 스톱 = 조회 버튼")


if __name__ == "__main__":
    main()
