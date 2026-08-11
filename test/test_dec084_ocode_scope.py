"""DEC-084 — 도서구분(Ocode) 스코프 기본값 회귀 가드.

배경
----
chul_09 계열(운영 4서버 전부)의 출고·입고·거래명세서 실데이터는 ``Ocode='A'``
(일부 레거시 입고 ``''``/NULL) 로 기록되는데, 통계·원장 계열이 ``'%B%'``/``'B'``
를 하드 기본으로 필터링해 "완료 거래가 통계에 안 잡히는" 사고가 났다.
레거시 정본: Subu61/67 기본 ``Ocode LIKE '%%'``(전체), Subu62 는 Ocode 절 없음.

가드 포인트
-----------
1. get_book_sales / get_publisher_sales_summary / get_inventory_ledger /
   customer ledger(단일·통합) — scope 미지정 시 Ocode 절 미부착(전체).
2. scope 'A'/'B' 명시 시에만 LIKE 필터 부착.
3. get_customer_sales — Ocode 절 자체가 없어야 한다(Subu62 원본 동등).
4. 통합 거래처원장 — Ocode 파라미터가 Hcode 파라미터보다 먼저 바인딩
   (종전엔 마지막에 append 되어 ``Hcode='%B%'`` 로 어긋나던 버그).
5. stats_service 위임 경로 — scope=None 전달(전체 집계).
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


class _SqlCapture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def exec(self, server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        self.calls.append((sql, tuple(params)))
        if "COUNT(DISTINCT Gdate)" in sql or "COUNT(DISTINCT Hcode)" in sql:
            return [{"cnt": 0}]
        if "Sv_Ghng" in sql:
            return [{"opening_date": None}]
        return []

    async def in_lookup(self, server_id: str, *, sql_template: str, keys: Any,
                        prefix_params: tuple = (), chunk_size: int | None = None):
        return []


class BookSalesOcodeScopeTests(IsolatedAsyncioTestCase):
    async def _run(self, scope: str | None) -> _SqlCapture:
        from app.services import reports_service as rpt
        cap = _SqlCapture()
        with patch("app.services.reports_service.execute_query", new=cap.exec), \
             patch("app.services.reports_service.in_clause_lookup", new=cap.in_lookup):
            await rpt.get_book_sales(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31", scope=scope,
            )
        return cap

    async def test_default_scope_drops_ocode(self) -> None:
        cap = await self._run(scope=None)
        main_sql = cap.calls[0][0]
        self.assertIn("FROM S1_Ssub", main_sql)
        self.assertNotIn("Ocode", main_sql)

    async def test_explicit_scope_keeps_like(self) -> None:
        for sc, pat in (("A", "%A%"), ("B", "%B%")):
            cap = await self._run(scope=sc)
            main_sql, main_params = cap.calls[0]
            self.assertIn("Ocode LIKE %s", main_sql)
            self.assertIn(pat, main_params)

    async def test_customer_sales_has_no_ocode_clause(self) -> None:
        from app.services import reports_service as rpt
        cap = _SqlCapture()
        with patch("app.services.reports_service.execute_query", new=cap.exec), \
             patch("app.services.reports_service.in_clause_lookup", new=cap.in_lookup):
            await rpt.get_customer_sales(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31",
            )
        main_sql = cap.calls[0][0]
        self.assertNotIn("Ocode", main_sql)  # Subu62 원본 — Ocode 필터 없음
        self.assertIn("Scode = %s", main_sql)

    async def test_publisher_summary_default_drops_ocode(self) -> None:
        from app.services import reports_service as rpt
        cap = _SqlCapture()
        with patch("app.services.reports_service.execute_query", new=cap.exec), \
             patch("app.services.reports_service.in_clause_lookup", new=cap.in_lookup):
            await rpt.get_publisher_sales_summary(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31",
            )
        self.assertNotIn("Ocode", cap.calls[0][0])


class InventoryLedgerOcodeScopeTests(IsolatedAsyncioTestCase):
    async def _run(self, scope: str | None) -> _SqlCapture:
        from app.services import inventory_service as inv
        cap = _SqlCapture()
        with patch("app.services.inventory_service.execute_query", new=cap.exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=cap.in_lookup):
            await inv.get_inventory_ledger(
                server_id="srv", hcode=None, bcode=None, bcode_to=None,
                date_from="2026-01-01", date_to="2026-01-31", scope=scope,
            )
        return cap

    async def test_default_scope_drops_ocode(self) -> None:
        cap = await self._run(scope=None)
        count_sql = [s for s, _ in cap.calls if "COUNT(DISTINCT Gdate)" in s][0]
        self.assertNotIn("Ocode", count_sql)

    async def test_explicit_scope_keeps_like(self) -> None:
        cap = await self._run(scope="B")
        count_sql, count_params = [c for c in cap.calls if "COUNT(DISTINCT Gdate)" in c[0]][0]
        self.assertIn("Ocode LIKE %s", count_sql)
        self.assertIn("%B%", count_params)


class IntegratedLedgerParamOrderTests(IsolatedAsyncioTestCase):
    async def _run(self, *, scope: str, scope_hcode: str) -> _SqlCapture:
        from app.services import customer_ledger_service as cls_
        cap = _SqlCapture()
        with patch("app.services.customer_ledger_service.execute_query", new=cap.exec), \
             patch("app.services.customer_ledger_service.in_clause_lookup", new=cap.in_lookup):
            await cls_.get_integrated_customer_ledger(
                server_id="srv", date_from="2026-01-01", date_to="2026-01-31",
                scope=scope, scope_hcode=scope_hcode,
            )
        return cap

    async def test_ocode_binds_before_hcode(self) -> None:
        """종전 버그 — ocode 파라미터가 마지막에 append 되어 Hcode 절에 '%B%' 바인딩."""
        cap = await self._run(scope="B", scope_hcode="5019")
        # DEC-137 — 통합 원장 페이지네이션 축 = 거래처(Gcode). Hcode 는 격리 스코프 절.
        count_sql, count_params = [c for c in cap.calls if "COUNT(DISTINCT Gcode)" in c[0]][0]
        # 절 순서: Gdate, Gdate, (Bdate), Ocode LIKE, Hcode = — 파라미터도 동일 순서.
        self.assertLess(count_sql.index("Ocode LIKE %s"), count_sql.index("Hcode = %s"))
        self.assertEqual(count_params[2], "%B%")
        self.assertEqual(count_params[3], "5019")

    async def test_all_scope_drops_ocode(self) -> None:
        cap = await self._run(scope="ALL", scope_hcode="5019")
        count_sql, count_params = [c for c in cap.calls if "COUNT(DISTINCT Gcode)" in c[0]][0]
        self.assertNotIn("Ocode", count_sql)
        self.assertEqual(count_params[2], "5019")


class StatsDelegationScopeTests(IsolatedAsyncioTestCase):
    async def test_sales_period_single_pass_no_ocode(self) -> None:
        """DEC-140 — 슬라이스별 get_book_sales 위임(N+1) 제거.

        일 단위 다구간이어도 S1_Ssub **단일 쿼리**여야 하고(30s 타임아웃 원인),
        DEC-084 정본대로 Ocode 절이 없어야 한다(도서구분 전체)."""
        from app.services import stats_service

        captured: list[str] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            return []

        with patch("app.services.reports_service.execute_query", new=fake_exec):
            await stats_service.get_sales_period(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31", group_by="daily",
            )
        s1 = [s for s in captured if "FROM S1_Ssub" in s]
        self.assertEqual(len(s1), 1, "일 단위 31구간이어도 단일 쿼리(N+1 금지)")
        self.assertNotIn("Ocode", s1[0])
        self.assertIn("GROUP BY Gdate", s1[0])


if __name__ == "__main__":  # pragma: no cover
    main()
