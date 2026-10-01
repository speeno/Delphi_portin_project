"""DEC-358 — 출고접수: 도서 확정 시 비율은 서버 체인(resolve_line_defaults) 결과를 그대로 반영.

종전엔 source=="G6_Ggeo"(특가)일 때만 반영해, 도서 마스터 위탁율(G4_Book.Grat1, 예: 교문사 90968=88)이
거래처 위탁율(G1 85)에 묻혔다(2026-10-01 교문사 경리부 보고). 서버 체인은 이미 G4 ≠0 이면 덮는다.
"""
from __future__ import annotations

import unittest
from pathlib import Path

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램/frontend/src"
PAGE = FE / "app/(app)/outbound/orders/new/page.tsx"
HELPER = FE / "lib/line-rate-chain.ts"
SHARED_USERS = [
    PAGE,
    FE / "app/(app)/outbound/orders/[orderKey]/page.tsx",
    FE / "components/outbound/order-detail-dialog.tsx",
]
SVC = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램/backend/app/services/sales_statement_create_service.py"
)


class TestOutboundBookRateFromChain(unittest.TestCase):
    def setUp(self) -> None:
        self.fn = HELPER.read_text(encoding="utf-8")

    def test_all_outbound_grids_share_helper(self) -> None:
        """출고 신규·상세 페이지·상세 팝업 = 같은 공급율 로직(2026-10-01 사용자 요청)."""
        for p in SHARED_USERS:
            src = p.read_text(encoding="utf-8")
            self.assertIn('from "@/lib/line-rate-chain"', src, p.name)
            self.assertIn("resolveChainLineRate(", src, p.name)
            self.assertNotIn('source === "G6_Ggeo"', src, p.name)

    def test_rate_applied_for_any_chain_source(self) -> None:
        self.assertNotIn('if (d?.source === "G6_Ggeo")', self.fn)
        self.assertIn("if (!src) return null;", self.fn)
        self.assertIn("grat1: Number(d.grat1) || 0", self.fn)

    def test_price_only_from_special_or_last_price(self) -> None:
        self.assertIn('src.startsWith("G6_Ggeo")', self.fn)
        self.assertIn('src === "S1_Ssub:last(grat1)"', self.fn)
        self.assertIn("...(priced ? { gdang:", self.fn)

    def test_server_chain_book_rate_overrides_customer(self) -> None:
        svc = SVC.read_text(encoding="utf-8")
        g4 = svc[svc.index("# 2) 도서마스터 (G4_Book)") : svc.index("# 2.5) 지점 공급율")]
        self.assertIn('out["source"] = "G4_Book"', g4)
        self.assertIn("if r != 0:", g4)
        # 레거시 S1_Ssub:last(grat1) 소스 문자열이 프론트 조건과 일치해야 한다.
        self.assertIn("f\"S1_Ssub:last({cfg['mode']})\"", svc)


if __name__ == "__main__":
    unittest.main()
