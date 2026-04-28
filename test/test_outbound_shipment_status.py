"""출고현황 집계 엔드포인트 회귀 — 리스트(C2)와 다른 완화 필터 + 서버 페이징.

추가 가드 (DEC-052 부산물): Sobo67 Panel102 토글 동등성 (storeKind A/B/ALL).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, MagicMock, patch

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
                    "Jubun": "J1",
                    "yesno_max": "1",
                    "qty": 6,
                    "amount": 600,
                },
                {
                    "Gdate": "2026.04.01",
                    "Hcode": "H001",
                    "Jubun": "J2",
                    "yesno_max": "1",
                    "qty": 4,
                    "amount": 400,
                }
            ],
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
        self.assertEqual(body["items"][0]["qty"], 10)
        self.assertEqual(body["items"][0]["amount"], 1000)
        self.assertEqual(body["page"]["total"], 1)
        mock_exec.assert_called_once()


class ShipmentStatusMysql3PathTests(TestCase):
    """파생 테이블 없이 단일 GROUP BY + 메모리 집계."""

    @patch("app.services.outbound_service.mysql3_protocol", return_value=False)
    @patch("app.services.outbound_service._fetch_customer_names", new_callable=AsyncMock)
    @patch("app.services.outbound_service.execute_query", new_callable=AsyncMock)
    def test_shipment_status_in_memory_aggregate_for_all_servers(
        self,
        mock_exec: AsyncMock,
        mock_names: AsyncMock,
        _mock_m3: MagicMock,
    ) -> None:
        mock_names.return_value = {"H001": "가게"}
        mock_exec.side_effect = [
            [
                {
                    "Gdate": "2026.04.01",
                    "Hcode": "H001",
                    "Jubun": "J1",
                    "yesno_max": "1",
                    "qty": 5,
                    "amount": 500,
                },
                {
                    "Gdate": "2026.04.01",
                    "Hcode": "H001",
                    "Jubun": "J2",
                    "yesno_max": "2",
                    "qty": 3,
                    "amount": 100,
                },
            ]
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
        self.assertEqual(body["items"][0]["orders"], 2)
        self.assertEqual(body["items"][0]["qty"], 8)
        self.assertEqual(body["items"][0]["cancelled_orders"], 1)
        mock_exec.assert_called_once()
        sql = mock_exec.call_args.args[1]
        self.assertNotIn("FROM (", sql)
        self.assertNotIn("CASE WHEN", sql)
        self.assertNotIn("COUNT(*) AS total FROM", sql)


class ShipmentStatusOrderLevelSqlTests(TestCase):
    """mysql3 inner SQL — COALESCE 미지원 회귀 (IFNULL 분기)."""

    @patch("app.services.outbound_service.mysql3_protocol", return_value=True)
    def test_order_level_sql_uses_ifnull_when_mysql3(self, _m: MagicMock) -> None:
        from app.services.outbound_service import _shipment_status_order_level_sql

        sql = _shipment_status_order_level_sql(
            "Gdate >= %s AND Gdate <= %s", "", server_id="remote_154"
        )
        self.assertIn("IFNULL(Jubun", sql)
        self.assertIn("IFNULL(SUM(Gsqut)", sql)
        self.assertNotIn("COALESCE", sql)

    @patch("app.services.outbound_service.mysql3_protocol", return_value=False)
    def test_order_level_sql_uses_coalesce_when_modern(self, _m: MagicMock) -> None:
        from app.services.outbound_service import _shipment_status_order_level_sql

        sql = _shipment_status_order_level_sql(
            "Gdate >= %s AND Gdate <= %s", "", server_id="remote_138"
        )
        self.assertIn("COALESCE(Jubun", sql)
        self.assertNotIn("IFNULL(Jubun", sql)


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
