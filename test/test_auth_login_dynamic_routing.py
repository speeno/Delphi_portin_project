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
    def test_index_ambiguous_strict_mode_blocks_without_hint(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
        _mock_bypass,
    ) -> None:
        """DSN-DEC-09 v2 — ``BLS_LOGIN_AMBIGUOUS_PROBE=block`` opt-in 시 v1 정책(즉시 차단) 보존.

        v2 default 는 password narrowing 이지만, 보안 격리 환경에서는 운영자가
        명시적으로 strict 모드를 켜 ``index_ambiguous`` 를 hcode/tenantId 없이는
        시도조차 하지 않게 할 수 있다. 본 테스트는 그 strict 정책의 회귀 가드.
        """
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

        with patch.dict(os.environ, {"BLS_LOGIN_AMBIGUOUS_PROBE": "block"}):
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
        self.assertTrue(rec.get("ambiguous_strict"))

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.routers.auth.should_bypass_login_id_index_ambiguity", return_value=False)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.login_id_index_service.lazy_refresh", new_callable=AsyncMock)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_ambiguous_default_password_narrowing_succeeds(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
        _mock_bypass,
    ) -> None:
        """DSN-DEC-09 v2 default — 미래가치 같은 ambiguous 계정의 비밀번호 기반 narrowing.

        시나리오:
        - login_id_index 가 ``chul_05_db`` / ``chul_09_db`` 둘 다에 동일 ID 행을 보고
        - hcode/tenantId 힌트 없음 (사용자가 자기 hcode 를 모름 — 일반적)
        - 비밀번호는 두 번째 후보(chul_09_db)에서만 일치
        → 두 번째 후보로 narrowing 되고 200 반환. 감사 로그에 narrow 발생 신호 기록.
        """
        ambiguous_single = {
            "remote_id": "",
            "db_name": "",
            "via": "index_ambiguous",
            "index_status": "ambiguous",
        }
        routes = [
            _route(
                "remote_153",
                "chul_05_db",
                via="index_ambiguous",
                candidate_via="index_ambiguous",
                index_status="ambiguous",
            ),
            _route(
                "remote_153",
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

        async def _fake_auth(server_id, user_id, password, *, db_name=None):
            if db_name == "chul_09_db":
                return _user(user_id, server_id=server_id, hcode="5088", db_name="chul_09_db")
            return None

        mock_auth.side_effect = _fake_auth

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BLS_LOGIN_AMBIGUOUS_PROBE", None)
            res = self.client.post(
                "/api/v1/auth/login",
                json={"userId": "미래가치", "password": "secret"},
            )

        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(mock_auth.await_count, 2, "narrow 위해 양쪽 후보 모두 시도해야 함")
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_153")

        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["result"], "success")
        self.assertEqual(rec["resolved_db"], "chul_09_db")
        self.assertTrue(rec.get("ambiguous_narrowed"), "ambiguous_narrowed audit 신호 필수")
        self.assertEqual(rec["candidate_attempts"], 2)
        self.assertIn("index_ambiguous", rec.get("candidate_sources") or [])
        self.assertEqual(rec["resolved_via"], "candidate_probe")

    @patch("app.routers.auth.should_bypass_login_id_index_ambiguity", return_value=False)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.login_id_index_service.lazy_refresh", new_callable=AsyncMock)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_ambiguous_default_password_narrowing_fails_when_no_match(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
        _mock_bypass,
    ) -> None:
        """DSN-DEC-09 v2 default — narrowing 시도했으나 어떤 후보도 비밀번호 미일치.

        모든 후보에 대해 ``authenticate_user`` 가 ``None`` 을 반환 → 401 +
        ``invalid_credentials_after_probe`` 사유. 사용자 ID 자체는 인덱스에 있는데
        비밀번호가 틀린 흔한 케이스. 감사 로그에 narrow 시도 흔적이 그대로 남는다.
        """
        ambiguous_single = {
            "remote_id": "",
            "db_name": "",
            "via": "index_ambiguous",
            "index_status": "ambiguous",
        }
        routes = [
            _route(
                "remote_153",
                "chul_05_db",
                via="index_ambiguous",
                candidate_via="index_ambiguous",
                index_status="ambiguous",
            ),
            _route(
                "remote_153",
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
        mock_auth.return_value = None

        os.environ.pop("BLS_LOGIN_AMBIGUOUS_PROBE", None)
        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "미래가치", "password": "wrong"},
        )

        self.assertEqual(res.status_code, 401)
        self.assertGreaterEqual(mock_auth.await_count, 2)
        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["result"], "failure")
        self.assertEqual(rec["reason"], "invalid_credentials_after_probe")
        self.assertTrue(rec.get("ambiguous_narrowed"))
        self.assertGreaterEqual(rec["candidate_attempts"], 2)

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
