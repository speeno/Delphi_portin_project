"""DEC-165 — 거래처거래원장 (Subu31 정본) 회귀 가드.

미수 running = 전일미수 + 출고금액 + 반품금액(음수 저장) − 수금액.
검증 앵커(홍익대[서울]대학서적 1015, remote_153/5019, 실데이터 대사 2026-08-14):
전일미수 2,227,265 · 합계 189/6,496,910/−120/−3,773,700/수금 4,950,475 · 최종 미수 0.
"""

import unittest
from unittest.mock import AsyncMock, patch

from app.services import customer_txn_ledger_service as svc


def _s1(gdate, gubun, jubun, bcode, qty, amt, *, pubun="", gjisa="", bigo=""):
    return {
        "Gdate": gdate, "Gubun": gubun, "Pubun": pubun, "Jubun": jubun,
        "Gjisa": gjisa, "Bcode": bcode, "Gbigo": bigo, "qty": qty, "amt": amt,
    }


class CustomerLedgerDailyTest(unittest.IsolatedAsyncioTestCase):
    async def test_running_and_totals_sign_convention(self):
        """출고 가산 · 반품(음수) 가산 · 수금 차감 — Subu31 L705~720 부호 규약."""
        s1_rows = [
            _s1("2026.02.20", "출고", "11", "B1", 100, 1000),
            _s1("2026.02.20", "출고", "11", "B2", 12, 500),        # 같은 전표 → 외1
            _s1("2026.03.26", "반품", "12", "B1", -34, -300),
        ]
        h1_rows = [
            {"Gdate": "2026.03.16", "Gubun": "입금", "Pubun": "현금",
             "Ocode": "", "Oname": "대학서적", "Gbigo": "", "amt": 700},
        ]

        async def fake_query(server_id, sql, params=None):
            if "FROM S1_Ssub" in sql and "SUM(" not in sql:
                return s1_rows
            if "FROM H1_Ssub" in sql and "Oname" in sql:
                return h1_rows
            if "FROM G4_Book" in sql:
                return [{"Gcode": "B1", "Gname": "테스트도서"}]
            return []

        with patch.object(svc, "execute_query", AsyncMock(side_effect=fake_query)), \
             patch.object(svc, "_opening_receivable", AsyncMock(return_value=2000)):
            res = await svc.customer_ledger_daily(
                server_id="remote_153", hcode="5019", gcode="1015",
                date_from="2026-01-01", date_to="2026-08-13",
            )

        self.assertEqual(res["opening"], 2000)
        items = res["items"]
        self.assertEqual(len(items), 3)

        slip = items[0]  # 2.20 출고 전표 (2라인 → 외1)
        self.assertEqual(slip["extra"], 1)
        self.assertEqual(slip["out_qty"], 112)
        self.assertEqual(slip["out_amt"], 1500)
        self.assertEqual(slip["label"], "테스트도서")
        self.assertEqual(slip["balance"], 2000 + 1500)

        pay = items[1]  # 3.16 수금 — 입금 양수, 미수 차감
        self.assertEqual(pay["kind"], 3)
        self.assertEqual(pay["collect"], 700)
        self.assertIn("대학서적", pay["label"])
        self.assertEqual(pay["balance"], 3500 - 700)

        rtn = items[2]  # 3.26 반품 — 음수 저장 그대로 가산(=실질 차감)
        self.assertEqual(rtn["rtn_qty"], -34)
        self.assertEqual(rtn["balance"], 2800 - 300)

        t = res["totals"]
        self.assertEqual(
            (t["out_qty"], t["out_amt"], t["rtn_qty"], t["rtn_amt"], t["collect"]),
            (112, 1500, -34, -300, 700),
        )
        self.assertEqual(t["balance"], 2500)

    async def test_opening_receivable_composition(self):
        """전일미수 = Sv_Chng 스냅샷(Gssum−Gsusu) + S1 Σ Gssum − H1 입금 + H1 출금 + Sg_Gsum."""

        async def fake_query(server_id, sql, params=None):
            if "MAX(Gdate)" in sql:
                return [{"d": "2025.12.31"}]
            if "FROM Sv_Chng" in sql:
                return [{"s": 5000, "u": 1000}]      # 스냅샷 +4000
            if "FROM S1_Ssub" in sql:
                return [{"s": 300}]                   # 델타 +300
            if "FROM H1_Ssub" in sql:
                return [{"inp": 200, "outp": 50}]     # −200 +50
            if "FROM Sg_Gsum" in sql:
                return [{"b": 10}]                    # +10
            return []

        with patch.object(svc, "execute_query", AsyncMock(side_effect=fake_query)):
            opening = await svc._opening_receivable(
                "remote_153", hcode="5019", gcode="1015", date_from="2026.01.01"
            )
        self.assertEqual(opening, 4000 + 300 - 200 + 50 + 10)


class CustomerLedgerSlipDetailTest(unittest.IsolatedAsyncioTestCase):
    async def test_detail_lines_running_and_kind_filter(self):
        """전표 상세 — kind 필터(출고성만) + 라인별 미수 running + 정가·% 표기."""
        rows = [
            _s1("2026.02.20", "출고", "11", "B1", 20, 374000) | {"grat1": 85},
            _s1("2026.02.20", "반품", "11", "B2", -5, -100) | {"grat1": 80},
        ]

        async def fake_query(server_id, sql, params=None):
            if "FROM S1_Ssub" in sql:
                return rows
            if "FROM G4_Book" in sql:
                return [{"Gcode": "B1", "Gname": "리빙토픽", "gdang": 22000}]
            return []

        with patch.object(svc, "execute_query", AsyncMock(side_effect=fake_query)):
            res = await svc.customer_ledger_slip_detail(
                server_id="remote_153", hcode="5019", gcode="1015",
                gdate="2026.02.20", jubun="11", gjisa="", kind=1, opening=2227265,
            )
        self.assertEqual(len(res["items"]), 1)  # 반품 라인은 kind=1 에서 제외
        line = res["items"][0]
        self.assertEqual(line["gname"], "리빙토픽")
        self.assertEqual(line["price"], 22000)
        self.assertEqual(line["grat1"], 85)
        self.assertEqual(line["qty"], 20)
        self.assertEqual(line["out_amt"], 374000)
        self.assertEqual(line["balance"], 2227265 + 374000)
        self.assertEqual(res["closing"], 2601265)


if __name__ == "__main__":
    unittest.main()
