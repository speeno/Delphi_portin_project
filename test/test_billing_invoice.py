"""
청구서 인쇄 데이터 — `settlement_service.billing_invoice`/`compute_invoice_totals` 회귀 가드.

정본: 레거시 Subu45(도서유통-New) Button821/812/601/602/905 + Edit201Exit 합계식.
골든값: 0013 *예방의학사 2026.07 실제 인쇄물(사용자 제공 2026-07-24) —
당월청구 491,864 / V.A.T 49,186 / 합계 541,050 / 전월입금 557,777 / 전월미수 0.
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

from app.services import settlement_service as ss  # noqa: E402

GOLDEN_RATES = {
    "base_qty": 500, "base_fee": 50000, "over_rate": 100, "local_rate": 100,
    "prot_rate": 120, "box_rate": 1100, "io_base_qty": 500, "io_base_fee": 50000,
    "io_over_rate": 70, "stmt_fee": 25000, "stock_rate": 27, "dismantle_rate": 0,
    "pickup_city_rate": 1500, "pickup_local_rate": 3000, "space_fee": 10000,
    "title_rate": 1000, "program_fee": 30000, "etc_fee": 20000,
}
GOLDEN_QTY = {
    "city": 84, "local": 60, "protector": 56, "box": 4, "pickup_city": 1,
    "pickup_local": 0, "dismantle": 0, "shipping": 17000, "stock": 7972, "titles": 56,
}


class ComputeInvoiceTotalsTests(TestCase):
    def test_golden_0013_202607(self) -> None:
        """실인쇄물 골든값 — 23항목 합/VAT(/10 절사)/총합계."""
        c = ss.compute_invoice_totals(
            rates=GOLDEN_RATES, qty=GOLDEN_QTY, prev_unpaid=0, vat_apply=True,
        )
        self.assertEqual(c["monthly"], 491864)
        self.assertEqual(c["vat"], 49186)          # 491,864/10=49,186.4 → 절사
        self.assertEqual(c["grand_total"], 541050)
        self.assertEqual(c["total_out"], 144)
        # 대표 항목 금액 (인쇄물 표기)
        it = c["items"]
        self.assertEqual(it["base"]["amt"], 50000)        # 기본월정료(고정)
        self.assertEqual(it["over"]["amt"], 0)            # 144<500 → 초과 0
        self.assertEqual(it["local_direct"]["amt"], 6000)  # 60×100
        self.assertEqual(it["per_title"]["amt"], 56000)    # 56×1,000
        self.assertEqual(it["stock_keep"]["amt"], 215244)  # 7,972×27
        self.assertEqual(it["io_base"]["amt"], 50000)
        self.assertEqual(it["pickup_city"]["amt"], 1500)   # 1×1,500
        self.assertEqual(it["space"]["amt"], 10000)
        self.assertEqual(it["statement"]["amt"], 25000)    # 거래명세표 발행(Sum25)
        self.assertEqual(it["protector"]["amt"], 6720)     # 56×120
        self.assertEqual(it["box"]["amt"], 4400)           # 4×1,100
        self.assertEqual(it["etc"]["amt"], 20000)

    def test_vat_not_applied(self) -> None:
        c = ss.compute_invoice_totals(
            rates=GOLDEN_RATES, qty=GOLDEN_QTY, prev_unpaid=100, vat_apply=False,
        )
        self.assertEqual(c["vat"], 0)
        self.assertEqual(c["grand_total"], 100 + c["monthly"])

    def test_over_qty_when_exceeds_base(self) -> None:
        qty = dict(GOLDEN_QTY, city=400, local=200)  # 총 600 > 기본 500
        c = ss.compute_invoice_totals(rates=GOLDEN_RATES, qty=qty, prev_unpaid=0, vat_apply=True)
        self.assertEqual(c["items"]["over"]["amt"], 100 * 100)      # 초과 100×100
        self.assertEqual(c["items"]["io_over"]["amt"], 100 * 70)    # 입출고 초과 100×70


class _Stub:
    """billing_invoice 쿼리 스텁 — SQL 조각으로 라우팅."""

    def __init__(self) -> None:
        self.slips = [
            # 15일 3슬립 중 1개 q=0 (레거시 화면 제외 대상)
            {"dd": "15", "Gcode": "00003", "jb": "11", "gj": "", "q": 0},
            {"dd": "15", "Gcode": "00027", "jb": "11", "gj": "", "q": 2},
            {"dd": "22", "Gcode": "00027", "jb": "11", "gj": "", "q": 1},
            {"dd": "22", "Gcode": "00023", "jb": "11", "gj": "", "q": 2},  # G1 폴백 케이스
        ]
        self.g1 = [
            # ''행 gu가 01/02 아님 → H행('01')로 폴백해야 시내 (레거시 Locate 체인)
            {"Hcode": "", "Gcode": "00023", "gu": "", "gname": "영풍문고"},
            {"Hcode": "0013", "Gcode": "00023", "gu": "01", "gname": "영풍문고"},
            {"Hcode": "", "Gcode": "00027", "gu": "01", "gname": "예스24"},
            {"Hcode": "", "Gcode": "00003", "gu": "02", "gname": "개인택배"},
        ]
        self.t4 = [
            {"Gcode": "00027", "Gdate": "2026.07.22", "gj": "", "jb": "11", "g2": 0, "g3": 1},
        ]

    async def exec_q(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        if "FROM S1_Ssub" in sql and "SUBSTRING(Gdate,9,2)" in sql and "Gubun = '출고'" in sql:
            return self.slips
        if "FROM T4_Ssub" in sql:
            return self.t4
        if "FROM T6_Ssub" in sql:
            return [{"dd": "08", "c1": 1, "c2": 0}]
        if "FROM S1_Ssub" in sql and "Bdate" in sql:
            return []
        if "FROM T1_Ssub" in sql:
            return [{"Gdate": "2026.07.06", "gcode": "c1", "gname": "김웅기 과장님",
                     "name1": "서울", "name2": "화물", "amt": 13500}]
        if "FROM G7_Ggeo" in sql:
            return [{"base_qty": 500, "base_fee": 50000, "over_rate": 100, "local_rate": 100,
                     "prot_rate": 120, "box_rate": 1100, "io_base_qty": 500, "io_base_fee": 50000,
                     "io_over_rate": 70, "stmt_fee": 25000, "stock_rate": 27, "dismantle_rate": 0,
                     "pickup_city_rate": 1500, "pickup_local_rate": 3000, "space_fee": 10000,
                     "title_rate": 1000, "program_fee": 30000, "etc_fee": 20000,
                     "vat_flag": "1", "title_mode": "2", "bigo": "비고", "pub_name": "예방의학사"}]
        if "FROM T2_Ssub" in sql:
            return [{"s26": 0, "s27": 507070, "s28": 50707, "s29": 8110}]
        if "FROM T5_Ssub" in sql:
            return [{"amt": 557777, "last_date": "2026.07.01"}]
        if "FROM G4_Book" in sql:
            return [{"n": 56}]
        if "GROUP BY Gubun" in sql:
            return [{"Gubun": "출고", "q": 5}, {"Gubun": "입고", "q": 3}]
        return []

    async def in_clause(self, server_id: str, *, sql_template: str, keys, prefix_params=(), **kw):  # noqa: ARG002
        return self.g1


class BillingInvoiceServiceTests(TestCase):
    def _run(self, stub: _Stub) -> dict[str, Any]:
        with patch.object(ss, "execute_query", new=stub.exec_q), patch.object(
            ss, "in_clause_lookup", new=stub.in_clause
        ):
            return asyncio.run(
                ss.billing_invoice(server_id="remote_1", gdate="202607", hcode="0013")
            )

    def test_grid_rules(self) -> None:
        res = self._run(_Stub())
        t = res["day_totals"]
        # q=0 슬립 제외: 15일은 00027(q2)만 — 시내2, 보호대2(폴백)
        d15 = next(d for d in res["days"] if d["day"] == "15")
        self.assertEqual((d15["city"], d15["protector"]), (2, 2))
        # G1 폴백: 00023 은 ''행 gu='' → H행 '01' 채택 = 시내
        d22 = next(d for d in res["days"] if d["day"] == "22")
        self.assertEqual(d22["city"], 3)           # 00027(1)+00023(2)
        self.assertEqual(d22["box"], 1)            # T4 매칭 슬립 박스1
        self.assertEqual(d22["protector"], 2)      # 비매칭 1슬립×2 + 매칭 g2=0
        self.assertEqual(t["ship_amount"], 13500)
        self.assertEqual(t["pickup_city"], 1)
        # 재고 = 전월 8,110 + 입고3 − 출고5 + 수거1 = 8,109
        self.assertEqual(res["qty"]["stock"], 8109)
        # 전월미수 = (0+507,070+50,707) − 557,777 = 0 / 전월입금 557,777
        self.assertEqual(res["calc"]["prev_unpaid"], 0)
        self.assertEqual(res["prev_paid"], 557777)
        self.assertEqual(res["qty"]["titles"], 56)
        self.assertEqual(res["publisher_name"], "예방의학사")

    def test_validation(self) -> None:
        with self.assertRaises(ss.SettlementValidationError):
            asyncio.run(ss.billing_invoice(server_id="s", gdate="202607", hcode=""))


if __name__ == "__main__":
    main()
