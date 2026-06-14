"""합성키 상세/출력 GET — path 내 hcode tamper 가드 회귀.

비슈퍼 계정이 order_key / receipt_key / return_key / billing_key 에
타사 hcode 를 넣으면 403, 본인 hcode 면 서비스 호출까지 통과하는지 검증한다.
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


def _t2_pub_ctx(hcode: str = "9001") -> dict[str, Any]:
    return {
        "user_id": "smoke",
        "server_id": "remote_1",
        "role": "operator",
        "hcode": hcode,
        "branch_id": "",
        "permissions": [
            "outbound.read",
            "inbound.read",
            "returns.read",
            "transactions.read",
            "settlement.read",
        ],
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "BLD-PUB-STD",
        "build_role": "publisher",
        "account_type": "T2_PUB",
        "dist_hcode": "",
    }


class DetailGetHcodeIdentityTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ctx = _t2_pub_ctx("9001")

        async def _user() -> dict[str, Any]:
            return ctx

        async def _ctx() -> dict[str, Any]:
            return ctx

        app.dependency_overrides[get_current_user] = _user
        app.dependency_overrides[get_user_context] = _ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_outbound_order_detail_other_hcode_returns_403(self) -> None:
        from app.services import outbound_service

        with patch.object(
            outbound_service,
            "get_order_detail",
            new=AsyncMock(return_value=None),
        ):
            res = self.client.get(
                "/api/v1/outbound/orders/2026.01.01|OTHER|",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 403)

    def test_outbound_order_detail_own_hcode_passes(self) -> None:
        from app.services import outbound_service

        with patch.object(
            outbound_service,
            "get_order_detail",
            new=AsyncMock(return_value=None),
        ) as svc:
            res = self.client.get(
                "/api/v1/outbound/orders/2026.01.01|9001|",
                params={"serverId": "remote_1"},
            )
        self.assertNotEqual(res.status_code, 403)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")

    def test_inbound_receipt_detail_other_hcode_returns_403(self) -> None:
        from app.services import inbound_service

        with patch.object(
            inbound_service,
            "get_receipt_detail",
            new=AsyncMock(return_value=None),
        ):
            res = self.client.get(
                "/api/v1/inbound/receipts/2026.01.01|OTHER|V01|",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 403)

    def test_returns_detail_other_hcode_returns_403(self) -> None:
        from app.services import returns_service

        with patch.object(
            returns_service,
            "get_return_detail",
            new=AsyncMock(return_value={"lines": []}),
        ):
            res = self.client.get(
                "/api/v1/returns/G|2026.01.01|OTHER|",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 403)

    def test_sales_statement_detail_other_hcode_returns_403(self) -> None:
        from app.services import transactions_service

        with patch.object(
            transactions_service,
            "get_sales_statement_detail",
            new=AsyncMock(return_value=None),
        ):
            res = self.client.get(
                "/api/v1/transactions/sales-statement/2026.01.01|OTHER|11||0||",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 403)

    def test_billing_detail_other_hcode_returns_403(self) -> None:
        from app.services import settlement_service

        with patch.object(
            settlement_service,
            "get_billing_detail",
            new=AsyncMock(return_value={"lines": []}),
        ):
            res = self.client.get(
                "/api/v1/settlement/billing/202601|OTHER",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 403)


if __name__ == "__main__":
    main()
