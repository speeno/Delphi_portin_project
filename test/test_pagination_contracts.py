"""
DEC-024 — list 응답 계약 회귀 가드 (C2/C6/C9 + reports).

목적
----
표준 ``page`` 객체가 모든 list/aggregate 라우터에 일관되게 노출되는지 검증.
- C2 outbound list: ``page`` + BC 평면(total/limit/offset).
- C6 sales-statement list: ``page`` + BC 평면.
- C6 reports book-sales / customer-sales: ``page`` (가상 페이징, BC total).
- C9 master 6개 (customer/book/publisher/book-code/discount/logistics-cost):
  ``page`` 단독 (BC 평면 없음 — 신규 표준).

실 DB 미사용 — 서비스 함수만 patch 하여 라우터 직렬화/스키마 계약을 검증.
"""

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
from app.services import (  # noqa: E402
    masters_service,
    outbound_service,
    reports_service,
    transactions_service,
)


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


PAGE_KEYS = {"limit", "offset", "total", "has_more"}


def _assert_page_shape(tc: TestCase, page: dict, *, expected_total: int) -> None:
    tc.assertEqual(set(page.keys()), PAGE_KEYS)
    tc.assertIsInstance(page["limit"], int)
    tc.assertIsInstance(page["offset"], int)
    tc.assertIsInstance(page["total"], int)
    tc.assertIsInstance(page["has_more"], bool)
    tc.assertEqual(page["total"], expected_total)


class C2OutboundListPageContract(TestCase):
    """C2 — 신규 page + BC 평면 동시 노출."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_returns_page_and_legacy_flat(self) -> None:
        items = [
            {
                "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "1"},
                "customer_name": "테스트",
                "lines": 1,
                "qty": 1,
                "amount": 100,
                "status": "active",
            }
        ]

        async def fake_list(**kwargs):  # noqa: ARG001
            return items, 37

        with patch.object(outbound_service, "list_orders", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/outbound/orders"
                "?serverId=remote_1&dateFrom=2026-04-18&dateTo=2026-04-25"
                "&limit=100&offset=0",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        # 신규 표준
        self.assertIn("page", body)
        _assert_page_shape(self, body["page"], expected_total=37)
        self.assertEqual(body["page"]["limit"], 100)
        self.assertEqual(body["page"]["offset"], 0)
        # BC 평면
        self.assertEqual(body["total"], 37)
        self.assertEqual(body["limit"], 100)
        self.assertEqual(body["offset"], 0)


class C6SalesStatementListPageContract(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_returns_page_and_legacy_flat(self) -> None:
        items = [
            {
                "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "1"},
                "customer_name": "테스트",
                "row_count": 2,
                "qty": 5,
                "amount": 50000,
                "status": "active",
            }
        ]

        async def fake_list(**kwargs):  # noqa: ARG001
            return items, 12

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get(
                "/api/v1/transactions/sales-statement"
                "?serverId=remote_1&hcode=A0001"
                "&dateFrom=2026-04-18&dateTo=2026-04-25"
                "&limit=50&offset=0",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("page", body)
        _assert_page_shape(self, body["page"], expected_total=12)
        self.assertEqual(body["page"]["limit"], 50)
        self.assertEqual(body["total"], 12)
        self.assertEqual(body["limit"], 50)


class C6ReportsPageContract(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_book_sales_returns_page(self) -> None:
        async def fake_book(**kwargs):  # noqa: ARG001
            limit = kwargs.get("limit") or 100
            offset = kwargs.get("offset") or 0
            return {
                "rows": [{"gcode": "G01", "gname": "도서A"}],
                "total": 7,
                "page": {
                    "limit": limit,
                    "offset": offset,
                    "total": 7,
                    "has_more": False,
                },
            }

        with patch.object(reports_service, "get_book_sales", side_effect=fake_book):
            res = self.client.get(
                "/api/v1/reports/book-sales"
                "?serverId=remote_1&hcode=A0001"
                "&dateFrom=2026-04-18&dateTo=2026-04-25"
                "&limit=200&offset=0",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("page", body)
        _assert_page_shape(self, body["page"], expected_total=7)
        # BC total 도 보존
        self.assertEqual(body["total"], 7)

    def test_customer_sales_returns_page(self) -> None:
        async def fake_cust(**kwargs):  # noqa: ARG001
            limit = kwargs.get("limit") or 100
            offset = kwargs.get("offset") or 0
            return {
                "rows": [{"hcode": "A0001", "gcode": "G01"}],
                "total": 3,
                "page": {
                    "limit": limit,
                    "offset": offset,
                    "total": 3,
                    "has_more": False,
                },
            }

        with patch.object(
            reports_service, "get_customer_sales", side_effect=fake_cust
        ):
            res = self.client.get(
                "/api/v1/reports/customer-sales"
                "?serverId=remote_1"
                "&dateFrom=2026-04-18&dateTo=2026-04-25"
                "&limit=100&offset=0",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("page", body)
        _assert_page_shape(self, body["page"], expected_total=3)


class C9MastersListPageContract(TestCase):
    """C9 마스터 6개 — 신규 표준 page 단독 (BC 평면 없음)."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def _check_only_page(self, body: dict, *, expected_total: int) -> None:
        self.assertIn("page", body)
        _assert_page_shape(self, body["page"], expected_total=expected_total)
        # C9 는 BC 평면을 노출하지 않는 신규 표준.
        self.assertNotIn("total", body)
        self.assertNotIn("limit", body)
        self.assertNotIn("offset", body)

    def _fake_response(self, total: int, *, limit: int = 100, offset: int = 0):
        """items 가 빈 리스트라도 page 계약은 동일하게 검증된다.

        실제 row 스키마는 모델별로 다르지만, paging 계약 회귀는 row 형태와 무관 —
        items=[] 로 항상 안전하게 검증.
        """

        async def fake(**kwargs):  # noqa: ARG001
            return {
                "items": [],
                "page": {
                    "limit": limit,
                    "offset": offset,
                    "total": total,
                    "has_more": False,
                },
            }

        return fake

    def test_customer_list(self) -> None:
        with patch.object(
            masters_service,
            "list_customer_master",
            side_effect=self._fake_response(5),
        ):
            res = self.client.get("/api/v1/masters/customer?serverId=remote_1")
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=5)

    def test_book_list(self) -> None:
        with patch.object(
            masters_service, "list_books", side_effect=self._fake_response(2)
        ):
            res = self.client.get("/api/v1/masters/book?serverId=remote_1")
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=2)

    def test_publisher_list(self) -> None:
        with patch.object(
            masters_service, "list_publishers", side_effect=self._fake_response(1)
        ):
            res = self.client.get("/api/v1/masters/publisher?serverId=remote_1")
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=1)

    def test_book_code_list(self) -> None:
        with patch.object(
            masters_service, "list_book_codes", side_effect=self._fake_response(4)
        ):
            res = self.client.get("/api/v1/masters/book-code?serverId=remote_1")
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=4)

    def test_discount_list(self) -> None:
        with patch.object(
            masters_service, "list_discounts", side_effect=self._fake_response(9)
        ):
            res = self.client.get("/api/v1/masters/discount?serverId=remote_1")
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=9)

    def test_logistics_cost_list(self) -> None:
        with patch.object(
            masters_service,
            "list_logistics_costs",
            side_effect=self._fake_response(6),
        ):
            res = self.client.get(
                "/api/v1/masters/logistics-cost?serverId=remote_1",
            )
        self.assertEqual(res.status_code, 200, res.text)
        self._check_only_page(res.json(), expected_total=6)


if __name__ == "__main__":
    main()
