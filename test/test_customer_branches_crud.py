"""H2_Gbun 거래처별 지사 마스터 — service·gjisa_value 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class H2GbunAdaptTest(IsolatedAsyncioTestCase):
    def test_gjisa_value_from_parts(self) -> None:
        from app.services.h2_gbun_adapt import gjisa_value_from_parts, parse_gjisa_combo

        self.assertEqual(gjisa_value_from_parts("", "강남점"), "강남점")
        self.assertEqual(gjisa_value_from_parts("01", "강남점"), "01|강남점")
        g, j = parse_gjisa_combo("01|강남점")
        self.assertEqual(g, "강남점")
        self.assertEqual(j, "01")
        g2, j2 = parse_gjisa_combo("강남점")
        self.assertEqual(g2, "강남점")
        self.assertEqual(j2, "")

    def test_branch_hcode_for_customer(self) -> None:
        from app.services.h2_gbun_adapt import branch_hcode_for_customer

        self.assertEqual(branch_hcode_for_customer("C001", "H9"), "")
        self.assertEqual(branch_hcode_for_customer("90001", "H9"), "H9")
        self.assertEqual(branch_hcode_for_customer("90001", None), "")

    def test_resolve_h2_hcode_chul09(self) -> None:
        from app.services.h2_gbun_adapt import resolve_h2_hcode_for_customer

        self.assertEqual(
            resolve_h2_hcode_for_customer("remote_153", "00004", "5019"),
            "5019",
        )

    def test_gcode_lookup_variants(self) -> None:
        from app.services.h2_gbun_adapt import gcode_lookup_variants

        self.assertEqual(set(gcode_lookup_variants("00001")), {"00001", "1"})
        self.assertEqual(gcode_lookup_variants("ABC"), ("ABC",))
        self.assertEqual(gcode_lookup_variants(""), ())

    def test_branch_list_order_sql_uses_actual_column_names(self) -> None:
        from app.services.h2_gbun_adapt import branch_list_order_sql

        cols = {"id", "gname", "oname", "scode"}
        exact = {"id": "id", "gname": "gname", "oname": "oname", "scode": "scode"}
        order = branch_list_order_sql(cols, exact)
        self.assertEqual(order, "oname, gname")
        self.assertNotIn("Oname", order)


class CustomerBranchServiceTest(IsolatedAsyncioTestCase):
    async def test_create_customer_branch_allocates_id(self) -> None:
        from app.services import masters_service
        from app.services.h2_gbun_adapt import clear_h2_column_cache_for_tests

        clear_h2_column_cache_for_tests()
        queries: list[tuple[str, tuple]] = []
        txs: list[list[tuple[str, tuple]]] = []

        async def fake_query(_server_id, sql, params=None):
            queries.append((sql, tuple(params or ())))
            if "SHOW COLUMNS" in sql:
                return [
                    {"Field": "ID"},
                    {"Field": "Hcode"},
                    {"Field": "Scode"},
                    {"Field": "Gcode"},
                    {"Field": "Gname"},
                    {"Field": "Jubun"},
                ]
            if "MAX(ID)" in sql:
                return [{"nid": 5}]
            return []

        async def fake_tx(_server_id, statements):
            txs.append(statements)
            return [1]

        old_q = masters_service.execute_query
        old_tx = masters_service.execute_in_transaction
        old_meta = masters_service.h2_gbun_column_meta
        masters_service.execute_query = fake_query
        masters_service.execute_in_transaction = fake_tx

        async def fake_meta(_server_id):
            return (
                {"id", "hcode", "scode", "gcode", "gname", "jubun"},
                {
                    "id": "ID",
                    "hcode": "Hcode",
                    "scode": "Scode",
                    "gcode": "Gcode",
                    "gname": "Gname",
                    "jubun": "Jubun",
                },
            )

        masters_service.h2_gbun_column_meta = fake_meta
        try:
            res = await masters_service.create_customer_branch(
                server_id="remote_138",
                gcode="C001",
                payload={"gname": "강남", "jubun": "J1"},
            )
        finally:
            masters_service.execute_query = old_q
            masters_service.execute_in_transaction = old_tx
            masters_service.h2_gbun_column_meta = old_meta
            clear_h2_column_cache_for_tests()

        self.assertEqual(res["id"], 5)
        self.assertIn("INSERT INTO H2_Gbun", txs[0][0][0])
        self.assertIn("X", txs[0][0][1])

    async def test_list_customer_branches_maps_gjisa_value(self) -> None:
        from app.services import masters_service

        async def fake_query(_server_id, sql, params=None):
            if "COUNT" in sql:
                return [{"row_count": 1}]
            return [
                {
                    "id": 1,
                    "gname": "강남",
                    "jubun": "J1",
                    "oname": "",
                    "gdate": "",
                    "gnum1": "",
                    "gbigo": "",
                    "hcode": "",
                    "scode": "X",
                    "gcode": "C001",
                }
            ]

        async def fake_meta(_server_id):
            return (
                {"id", "gname", "jubun", "oname", "gdate", "gnum1", "gbigo", "hcode", "scode", "gcode"},
                {
                    "id": "ID",
                    "gname": "Gname",
                    "jubun": "Jubun",
                    "oname": "Oname",
                    "gdate": "Gdate",
                    "gnum1": "Gnum1",
                    "gbigo": "Gbigo",
                    "hcode": "Hcode",
                    "scode": "Scode",
                    "gcode": "Gcode",
                },
            )

        old_q = masters_service.execute_query
        masters_service.execute_query = fake_query
        masters_service.h2_gbun_column_meta = fake_meta
        try:
            res = await masters_service.list_customer_branches(
                server_id="remote_138",
                gcode="C001",
            )
        finally:
            masters_service.execute_query = old_q

        self.assertEqual(res["items"][0]["gjisa_value"], "J1|강남")
        self.assertEqual(res["items"][0]["label"], "J1|강남")

    async def test_list_customer_branches_uses_gcode_in(self) -> None:
        from app.services import masters_service

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "COUNT" in sql:
                return [{"row_count": 0}]
            return []

        async def fake_meta(_server_id):
            return (
                {"id", "gname", "jubun", "oname", "gdate", "gnum1", "gbigo", "hcode", "scode", "gcode"},
                {
                    "id": "id",
                    "gname": "gname",
                    "jubun": "jubun",
                    "oname": "oname",
                    "gdate": "gdate",
                    "gnum1": "gnum1",
                    "gbigo": "gbigo",
                    "hcode": "hcode",
                    "scode": "scode",
                    "gcode": "gcode",
                },
            )

        old_q = masters_service.execute_query
        masters_service.execute_query = fake_query
        masters_service.h2_gbun_column_meta = fake_meta
        try:
            await masters_service.list_customer_branches(
                server_id="remote_138",
                gcode="00001",
            )
        finally:
            masters_service.execute_query = old_q

        list_sql = next(s for s, _ in captured if "FROM H2_Gbun h" in s and "COUNT" not in s)
        self.assertIn("Gcode IN", list_sql)
        self.assertIn("ORDER BY oname, gname", list_sql)
        self.assertIn("IFNULL(h.", list_sql)
        list_params = next(p for s, p in captured if "FROM H2_Gbun" in s and "COUNT" not in s)
        self.assertIn("00001", list_params)
        self.assertIn("1", list_params)

