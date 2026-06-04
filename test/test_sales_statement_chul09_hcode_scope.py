"""chul_09_db 거래명세서 — Hnnnn·Ocode A·H2 scope 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class Chul09HcodeScopeTest(TestCase):
    def test_resolve_h2_hcode_chul09_uses_scope(self) -> None:
        from app.services.h2_gbun_adapt import (
            clear_h2_column_cache_for_tests,
            resolve_h2_hcode_for_customer,
            server_uses_session_hcode_for_branches,
        )

        self.assertTrue(server_uses_session_hcode_for_branches("remote_153"))
        self.assertEqual(
            resolve_h2_hcode_for_customer("remote_153", "00004", "5019"),
            "5019",
        )
        self.assertEqual(
            resolve_h2_hcode_for_customer("remote_no_such", "00004", "5019"),
            "",
        )
        clear_h2_column_cache_for_tests()

    def test_sales_statement_ocode_chul09_is_a(self) -> None:
        from app.services.h2_gbun_adapt import sales_statement_ocode_sql

        self.assertEqual(sales_statement_ocode_sql("remote_153"), "Ocode = 'A'")
        self.assertEqual(sales_statement_ocode_sql("remote_no_such"), "Ocode = 'B'")


class Chul09ListSqlTest(IsolatedAsyncioTestCase):
    async def test_list_where_uses_hcode_5019_and_ocode_a(self) -> None:
        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "row_count" in sql.lower():
                return [{"row_count": 1}]
            return [
                {
                    "Gdate": "2026.05.14",
                    "Hcode": "5019",
                    "Jubun": "11",
                    "Gjisa": "온라인",
                    "stmt_gcode": "00004",
                    "row_count": 1,
                    "qty": 1,
                    "amount": 1,
                    "yesno_max": "2",
                }
            ]

        async def fake_count(*_a, **_k):
            return 1

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        old_assert = h2bl.assert_sales_statement_search_allowed
        transactions_service.execute_query = fake_query
        transactions_service.count_grouped = fake_count
        h2bl.assert_sales_statement_search_allowed = noop_assert
        try:
            await transactions_service.list_sales_statements(
                server_id="remote_153",
                hcode="5019",
                date_from="2026-05-14",
                date_to="2026-05-14",
                gcode="00004",
                gubun="출고",
                gjisa="온라인",
                limit=10,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            h2bl.assert_sales_statement_search_allowed = old_assert

        list_sql = next(
            (s for s, _ in captured if "FROM S1_Ssub" in s and "GROUP BY" in s),
            "",
        )
        self.assertIn("Hcode = %s", list_sql)
        self.assertIn("Ocode = 'A'", list_sql)
        self.assertNotIn("Ocode = 'B'", list_sql)
        self.assertNotIn("HAVING MAX(Yesno)", list_sql)
