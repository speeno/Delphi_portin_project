"""Sobo48/Sobo29 phase1 승격 회귀 가드."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import customer_ledger_service, transactions_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


class Sobo48PublisherSettingsRouterTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_publisher_settings_route(self) -> None:
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {
                "items": [{"gcode": "P001", "gname": "출판사", "chek3": "Y", "yesno": "N"}],
                "page": {"limit": 50, "offset": 0, "total": 1, "has_more": False},
            }

        with patch.object(customer_ledger_service, "list_publisher_settings", side_effect=fake):
            res = self.client.get("/api/v1/ledger/comparison?serverId=remote_1&keyword=P&limit=50")
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["keyword"], "P")
        self.assertEqual(res.json()["items"][0]["gcode"], "P001")

    def test_patch_publisher_setting_route(self) -> None:
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {"gcode": kwargs["gcode"], "updated": 1}

        with patch.object(customer_ledger_service, "update_publisher_setting", side_effect=fake):
            res = self.client.patch(
                "/api/v1/ledger/comparison/P001?serverId=remote_1",
                json={"chek3": "Y", "yesno": "N"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["gcode"], "P001")
        self.assertEqual(captured["chek3"], "Y")
        self.assertEqual(captured["yesno"], "N")


class Sobo29OtherStatementRouterTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_other_statements_route(self) -> None:
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {
                "items": [{"gdate": "2026.04.01", "hcode": "H001", "bcode": "B001", "jubun": "신간"}],
                "page": {"limit": 25, "offset": 0, "total": 1, "has_more": False},
            }

        with patch.object(transactions_service, "list_other_statements", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/other?serverId=remote_1"
                "&dateFrom=2026-04-01&dateTo=2026-04-30&hcode=H001&jubun=신간&limit=25"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["hcode"], "H001")
        self.assertEqual(captured["jubun"], "신간")
        self.assertEqual(res.json()["page"]["total"], 1)

    def test_upsert_other_memo_route(self) -> None:
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {
                "key": {"gdate": kwargs["gdate"], "hcode": kwargs["hcode"], "jubun": kwargs["jubun"], "gjisa": ""},
                "action": "updated",
                "updated_at": "2026-05-01T00:00:00+00:00",
            }

        with patch.object(transactions_service, "upsert_other_statement_memo", side_effect=fake):
            res = self.client.patch(
                "/api/v1/transactions/other/memo",
                json={
                    "serverId": "remote_1",
                    "gdate": "2026-04-01",
                    "hcode": "H001",
                    "jubun": "신간",
                    "gbigo": "메모",
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["server_id"], "remote_1")
        self.assertEqual(captured["gbigo"], "메모")


if __name__ == "__main__":
    main(verbosity=2)
