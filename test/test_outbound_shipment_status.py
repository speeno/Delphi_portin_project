"""출고현황 집계 엔드포인트 회귀 — 리스트(C2)와 다른 완화 필터 + 서버 페이징.

추가 가드 (DEC-052 부산물): Sobo67 Panel102 토글 동등성 (storeKind A/B/ALL).
"""

from __future__ import annotations

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


def _override_auth() -> dict:
    return {"user_id": "u1", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


class ShipmentStatusRouteTests(TestCase):
    def tearDown(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth

    @patch("app.services.outbound_service._fetch_customer_names", new_callable=AsyncMock)
    @patch("app.services.outbound_service.execute_query", new_callable=AsyncMock)
    def test_shipment_status_endpoint_ok(self, mock_exec: AsyncMock, mock_names: AsyncMock) -> None:
        mock_names.return_value = {"H001": "테스트상점"}
        mock_exec.side_effect = [
            [
                {
                    "Gdate": "2026.04.01",
                    "Hcode": "H001",
                    "order_count": 2,
                    "qty_sum": 10,
                    "amt_sum": 1000,
                    "cancelled_cnt": 0,
                }
            ],
            [{"total": 1}],
        ]
        client = TestClient(app)
        r = client.get(
            "/api/v1/outbound/shipment-status",
            params={
                "serverId": "remote_1",
                "dateFrom": "2026-04-01",
                "dateTo": "2026-04-30",
                "limit": 50,
                "offset": 0,
            },
        )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(len(body["items"]), 1)
        self.assertEqual(body["items"][0]["hcode"], "H001")
        self.assertEqual(body["items"][0]["orders"], 2)
        self.assertEqual(body["page"]["total"], 1)


class ShipmentStatusStoreKindTests(TestCase):
    """``storeKind`` 토글 (A/B/ALL) → ``_shipment_status_where`` SQL 동등성 가드."""

    def test_default_is_warehouse_B(self) -> None:
        from app.services.outbound_service import _shipment_status_where

        sql, params = _shipment_status_where(
            date_from="2026-04-01", date_to="2026-04-30", hcode=None
        )
        self.assertIn("Ocode = %s", sql)
        self.assertIn("B", params)

    def test_store_kind_A_means_headquarters(self) -> None:
        from app.services.outbound_service import _shipment_status_where

        sql, params = _shipment_status_where(
            date_from="2026-04-01", date_to="2026-04-30", hcode=None, store_kind="A"
        )
        self.assertIn("Ocode = %s", sql)
        self.assertIn("A", params)
        self.assertNotIn("B", params)

    def test_store_kind_ALL_omits_ocode_clause(self) -> None:
        from app.services.outbound_service import _shipment_status_where

        sql, params = _shipment_status_where(
            date_from="2026-04-01",
            date_to="2026-04-30",
            hcode=None,
            store_kind="ALL",
        )
        self.assertNotIn("Ocode", sql)
        self.assertNotIn("A", params)
        self.assertNotIn("B", [p for p in params if isinstance(p, str) and len(p) == 1])


if __name__ == "__main__":
    main(verbosity=2)
