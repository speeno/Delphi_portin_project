"""거래명세서 조회 가드 — Grat9 / H2_Gbun.Gbigo (Subu21 L467–489)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))


class SalesStatementShippingStopTest(IsolatedAsyncioTestCase):
    async def test_customer_shipping_stop_raises(self) -> None:
        from app.services.h2_branch_lookup import assert_sales_statement_search_allowed

        async def fake_query(_server_id, sql, params=None):
            if "grat9" in sql.lower():
                return [{"grat9": "1"}]
            return []

        async def fake_meta(_server_id):
            return ({"grat9"}, {"grat9": "Grat9"})

        with patch(
            "app.services.h2_branch_lookup.execute_query",
            new=fake_query,
        ), patch(
            "app.services.h2_branch_lookup.g1_geo_column_meta",
            new=fake_meta,
        ):
            with self.assertRaises(ValueError) as ctx:
                await assert_sales_statement_search_allowed(
                    server_id="remote_138",
                    gcode="C001",
                    gjisa=None,
                )
            self.assertEqual(str(ctx.exception), "CUSTOMER_SHIPPING_STOP")

    async def test_branch_shipping_stop_raises(self) -> None:
        from app.services.h2_branch_lookup import assert_sales_statement_search_allowed

        async def fake_query(_server_id, sql, params=None):
            if "H2_Gbun" in sql:
                return [{"gbigo": "정지 테스트"}]
            return []

        async def fake_meta(_server_id):
            return (set(), {})

        with patch(
            "app.services.h2_branch_lookup.execute_query",
            new=fake_query,
        ), patch(
            "app.services.h2_branch_lookup.g1_geo_column_meta",
            new=fake_meta,
        ):
            with self.assertRaises(ValueError) as ctx:
                await assert_sales_statement_search_allowed(
                    server_id="remote_138",
                    gcode="C001",
                    gjisa="J1|강남",
                )
            self.assertTrue(str(ctx.exception).startswith("BRANCH_SHIPPING_STOP:"))
