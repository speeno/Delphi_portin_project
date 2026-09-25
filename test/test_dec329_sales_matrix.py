"""
DEC-329 — 년/월(통계) 세분화 판매 매트릭스 6종(레거시 출판 빌드 Sobo79_1~4 · Sobo73 · Sobo74).

한 서비스(sales_matrix_service) + 한 화면(SalesMatrixScreen) + 설정 6개.
- 월별/일별: 출력조건 1개를 월·일 열로 펼침(레거시 WHERE 그대로), 실제 연월/일자 순 열, 상한 24개월/31일.
- 년/월 비교: 기간 ≤3개(YYYY·YYYY.MM, 년도엔 분기/반기) × 출고·반품·판매·판매금액(+거래처축 수금액).
- 보기: 분류/저자(도서), 구분/지역/담당(거래처) × 항목 표시 여부.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "도서물류관리프로그램"
BACKEND = PRODUCT / "backend"
FE = PRODUCT / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services import sales_matrix_service as sms  # noqa: E402

ROUTES = {
    "book-sales-monthly": ("Sobo79_1", "book", "monthly"),
    "customer-sales-monthly": ("Sobo79_2", "customer", "monthly"),
    "book-sales-daily": ("Sobo79_3", "book", "daily"),
    "customer-sales-daily": ("Sobo79_4", "customer", "daily"),
    "sales-by-book-monthly": ("Sobo73", "book", "compare"),
    "sales-by-customer-monthly": ("Sobo74", "customer", "compare"),
}


class PeriodParsing(TestCase):
    def test_month_buckets_cross_year_and_cap(self):
        self.assertEqual(sms.month_buckets("2025.11", "202602"), ["2025.11", "2025.12", "2026.01", "2026.02"])
        with self.assertRaises(sms.SalesMatrixValidationError):
            sms.month_buckets("2024.01", "2026.01")  # 25개월
        with self.assertRaises(sms.SalesMatrixValidationError):
            sms.month_buckets("2026.03", "2026.01")

    def test_day_buckets_cap(self):
        self.assertEqual(sms.day_buckets("2026-02-27", "2026.03.01"), ["2026.02.27", "2026.02.28", "2026.03.01"])
        with self.assertRaises(sms.SalesMatrixValidationError):
            sms.day_buckets("2026.01.01", "2026.02.01")  # 32일

    def test_compare_period_parts(self):
        self.assertEqual(sms.parse_compare_period("2025", None), {"label": "2025", "lo": "2025.00", "hi": "2025.99"})
        self.assertEqual(sms.parse_compare_period("2026", "q2")["lo"], "2026.04.01")  # 레거시 Seek_Date
        self.assertEqual(sms.parse_compare_period("2026", "H2")["label"], "2026 3~4분기")
        self.assertEqual(sms.parse_compare_period("202603", "")["lo"], "2026.03.00")
        with self.assertRaises(sms.SalesMatrixValidationError):
            sms.parse_compare_period("2026.03", "Q1")  # 분기는 년도 기간에만


class LegacyMeasureWhere(TestCase):
    def test_book_sale_matches_subu79_1(self):
        w, p = sms._book_measure_where("sale")
        self.assertIn("S.Scode <> 'Y'", w)
        self.assertIn("((S.Scode = 'Z' AND S.Pubun <> %s) OR S.Scode = 'X' OR S.Scode = 'Y')", w)
        self.assertEqual(p, ["증정", "폐기", "폐기"])
        w, p = sms._book_measure_where("in")
        self.assertIn("S.Scode = 'Y'", w)

    def test_customer_ret_matches_subu79_2(self):
        w, p = sms._customer_measure_where("ret", "X")
        self.assertEqual(w, ["S.Scode = %s", "S.Scode = 'X'", "S.Gubun = %s"])
        self.assertEqual(p, ["X", "반품"])

    def test_measure_catalog_has_legacy_items(self):
        labels = [m[1] for m in sms.MEASURES]
        self.assertEqual(labels[:6], ["판매수량", "판매금액", "출고수량", "출고금액", "반품수량", "반품금액"])
        self.assertEqual(len(labels), len(set(labels)))


class _FakeDB:
    def __init__(self, sales_rows, h1_rows=None):
        self.sales_rows = sales_rows
        self.h1_rows = h1_rows or []
        self.sqls: list[tuple[str, tuple]] = []

    async def execute_query(self, server_id, sql, params=()):
        self.sqls.append((sql, params))
        return self.h1_rows if "H1_Ssub" in sql else self.sales_rows

    async def in_clause_lookup(self, server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
        if "G4_Book" in sql_template:
            meta = {"B1": ("책1", "C1", "저자A"), "B2": ("책2", "C1", "저자B"), "B3": ("책3", "", "")}
            return [{"Gcode": k, "Gname": meta[k][0], "Gubun": meta[k][1], "Gjeja": meta[k][2]} for k in keys if k in meta]
        if "G4_Gbun" in sql_template or "G1_Gbun" in sql_template:
            return [{"Gcode": "C1", "Gname": "경영"}, {"Gcode": "K1", "Gname": "인터넷서점"}]
        if "G1_Ggeo" in sql_template:
            return [{"Hcode": "5019", "Gcode": k, "Gname": f"거래처{k}", "Gubun": "K1", "Jubun": "서울", "Gpper": "홍"} for k in keys]
        return []


class MatrixService(IsolatedAsyncioTestCase):
    async def _run(self, db, **kw):
        old = (sms.execute_query, sms.in_clause_lookup)
        sms.execute_query, sms.in_clause_lookup = db.execute_query, db.in_clause_lookup
        try:
            return await sms.get_sales_matrix(server_id="remote_153", hcode="5019", **kw)
        finally:
            sms.execute_query, sms.in_clause_lookup = old

    async def test_book_monthly_buckets_totals_and_group_sort(self):
        db = _FakeDB([
            {"K": "B1", "B": "2026.01", "V": 3}, {"K": "B1", "B": "2026.02", "V": -1},
            {"K": "B3", "B": "2026.02", "V": 5}, {"K": "B2", "B": "2025.12", "V": 9},  # 범위 밖 버킷 무시
        ])
        r = await self._run(db, axis="book", period="monthly", measure="sale_qty",
                            month_from="2026.01", month_to="2026.02", layout="class_items")
        self.assertEqual([c["label"] for c in r["columns"]], ["2026.01", "2026.02"])
        self.assertEqual([x["code"] for x in r["rows"]], ["B1", "B3"])  # 분류명 순, 미지정 맨 뒤
        self.assertEqual(r["rows"][0]["group_name"], "경영")
        self.assertEqual((r["rows"][0]["c0"], r["rows"][0]["c1"], r["rows"][0]["total"]), (3, -1, 2))
        self.assertEqual(r["totals"], {"c0": 3, "c1": 4, "total": 7})
        self.assertEqual(r["group_label"], "분류명")
        sql, params = db.sqls[0]
        self.assertIn("S.Hcode = %s", sql)
        self.assertIn("GROUP BY K, B", sql)
        self.assertEqual(params[:3], ("2026.01.00", "2026.02.99", "5019"))

    async def test_group_only_aggregates(self):
        db = _FakeDB([{"K": "B1", "B": "2026.01", "V": 3}, {"K": "B2", "B": "2026.01", "V": 4}])
        r = await self._run(db, axis="book", period="monthly", measure="sale_qty",
                            month_from="2026.01", month_to="2026.01", layout="class_only")
        self.assertEqual(len(r["rows"]), 1)
        self.assertEqual((r["rows"][0]["name"], r["rows"][0]["item_count"], r["rows"][0]["c0"]), ("경영", 2, 7))
        self.assertFalse(r["show_items"])

    async def test_customer_compare_with_receipts(self):
        db = _FakeDB(
            [{"K": "00001", "G": "출고", "Q": 10, "A": 1000}, {"K": "00001", "G": "반품", "Q": -2, "A": -200}],
            h1_rows=[{"K": "00001", "R": 700}, {"K": "00009", "R": 50}],
        )
        r = await self._run(db, axis="customer", period="compare",
                            compare=[("2025", None), ("", None), ("", None)], layout="items")
        self.assertEqual([c["label"] for c in r["columns"]],
                         ["2025 출고", "2025 반품", "2025 판매", "2025 판매금액", "2025 수금액"])
        row = next(x for x in r["rows"] if x["code"] == "00001")
        self.assertEqual((row["p1_out"], row["p1_ret"], row["p1_sale"], row["p1_amt"], row["p1_rcv"]),
                         (10, -2, 8, 800, 700))
        # 판매 없이 수금만 있는 거래처도 행(레거시 수금조회 Append)
        self.assertIn("00009", [x["code"] for x in r["rows"]])
        h1_sql, h1_params = next(s for s in db.sqls if "H1_Ssub" in s[0])
        self.assertIn("Hcode = %s", h1_sql)
        self.assertEqual(h1_params[:2], ("입금", "출금"))

    async def test_validation(self):
        with self.assertRaises(sms.SalesMatrixValidationError):
            await self._run(_FakeDB([]), axis="book", period="compare", compare=[("", None)])
        with self.assertRaises(sms.SalesMatrixValidationError):
            await sms.get_sales_matrix(server_id="x", hcode="", axis="book", period="monthly",
                                       month_from="2026.01", month_to="2026.01")


class ScreenWiring(TestCase):
    def test_six_routes_use_shared_screen(self):
        for route, (lid, axis, period) in ROUTES.items():
            src = (FE / "app" / "(app)" / "year-month-stats" / route / "page.tsx").read_text(encoding="utf-8")
            self.assertIn("<SalesMatrixScreen", src)
            self.assertIn(f'legacyId: "{lid}"', src)
            self.assertIn(f'axis: "{axis}"', src)
            self.assertIn(f'period: "{period}"', src)

    def test_registry_hub_probe_router(self):
        reg = (FE / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        hub = (FE / "app" / "(app)" / "year-month-stats" / "page.tsx").read_text(encoding="utf-8")
        for route, (lid, _a, _p) in ROUTES.items():
            self.assertIn(f'id: "{lid}"', reg)
            self.assertIn(f'route: "/year-month-stats/{route}"', reg)
            self.assertIn(f'"/year-month-stats/{route}"', hub)
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("/api/v1/stats/sales-matrix", probe)
        router = (BACKEND / "app" / "routers" / "stats.py").read_text(encoding="utf-8")
        body = router.split('"/sales-matrix"')[1].split("@router")[0]
        self.assertIn("enforce_hcode_isolation(hcode, ctx)", body)

    def test_screen_features(self):
        src = (FE / "components" / "stats" / "sales-matrix-screen.tsx").read_text(encoding="utf-8")
        for token in ("GridColumnSettings", "useGridPrefs", "totals={totalsForGrid}", "exportTableXlsx",
                      'L("CheckBox2")', 'L("ComboBox1")', 'L("ComboBox2")', "PART_OPTIONS"):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
