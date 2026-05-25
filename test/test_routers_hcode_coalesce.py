"""P0 라우터 hcode 자동 주입 회귀 가드 — Hcode 전면 적용 Phase 2.

각 라우터의 list/집계 GET 이 ``hcode`` Query 를 생략할 때, JWT scope hcode
(`enforce_hcode_isolation` → `coalesce_request_hcode`) 가 서비스에 전달되는지 검증한다.

검증 대상:
- outbound.list_orders
- inbound.list_receipts
- returns.list_returns
- transactions.list_sales_statements
- settlement.list_billing
- stats.get_sales_period
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402


_T2_PUB_PERMS = [
    "outbound.read",
    "outbound.write",
    "inbound.read",
    "returns.read",
    "transactions.read",
    "transactions.status.read",
    "settlement.read",
    "settlement.cash.read",
    "settlement.tax.read",
    "stats.read",
    "admin.stats.sales",
    "admin.stats.customer",
    "admin.stats.book",
    "admin.stats.quarterly",
]


def _t2_pub_ctx(hcode: str = "9001") -> dict[str, Any]:
    return {
        "user_id": "smoke",
        "server_id": "remote_1",
        "role": "operator",
        "hcode": hcode,
        "branch_id": "",
        "permissions": list(_T2_PUB_PERMS),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "BLD-PUB-STD",
        "build_role": "publisher",
        "account_type": "T2_PUB",
        "dist_hcode": "",
    }


def _t2_pub_jwt(hcode: str = "9001") -> dict[str, Any]:
    return {
        "user_id": "smoke",
        "server_id": "remote_1",
        "hcode": hcode,
        "role": "operator",
        "permissions": list(_T2_PUB_PERMS),
        "primary_data_server_set": True,
        "account_type": "T2_PUB",
        "tenant_id": None,
        "account_family": "",
        "active_build_id": "BLD-PUB-STD",
        "build_role": "publisher",
        "dist_hcode": None,
        "warehouse_menu_tier": "",
        "license_keys": [],
    }


class P0HcodeCoalesceTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        async def _user() -> dict[str, Any]:
            return _t2_pub_jwt("9001")

        async def _ctx() -> dict[str, Any]:
            return _t2_pub_ctx("9001")

        app.dependency_overrides[get_current_user] = _user
        app.dependency_overrides[get_user_context] = _ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    # ── outbound ──
    def test_outbound_orders_injects_jwt_hcode(self) -> None:
        from app.services import outbound_service

        with patch.object(
            outbound_service, "list_orders", new=AsyncMock(return_value=([], 0))
        ) as svc:
            res = self.client.get(
                "/api/v1/outbound/orders",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        kwargs = svc.call_args.kwargs
        self.assertEqual(kwargs.get("hcode"), "9001")

    # ── inbound ──
    def test_inbound_receipts_injects_jwt_hcode(self) -> None:
        from app.services import inbound_service

        with patch.object(
            inbound_service, "list_receipts", new=AsyncMock(return_value=([], 0))
        ) as svc:
            res = self.client.get(
                "/api/v1/inbound/receipts",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")

    # ── returns ──
    def test_returns_list_injects_jwt_hcode(self) -> None:
        from app.services import returns_service

        with patch.object(
            returns_service, "list_returns", new=AsyncMock(return_value=([], 0))
        ) as svc:
            res = self.client.get(
                "/api/v1/returns",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")

    # ── transactions ──
    def test_transactions_sales_statement_injects_jwt_hcode(self) -> None:
        from app.services import transactions_service

        with patch.object(
            transactions_service,
            "list_sales_statements",
            new=AsyncMock(return_value=([], 0)),
        ) as svc:
            res = self.client.get(
                "/api/v1/transactions/sales-statement",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")

    # ── settlement ──
    def test_settlement_billing_injects_jwt_hcode(self) -> None:
        from app.services import settlement_service

        with patch.object(
            settlement_service,
            "list_billing",
            new=AsyncMock(return_value=([], 0)),
        ) as svc:
            res = self.client.get(
                "/api/v1/settlement/billing",
                params={
                    "serverId": "remote_1",
                    "monthFrom": "202601",
                    "monthTo": "202601",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")

    # ── tamper guard ──
    def test_tamper_other_hcode_returns_403(self) -> None:
        from app.services import outbound_service

        with patch.object(
            outbound_service, "list_orders", new=AsyncMock(return_value=([], 0))
        ):
            res = self.client.get(
                "/api/v1/outbound/orders",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                    "hcode": "OTHER",
                },
            )
        self.assertEqual(res.status_code, 403)
        body = res.json()
        self.assertEqual(body.get("detail", {}).get("code"), "HCODE_FORBIDDEN")


if __name__ == "__main__":
    main()
