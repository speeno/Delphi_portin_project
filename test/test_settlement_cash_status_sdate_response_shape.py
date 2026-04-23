"""cash-status sdate variant 응답 모델 회귀 가드 (DEC-058 Wave B / DEC-019).

배경
----
backend.log 4월 21~22일에 ``GET /api/v1/settlement/cash-status?variant=sdate``
가 422 Unprocessable Entity 로 일관 실패 (hcode variant 는 정상 200).
- 라이브 probe 2026-04-22 결과: 4 서버 모두 200 OK 회복.
- 하지만 응답 dict 의 ``items`` / ``totals`` / ``total_count`` / ``variant``
  키가 누락되거나 모델 분기가 변경되면 다시 422 발생 가능.

본 가드는 ``execute_query`` 만 mock 한 상태에서 ``cash_status(variant='sdate')``
를 호출하여 (1) 예외 없이 반환, (2) 표준 응답 키 모두 존재, (3) hcode
variant 와 *동일 키 셋* 인지 검증 — 응답 모델 정합 보장.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))


def _fake_execute_query(*args: Any, **kwargs: Any):
    """모든 SQL 호출에 대해 빈 결과 — 422 를 일으키는 None 필드 부재 검증용."""
    sql = args[1] if len(args) > 1 else kwargs.get("sql", "")
    s = (sql or "").upper()
    if s.startswith("SHOW COLUMNS"):
        # T5_Ssub 컬럼 — sdate variant 에서 t5_month_key_expr 가 사용
        return [
            {"Field": "Gssum"}, {"Field": "Gdate"}, {"Field": "Hcode"},
            {"Field": "Yesno"}, {"Field": "Sdate"},
        ]
    if "COUNT(*)" in s and "AS CNT" in s:
        return [{"cnt": 0}]
    return []


class CashStatusSdateResponseShapeTest(IsolatedAsyncioTestCase):
    """sdate variant 응답이 hcode variant 와 동일 키 셋을 유지하는지 검증."""

    REQUIRED_KEYS = {"variant", "items", "totals", "total_count"}
    TOTALS_KEYS = {"gsumx", "gosum", "gbsum", "gssum", "gsusu", "gsumy"}

    async def asyncSetUp(self) -> None:
        # 컬럼 캐시 초기화 — 다른 테스트에 의한 오염 방지
        from app.services.t5_ssub_adapt import clear_t5_column_cache_for_tests
        clear_t5_column_cache_for_tests()

    async def test_sdate_variant_returns_standard_shape(self) -> None:
        from app.services import settlement_service
        from app.services import t5_ssub_adapt
        mock = AsyncMock(side_effect=_fake_execute_query)
        with patch.object(settlement_service, "execute_query", new=mock), \
             patch.object(t5_ssub_adapt, "execute_query", new=mock):
            res = await settlement_service.cash_status(
                server_id="remote_152",
                variant="sdate",
                month="202604",
                hcode=None,
                limit=10, offset=0,
            )
        self.assertIsInstance(res, dict, "cash_status sdate 응답이 dict 가 아님 → 422 회귀")
        self.assertEqual(res["variant"], "sdate")
        self.assertEqual(set(res.keys()) >= self.REQUIRED_KEYS, True,
                         f"응답 키 누락: {self.REQUIRED_KEYS - set(res.keys())}")
        self.assertEqual(res["items"], [])
        self.assertEqual(res["total_count"], 0)
        self.assertTrue(self.TOTALS_KEYS <= set(res["totals"].keys()),
                        f"totals 키 누락: {self.TOTALS_KEYS - set(res['totals'].keys())}")

    async def test_sdate_and_hcode_variants_share_response_shape(self) -> None:
        """variant 별 응답 키 셋이 동일 — 422 회귀 일반화 가드."""
        from app.services import settlement_service
        from app.services import t5_ssub_adapt
        mock = AsyncMock(side_effect=_fake_execute_query)
        with patch.object(settlement_service, "execute_query", new=mock), \
             patch.object(t5_ssub_adapt, "execute_query", new=mock):
            res_h = await settlement_service.cash_status(
                server_id="remote_152", variant="hcode",
                month="202604", hcode=None, limit=10, offset=0,
            )
            res_s = await settlement_service.cash_status(
                server_id="remote_152", variant="sdate",
                month="202604", hcode=None, limit=10, offset=0,
            )
        self.assertEqual(set(res_h.keys()), set(res_s.keys()),
                         "hcode/sdate variant 응답 키 셋 불일치 → 422 회귀 위험")
        self.assertEqual(set(res_h["totals"].keys()), set(res_s["totals"].keys()))


if __name__ == "__main__":
    main()
