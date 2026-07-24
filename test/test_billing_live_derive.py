"""
청구서관리 목록 실시간 파생 — `settlement_service._derive_billing_list` 회귀 가드.

대상(2026-07-24 사용자 결정): T2_Ssub 미집계 월도 레거시처럼 "열면 바로" 표시.
recalc_billing 공식(Sum26=출고Gssum−반품Gssum, Sum27=round×0.1, Sum28=합계, Yesno='0')을
(월, 출판사) 단위로 읽기전용 재현. DEC-091: Yesno 필터 없음·월키 정규화·R3 부재 폴백.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import settlement_service  # noqa: E402


def _run(out_rows, ret_rows, *, ret_raises=False):
    async def fake_eq(server_id, sql, params=None):  # noqa: ARG001
        if "FROM S1_Ssub" in sql:
            return out_rows
        if "FROM R3_Ssub" in sql:
            if ret_raises:
                raise RuntimeError("R3_Ssub absent")
            return ret_rows
        return []

    async def fake_ic(server_id, *, sql_template, keys, **kw):  # noqa: ARG001
        return [
            {"Gcode": "0013", "Gname": "예방의학사"},
            {"Gcode": "0007", "Gname": "도서출판 품"},
        ]

    with patch.object(settlement_service, "execute_query", new=fake_eq), patch.object(
        settlement_service, "in_clause_lookup", new=fake_ic
    ):
        return asyncio.run(
            settlement_service._derive_billing_list("remote_1", "202607", "202607", "", 50, 0)
        )


class BillingLiveDeriveTests(TestCase):
    def test_formula_and_names(self) -> None:
        out = [
            {"Gdm": "202607", "Hcode": "0013", "Amt": 20000, "Days": 5},
            {"Gdm": "202607", "Hcode": "0007", "Amt": 5000, "Days": 2},
        ]
        ret = [{"Gdm": "202607", "Hcode": "0013", "Amt": 2000}]
        items, total = _run(out, ret)
        self.assertEqual(total, 2)
        by = {i["hcode"]: i for i in items}
        # 0013: 20000-2000=18000, 세액 round(1800)=1800, 합계 19800
        self.assertEqual(by["0013"]["sum26"], 18000)
        self.assertEqual(by["0013"]["sum27"], 1800)
        self.assertEqual(by["0013"]["sum28"], 19800)
        self.assertEqual(by["0013"]["yesno"], "0")  # 미집계 = 임시
        self.assertEqual(by["0013"]["hname"], "예방의학사")
        self.assertEqual(by["0013"]["total_lines"], 5)  # 활동일수(COUNT DISTINCT Gdate)
        # 0007: 반품 없음 → 5000, 500, 5500
        self.assertEqual((by["0007"]["sum26"], by["0007"]["sum27"], by["0007"]["sum28"]), (5000, 500, 5500))

    def test_sort_month_desc_hcode_asc(self) -> None:
        out = [
            {"Gdm": "202606", "Hcode": "0013", "Amt": 100, "Days": 1},
            {"Gdm": "202607", "Hcode": "0013", "Amt": 100, "Days": 1},
            {"Gdm": "202607", "Hcode": "0007", "Amt": 100, "Days": 1},
        ]
        items, _ = _run(out, [])
        # 월 내림차순, 같은 월 내 출판사 오름차순
        self.assertEqual(
            [(i["gdate"], i["hcode"]) for i in items],
            [("202607", "0007"), ("202607", "0013"), ("202606", "0013")],
        )

    def test_return_source_absent_falls_back_zero(self) -> None:
        out = [{"Gdm": "202607", "Hcode": "0013", "Amt": 9000, "Days": 3}]
        items, total = _run(out, [], ret_raises=True)  # R3_Ssub 부재
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["sum26"], 9000)  # 반품 0 폴백 → 출고 그대로

    def test_empty_source_returns_empty(self) -> None:
        items, total = _run([], [])
        self.assertEqual((items, total), ([], 0))


if __name__ == "__main__":
    main()
