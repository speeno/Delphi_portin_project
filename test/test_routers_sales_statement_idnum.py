"""DEC-064 §Idnum 정합 라우터 회귀 — list/detail/customer-preview 가 idnum 을 통과시키는지."""

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


def _ctx() -> dict[str, Any]:
    return {
        "user_id": "smoke",
        "server_id": "remote_153",
        "role": "operator",
        "hcode": "5019",
        "branch_id": "",
        "permissions": ["transactions.read"],
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "T2_PUB",
        "dist_hcode": "",
    }


def _jwt() -> dict[str, Any]:
    return {
        "user_id": "smoke",
        "server_id": "remote_153",
        "hcode": "5019",
        "role": "operator",
        "permissions": ["transactions.read"],
        "primary_data_server_set": True,
        "account_type": "T2_PUB",
        "tenant_id": None,
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "dist_hcode": None,
        "warehouse_menu_tier": "",
        "license_keys": [],
    }


class IdnumRouterTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        async def _user() -> dict[str, Any]:
            return _jwt()

        async def _c() -> dict[str, Any]:
            return _ctx()

        app.dependency_overrides[get_current_user] = _user
        app.dependency_overrides[get_user_context] = _c
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_list_passes_idnum_query_to_service(self) -> None:
        """LIST GET ``idnum`` 쿼리는 서비스 ``idnum`` kwarg 로 전달된다."""
        from app.services import transactions_service

        with patch.object(
            transactions_service,
            "list_sales_statements",
            new=AsyncMock(return_value=([], 0)),
        ) as svc:
            res = self.client.get(
                "/api/v1/transactions/sales-statement",
                params={
                    "serverId": "remote_153",
                    "dateFrom": "2026.05.14",
                    "dateTo": "2026.05.14",
                    "idnum": "00001",
                },
            )
        self.assertEqual(res.status_code, 200)
        kwargs = svc.call_args.kwargs
        self.assertEqual(kwargs.get("idnum"), "00001")

    def test_customer_preview_accepts_idnum_query(self) -> None:
        from app.services import transactions_service

        with patch.object(
            transactions_service,
            "get_sales_statement_customer_preview",
            new=AsyncMock(
                return_value={
                    "gcode": "00004",
                    "customer_profile": {},
                    "stock_qty": None,
                    "memo_preview": {},
                }
            ),
        ) as svc:
            res = self.client.get(
                "/api/v1/transactions/sales-statement/customer-preview",
                params={
                    "serverId": "remote_153",
                    "gcode": "00004",
                    "dateFrom": "2026.05.14",
                    "dateTo": "2026.05.14",
                    "idnum": "00001",
                },
            )
        self.assertEqual(res.status_code, 200)
        kwargs = svc.call_args.kwargs
        self.assertEqual(kwargs.get("idnum"), "00001")

    def test_detail_path_accepts_7_segment_extended_key(self) -> None:
        from app.services import transactions_service

        async def fake_detail(**kwargs: Any) -> dict[str, Any]:
            return {
                "order_key": {
                    "gdate": kwargs["gdate"],
                    "hcode": kwargs["hcode"],
                    "jubun": kwargs["jubun"],
                    "gjisa": kwargs.get("gjisa") or "",
                    "idnum": int(kwargs.get("idnum") or 0),
                    "gubun": str(kwargs.get("gubun") or ""),
                    "gcode": str(kwargs.get("gcode") or ""),
                },
                "customer": {
                    "hcode": kwargs["hcode"],
                    "gname": "테스트",
                    "gcode": "00004",
                },
                "gubun": "출고",
                "slip_no": "00001",
                "customer_profile": {},
                "stock_qty": 10,
                "status": "active",
                "lines": [
                    {
                        "gcode": "00004",
                        "bcode": "BK99",
                        "product_name": "도서",
                        "shelf": "",
                        "pubun": "",
                        "gsqut": 1,
                        "gssum": 1000,
                        "gbigo": "",
                        "gdang": 1000,
                        "grat1": 0,
                        "yesno": "1",
                    }
                ],
                "memo": {},
            }

        with patch.object(
            transactions_service,
            "get_sales_statement_detail",
            new=AsyncMock(side_effect=fake_detail),
        ) as svc:
            from urllib.parse import quote

            key = "|".join(
                [
                    quote("2026.05.14"),
                    quote("5019"),
                    quote("11"),
                    quote(""),
                    quote("1"),
                    quote("출고"),
                    quote("00004"),
                ]
            )
            res = self.client.get(
                f"/api/v1/transactions/sales-statement/{key}",
                params={"serverId": "remote_153"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        kwargs = svc.call_args.kwargs
        self.assertEqual(kwargs.get("idnum"), 1)
        self.assertEqual(kwargs.get("gubun"), "출고")
        self.assertEqual(kwargs.get("gcode"), "00004")
        body = res.json()
        self.assertEqual(body["order_key"]["idnum"], 1)
        self.assertEqual(body["order_key"]["gubun"], "출고")

    def test_detail_path_accepts_legacy_4_segment_key(self) -> None:
        from app.services import transactions_service

        async def fake_detail(**kwargs: Any) -> dict[str, Any] | None:
            return {
                "order_key": {
                    "gdate": kwargs["gdate"],
                    "hcode": kwargs["hcode"],
                    "jubun": kwargs["jubun"],
                    "gjisa": kwargs.get("gjisa") or "",
                    "idnum": 0,
                    "gubun": "",
                    "gcode": "",
                },
                "customer": {"hcode": kwargs["hcode"], "gname": "", "gcode": ""},
                "gubun": "",
                "slip_no": "",
                "customer_profile": {},
                "stock_qty": None,
                "status": "active",
                "lines": [],
                "memo": {},
            }

        with patch.object(
            transactions_service,
            "get_sales_statement_detail",
            new=AsyncMock(side_effect=fake_detail),
        ) as svc:
            from urllib.parse import quote

            key = "|".join(
                [quote("2026.05.14"), quote("5019"), quote("11"), quote("")]
            )
            res = self.client.get(
                f"/api/v1/transactions/sales-statement/{key}",
                params={"serverId": "remote_153"},
            )
        # 라인 0 → 404; svc 는 호출되었어야 함.
        self.assertIn(res.status_code, (200, 404))
        kwargs = svc.call_args.kwargs
        # 4세그먼트 fallback — idnum None.
        self.assertIsNone(kwargs.get("idnum"))


if __name__ == "__main__":
    main()
