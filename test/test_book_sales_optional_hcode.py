"""Sobo33_1_ledger(통합 도서수불장) 백엔드 hcode 옵셔널화 회귀 — DEC-033 (f).

대상 함수
---------
- ``app.services.reports_service.get_book_sales`` (Sobo33_1_ledger /ledger/book-integrated 의
  실제 백엔드 — Sobo61 도서별 판매 SQL-INQ-7/8 공유).

검증 포인트
-----------
1. ``hcode`` 가 None/빈/'%' 이면 SQL-INQ-7 본문에 ``Hcode = %s`` 절이 빠진다.
2. ``hcode`` 가 None/빈/'%' 이면 SQL-INQ-8 (Sg_Csum 후처리) 본문에서도 ``Hcode = %s`` 절이 빠진다.
3. 도서명 lookup 의 ``in_clause_lookup`` 호출은 hcode 미입력 시 prefix_params 가 빈 튜플,
   sql_template 에 ``Hcode=`` 가 없다 (DEC-033 (e) + (f)).
4. ``hcode`` 가 입력된 정상 경로에서는 기존 SQL 모양과 prefix_params 가 보존된다 (회귀 가드).

격리
-----
- ``app.services.reports_service.execute_query`` + ``in_clause_lookup`` 만 patch.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _main_row(bcode: str = "B0001") -> dict[str, Any]:
    return {
        "Bcode": bcode,
        "Scode": "X",
        "Gubun": "출고",
        "Pubun": "",
        "Gsqut": 1,
        "Gssum": 100,
    }


class BookSalesOptionalHcodeTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        hcode: str | None,
    ) -> tuple[list[tuple[str, tuple[Any, ...]]], AsyncMock]:
        from app.services import reports_service as rs

        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append((sql, tuple(params)))
            if "S1_Ssub" in sql:
                return [_main_row()]
            # Sg_Csum
            return []

        spy = AsyncMock(return_value=[])
        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=spy):
            await rs.get_book_sales(
                server_id="srv",
                hcode=hcode,
                date_from="2026-04-01",
                date_to="2026-04-30",
            )
        return captured, spy

    async def test_hcode_none_drops_clause_in_main_and_waste(self) -> None:
        captured, spy = await self._run(hcode=None)
        # 첫 호출 = SQL-INQ-7 (S1_Ssub)
        s1_sql = captured[0][0]
        self.assertIn("S1_Ssub", s1_sql)
        self.assertNotIn("Hcode = %s", s1_sql)
        # 두 번째 호출 = SQL-INQ-8 (Sg_Csum)
        sg_sql = captured[1][0]
        self.assertIn("Sg_Csum", sg_sql)
        self.assertNotIn("Hcode = %s", sg_sql)
        # 도서명 lookup
        kwargs = spy.await_args.kwargs
        self.assertEqual(kwargs.get("prefix_params"), ())
        self.assertNotIn("Hcode=%s", kwargs.get("sql_template", ""))

    async def test_hcode_blank_treated_as_none(self) -> None:
        captured, spy = await self._run(hcode="   ")
        self.assertNotIn("Hcode = %s", captured[0][0])
        self.assertEqual(spy.await_args.kwargs.get("prefix_params"), ())

    async def test_hcode_percent_treated_as_none(self) -> None:
        captured, spy = await self._run(hcode="%")
        self.assertNotIn("Hcode = %s", captured[0][0])
        self.assertEqual(spy.await_args.kwargs.get("prefix_params"), ())

    async def test_hcode_present_keeps_clause(self) -> None:
        # 회귀 가드 — 정상 경로에서는 기존 SQL 모양 보존.
        captured, spy = await self._run(hcode="H001")
        s1_sql, s1_params = captured[0]
        self.assertIn("Hcode = %s", s1_sql)
        self.assertIn("H001", s1_params)
        sg_sql, sg_params = captured[1]
        self.assertIn("Hcode = %s", sg_sql)
        self.assertIn("H001", sg_params)
        kwargs = spy.await_args.kwargs
        self.assertEqual(kwargs.get("prefix_params"), ("H001",))
        self.assertIn("Hcode=%s", kwargs.get("sql_template", ""))


if __name__ == "__main__":  # pragma: no cover
    main()
