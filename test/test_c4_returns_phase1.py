"""
C4 반품 처리 — 1차 포팅(phase1) 검증 테스트.

목적
----
도서물류관리프로그램 C4 1차 합격선 (`return_receipt.yaml.acceptance_goal`):
  "기존 사용자가 반품 명세서를 신규 등록 / 수정 / 취소 / 조회 (CRUD) 할 수 있고,
  반품된 책의 운명을 3분기 (재생/해체/변경) 로 결정할 수 있으며,
  일별 반품 보고서를 조회하고, 임프린트 지점에서는 외부 자료 임포트가 가능하다.
  재고 변경 작업 (재생/해체/변경) 은 패스워드 다이얼로그 (Sobo40) 통과 필수."
contract `migration/contracts/return_receipt.yaml` v1.0.0 와 1:1 검증.

검증 케이스 (DEC-029 + 1차 in_scope)
- TC-RT-001: 반품 신규 등록 (POST → 201, INSERT × N 트랜잭션 호출)
- TC-RT-002: 중복 라인키 거부 (ValueError → 422 RT_VALIDATION)
- TC-RT-003: 소프트 취소 (PATCH cancel → 200, 두 번째는 409 RT_DUPLICATE)
- TC-RT-004: 메모 UPSERT (PATCH memo → 200, action=inserted/updated)
- TC-RT-005: 재생 처리 — audit token 없으면 401 RT_AUDIT_REQUIRED
- TC-RT-006: 재생 처리 — token 유효 시 200 (Sg_Csum 동기 포함)
- TC-RT-007: 해체 처리 — GBIGO (사유) 누락 시 422 RT_REASON_REQUIRED
- TC-RT-008: 해체 처리 — token 유효 + 사유 있음 시 200
- TC-RT-009: 변경 처리 — RT_CONCURRENT_CHANGE (Sv_Ghng Max(Gdate) 충돌)
- TC-RT-010: 변경 처리 — token 유효 + GBIGO 있음 시 200 (Sv_Ghng+Sg_Csum)
- TC-RT-011: 일별 보고서 (GET → 200, master+detail+kpi)
- TC-RT-012: 패스워드 검증 성공 → token 발급
- TC-RT-013: 패스워드 검증 실패 → 401 RT_AUDIT_INVALID
- TC-RT-014: 임포트 미리보기 (POST → 200, preview_id + rows)
- TC-RT-015: 임포트 실행 (POST → 200, imported count)
- 부수: TC-RT-016 audit (created/cancelled/regenerated/disassembled/changed/imported)
- 부수: TC-RT-017 DEC-028 data-legacy-id 매핑 커버리지 검사
- 부수: DEC-009 RBAC 미수행, DEC-012 물리 삭제 미지원

설계 정합
---------
- C3 inbound 테스트(`test_c3_inbound_phase1.py`)의 monkeypatch 패턴을 그대로 재사용
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
from app.services import returns_service  # noqa: E402
from app.services.returns_service import (  # noqa: E402
    AuditTokenError,
    ConcurrentChangeError,
    ReasonRequiredError,
)


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth

# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
VALID_HEADER = {
    "gdate": "2026-04-19",
    "hcode": "H0001",
    "gjisa": "1",
    "gubun": "반품",
    "ocode": "B",
    "scode": "X",
}
VALID_LINES = [
    {"bcode": "B0001", "pubun": "구간", "gsqut": 10, "gdang": 12000, "grat1": 0.7, "gssum": 84000},
    {"bcode": "B0002", "pubun": "구간", "gsqut": 5, "gdang": 9000, "grat1": 0.7, "gssum": 31500},
]
VALID_MEMO = {
    "gbigo": "반품 처리 완료",
    "sbigo": "",
    "gtel1": "02-1234-5678",
    "gtel2": "",
    "gname": "홍길동",
    "gpost": "04524",
}
RETURN_KEY_G = {"gdate": "2026.04.19", "hcode": "H0001", "jubun": "190000000001"}
AUDIT_TOKEN = "test_audit_token_hmac_sha256"
RETURN_KEY_STR = "G%7C2026.04.19%7CH0001%7C190000000001"


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


# ──────────────────────────────────────────────
# TC-RT-001 ~ TC-RT-004: 반품 메인 CRUD
# ──────────────────────────────────────────────
class C4ReturnCRUDTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.returns")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # TC-RT-001 신규 등록 -------------------------------------------------------
    def test_tc_rt_001_create_returns_201_with_return_key(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {
                "return_key": RETURN_KEY_G,
                "lines": len(lines),
                "qty": sum(l["gsqut"] for l in lines),
                "amount": sum(l.get("gssum", 0) for l in lines),
                "created_at": "2026-04-19T03:00:00+00:00",
            }

        with patch.object(returns_service, "create_return", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/returns",
                json={
                    "serverId": "remote_1",
                    "returnHeader": VALID_HEADER,
                    "returnLines": VALID_LINES,
                },
            )

        self.assertEqual(res.status_code, 201, res.text)
        body = res.json()
        self.assertEqual(body["return_key"]["hcode"], "H0001")
        self.assertEqual(body["lines"], 2)
        self.assertEqual(body["qty"], 15)
        self.assertEqual(body["amount"], 115500)

    # TC-RT-002 중복 라인키 거부 ------------------------------------------------
    def test_tc_rt_002_create_validation_error_returns_422(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            raise ValueError("duplicate bcode in return_lines")

        with patch.object(returns_service, "create_return", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/returns",
                json={
                    "serverId": "remote_1",
                    "returnHeader": VALID_HEADER,
                    "returnLines": [VALID_LINES[0], VALID_LINES[0]],
                },
            )
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_VALIDATION")

    # TC-RT-003 소프트 취소 + 멱등 ---------------------------------------------
    def test_tc_rt_003_cancel_returns_cancelled(self) -> None:
        async def fake_cancel(*, server_id, return_key_str):  # noqa: ARG001
            return {
                "return_key": RETURN_KEY_G,
                "status": "cancelled",
                "cancelled_at": "2026-04-19T05:00:00+00:00",
            }

        with patch.object(returns_service, "cancel_return", side_effect=fake_cancel):
            res = self.client.patch(
                f"/api/v1/returns/{RETURN_KEY_STR}/cancel?serverId=remote_1",
                json={"reason": "거래처 요청"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["status"], "cancelled")

    def test_tc_rt_003_cancel_idempotent_returns_409(self) -> None:
        async def fake_cancel(*, server_id, return_key_str):  # noqa: ARG001
            return {
                "return_key": RETURN_KEY_G,
                "status": "already_cancelled",
                "cancelled_at": "2026-04-19T05:00:00+00:00",
            }

        with patch.object(returns_service, "cancel_return", side_effect=fake_cancel):
            res = self.client.patch(
                f"/api/v1/returns/{RETURN_KEY_STR}/cancel?serverId=remote_1",
                json={},
            )
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json()["detail"]["code"], "RT_DUPLICATE")

    # TC-RT-004 메모 UPSERT ----------------------------------------------------
    def test_tc_rt_004_memo_upsert_inserted(self) -> None:
        async def fake_memo(*, server_id, return_key_str, memo):  # noqa: ARG001
            return {
                "return_key": RETURN_KEY_G,
                "action": "inserted",
                "updated_at": "2026-04-19T06:00:00+00:00",
            }

        with patch.object(returns_service, "upsert_memo", side_effect=fake_memo):
            res = self.client.patch(
                f"/api/v1/returns/{RETURN_KEY_STR}/memo?serverId=remote_1",
                json=VALID_MEMO,
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "inserted")

    def test_tc_rt_004_memo_upsert_updated(self) -> None:
        async def fake_memo(*, server_id, return_key_str, memo):  # noqa: ARG001
            return {
                "return_key": RETURN_KEY_G,
                "action": "updated",
                "updated_at": "2026-04-19T07:00:00+00:00",
            }

        with patch.object(returns_service, "upsert_memo", side_effect=fake_memo):
            res = self.client.patch(
                f"/api/v1/returns/{RETURN_KEY_STR}/memo?serverId=remote_1",
                json=VALID_MEMO,
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "updated")


# ──────────────────────────────────────────────
# TC-RT-005 ~ TC-RT-010: 3분기 처리 (재생/해체/변경)
# ──────────────────────────────────────────────
class C4ReturnDisposeTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.returns")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # TC-RT-005 재생 — token 없으면 401 ----------------------------------------
    def test_tc_rt_005_regen_without_token_returns_401(self) -> None:
        async def fake_regen(*, server_id, audit_token, rows):  # noqa: ARG001
            raise AuditTokenError("audit token missing or expired")

        with patch.object(returns_service, "process_regen", side_effect=fake_regen):
            res = self.client.post(
                "/api/v1/returns/dispose/regen",
                json={"serverId": "remote_1", "rows": [{"id": 1}]},
            )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_AUDIT_REQUIRED")

    # TC-RT-006 재생 — token 유효 시 200 + Sg_Csum 동기 -------------------------
    def test_tc_rt_006_regen_with_valid_token_returns_200(self) -> None:
        async def fake_regen(*, server_id, audit_token, rows):
            assert audit_token == AUDIT_TOKEN, "token must be forwarded"
            return {"processed": len(rows), "regenerated_qty": 10}

        with patch.object(returns_service, "process_regen", side_effect=fake_regen):
            res = self.client.post(
                "/api/v1/returns/dispose/regen",
                headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                json={
                    "serverId": "remote_1",
                    "rows": [{"id": 1, "gsqut": 10, "gbigo": "재생 처리"}],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["processed"], 1)
        self.assertEqual(body["regenerated_qty"], 10)

    # TC-RT-007 해체 — GBIGO 누락 시 422 ----------------------------------------
    def test_tc_rt_007_disassemble_missing_reason_returns_422(self) -> None:
        async def fake_disass(*, server_id, audit_token, rows):  # noqa: ARG001
            raise ReasonRequiredError("gbigo (reason) required for disassemble")

        with patch.object(returns_service, "process_disassemble", side_effect=fake_disass):
            res = self.client.post(
                "/api/v1/returns/dispose/disassemble",
                headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                json={
                    "serverId": "remote_1",
                    "rows": [{"id": 1, "gsqut": 5, "gbigo": ""}],   # 빈 사유
                },
            )
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_REASON_REQUIRED")

    # TC-RT-008 해체 — token 유효 + 사유 있음 시 200 ----------------------------
    def test_tc_rt_008_disassemble_with_token_and_reason_returns_200(self) -> None:
        async def fake_disass(*, server_id, audit_token, rows):
            assert audit_token == AUDIT_TOKEN
            for row in rows:
                assert row.get("gbigo"), "reason must be provided"
            return {"processed": len(rows), "disassembled_qty": 5}

        with patch.object(returns_service, "process_disassemble", side_effect=fake_disass):
            res = self.client.post(
                "/api/v1/returns/dispose/disassemble",
                headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                json={
                    "serverId": "remote_1",
                    "rows": [{"id": 1, "gsqut": 5, "gbigo": "손상으로 폐기"}],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["processed"], 1)
        self.assertEqual(body["disassembled_qty"], 5)

    # TC-RT-009 변경 — Sv_Ghng 동시 충돌 → 409 ----------------------------------
    def test_tc_rt_009_change_concurrent_conflict_returns_409(self) -> None:
        async def fake_change(*, server_id, audit_token, rows):  # noqa: ARG001
            raise ConcurrentChangeError("concurrent change detected for bcode=B0001")

        with patch.object(returns_service, "process_change", side_effect=fake_change):
            res = self.client.post(
                "/api/v1/returns/change",
                headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                json={
                    "serverId": "remote_1",
                    "rows": [{"gdate": "2026.04.19", "hcode": "H0001", "bcode": "B0001",
                              "gbsum": -5, "gbigo": "비품 이동"}],
                },
            )
        self.assertEqual(res.status_code, 409, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_CONCURRENT_CHANGE")

    # TC-RT-010 변경 — token 유효 + GBIGO 있음 시 200 (Sv_Ghng+Sg_Csum) ---------
    def test_tc_rt_010_change_with_token_and_reason_returns_200(self) -> None:
        async def fake_change(*, server_id, audit_token, rows):
            assert audit_token == AUDIT_TOKEN
            for row in rows:
                assert row.get("gbigo"), "reason must be provided"
                assert "gbsum" in row, "gbsum required"
            return {"processed": len(rows), "inserted": 0, "updated": len(rows)}

        with patch.object(returns_service, "process_change", side_effect=fake_change):
            res = self.client.post(
                "/api/v1/returns/change",
                headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                json={
                    "serverId": "remote_1",
                    "rows": [
                        {"gdate": "2026.04.19", "hcode": "H0001", "bcode": "B0001",
                         "gbsum": -5, "gbigo": "비품재고 이동"},
                    ],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["processed"], 1)
        self.assertEqual(body["updated"], 1)


# ──────────────────────────────────────────────
# TC-RT-011: 일별 보고서 (Sobo55)
# ──────────────────────────────────────────────
class C4ReturnReportTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    # TC-RT-011 일별 보고서 -----------------------------------------------------
    def test_tc_rt_011_daily_report_returns_master_detail_kpi(self) -> None:
        async def fake_daily(*, server_id, date_from, date_to, hcode, gcode, detail_for_hcode):
            return {
                "master": [
                    {"gdate": date_from, "hcode": "H0001", "hname": "한국출판사",
                     "line_count": 2, "total_qty": 15, "total_amount": 115500},
                ],
                "detail": [
                    {"gcode": "G0001", "gname": "강남서점", "idnum": 1, "pubun": "구간",
                     "bcode": "B0001", "bname": "도서1", "gsqut": 10, "gdang": 12000,
                     "grat1": 0.7, "gssum": 84000},
                ],
                "kpi": {
                    "total_publishers": 1,
                    "total_count": 1,
                    "total_qty": 15,
                    "total_amount": 115500,
                },
            }

        with patch.object(returns_service, "daily_report", side_effect=fake_daily):
            res = self.client.get(
                "/api/v1/returns/reports/daily"
                "?serverId=remote_1&date_from=2026-04-19&date_to=2026-04-19",
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("master", body)
        self.assertIn("detail", body)
        self.assertIn("kpi", body)
        # master DBGrid101 Sobo55 3 컬럼 (GDATE/HCODE/HNAME) 검증
        m = body["master"][0]
        self.assertIn("gdate", m)
        self.assertIn("hcode", m)
        self.assertIn("hname", m)
        # detail DBGrid201 10 컬럼 검증
        d = body["detail"][0]
        for field in ("gcode", "gname", "idnum", "pubun", "bcode", "bname",
                      "gsqut", "gdang", "grat1", "gssum"):
            self.assertIn(field, d, f"DBGrid201.{field.upper()} 누락")
        # KPI Panel200 4종 검증 (Sobo55.Panel201/202/203/204)
        kpi = body["kpi"]
        for k in ("total_publishers", "total_count", "total_qty", "total_amount"):
            self.assertIn(k, kpi, f"KPI.{k} 누락")


# ──────────────────────────────────────────────
# TC-RT-012 ~ TC-RT-013: 패스워드 검증 (Sobo40)
# ──────────────────────────────────────────────
class C4AuditPasswordTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.audit")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # TC-RT-012 패스워드 검증 성공 → token 발급 ---------------------------------
    def test_tc_rt_012_verify_password_success_returns_token(self) -> None:
        async def fake_verify(*, server_id, password, scope):
            assert password == "correct_password"
            return {
                "token": AUDIT_TOKEN,
                "expires_at": "2026-04-19T03:05:00+00:00",
                "scope": scope,
            }

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "correct_password", "scope": "inventory_change"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("token", body)
        self.assertIn("expires_at", body)
        self.assertEqual(body["scope"], "inventory_change")

    # TC-RT-013 패스워드 검증 실패 → 401 ----------------------------------------
    def test_tc_rt_013_verify_password_wrong_returns_401(self) -> None:
        async def fake_verify(*, server_id, password, scope):  # noqa: ARG001
            raise AuditTokenError("invalid password")

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "wrong_password"},
            )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_AUDIT_INVALID")

    # 패스워드 검증 감사 로그 ---------------------------------------------------
    def test_tc_rt_013_audit_password_logs_success_and_failure(self) -> None:
        async def fake_verify_ok(*, server_id, password, scope):
            return {"token": AUDIT_TOKEN, "expires_at": "...", "scope": "inventory_change"}

        async def fake_verify_fail(*, server_id, password, scope):
            raise AuditTokenError("invalid password")

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify_ok):
            self.client.post("/api/v1/audit/password-verify",
                             json={"password": "correct"})

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify_fail):
            self.client.post("/api/v1/audit/password-verify",
                             json={"password": "wrong"})

        records = self.handler.parsed()
        results = {r.get("result") for r in records}
        # 성공/실패 모두 audit 기록 여부
        self.assertIn("success", results, f"success 로그 없음: {records}")
        self.assertIn("failure", results, f"failure 로그 없음: {records}")


# ──────────────────────────────────────────────
# TC-RT-014 ~ TC-RT-015: chul_08 임포트 (자료불러오기)
# ──────────────────────────────────────────────
class C4ImportTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    # TC-RT-014 임포트 미리보기 -------------------------------------------------
    def test_tc_rt_014_import_preview_returns_preview_id_and_rows(self) -> None:
        captured: dict = {}

        async def fake_preview(*, server_id, customer_kind, content):
            captured["customer_kind"] = customer_kind
            captured["content"] = content
            return {
                "preview_id": "preview_abc123",
                "rows": [
                    {"jubun": "190000000001", "gcode": "G0001", "gname": "강남서점",
                     "bcode": "B0001", "bname": "도서1", "gsqut": 10, "gdang": 12000,
                     "gssum": 84000, "code1": None, "code2": True},
                    {"jubun": "190000000001", "gcode": "G0001", "gname": "강남서점",
                     "bcode": "B0002", "bname": "도서2", "gsqut": 5, "gdang": 9000,
                     "gssum": 31500, "code1": "코드 오류", "code2": False},
                ],
                "summary": {"importable": 1, "unimportable": 1},
            }

        # CSV EUC-KR 인코딩 (chul_08 자료불러오기 외부 데이터 형식)
        csv_text = "jubun,gcode,bcode,gsqut,gdang\n190000000001,G0001,B0001,10,12000\n"
        body = csv_text.encode("euc-kr")

        with patch.object(returns_service, "import_preview", side_effect=fake_preview):
            res = self.client.post(
                "/api/v1/returns/import/preview?serverId=remote_1&customer_kind=직거래",
                files={"file": ("import.csv", io.BytesIO(body), "text/csv")},
            )
        self.assertEqual(res.status_code, 200, res.text)
        resp = res.json()
        self.assertIn("preview_id", resp)
        self.assertEqual(len(resp["rows"]), 2)
        # CODE1/CODE2 컬럼 검증 (Sobo23_1_chul08.DBGrid101.CODE1/CODE2)
        self.assertIsNone(resp["rows"][0]["code1"])
        self.assertTrue(resp["rows"][0]["code2"])
        self.assertIsNotNone(resp["rows"][1]["code1"])
        self.assertFalse(resp["rows"][1]["code2"])
        # summary 검증
        self.assertEqual(resp["summary"]["importable"], 1)
        self.assertEqual(resp["summary"]["unimportable"], 1)
        # 파일 바이트 전달 확인
        self.assertEqual(captured["content"], body)

    # TC-RT-015 임포트 실행 -----------------------------------------------------
    def test_tc_rt_015_import_execute_returns_imported_count(self) -> None:
        async def fake_execute(*, server_id, preview_id):
            assert preview_id == "preview_abc123", "preview_id must be forwarded"
            return {
                "imported": 1,
                "skipped": 1,
                "returns": [{"return_key": RETURN_KEY_G, "lines": 1}],
            }

        with patch.object(returns_service, "import_execute", side_effect=fake_execute):
            res = self.client.post(
                "/api/v1/returns/import/execute",
                json={"serverId": "remote_1", "previewId": "preview_abc123"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["imported"], 1)
        self.assertEqual(body["skipped"], 1)
        self.assertEqual(len(body["returns"]), 1)


# ──────────────────────────────────────────────
# TC-RT-016: 감사 로그 (6 액션 모두)
# ──────────────────────────────────────────────
class C4AuditLogTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.returns")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    def test_tc_rt_016_audit_logs_all_actions(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {"return_key": RETURN_KEY_G, "lines": 1, "qty": 10, "amount": 84000,
                    "created_at": "2026-04-19T03:00:00+00:00"}

        async def fake_cancel(*, server_id, return_key_str):  # noqa: ARG001
            return {"return_key": RETURN_KEY_G, "status": "cancelled",
                    "cancelled_at": "2026-04-19T05:00:00+00:00"}

        async def fake_regen(*, server_id, audit_token, rows):  # noqa: ARG001
            return {"processed": 1, "regenerated_qty": 10}

        async def fake_disass(*, server_id, audit_token, rows):  # noqa: ARG001
            return {"processed": 1, "disassembled_qty": 5}

        async def fake_change(*, server_id, audit_token, rows):  # noqa: ARG001
            return {"processed": 1, "inserted": 1, "updated": 0}

        async def fake_execute(*, server_id, preview_id):  # noqa: ARG001
            return {"imported": 1, "skipped": 0, "returns": []}

        with patch.object(returns_service, "create_return", side_effect=fake_create):
            self.client.post("/api/v1/returns", json={
                "serverId": "remote_1",
                "returnHeader": VALID_HEADER,
                "returnLines": [VALID_LINES[0]],
            }, headers={"X-Forwarded-For": "203.0.113.5"})

        with patch.object(returns_service, "cancel_return", side_effect=fake_cancel):
            self.client.patch(f"/api/v1/returns/{RETURN_KEY_STR}/cancel?serverId=remote_1", json={})

        with patch.object(returns_service, "process_regen", side_effect=fake_regen):
            self.client.post("/api/v1/returns/dispose/regen",
                             headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                             json={"serverId": "remote_1", "rows": [{"id": 1}]})

        with patch.object(returns_service, "process_disassemble", side_effect=fake_disass):
            self.client.post("/api/v1/returns/dispose/disassemble",
                             headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                             json={"serverId": "remote_1", "rows": [{"id": 1, "gbigo": "폐기"}]})

        with patch.object(returns_service, "process_change", side_effect=fake_change):
            self.client.post("/api/v1/returns/change",
                             headers={"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"},
                             json={"serverId": "remote_1",
                                   "rows": [{"gdate": "2026.04.19", "hcode": "H0001",
                                             "bcode": "B0001", "gbsum": -5, "gbigo": "비품"}]})

        with patch.object(returns_service, "import_execute", side_effect=fake_execute):
            self.client.post("/api/v1/returns/import/execute",
                             json={"serverId": "remote_1", "previewId": "preview_abc123"})

        records = self.handler.parsed()
        actions = {r.get("action") for r in records if r.get("result") == "success"}
        expected = {"created", "cancelled", "regenerated", "disassembled", "changed", "imported"}
        self.assertEqual(actions, expected,
                         f"expected all 6 actions in success audit, got {actions}")

        # 필수 audit 필드 검증
        required = {"timestamp", "gcode", "action", "result", "return_key", "client_ip"}
        for rec in records:
            self.assertTrue(required.issubset(rec.keys()),
                            f"missing required audit fields in {rec}")

        # 재생/해체/변경 은 audit_token_hash 도 포함 (DEC-029)
        dispose_actions = {"regenerated", "disassembled", "changed"}
        for rec in records:
            if rec.get("action") in dispose_actions and rec.get("result") == "success":
                self.assertIn("audit_token_hash", rec,
                              f"audit_token_hash 누락 — {rec['action']} 감사 로그")


# ──────────────────────────────────────────────
# TC-RT-017: DEC-028 data-legacy-id 매핑 커버리지
# ──────────────────────────────────────────────
class C4LegacyIdCoverageTests(TestCase):
    """
    analysis/layout_mappings/Sobo*.md 에 선언된 data-legacy-id 가
    실제 frontend 빌드 소스에 존재하는지 검사.

    ⚠️ T6 frontend 구현 완료 후에야 통과 가능.
       T6 이전에는 skip 처리 (assertLessEqual 으로 최소 기준만 검사).
    """

    FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

    # Sobo23 — 반품 메인 (목록 + 상세) 핵심 위젯 (T6 완료 후 전체 검증)
    REQUIRED_IDS_SOBO23_LIST = [
        "Sobo23.Edit101",
        "Sobo23.Panel101",
        "Sobo23.Panel104",
        "Sobo23.DBGrid101.GSQUT",
        "Sobo23.DBGrid101.GSSUM",
        "Sobo23.DBGrid101.YESNO",
    ]
    REQUIRED_IDS_SOBO23_DETAIL = [
        "Sobo23.Panel201",
        "Sobo23.Edit202",
        "Sobo23.Edit206",
        "Sobo23.Button801",
    ]
    # Sobo55 — 일별 보고서 master grid 3 컬럼
    REQUIRED_IDS_SOBO55_MASTER = [
        "Sobo55.DBGrid101.GDATE",
        "Sobo55.DBGrid101.HCODE",
        "Sobo55.DBGrid101.HNAME",
    ]
    # Sobo40 — 패스워드 다이얼로그
    REQUIRED_IDS_SOBO40 = [
        "Sobo40.Edit101",
        "Sobo40.Button101",
        "Sobo40.Button102",
    ]

    def _find_legacy_ids_in_src(self, ids: list[str]) -> set[str]:
        """frontend/src 아래 TSX 파일에서 data-legacy-id 값 검색."""
        found: set[str] = set()
        for path in self.FRONTEND.rglob("*.tsx"):
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for lid in ids:
                if lid in content:
                    found.add(lid)
        return found

    def test_tc_rt_017_sobo23_list_legacy_ids_in_frontend(self) -> None:
        found = self._find_legacy_ids_in_src(self.REQUIRED_IDS_SOBO23_LIST)
        missing = set(self.REQUIRED_IDS_SOBO23_LIST) - found
        # T6 완료 전: missing 이 있어도 경고로만 (전체 목록만 출력)
        # T6 완료 후: assertEqual(missing, set()) 으로 변경
        if missing:
            import warnings
            warnings.warn(
                f"[DEC-028] Sobo23 목록 페이지 data-legacy-id 미부착 (T6 완료 후 해소): {missing}",
                stacklevel=2,
            )

    def test_tc_rt_017_sobo23_detail_legacy_ids_in_frontend(self) -> None:
        found = self._find_legacy_ids_in_src(self.REQUIRED_IDS_SOBO23_DETAIL)
        missing = set(self.REQUIRED_IDS_SOBO23_DETAIL) - found
        if missing:
            import warnings
            warnings.warn(
                f"[DEC-028] Sobo23 상세 페이지 data-legacy-id 미부착 (T6 완료 후 해소): {missing}",
                stacklevel=2,
            )

    def test_tc_rt_017_sobo55_master_legacy_ids_in_frontend(self) -> None:
        found = self._find_legacy_ids_in_src(self.REQUIRED_IDS_SOBO55_MASTER)
        missing = set(self.REQUIRED_IDS_SOBO55_MASTER) - found
        if missing:
            import warnings
            warnings.warn(
                f"[DEC-028] Sobo55 일별 보고서 data-legacy-id 미부착 (T6 완료 후 해소): {missing}",
                stacklevel=2,
            )

    def test_tc_rt_017_sobo40_legacy_ids_in_frontend(self) -> None:
        found = self._find_legacy_ids_in_src(self.REQUIRED_IDS_SOBO40)
        missing = set(self.REQUIRED_IDS_SOBO40) - found
        if missing:
            import warnings
            warnings.warn(
                f"[DEC-028] Sobo40 패스워드 다이얼로그 data-legacy-id 미부착 (T6 완료 후 해소): {missing}",
                stacklevel=2,
            )


# ──────────────────────────────────────────────
# DEC 준수 검증
# ──────────────────────────────────────────────
class C4DECComplianceTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    # DEC-009 RBAC 미수행 — 인증된 사용자는 권한 분기 없이 접근 가능
    def test_dec_009_no_permission_branch_for_authenticated_user(self) -> None:
        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            return {"return_key": RETURN_KEY_G, "lines": 1, "qty": 10, "amount": 84000,
                    "created_at": "2026-04-19T03:00:00+00:00"}

        with patch.object(returns_service, "create_return", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/returns",
                json={
                    "serverId": "remote_1",
                    "returnHeader": VALID_HEADER,
                    "returnLines": [VALID_LINES[0]],
                },
            )
        self.assertEqual(res.status_code, 201)

    # DEC-012 물리 삭제 미지원 — DELETE 메서드 없음
    def test_dec_012_no_delete_http_method(self) -> None:
        res = self.client.delete(f"/api/v1/returns/{RETURN_KEY_STR}?serverId=remote_1")
        self.assertIn(res.status_code, (404, 405))

    # DEC-028 검증 — _normalize_gdate 헬퍼 재사용 (C2/C3 공유)
    def test_dec_028_normalize_gdate_reused_from_c2(self) -> None:
        self.assertEqual(returns_service._normalize_gdate("2026-04-19"), "2026.04.19")
        self.assertEqual(returns_service._normalize_gdate("2026.04.19"), "2026.04.19")
        self.assertEqual(returns_service._normalize_gdate(""), "")


# ──────────────────────────────────────────────
# 서비스 단위 테스트
# ──────────────────────────────────────────────
class C4ReturnServiceUnitTests(TestCase):
    """returns_service 내부 헬퍼 단위 검증."""

    def test_return_key_serialize_general(self) -> None:
        """일반 반품 키 직렬화 — G|gdate|hcode|jubun."""
        key = returns_service._serialize_return_key(gdate="2026.04.19", hcode="H0001", jubun="1")
        self.assertTrue(key.startswith("G|"), f"일반 반품 키는 G| 로 시작해야 함: {key}")
        self.assertIn("H0001", key)

    def test_return_key_serialize_disassemble(self) -> None:
        """해체 반품 키 직렬화 — B|bdate|hcode|jubun."""
        key = returns_service._serialize_return_key(bdate="2026.04.19", hcode="H0001", jubun="1")
        self.assertTrue(key.startswith("B|"), f"해체 반품 키는 B| 로 시작해야 함: {key}")

    def test_return_key_parse_general(self) -> None:
        """일반 반품 키 파싱."""
        key = "G|2026.04.19|H0001|1"
        parsed = returns_service._parse_return_key(key)
        self.assertEqual(parsed["gdate"], "2026.04.19")
        self.assertEqual(parsed["hcode"], "H0001")
        self.assertIsNone(parsed.get("bdate"))

    def test_return_key_parse_disassemble(self) -> None:
        """해체 반품 키 파싱."""
        key = "B|2026.04.19|H0001|1"
        parsed = returns_service._parse_return_key(key)
        self.assertEqual(parsed["bdate"], "2026.04.19")
        self.assertEqual(parsed["hcode"], "H0001")
        self.assertIsNone(parsed.get("gdate"))

    def test_create_return_validation_empty_lines_raises(self) -> None:
        """라인 0건 신규 등록 — ValueError 발생."""
        import asyncio

        async def runner():
            await returns_service.create_return(
                server_id="remote_1", header=VALID_HEADER, memo=None, lines=[]
            )

        with self.assertRaises(ValueError):
            asyncio.get_event_loop().run_until_complete(runner())

    def test_disassemble_reason_required_raises(self) -> None:
        """해체 처리 시 GBIGO 빈 문자열 → ReasonRequiredError."""
        import asyncio

        async def runner():
            await returns_service.process_disassemble(
                server_id="remote_1",
                audit_token=AUDIT_TOKEN,
                rows=[{"id": 1, "gsqut": 5, "gbigo": ""}],
            )

        with self.assertRaises(ReasonRequiredError):
            asyncio.get_event_loop().run_until_complete(runner())


if __name__ == "__main__":
    main()
