"""재고관리 메뉴 일자 SQL 페이지네이션 회귀 — DEC-033 (g→h).

대상 함수
---------
- ``app.services.inventory_service.get_inventory_ledger`` (Sobo44_inv 재고현황,
  Sobo33_ledger 도서수불장 의 공통 백엔드).

검증 포인트
-----------
1. 응답 dict 에 ``page`` (limit/offset/total/has_more) + ``total`` 필드가 항상 존재.
2. ``COUNT(DISTINCT Gdate)`` 결과가 ``page.total`` 로 노출된다.
3. ``SELECT DISTINCT Gdate ... LIMIT/OFFSET`` 으로 페이지의 일자만 fetch 한다.
4. raw 행 fetch (``IN (page_dates)``) 가 페이지에 한정되므로 truncated 는 사실상 미발생.
5. ``has_more`` 신호 = (offset + returned < total).
6. ``limit`` 미지정 시 기본값(100) + ``ceil`` 상한(2000) ``clamp_limit`` 정책 적용.
7. raw 행이 LEDGER_MAX 초과 안전망 — truncated=True (페이지네이션과 직교 유지).
8. ``rows`` 결과가 비어 있어도 ``page.total=0`` / ``page.has_more=False`` 로 반환.

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
    day = (idx % 28) + 1
    month = ((idx // 28) % 12) + 1
    return f"2026.{month:02d}.{day:02d}"


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


class InventoryLedgerPagingTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        total_dates: int,
        rows_per_date: int = 1,
        rows_for_page_override: int | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[dict[str, Any], list[tuple[str, tuple[Any, ...]]], list[dict[str, Any]]]:
        """SQL-aware mock 으로 새 3-step 아키텍처를 재현.

        Parameters
        ----------
        total_dates
            ``COUNT(DISTINCT Gdate)`` 가 반환할 가상 일자 수 (= page.total).
        rows_per_date
            in_clause_lookup 으로 fetch 되는 일자별 raw 행 수 (truncated 시뮬레이션).
        rows_for_page_override
            in_clause_lookup 결과 행 총수를 강제 지정 (truncated 회귀 가드 용).
        """
        from app.services import inventory_service as inv

        captured_sql: list[tuple[str, tuple[Any, ...]]] = []
        page_dates_holder: list[str] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append((sql, tuple(params)))
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "COUNT(DISTINCT Gdate)" in sql:
                return [{"cnt": total_dates}]
            if sql.lstrip().startswith("SELECT DISTINCT Gdate"):
                lim_p, off_p = params[-2], params[-1]
                end = min(off_p + lim_p, total_dates)
                dates = [_date_str(i) for i in range(off_p, end)]
                page_dates_holder.extend(dates)
                return [{"Gdate": d} for d in dates]
            return []

        async def fake_in_lookup(
            server_id: str,
            *,
            sql_template: str,
            keys: Any,
            prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "G4_Book" in sql_template:
                return []
            keys_list = list(keys)
            if rows_for_page_override is not None:
                base = keys_list[0] if keys_list else "2026.01.01"
                return [_raw_row(base, i) for i in range(rows_for_page_override)]
            return [
                _raw_row(d, i * 100 + j)
                for i, d in enumerate(keys_list)
                for j in range(rows_per_date)
            ]

        with patch("app.services.inventory_service.execute_query", new=fake_exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=fake_in_lookup):
            result = await inv.get_inventory_ledger(
                server_id="srv",
                hcode=None,
                bcode=None,
                bcode_to=None,
                date_from="2026-01-01",
                date_to="2026-12-31",
                limit=limit,
                offset=offset,
            )
        return result, captured_sql, [{"Gdate": d} for d in page_dates_holder]

    async def test_page_meta_always_present(self) -> None:
        result, _, _ = await self._run(total_dates=10)
        self.assertIn("page", result)
        self.assertIn("total", result)
        for key in ("limit", "offset", "total", "has_more"):
            self.assertIn(key, result["page"], f"page.{key} 필수")

    async def test_total_uses_count_distinct(self) -> None:
        # total = COUNT(DISTINCT Gdate) 결과를 그대로 노출.
        result, captured, _ = await self._run(total_dates=42, limit=10)
        self.assertEqual(result["page"]["total"], 42)
        self.assertEqual(result["total"], 42)
        # COUNT 쿼리가 발행되었는지 확인.
        count_sqls = [s for s, _ in captured if "COUNT(DISTINCT Gdate)" in s]
        self.assertTrue(count_sqls, "COUNT(DISTINCT Gdate) SQL 발행 필수")

    async def test_default_limit_when_not_specified(self) -> None:
        result, _, _ = await self._run(total_dates=5, limit=None)
        self.assertEqual(result["page"]["limit"], 100)
        self.assertEqual(result["page"]["offset"], 0)
        self.assertEqual(result["page"]["total"], 5)
        self.assertFalse(result["page"]["has_more"])
        self.assertEqual(len(result["rows"]), 5)

    async def test_limit_offset_paginates_dates(self) -> None:
        # total=30, limit=10, offset=10 → 일자 10개 page → rows 10개 (each date 1 row).
        result, captured, _ = await self._run(total_dates=30, limit=10, offset=10)
        self.assertEqual(result["page"]["limit"], 10)
        self.assertEqual(result["page"]["offset"], 10)
        self.assertEqual(result["page"]["total"], 30)
        self.assertEqual(len(result["rows"]), 10)
        self.assertTrue(result["page"]["has_more"])
        # SELECT DISTINCT Gdate 쿼리가 발행되었는지 확인.
        dates_sqls = [s for s, _ in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
        self.assertTrue(dates_sqls)

    async def test_last_page_has_more_false(self) -> None:
        result, _, _ = await self._run(total_dates=25, limit=10, offset=20)
        self.assertEqual(len(result["rows"]), 5)
        self.assertFalse(result["page"]["has_more"])

    async def test_empty_result_skips_dates_and_raw_queries(self) -> None:
        result, captured, _ = await self._run(total_dates=0, limit=50)
        self.assertEqual(result["rows"], [])
        self.assertEqual(result["page"]["total"], 0)
        self.assertFalse(result["page"]["has_more"])
        self.assertFalse(result["truncated"])
        # total=0 이면 dates page / raw 쿼리는 발행되지 않아야 한다 (round-trip 절감).
        dates_sqls = [s for s, _ in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
        self.assertFalse(dates_sqls, "total=0 이면 dates page SQL 미발행")

    async def test_limit_ceiling_clamped(self) -> None:
        result, _, _ = await self._run(total_dates=10, limit=5000)
        self.assertEqual(result["page"]["limit"], 2000)

    async def test_truncated_flag_safety_net(self) -> None:
        from app.services import inventory_service as inv
        # 페이지 raw 가 LEDGER_MAX + 1 → truncated=True (안전망).
        result, _, _ = await self._run(
            total_dates=20,
            limit=20,
            rows_for_page_override=inv.LEDGER_MAX + 1,
        )
        self.assertTrue(result["truncated"])
        self.assertEqual(result["page"]["limit"], 20)


if __name__ == "__main__":  # pragma: no cover
    main()
