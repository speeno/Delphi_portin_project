"""DEC-286 — 기간별미수원장(Sobo33 · 레거시 Subu33) 백엔드 가드 (2026-09-12).

사용자 요청(교문사): 「정산관리 – 미수현황이 정상 작동 안 됨 → 원장관리 – 기간별미수원장 복원」.
미수현황은 정산 테이블(T2/T5_Ssub)을 읽는데 이 테넌트에는 그 데이터가 없다(라이브: T5_Ssub 0행,
T2_Ssub 3행). 레거시 기간별미수원장은 거래(S1_Ssub)·입출금(H1_Ssub)·미수 스냅샷(Sv_Chng)·
장부조정(Sg_Gsum)에서 계산한다(H1_Ssub 74,720행) — 그래서 같은 원천을 쓰는 화면을 새로 만든다.

산식은 **이미 검증된 통합 거래처원장(DEC-165/166)** 재사용:
  미수금 = 전일미수(_Sv_Chng_ 1:1) + 출고금액 + 반품금액(음수 저장) − 수금액.
레거시 컬럼(Subu33.dfm L544~614): 구분명·전일미수금·판매수량·출고금액·반품금액·증정수량·수금액·미수금.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import customer_txn_ledger_service as cs  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


S1 = [
    {"Gcode": "C1", "Gubun": "출고", "Pubun": "위탁", "qty": 10, "amt": 100000},
    {"Gcode": "C1", "Gubun": "출고", "Pubun": "증정", "qty": 3, "amt": 0},
    {"Gcode": "C1", "Gubun": "반품", "Pubun": "정품", "qty": -2, "amt": -20000},
    {"Gcode": "C2", "Gubun": "출고", "Pubun": "위탁", "qty": 5, "amt": 50000},
]
H1 = [{"Gcode": "C1", "inp": 30000, "outp": 5000}]
NAMES = [
    {"Gcode": "C1", "Gname": "가서점", "Gubun": "10001"},
    {"Gcode": "C2", "Gname": "나서점", "Gubun": "10005"},
]
GBUN = [{"Gcode": "10001", "Gname": "구내서점"}, {"Gcode": "10005", "Gname": "일반서점"}]


def _call(*, opening=None, capture=None):
    async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
        if capture is not None:
            capture.append(sql)
        if "FROM S1_Ssub" in sql and "GROUP BY Gcode, Gubun, Pubun" in sql:
            return list(S1)
        if "FROM H1_Ssub" in sql:
            return list(H1)
        if "FROM G1_Ggeo" in sql:
            return list(NAMES)
        if "FROM G1_Gbun" in sql:
            return list(GBUN)
        return []

    with patch.object(cs, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
         patch.object(cs, "_opening_receivable_map", new=AsyncMock(return_value=dict(opening or {}))):
        return _run(cs.receivable_period_ledger(
            server_id="remote_153", hcode="5019",
            date_from="2026-08-01", date_to="2026-08-31",
        ))


class ReceivableLedgerTests(TestCase):
    def test_balance_formula_matches_legacy(self) -> None:
        """미수금 = 전일미수 + 출고금액 + 반품금액(음수) − 수금액."""
        out = _call(opening={"C1": 500000})
        c1 = next(r for r in out["by_customer"] if r["gcode"] == "C1")
        self.assertEqual(c1["opening"], 500000)
        self.assertEqual(c1["out_amt"], 100000, "증정 금액도 출고금액에 합산(Subu33 분기표)")
        self.assertEqual(c1["rtn_amt"], -20000)
        self.assertEqual(c1["collect"], 25000, "수금액 = 입금 − 출금")
        self.assertEqual(c1["balance"], 500000 + 100000 - 20000 - 25000)

    def test_gift_quantity_is_its_own_column(self) -> None:
        out = _call()
        c1 = next(r for r in out["by_customer"] if r["gcode"] == "C1")
        self.assertEqual(c1["gift_qty"], 3, "증정수량은 별도 칸")
        self.assertEqual(c1["out_qty"], 10, "증정 수량은 판매수량에 넣지 않는다")

    def test_rollup_by_customer_class(self) -> None:
        out = _call(opening={"C1": 500000, "C2": 0})
        by = {g["gubun"]: g for g in out["by_gubun"]}
        self.assertEqual(set(by), {"10001", "10005"})
        self.assertEqual(by["10001"]["gname"], "구내서점", "구분명은 G1_Gbun 에서")
        self.assertEqual(by["10001"]["customers"], 1)
        self.assertEqual(by["10005"]["out_amt"], 50000)
        self.assertEqual(
            sum(g["balance"] for g in out["by_gubun"]),
            out["totals"]["balance"],
            "구분 합 == 전체 합계",
        )

    def test_queries_are_hcode_scoped(self) -> None:
        cap: list[str] = []
        _call(capture=cap)
        for sql in cap:
            if "FROM S1_Ssub" in sql or "FROM H1_Ssub" in sql or "FROM G1_Gbun" in sql:
                self.assertIn("Hcode=%s", sql.replace(" = %s", "=%s"), f"회사 격리 누락: {sql[:60]}")

    def test_route_registered(self) -> None:
        src = (_BACKEND / "app" / "routers" / "ledger.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/receivable")', src)
        self.assertIn("receivable_period_ledger", src)
        self.assertIn("enforce_hcode_identity", src)

    def test_screen_exists_and_shows_legacy_columns(self) -> None:
        page = (_HUB / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
                / "ledger" / "receivable" / "page.tsx").read_text(encoding="utf-8")
        for label in ("전일미수금", "판매수량", "출고금액", "반품금액", "증정수량", "수금액", "미수금"):
            self.assertIn(label, page, f"레거시 컬럼 {label} 누락")
        self.assertIn("SplitListPanes", page, "상단 구분별 / 하단 거래처별 2단")


if __name__ == "__main__":
    main()
