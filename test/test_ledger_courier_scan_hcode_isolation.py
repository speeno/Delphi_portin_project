"""ACC-DATA-03 갭 클로즈 — ledger / courier / scan 라우터 hcode tamper 가드.

기존 ``enforce`` 누락 우회 경로(식별자/범위/패턴/body hcode)가 격리 계정에서
타사 hcode 를 명시하면 403, 본인/빈 값이면 JWT scope 로 강제되는지 검증한다.

검증 대상
---------
- ledger.get_customer_ledger          : customerCode → Hcode
- ledger.get_integrated_customer_ledger : customerPattern → Hcode LIKE
- ledger.list_publisher_settings      : G7_Ggeo.Gcode scope
- courier.list_courier_lines          : hcodeFrom~hcodeTo 구간
- courier.get_courier_memo            : hcode 단건
- scan.scan_match                     : body hcode
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
        "permissions": ["ledger.read", "transactions.read", "scan.read"],
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "BLD-PUB-STD",
        "build_role": "publisher",
        "account_type": "T2_PUB",
        "dist_hcode": "",
    }


def _t2_dist_ctx(hcode: str = "1001") -> dict[str, Any]:
    ctx = _t2_pub_ctx(hcode)
    ctx["account_type"] = "T2_DIST"
    ctx["account_family"] = "kbt"
    return ctx


class _BaseRouterTest(IsolatedAsyncioTestCase):
    CTX = staticmethod(_t2_pub_ctx)

    def setUp(self) -> None:
        ctx = self.CTX("9001")

        async def _user() -> dict[str, Any]:
            return ctx

        async def _ctx() -> dict[str, Any]:
            return ctx

        app.dependency_overrides[get_current_user] = _user
        app.dependency_overrides[get_user_context] = _ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()


class LedgerHcodeIsolationTests(_BaseRouterTest):
    def test_customer_ledger_own_code_passes(self) -> None:
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "get_customer_ledger",
            new=AsyncMock(
                return_value={"rows": [], "summary": {}, "page": {}, "truncated": False}
            ),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/customer",
                params={
                    "serverId": "remote_1",
                    "customerCode": "9001",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("customer_code"), "9001")

    def test_customer_ledger_other_code_scoped_not_403(self) -> None:
        """DEC-137 축 교정 — customerCode 는 거래처(Gcode) 선택값이라 403 대상이
        아니다(교문사-경리부 HCODE_FORBIDDEN 사고의 원인). 격리는 출판사 축:
        publisher_scope_hcode 에 자사 hcode 가 강제로 실려야 한다."""
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "get_customer_ledger",
            new=AsyncMock(
                return_value={"rows": [], "summary": {}, "page": {}, "truncated": False}
            ),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/customer",
                params={
                    "serverId": "remote_1",
                    "customerCode": "OTHER",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("customer_code"), "OTHER")
        self.assertEqual(svc.call_args.kwargs.get("publisher_scope_hcode"), "9001")

    def test_integrated_other_pattern_scoped_not_403(self) -> None:
        """DEC-137 — customerPattern 은 거래처(Gcode) LIKE. 격리 계정은 Hcode=자사
        스코프가 항상 동반되므로 패턴 자체는 자유(타사 노출 없음)."""
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "get_integrated_customer_ledger",
            new=AsyncMock(return_value={"rows": [], "page": {}}),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/customer-integrated",
                params={
                    "serverId": "remote_1",
                    "customerPattern": "00",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("customer_pattern"), "00")
        self.assertEqual(svc.call_args.kwargs.get("scope_hcode"), "9001")

    def test_integrated_empty_pattern_binds_scope(self) -> None:
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "get_integrated_customer_ledger",
            new=AsyncMock(return_value={"rows": [], "page": {}}),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/customer-integrated",
                params={
                    "serverId": "remote_1",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("scope_hcode"), "9001")

    def test_publisher_settings_binds_scope(self) -> None:
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "list_publisher_settings",
            new=AsyncMock(return_value={"items": [], "page": {}}),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/comparison",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("scope_hcode"), "9001")


class LedgerDistScopedTests(_BaseRouterTest):
    CTX = staticmethod(_t2_dist_ctx)

    def test_publisher_settings_dist_binds_scope(self) -> None:
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "list_publisher_settings",
            new=AsyncMock(return_value={"items": [], "page": {}}),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/comparison",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("scope_hcode"), "9001")

    def test_integrated_dist_pattern_global_scope(self) -> None:
        """DEC-137 — 단일 테넌트 좌표의 총판(T2_DIST)은 출판사 스코프 None(전체,
        레거시 총판 Subu31 정본). 거래처 패턴은 그대로 전달된다."""
        from app.services import customer_ledger_service

        with patch.object(
            customer_ledger_service,
            "get_integrated_customer_ledger",
            new=AsyncMock(return_value={"rows": [], "page": {}}),
        ) as svc:
            res = self.client.get(
                "/api/v1/ledger/customer-integrated",
                params={
                    "serverId": "remote_1",
                    "customerPattern": "00",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("customer_pattern"), "00")
        self.assertIsNone(svc.call_args.kwargs.get("scope_hcode"))


class CourierHcodeIsolationTests(_BaseRouterTest):
    def test_lines_empty_range_forces_scope(self) -> None:
        from app.services import courier_service

        with patch.object(
            courier_service,
            "list_courier_lines",
            new=AsyncMock(return_value=([], 0)),
        ) as svc:
            res = self.client.get(
                "/api/v1/shipping/courier/lines",
                params={"serverId": "remote_1", "gdate": "2026.01.01"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode_from"), "9001")
        self.assertEqual(svc.call_args.kwargs.get("hcode_to"), "9001")

    def test_lines_other_range_returns_403(self) -> None:
        from app.services import courier_service

        with patch.object(
            courier_service,
            "list_courier_lines",
            new=AsyncMock(return_value=([], 0)),
        ):
            res = self.client.get(
                "/api/v1/shipping/courier/lines",
                params={
                    "serverId": "remote_1",
                    "gdate": "2026.01.01",
                    "hcodeFrom": "0001",
                    "hcodeTo": "ZZZZ",
                },
            )
        self.assertEqual(res.status_code, 403)

    def test_memo_other_hcode_returns_403(self) -> None:
        from app.services import courier_service

        with patch.object(
            courier_service,
            "get_courier_memo",
            new=AsyncMock(return_value={}),
        ):
            res = self.client.get(
                "/api/v1/shipping/courier/memo",
                params={
                    "serverId": "remote_1",
                    "gdate": "2026.01.01",
                    "hcode": "OTHER",
                    "gcode": "G1",
                },
            )
        self.assertEqual(res.status_code, 403)

    def test_memo_own_hcode_passes(self) -> None:
        from app.services import courier_service

        with patch.object(
            courier_service,
            "get_courier_memo",
            new=AsyncMock(return_value={}),
        ) as svc:
            res = self.client.get(
                "/api/v1/shipping/courier/memo",
                params={
                    "serverId": "remote_1",
                    "gdate": "2026.01.01",
                    "hcode": "9001",
                    "gcode": "G1",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")


class ScanHcodeIsolationTests(_BaseRouterTest):
    def test_match_other_hcode_returns_403(self) -> None:
        from app.services import scan_match_service

        with patch.object(
            scan_match_service,
            "match_barcode",
            new=AsyncMock(
                return_value={
                    "status": "nodata",
                    "resolved": None,
                    "barcode": "9788900000000",
                    "hcode": "9001",
                    "context": "outbound",
                }
            ),
        ):
            res = self.client.post(
                "/api/v1/scan/match",
                json={
                    "barcode": "9788900000000",
                    "hcode": "OTHER",
                    "context": "outbound",
                    "server_id": "remote_1",
                },
            )
        self.assertEqual(res.status_code, 403)

    def test_match_own_hcode_passes(self) -> None:
        from app.services import scan_match_service

        with patch.object(
            scan_match_service,
            "match_barcode",
            new=AsyncMock(
                return_value={
                    "status": "nodata",
                    "resolved": None,
                    "barcode": "9788900000000",
                    "hcode": "9001",
                    "context": "outbound",
                }
            ),
        ) as svc:
            res = self.client.post(
                "/api/v1/scan/match",
                json={
                    "barcode": "9788900000000",
                    "hcode": "9001",
                    "context": "outbound",
                    "server_id": "remote_1",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(svc.call_args.kwargs.get("hcode"), "9001")


if __name__ == "__main__":
    main()
