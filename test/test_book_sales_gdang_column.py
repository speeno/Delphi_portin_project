"""도서별판매 정가(Gdang) 컬럼 회귀 — 2026-07-31 사용자 요청.

정가 = G4_Book.Gdang (도서마스터 '단가' = 거래명세서 인쇄 '정가').
- 도서명 lookup 에 Gdang 동승 → 행 ``gdang`` 필드.
- Gdang 부재 테넌트(DDL drift 1054)는 도서명만 폴백(gdang=0) — 500 금지.
- 정렬 화이트리스트·XLSX 내보내기 컬럼 포함.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import reports_service as rs  # noqa: E402


def _s1_row(bcode: str, gssum: int = 100) -> dict[str, Any]:
    return {
        "Bcode": bcode, "Scode": "X", "Gubun": "출고", "Pubun": "",
        "Gdate": "2026.04.10", "Gsqut": 1, "Gssum": gssum,
    }


class BookSalesGdangTests(IsolatedAsyncioTestCase):
    async def _run(self, *, lookup_impl, s1_rows=None):
        captured_templates: list[str] = []

        async def fake_exec(server_id, sql, params):  # noqa: ARG001
            if "S1_Ssub" in sql:
                return s1_rows if s1_rows is not None else [_s1_row("B0001")]
            return []  # Sg_Csum

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=()):  # noqa: ARG001
            captured_templates.append(sql_template)
            return await lookup_impl(sql_template, keys)

        with patch.object(rs, "execute_query", new=fake_exec), patch.object(
            rs, "in_clause_lookup", new=fake_lookup
        ):
            res = await rs.get_book_sales(
                server_id="srv", hcode="H0001",
                date_from="2026-04-01", date_to="2026-04-30",
            )
        return res, captured_templates

    async def test_gdang_included_from_g4_lookup(self) -> None:
        async def lookup(sql_template, keys):  # noqa: ARG001
            return [{"bcode": "B0001", "gname": "기계산업마케팅총람", "gdang": 25000}]

        res, templates = await self._run(lookup_impl=lookup)
        self.assertIn("Gdang", templates[0], "G4 lookup 에 정가(Gdang) 동승")
        row = res["rows"][0]
        self.assertEqual(row["gdang"], 25000)
        self.assertEqual(row["gname"], "기계산업마케팅총람")

    async def test_gdang_missing_column_falls_back_to_names_only(self) -> None:
        calls = {"n": 0}

        async def lookup(sql_template, keys):  # noqa: ARG001
            calls["n"] += 1
            if "Gdang" in sql_template:
                raise RuntimeError("1054 Unknown column 'Gdang'")
            return [{"bcode": "B0001", "gname": "기계산업마케팅총람"}]

        res, _ = await self._run(lookup_impl=lookup)
        self.assertEqual(calls["n"], 2, "Gdang 실패 → 도서명만 재조회")
        row = res["rows"][0]
        self.assertEqual(row["gdang"], 0)
        self.assertEqual(row["gname"], "기계산업마케팅총람", "폴백에서도 도서명 유지")

    async def test_sort_by_gdang_whitelisted(self) -> None:
        async def lookup(sql_template, keys):  # noqa: ARG001
            return [
                {"bcode": "B0001", "gname": "가", "gdang": 10000},
                {"bcode": "B0002", "gname": "나", "gdang": 30000},
            ]

        captured: list[str] = []

        async def fake_exec(server_id, sql, params):  # noqa: ARG001
            if "S1_Ssub" in sql:
                return [_s1_row("B0001"), _s1_row("B0002")]
            return []

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=()):  # noqa: ARG001
            captured.append(sql_template)
            return await lookup(sql_template, keys)

        with patch.object(rs, "execute_query", new=fake_exec), patch.object(
            rs, "in_clause_lookup", new=fake_lookup
        ):
            res = await rs.get_book_sales(
                server_id="srv", hcode="H0001",
                date_from="2026-04-01", date_to="2026-04-30",
                sort_by="gdang", sort_dir="desc",
            )
        self.assertEqual([r["gcode"] for r in res["rows"]], ["B0002", "B0001"])


class ExportColumnsTests(TestCase):
    def test_xlsx_export_has_price_column(self) -> None:
        from app.routers.reports import _BOOK_SALES_EXPORT_COLUMNS

        self.assertIn(("정가", "gdang"), _BOOK_SALES_EXPORT_COLUMNS)


if __name__ == "__main__":
    main()
