"""동적 서버 선택 로그인 신뢰도 회귀 가드 (DSN-DEC-08/09)."""

from __future__ import annotations

import json
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

from app.core.security import decode_token  # noqa: E402
from app.main import app  # noqa: E402


def _route(
    remote_id: str,
    db_name: str,
    *,
    via: str = "index",
    candidate_via: str | None = None,
    index_status: str = "single",
    priority: int = 0,
) -> dict:
    return {
        "remote_id": remote_id,
        "db_name": db_name,
        "tenant_id": "tenant-test",
        "account_family": db_name.removesuffix("_db"),
        "primary_server_label": "",
        "build_role": "",
        "default_account_type": "",
        "tenant_label_kor": "",
        "via": via,
        "index_status": index_status,
        "candidate_via": candidate_via or via,
        "confidence": "high",
        "priority": priority,
    }


def _user(user_id: str, *, server_id: str, hcode: str = "1001", db_name: str = "tenant_db") -> dict:
    return {
        "user_id": user_id,
        "user_name": "테스트 사용자",
        "display_name": "테스트",
        "server_id": server_id,
        "server_label": server_id,
        "hcode": hcode,
        "auth_flags": f"{hcode}:테스트",
        "role": "",
        "permissions": [],
        "resolved_db": db_name,
    }


class CapturingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def parsed(self) -> list[dict]:
        out: list[dict] = []
        for record in self.records:
            msg = record.getMessage()
            idx = msg.find("{")
            if idx < 0:
                continue
            out.append(json.loads(msg[idx:]))
        return out


class DynamicLoginRoutingTests(TestCase):
    def setUp(self) -> None:
        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.auth")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)
        try:
            from app.services import login_id_index_service

            login_id_index_service.reset_refresh_state_for_tests()
        except Exception:
            pass

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_single_routes_to_resolved_db(
        self,
        mock_auth: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        route = _route("remote_153", "book_07_db", via="index", candidate_via="index_single")
        mock_single.return_value = route
        mock_candidates.return_value = [route]
        mock_auth.return_value = _user("book-user", server_id="remote_153", db_name="book_07_db")

        res = self.client.post(
            "/api/v1/auth/login",
            json={"serverId": "remote_999", "userId": "book-user", "password": "pw"},
        )

        self.assertEqual(res.status_code, 200, res.text)
        mock_auth.assert_awaited_once_with(
            "remote_153", "book-user", "pw", db_name="book_07_db"
        )
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_153")
        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["resolved_via"], "index_single")
        self.assertEqual(rec["candidate_sources"], ["index_single"])

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.login_id_index_service.lazy_refresh", new_callable=AsyncMock)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_miss_lazy_refresh_rebuilds_then_succeeds(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        refreshed = {"done": False}
        route = _route("remote_154", "chul_09_db", via="index", candidate_via="index_single")

        async def _lazy():
            refreshed["done"] = True
            return {"refreshed": True, "reason": "rebuilt", "stats": {"errors": []}}

        mock_lazy.side_effect = _lazy
        mock_single.side_effect = lambda **_kw: route if refreshed["done"] else None
        mock_candidates.side_effect = lambda **_kw: [route] if refreshed["done"] else []
        mock_auth.return_value = _user("late-user", server_id="remote_154", db_name="chul_09_db")

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "late-user", "password": "pw"},
        )

        self.assertEqual(res.status_code, 200, res.text)
        mock_lazy.assert_awaited_once()
        mock_auth.assert_awaited_once_with(
            "remote_154", "late-user", "pw", db_name="chul_09_db"
        )
        rec = self.handler.parsed()[-1]
        self.assertTrue(rec["lazy_refreshed"])
        self.assertEqual(rec["lazy_refresh_reason"], "rebuilt")

    @patch("app.routers.auth.should_bypass_login_id_index_ambiguity", return_value=False)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.login_id_index_service.lazy_refresh", new_callable=AsyncMock)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_ambiguous_without_hint_is_not_probed(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
        _mock_bypass,
    ) -> None:
        ambiguous_single = {
            "remote_id": "",
            "db_name": "",
            "via": "index_ambiguous",
            "index_status": "ambiguous",
        }
        routes = [
            _route(
                "remote_153",
                "book_07_db",
                via="index_ambiguous",
                candidate_via="index_ambiguous",
                index_status="ambiguous",
            ),
            _route(
                "remote_154",
                "chul_09_db",
                via="index_ambiguous",
                candidate_via="index_ambiguous",
                index_status="ambiguous",
                priority=1,
            ),
        ]
        mock_single.return_value = ambiguous_single
        mock_candidates.return_value = routes
        mock_lazy.return_value = {"refreshed": False, "reason": "cooldown", "stats": None}

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "shared-user", "password": "pw"},
        )

        self.assertEqual(res.status_code, 401)
        mock_auth.assert_not_awaited()
        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["reason"], "ambiguous_route")
        self.assertEqual(rec["resolved_via"], "index_ambiguous")
        self.assertEqual(rec["candidate_attempts"], 0)
        self.assertEqual(rec["lazy_refresh_reason"], "cooldown")

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_ambiguous_with_hcode_can_be_narrowed(
        self,
        mock_auth: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        route = _route("remote_155", "book_21_db", via="index_hcode", candidate_via="index_single")
        mock_single.return_value = route
        mock_candidates.return_value = [route]
        mock_auth.return_value = _user("shared-user", server_id="remote_155", hcode="2002", db_name="book_21_db")

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "shared-user", "password": "pw", "hcode": "2002"},
        )

        self.assertEqual(res.status_code, 200, res.text)
        mock_auth.assert_awaited_once_with(
            "remote_155", "shared-user", "pw", db_name="book_21_db"
        )
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_155")


if __name__ == "__main__":
    main(verbosity=2)
