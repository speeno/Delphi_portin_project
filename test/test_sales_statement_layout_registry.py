"""거래명세서 layout 레지스트리."""
from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.routers.auth import get_current_user
from app.services import sales_statement_layout_registry as reg


def _override_user() -> dict:
    return {"user_id": "u1", "server_id": "remote_test"}


class SalesStatementLayoutRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_user

    def tearDown(self) -> None:
        app.dependency_overrides.pop(get_current_user, None)

    def test_normalize_known(self) -> None:
        self.assertEqual(reg.normalize_sales_statement_layout("DEFAULT"), "default")
        self.assertEqual(
            reg.normalize_sales_statement_layout("legacy_triplicate"),
            "legacy_triplicate",
        )

    def test_normalize_unknown(self) -> None:
        self.assertIsNone(reg.normalize_sales_statement_layout("bogus"))

    def test_list_entries_include_ids(self) -> None:
        ids = {e["id"] for e in reg.list_layout_entries()}
        self.assertEqual(ids, {"default", "legacy_triplicate"})

    def test_layouts_endpoint_not_captured_by_pdf_route(self) -> None:
        client = TestClient(app)
        res = client.get(
            "/api/v1/print/sales-statement/layouts",
            params={"serverId": "remote_test"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(
            {row["id"] for row in body["layouts"]},
            {"default", "legacy_triplicate"},
        )


if __name__ == "__main__":
    unittest.main()
