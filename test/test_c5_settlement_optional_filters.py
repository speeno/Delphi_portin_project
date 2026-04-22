"""C5 정산 — DEC-033 (f) 필터 옵셔널화 + 페이저 round-trip 회귀 가드.

배경
----
2026-04-22 발송비/입금 422 핫픽스 사이클 (사이클 ID: settlement-422-hotfix).
이전: hcode 비움 + 자동 load() → 422 / 500 회귀.
이후: hcode 옵셔널화 + 전체 거래처 fallback (DEC-033 (f)) + DataGridPager (DEC-033 (g)).

검증 5 클래스 (contract migration/contracts/settlement_billing.yaml v1.3.0 부속)
- PeriodOptionalHcodeTests:           /billing/period (Sobo47)
- CashStatusSdateOptionalHcodeTests:  /cash-status?variant=sdate (Sobo42_1)
- TaxInvoiceOptionalHcodeTests:       /tax-invoice (Sobo49)
- OutstandingAggregateTests:          /outstanding (신규)
- PaginationRoundTripTests:           5 list endpoint 의 limit/offset 보존

설계 정합 (사용자 룰)
-------------------
- 기존 test_c5_settlement_phase1.py 의 monkeypatch + dependency_overrides 패턴 재사용.
- 신규 헬퍼 0 (test_p1_12_period_summary_validation 와 동일 패턴).
- 작은 케이스, 빠른 실행 (mock 만 사용, DB 의존 0).
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
from app.services import settlement_service, tax_invoice_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}


app.dependency_overrides[get_current_user] = _override_auth


class _BaseClient(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)


class PeriodOptionalHcodeTests(_BaseClient):
    """TC-ST-P1-12-OPT-HCODE / TC-ST-P1-12-MISS-MONTH 회귀 가드."""

    def test_hcode_omitted_returns_200_with_none_passed(self) -> None:
        captured: dict = {}

        async def fake_period(**kwargs):
            captured.update(kwargs)
            return {"items": [], "totals": {"gsumx": 0, "gsumy": 0, "gssum": 0}, "total": 0}

        with patch.object(settlement_service, "list_period_summary",
                          side_effect=fake_period, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing/period"
                "?serverId=remote_1&monthFrom=202603&monthTo=202604"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIsNone(captured.get("hcode"))

    def test_boundary_month_missing_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/billing/period"
            "?serverId=remote_1&monthTo=202604"
        )
        self.assertEqual(res.status_code, 422, res.text)


class CashStatusSdateOptionalHcodeTests(_BaseClient):
    """TC-ST-CASH-STATUS-SDATE-OPT — variant=sdate + hcode 빈값 → 200 fallback."""

    def test_sdate_variant_without_hcode_returns_200(self) -> None:
        captured: dict = {}

        async def fake_cash_status(**kwargs):
            captured.update(kwargs)
            return {
                "variant": "sdate",
                "items": [],
                "totals": {"gpsum": 0, "gssum": 0},
                "total_count": 0,
            }

        with patch.object(settlement_service, "cash_status",
                          side_effect=fake_cash_status, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash-status"
                "?serverId=remote_1&variant=sdate&month=202603"
            )
        self.assertEqual(res.status_code, 200, res.text)
        # hcode 가 None 으로 서비스에 전달되어 전체 거래처 fallback 트리거.
        self.assertIsNone(captured.get("hcode"))
        self.assertEqual(captured.get("variant"), "sdate")

    def test_boundary_month_missing_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/cash-status"
            "?serverId=remote_1&variant=sdate"
        )
        self.assertEqual(res.status_code, 422, res.text)


class TaxInvoiceOptionalHcodeTests(_BaseClient):
    """TC-ST-TAX-OPT-HCODE — hcode 옵셔널 + limit/offset round-trip."""

    def test_tax_invoice_without_hcode_returns_200(self) -> None:
        captured: dict = {}

        async def fake_list_tax(**kwargs):
            captured.update(kwargs)
            return {
                "gdate": kwargs.get("gdate", ""),
                "items": [],
                "totals": {"sum27": 0},
                "total": 0,
            }

        with patch.object(tax_invoice_service, "list_tax_invoices",
                          side_effect=fake_list_tax, create=True):
            res = self.client.get(
                "/api/v1/settlement/tax-invoice"
                "?serverId=remote_1&gdate=202603&limit=20&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIsNone(captured.get("hcode"))
        self.assertEqual(captured.get("limit"), 20)
        self.assertEqual(captured.get("offset"), 0)

    def test_gdate_too_short_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/tax-invoice"
            "?serverId=remote_1&gdate=20"
        )
        self.assertEqual(res.status_code, 422, res.text)


class OutstandingAggregateTests(_BaseClient):
    """TC-ST-OUTSTANDING-200 — 신규 서버 집계 endpoint 라우팅 + truncated 플래그."""

    def test_outstanding_default_200(self) -> None:
        captured: dict = {}

        async def fake_compute(**kwargs):
            captured.update(kwargs)
            return {
                "items": [
                    {"hcode": "C001", "hname": "신화서점",
                     "billed": 1000, "paid": 600, "balance": 400},
                ],
                "totals": {"billed": 1000, "cash_received": 600, "balance": 400},
                "total": 1,
                "limit": kwargs.get("limit", 50),
                "offset": kwargs.get("offset", 0),
                "truncated": False,
            }

        with patch.object(settlement_service, "compute_outstanding_by_customer",
                          side_effect=fake_compute, create=True):
            res = self.client.get(
                "/api/v1/settlement/outstanding"
                "?serverId=remote_1&monthFrom=202601&monthTo=202604&limit=50&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["totals"]["balance"], 400)
        self.assertFalse(body["truncated"])
        self.assertEqual(body["items"][0]["hcode"], "C001")
        self.assertIsNone(captured.get("hcode"))

    def test_outstanding_truncated_flag_propagates(self) -> None:
        async def fake_compute(**kwargs):
            return {
                "items": [],
                "totals": {"billed": 0, "cash_received": 0, "balance": 0},
                "total": 0,
                "limit": kwargs.get("limit", 50),
                "offset": kwargs.get("offset", 0),
                "truncated": True,
            }

        with patch.object(settlement_service, "compute_outstanding_by_customer",
                          side_effect=fake_compute, create=True):
            res = self.client.get(
                "/api/v1/settlement/outstanding"
                "?serverId=remote_1&monthFrom=202601&monthTo=202612"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["truncated"])

    def test_outstanding_boundary_missing_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/outstanding?serverId=remote_1&monthTo=202604"
        )
        self.assertEqual(res.status_code, 422, res.text)


class PaginationRoundTripTests(_BaseClient):
    """TC-ST-PAGER-ROUND-TRIP — 5 list endpoint 의 limit/offset 라우팅 보존."""

    def test_period_pager_round_trip(self) -> None:
        captured: dict = {}

        async def fake_period(**kwargs):
            captured.update(kwargs)
            return {"items": [], "totals": {"gsumx": 0, "gsumy": 0, "gssum": 0},
                    "total": 0}

        with patch.object(settlement_service, "list_period_summary",
                          side_effect=fake_period, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing/period"
                "?serverId=remote_1&monthFrom=202603&monthTo=202604"
                "&limit=10&offset=20"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("limit"), 10)
        self.assertEqual(captured.get("offset"), 20)

    def test_cash_status_pager_round_trip(self) -> None:
        captured: dict = {}

        async def fake_cash_status(**kwargs):
            captured.update(kwargs)
            return {
                "variant": "hcode", "items": [],
                "totals": {}, "total_count": 0,
            }

        with patch.object(settlement_service, "cash_status",
                          side_effect=fake_cash_status, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash-status"
                "?serverId=remote_1&variant=hcode&month=202603"
                "&limit=25&offset=50"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("limit"), 25)
        self.assertEqual(captured.get("offset"), 50)
        body = res.json()
        self.assertEqual(body["page"]["limit"], 25)
        self.assertEqual(body["page"]["offset"], 50)

    def test_tax_invoice_pager_round_trip(self) -> None:
        captured: dict = {}

        async def fake_list_tax(**kwargs):
            captured.update(kwargs)
            return {
                "gdate": kwargs.get("gdate", ""),
                "items": [], "totals": {"sum27": 0}, "total": 0,
            }

        with patch.object(tax_invoice_service, "list_tax_invoices",
                          side_effect=fake_list_tax, create=True):
            res = self.client.get(
                "/api/v1/settlement/tax-invoice"
                "?serverId=remote_1&gdate=202603&limit=15&offset=30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("limit"), 15)
        self.assertEqual(captured.get("offset"), 30)

    def test_outstanding_pager_round_trip(self) -> None:
        captured: dict = {}

        async def fake_compute(**kwargs):
            captured.update(kwargs)
            return {
                "items": [],
                "totals": {"billed": 0, "cash_received": 0, "balance": 0},
                "total": 0,
                "limit": kwargs.get("limit", 50),
                "offset": kwargs.get("offset", 0),
                "truncated": False,
            }

        with patch.object(settlement_service, "compute_outstanding_by_customer",
                          side_effect=fake_compute, create=True):
            res = self.client.get(
                "/api/v1/settlement/outstanding"
                "?serverId=remote_1&monthFrom=202601&monthTo=202604"
                "&limit=12&offset=24"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("limit"), 12)
        self.assertEqual(captured.get("offset"), 24)
        body = res.json()
        self.assertEqual(body["page"]["limit"], 12)
        self.assertEqual(body["page"]["offset"], 24)

    def test_billing_pager_round_trip(self) -> None:
        """5 화면 표준 페이저 정책 합류 — billing list 도 페이지 메타 보존."""
        captured: dict = {}

        async def fake_list_billing(**kwargs):
            captured.update(kwargs)
            return ([], 0)

        with patch.object(settlement_service, "list_billing",
                          side_effect=fake_list_billing, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing"
                "?serverId=remote_1&monthFrom=202603&monthTo=202604"
                "&limit=10&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("limit"), 10)
        self.assertEqual(captured.get("offset"), 0)


if __name__ == "__main__":  # pragma: no cover
    main()
