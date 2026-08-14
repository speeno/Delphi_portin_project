"""DEC-166 — 통합 거래처원장(전 거래처 미수 요약) 회귀 가드.

행 미수 = 전일미수 + 출고금액 + 반품금액(음수 저장) − 수금액 (DEC-165 running
기말값과 동치). '-전자책' 거래처 미수 0 고정 특례 포함.
검증 앵커(실데이터 대사 2026-08-14): 1015 행 = 단일 거래처원장 합계와 완전 일치,
임의 2개 거래처(00437·3255) summary↔daily 교차 대사 MATCH.
"""

import unittest
from unittest.mock import AsyncMock, patch

from app.services import customer_txn_ledger_service as svc


class CustomerLedgerSummaryTest(unittest.IsolatedAsyncioTestCase):
    def _fake_query(self):
        async def fake(server_id, sql, params=None):
            if "MAX(Gdate)" in sql:
                return [{"d": "2025.12.31"}]
            if "FROM Sv_Chng" in sql:  # 스냅샷 GROUP BY Gcode
                return [
                    {"Gcode": "1001", "s": 5000, "u": 1000},   # +4000
                    {"Gcode": "2002", "s": 100, "u": 0},        # +100
                ]
            if "FROM S1_Ssub" in sql and "GROUP BY Gcode, Gubun, Pubun" in sql:
                return [  # 기간 집계
                    {"Gcode": "1001", "Gubun": "출고", "Pubun": "판매", "qty": 10, "amt": 900},
                    {"Gcode": "1001", "Gubun": "반품", "Pubun": "반품", "qty": -2, "amt": -200},
                    {"Gcode": "3003", "Gubun": "출고", "Pubun": "판매", "qty": 5, "amt": 500},
                ]
            if "FROM S1_Ssub" in sql:  # 기간전 델타 GROUP BY Gcode
                return [{"Gcode": "1001", "s": 300}]
            if "FROM H1_Ssub" in sql:
                # 기간전(win) 호출과 기간(>=,<=) 호출 구분: params 로 판별
                if params and len(params) >= 2 and str(params[1]).startswith("2026") and "Gdate > " not in sql:
                    return [{"Gcode": "1001", "inp": 400, "outp": 0}]   # 기간 수금
                return [{"Gcode": "1001", "inp": 200, "outp": 50}]      # 기간전 −150
            if "FROM Sg_Gsum" in sql:
                return [{"Gcode": "1001", "b": 10}]
            if "FROM G1_Ggeo" in sql:
                return [
                    {"Gcode": "1001", "Gname": "일반서점"},
                    {"Gcode": "2002", "Gname": "누리-전자책"},
                    {"Gcode": "3003", "Gname": "신규서점"},
                ]
            return []

        return fake

    async def test_summary_balance_and_ebook_rule(self):
        with patch.object(svc, "execute_query", AsyncMock(side_effect=self._fake_query())):
            res = await svc.customer_ledger_summary(
                server_id="remote_153", hcode="5019",
                date_from="2026-01-01", date_to="2026-08-13",
            )
        by = {r["gcode"]: r for r in res["items"]}

        # 1001: opening 4000+300−200+50+10=4160, 기간 출고 900·반품 −200·수금 400.
        r = by["1001"]
        self.assertEqual(r["opening"], 4160)
        self.assertEqual((r["out_qty"], r["out_amt"]), (10, 900))
        self.assertEqual((r["rtn_qty"], r["rtn_amt"]), (-2, -200))
        self.assertEqual(r["collect"], 400)
        self.assertEqual(r["balance"], 4160 + 900 - 200 - 400)

        # 2002: '-전자책' 특례 — opening 100 이어도 미수 0 고정.
        self.assertEqual(by["2002"]["balance"], 0)

        # 3003: opening 0, 기간 출고만 — 미수 = 500.
        self.assertEqual(by["3003"]["balance"], 500)

        t = res["totals"]
        self.assertEqual(t["balance"], 4460 + 0 + 500)
        self.assertEqual(t["out_amt"], 1400)

    async def test_summary_name_filter(self):
        with patch.object(svc, "execute_query", AsyncMock(side_effect=self._fake_query())):
            res = await svc.customer_ledger_summary(
                server_id="remote_153", hcode="5019",
                date_from="2026-01-01", date_to="2026-08-13",
                name_filter="전자책",
            )
        self.assertEqual([r["gcode"] for r in res["items"]], ["2002"])


if __name__ == "__main__":
    unittest.main()
