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
    tenant_id: str = "tenant-test",
) -> dict:
    return {
        "remote_id": remote_id,
        "db_name": db_name,
        "tenant_id": tenant_id,
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


def _user(
    user_id: str,
    *,
    server_id: str,
    hcode: str = "1001",
    db_name: str = "tenant_db",
    active_build_id: str | None = None,
    tenant_id: str | None = None,
    ownership_status: str = "none",
    login_profile: str = "",
    menu_shell_hint: str = "",
) -> dict:
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
        "active_build_id": active_build_id,
        "tenant_id": tenant_id,
        "login_profile": login_profile,
        "menu_shell_hint": menu_shell_hint,
        "ownership_status": ownership_status,
        "ownership_candidate_count": 0 if ownership_status != "ambiguous" else 2,
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
            "remote_153", "book-user", "pw", db_name="book_07_db",
            tenant_id_hint=None, hcode_hint=None,
        )
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_153")
        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["resolved_via"], "index_single")
        self.assertEqual(rec["candidate_sources"], ["index_single"])

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_active_build_id_survives_login_token_and_response(
        self,
        mock_auth: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        route = _route("remote_153", "chul_09_db", via="index", candidate_via="index_single")
        mock_single.return_value = route
        mock_candidates.return_value = [route]
        mock_auth.return_value = _user(
            "warehouse-user",
            server_id="remote_153",
            db_name="chul_09_db",
            active_build_id="BLD-PUB-WAREHOUSE-WELOVE",
        )

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "warehouse-user", "password": "pw"},
        )

        self.assertEqual(res.status_code, 200, res.text)
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["active_build_id"], "BLD-PUB-WAREHOUSE-WELOVE")
        self.assertEqual(res.json()["user"]["active_build_id"], "BLD-PUB-WAREHOUSE-WELOVE")

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
            "remote_154", "late-user", "pw", db_name="chul_09_db",
            tenant_id_hint=None, hcode_hint=None,
        )
        rec = self.handler.parsed()[-1]
        self.assertTrue(rec["lazy_refreshed"])
        self.assertEqual(rec["lazy_refresh_reason"], "rebuilt")

    @patch("app.routers.auth.should_bypass_login_id_index_ambiguity", return_value=False)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.services.login_id_index_service.lazy_refresh", new_callable=AsyncMock)
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_index_ambiguous_strict_mode_probes_with_warnings(
        self,
        mock_auth: AsyncMock,
        mock_lazy: AsyncMock,
        mock_candidates,
        mock_single,
        _mock_bypass,
    ) -> None:
        """DSN-DEC-09 — strict env(`BLS_LOGIN_AMBIGUOUS_PROBE=block`) 에서도 암호 일치 시 로그인 + warnings."""
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
        mock_auth.side_effect = [
            None,
            _user("shared-user", server_id="remote_154", db_name="chul_09_db"),
        ]

        with patch.dict(os.environ, {"BLS_LOGIN_AMBIGUOUS_PROBE": "block"}):
            res = self.client.post(
                "/api/v1/auth/login",
                json={"userId": "shared-user", "password": "pw"},
            )

        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertTrue(body.get("access_token"))
        warnings = body.get("warnings") or []
        self.assertTrue(
            any("여러" in w or "회사" in w for w in warnings),
            warnings,
        )
        self.assertGreaterEqual(mock_auth.await_count, 1)
        rec = self.handler.parsed()[-1]
        self.assertEqual(rec["result"], "success")
        self.assertEqual(rec["lazy_refresh_reason"], "cooldown")

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

        async def _fake_auth(server_id, user_id, password, *, db_name=None, **kwargs):
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
            "remote_155", "shared-user", "pw", db_name="book_21_db",
            tenant_id_hint=None, hcode_hint="2002",
        )
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["sid"], "remote_155")

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_login_forwards_tenant_id_hint_to_authenticate(
        self,
        mock_auth: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        tid = "fa6758ea-a7e5-5d27-bf87-ccee0a90e72c"
        route = _route(
            "remote_153",
            "chul_09_db",
            via="tenant_id",
            candidate_via="tenant_id",
            tenant_id=tid,
        )
        mock_single.return_value = route
        mock_candidates.return_value = [route]
        mock_auth.return_value = _user(
            "경리부",
            server_id="remote_153",
            db_name="chul_09_db",
            tenant_id=tid,
            ownership_status="unique",
        )

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "경리부", "password": "pw", "tenantId": tid},
        )

        self.assertEqual(res.status_code, 200, res.text)
        mock_auth.assert_awaited_once_with(
            "remote_153", "경리부", "pw", db_name="chul_09_db",
            tenant_id_hint=tid, hcode_hint=None,
        )
        self.assertEqual(res.json()["user"]["ownership_status"], "unique")

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_login_profile_claims_roundtrip_to_token_and_user(
        self,
        mock_auth: AsyncMock,
        mock_candidates,
        mock_single,
    ) -> None:
        route = _route("remote_153", "chul_09_db", via="tenant_id", candidate_via="tenant_id")
        mock_single.return_value = route
        mock_candidates.return_value = [route]
        mock_auth.return_value = _user(
            "경리부",
            server_id="remote_153",
            db_name="chul_09_db",
            login_profile="department_accounting",
            menu_shell_hint="accounting_only",
        )

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "경리부", "password": "pw"},
        )

        self.assertEqual(res.status_code, 200, res.text)
        payload = decode_token(res.json()["access_token"])
        self.assertEqual(payload["login_profile"], "department_accounting")
        self.assertEqual(payload["menu_shell_hint"], "accounting_only")
        self.assertEqual(res.json()["user"]["login_profile"], "department_accounting")
        self.assertEqual(res.json()["user"]["menu_shell_hint"], "accounting_only")


if __name__ == "__main__":
    main(verbosity=2)
