"""
DEC-332 — 출판사통계 개선(사용자 2026-09-25): 거래처·도서통계(목록)(DEC-328/330)와 같은 컬럼·총합·반품율.

- 종전 「잔량」 = 증정(GJQUT) 오라벨 → 「증정수량」(gift_qut). 폐기·반품금액·판매수량·판매금액·반품율 추가.
- 총합 행 + 요약 카드(판매수량·판매금액·반품율). 최종거래일 = 선택 컬럼(기본 숨김), 엑셀엔 끝에 포함.
- 차트: 출판사 여럿 = 표 순서 상위 N 판매금액·판매수량(이축), 1곳(출판사 계정) = 수량 구성.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "stats" / "publisher" / "page.tsx"
sys.path.insert(0, str(BACKEND))


class PublisherStatsService(IsolatedAsyncioTestCase):
    async def test_new_fields_and_totals(self):
        from app.services import stats_service

        async def fake_summary(**kw):
            return {"rows": [
                {"hcode": "P1", "book_count": 3, "giqut": 10, "goqut": 200, "gbqut": -10, "gbsum": -1000,
                 "gjqut": 5, "gpqut": 2, "gosum": 20000, "gpsum": 0, "gdate": "2026.09.01"},
                {"hcode": "P2", "book_count": 1, "giqut": 0, "goqut": 0, "gbqut": -3, "gbsum": -300,
                 "gjqut": 0, "gpqut": 0, "gosum": 0, "gpsum": 0, "gdate": "2026.09.02"},
            ]}

        async def fake_names(server_id, hcodes):
            return {"P1": "출판1", "P2": "출판2"}

        old = (stats_service.reports_service.get_publisher_sales_summary, stats_service.inbound_service._fetch_publisher_names)
        stats_service.reports_service.get_publisher_sales_summary = fake_summary
        stats_service.inbound_service._fetch_publisher_names = fake_names
        try:
            res = await stats_service.get_publisher_stats(
                server_id="remote_153", hcode=None, date_from="2026-09-01", date_to="2026-09-30",
                sort_by="sale_amt", sort_dir="desc",
            )
        finally:
            stats_service.reports_service.get_publisher_sales_summary, stats_service.inbound_service._fetch_publisher_names = old
        p1 = res["items"][0]
        self.assertEqual(p1["publisher_code"], "P1")
        self.assertEqual((p1["gift_qut"], p1["disposal_qut"], p1["return_sum"]), (5, 2, -1000))
        self.assertEqual((p1["sale_qut"], p1["sale_amt"], p1["return_rate"]), (190, 19000, 5.0))
        self.assertEqual(res["items"][1]["return_rate"], 0.0)  # 출고 0 → 0
        t = res["totals"]
        self.assertEqual((t["sale_qut_total"], t["sale_amt_total"], t["gift_total"]), (187, 18700, 5))
        self.assertEqual(t["return_rate"], 6.5)  # Σ(−반품) 13 ÷ Σ출고 200


class PublisherPage(TestCase):
    def setUp(self):
        self.src = PAGE.read_text(encoding="utf-8")

    def test_columns_labels(self):
        body = self.src.split("const PUBLISHER_COLUMNS")[1].split("];")[0]
        self.assertNotIn('label: "잔량"', body)
        labels = ["출판사", "코드", "도서수", "입고수량", "출고수량", "증정수량", "반품수량", "폐기수량",
                  "출고금액", "반품금액", "판매금액", "반품율(%)"]
        pos = [body.index(f'label: "{l}"') for l in labels]
        self.assertEqual(pos, sorted(pos))
        self.assertIn('const PUBLISHER_DEFAULT_HIDDEN = ["last_date"] as const;', self.src)

    def test_totals_chart_export(self):
        self.assertIn('totalsLabel="총합"', self.src)
        self.assertIn("const single = (data?.totals.publisher_count ?? 0) <= 1;", self.src)
        self.assertIn("secondaryAxisRaw", self.src)
        self.assertIn(".concat(exportOnlyColumns)", self.src)

    def test_router_export_default(self):
        router = (BACKEND / "app" / "routers" / "stats.py").read_text(encoding="utf-8")
        body = router.split("_PUBLISHER_EXPORT_COLUMNS = [")[1].split("]\n")[0]
        self.assertNotIn('"잔량"', body)
        for k in ('"gift_qut"', '"sale_amt"', '"return_rate"', '"last_date"'):
            self.assertIn(k, body)


if __name__ == "__main__":
    main(verbosity=2)
