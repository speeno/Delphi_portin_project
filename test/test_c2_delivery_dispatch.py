from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402


def _ctx() -> dict[str, Any]:
    return {
        "user_id": "tester",
        "server_id": "remote_1",
        "role": "admin",
        "hcode": "0000",
        "permissions": ["*"],
        "tenant_id": "",
        "account_type": "T1",
    }


class DeliveryDispatchRouterTest(TestCase):
    def setUp(self) -> None:
        async def _user() -> dict[str, Any]:
            return _ctx()

        async def _user_ctx() -> dict[str, Any]:
            return _ctx()

        app.dependency_overrides[get_current_user] = _user
        app.dependency_overrides[get_user_context] = _user_ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_list_filters(self) -> None:
        rows = [
            {
                "dispatch_id": "A",
                "gdate": "2026.06.01",
                "hcode": "H1",
                "gcode": "G1",
                "jubun": "J1",
                "gjisa": "",
                "gname": "거래처1",
                "gtel1": "",
                "gtel2": "",
                "hname": "출판사1",
                "sum_gsqut": 1,
                "sum_gssum": 1000,
                "carrier": "hanjin",
                "tracking_no": "T1",
                "status": "mapped",
                "source": "manual",
                "last_updated": None,
                "last_checked": None,
                "status_message": None,
            },
            {
                "dispatch_id": "B",
                "gdate": "2026.06.01",
                "hcode": "H2",
                "gcode": "G2",
                "jubun": "J2",
                "gjisa": "",
                "gname": "거래처2",
                "gtel1": "",
                "gtel2": "",
                "hname": "출판사2",
                "sum_gsqut": 2,
                "sum_gssum": 2000,
                "carrier": "manual",
                "tracking_no": None,
                "status": "pending",
                "source": "manual",
                "last_updated": None,
                "last_checked": None,
                "status_message": None,
            },
        ]
        with patch(
            "app.routers.delivery_dispatch.delivery_dispatch_service.list_dispatch",
            return_value=(rows, 2),
        ), patch(
            "app.routers.delivery_dispatch.delivery_dispatch_service.integration_state",
            return_value=(False, "manual"),
        ):
            res = self.client.get(
                "/api/v1/delivery/dispatch",
                params={
                    "serverId": "remote_1",
                    "ship_date": "2026.06.01",
                    "carrier": "hanjin",
                    "status": "mapped",
                    "limit": 10,
                    "offset": 0,
                },
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["total"], 2)
        self.assertEqual(len(body["items"]), 1)
        self.assertEqual(body["items"][0]["dispatch_id"], "A")
        self.assertFalse(body["integration_enabled"])

    def test_put_tracking(self) -> None:
        with patch(
            "app.routers.delivery_dispatch.delivery_dispatch_service.upsert_tracking",
            return_value={
                "dispatch_id": "A",
                "tracking_no": "1111",
                "carrier": "hanjin",
                "status": "mapped",
                "source": "manual",
                "updated_at": "2026-06-01T00:00:00+00:00",
            },
        ):
            res = self.client.put(
                "/api/v1/delivery/dispatch/A/tracking",
                params={"serverId": "remote_1"},
                json={"tracking_no": "1111", "carrier": "hanjin"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "mapped")

    def test_refresh_fallback_manual(self) -> None:
        with patch(
            "app.routers.delivery_dispatch.delivery_dispatch_service.refresh_dispatch",
            return_value={
                "dispatch_id": "A",
                "status": "mapped",
                "source": "manual",
                "last_updated": "2026-06-01T00:00:00+00:00",
                "last_checked": "2026-06-01T00:00:00+00:00",
                "status_message": None,
                "fallback_reason": "manual_or_no_tracking",
            },
        ):
            res = self.client.post(
                "/api/v1/delivery/dispatch/A/refresh",
                params={"serverId": "remote_1"},
                json={},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["source"], "manual")
