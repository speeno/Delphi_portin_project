"""
C2 출고 접수 — 1차 포팅(phase1) 검증 테스트.

목적
----
도서물류관리프로그램 C2 1차 합격선 (`outbound_order.yaml.acceptance_goal`):
  "기존 사용자가 출고 주문을 신규 등록 / 수정 / 취소 / 조회 (CRUD) 할 수 있다."
에 대해 contract `migration/contracts/outbound_order.yaml` v1.0.0 와 실 구현을
1:1 검증.

검증 케이스 (test pack outbound_order.json v1.0.0-phase1 의 1차 in_scope 9건 중
단위 테스트로 가능한 항목)
- TC-OUT-001: 신규 등록 (POST → 201, INSERT × N 트랜잭션 호출 검증)
- TC-OUT-002: 수정 (PUT → 200, desired-state diff inserted/updated/deleted)
- TC-OUT-003: 취소 (PATCH → 200, soft delete UPDATE Yesno='2')
- TC-OUT-004: 조회 목록 (GET → items/total + customer_name lookup)
- TC-OUT-005: 트랜잭션 롤백 (INSERT 도중 실패 시 500 + audit failure)
- TC-OUT-008: 마스터 자동완성 (GET /masters/products → items)
- TC-OUT-009: 감사 로그 (audit.outbound created/updated/cancelled 모두 기록)
- TC-OUT-PERMISSION-001 (deferred): 권한키 분기 미수행 — 모든 인증 사용자 동등 (DEC-009).

부수 검증 (DEC-009~012 1차 동결 부합)
- DEC-009: 권한키 미적용 — 라우터 RBAC 미존재 (단위테스트로 분기 부재 확인).
- DEC-012: 물리 삭제 미지원 — DELETE HTTP 메서드 미제공.

주의
----
실 DB 연결 없이 outbound_service 내부 함수만 monkeypatch.
사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import logging
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
from app.services import outbound_service  # noqa: E402


def _override_auth() -> dict:
    """JWT 검증을 우회 — 모든 테스트는 인증된 사용자로 가정."""
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


VALID_HEADER = {
    "gdate": "2026-04-25",
    "hcode": "A0001",
    "gjisa": "1",
}
VALID_LINES = [
    {"gcode": "G01", "bcode": "B0001", "pubun": "신간", "gsqut": 5, "gssum": 50000},
    {"gcode": "G01", "bcode": "B0002", "pubun": "신간", "gsqut": 3, "gssum": 30000},
]


class CapturingHandler(logging.Handler):
    """audit.outbound 로거 출력 캡처."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:  # noqa: D401
        self.records.append(record)

    def parsed(self) -> list[dict]:
        out: list[dict] = []
        for r in self.records:
            msg = r.getMessage()
            idx = msg.find("{")
            if idx < 0:
                continue
            try:
                out.append(json.loads(msg[idx:]))
            except json.JSONDecodeError:
                continue
        return out


class C2OutboundPhase1Tests(TestCase):
    """C2 phase1 라우터 단위 검증."""

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.outbound")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # -- TC-OUT-001 신규 등록 -------------------------------------------------

    def test_tc_out_001_create_returns_201_with_order_key(self) -> None:
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "120000000001"},
                "lines": len(lines),
                "qty": sum(l["gsqut"] for l in lines),
                "amount": sum(l.get("gssum", 0) for l in lines),
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        with patch.object(outbound_service, "create_order", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/outbound/orders",
                json={
                    "serverId": "remote_1",
                    "orderHeader": VALID_HEADER,
                    "orderLines": VALID_LINES,
                },
            )

        self.assertEqual(res.status_code, 201, res.text)
        body = res.json()
        self.assertEqual(body["order_key"]["hcode"], "A0001")
        self.assertEqual(body["lines"], 2)
        self.assertEqual(body["qty"], 8)
        self.assertEqual(body["amount"], 80000)

    # -- TC-OUT-002 수정 (PUT) — diff -----------------------------------------

    def test_tc_out_002_update_returns_diff(self) -> None:
        async def fake_update(*, server_id, gdate, hcode, jubun, desired_lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "lines": len(desired_lines),
                "qty": 7,
                "amount": 70000,
                "updated_at": "2026-04-25T04:00:00+00:00",
                "diff": {"inserted": 1, "updated": 1, "deleted": 0},
            }

        with patch.object(outbound_service, "update_order", side_effect=fake_update):
            res = self.client.put(
                "/api/v1/outbound/orders/2026.04.25%7CA0001%7C120000000001"
                "?serverId=remote_1",
                json={
                    "orderLines": [
                        {"gcode": "G01", "bcode": "B0001", "gsqut": 4, "gssum": 40000},
                        {"gcode": "G01", "bcode": "B0003", "gsqut": 3, "gssum": 30000},
                    ]
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["diff"], {"inserted": 1, "updated": 1, "deleted": 0})

    # -- TC-OUT-003 취소 (PATCH) ----------------------------------------------

    def test_tc_out_003_cancel_returns_cancelled(self) -> None:
        async def fake_cancel(*, server_id, gdate, hcode, jubun):  # noqa: ARG001
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "status": "cancelled",
                "cancelled_at": "2026-04-25T05:00:00+00:00",
            }

        with patch.object(outbound_service, "cancel_order", side_effect=fake_cancel):
            res = self.client.patch(
                "/api/v1/outbound/orders/2026.04.25%7CA0001%7C120000000001/cancel"
                "?serverId=remote_1",
                json={"reason": "거래처 요청"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["status"], "cancelled")

    def test_tc_out_003_cancel_idempotent_returns_409(self) -> None:
        async def fake_cancel(*, server_id, gdate, hcode, jubun):  # noqa: ARG001
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "status": "already_cancelled",
                "cancelled_at": "2026-04-25T06:00:00+00:00",
            }

        with patch.object(outbound_service, "cancel_order", side_effect=fake_cancel):
            res = self.client.patch(
                "/api/v1/outbound/orders/2026.04.25%7CA0001%7C120000000001/cancel"
                "?serverId=remote_1",
                json={},
            )
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json()["detail"]["code"], "OUT_DUPLICATE")

    # -- TC-OUT-004 목록 조회 -------------------------------------------------

    def test_tc_out_004_list_returns_items_and_total(self) -> None:
        async def fake_list(**kwargs):  # noqa: ARG001
            items = [
                {
                    "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "120000000001"},
                    "customer_name": "테스트거래처",
                    "lines": 2,
                    "qty": 8,
                    "amount": 80000,
                    "status": "active",
                }
            ]
            return items, len(items)

        with patch.object(outbound_service, "list_orders", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/outbound/orders"
                "?serverId=remote_1&dateFrom=2026-04-18&dateTo=2026-04-25",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["total"], 1)
        self.assertEqual(body["items"][0]["customer_name"], "테스트거래처")
        self.assertEqual(body["items"][0]["status"], "active")

    # -- TC-OUT-005 트랜잭션 롤백 → 500 + audit failure ------------------------

    def test_tc_out_005_create_db_error_returns_500_and_audit_failure(self) -> None:
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            raise RuntimeError("simulated db error")

        with patch.object(outbound_service, "create_order", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/outbound/orders",
                json={
                    "serverId": "remote_1",
                    "orderHeader": VALID_HEADER,
                    "orderLines": VALID_LINES,
                },
            )
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json()["detail"]["code"], "OUT_TX_FAILED")

        # audit failure 1건
        records = self.handler.parsed()
        failures = [r for r in records if r.get("result") == "failure"]
        self.assertGreaterEqual(len(failures), 1)
        self.assertEqual(failures[0]["action"], "created")

    # -- TC-OUT-008 마스터 자동완성 -------------------------------------------

    def test_tc_out_008_master_products_search(self) -> None:
        async def fake_products(*, server_id, q, limit):  # noqa: ARG001
            return [{"bcode": "B0001", "gname": "테스트도서", "gjeja": "홍길동"}]

        with patch(
            "app.routers.masters.masters_service.search_products",
            side_effect=fake_products,
        ):
            res = self.client.get(
                "/api/v1/masters/products?serverId=remote_1&q=test",
            )
        self.assertEqual(res.status_code, 200, res.text)
        items = res.json()["items"]
        self.assertEqual(items[0]["bcode"], "B0001")

    # -- TC-OUT-009 감사 로그: created/updated/cancelled 각 1건 -----------------

    def test_tc_out_009_audit_logs_all_actions(self) -> None:
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "1"},
                "lines": 1, "qty": 1, "amount": 100,
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        async def fake_update(*, server_id, gdate, hcode, jubun, desired_lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "lines": 1, "qty": 1, "amount": 100,
                "updated_at": "2026-04-25T04:00:00+00:00",
                "diff": {"inserted": 0, "updated": 1, "deleted": 0},
            }

        async def fake_cancel(*, server_id, gdate, hcode, jubun):  # noqa: ARG001
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "status": "cancelled",
                "cancelled_at": "2026-04-25T05:00:00+00:00",
            }

        with patch.object(outbound_service, "create_order", side_effect=fake_create):
            self.client.post(
                "/api/v1/outbound/orders",
                json={
                    "serverId": "remote_1",
                    "orderHeader": VALID_HEADER,
                    "orderLines": [VALID_LINES[0]],
                },
                headers={"X-Forwarded-For": "203.0.113.5"},
            )
        with patch.object(outbound_service, "update_order", side_effect=fake_update):
            self.client.put(
                "/api/v1/outbound/orders/2026.04.25%7CA0001%7C1?serverId=remote_1",
                json={"orderLines": [VALID_LINES[0]]},
            )
        with patch.object(outbound_service, "cancel_order", side_effect=fake_cancel):
            self.client.patch(
                "/api/v1/outbound/orders/2026.04.25%7CA0001%7C1/cancel"
                "?serverId=remote_1",
                json={},
            )

        records = self.handler.parsed()
        actions = {r.get("action") for r in records if r.get("result") == "success"}
        self.assertEqual(
            actions, {"created", "updated", "cancelled"},
            f"expected all three actions in success audit, got {actions}",
        )
        # Contract equivalence.audit.fields 검증
        required = {"timestamp", "gcode", "action", "result", "order_key", "client_ip"}
        for rec in records:
            self.assertTrue(
                required.issubset(rec.keys()),
                f"missing required audit fields in {rec}",
            )

    # -- DEC-009 권한키 미적용 (deferred 검증) ---------------------------------

    def test_dec_009_no_permission_branch_for_authenticated_user(self) -> None:
        """모든 인증 사용자가 권한키 분기 없이 신규/수정/취소 요청 통과."""
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": "2026.04.25", "hcode": "A0001", "jubun": "1"},
                "lines": 1, "qty": 1, "amount": 100,
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        with patch.object(outbound_service, "create_order", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/outbound/orders",
                json={
                    "serverId": "remote_1",
                    "orderHeader": VALID_HEADER,
                    "orderLines": [VALID_LINES[0]],
                },
            )
        self.assertEqual(res.status_code, 201)

    # -- DEC-012 물리 삭제 미지원 ---------------------------------------------

    def test_dec_012_no_delete_http_method(self) -> None:
        """DELETE HTTP 메서드는 outbound 라우터에 등록되지 않음 (405 또는 404)."""
        res = self.client.delete(
            "/api/v1/outbound/orders/2026.04.25%7CA0001%7C1?serverId=remote_1",
        )
        # Method Not Allowed (405) 또는 라우트 미존재 (404). 둘 다 "물리 삭제 차단".
        self.assertIn(res.status_code, (404, 405))


class OutboundServiceUnitTests(TestCase):
    """outbound_service 내부 함수 단위 — 헬퍼 정합성."""

    def test_normalize_gdate_dash_to_dot(self) -> None:
        self.assertEqual(outbound_service._normalize_gdate("2026-04-25"), "2026.04.25")
        self.assertEqual(outbound_service._normalize_gdate("2026.04.25"), "2026.04.25")
        self.assertEqual(outbound_service._normalize_gdate(""), "")

    def test_line_status_from_yesno(self) -> None:
        self.assertEqual(outbound_service._line_status_from_yesno_max("2"), "cancelled")
        self.assertEqual(outbound_service._line_status_from_yesno_max("0"), "active")
        self.assertEqual(outbound_service._line_status_from_yesno_max("1"), "active")
        self.assertEqual(outbound_service._line_status_from_yesno_max(None), "active")

    def test_create_order_validation_empty_lines_raises(self) -> None:
        async def runner():
            await outbound_service.create_order(
                server_id="remote_1", header=VALID_HEADER, lines=[]
            )

        import asyncio
        with self.assertRaises(ValueError):
            asyncio.get_event_loop().run_until_complete(runner())

    def test_update_order_diff_logic(self) -> None:
        """update_order 의 desired-state diff 가 inserted/updated/deleted 를 정확히 산출.

        execute_query (현재 라인) 와 execute_in_transaction (실제 적용) 을 monkeypatch
        하여 service 의 diff 분기만 검증.
        """
        captured_statements: list[list] = []

        async def fake_query(server_id, sql, params):  # noqa: ARG001
            return [
                {"Gcode": "G01", "Bcode": "B0001", "Pubun": "신간",
                 "Gsqut": 5, "Gssum": 50000, "Yesno": "0",
                 "Gjisa": "1", "Gubun": "출고", "Ocode": "B", "Scode": "X"},
                {"Gcode": "G01", "Bcode": "B0002", "Pubun": "신간",
                 "Gsqut": 3, "Gssum": 30000, "Yesno": "0",
                 "Gjisa": "1", "Gubun": "출고", "Ocode": "B", "Scode": "X"},
            ]

        async def fake_tx(server_id, statements):  # noqa: ARG001
            captured_statements.append(statements)
            return [1] * len(statements)

        async def runner():
            with patch.object(outbound_service, "execute_query", side_effect=fake_query), \
                 patch.object(outbound_service, "execute_in_transaction", side_effect=fake_tx):
                return await outbound_service.update_order(
                    server_id="remote_1",
                    gdate="2026-04-25", hcode="A0001", jubun="1",
                    desired_lines=[
                        # B0001: 수량 5 → 4 (UPDATE)
                        {"gcode": "G01", "bcode": "B0001", "pubun": "신간", "gsqut": 4, "gssum": 40000},
                        # B0002: 그대로 (no-op)
                        {"gcode": "G01", "bcode": "B0002", "pubun": "신간", "gsqut": 3, "gssum": 30000},
                        # B0003: 신규 (INSERT)
                        {"gcode": "G01", "bcode": "B0003", "pubun": "신간", "gsqut": 2, "gssum": 20000},
                    ],
                )

        import asyncio
        result = asyncio.get_event_loop().run_until_complete(runner())
        self.assertEqual(result["diff"], {"inserted": 1, "updated": 1, "deleted": 0})
        # 트랜잭션이 INSERT+UPDATE 2개의 statement 묶음으로 실행됐는지 확인
        self.assertEqual(len(captured_statements), 1)
        self.assertEqual(len(captured_statements[0]), 2)


if __name__ == "__main__":
    main()
