"""S1_Ssub Gjisa lookup variants — pipe·dot·공백 정규화 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class GjisaLookupVariantsTest(TestCase):
    def test_pipe_and_dot_bugokri(self) -> None:
        from app.services.h2_gbun_adapt import gjisa_lookup_variants

        v = gjisa_lookup_variants("2|부곡리(매장)")
        self.assertIn("2|부곡리(매장)", v)
        self.assertIn("2.부곡리(매장)", v)
        self.assertIn("부곡리(매장)", v)

    def test_dot_input_expands_to_pipe(self) -> None:
        from app.services.h2_gbun_adapt import gjisa_lookup_variants

        v = gjisa_lookup_variants("2.부곡리(매장)")
        self.assertIn("2|부곡리(매장)", v)
        self.assertIn("부곡리(매장)", v)

    def test_gwanghwamun_pipe(self) -> None:
        from app.services.h2_gbun_adapt import gjisa_lookup_variants

        v = gjisa_lookup_variants("01|광화문점")
        self.assertIn("01|광화문점", v)
        self.assertIn("광화문점", v)

    def test_paren_space_normalization(self) -> None:
        from app.services.h2_gbun_adapt import gjisa_lookup_variants

        v = gjisa_lookup_variants("부곡리 (매장)")
        self.assertIn("부곡리(매장)", v)


class GjisaFilterSqlTest(IsolatedAsyncioTestCase):
    async def test_list_uses_gjisa_in(self) -> None:
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

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        old_assert = h2bl.assert_sales_statement_search_allowed
        transactions_service.execute_query = fake_query
        transactions_service.count_grouped = fake_count
        h2bl.assert_sales_statement_search_allowed = noop_assert

        # 어댑터(SHOW COLUMNS 캐시) 는 자체 import 한 execute_query 를 쓰므로 함께 fake 로
        # 대체 — 미대체 시 servers.yaml 라이브 DB 로 나가 스위트 실행 순서(이벤트 루프)
        # 에 따라 실패하던 순서 의존을 제거한다.
        import app.services.s1_ssub_adapt as s1a
        import app.services.h2_gbun_adapt as h2a

        async def fake_adapter_query(_server_id, sql, params=None):
            up = sql.strip().upper()
            if up.startswith("SHOW COLUMNS FROM S1_SSUB"):
                return [{"Field": f} for f in (
                    "Gdate", "Hcode", "Jubun", "Gjisa", "Gcode", "Bcode", "Gubun",
                    "Scode", "Ocode", "Yesno", "Gsqut", "Gssum", "Gbigo", "Idnum",
                )]
            if up.startswith("SHOW COLUMNS FROM H2_GBUN"):
                return [{"Field": f} for f in (
                    "id", "Scode", "Gcode", "Hcode", "Gname", "oname", "gdate",
                    "gnum1", "jubun", "gbigo",
                )]
            return []

        old_s1_q = s1a.execute_query
        old_h2_q = h2a.execute_query
        s1a.execute_query = fake_adapter_query
        h2a.execute_query = fake_adapter_query
        s1a.clear_s1_column_cache_for_tests()
        h2a.clear_h2_column_cache_for_tests()
        try:
            await transactions_service.list_sales_statements(
                server_id="remote_138",
                date_from="2026-05-14",
                date_to="2026-05-14",
                gcode="00001",
                gjisa="2|부곡리(매장)",
                limit=10,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            h2bl.assert_sales_statement_search_allowed = old_assert
            s1a.execute_query = old_s1_q
            h2a.execute_query = old_h2_q
            s1a.clear_s1_column_cache_for_tests()
            h2a.clear_h2_column_cache_for_tests()

        list_sql = next(
            (s for s, _ in captured if "FROM S1_Ssub" in s and "GROUP BY" in s),
            "",
        )
        self.assertIn("COALESCE(Gjisa,'') IN", list_sql)
        self.assertIn("Scode = 'X'", list_sql)

    async def test_customer_preview_memo_load(self) -> None:
        from app.services import transactions_service
        import app.services.h2_gbun_adapt as h2a
        import app.services.s1_memo_adapt as s1m

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "S1_Memo" in sql:
                return [{"Gbigo": "선주문", "Sbigo": "", "Gtel1": "", "Gtel2": "", "Gname": "", "Gpost": ""}]
            if "SUM(Gsqut)" in sql:
                return [{"stock_qty": 9}]
            return []

        async def fake_profile(*_a, **_k):
            return {"gname": "교보문고", "address": "서울", "phone": "", "fax": "", "gposa": ""}

        async def fake_meta(_server_id):
            cols = {
                "gdate", "gcode", "gubun", "jubun", "gjisa", "hcode", "scode",
                "gbigo", "sbigo", "gtel1", "gtel2", "gname", "gpost", "ocode",
            }
            exact = {k: k.capitalize() if k != "gcode" else "Gcode" for k in cols}
            exact.update({"gdate": "Gdate", "gjisa": "Gjisa", "gbigo": "Gbigo", "sbigo": "Sbigo"})
            return cols, exact

        async def fake_gjisa(*_a, **_k):
            return ("2|부곡리(매장)",)

        old = transactions_service.execute_query
        old_profile = transactions_service.fetch_g1_customer_profile
        old_meta = s1m.s1_memo_column_meta
        old_gj = h2a.gjisa_search_variants
        transactions_service.execute_query = fake_query
        transactions_service.fetch_g1_customer_profile = fake_profile
        s1m.s1_memo_column_meta = fake_meta
        h2a.gjisa_search_variants = fake_gjisa
        try:
            res = await transactions_service.get_sales_statement_customer_preview(
                server_id="remote_138",
                gcode="00001",
                date_from="2026-05-14",
                date_to="2026-05-14",
                gjisa="2|부곡리(매장)",
                gubun="출고",
                jubun="00001",
            )
        finally:
            transactions_service.execute_query = old
            transactions_service.fetch_g1_customer_profile = old_profile
            s1m.s1_memo_column_meta = old_meta
            h2a.gjisa_search_variants = old_gj

        self.assertEqual(res["memo_preview"].get("gbigo"), "선주문")
        memo_sql = next((s for s, _ in captured if "FROM S1_Memo" in s), "")
        self.assertRegex(memo_sql, r"COALESCE\([Gg]jisa,''\)\s+IN\s+\(")
