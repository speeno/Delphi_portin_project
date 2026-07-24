"""
총판(T2_DIST) 출고접수 현황판 — `outbound_service.distributor_board` 회귀 가드.

대상(2026-07-24 사용자): 총판 계정이 소속 출판사별 당일 출고 접수/완료 + 상태
(미사용/사용중/접수/완료)를 본다. 슬립 단위 MAX(Yesno) → Hcode별 집계 + 플래그 도출을
서비스 레벨에서 검증(3.23 파생테이블 없이).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import outbound_service  # noqa: E402


class _Stub:
    def __init__(self, pubs: list[dict[str, Any]], slips: list[dict[str, Any]]) -> None:
        self.pubs = pubs
        self.slips = slips
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        if "G7_Ggeo" in sql:
            return self.pubs
        if "S1_Ssub" in sql:
            return self.slips
        return []


def _run(pubs, slips, scope_hcode=None):
    stub = _Stub(pubs, slips)
    with patch.object(outbound_service, "execute_query", new=stub), patch.object(
        outbound_service, "mysql3_protocol", new=lambda s: False
    ), patch.object(outbound_service, "_default_outbound_ocode", new=lambda s: "B"):
        res = asyncio.run(
            outbound_service.distributor_board(
                server_id="remote_1", gdate="2026-07-22", scope_hcode=scope_hcode
            )
        )
    return res, stub


class DistributorBoardTests(TestCase):
    def test_counts_and_flags(self) -> None:
        pubs = [
            # 전화는 분할 저장: Gtel1(앞자리) + Gtel2(나머지) → "031-946-4841" 로 결합돼야 함.
            {"code": "0007", "name": "도서출판 품", "tel1": "031", "tel2": "946-4841"},
            {"code": "0011", "name": "초타원형", "tel1": "", "tel2": "010-2859-4550"},
            {"code": "9999", "name": "무활동사", "tel1": "02", "tel2": ""},
        ]
        slips = [
            {"Hcode": "0007", "yesno_max": "1"},
            {"Hcode": "0007", "yesno_max": "2"},  # '2' 도 완료(DEC-081)
            {"Hcode": "0007", "yesno_max": "1"},
            {"Hcode": "0011", "yesno_max": "0"},  # 접수
        ]
        res, _ = _run(pubs, slips)
        self.assertEqual(res["date"], "2026.07.22")  # 정규화
        by = {p["code"]: p for p in res["publishers"]}

        self.assertEqual(by["0007"]["done_count"], 3)
        self.assertTrue(by["0007"]["done"])
        self.assertFalse(by["0007"]["received"])
        self.assertFalse(by["0007"]["unused"])

        self.assertEqual(by["0007"]["tel"], "031-946-4841")  # Gtel1+'-'+Gtel2 결합

        self.assertEqual(by["0011"]["received_count"], 1)
        self.assertTrue(by["0011"]["received"])
        self.assertFalse(by["0011"]["done"])
        self.assertEqual(by["0011"]["tel"], "010-2859-4550")  # tel2 만 있으면 그대로

        self.assertTrue(by["9999"]["unused"])  # 당일 슬립 0 → 미사용
        self.assertFalse(by["9999"]["done"])

    def test_in_use_pending(self) -> None:
        pubs = [{"code": "0007", "name": "품", "tel1": "", "tel2": ""}]
        slips = [{"Hcode": "0007", "yesno_max": ""}]  # 대기(pending)
        res, _ = _run(pubs, slips)
        p = res["publishers"][0]
        self.assertTrue(p["in_use"])
        self.assertEqual(p["pending_count"], 1)
        self.assertFalse(p["unused"])

    def test_scope_hcode_filters(self) -> None:
        pubs = [{"code": "0007", "name": "품", "tel1": "", "tel2": ""}]
        _, stub = _run(pubs, [], scope_hcode="0007")
        slip_call = [c for c in stub.calls if "S1_Ssub" in c[0]][0]
        self.assertIn("0007", slip_call[1])  # S1_Ssub 에 Hcode 필터
        pub_call = [c for c in stub.calls if "G7_Ggeo" in c[0]][0]
        self.assertIn("0007", pub_call[1])  # G7_Ggeo 에 Gcode 필터

    def test_no_scope_no_hcode_filter(self) -> None:
        pubs = [{"code": "0007", "name": "품", "tel1": "", "tel2": ""}]
        _, stub = _run(pubs, [], scope_hcode=None)
        slip_call = [c for c in stub.calls if "S1_Ssub" in c[0]][0]
        self.assertNotIn("Hcode = %s", slip_call[0])  # 총판=미필터
        # Ocode 는 서버기준 기본값이 테넌트 실제값과 달라 제외(DEC-095) — 필터에 없어야 함.
        self.assertNotIn("Ocode", slip_call[0])
        self.assertEqual(slip_call[1], ("2026.07.22",))  # gdate 만


if __name__ == "__main__":
    main()
