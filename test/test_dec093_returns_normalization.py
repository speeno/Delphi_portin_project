"""DEC-093 — 반품관리 정비 회귀 가드.

축
--
1) Ocode: 조회 SQL 에서 ='B' 리터럴 제거(운영 chul_09 반품 행은 'A'/'' 혼재 — Subu21
   경유), INSERT 는 _default_outbound_ocode(server_id) 서버 가변.
2) Yesno: INSERT '1'(레거시 접수), 읽기측 s.Yesno='1' 필터 전부 제거(레거시 무필터),
   목록 기본 HAVING 제외 제거(DEC-081 미러) + 3-state status.
3) 날짜 정규화: ledger/period 대시 입력 → 점 표기.
4) 스코프: 일별 상세 로그인 폴백 + 기간 KPI hcode 필터 (크로스테넌트 차단).
5) inventory-candidates 신설 + export 4종 라우트 등록.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import returns_service as svc  # noqa: E402


class SqlConstantsTests(TestCase):
    def test_insert_parameterized_ocode_and_yesno_received(self) -> None:
        self.assertNotIn("'B'", svc.SQL_INSERT_LINE, "INSERT Ocode 하드코딩 금지")
        self.assertIn("'1'", svc.SQL_INSERT_LINE, "Yesno='1'(레거시 접수)")
        self.assertNotIn("'0',", svc.SQL_INSERT_LINE)

    def test_daily_sql_no_ocode(self) -> None:
        self.assertNotIn("Ocode='B'", svc.SQL_DAILY_MASTER)
        self.assertNotIn("Ocode='B'", svc.SQL_DAILY_DETAIL)
        # 반품 판별은 Gubun+Scode 로 유지.
        self.assertIn("Gubun='반품'", svc.SQL_DAILY_MASTER)
        self.assertIn("Scode='X'", svc.SQL_DAILY_MASTER)

    def test_no_read_side_yesno_filters(self) -> None:
        for name in dir(svc):
            if not name.startswith("SQL_"):
                continue
            sql = getattr(svc, name)
            if not isinstance(sql, str) or "INSERT" in sql or "UPDATE" in sql:
                continue
            self.assertNotIn(
                "s.Yesno='1'", sql, f"{name}: 읽기측 Yesno='1' 필터 잔존(레거시 무필터)",
            )

    def test_period_kpi_has_hcode_scope(self) -> None:
        self.assertIn("(%s='' OR s.Hcode=%s)", svc.SQL_PERIOD_KPI)

    def test_status_vocab_three_state(self) -> None:
        self.assertEqual(svc._returns_status_from_yesno("2"), "done")
        self.assertEqual(svc._returns_status_from_yesno("1"), "received")
        for v in ("", "0", "O", "3"):
            self.assertEqual(svc._returns_status_from_yesno(v), "pending", v)


class ListReturnsTests(IsolatedAsyncioTestCase):
    async def _run(self, captured, **kw):
        async def fake(server_id, sql, params=()):  # noqa: ARG001
            captured.append((sql, params))
            up = sql.strip().upper()
            if up.startswith("SELECT COUNT("):
                return [{"cnt": 1, "total": 1}]
            if "GROUP BY" in up and "YESNO_MAX" in up.upper():
                return [{"Gdate": "2026.07.01", "Hcode": "5019", "Jubun": "0001",
                         "line_count": 2, "qty": 5, "amount": 50000, "yesno_max": "2"}]
            return []

        with patch.object(svc, "execute_query", side_effect=fake), \
             patch.object(svc, "count_grouped", return_value=1), \
             patch.object(svc, "in_clause_lookup", return_value=[]):
            return await svc.list_returns(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31", **kw,
            )

    async def test_no_ocode_no_having_and_done_status(self) -> None:
        cap: list = []
        items, total = await self._run(cap)
        list_sql = cap[0][0]
        self.assertNotIn("Ocode", list_sql, "목록 Ocode 절 제거")
        self.assertNotIn("HAVING", list_sql, "기본 HAVING 제외 제거(DEC-081 미러)")
        # Yesno='2' 행은 항상 표시 + status='done'(완료, 취소 아님).
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "done")

    async def test_dates_normalized_to_dots(self) -> None:
        cap: list = []
        await self._run(cap)
        _, params = cap[0]
        self.assertEqual(params[0], "2026.07.01")
        self.assertEqual(params[1], "2026.07.31")


class LedgerPeriodDateTests(IsolatedAsyncioTestCase):
    async def test_ledger_normalizes_dash_dates(self) -> None:
        cap: list = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            cap.append((sql, params))
            return []

        with patch.object(svc, "execute_query", side_effect=fake):
            await svc.ledger_query(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
            )
        _, params = cap[0]
        self.assertIn("2026.07.01", params)
        self.assertIn("2026.07.31", params)

    async def test_period_normalizes_and_kpi_scoped(self) -> None:
        cap: list = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            cap.append((sql, params))
            if "total" in sql:
                return [{"total": 0}]
            return []

        with patch.object(svc, "execute_query", side_effect=fake):
            await svc.period_report_query(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019",
            )
        kpi_sql, kpi_params = next((s, p) for s, p in cap if "publisher_count" in s)
        self.assertIn("2026.07.01", kpi_params)
        self.assertIn("5019", kpi_params, "KPI 에 hcode 스코프 바인딩")


class DailyDetailScopeTests(IsolatedAsyncioTestCase):
    async def test_detail_falls_back_to_login_scope(self) -> None:
        cap: list = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            cap.append((sql, params))
            return []

        with patch.object(svc, "execute_query", side_effect=fake), \
             patch.object(svc, "in_clause_lookup", return_value=[]):
            await svc.daily_report(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019", gcode=None, detail_for_hcode=None,
            )
        detail_sql, detail_params = next(
            (s, p) for s, p in cap if "s.Jubun AS idnum" in s
        )
        self.assertIn("s.Hcode=%s", detail_sql, "상세 무필터 크로스테넌트 차단")
        self.assertIn("5019", detail_params)


class InventoryCandidatesTests(IsolatedAsyncioTestCase):
    async def test_candidates_query_shape(self) -> None:
        cap: list = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            cap.append((sql, params))
            if sql.strip().upper().startswith("SELECT COUNT("):
                return [{"total": 1}]
            return [{"id": 7, "Gdate": "2026.07.01", "Hcode": "5019", "Jubun": "0001",
                     "Bcode": "B0001", "gsqut": 3, "gbigo": ""}]

        with patch.object(svc, "execute_query", side_effect=fake), \
             patch.object(svc, "_fetch_product_names", return_value={"B0001": "책"}):
            res = await svc.list_inventory_candidates(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019",
            )
        list_sql = cap[0][0]
        self.assertIn("Gubun='반품'", list_sql)
        self.assertIn("Scode='X'", list_sql)
        self.assertNotIn("Ocode", list_sql)
        self.assertNotIn("Yesno", list_sql)
        self.assertEqual(res["items"][0]["id"], 7)
        self.assertEqual(res["items"][0]["bname"], "책")


class RouterRegistrationTests(TestCase):
    def test_new_routes_registered(self) -> None:
        from app.main import app

        paths = {getattr(r, "path", "") for r in app.routes}
        for p in (
            "/api/v1/returns/inventory-candidates",
            "/api/v1/returns/export.xlsx",
            "/api/v1/returns/ledger/export.xlsx",
            "/api/v1/returns/period-report/export.xlsx",
            "/api/v1/returns/reports/daily/export.xlsx",
        ):
            self.assertIn(p, paths, f"missing: {p}")


if __name__ == "__main__":
    main()
