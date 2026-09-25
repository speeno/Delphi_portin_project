"""
DEC-328 — 거래처통계(목록) 컬럼·반품율·총합(사용자 2026-09-25, 위러브솔루션 「거래처/구분별판매」 기준).

- 컬럼: 거래처코드·거래처명·구분·출고수량·출고금액·증정수량·반품수량·반품금액·수금액·판매부수·판매금액·반품율(%).
- 반품율 = −반품수량 ÷ 출고수량 × 100, 출고 0 → 0 (레거시 Subu69_2 「거래처판매율」). 합계 반품율 = Σ(−반품) ÷ Σ출고 × 100.
- 최종거래일: 화면 미표시, 엑셀에만.
- 하단 총합 = 검색 결과 전체(페이지 무관).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "stats" / "customer" / "page.tsx"
sys.path.insert(0, str(BACKEND))


class ReturnRate(TestCase):
    def test_formula(self):
        from app.services.reports_service import _return_rate

        self.assertEqual(_return_rate(-212, 6095), 3.5)
        self.assertEqual(_return_rate(-5, 0), 0.0)   # 출고 0 → 0 (레거시 T05:=0)
        self.assertEqual(_return_rate(0, 10), 0.0)

    def test_sort_key_whitelisted(self):
        from app.services.reports_service import _CUSTOMER_SALES_SORT_KEYS

        self.assertIn("return_rate", _CUSTOMER_SALES_SORT_KEYS)


class AnalysisTotalsUseFullResult(IsolatedAsyncioTestCase):
    async def test_totals_from_full_result_not_page(self):
        from app.services import stats_service

        async def fake(**kw):
            return {
                "rows": [{"gcode": "A", "goqut": 10, "gbqut": -1}],   # 1페이지 행
                "total": 3,
                "totals": {"goqut": 100, "gosum": 5000, "gjqut": 7, "gbqut": -20, "gbsum": -900,
                           "gsusu": 80, "gjsum": 1234, "gssum": 4100, "return_rate": 20.0},
            }

        old = stats_service.reports_service.get_customer_sales
        stats_service.reports_service.get_customer_sales = fake
        try:
            res = await stats_service.get_customer_analysis(
                server_id="remote_153", hcode="5019", date_from="2026-06-25", date_to="2026-09-25",
                limit=1, offset=0,
            )
        finally:
            stats_service.reports_service.get_customer_sales = old
        t = res["totals"]
        self.assertEqual((t["qut_total"], t["bqut_total"], t["sell_qut_total"]), (100, -20, 80))
        self.assertEqual((t["gift_qut_total"], t["receipt_total"], t["return_rate"]), (7, 1234, 20.0))


class PageAndExport(TestCase):
    def setUp(self):
        self.src = PAGE.read_text(encoding="utf-8")

    def test_columns(self):
        body = self.src.split("const CUSTOMER_COLUMNS")[1].split("];")[0]
        labels = ["거래처코드", "거래처명", "구분", "출고수량", "출고금액", "증정수량", "반품수량",
                  "반품금액", "수금액", "판매부수", "판매금액", "반품율(%)"]
        pos = [body.index(f'label: "{l}"') for l in labels]
        self.assertEqual(pos, sorted(pos))
        self.assertNotIn('label: "최종거래일"', body)   # 화면 미표시

    def test_export_only_last_trade_date_and_totals(self):
        self.assertIn('const EXPORT_ONLY_COLUMNS = [{ key: "gdate", label: "최종거래일" }]', self.src)
        self.assertIn(".concat(EXPORT_ONLY_COLUMNS)", self.src)
        self.assertIn('totalsLabel="총합"', self.src)
        self.assertIn("t.return_rate", self.src)

    def test_router_export_default(self):
        router = (BACKEND / "app" / "routers" / "stats.py").read_text(encoding="utf-8")
        body = router.split("_CUSTOMER_ANALYSIS_EXPORT_COLUMNS = [")[1].split("]\n")[0]
        for key in ('"cust_gubun"', '"gjqut"', '"gjsum"', '"return_rate"', '"gdate"'):
            self.assertIn(key, body)


if __name__ == "__main__":
    main(verbosity=2)
