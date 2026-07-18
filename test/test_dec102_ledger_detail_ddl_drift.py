"""DEC-102 — 기간별 재고원장 도서별 누계 상세: S1_Ssub 재고변동 컬럼 부재 회귀.

증상(2026-07-17): 재고원장 도서별 누계에서 도서 행을 선택(detailForBcode)하면
``returns_ledger_failed: OperationalError: (1054, "Unknown column 's.Giqut'")`` 500.

원인: 상세 SQL(SQL-RT-29)이 S1_Ssub 에서 Giqut/Goqut/Gjqut/Gbqut 등 재고변동
컬럼을 고정 SELECT — 해당 컬럼이 없는 테넌트에서 1054. DEC-033 대로 존재 컬럼만
SELECT(부재 컬럼 0 별칭), Idnum 부재 시 ORDER BY 에서도 제거한다.

본 테스트는 S1_Ssub 에 재고변동/Idnum 컬럼이 없는 테넌트를 모사(SHOW COLUMNS 목킹)해
발행 SQL 에 부재 컬럼 참조가 없고 alias 는 유지됨을 고정한다.
"""
from __future__ import annotations

from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch


class LedgerDetailDdlDriftTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        from app.services.s1_ssub_adapt import clear_s1_column_cache_for_tests

        clear_s1_column_cache_for_tests()

    async def _run(self, present_cols: set[str]) -> str:
        """detail_for_bcode 로 상세를 트리거하고, 상세 SELECT 로 발행된 SQL 을 돌려준다."""
        from app.services import returns_service as svc

        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_execute(server_id: str, sql: str, params: tuple = ()):  # noqa: ARG001
            captured.append((sql, params))
            return []

        with patch.object(svc, "execute_query", side_effect=fake_execute), \
             patch.object(svc, "s1_column_names", new=AsyncMock(return_value=present_cols)), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={})), \
             patch.object(svc, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(svc, "build_d_select_clause", new=AsyncMock(return_value="1=1")):
            await svc.ledger_query(
                server_id="remote_153",
                date_from="2026-07-01",
                date_to="2026-07-31",
                detail_for_bcode="B0001",
            )
        detail_sql = next(
            (s for s, _ in captured if " FROM S1_Ssub s " in s and "gname" in s),
            "",
        )
        self.assertTrue(detail_sql, "상세 SQL 미발행")
        return detail_sql

    async def test_missing_metric_columns_no_reference(self) -> None:
        """재고변동 컬럼 부재 테넌트 — 발행 SQL 에 s.Giqut 등 참조 없음, 0 별칭 유지."""
        # Idnum 도 없고 재고변동 컬럼도 없는 최소 스키마.
        cols = {"gdate", "gubun", "gcode", "hcode", "bcode", "gsqut", "gssum"}
        sql = await self._run(cols)
        for absent in ("s.Giqut", "s.Gisum", "s.Goqut", "s.Gosum",
                       "s.Gjqut", "s.Gjsum", "s.Gbqut", "s.Gbsum"):
            self.assertNotIn(absent, sql, f"부재 컬럼 참조 잔존: {absent}")
        # alias 는 전부 유지(프론트 계약 보존).
        for alias in ("giqut", "goqut", "gjqut", "gbqut", "gsqut", "gssum"):
            self.assertIn(f"AS {alias}", sql)
        # Idnum 부재 → ORDER BY 에 Idnum 없음.
        self.assertNotIn("s.Idnum", sql)
        self.assertIn("ORDER BY s.Gdate", sql)
        # 존재하는 metric(gsqut/gssum)은 COALESCE 로 실제 컬럼 참조.
        self.assertIn("COALESCE(s.Gsqut,0) AS gsqut", sql)

    async def test_present_metric_columns_referenced(self) -> None:
        """재고변동 컬럼 존재 테넌트 — 실제 컬럼을 COALESCE 로 참조(기존 동작 보존)."""
        cols = {
            "gdate", "gubun", "gcode", "hcode", "bcode", "idnum",
            "giqut", "gisum", "goqut", "gosum", "gjqut", "gjsum",
            "gbqut", "gbsum", "gsqut", "gssum",
        }
        sql = await self._run(cols)
        self.assertIn("COALESCE(s.Giqut,0) AS giqut", sql)
        self.assertIn("COALESCE(s.Gbsum,0) AS gbsum", sql)
        self.assertIn("s.Idnum", sql)  # Idnum 존재 → ORDER BY 포함


if __name__ == "__main__":
    from unittest import main

    main()
