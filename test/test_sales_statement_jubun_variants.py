"""S1_Ssub Jubun lookup variants — zero-pad 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class JubunLookupVariantsTest(TestCase):
    def test_zfill_five(self) -> None:
        from app.services.h2_gbun_adapt import jubun_lookup_variants

        v = jubun_lookup_variants("1")
        self.assertIn("00001", v)
        self.assertIn("1", v)

    def test_padded_input(self) -> None:
        from app.services.h2_gbun_adapt import jubun_lookup_variants

        v = jubun_lookup_variants("00001")
        self.assertIn("00001", v)
        self.assertIn("1", v)


class JubunFilterSqlTest(IsolatedAsyncioTestCase):
    async def test_list_where_uses_jubun_in_and_scode(self) -> None:
        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "row_count" in sql.lower():
                return [{"row_count": 0}]
            return []

        async def fake_count(*_a, **_k):
            return 0

        import app.services.h2_gbun_adapt as h2a

        async def fake_gjisa(*_a, **_k):
            return ("온라인",)

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        old_assert = h2bl.assert_sales_statement_search_allowed
        old_gj = h2a.gjisa_search_variants
        transactions_service.execute_query = fake_query
        transactions_service.count_grouped = fake_count
        h2bl.assert_sales_statement_search_allowed = noop_assert
        h2a.gjisa_search_variants = fake_gjisa
        try:
            await transactions_service.list_sales_statements(
                server_id="remote_138",
                date_from="2026-05-14",
                date_to="2026-05-14",
                gcode="00004",
                gubun="출고",
                jubun="1",
                gjisa="온라인",
                limit=10,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            h2bl.assert_sales_statement_search_allowed = old_assert
            h2a.gjisa_search_variants = old_gj

        list_sql, list_params = next(
            (s, p) for s, p in captured if "FROM S1_Ssub" in s and "GROUP BY" in s
        )
        self.assertIn("Scode = 'X'", list_sql)
        self.assertIn("COALESCE(Jubun,'')", list_sql)
        self.assertIn("00001", list_params)


if __name__ == "__main__":
    from unittest import main

    main()
