"""DEC-169 GROUP 2 (거래/출고 계열) — 도서명 목록에 ISBN(gisbn) 동봉 회귀 가드.

대상
----
- ``transactions_service._fetch_book_line_meta`` : G4_Book lookup 에 ISBN(Gisbn) 동봉
  (컬럼 드리프트 — Gisbn 부재 테넌트는 ``'' AS gisbn``).
- ``transactions_service.list_outbound_status_lines`` : 출고현황 라인 행에 ``gisbn`` 키.
- ``transactions_service.get_sales_statement_detail`` : 거래명세서 라인에 ``gisbn`` 키.
- ``author_history_service.list_author_history`` : ``attach_book_meta`` 후처리 → ``gisbn``
  (전표 단가 gdang 은 마스터 정가로 덮어쓰지 않음).

DB 경계(execute_query / in_clause_lookup / g4_column_names / s1_column_names 등)는
monkeypatch 로 막고 결과 dict 만 본다(라이브 DB 불필요).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import transactions_service as tx  # noqa: E402


class BookLineMetaIsbnTests(IsolatedAsyncioTestCase):
    async def test_select_includes_gisbn_when_column_exists(self) -> None:
        captured: dict = {}

        async def fake_lookup(_sid, *, sql_template, keys, prefix_params=(), **_kw):
            captured["sql"] = sql_template
            captured["prefix"] = prefix_params
            return [{"bcode": "B1", "gname": "도서A", "shelf": "", "gisbn": "9788901234567"}]

        with patch.object(tx, "in_clause_lookup", fake_lookup), \
                patch("app.services.g4_book_adapt.g4_column_names",
                      AsyncMock(return_value={"gcode", "gname", "gisbn"})):
            meta = await tx._fetch_book_line_meta("remote_1", "H0001", ["B1"])

        self.assertIn("IFNULL(Gisbn,'') AS gisbn", captured["sql"])
        self.assertIn("Hcode=%s", captured["sql"])
        self.assertEqual(captured["prefix"], ("H0001",))
        self.assertEqual(meta["B1"]["gisbn"], "9788901234567")

    async def test_select_falls_back_when_gisbn_column_missing(self) -> None:
        captured: dict = {}

        async def fake_lookup(_sid, *, sql_template, keys, prefix_params=(), **_kw):
            captured["sql"] = sql_template
            return [{"bcode": "B1", "gname": "도서A", "shelf": "", "gisbn": ""}]

        with patch.object(tx, "in_clause_lookup", fake_lookup), \
                patch("app.services.g4_book_adapt.g4_column_names",
                      AsyncMock(return_value={"gcode", "gname"})):
            meta = await tx._fetch_book_line_meta("remote_1", "H0001", ["B1"])

        self.assertIn("'' AS gisbn", captured["sql"])
        self.assertNotIn("Gisbn", captured["sql"])
        self.assertEqual(meta["B1"]["gisbn"], "")


class OutboundStatusLinesIsbnTests(IsolatedAsyncioTestCase):
    async def test_lines_carry_gisbn_from_book_meta(self) -> None:
        async def fake_exec(_sid, sql, _params=()):
            if "COUNT(*) AS cnt" in sql:
                return [{"cnt": 1, "qty": 5, "amount": 50000, "hcode": "H0001"}]
            return [
                {"gdate": "2026.04.19", "hcode": "H0001", "jubun": "1", "gcode": "00001",
                 "bcode": "B1", "idnum": 3, "pubun": "위탁", "gsqut": 5, "gdang": 10000,
                 "grat1": 70.0, "gssum": 50000, "gbigo": "", "yesno": "0"},
            ]

        book_rows = AsyncMock(return_value=[
            {"bcode": "B1", "gname": "도서A", "shelf": "", "gisbn": "9788901234567"},
        ])
        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "in_clause_lookup", book_rows), \
                patch.object(tx, "fetch_g1_customer_gnames",
                             AsyncMock(return_value={("H0001", "00001"): "북센"})), \
                patch("app.services.s1_ssub_adapt.s1_column_names",
                      AsyncMock(return_value={"gdang", "grat1", "pubun", "idnum"})), \
                patch("app.services.g4_book_adapt.g4_column_names",
                      AsyncMock(return_value={"gcode", "gname", "gisbn"})):
            lines, _total, _totals = await tx.list_outbound_status_lines(
                server_id="remote_1", date_from="2026-04-01", date_to="2026-04-30",
                hcode="H0001", limit=10, offset=0,
            )

        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["bname"], "도서A")
        self.assertEqual(lines[0]["gisbn"], "9788901234567")
        # 전표 단가(GDANG)는 그대로 — 마스터 정가로 덮어쓰지 않는다.
        self.assertEqual(lines[0]["gdang"], 10000)


class SalesStatementDetailIsbnTests(IsolatedAsyncioTestCase):
    async def test_detail_lines_include_gisbn(self) -> None:
        line_rows = [{
            "Gcode": "00405", "Bcode": "3417", "Gubun": "출고", "Pubun": "위탁",
            "Gsqut": 1, "Gssum": 1000, "Gbigo": "", "Yesno": "1", "Gdang": 1000,
            "Grat1": 85, "idnum": 1, "Gjisa": "", "Ocode": "A",
        }]

        async def fake_exec(_sid, sql, _params=()):
            if "FROM S1_Memo" in sql:
                return []
            if "FROM S1_Ssub" in sql and "GROUP BY" not in sql:
                return line_rows
            return []

        async def fake_book_meta(_sid, _hc, _bcodes):
            return {bc: {"gname": f"book-{bc}", "shelf": "", "gisbn": f"ISBN-{bc}"} for bc in _bcodes}

        with patch.object(tx, "execute_query", new=fake_exec), \
             patch.object(tx, "_fetch_book_line_meta", new=fake_book_meta), \
             patch.object(tx, "fetch_g1_customer_profile", new=AsyncMock(return_value={"gname": "x"})), \
             patch.object(tx, "fetch_g1_customer_gnames", new=AsyncMock(return_value={})), \
             patch.object(tx, "compute_sales_statement_stock_qty", new=AsyncMock(return_value=0)), \
             patch("app.services.s1_ssub_adapt.detail_lines_select_sql",
                   new=AsyncMock(return_value="Gcode, Bcode, Gubun, Pubun, Gsqut, Gssum, Gbigo, Yesno, Gdang, Grat1, idnum AS Idnum, Gjisa, Ocode")), \
             patch("app.services.s1_memo_adapt.s1_memo_column_meta",
                   new=AsyncMock(return_value=(set(), {}))), \
             patch("app.services.s1_memo_adapt.memo_preview_select_sql", return_value="Gbigo, Sbigo"):
            detail = await tx.get_sales_statement_detail(
                server_id="remote_1", gdate="2026-06-05", hcode="5019", jubun="1", idnum=1,
            )

        self.assertIsNotNone(detail)
        self.assertEqual(detail["lines"][0]["gisbn"], "ISBN-3417")
        self.assertEqual(detail["lines"][0]["gdang"], 1000)


class AuthorHistoryIsbnTests(IsolatedAsyncioTestCase):
    async def test_items_get_gisbn_and_keep_slip_gdang(self) -> None:
        from app.services import author_history_service as ah
        from app.services import book_meta_lookup as bml

        async def fake_exec(_sid, sql, _params=()):
            if "SUM(Gsqut)" in sql:
                return [{"qty": 2, "amount": 20000}]
            return [{
                "Gdate": "2026.05.01", "Idnum": "7", "Gcode": "00001", "Bcode": "B1",
                "Pubun": "위탁", "Gubun": "출고", "Jubun": "1", "Gsqut": 2, "Gssum": 20000,
                "Gdang": 10000, "Grat1": 85, "Yesno": "0",
            }]

        async def fake_author_meta(_sid, _hc, bcodes):
            return {bc: {"gname": f"book-{bc}", "gjeja": "홍길동"} for bc in bcodes}

        async def fake_meta_lookup(_sid, sql_template, keys, prefix_params=(), **_kw):
            # 마스터 정가 99999 — 전표 단가(10000)를 덮어쓰면 안 된다(price_key=None).
            return [{"bcode": k, "gname": f"book-{k}", "gdang": 99999, "gisbn": f"ISBN-{k}"} for k in keys]

        with patch.object(ah, "execute_query", new=fake_exec), \
             patch.object(ah, "_fetch_book_author_meta", new=fake_author_meta), \
             patch.object(ah, "apply_limit_offset_syntax", new=lambda sql, _sid: sql, create=True), \
             patch.object(bml, "in_clause_lookup", new=fake_meta_lookup), \
             patch.object(bml, "g4_book_column_meta",
                          new=AsyncMock(return_value=({"gcode", "gname", "gdang", "gisbn"},
                                                      {"gdang": "Gdang", "gisbn": "Gisbn"}))):
            res = await ah.list_author_history(
                server_id="remote_1", hcode="5019", date_from="2026-05-01", date_to="2026-05-31",
            )

        items = res["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["gisbn"], "ISBN-B1")
        self.assertEqual(items[0]["gdang"], 10000)


if __name__ == "__main__":
    main()
