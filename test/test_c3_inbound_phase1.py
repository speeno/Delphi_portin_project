"""
C3 입고 접수 — 1차 포팅(phase1) 검증 테스트.

목적
----
도서물류관리프로그램 C3 1차 합격선 (`inbound_receipt.yaml.acceptance_goal`):
  "기존 사용자가 입고 접수를 신규 등록 / 수정 / 취소 / 조회 (CRUD) +
   EUC-KR 인코딩 CSV/TXT 파일을 업로드하여 라인을 일괄 적재할 수 있다."
contract `migration/contracts/inbound_receipt.yaml` v1.0.0 와 1:1 검증.

검증 케이스 (DEC-027 + 1차 in_scope)
- TC-IN-001: 신규 등록 (POST → 201, INSERT × N 트랜잭션 호출)
- TC-IN-002: 중복 라인키 거부 (model 레벨 — bcode 중복 시 ValueError 422)
- TC-IN-003: 소프트 취소 (PATCH → 200, 두 번째는 409 IN_DUPLICATE)
- TC-IN-004: EUC-KR CSV 업로드 (decode 성공 + 헤더별 트랜잭션)
- TC-IN-005: 마감 차단 (PeriodLockedError → 423 IN_PERIOD_LOCKED)
- 부수: TC-IN-006 audit (created/updated/cancelled/imported 4종 모두 기록)
- 부수: DEC-009 RBAC 미수행, DEC-012 물리 삭제 미지원

설계 정합
---------
- C2 outbound 테스트(`test_c2_outbound_phase1.py`)의 monkeypatch 패턴을 그대로 재사용
  (사용자 룰: 신규 헬퍼 금지, 기존 활용가능 코드 우선).
- 사용자 룰: test 폴더에 저장.
"""

from __future__ import annotations

import io
import json
import logging
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
from app.services import inbound_service  # noqa: E402
from app.services.inbound_service import (  # noqa: E402
    ImportDecodeError,
    PeriodLockedError,
)


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


VALID_HEADER = {
    "gdate": "2026-04-25",
    "hcode": "H0001",
    "gcode": "V0001",
    "gjisa": "1",
    "gubun": "입고",
    "ocode": "B",
    "scode": "X",
}
VALID_LINES = [
    {"bcode": "B0001", "pubun": "신간", "gsqut": 5, "gdang": 10000, "grat1": 0.7, "gssum": 35000},
    {"bcode": "B0002", "pubun": "신간", "gsqut": 3, "gdang": 8000, "grat1": 0.7, "gssum": 16800},
]


class CapturingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
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


class C3InboundPhase1Tests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.inbound")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # -- TC-IN-001 신규 등록 --------------------------------------------------

    def test_tc_in_001_create_returns_201_with_receipt_key(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {
                "receipt_key": {
                    "gdate": "2026.04.25", "hcode": "H0001",
                    "gcode": "V0001", "jubun": "120000000001",
                },
                "lines": len(lines),
                "qty": sum(l["gsqut"] for l in lines),
                "amount": sum(l.get("gssum", 0) for l in lines),
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        with patch.object(inbound_service, "create_receipt", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/inbound/receipts",
                json={
                    "serverId": "remote_1",
                    "receiptHeader": VALID_HEADER,
                    "receiptLines": VALID_LINES,
                },
            )

        self.assertEqual(res.status_code, 201, res.text)
        body = res.json()
        self.assertEqual(body["receipt_key"]["hcode"], "H0001")
        self.assertEqual(body["receipt_key"]["gcode"], "V0001")
        self.assertEqual(body["lines"], 2)
        self.assertEqual(body["qty"], 8)
        self.assertEqual(body["amount"], 51800)

    # -- TC-IN-002 중복 라인키 거부 (svc 레벨 ValueError → 422) ----------------

    def test_tc_in_002_create_validation_error_returns_422(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            raise ValueError("duplicate bcode in receipt_lines")

        with patch.object(inbound_service, "create_receipt", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/inbound/receipts",
                json={
                    "serverId": "remote_1",
                    "receiptHeader": VALID_HEADER,
                    "receiptLines": [VALID_LINES[0], VALID_LINES[0]],
                },
            )
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "IN_VALIDATION")

    # -- TC-IN-003 소프트 취소 + 멱등 ------------------------------------------

    def test_tc_in_003_cancel_returns_cancelled(self) -> None:
        async def fake_cancel(*, server_id, gdate, hcode, gcode, jubun):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": gdate, "hcode": hcode, "gcode": gcode, "jubun": jubun},
                "status": "cancelled",
                "cancelled_at": "2026-04-25T05:00:00+00:00",
            }

        with patch.object(inbound_service, "cancel_receipt", side_effect=fake_cancel):
            res = self.client.patch(
                "/api/v1/inbound/receipts/2026.04.25%7CH0001%7CV0001%7C120000000001/cancel"
                "?serverId=remote_1",
                json={"reason": "거래처 요청"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["status"], "cancelled")

    def test_tc_in_003_cancel_idempotent_returns_409(self) -> None:
        async def fake_cancel(*, server_id, gdate, hcode, gcode, jubun):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": gdate, "hcode": hcode, "gcode": gcode, "jubun": jubun},
                "status": "already_cancelled",
                "cancelled_at": "2026-04-25T06:00:00+00:00",
            }

        with patch.object(inbound_service, "cancel_receipt", side_effect=fake_cancel):
            res = self.client.patch(
                "/api/v1/inbound/receipts/2026.04.25%7CH0001%7CV0001%7C120000000001/cancel"
                "?serverId=remote_1",
                json={},
            )
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json()["detail"]["code"], "IN_DUPLICATE")

    # -- TC-IN-004 EUC-KR CSV 업로드 ------------------------------------------

    def test_tc_in_004_import_euckr_csv_imports_lines(self) -> None:
        captured: dict = {}

        async def fake_import(*, server_id, content, dry_run):  # noqa: ARG001
            captured["content"] = content
            captured["dry_run"] = dry_run
            return {"imported": 2, "receipts": 1, "errors": []}

        # EUC-KR 인코딩 CSV (헤더 + 2 라인)
        rows = [
            "gdate,hcode,gcode,bcode,pubun,gsqut,gdang,grat1,gssum,gbigo",
            "2026-04-25,H0001,V0001,B0001,신간,5,10000,0.7,35000,비고1",
            "2026-04-25,H0001,V0001,B0002,신간,3,8000,0.7,16800,비고2",
        ]
        text = "\r\n".join(rows)
        body = text.encode("euc-kr")

        with patch.object(inbound_service, "import_from_file", side_effect=fake_import):
            res = self.client.post(
                "/api/v1/inbound/import?serverId=remote_1",
                files={"file": ("inbound.csv", io.BytesIO(body), "text/csv")},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["imported"], 2)
        self.assertEqual(res.json()["receipts"], 1)
        # 라우터가 실제 EUC-KR 바이트를 그대로 서비스에 전달했는지 확인
        self.assertEqual(captured["content"], body)

    def test_tc_in_004_import_decode_error_returns_400(self) -> None:
        async def fake_import(*, server_id, content, dry_run):  # noqa: ARG001
            raise ImportDecodeError("invalid byte 0xff")

        with patch.object(inbound_service, "import_from_file", side_effect=fake_import):
            res = self.client.post(
                "/api/v1/inbound/import?serverId=remote_1",
                files={"file": ("bad.bin", io.BytesIO(b"\xff\xfe\x00\x00"), "application/octet-stream")},
            )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["detail"]["code"], "IN_IMPORT_DECODE")

    # -- TC-IN-005 마감 차단 → 423 IN_PERIOD_LOCKED ---------------------------

    def test_tc_in_005_period_locked_returns_423(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            raise PeriodLockedError("period locked for gdate=2026.04.25")

        with patch.object(inbound_service, "create_receipt", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/inbound/receipts",
                json={
                    "serverId": "remote_1",
                    "receiptHeader": VALID_HEADER,
                    "receiptLines": VALID_LINES,
                },
            )
        self.assertEqual(res.status_code, 423, res.text)
        self.assertEqual(res.json()["detail"]["code"], "IN_PERIOD_LOCKED")

        # audit failure 1건
        records = self.handler.parsed()
        failures = [r for r in records if r.get("result") == "failure"]
        self.assertGreaterEqual(len(failures), 1)
        self.assertEqual(failures[0]["action"], "created")

    # -- TC-IN-006 감사 로그: 4 액션 모두 ---------------------------------

    def test_tc_in_006_audit_logs_all_actions(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": "2026.04.25", "hcode": "H0001", "gcode": "V0001", "jubun": "1"},
                "lines": 1, "qty": 1, "amount": 100,
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        async def fake_update(*, server_id, gdate, hcode, gcode, jubun, desired_lines, memo):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": gdate, "hcode": hcode, "gcode": gcode, "jubun": jubun},
                "lines": 1, "qty": 1, "amount": 100,
                "updated_at": "2026-04-25T04:00:00+00:00",
                "diff": {"inserted": 0, "updated": 1, "deleted": 0},
            }

        async def fake_cancel(*, server_id, gdate, hcode, gcode, jubun):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": gdate, "hcode": hcode, "gcode": gcode, "jubun": jubun},
                "status": "cancelled",
                "cancelled_at": "2026-04-25T05:00:00+00:00",
            }

        async def fake_import(*, server_id, content, dry_run):  # noqa: ARG001
            return {"imported": 1, "receipts": 1, "errors": []}

        with patch.object(inbound_service, "create_receipt", side_effect=fake_create):
            self.client.post(
                "/api/v1/inbound/receipts",
                json={
                    "serverId": "remote_1",
                    "receiptHeader": VALID_HEADER,
                    "receiptLines": [VALID_LINES[0]],
                },
                headers={"X-Forwarded-For": "203.0.113.5"},
            )
        with patch.object(inbound_service, "update_receipt", side_effect=fake_update):
            self.client.put(
                "/api/v1/inbound/receipts/2026.04.25%7CH0001%7CV0001%7C1?serverId=remote_1",
                json={"receiptLines": [VALID_LINES[0]]},
            )
        with patch.object(inbound_service, "cancel_receipt", side_effect=fake_cancel):
            self.client.patch(
                "/api/v1/inbound/receipts/2026.04.25%7CH0001%7CV0001%7C1/cancel"
                "?serverId=remote_1",
                json={},
            )
        with patch.object(inbound_service, "import_from_file", side_effect=fake_import):
            self.client.post(
                "/api/v1/inbound/import?serverId=remote_1",
                files={"file": ("ok.csv", io.BytesIO(b"gdate,hcode\n2026-04-25,H0001\n"), "text/csv")},
            )

        records = self.handler.parsed()
        actions = {r.get("action") for r in records if r.get("result") == "success"}
        self.assertEqual(
            actions, {"created", "updated", "cancelled", "imported"},
            f"expected all four actions in success audit, got {actions}",
        )
        required = {"timestamp", "gcode", "action", "result", "receipt_key", "client_ip"}
        for rec in records:
            self.assertTrue(
                required.issubset(rec.keys()),
                f"missing required audit fields in {rec}",
            )

    # -- DEC-009 RBAC 미수행 ---------------------------------------------------

    def test_dec_009_no_permission_branch_for_authenticated_user(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {
                "receipt_key": {"gdate": "2026.04.25", "hcode": "H0001", "gcode": "V0001", "jubun": "1"},
                "lines": 1, "qty": 1, "amount": 100,
                "created_at": "2026-04-25T03:00:00+00:00",
            }

        with patch.object(inbound_service, "create_receipt", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/inbound/receipts",
                json={
                    "serverId": "remote_1",
                    "receiptHeader": VALID_HEADER,
                    "receiptLines": [VALID_LINES[0]],
                },
            )
        self.assertEqual(res.status_code, 201)

    # -- DEC-012 물리 삭제 미지원 ---------------------------------------------

    def test_dec_012_no_delete_http_method(self) -> None:
        res = self.client.delete(
            "/api/v1/inbound/receipts/2026.04.25%7CH0001%7CV0001%7C1?serverId=remote_1",
        )
        self.assertIn(res.status_code, (404, 405))


class InboundServiceUnitTests(TestCase):
    """inbound_service 내부 함수 단위 — 헬퍼 정합성 (outbound 와 공유 헬퍼 우회 검증)."""

    def test_normalize_gdate_dash_to_dot(self) -> None:
        # 출고와 동일한 헬퍼를 재사용하므로 기능 동치
        self.assertEqual(inbound_service._normalize_gdate("2026-04-25"), "2026.04.25")
        self.assertEqual(inbound_service._normalize_gdate("2026.04.25"), "2026.04.25")
        self.assertEqual(inbound_service._normalize_gdate(""), "")

    def test_decode_upload_utf8_then_euckr(self) -> None:
        # UTF-8 BOM
        self.assertEqual(
            inbound_service._decode_upload(b"\xef\xbb\xbfHello"), "Hello"
        )
        # EUC-KR 한글
        self.assertEqual(
            inbound_service._decode_upload("입고".encode("euc-kr")), "입고"
        )
        # 잘못된 바이트 — errors='replace' 로 통과해야 함
        result = inbound_service._decode_upload(b"\xff\xfe\x00abc")
        self.assertIn("abc", result)

    def test_parse_import_rows_missing_header_returns_error(self) -> None:
        rows, errs = inbound_service._parse_import_rows("foo,bar\n1,2\n")
        self.assertEqual(rows, [])
        self.assertEqual(len(errs), 1)
        self.assertIn("header columns missing", errs[0]["detail"])

    def test_parse_import_rows_valid_csv(self) -> None:
        text = (
            "gdate,hcode,gcode,bcode,gsqut\n"
            "2026-04-25,H0001,V0001,B0001,5\n"
            "2026-04-25,H0001,V0001,B0002,3\n"
        )
        rows, errs = inbound_service._parse_import_rows(text)
        self.assertEqual(len(rows), 2)
        self.assertEqual(errs, [])
        self.assertEqual(rows[0]["bcode"], "B0001")

    def test_create_receipt_validation_empty_lines_raises(self) -> None:
        async def runner():
            await inbound_service.create_receipt(
                server_id="remote_1", header=VALID_HEADER, memo=None, lines=[]
            )

        import asyncio
        with self.assertRaises(ValueError):
            asyncio.get_event_loop().run_until_complete(runner())


if __name__ == "__main__":
    main()
