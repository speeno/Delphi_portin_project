"""DEC-138 — 도서별판매 일자×도서 축 + 기간말 재고 3종(수불 누적) 회귀 가드.

영업팀 Q1~Q3 회신(2026-08-11) 반영:
- Q1=②: 재고 = 설정 기간 말 시점, 수불 누적 계산(레거시 Tong04.pas TTong40 산식).
  라이브 대사: 도서 3411(교문사 5019) asof 07.09=981 / 07.16=960 — 레거시
  도서별수불원장 현재고와 정확 일치 확인(2026-08-11).
- Q2: 검색 팝업 [선택] 버튼 유지(오클릭 대비).
- Q3: 회신 누락 — 원문 의견("동일 일자 여러 도서 → 클릭 시 우측 상세")대로
  일자×도서 다행 가정(가정 기록은 DEC-138).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import reports_service as rpt  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class StockBranchTableTests(TestCase):
    """Tong40 정품재고(GsumX) 분기표 1:1 — _apply_stock_branch."""

    def test_branches(self) -> None:
        cases = [
            # (scode, gubun, pubun, q) -> 기대 증감
            (("Y", "입고", "", 700), 700),          # 입고 +
            (("Y", "반품", "반품", 3), 3),           # Y 반품/반품 +
            (("Y", "", "반품", 2), 2),               # Y *,반품 + (반품재고→정품 회수)
            (("X", "출고", "", 5), -5),              # 출고 −
            (("X", "", "증정", 1), -1),              # 증정 −
            (("X", "폐기", "", -4), -4),             # 폐기(음수 저장 관례) → GsumX += q
            (("X", "폐기", "비품", -4), 0),          # 폐기+비품 → 반품재고 버킷(정품 무영향)
            (("X", "", "비품", 7), 0),               # 비품 → 정품 무영향
            (("X", "반품", "", -2), 2),              # (비Y) 반품 → GsumX −= q (음수 관례)
            (("X", "이동", "", 9), 0),               # 분기표 밖 → 무영향
        ]
        for (scode, gubun, pubun, q), want in cases:
            got = rpt._apply_stock_branch(scode, gubun, pubun, q)
            self.assertEqual(got, want, f"{scode}/{gubun}/{pubun}/{q}")


class FetchStockAsofTests(IsolatedAsyncioTestCase):
    async def test_snapshot_plus_delta(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            if "MAX(Gdate)" in sql:
                return [{"d": "2025.12.31"}]
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            captured.append((sql_template, tuple(prefix_params)))
            if "FROM Sv_Ghng" in sql_template:
                # 스냅샷: Σ(Gsusu−Gsqut) = 1000
                return [{"bcode": "B1", "gsum": 1000}]
            # 델타: 출고 30, 입고 10 → −20
            return [
                {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "", "q": 30},
                {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "", "q": 10},
            ]

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            stock = await rpt._fetch_stock_asof(
                "remote_1", hcode="5019", asof="2026.08.10",
                axis_like="%A%", bcodes=["B1"],
            )
        self.assertEqual(stock["B1"], 1000 - 30 + 10)
        # 축 필터가 스냅샷(Scode LIKE)·델타(Ocode LIKE) 양쪽에 전달됐는지.
        sv_sql, sv_params = next(c for c in captured if "FROM Sv_Ghng" in c[0] and "Gcode IN" in c[0])
        self.assertIn("Scode LIKE %s", sv_sql)
        self.assertIn("%A%", sv_params)
        d_sql, d_params = next(c for c in captured if "FROM S1_Ssub" in c[0])
        self.assertIn("Ocode LIKE %s", d_sql)
        self.assertIn("%A%", d_params)
        self.assertIn("Gdate > %s", d_sql)  # 스냅샷 이후 델타

    async def test_no_snapshot_full_delta(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            return [{"d": None}]

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            if "FROM Sv_Ghng" in sql_template:
                return []
            self_sql = sql_template
            assert "Gdate > %s" not in self_sql  # 스냅샷 없으면 전체 누적
            return [{"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "", "q": 7}]

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            stock = await rpt._fetch_stock_asof(
                "remote_1", hcode=None, asof="2026.08.10",
                axis_like=None, bcodes=["B1"],
            )
        self.assertEqual(stock["B1"], 7)


class BookSalesDailyTests(IsolatedAsyncioTestCase):
    async def _run(self, s1_rows, *, include_stock=False):
        async def fake_exec(server_id, sql, params=()):
            if "FROM S1_Ssub" in sql:
                return s1_rows
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            if "FROM G4_Book" in sql_template:
                return [{"bcode": k, "gname": f"도서{k}", "gdang": 500} for k in keys]
            return []

        async def fake_attach(server_id, rows, *, hcode, asof, bcode_key="gcode"):
            for r in rows:
                r["hq_stock"], r["wh_stock"], r["total_stock"] = 700, 300, 1000

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in), \
                patch.object(rpt, "attach_period_end_stock", fake_attach):
            return await rpt.get_book_sales_daily(
                server_id="remote_1", hcode="5019",
                date_from="2026.07.01", date_to="2026.07.16",
                include_stock=include_stock, limit=50,
            )

    async def test_daily_axis_rows_and_zero_exclusion(self) -> None:
        rows = [
            {"Gdate": "2026.07.06", "Bcode": "A", "Scode": "X", "Gubun": "출고",
             "Pubun": "", "Gsqut": 6, "Gssum": 9000},
            {"Gdate": "2026.07.06", "Bcode": "A", "Scode": "X", "Gubun": "",
             "Pubun": "증정", "Gsqut": 3, "Gssum": 0},
            {"Gdate": "2026.07.07", "Bcode": "A", "Scode": "X", "Gubun": "출고",
             "Pubun": "", "Gsqut": 1, "Gssum": 1500},
            # 분기표 밖(이동) 단독 일자 → 전 측정치 0 → 행 제외
            {"Gdate": "2026.07.08", "Bcode": "A", "Scode": "X", "Gubun": "이동",
             "Pubun": "", "Gsqut": 2, "Gssum": 0},
            # 같은 일자 다른 도서 = 별도 행 (Q3 가정: 일자×도서 다행)
            {"Gdate": "2026.07.06", "Bcode": "B", "Scode": "X", "Gubun": "출고",
             "Pubun": "", "Gsqut": 2, "Gssum": 3000},
        ]
        res = await self._run(rows)
        keys = [(r["gdate"], r["gcode"]) for r in res["rows"]]
        self.assertEqual(
            keys,
            [("2026.07.06", "A"), ("2026.07.06", "B"), ("2026.07.07", "A")],
        )
        first = res["rows"][0]
        self.assertEqual((first["goqut"], first["gjqut"]), (6, 3))
        self.assertEqual(first["gname"], "도서A")

    async def test_include_stock_attaches_three_columns(self) -> None:
        rows = [
            {"Gdate": "2026.07.06", "Bcode": "A", "Scode": "X", "Gubun": "출고",
             "Pubun": "", "Gsqut": 6, "Gssum": 9000},
        ]
        res = await self._run(rows, include_stock=True)
        r = res["rows"][0]
        self.assertEqual(
            (r["hq_stock"], r["wh_stock"], r["total_stock"]), (700, 300, 1000)
        )


class DayDetailTests(IsolatedAsyncioTestCase):
    async def test_customer_breakdown(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            assert "Gdate = %s" in sql and "Bcode = %s" in sql
            return [
                {"Gcode": "00431", "Scode": "X", "Gubun": "출고", "Pubun": "",
                 "Gsqut": 1, "Gssum": 21000},
                {"Gcode": "00999", "Scode": "X", "Gubun": "이동", "Pubun": "",
                 "Gsqut": 5, "Gssum": 0},  # 전 측정치 0 → 제외
            ]

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            assert "FROM G1_Ggeo" in sql_template
            return [{"gcode": k, "gname": "알라딘" if k == "00431" else ""} for k in keys]

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            res = await rpt.get_book_sales_day_detail(
                server_id="remote_1", hcode="5019",
                gdate="2026.07.09", bcode="3411",
            )
        self.assertEqual(len(res["rows"]), 1)
        self.assertEqual(res["rows"][0]["gcode"], "00431")
        self.assertEqual(res["rows"][0]["gname"], "알라딘")
        self.assertEqual(res["rows"][0]["goqut"], 1)


class RouterWiringTests(IsolatedAsyncioTestCase):
    async def test_daily_mode_dispatch(self) -> None:
        from app.routers import reports as reports_router

        seen: dict = {}

        async def fake_daily(**kw):
            seen.update(kw)
            return {"rows": [], "total": 0,
                    "page": {"limit": 100, "offset": 0, "total": 0, "has_more": False},
                    "truncated": False}

        ctx = {"user_id": "u", "role": "admin", "permissions": ["*"], "hcode": "0000"}
        with patch.object(rpt, "get_book_sales_daily", fake_daily):
            await reports_router.get_book_sales(
                server_id="remote_1", hcode=None,
                date_from="2026.07.01", date_to="2026.07.16",
                bcode_from=None, bcode_to=None, bcode=None, scope=None,
                group_mode="daily", include_stock=True,
                sort_by=None, sort_dir=None, limit=100, offset=0, current=ctx,
            )
        self.assertTrue(seen.get("include_stock"))
        self.assertNotIn("bcode_from", seen)  # daily 모드는 단일 bcode 만


class FrontendSourceGuards(TestCase):
    def test_page_uses_daily_axis_and_stock_columns(self) -> None:
        src = (FRONT / "app" / "(app)" / "reports" / "book-sales" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn('groupMode: "daily"', src)
        self.assertIn("includeStock: true", src)
        for label in ("본사재고", "창고재고", "재고합계"):
            self.assertIn(label, src, f"재고 컬럼 {label} 누락 — DEC-138 회귀")
        self.assertIn("bookSalesDayDetail", src)
        self.assertIn("onRowClick", src)

    def test_lookup_dialog_keeps_select_button(self) -> None:
        # Q2 회신 — [선택] 버튼 유지(오클릭 대비).
        src = (FRONT / "components" / "master" / "master-lookup-dialog.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn("선택", src, "검색 팝업 [선택] 버튼 제거 — Q2 회신 위반")


if __name__ == "__main__":
    main()
