"""재고관리 메뉴 hcode/bcode 옵셔널화 회귀 — DEC-033 (f) + (h).

대상 함수
---------
- ``app.services.inventory_service.get_inventory_ledger`` (Sobo44_inv 재고현황,
  Sobo33_ledger 도서수불장 의 공통 백엔드).

검증 포인트
-----------
1. ``hcode`` 빈/None/'%' → 모든 메인 SQL(count/dates/raw) 에 ``Hcode = %s`` 절 미포함.
2. ``bcode`` 빈/None  → 모든 메인 SQL 에 ``Bcode = %s`` / ``Bcode BETWEEN`` 절 미포함.
3. 페이지 raw 행 수 > ``LEDGER_MAX`` 안전망 → ``truncated=True``.
4. 도서명 lookup 은 항상 ``in_clause_lookup`` 으로 청크 분할 (DEC-033 (e)) — hcode 미입력 시
   helper 호출의 ``prefix_params`` 는 빈 튜플.
5. 일자(date_from/date_to) 는 항상 메인 SQL 의 첫 두 인자로 전달된다 (mysql3 stall 가드).
6. DEC-033 (h) — count/dates/raw 3-step 흐름 SQL 이 모두 발행된다.

격리
-----
- ``app.services.inventory_service.execute_query`` / ``in_clause_lookup`` 만 patch.
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


def _date_str(idx: int) -> str:
    return f"2026.04.{(idx % 28) + 1:02d}"


def _raw_row(date: str, idx: int) -> dict[str, Any]:
    return {
        "Gdate": date,
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
        total_dates: int = 1,
        rows_for_page_override: int | None = None,
    ) -> tuple[list[tuple[str, tuple[Any, ...]]], dict[str, Any], AsyncMock]:
        """공통 실행 헬퍼.

        Returns
        -------
        captured : list of (sql, params) for execute_query (opening / count / dates).
        result   : ``get_inventory_ledger`` 반환 dict.
        spy      : in_clause_lookup AsyncMock — 호출 인자 검증용.
        """
        from app.services import inventory_service as inv

        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append((sql, tuple(params)))
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "COUNT(DISTINCT Gdate)" in sql:
                return [{"cnt": total_dates}]
            if sql.lstrip().startswith("SELECT DISTINCT Gdate"):
                lim_p, off_p = params[-2], params[-1]
                end = min(off_p + lim_p, total_dates)
                return [{"Gdate": _date_str(i)} for i in range(off_p, end)]
            return []

        # 도서명 lookup spy + raw 행 fetch 시뮬레이터.
        # in_clause_lookup 은 (a) raw 행 fetch (S1_Ssub), (b) 도서명 lookup (G4_Book)
        # 두 용도로 호출되므로 sql_template 으로 구분.
        book_lookup_calls: list[dict[str, Any]] = []

        async def fake_in_lookup(
            server_id: str,
            *,
            sql_template: str,
            keys: Any,
            prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "G4_Book" in sql_template:
                book_lookup_calls.append({
                    "sql_template": sql_template,
                    "prefix_params": prefix_params,
                    "keys": list(keys),
                })
                return []
            keys_list = list(keys)
            if rows_for_page_override is not None:
                base = keys_list[0] if keys_list else "2026.04.01"
                return [_raw_row(base, i) for i in range(rows_for_page_override)]
            return [_raw_row(d, i) for i, d in enumerate(keys_list)]

        spy = AsyncMock(side_effect=fake_in_lookup)
        spy.book_lookup_calls = book_lookup_calls  # type: ignore[attr-defined]
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

    @staticmethod
    def _last_book_lookup(spy: AsyncMock) -> dict[str, Any] | None:
        calls = getattr(spy, "book_lookup_calls", [])
        return calls[-1] if calls else None

    @staticmethod
    def _main_sqls(captured: list[tuple[str, tuple[Any, ...]]]) -> list[tuple[str, tuple[Any, ...]]]:
        """opening(Sv_Ghng) 이후 발행된 메인 SQL(count + dates) 만 반환."""
        return [(s, p) for s, p in captured if "Sv_Ghng" not in s]

    async def test_hcode_none_drops_hcode_clause(self) -> None:
        captured, result, spy = await self._run_case(hcode=None, bcode="B0001")
        opening_sql, opening_params = captured[0]
        self.assertIn("Sv_Ghng", opening_sql)
        self.assertNotIn("Hcode", opening_sql, "hcode 미입력 시 이월 SQL 에 Hcode 절 없음")
        self.assertEqual(opening_params, ("2026.04.01",))
        for sql, params in self._main_sqls(captured):
            self.assertNotIn("Hcode = %s", sql)
            self.assertEqual(params[:2], ("2026.04.01", "2026.04.30"))
        # bcode 는 입력됐으므로 메인 SQL 에 포함.
        self.assertTrue(any("Bcode = %s" in s for s, _ in self._main_sqls(captured)))
        last = self._last_book_lookup(spy)
        self.assertIsNotNone(last)
        self.assertEqual(last["prefix_params"], ())
        self.assertFalse(result["truncated"])

    async def test_hcode_empty_string_treated_as_none(self) -> None:
        captured, _, spy = await self._run_case(hcode="   ", bcode="B0001")
        for sql, _ in self._main_sqls(captured):
            self.assertNotIn("Hcode = %s", sql)
        last = self._last_book_lookup(spy)
        self.assertIsNotNone(last)
        self.assertEqual(last["prefix_params"], ())

    async def test_hcode_percent_treated_as_none(self) -> None:
        captured, _, spy = await self._run_case(hcode="%", bcode="B0001")
        for sql, _ in self._main_sqls(captured):
            self.assertNotIn("Hcode = %s", sql,
                             "Sobo33_ledger 의 '%' 트릭은 None 으로 정규화돼야 함")
        last = self._last_book_lookup(spy)
        self.assertIsNotNone(last)
        self.assertEqual(last["prefix_params"], ())

    async def test_bcode_none_drops_bcode_clause(self) -> None:
        captured, _, _ = await self._run_case(hcode="H001", bcode=None)
        for sql, _ in self._main_sqls(captured):
            self.assertNotIn("Bcode = %s", sql)
            self.assertNotIn("Bcode BETWEEN", sql)
            self.assertIn("Hcode = %s", sql, "hcode 입력 시 Hcode 절 유지")

    async def test_bcode_range_keeps_between_clause(self) -> None:
        captured, _, _ = await self._run_case(
            hcode="H001", bcode="B0001", bcode_to="B0010"
        )
        # count + dates 두 SQL 모두 BETWEEN 절을 가져야 한다.
        mains = self._main_sqls(captured)
        self.assertTrue(mains)
        for sql, params in mains:
            self.assertIn("Bcode BETWEEN %s AND %s", sql)
            self.assertIn("B0001", params)
            self.assertIn("B0010", params)

    async def test_all_optional_drops_both_clauses(self) -> None:
        captured, _, spy = await self._run_case(hcode=None, bcode=None)
        for sql, _ in self._main_sqls(captured):
            self.assertNotIn("Hcode = %s", sql)
            # SELECT 절에는 Bcode 컬럼이 남아 있을 수 있어 WHERE 토큰만 검사.
            self.assertNotIn("Bcode = %s", sql)
            self.assertNotIn("Bcode BETWEEN", sql)
        last = self._last_book_lookup(spy)
        self.assertIsNotNone(last)
        self.assertEqual(last["prefix_params"], ())
        self.assertNotIn("Hcode=%s", last["sql_template"])

    async def test_truncated_when_page_raw_exceeds_limit(self) -> None:
        from app.services import inventory_service as inv
        # 페이지 단위 raw 안전망 — LEDGER_MAX + 1 행 시 truncated=True.
        _, result, _ = await self._run_case(
            hcode="H001",
            bcode="B0001",
            total_dates=20,
            rows_for_page_override=inv.LEDGER_MAX + 1,
        )
        self.assertTrue(result["truncated"])

    async def test_not_truncated_when_below_limit(self) -> None:
        _, result, _ = await self._run_case(
            hcode="H001",
            bcode="B0001",
            total_dates=10,
            rows_for_page_override=10,
        )
        self.assertFalse(result["truncated"])

    async def test_lookup_uses_in_clause_lookup_with_hcode(self) -> None:
        _, _, spy = await self._run_case(hcode="H001", bcode="B0001")
        last = self._last_book_lookup(spy)
        self.assertIsNotNone(last)
        self.assertEqual(last["prefix_params"], ("H001",))
        self.assertIn("Hcode=%s", last["sql_template"])

    async def test_three_step_sqls_emitted(self) -> None:
        # DEC-033 (h) — opening + count + dates 3개 execute_query 호출이 발행돼야 한다
        # (raw 행 fetch 는 in_clause_lookup 경로).
        captured, _, _ = await self._run_case(
            hcode="H001", bcode="B0001", total_dates=5
        )
        sqls = [s for s, _ in captured]
        self.assertTrue(any("Sv_Ghng" in s for s in sqls), "opening SQL 필수")
        self.assertTrue(any("COUNT(DISTINCT Gdate)" in s for s in sqls), "count SQL 필수")
        self.assertTrue(
            any(s.lstrip().startswith("SELECT DISTINCT Gdate") for s in sqls),
            "dates page SQL 필수",
        )


if __name__ == "__main__":  # pragma: no cover
    main()
