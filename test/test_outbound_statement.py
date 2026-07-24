"""
총판 출고내역서 — `outbound_service.outbound_statement` 회귀 가드.

대상(2026-07-24 사용자, 레거시 Subu39): 선택 출판사(Hcode)의 당일 출고를 거래처·지점·전표
단위로 수량(S1_Ssub.Gsqut) + 덩이/보호대/박스(T4_Ssub.Gqut1/2/3) 병합, 지역(시내/지방)은
G1_Ggeo.Gubun('01'→시내 else 지방) 파생, 시내/지방/합계 요약.
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
    def __init__(self, qty, pack, g1) -> None:
        self.qty, self.pack, self.g1 = qty, pack, g1
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        if "S1_Ssub" in sql:
            return self.qty
        if "T4_Ssub" in sql:
            return self.pack
        if "G1_Ggeo" in sql:
            return self.g1
        return []


def _run(qty, pack, g1, hcode="0013"):
    stub = _Stub(qty, pack, g1)
    with patch.object(outbound_service, "execute_query", new=stub), patch.object(
        outbound_service, "mysql3_protocol", new=lambda s: False
    ), patch.object(outbound_service, "_default_outbound_ocode", new=lambda s: "B"):
        res = asyncio.run(
            outbound_service.outbound_statement(
                server_id="remote_1", gdate="2026-07-22", hcode=hcode
            )
        )
    return res, stub


class OutboundStatementTests(TestCase):
    def test_merge_region_and_summary(self) -> None:
        qty = [
            {"Gcode": "00027", "gjisa": "05", "Jubun": "11", "gsqut": 1},
            {"Gcode": "00028", "gjisa": "05", "Jubun": "11", "gsqut": 3},
            {"Gcode": "01016", "gjisa": "05", "Jubun": "11", "gsqut": 3},  # 지방
        ]
        pack = [
            {"Gcode": "00027", "gjisa": "05", "Jubun": "11", "gqut1": 1, "gqut2": 2, "gqut3": 0},
            {"Gcode": "00028", "gjisa": "05", "Jubun": "11", "gqut1": 1, "gqut2": 2, "gqut3": 0},
            {"Gcode": "01016", "gjisa": "05", "Jubun": "11", "gqut1": 1, "gqut2": 2, "gqut3": 0},
        ]
        g1 = [
            {"Hcode": "0013", "Gcode": "00027", "gname": "파주)에스24", "gubun": "01"},  # 시내
            {"Hcode": "0013", "Gcode": "00028", "gname": "파주)교보", "gubun": "01"},  # 시내
            {"Hcode": "0013", "Gcode": "01016", "gname": "파주)알라딘", "gubun": "02"},  # 지방
        ]
        res, _ = _run(qty, pack, g1)
        self.assertEqual(res["date"], "2026.07.22")
        self.assertEqual(len(res["rows"]), 3)
        by = {r["code"]: r for r in res["rows"]}
        self.assertEqual(by["00027"]["region"], "시내")
        self.assertEqual(by["00027"]["name"], "파주)에스24")
        self.assertEqual(by["00027"]["qty"], 1)
        self.assertEqual(by["00027"]["protector"], 2)
        self.assertEqual(by["01016"]["region"], "지방")  # gubun 02

        s = res["summary"]
        # 시내: 00027(q1,b1,p2)+00028(q3,b1,p2) = q4,b2,p4 ; 지방: 01016 q3,b1,p2 ; 합계 q7,b3,p6
        self.assertEqual(s["city"], {"qty": 4, "bundle": 2, "protector": 4, "box": 0})
        self.assertEqual(s["local"], {"qty": 3, "bundle": 1, "protector": 2, "box": 0})
        self.assertEqual(s["total"], {"qty": 7, "bundle": 3, "protector": 6, "box": 0})

    def test_missing_packaging_defaults_zero(self) -> None:
        qty = [{"Gcode": "00027", "gjisa": "", "Jubun": "1", "gsqut": 5}]
        g1 = [{"Hcode": "0013", "Gcode": "00027", "gname": "A", "gubun": "01"}]
        res, _ = _run(qty, [], g1)  # T4 없음
        r = res["rows"][0]
        self.assertEqual(r["qty"], 5)
        self.assertEqual((r["bundle"], r["protector"], r["box"]), (0, 0, 0))

    def test_empty_hcode(self) -> None:
        res, stub = _run([], [], [], hcode="  ")
        self.assertEqual(res["rows"], [])
        self.assertEqual(stub.calls, [])  # 쿼리 없음

    def test_s1_filters_selected_publisher(self) -> None:
        qty = [{"Gcode": "00027", "gjisa": "", "Jubun": "1", "gsqut": 1}]
        g1 = [{"Hcode": "0013", "Gcode": "00027", "gname": "A", "gubun": "01"}]
        _, stub = _run(qty, [], g1, hcode="0013")
        s1 = [c for c in stub.calls if "S1_Ssub" in c[0]][0]
        self.assertIn("0013", s1[1])  # Hcode=선택 출판사
        self.assertIn("Hcode=%s", s1[0])


if __name__ == "__main__":
    main()
