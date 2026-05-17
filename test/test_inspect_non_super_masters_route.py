"""
비수퍼 + 점검 Authorization-Context 가 GET /api/v1/masters/customer 를 403으로 막지 않는지 회귀.

실 DB 없이 get_current_user override + list_customer_master monkeypatch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402


def _non_super_user() -> dict:
    return {
        "user_id": "dist01",
        "server_id": "remote_138",
        "role": "operator",
        "hcode": "1001",
        "permissions": ["master.read"],
        "tenant_id": "t1",
        "account_type": "T2_DIST",
        "build_role": "",
        "warehouse_menu_tier": "",
    }


class InspectNonSuperMastersRouteTests(TestCase):
    def tearDown(self) -> None:
        app.dependency_overrides.pop(get_current_user, None)

    def test_masters_customer_get_not_403_with_stale_inspect_header(self) -> None:
        app.dependency_overrides[get_current_user] = lambda: _non_super_user()
        fake = AsyncMock(
            return_value={
                "items": [],
                "page": {"limit": 20, "offset": 0, "total": 0, "has_more": False},
            }
        )
        inspect_hdr = json.dumps(
            {
                "inspect_mode": True,
                "inspect_server_id": "remote_153",
                "inspect_db_name": "chul_05_db",
                "inspect_reason": "stale",
            }
        )
        with patch("app.routers.masters.masters_service.list_customer_master", fake):
            client = TestClient(app)
            res = client.get(
                "/api/v1/masters/customer",
                params={"serverId": "remote_138", "limit": 20, "offset": 0},
                headers={
                    "Authorization": "Bearer test-token",
                    "Authorization-Context": inspect_hdr,
                },
            )
        self.assertNotEqual(res.status_code, 403, msg=res.text)
        self.assertEqual(res.status_code, 200, msg=res.text)
        body = res.json()
        self.assertEqual(body.get("items"), [])
        fake.assert_awaited()

    def test_masters_customer_get_super_with_inspect_still_ok(self) -> None:
        app.dependency_overrides[get_current_user] = lambda: {
            "user_id": "admin",
            "server_id": "remote_138",
            "role": "admin",
            "hcode": "0000",
            "permissions": ["*"],
            "tenant_id": "",
            "account_type": "",
            "build_role": "",
            "warehouse_menu_tier": "",
        }
        fake = AsyncMock(
            return_value={
                "items": [],
                "page": {"limit": 20, "offset": 0, "total": 0, "has_more": False},
            }
        )
        inspect_hdr = json.dumps(
            {
                "inspect_mode": True,
                "inspect_server_id": "remote_153",
                "inspect_db_name": "chul_05_db",
                "inspect_reason": "점검",
            }
        )
        with patch("app.routers.masters.masters_service.list_customer_master", fake):
            client = TestClient(app)
            res = client.get(
                "/api/v1/masters/customer",
                params={"serverId": "remote_153", "limit": 20, "offset": 0},
                headers={
                    "Authorization": "Bearer test-token",
                    "Authorization-Context": inspect_hdr,
                },
            )
        self.assertEqual(res.status_code, 200, msg=res.text)
        fake.assert_awaited()


if __name__ == "__main__":
    main(verbosity=2)
