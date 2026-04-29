"""DSN-DEC-08 / DEC-051 — 로그인 핸들러 회귀 가드.

문제 패턴 (재발 방지)
---------------------
``POST /api/v1/auth/login`` 의 **성공 경로 꼬리**(``log_login_attempt`` /
``_make_token_pair`` / ``_enrich_user_profile`` / JWT 인코딩) 가 예외를 던지면
글로벌 핸들러가 500 으로 변환되어 사용자에게 노출됐다 (`401` 통합 정책 위배).

실제 트리거 사례
~~~~~~~~~~~~~~~~
1. ``authenticate_user`` 가 반환한 ``user`` dict 의 ``tenant_id`` /
   ``license_keys`` / ``permissions`` 에 비-문자열 (int 등) 이 섞여 ``UserInfo``
   Pydantic 검증이 ``ValidationError`` 를 던짐.
2. ``hit_candidate.priority`` 가 비-숫자 (``"high"`` 등) 라 ``int(...)`` 가
   ``ValueError``.
3. ``_enrich_user_profile`` 안의 ``parent_distributor_label_ko`` 분기가
   외부 룩업 함수가 ``None`` 이 아닌 예외를 던질 때 (이미 try 로 보호됐지만
   주변부에서 새 코드가 추가될 때마다 회귀 가능).
4. ``log_login_attempt`` 핸들러가 디스크 풀 / 권한 오류로 raise — audit 가
   로그인을 깨뜨리는 건 *원인-결과 역전*.

본 테스트의 보호 가드
---------------------
- 위 1·2 케이스를 인위적으로 만들어, 응답이 ``500`` 이 아닌 **한국어 401** 또는
  **정상 200** 으로 끝남을 검증한다.
- 감사 로거가 ``RuntimeError`` 를 raise 하더라도 로그인 응답이 ``500`` 으로
  떨어지지 않음을 검증한다.
- 회귀 시 즉시 적색 — 새 메타데이터 필드가 추가될 때마다 같은 사고가 재발하는
  것을 막는다.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

_STUB_SINGLE = {
    "remote_id": "remote_138",
    "db_name": "app_db",
    "tenant_id": "stub",
    "account_family": "stub",
    "primary_server_label": "",
    "build_role": "",
    "default_account_type": "",
    "tenant_label_kor": "",
    "via": "stub",
    "index_status": "",
}


def _stub_candidates(*_a, **_kw):
    c = dict(_STUB_SINGLE)
    c["candidate_via"] = "stub"
    c["confidence"] = "high"
    c["priority"] = 0
    return [c]


def _stub_single(**_kw):
    return dict(_STUB_SINGLE)


class LoginNoFiveHundredOnDirtyUserDictTests(TestCase):
    """``authenticate_user`` 가 더러운 dict 를 돌려줘도 500 이 나면 안 된다."""

    def setUp(self) -> None:
        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"
        self.client = TestClient(app)

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch("app.services.tenants_directory_service.resolve_login_route", _stub_single)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_dirty_types_in_user_do_not_500(self, mock_auth: AsyncMock) -> None:
        # 운영 시드/오버레이가 int·None 으로 섞여 들어오는 회귀 케이스.
        mock_auth.return_value = {
            "user_id": "tester",
            "user_name": "테스터",
            "server_id": "remote_138",
            "server_label": "AUTH",
            "hcode": "0001",
            "auth_flags": "0001:tester",
            "role": "admin",
            "permissions": ["*", 1, None],  # 비-문자열 섞임
            "license_keys": [1, 2, "k3"],   # 비-문자열 섞임
            "tenant_id": 12345,             # int — UserInfo 는 str|None 을 기대
            "account_family": 999,
            "dist_hcode": 7777,
            "warehouse_menu_tier": "lite",
        }
        r = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "pw"},
        )
        # 핵심: 500 절대 금지. 정책상 현재는 200 (성공 경로)이 맞다.
        self.assertNotEqual(r.status_code, 500, r.text)
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertIn("access_token", body)
        # 잘려도 깨지지 않게: tenant_id 는 str 로 정규화돼야 한다.
        self.assertEqual(body["user"]["tenant_id"], "12345")
        self.assertIn("k3", body["user"]["license_keys"])

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.tenants_directory_service.resolve_login_route", _stub_single)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_non_numeric_priority_does_not_500(
        self, mock_auth: AsyncMock, mock_cands
    ) -> None:
        # priority 가 비-숫자로 들어온 회귀 (라우팅 메타 변경 시 흔한 사고).
        c = dict(_STUB_SINGLE)
        c.update({"candidate_via": "stub", "confidence": "high", "priority": "high"})
        mock_cands.return_value = [c]
        mock_auth.return_value = {
            "user_id": "tester",
            "user_name": "테스터",
            "server_id": "remote_138",
            "server_label": "AUTH",
            "hcode": "0001",
            "auth_flags": "0001:tester",
            "role": "",
            "permissions": [],
        }
        r = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "pw"},
        )
        self.assertNotEqual(r.status_code, 500, r.text)
        self.assertEqual(r.status_code, 200, r.text)


class LoginAuditLoggerFailureIsolationTests(TestCase):
    """감사 로거가 깨져도 로그인 자체는 200/401 로 끝나야 한다."""

    def setUp(self) -> None:
        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"
        self.client = TestClient(app)
        self._broken = _BrokenHandler()
        logging.getLogger("audit.auth").addHandler(self._broken)

    def tearDown(self) -> None:
        logging.getLogger("audit.auth").removeHandler(self._broken)

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch("app.services.tenants_directory_service.resolve_login_route", _stub_single)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_audit_logger_raise_does_not_500_on_success(self, mock_auth: AsyncMock) -> None:
        mock_auth.return_value = {
            "user_id": "tester",
            "user_name": "테스터",
            "server_id": "remote_138",
            "server_label": "AUTH",
            "hcode": "0001",
            "auth_flags": "0001:tester",
            "role": "",
            "permissions": [],
        }
        r = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "pw"},
        )
        self.assertNotEqual(r.status_code, 500, r.text)
        self.assertEqual(r.status_code, 200, r.text)

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch("app.services.tenants_directory_service.resolve_login_route", _stub_single)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_audit_logger_raise_does_not_500_on_failure(self, mock_auth: AsyncMock) -> None:
        mock_auth.return_value = None
        r = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "wrong"},
        )
        self.assertNotEqual(r.status_code, 500, r.text)
        self.assertEqual(r.status_code, 401, r.text)


class _BrokenHandler(logging.Handler):
    """audit.auth 로거에 부착해 항상 emit 시점에 raise — 회귀 시뮬레이션."""

    def emit(self, record: logging.LogRecord) -> None:  # noqa: D401
        raise RuntimeError("simulated audit handler failure")


if __name__ == "__main__":
    main(verbosity=2)
