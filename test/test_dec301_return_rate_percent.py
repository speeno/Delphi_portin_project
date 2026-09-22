"""DEC-301 — 반품 비율 = 거래처 G1 Grat1(%) + 저장 시 수량 음수·금액 재계산 (2026-09-22).

원문: "반품접수신규입력 화면에서 거래처 「[파]교문사」에 대해서 레거시에서는 공급율을 85%로 설정되어있습니다.
현재 0.7로 나와서 공급율 매칭이 잘못된거 같습니다."

레거시 정본(교문사 = 도서유통-출판 빌드, 반품은 Subu21 거래명세서 경유):
- Tong20.PrinZing: ``Gubun='반품' → Grat1`` (구분 정품/비품/폐기 무관) — G1_Ggeo → G4_Book(≠0) → G6 특가.
- Tong20.PrinYing: 반품/폐기 수량 양수 → **음수**, ``Gssum = Gdang*Gsqut*Grat1/100`` (Grat1=0 이면 0).
- 실측(remote_153, 2026 반품 149전표·2,860행): Grat1 = 85/88/84/80/75/… 전부 %, 0~1 소수 0건.
종전 모던 반품 접수는 0~1 「할인율」 모드 + 고정 0.7 이라 레거시와 단위·값 모두 어긋났다(웹 저장 반품은 아직 0건).
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import returns_service as svc  # noqa: E402

FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class CreateReturnNormalizesLikeLegacy(unittest.IsolatedAsyncioTestCase):
    async def test_qty_negative_and_amount_recomputed_with_percent(self) -> None:
        captured: list[tuple] = []

        async def fake_tx(server_id, ops):
            captured.extend(ops)

        with patch.object(svc, "_generate_jubun", AsyncMock(return_value="21")), \
             patch.object(svc, "execute_in_transaction", AsyncMock(side_effect=fake_tx)):
            res = await svc.create_return(
                server_id="remote_153",
                header={"gdate": "2026-09-22", "hcode": "5019", "gcode": "80028"},
                memo=None,
                lines=[
                    # 화면은 양수 수량·% 비율 — 클라이언트 금액(엉터리)은 무시되고 서버가 재계산.
                    {"bcode": "00002", "pubun": "정품", "gsqut": 1, "gdang": 30000, "grat1": 85, "gssum": 999},
                    {"bcode": "00003", "pubun": "비품", "gsqut": -2, "gdang": 12345, "grat1": 85, "gssum": 0},
                    {"bcode": "00004", "pubun": "폐기", "gsqut": 3, "gdang": 10000, "grat1": 0, "gssum": 0},
                ],
            )
        lines = [params for sql, params in captured if sql is svc.SQL_INSERT_LINE]
        self.assertEqual(len(lines), 3)
        # 파라미터 순서: gdate,hcode,jubun,gjisa,pubun,bcode,ocode,gcode,Gsqut,Gdang,Grat1,Gssum,Gbigo
        self.assertEqual(lines[0][8:12], (-1, 30000, 85.0, -25500))  # 레거시 실데이터(80028 09.20)와 같은 행
        self.assertEqual(lines[1][8:12], (-2, 12345, 85.0, round(12345 * -2 * 85 / 100)))
        self.assertEqual(lines[2][8:12], (-3, 10000, 0.0, 0))
        self.assertEqual(res["qty"], -6)
        self.assertEqual(res["amount"], -25500 + round(12345 * -2 * 85 / 100))


class ReturnAxisIsPercent(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = (FE / "components" / "outbound" / "order-line-grid.tsx").read_text(encoding="utf-8")

    def test_no_fraction_mode_left(self) -> None:
        self.assertNotIn('rateMode: "fraction"', self.grid)
        self.assertNotIn('mode === "fraction"', self.grid)
        self.assertNotIn('rateMode === "fraction"', self.grid)
        self.assertIn('rateMode: "percent" | "percent_total";', self.grid)
        self.assertIn("export const RETURN_GRAT1_DEFAULT = 0;", self.grid)

    def test_return_axis_percent_total_and_keep_slip_dang(self) -> None:
        i = self.grid.index("export const RETURN_LINE_AXIS")
        block = self.grid[i : self.grid.index("};", i)]
        self.assertIn('rateLabel: "비율(%)",', block)
        self.assertIn('rateMode: "percent_total",', block)
        self.assertIn("keepSlipDang: true,", block)
        # 금액식 = 레거시 PrinYing / 서버 compute_gssum 과 같은 총액 반올림.
        self.assertIn("Math.round((gdang * gsqut * grat1) / 100)", self.grid)
        self.assertIn("if (axis.keepSlipDang && Number(lines[idx]?.gdang) > 0)", self.grid)


class ReturnsPageUsesCustomerRate(unittest.TestCase):
    def setUp(self) -> None:
        self.page = (FE / "app" / "(app)" / "returns" / "receipts" / "new" / "page.tsx").read_text(encoding="utf-8")

    def test_customer_g1_grat1_seeds_all_return_pubun(self) -> None:
        self.assertIn("setCustomerRate(Number(c.grat1) || 0);", self.page)
        self.assertIn("for (const p of RETURN_PUBUN_OPTIONS) out[p] = customerRate;", self.page)
        self.assertIn("customerRateMap={returnRateMap}", self.page)
        self.assertIn("defaultRate={customerRate}", self.page)

    def test_book_rate_from_server_line_defaults_chain(self) -> None:
        self.assertIn("resolveSpecial={resolveReturnRate}", self.page)
        self.assertIn("transactionsApi.lineDefaults({", self.page)


class DetailShowsStoredPercent(unittest.TestCase):
    def test_no_times_100(self) -> None:
        src = (FE / "app" / "(app)" / "returns" / "receipts" / "[returnKey]" / "page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("(ln.grat1 ?? 0) * 100", src)
        self.assertIn("{Number(ln.grat1 ?? 0)}%", src)


if __name__ == "__main__":
    unittest.main()
