"""CJ대한통운 택배 연동 — 목업 모드 회귀.

키 미설정(config.CJ_API_ENABLED=False) 이면 cj_client 는 HTTP 호출 없이 가이드(V3.9.4)
스키마에 맞춘 결정적 mock 응답을 돌려준다. 라이브 호출은 0 (CI 안전). 실연동은
``RUN_COURIER_SMOKE`` 로 별도 opt-in 예정.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import TestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.main import app  # noqa: E402
from app.core.deps import get_user_context  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import cj_booking_service  # noqa: E402
from app.services.carriers import cj_client  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402


def _ctx() -> dict[str, Any]:
    return {
        "user_id": "tester",
        "server_id": "remote_1",
        "role": "admin",
        "hcode": "0000",
        "permissions": ["*"],
        "tenant_id": "",
        "account_type": "T1",
    }


def _no_http(*_a, **_k):  # pragma: no cover - 목업에서 호출되면 실패시킨다
    raise AssertionError("mock 모드에서 HTTP 호출이 발생하면 안 됨")


class CjClientMockTest(TestCase):
    def test_mode_is_mock_without_credentials(self) -> None:
        self.assertFalse(cj_client.is_enabled())
        self.assertEqual(cj_client.mode(), "mock")

    def test_mock_apis_no_http_and_ok(self) -> None:
        with patch("app.services.open_api_http.urlopen", _no_http):
            tok = cj_client.get_token()
            self.assertTrue(tok.startswith("MOCK-TOKEN-"))

            inv = cj_client.gen_invoice_no(cust_use_no="2026.06.20|5019|00044|11|")
            self.assertTrue(inv["ok"] and inv["mock"])
            invoice = inv["data"]["INVC_NO"]
            self.assertTrue(invoice and invoice.isdigit())

            # 결정적 — 동일 키는 동일 운송장
            self.assertEqual(
                cj_client.gen_invoice_no(cust_use_no="2026.06.20|5019|00044|11|")["data"]["INVC_NO"],
                invoice,
            )

            book = cj_client.register_book({"INVC_NO": invoice, "CUST_USE_NO": "x"})
            self.assertTrue(book["ok"] and book["mock"])

            trk = cj_client.track_by_invoice(invoice)
            self.assertTrue(trk["ok"])
            self.assertIn(trk["data"]["status"], {"pending", "in_transit", "delivered", "booked"})
            self.assertTrue(trk["data"]["CRG_ST_NM"])  # 화물상태명 매핑

            cancel = cj_client.cancel_book(cust_use_no="x", rcpt_ymd="20260620")
            self.assertTrue(cancel["ok"] and cancel["mock"])

            addr = cj_client.refine_address("서울 강남구 테헤란로 1")
            self.assertTrue(addr["ok"] and addr["mock"])


class CjBookingServiceMockTest(TestCase):
    def test_book_then_cancel_updates_dispatch_state(self) -> None:
        calls: dict[str, Any] = {}

        def _upsert(server_id, *, dispatch_id, tracking_no, carrier):  # noqa: ANN001
            calls["upsert"] = (server_id, dispatch_id, tracking_no, carrier)
            return {"dispatch_id": dispatch_id, "tracking_no": tracking_no}

        def _set_status(server_id, *, dispatch_id, status, source="manual", tracking_no=None):  # noqa: ANN001
            calls.setdefault("status", []).append(status)
            return {"dispatch_id": dispatch_id, "status": status}

        with patch("app.services.open_api_http.urlopen", _no_http), \
             patch.object(cj_booking_service.dispatch, "upsert_tracking", _upsert), \
             patch.object(cj_booking_service.dispatch, "set_dispatch_status", _set_status):
            did = "2026.06.20|5019|00044|11|"
            res = cj_booking_service.book_dispatch(
                "remote_1",
                dispatch_id=did,
                sender={"name": "교문사", "tel": "02-1577-1111"},
                recipient={"name": "(주)북센", "tel": "031-955-6777", "zip": "10881"},
                goods=[{"name": "도서", "qty": 3, "amount": 187000}],
            )
            self.assertTrue(res["ok"])
            self.assertTrue(res["invoice_no"])
            # 운송장이 carrier='cj' 로 저장되고 상태 'booked' 확정
            self.assertEqual(calls["upsert"][3], "cj")
            self.assertIn("booked", calls["status"])

            cancel = cj_booking_service.cancel_dispatch("remote_1", dispatch_id=did, invoice_no=res["invoice_no"])
            self.assertTrue(cancel["ok"])
            self.assertIn("cancelled", calls["status"])

    def test_tel_split(self) -> None:
        self.assertEqual(cj_booking_service._split_tel("02-1577-1111"), ("02", "1577", "1111"))
        self.assertEqual(cj_booking_service._split_tel("031-955-6777"), ("031", "955", "6777"))

    def test_dispatch_refresh_response_accepts_cj_source(self) -> None:
        # 회귀(2026-06-21): 배송조회 응답 source Literal 이 'cj'/'cj-mock' 와 status
        # 'booked'/'cancelled' 를 허용해야 한다(화면 데모에서 refresh 500 잡힘).
        from app.models.delivery_dispatch import DeliveryDispatchRefreshResponse

        for src in ("cj", "cj-mock"):
            m = DeliveryDispatchRefreshResponse(
                dispatch_id="d", status="booked", source=src,
                last_updated="t", last_checked="t",
            )
            self.assertEqual(m.source, src)
        self.assertEqual(
            DeliveryDispatchRefreshResponse(
                dispatch_id="d", status="cancelled", source="cj",
                last_updated="t", last_checked="t",
            ).status,
            "cancelled",
        )


class CjRouterMockTest(TestCase):
    def setUp(self) -> None:
        async def _u() -> dict[str, Any]:
            return _ctx()

        app.dependency_overrides[get_current_user] = _u
        app.dependency_overrides[get_user_context] = _u
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_status_endpoint_mock(self) -> None:
        r = self.client.get("/api/v1/courier/cj/status?serverId=remote_1")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["mode"], "mock")

    def test_booking_and_cancel_endpoints(self) -> None:
        with patch("app.services.open_api_http.urlopen", _no_http), \
             patch.object(cj_booking_service.dispatch, "upsert_tracking", lambda *a, **k: {}), \
             patch.object(cj_booking_service.dispatch, "set_dispatch_status", lambda *a, **k: {}):
            book = self.client.post(
                "/api/v1/courier/cj/booking",
                json={
                    "serverId": "remote_1",
                    "dispatchId": "2026.06.20|5019|00044|11|",
                    "recipient": {"name": "(주)북센", "tel": "031-955-6777"},
                },
            )
            self.assertEqual(book.status_code, 200, book.text)
            body = book.json()
            self.assertTrue(body["ok"] and body["invoice_no"])

            cancel = self.client.post(
                "/api/v1/courier/cj/cancel",
                json={"serverId": "remote_1", "dispatchId": "2026.06.20|5019|00044|11|"},
            )
            self.assertEqual(cancel.status_code, 200, cancel.text)
            self.assertTrue(cancel.json()["ok"])


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
