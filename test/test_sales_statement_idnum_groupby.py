"""DEC-064 §Idnum 정합 회귀 — _GROUP_BY_STMT_KEYS 6축 + idnum 필터 + 합성키 7세그먼트."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class IdnumGroupByTest(TestCase):
    """`_GROUP_BY_STMT_KEYS` / `_SELECT_STMT_GROUP_KEYS` 6축 합성키 정적 회귀."""

    def test_group_by_keys_include_idnum_gubun_gcode(self) -> None:
        from app.services import transactions_service as svc

        gb = svc._GROUP_BY_STMT_KEYS
        # Idnum, Gubun, Gcode 모두 GROUP BY 키에 포함되어야 1슬립=1행 보장.
        self.assertIn("COALESCE(Idnum,0)", gb)
        self.assertIn("Gubun", gb)
        self.assertIn("Gcode", gb)

    def test_select_keys_surface_idnum_gubun_stmt_gcode(self) -> None:
        from app.services import transactions_service as svc

        sel = svc._SELECT_STMT_GROUP_KEYS
        self.assertIn("AS Idnum", sel)
        self.assertIn("Gubun", sel)
        # MAX(Gcode) 패턴 제거 — Gcode 자체가 group key.
        self.assertNotIn("MAX(Gcode)", sel)
        self.assertIn("AS stmt_gcode", sel)


class IdnumFilterHelperTest(TestCase):
    """`_append_idnum_filter` — Subu21 Button901Click L924 ``Idnum= @Idnum`` 동등."""

    def test_skip_when_blank_or_zero(self) -> None:
        from app.services import transactions_service as svc

        for raw in ("", "   ", None, 0, "0"):
            where: list[str] = []
            params: list[object] = []
            svc._append_idnum_filter(where, params, raw)
            self.assertEqual(where, [], f"value={raw!r}")
            self.assertEqual(params, [])

    def test_int_match_with_zero_pad_stripped(self) -> None:
        from app.services import transactions_service as svc

        where: list[str] = []
        params: list[object] = []
        svc._append_idnum_filter(where, params, "00001")
        self.assertEqual(where, ["COALESCE(Idnum,0) = %s"])
        self.assertEqual(params, [1])

    def test_int_match_for_plain_integer(self) -> None:
        from app.services import transactions_service as svc

        where: list[str] = []
        params: list[object] = []
        svc._append_idnum_filter(where, params, 42)
        self.assertEqual(where, ["COALESCE(Idnum,0) = %s"])
        self.assertEqual(params, [42])


class StmtLineWhereExtendedTest(TestCase):
    """`_build_stmt_line_where` — idnum/gubun/gcode 부착 시 단일 슬립 매칭."""

    def test_legacy_empty_jubun_backward_compat(self) -> None:
        from app.services import transactions_service as svc

        sql, params = svc._build_stmt_line_where(
            "2026.05.14", "5019", "", ""
        )
        self.assertIn("Gdate=%s", sql)
        self.assertIn("Hcode=%s", sql)
        self.assertIn("COALESCE(Jubun,'')=%s", sql)
        self.assertIn("Scode = 'X'", sql)
        self.assertNotIn("COALESCE(Idnum,0)=%s", sql)
        self.assertNotIn("Gubun=%s", sql)
        self.assertEqual(params, ["2026.05.14", "5019", "", ""])

    def test_jubun_non_empty_uses_variants_in(self) -> None:
        from app.services import transactions_service as svc

        sql, params = svc._build_stmt_line_where(
            "2026.05.14", "5019", "11", ""
        )
        self.assertIn("COALESCE(Jubun,'') IN", sql)
        self.assertIn("11", params)

    def test_extended_attaches_idnum_gubun_gcode(self) -> None:
        from app.services import transactions_service as svc

        sql, params = svc._build_stmt_line_where(
            "2026.05.14",
            "5019",
            "11",
            "",
            idnum=1,
            gubun="출고",
            gcode="00004",
        )
        self.assertIn("COALESCE(Idnum,0)=%s", sql)
        self.assertIn("Gubun=%s", sql)
        # Gcode 는 IN(variants) — gcode_lookup_variants 사용.
        self.assertIn("Gcode IN", sql)
        self.assertIn(1, params)
        self.assertIn("출고", params)


class OrderKey7SegmentTest(TestCase):
    """`inquiry_order_key.parse_sales_statement_order_key_extended` — 4·7세그먼트 호환."""

    def test_legacy_4_segment(self) -> None:
        from app.services.inquiry_order_key import (
            parse_sales_statement_order_key_extended,
        )

        out = parse_sales_statement_order_key_extended(
            "2026.05.14|5019|11|"
        )
        self.assertEqual(out["gdate"], "2026.05.14")
        self.assertEqual(out["hcode"], "5019")
        self.assertEqual(out["jubun"], "11")
        self.assertEqual(out["gjisa"], "")
        self.assertEqual(out["idnum"], 0)
        self.assertEqual(out["gubun"], "")
        self.assertEqual(out["gcode"], "")

    def test_extended_7_segment(self) -> None:
        from app.services.inquiry_order_key import (
            parse_sales_statement_order_key_extended,
        )

        out = parse_sales_statement_order_key_extended(
            "2026.05.14|5019|11||1|%EC%B6%9C%EA%B3%A0|00004"
        )
        self.assertEqual(out["idnum"], 1)
        self.assertEqual(out["gubun"], "출고")
        self.assertEqual(out["gcode"], "00004")

    def test_invalid_segment_count_rejected(self) -> None:
        from app.services.inquiry_order_key import (
            parse_sales_statement_order_key_extended,
        )

        with self.assertRaises(ValueError):
            parse_sales_statement_order_key_extended("a|b|c|d|e|f")
        with self.assertRaises(ValueError):
            parse_sales_statement_order_key_extended("a|b|c|d|e|f|g|h")
        with self.assertRaises(ValueError):
            parse_sales_statement_order_key_extended("|x|11")


class StatementKeyPydanticTest(TestCase):
    """`StatementKey` 모델 — idnum/gubun/gcode 기본값 backward-compat."""

    def test_legacy_input_still_validates(self) -> None:
        from app.models.inquiry import StatementKey

        sk = StatementKey(gdate="2026.05.14", hcode="5019", jubun="11", gjisa="")
        self.assertEqual(sk.idnum, 0)
        self.assertEqual(sk.gubun, "")
        self.assertEqual(sk.gcode, "")

    def test_extended_input_round_trips(self) -> None:
        from app.models.inquiry import StatementKey

        sk = StatementKey(
            gdate="2026.05.14",
            hcode="5019",
            jubun="11",
            gjisa="",
            idnum=1,
            gubun="출고",
            gcode="00004",
        )
        self.assertEqual(sk.idnum, 1)
        self.assertEqual(sk.gubun, "출고")
        self.assertEqual(sk.gcode, "00004")


class RowKeyCaseInsensitiveTest(TestCase):
    """소문자 SQL alias — LIST ``order_key.idnum`` / ``gcode`` surface."""

    def test_stmt_list_fields_lowercase_keys(self) -> None:
        from app.services import transactions_service as svc

        row = {
            "gdate": "2026.06.04",
            "hcode": "5019",
            "jubun": "11",
            "gjisa": "",
            "idnum": 1,
            "gubun": "출고",
            "gcode": "00405",
        }
        fields = svc._stmt_list_fields_from_row(row)
        self.assertEqual(fields["idnum"], 1)
        self.assertEqual(fields["gcode"], "00405")


class ListItemSurfacesIdnumTest(IsolatedAsyncioTestCase):
    """LIST 응답의 ``order_key`` 가 idnum/gubun/gcode 도 surface 하는지 회귀."""

    async def test_list_items_surface_extended_keys(self) -> None:
        from app.services import transactions_service as svc
        import app.services.h2_branch_lookup as h2bl

        async def noop_assert(**_kwargs):
            return None

        # GROUP BY 결과 1행을 가짜 fetch — 6축 surface 검증.
        # mysql3/aiomysql — 소문자 alias 회귀 (DEC-064 §Idnum 상세수정).
        fake_grouped_row = {
            "gdate": "2026.05.14",
            "hcode": "5019",
            "idnum": 1,
            "gubun": "출고",
            "jubun": "11",
            "gjisa": "",
            "gcode": "00004",
            "row_count": 3,
            "qty": 30,
            "amount": 50000,
            "yesno_max": "1",
        }

        async def fake_execute_query(_sid, _sql, _params=()):
            # 첫 호출은 base_select(GROUP BY), 후속은 g1_gname 등 → 빈 리스트 반환.
            if "S1_Ssub" in _sql and "GROUP BY" in _sql:
                return [fake_grouped_row]
            return []

        old_assert = h2bl.assert_sales_statement_search_allowed
        old_eq = svc.execute_query
        old_pairs = svc.fetch_g1_customer_gnames
        old_count = svc.count_grouped
        h2bl.assert_sales_statement_search_allowed = noop_assert
        svc.execute_query = fake_execute_query

        async def fake_pairs(_sid, _pairs):
            return {}

        async def fake_count(*_args, **_kwargs):
            return 1

        async def fake_has_idnum(_sid):
            return True

        async def fake_idnum_group(_sid):
            return "COALESCE(Idnum,0)"

        async def fake_idnum_select(_sid):
            return "COALESCE(Idnum,0) AS Idnum"

        svc.fetch_g1_customer_gnames = fake_pairs
        svc.count_grouped = fake_count
        try:
            import app.services.s1_ssub_adapt as s1a

            old_has = s1a.s1_has_idnum_column
            old_grp = s1a.s1_idnum_group_expr
            old_sel = s1a.s1_idnum_select_expr
            s1a.s1_has_idnum_column = fake_has_idnum
            s1a.s1_idnum_group_expr = fake_idnum_group
            s1a.s1_idnum_select_expr = fake_idnum_select
            items, total = await svc.list_sales_statements(
                server_id="remote_153",
                hcode="5019",
                date_from="2026-05-14",
                date_to="2026-05-14",
                limit=10,
                offset=0,
            )
        finally:
            h2bl.assert_sales_statement_search_allowed = old_assert
            svc.execute_query = old_eq
            svc.fetch_g1_customer_gnames = old_pairs
            svc.count_grouped = old_count
            s1a.s1_has_idnum_column = old_has
            s1a.s1_idnum_group_expr = old_grp
            s1a.s1_idnum_select_expr = old_sel

        self.assertEqual(len(items), 1)
        ok = items[0]["order_key"]
        self.assertEqual(ok["idnum"], 1)
        self.assertEqual(ok["gubun"], "출고")
        self.assertEqual(ok["gcode"], "00004")
        self.assertEqual(ok["jubun"], "11")
        self.assertEqual(total, 1)


if __name__ == "__main__":
    from unittest import main

    main()
