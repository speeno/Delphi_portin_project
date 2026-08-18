"""전표번호(jubun) 단독 LIST — Subu21 자동채움 UX 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class JubunPrimaryListTest(IsolatedAsyncioTestCase):
    async def test_list_jubun_only_without_gcode_returns_rows(self) -> None:
        """전표번호만(gcode 없음)으로 LIST 가 차단되지 않고 행을 돌려준다.

        원래는 remote_153 라이브 DB 조회였으나(servers.yaml 터널 의존 — 스위트 전체
        실행 시 이벤트 루프 순서에 따라 실패), 서비스·어댑터의 execute_query 를
        fake 로 대체해 "jubun 단독 → Jubun 필터가 걸린 목록 SQL 실행 + 행 반환" 만
        검증한다.
        """
        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl
        import app.services.s1_ssub_adapt as s1a
        import app.services.h2_gbun_adapt as h2a

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
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
            if "row_count" in sql.lower() and "GROUP BY" not in sql:
                return [{"row_count": 1}]
            if "FROM S1_Ssub" in sql and "GROUP BY" in sql:
                return [
                    {
                        "Gdate": "2026.05.25",
                        "Hcode": "5019",
                        "Jubun": "11",
                        "Gjisa": "",
                        "stmt_gcode": "00004",
                        "idnum": 1,
                        "row_count": 1,
                        "qty": 1,
                        "amount": 1,
                        "yesno_max": "2",
                    }
                ]
            return []

        async def fake_count(*_a, **_k):
            return 1

        async def fake_pairs(_sid, _pairs):
            return {}

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        old_pairs = transactions_service.fetch_g1_customer_gnames
        old_assert = h2bl.assert_sales_statement_search_allowed
        old_s1_q = s1a.execute_query
        old_h2_q = h2a.execute_query
        transactions_service.execute_query = fake_query
        transactions_service.count_grouped = fake_count
        transactions_service.fetch_g1_customer_gnames = fake_pairs
        h2bl.assert_sales_statement_search_allowed = noop_assert
        s1a.execute_query = fake_query
        h2a.execute_query = fake_query
        s1a.clear_s1_column_cache_for_tests()
        h2a.clear_h2_column_cache_for_tests()
        try:
            items, total = await transactions_service.list_sales_statements(
                server_id="remote_153",
                hcode="5019",
                date_from="2026-05-25",
                date_to="2026-06-04",
                jubun="11",
                gcode=None,
                limit=5,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            transactions_service.fetch_g1_customer_gnames = old_pairs
            h2bl.assert_sales_statement_search_allowed = old_assert
            s1a.execute_query = old_s1_q
            h2a.execute_query = old_h2_q
            s1a.clear_s1_column_cache_for_tests()
            h2a.clear_h2_column_cache_for_tests()

        list_sql, list_params = next(
            (s, p) for s, p in captured if "FROM S1_Ssub" in s and "GROUP BY" in s
        )
        self.assertIn("Jubun", list_sql)
        self.assertIn("11", list_params)
        self.assertGreater(total, 0)
        self.assertGreater(len(items), 0)
        self.assertEqual(items[0].get("order_key", {}).get("jubun"), "11")

    async def test_customer_preview_stock_uses_bcode(self) -> None:
        from app.services import transactions_service

        captured: list[tuple[str, str, str]] = []

        async def fake_stock(_server_id, *, bcode, hcode, ocode="B"):
            captured.append((bcode, hcode, ocode))
            return 42

        async def fake_profile(*_a, **_k):
            return {"gname": "테스트"}

        async def fake_memo(*_a, **_k):
            return {}

        old_stock = transactions_service.compute_sales_statement_stock_qty
        old_prof = transactions_service.fetch_g1_customer_profile
        old_memo = transactions_service.load_sales_statement_memo_preview
        transactions_service.compute_sales_statement_stock_qty = fake_stock
        transactions_service.fetch_g1_customer_profile = fake_profile
        transactions_service.load_sales_statement_memo_preview = fake_memo
        try:
            out = await transactions_service.get_sales_statement_customer_preview(
                server_id="remote_138",
                gcode="00004",
                date_from="2026-05-14",
                date_to="2026-05-14",
                hcode="5019",
                bcode="BK99",
                ocode="B",
                g1_fallback_hcodes=("5019",),
            )
        finally:
            transactions_service.compute_sales_statement_stock_qty = old_stock
            transactions_service.fetch_g1_customer_profile = old_prof
            transactions_service.load_sales_statement_memo_preview = old_memo

        self.assertEqual(captured, [("BK99", "5019", "B")])
        self.assertEqual(out.get("stock_qty"), 42)


if __name__ == "__main__":
    from unittest import main

    main()
