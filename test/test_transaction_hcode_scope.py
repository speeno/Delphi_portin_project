"""업무 라우터 hcode scope 강제 경로 정적 회귀."""
from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers"


class TransactionHcodeScopeStaticTest(TestCase):
    def test_stats_router_enforces_hcode_isolation(self) -> None:
        src = (BACKEND / "stats.py").read_text(encoding="utf-8")
        self.assertIn("enforce_hcode_isolation", src)
        # 핵심 stats endpoint 가 request hcode를 scope에 통과시키는지 확인
        for fn in ("get_customer_analysis", "get_book_turnover", "get_sales_period"):
            pat = rf"async def {fn}\([\s\S]+?_effective_hcode = enforce_hcode_isolation\(hcode, ctx\)"
            self.assertRegex(src, pat)

    def test_outbound_router_enforces_hcode_isolation(self) -> None:
        src = (BACKEND / "outbound.py").read_text(encoding="utf-8")
        self.assertIn("enforce_hcode_isolation", src)
        self.assertRegex(src, r"_effective_hcode = enforce_hcode_isolation\(hcode, current\)")


if __name__ == "__main__":
    main(verbosity=2)

