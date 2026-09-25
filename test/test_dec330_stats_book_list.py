"""
DEC-330 — 도서통계(목록) 컬럼 재구성·판매금액·반품율·총합·엑셀 전 필드(사용자 2026-09-25, DEC-328 과 같은 방식).

- 컬럼: 구분·도서명·입고·출고·증정·반품·폐기수량·출고금액·반품금액·판매금액·반품율(%).
- 코드·ISBN·최종거래일 = 컬럼 설정의 선택 컬럼(기본 숨김). 정가 제외.
- 반품율 = −반품수량 ÷ 출고수량 × 100(레거시 Subu69_1 도서별판매율), 합계 반품율 = Σ(−반품) ÷ Σ출고 × 100.
- 엑셀 = 전 필드(숨긴 선택 컬럼 포함), 하단 총합 = 검색 결과 전체.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "stats" / "book" / "page.tsx"
sys.path.insert(0, str(BACKEND))


class BookSalesSaleAmtAndRate(IsolatedAsyncioTestCase):
    async def test_rows_and_totals(self):
        from app.services import reports_service as rs

        async def fake_exec(server_id, sql, params=()):
            if "FROM S1_Ssub" in sql:
                return [
                    {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gdate": "2026.09.01", "Gsqut": 100, "Gssum": 10000},
                    {"Bcode": "B1", "Scode": "X", "Gubun": "반품", "Pubun": "", "Gdate": "2026.09.02", "Gsqut": -5, "Gssum": -500},
                    {"Bcode": "B2", "Scode": "X", "Gubun": "반품", "Pubun": "", "Gdate": "2026.09.03", "Gsqut": -2, "Gssum": -200},
                ]
            return []

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            return []

        async def noop(*a, **k):
            return None

        olds = (rs.execute_query, rs.in_clause_lookup, rs._attach_meta_soft, rs._attach_book_class_soft)
        rs.execute_query, rs.in_clause_lookup = fake_exec, fake_lookup
        rs._attach_meta_soft = rs._attach_book_class_soft = noop
        try:
            res = await rs.get_book_sales(server_id="remote_153", hcode="5019",
                                          date_from="2026.09.01", date_to="2026.09.30",
                                          sort_by="return_rate", sort_dir="desc")
        finally:
            rs.execute_query, rs.in_clause_lookup, rs._attach_meta_soft, rs._attach_book_class_soft = olds
        b1 = next(r for r in res["rows"] if r["gcode"] == "B1")
        b2 = next(r for r in res["rows"] if r["gcode"] == "B2")
        self.assertEqual((b1["sale_amt"], b1["return_rate"]), (9500, 5.0))
        self.assertEqual((b2["sale_amt"], b2["return_rate"]), (-200, 0.0))  # 출고 0 → 0
        self.assertEqual(res["rows"][0]["gcode"], "B1")                     # return_rate 정렬 허용
        self.assertEqual((res["totals"]["sale_amt"], res["totals"]["return_rate"]), (9300, 7.0))

    def test_models_and_export_allowlist(self):
        from app.models.inquiry import BookSalesRow, BookSalesTotals
        from app.routers.reports import _BOOK_SALES_EXPORT_KEYS

        self.assertIn("return_rate", BookSalesRow.model_fields)
        self.assertIs(BookSalesTotals.model_fields["return_rate"].annotation, float)
        self.assertTrue({"sale_amt", "return_rate"} <= _BOOK_SALES_EXPORT_KEYS)


class StatsBookPage(TestCase):
    def setUp(self):
        self.src = PAGE.read_text(encoding="utf-8")

    def test_columns_order_and_optional(self):
        body = self.src.split("const BOOK_COLUMNS")[1].split("];")[0]
        labels = ["구분", "도서명", "입고수량", "출고수량", "증정수량", "반품수량", "폐기수량",
                  "출고금액", "반품금액", "판매금액", "반품율(%)"]
        pos = [body.index(f'label: "{l}"') for l in labels]
        self.assertEqual(pos, sorted(pos))
        self.assertNotIn('label: "정가"', body)
        self.assertIn('const BOOK_DEFAULT_HIDDEN = ["gcode", "gisbn", "gdate"] as const;', self.src)
        self.assertIn('useGridPrefs(user?.server_id, "stats.book.v2", { defaultHidden: BOOK_DEFAULT_HIDDEN })', self.src)

    def test_totals_and_export_all(self):
        self.assertIn('totalsLabel="총합"', self.src)
        self.assertIn("setTotals(res.totals ?? null)", self.src)
        self.assertIn("columns: allColumns.map((c) => ({ key: c.id ?? c.key, label: c.label }))", self.src)


if __name__ == "__main__":
    main(verbosity=2)
