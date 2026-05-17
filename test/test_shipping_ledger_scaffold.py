"""발송비 scaffold API — GET shipping-ledger / shipping-status (W2)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402

_SID = "remote_138"


def _user() -> dict:
    return {
        "user_id": "ship_test",
        "server_id": _SID,
        "role": "operator",
        "hcode": "H0001",
        "permissions": ["settlement.report.read"],
    }


async def _override_user() -> dict:
    return _user()


async def _override_ctx() -> dict:
    u = _user()
    return {
        "user_id": u["user_id"],
        "server_id": u["server_id"],
        "role": u["role"],
        "hcode": u["hcode"],
        "branch_id": u["hcode"],
        "permissions": list(u["permissions"]),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "",
        "dist_hcode": "",
    }


class ShippingLedgerScaffoldTests(TestCase):
    def setUp(self) -> None:
        self._prev_user = app.dependency_overrides.get(get_current_user)
        self._prev_ctx = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _override_user
        app.dependency_overrides[get_user_context] = _override_ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev_user is not None:
            app.dependency_overrides[get_current_user] = self._prev_user
        else:
            app.dependency_overrides.pop(get_current_user, None)
        if self._prev_ctx is not None:
            app.dependency_overrides[get_user_context] = self._prev_ctx
        else:
            app.dependency_overrides.pop(get_user_context, None)

    def test_shipping_ledger_scaffold(self) -> None:
        r = self.client.get(
            f"/api/v1/settlement/shipping-ledger?serverId={_SID}&limit=10&offset=0",
        )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body.get("scaffold"), True)
        self.assertIn("items", body)
        self.assertIn("page", body)
        self.assertEqual(body["items"], [])

    def test_shipping_status_scaffold(self) -> None:
        r = self.client.get(
            f"/api/v1/settlement/shipping-status?serverId={_SID}&limit=10&offset=0",
        )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body.get("scaffold"), True)
        self.assertIn("rows", body)
        self.assertEqual(body["rows"], [])


if __name__ == "__main__":
    main()
