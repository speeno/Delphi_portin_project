"""재고관리 메뉴 일자 누적 페이지네이션 회귀 — DEC-033 (g).

대상 함수
---------
- ``app.services.inventory_service.get_inventory_ledger`` (Sobo44_inv 재고현황,
  Sobo33_ledger 도서수불장 의 공통 백엔드).

검증 포인트
-----------
1. 응답 dict 에 ``page`` (limit/offset/total/has_more) + ``total`` 필드가 항상 존재.
2. ``limit`` / ``offset`` 으로 일자(by_date) 누적 결과가 정확히 슬라이싱된다.
3. ``has_more`` 신호는 다음 페이지가 남았을 때 True (offset+returned < total).
4. ``truncated`` 플래그(raw 행 LIMIT 가드)는 페이지네이션과 독립으로 유지된다.
5. ``limit`` 미지정 시 기본값(100) + ``ceil`` 상한(2000) 정책이 ``clamp_limit`` 으로 적용된다.
6. ``rows`` 결과가 비어 있어도 ``page.total=0`` / ``page.has_more=False`` 로 반환.

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


def _row(idx: int) -> dict[str, Any]:
    """일자별 1행씩 — by_date 누적 후 N개 일자 = N개 결과 행."""
    day = (idx % 28) + 1
    month = ((idx // 28) % 12) + 1
    return {
        "Gdate": f"2026.{month:02d}.{day:02d}",
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
        raw_count: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> dict[str, Any]:
        from app.services import inventory_service as inv

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            return [_row(i) for i in range(raw_count)]

        spy = AsyncMock(return_value=[])
        with patch("app.services.inventory_service.execute_query", new=fake_exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=spy):
            return await inv.get_inventory_ledger(
                server_id="srv",
                hcode=None,
                bcode=None,
                bcode_to=None,
                date_from="2026-01-01",
                date_to="2026-12-31",
                limit=limit,
                offset=offset,
            )

    async def test_page_meta_always_present(self) -> None:
        result = await self._run(raw_count=10)
        self.assertIn("page", result)
        self.assertIn("total", result)
        page = result["page"]
        for key in ("limit", "offset", "total", "has_more"):
            self.assertIn(key, page, f"page.{key} 필수")

    async def test_default_limit_when_not_specified(self) -> None:
        # limit=None → clamp_limit 기본값(100).
        result = await self._run(raw_count=5, limit=None)
        self.assertEqual(result["page"]["limit"], 100)
        self.assertEqual(result["page"]["offset"], 0)
        self.assertEqual(result["page"]["total"], 5)
        self.assertFalse(result["page"]["has_more"])
        self.assertEqual(len(result["rows"]), 5)

    async def test_limit_offset_slices_aggregated_rows(self) -> None:
        # 일자가 모두 다른 30행(by_date 누적 후 30 결과 행)을 limit=10, offset=10 으로 페이징.
        result = await self._run(raw_count=30, limit=10, offset=10)
        self.assertEqual(result["page"]["limit"], 10)
        self.assertEqual(result["page"]["offset"], 10)
        self.assertEqual(result["page"]["total"], 30)
        self.assertEqual(len(result["rows"]), 10)
        self.assertTrue(result["page"]["has_more"], "offset+returned(20) < total(30) 이면 has_more=True")

    async def test_last_page_has_more_false(self) -> None:
        result = await self._run(raw_count=25, limit=10, offset=20)
        self.assertEqual(len(result["rows"]), 5)
        self.assertFalse(result["page"]["has_more"], "마지막 페이지는 has_more=False")

    async def test_empty_result_returns_zero_page(self) -> None:
        result = await self._run(raw_count=0, limit=50)
        self.assertEqual(result["rows"], [])
        self.assertEqual(result["page"]["total"], 0)
        self.assertEqual(result["page"]["limit"], 50)
        self.assertFalse(result["page"]["has_more"])
        self.assertFalse(result["truncated"])

    async def test_limit_ceiling_clamped(self) -> None:
        # ceil=2000. 5000 요청 시 2000 으로 클램프.
        result = await self._run(raw_count=10, limit=5000)
        self.assertEqual(result["page"]["limit"], 2000)

    async def test_truncated_flag_orthogonal_to_paging(self) -> None:
        from app.services import inventory_service as inv
        # raw 행이 LEDGER_MAX + 1 → truncated True. 페이지네이션은 그래도 동작.
        result = await self._run(raw_count=inv.LEDGER_MAX + 1, limit=20, offset=0)
        self.assertTrue(result["truncated"], "raw 가 LEDGER_MAX 초과 시 truncated=True")
        self.assertEqual(result["page"]["limit"], 20)
        self.assertLessEqual(len(result["rows"]), 20)


if __name__ == "__main__":  # pragma: no cover
    main()
