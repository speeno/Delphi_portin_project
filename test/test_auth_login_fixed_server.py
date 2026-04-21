"""DEC-051 — 로그인 인증 서버 단일화(`BLS_AUTH_SERVER_ID`) + JWT sid = primary 가드."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.core.security import decode_token  # noqa: E402


class FixedAuthServerTests(TestCase):
    """`/api/v1/auth/login` 은 ``serverId`` 입력을 무시하고 항상 인증 서버로 검증."""

    def setUp(self) -> None:
        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"

    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    @patch("app.services.admin_service.get_primary_data_server")
    def test_login_ignores_serverId_and_uses_env(
        self, mock_primary: MagicMock, mock_auth: AsyncMock
    ) -> None:
        """입력 ``serverId='other'`` 를 보내도 ``authenticate_user`` 는 ``remote_138`` 로 호출."""
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
        mock_primary.return_value = "remote_154"

        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"serverId": "remote_999_should_be_ignored", "userId": "tester", "password": "pw"},
        )
        self.assertEqual(r.status_code, 200, r.text)

        # 인증 호출은 BLS_AUTH_SERVER_ID 로 고정.
        mock_auth.assert_awaited_once()
        called_server_id = mock_auth.await_args.args[0]
        self.assertEqual(called_server_id, "remote_138")

        body = r.json()
        # JWT sid 는 primary 매핑 결과여야 한다 (DEC-052).
        token = body["access_token"]
        payload = decode_token(token)
        self.assertEqual(payload["sub"], "tester")
        self.assertEqual(payload["sid"], "remote_154")

    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    @patch("app.services.admin_service.get_primary_data_server")
    def test_login_falls_back_to_auth_server_when_primary_missing(
        self, mock_primary: MagicMock, mock_auth: AsyncMock
    ) -> None:
        """Primary 미설정 사용자는 인증 서버를 그대로 sid 로 사용 (폴백)."""
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
        mock_primary.return_value = None

        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"userId": "noprim", "password": "pw"},  # serverId 미전송
        )
        self.assertEqual(r.status_code, 200, r.text)
        payload = decode_token(r.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_138")

    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    @patch("app.services.admin_service.get_primary_data_server")
    def test_login_failure_logs_auth_server(
        self, mock_primary: MagicMock, mock_auth: AsyncMock
    ) -> None:
        mock_auth.return_value = None
        mock_primary.return_value = None
        client = TestClient(app)
        r = client.post(
            "/api/v1/auth/login",
            json={"userId": "tester", "password": "wrong"},
        )
        self.assertEqual(r.status_code, 401)
        # 인증 호출은 항상 인증 서버로
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
