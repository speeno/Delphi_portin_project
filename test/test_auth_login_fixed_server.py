"""DEC-051 — 로그인 인증 서버 단일화(`BLS_AUTH_SERVER_ID`) + JWT sid = 검증 성공 서버."""

from __future__ import annotations

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
from app.core.security import decode_token  # noqa: E402

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


class FixedAuthServerTests(TestCase):
    """`/api/v1/auth/login` 은 ``serverId`` 입력을 무시하고 라우팅 후보로 검증한다."""

    def setUp(self) -> None:
        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch(
        "app.services.tenants_directory_service.resolve_login_route",
        lambda **kw: dict(_STUB_SINGLE),
    )
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_login_ignores_serverId_and_uses_env(self, mock_auth: AsyncMock) -> None:
        """입력 ``serverId`` 는 무시되며, 스텁 라우트의 서버로 ``authenticate_user`` 가 호출된다."""
        mock_auth.return_value = {
            "user_id": "tester",
            "user_name": "테스터",
            "server_id": "remote_138",
            "server_label": "AUTH",
            "hcode": "0001",
            "auth_flags": "0001:tester",
            "role": "admin",
            "permissions": ["*"],
        }

        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"serverId": "remote_999_should_be_ignored", "userId": "tester", "password": "pw"},
        )
        self.assertEqual(r.status_code, 200, r.text)

        mock_auth.assert_awaited()
        called_server_id = mock_auth.await_args.args[0]
        self.assertEqual(called_server_id, "remote_138")

        body = r.json()
        token = body["access_token"]
        payload = decode_token(token)
        self.assertEqual(payload["sub"], "tester")
        self.assertEqual(payload["sid"], "remote_138")
        self.assertTrue(payload.get("pset", False))

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch(
        "app.services.tenants_directory_service.resolve_login_route",
        lambda **kw: dict(_STUB_SINGLE),
    )
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_login_jwt_sid_matches_resolved_server(self, mock_auth: AsyncMock) -> None:
        """성공 시 JWT ``sid`` 는 검증에 사용된 데이터 서버 id."""
        mock_auth.return_value = {
            "user_id": "noprim",
            "user_name": "no",
            "server_id": "remote_138",
            "server_label": "AUTH",
            "hcode": "1234",
            "auth_flags": "1234:noprim",
            "role": "",
            "permissions": [],
        }

        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"userId": "noprim", "password": "pw"},
        )
        self.assertEqual(r.status_code, 200, r.text)
        payload = decode_token(r.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_138")

    @patch("app.services.tenants_directory_service.resolve_login_route_candidates", _stub_candidates)
    @patch(
        "app.services.tenants_directory_service.resolve_login_route",
        lambda **kw: dict(_STUB_SINGLE),
    )
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_login_failure_logs_auth_server(self, mock_auth: AsyncMock) -> None:
        mock_auth.return_value = None
        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "wrong"},
        )
        self.assertEqual(r.status_code, 401)
        called_server_id = mock_auth.await_args.args[0]
        self.assertEqual(called_server_id, "remote_138")


class LoginRequestModelTests(TestCase):
    """``LoginRequest.server_id`` 가 더 이상 필수 필드가 아니어야 한다."""

    def test_login_request_serverId_optional(self) -> None:
        from app.models.auth import LoginRequest

        req = LoginRequest(userId="x", password="y")  # serverId 미입력
        self.assertEqual(req.user_id, "x")
        self.assertEqual(req.server_id, "")


if __name__ == "__main__":
    main(verbosity=2)
