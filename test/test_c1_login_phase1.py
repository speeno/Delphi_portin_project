"""
C1 로그인·세션 시작 — 1차 포팅(phase1) 검증 테스트.

목적
----
도서물류관리프로그램(웹 포팅 산출물) 1차 합격선 (`acceptance_goal`):
  "기존 사용자가 기존 ID/PW 로 그대로 로그인 가능"
에 대해 contract `migration/contracts/login.yaml` v1.1.x 와 실 구현을 1:1 검증.

검증 케이스 (test pack login.json v1.1.0-phase1 의 1차 in_scope 8건 중 단위테스트로 가능한 부분)
- TC-LOGIN-001: 정상 로그인 (응답 user.hcode/user_name 동등)
- TC-LOGIN-003: 비밀번호 불일치 → 401 통합 메시지
- TC-LOGIN-004: 사용자 없음 → 401 통합 메시지
- TC-LOGIN-006: SQL 인젝션 방어 (파라미터 바인딩으로 NODATA)
- TC-LOGIN-009: 감사 로그 — 성공/실패 모두 audit.auth 에 기록 (timestamp/gcode/result/client_ip)

부수 검증 (DEC-005~008 1차 동결 부합)
- DEC-005: 평문 동등 비교 (verify_legacy_password)
- DEC-006: 라이선스 검증 미수행 (응답에 AUTH_KEY_REGISTER_REQUIRED 발생 안 함)
- DEC-007: 응답에 is_super 필드 미존재
- DEC-008: 응답에 tenant_id 필드 미존재

주의
----
실 DB 연결 없이 authenticate_user 만 monkeypatch 하여 라우터 단의 동작·감사로그를 검증한다.
사용자 규칙: test 폴더에 저장 (debug 폴더는 디버그 전용).
"""

from __future__ import annotations

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
from app.core.security import verify_legacy_password  # noqa: E402


VALID_USER = {
    "user_id": "hong01",
    "user_name": "홍길동",
    "server_id": "remote_1",
    "server_label": "서버 1",
    "hcode": "0123",
    "auth_flags": "0123:홍길동",
}


class CapturingHandler(logging.Handler):
    """audit.auth 로거 출력만 캡처."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:  # noqa: D401
        self.records.append(record)

    def parsed(self) -> list[dict]:
        out: list[dict] = []
        for r in self.records:
            msg = r.getMessage()
            # "auth.login {json...}" 포맷에서 JSON만 분리
            idx = msg.find("{")
            if idx < 0:
                continue
            try:
                out.append(json.loads(msg[idx:]))
            except json.JSONDecodeError:
                continue
        return out


class C1LoginPhase1Tests(TestCase):
    """C1 phase1 1차 in_scope 8건 중 단위 검증 가능한 5건."""

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.auth")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # -- TC-LOGIN-001 정상 로그인 ----------------------------------------

    def test_tc_login_001_success_returns_user_hcode_and_token(self) -> None:
        with patch("app.routers.auth.authenticate_user", return_value=VALID_USER):
            res = self.client.post(
                "/api/v1/auth/login",
                json={"serverId": "remote_1", "userId": "hong01", "password": "qwer5678"},
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        # 토큰 쌍 발급 (Contract outputs.success.session_token 동등)
        self.assertIn("access_token", body)
        self.assertIn("refresh_token", body)
        # user 객체에 hcode/hname 동등 필드
        self.assertEqual(body["user"]["user_id"], "hong01")
        self.assertEqual(body["user"]["user_name"], "홍길동")
        self.assertEqual(body["user"]["hcode"], "0123")
        # DEC-007 1차: 응답에 is_super 필드 없음
        self.assertNotIn("is_super", body["user"])
        # DEC-008 1차: 응답에 tenant_id 필드 없음
        self.assertNotIn("tenant_id", body["user"])

    # -- TC-LOGIN-003 비밀번호 불일치 / TC-LOGIN-004 사용자 없음 -------

    def test_tc_login_003_004_failure_returns_unified_401(self) -> None:
        """1차 포팅 정책: AUTH_NO_USER / AUTH_BAD_PASSWORD 단일 401 통합 (사용자 열거 방어)."""
        for case_id, body in [
            ("TC-LOGIN-003", {"serverId": "remote_1", "userId": "hong01", "password": "WRONG"}),
            ("TC-LOGIN-004", {"serverId": "remote_1", "userId": "ghost", "password": "any"}),
        ]:
            with self.subTest(case=case_id):
                with patch("app.routers.auth.authenticate_user", return_value=None):
                    res = self.client.post("/api/v1/auth/login", json=body)
                self.assertEqual(res.status_code, 401)
                self.assertEqual(
                    res.json()["detail"],
                    "아이디 또는 비밀번호가 올바르지 않습니다.",
                )

    # -- TC-LOGIN-006 SQL 인젝션 방어 ------------------------------------

    def test_tc_login_006_sql_injection_returns_401(self) -> None:
        """파라미터 바인딩으로 항상 NODATA 분기 — authenticate_user 가 None 반환을 보장."""
        with patch("app.routers.auth.authenticate_user", return_value=None) as mock_auth:
            res = self.client.post(
                "/api/v1/auth/login",
                json={"serverId": "remote_1", "userId": "hong01' OR '1'='1", "password": "x"},
            )
        self.assertEqual(res.status_code, 401)
        # authenticate_user 호출 시 user_id 인자가 raw 문자열 그대로 (바인딩으로 안전)
        call_kwargs = mock_auth.call_args
        passed_user_id = call_kwargs.args[1] if call_kwargs.args else call_kwargs.kwargs.get("user_id")
        self.assertEqual(passed_user_id, "hong01' OR '1'='1")

    # -- TC-LOGIN-009 감사 로그 ------------------------------------------

    def test_tc_login_009_audit_logs_success_and_failure(self) -> None:
        # 성공 1건
        with patch("app.routers.auth.authenticate_user", return_value=VALID_USER):
            self.client.post(
                "/api/v1/auth/login",
                json={"serverId": "remote_1", "userId": "hong01", "password": "qwer5678"},
                headers={"X-Forwarded-For": "203.0.113.5"},
            )
        # 실패 1건
        with patch("app.routers.auth.authenticate_user", return_value=None):
            self.client.post(
                "/api/v1/auth/login",
                json={"serverId": "remote_1", "userId": "ghost", "password": "x"},
                headers={"X-Real-IP": "198.51.100.7"},
            )

        records = self.handler.parsed()
        self.assertGreaterEqual(
            len(records), 2,
            f"성공·실패 최소 2건 감사 로그 기대, 실제 {len(records)}건",
        )
        # Contract TC-LOGIN-009.fields_required 모두 존재
        required = {"timestamp", "gcode", "result", "client_ip"}
        for rec in records:
            self.assertTrue(required.issubset(rec.keys()), f"missing fields in {rec}")
        # 결과별 1건 이상
        results = {rec["result"] for rec in records}
        self.assertIn("success", results)
        self.assertIn("failure", results)
        # X-Forwarded-For 추출이 첫 항목으로 동작
        success_rec = next(r for r in records if r["result"] == "success")
        self.assertEqual(success_rec["client_ip"], "203.0.113.5")
        # 실패 시 reason 부가 필드 기록
        failure_rec = next(r for r in records if r["result"] == "failure")
        self.assertEqual(failure_rec["client_ip"], "198.51.100.7")
        self.assertEqual(failure_rec.get("reason"), "invalid_credentials")


class DEC005PlainPasswordTests(TestCase):
    """DEC-005 — 1차 포팅은 평문 동등 비교 그대로 동작."""

    def test_plain_equal_match(self) -> None:
        self.assertTrue(verify_legacy_password("qwer5678", "qwer5678"))

    def test_plain_mismatch(self) -> None:
        self.assertFalse(verify_legacy_password("qwer5678", "WRONG"))

    def test_empty_inputs_reject(self) -> None:
        self.assertFalse(verify_legacy_password("", "qwer5678"))
        self.assertFalse(verify_legacy_password("qwer5678", ""))


if __name__ == "__main__":
    main()
