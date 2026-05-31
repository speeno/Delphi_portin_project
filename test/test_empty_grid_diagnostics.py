"""빈 그리드 진단 배너/조회기간 기본값 정적 회귀."""
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class EmptyGridDiagnosticsStaticTest(TestCase):
    def test_shared_banner_exists(self) -> None:
        p = FE / "components" / "shared" / "list-diagnostics-banner.tsx"
        src = p.read_text(encoding="utf-8")
        self.assertIn("DB 서버 정보가 없습니다. 다시 로그인해 주세요.", src)
        self.assertIn("선택한 기간/조건에 데이터가 없습니다.", src)

    def test_outbound_orders_uses_banner_and_90day_default(self) -> None:
        src = (FE / "app" / "(app)" / "outbound" / "orders" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("ListDiagnosticsBanner", src)
        self.assertIn("d.setDate(d.getDate() - 90)", src)

    def test_settlement_cash_uses_banner_and_90day_default(self) -> None:
        src = (FE / "app" / "(app)" / "settlement" / "cash" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("ListDiagnosticsBanner", src)
        self.assertIn("d.setDate(d.getDate() - 90)", src)

    def test_stats_customer_analysis_uses_banner(self) -> None:
        src = (FE / "app" / "(app)" / "stats" / "customer-analysis" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("ListDiagnosticsBanner", src)
        self.assertIn("serverId={user?.server_id}", src)


if __name__ == "__main__":
    main(verbosity=2)

