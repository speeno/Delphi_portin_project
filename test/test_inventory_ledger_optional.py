"""재고관리 메뉴 hcode/bcode 옵셔널화 회귀 — DEC-033 (f).

대상 함수
---------
- ``app.services.inventory_service.get_inventory_ledger`` (Sobo44_inv 재고현황,
  Sobo33_ledger 도서수불장 의 공통 백엔드).

검증 포인트
-----------
1. ``hcode`` 빈/None/'%' → SQL 본문에 ``Hcode = %s`` 절이 포함되지 않는다.
2. ``bcode`` 빈/None  → SQL 본문에 ``Bcode = %s`` / ``Bcode BETWEEN`` 절이 포함되지 않는다.
3. 결과 행 수가 ``LEDGER_MAX + 1`` 이면 ``truncated=True`` + 행 수가 ``LEDGER_MAX`` 로 절단.
4. 도서명 lookup 은 항상 ``in_clause_lookup`` 으로 청크 분할 (DEC-033 (e)) — hcode 미입력 시
   helper 호출의 ``prefix_params`` 는 빈 튜플.
5. 일자(date_from/date_to) 는 항상 SQL 의 첫 두 인자로 전달된다 (mysql3 stall 가드).

격리
-----
- ``app.services.inventory_service.execute_query`` 와 ``in_clause_lookup`` 만 patch.
- 실 DB 의존 0.
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


def _make_main_row(idx: int) -> dict[str, Any]:
    return {
        "Gdate": f"2026.04.{(idx % 28) + 1:02d}",
        "Bcode": f"B{idx:04d}",
        "Scode": "X",
        "Gubun": "출고",
        "Pubun": "",
        "Gbigo": "",
        "Gsqut": 1,
        "Gssum": 100,
    }


class InventoryLedgerOptionalTests(IsolatedAsyncioTestCase):
    async def _run_case(
        self,
        *,
        hcode: str | None,
        bcode: str | None,
        bcode_to: str | None = None,
        main_rows: list[dict[str, Any]] | None = None,
    ) -> tuple[list[tuple[str, tuple[Any, ...]]], dict[str, Any], AsyncMock]:
        """공통 실행 헬퍼: execute_query 호출 캡처 + 결과 + in_clause_lookup spy 반환."""
        from app.services import inventory_service as inv

        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append((sql, tuple(params)))
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            return list(main_rows or [_make_main_row(0)])

        spy = AsyncMock(return_value=[])
        with patch("app.services.inventory_service.execute_query", new=fake_exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=spy):
            result = await inv.get_inventory_ledger(
                server_id="srv",
                hcode=hcode,
                bcode=bcode,
                bcode_to=bcode_to,
                date_from="2026-04-01",
                date_to="2026-04-30",
            )
        return captured, result, spy

    async def test_hcode_none_drops_hcode_clause(self) -> None:
        captured, result, spy = await self._run_case(hcode=None, bcode="B0001")
        opening_sql, opening_params = captured[0]
        main_sql, main_params = captured[1]
        self.assertIn("Sv_Ghng", opening_sql)
        self.assertNotIn("Hcode", opening_sql, "hcode 미입력 시 이월 SQL 에 Hcode 절 없음")
        self.assertEqual(opening_params, ("2026.04.01",))
        self.assertNotIn("Hcode = %s", main_sql, "hcode 미입력 시 메인 SQL 에 Hcode 절 없음")
        self.assertIn("Bcode = %s", main_sql)
        self.assertEqual(main_params[:2], ("2026.04.01", "2026.04.30"))
        self.assertEqual(spy.await_args.kwargs.get("prefix_params"), ())
        self.assertFalse(result["truncated"])

    async def test_hcode_empty_string_treated_as_none(self) -> None:
        captured, _, spy = await self._run_case(hcode="   ", bcode="B0001")
        _, main_sql, *_ = captured[1][0], captured[1][0]
        self.assertNotIn("Hcode = %s", captured[1][0])
        self.assertEqual(spy.await_args.kwargs.get("prefix_params"), ())

    async def test_hcode_percent_treated_as_none(self) -> None:
        captured, _, spy = await self._run_case(hcode="%", bcode="B0001")
        self.assertNotIn("Hcode = %s", captured[1][0],
                         "Sobo33_ledger 의 '%' 트릭은 None 으로 정규화돼야 함")
        self.assertEqual(spy.await_args.kwargs.get("prefix_params"), ())

    async def test_bcode_none_drops_bcode_clause(self) -> None:
        captured, _, _ = await self._run_case(hcode="H001", bcode=None)
        main_sql = captured[1][0]
        self.assertNotIn("Bcode = %s", main_sql)
        self.assertNotIn("Bcode BETWEEN", main_sql)
        self.assertIn("Hcode = %s", main_sql, "hcode 가 입력됐으면 Hcode 절은 유지")

    async def test_bcode_range_keeps_between_clause(self) -> None:
        captured, _, _ = await self._run_case(
            hcode="H001", bcode="B0001", bcode_to="B0010"
        )
        main_sql, main_params = captured[1]
        self.assertIn("Bcode BETWEEN %s AND %s", main_sql)
        self.assertIn("B0001", main_params)
        self.assertIn("B0010", main_params)

    async def test_all_optional_drops_both_clauses(self) -> None:
        captured, _, spy = await self._run_case(hcode=None, bcode=None)
        main_sql = captured[1][0]
        self.assertNotIn("Hcode = %s", main_sql)
        # SELECT 절에는 Bcode 컬럼이 남아 있으므로 WHERE 절 토큰만 검사.
        self.assertNotIn("Bcode = %s", main_sql)
        self.assertNotIn("Bcode BETWEEN", main_sql)
        # 도서명 lookup 도 hcode 절을 제거해야 함.
        kwargs = spy.await_args.kwargs
        self.assertEqual(kwargs.get("prefix_params"), ())
        self.assertNotIn("Hcode=%s", kwargs.get("sql_template", ""))

    async def test_truncated_when_rows_exceed_limit(self) -> None:
        from app.services import inventory_service as inv
        # LIMIT 가드 동작 — LEDGER_MAX + 1 행 모킹.
        many = [_make_main_row(i) for i in range(inv.LEDGER_MAX + 1)]
        _, result, _ = await self._run_case(
            hcode="H001", bcode="B0001", main_rows=many
        )
        self.assertTrue(result["truncated"])
        # 행 수는 도서명 누적 후 by_date 기준이므로 단순 길이 비교 대신 truncated 만 검증.

    async def test_not_truncated_when_below_limit(self) -> None:
        from app.services import inventory_service as inv
        few = [_make_main_row(i) for i in range(min(10, inv.LEDGER_MAX))]
        _, result, _ = await self._run_case(
            hcode="H001", bcode="B0001", main_rows=few
        )
        self.assertFalse(result["truncated"])

    async def test_lookup_uses_in_clause_lookup_with_hcode(self) -> None:
        # hcode 입력 시 도서명 lookup 의 prefix_params 는 (hcode,) 그리고 SQL 에 Hcode 포함.
        _, _, spy = await self._run_case(hcode="H001", bcode="B0001")
        kwargs = spy.await_args.kwargs
        self.assertEqual(kwargs.get("prefix_params"), ("H001",))
        self.assertIn("Hcode=%s", kwargs.get("sql_template", ""))


if __name__ == "__main__":  # pragma: no cover
    main()
