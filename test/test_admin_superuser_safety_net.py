"""DEC-056 보강 — admin 슈퍼유저 3중 안전망 회귀 가드.

3중 안전망 구성
---------------
#1 ``Id_Logn.hcode == '0000'`` (auth_service 분기 1) — DEC-007 동등 (M0 적용 후)
#2 ``BLS_ADMIN_USER_IDS`` 화이트리스트 (auth_service 분기 2)
   - **신규**: env 미설정 시 기본 폴백 ``{'admin'}`` (이 테스트가 가드)
   - env="" 명시 시 폴백 비활성 (운영자 의도 존중)
   - env="X,Y" 명시 시 그 값만 사용 (기본 폴백 미사용)
#3 ``web_admin.json`` 의 admin 사용자 → ``role-admin`` 매핑 (auth_service 분기 4)
   - **신규**: ``_empty_state()`` 가 신규 환경에 자동 시드
   - **신규**: ``_ensure_admin_role_mapping()`` 이 기존 환경에 idempotent 보정

본 테스트는 위 3 안전망 모두를 *독립적으로* 검증해 어느 하나가 실패해도 다른
경로로 admin 이 슈퍼유저로 인식됨을 보장한다.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))


# ────────────────────────────────────────────────────────────────────────────
# 안전망 #2 — _admin_whitelist_ids() 폴백 정책
# ────────────────────────────────────────────────────────────────────────────
class AdminWhitelistFallbackTest(TestCase):
    """``_admin_whitelist_ids`` 의 env 정책 3 분기 검증."""

    def setUp(self) -> None:
        self._prev = os.environ.pop("BLS_ADMIN_USER_IDS", None)
        from app.services import auth_service  # noqa: PLC0415
        self._svc = auth_service

    def tearDown(self) -> None:
        os.environ.pop("BLS_ADMIN_USER_IDS", None)
        if self._prev is not None:
            os.environ["BLS_ADMIN_USER_IDS"] = self._prev

    def test_env_unset_returns_default_admin(self) -> None:
        """env 미설정 → 기본 폴백 ``{'admin'}`` (3중 안전망 #2 핵심)."""
        os.environ.pop("BLS_ADMIN_USER_IDS", None)
        ids = self._svc._admin_whitelist_ids()
        self.assertIn("admin", ids, "env 미설정 시 기본 폴백 {'admin'} 누락")
        self.assertEqual(ids, {"admin"})

    def test_env_empty_string_disables_fallback(self) -> None:
        """env="" 명시 → 빈 set (운영자 의도 존중 — 보안 격리 환경)."""
        os.environ["BLS_ADMIN_USER_IDS"] = ""
        ids = self._svc._admin_whitelist_ids()
        self.assertEqual(ids, set(), "env='' 명시 비활성화 동작 회귀")

    def test_env_explicit_overrides_default(self) -> None:
        """env="ops-1,ops-2" → 그 값만 (기본 폴백 'admin' 미부여)."""
        os.environ["BLS_ADMIN_USER_IDS"] = "ops-1,ops-2"
        ids = self._svc._admin_whitelist_ids()
        self.assertEqual(ids, {"ops-1", "ops-2"})
        self.assertNotIn("admin", ids, "명시 지정 시 기본 'admin' 폴백 침해")


class AdminLoginSuperUserResolutionTest(IsolatedAsyncioTestCase):
    """``admin`` user_id + 비-0000 hcode 입력 → 분기 2 폴백 → admin / ['*']."""

    def setUp(self) -> None:
        self._prev_admin_ids = os.environ.pop("BLS_ADMIN_USER_IDS", None)
        self._prev_default_role = os.environ.pop("BLS_DEFAULT_ROLE", None)
        from app.services import auth_service  # noqa: PLC0415
        self._svc = auth_service

    def tearDown(self) -> None:
        os.environ.pop("BLS_ADMIN_USER_IDS", None)
        os.environ.pop("BLS_DEFAULT_ROLE", None)
        if self._prev_admin_ids is not None:
            os.environ["BLS_ADMIN_USER_IDS"] = self._prev_admin_ids
        if self._prev_default_role is not None:
            os.environ["BLS_DEFAULT_ROLE"] = self._prev_default_role

    async def test_admin_user_id_with_5digit_hcode_is_super(self) -> None:
        """레거시 5자리 ``hcode='00000'`` 환경에서도 admin 분기 2 폴백 성공."""
        role, perms = await self._svc._resolve_role_and_permissions_async(
            "admin", "00000", "remote_138"
        )
        self.assertEqual(role, "admin", "admin user_id 가 슈퍼유저로 해석되지 않음")
        self.assertEqual(perms, ["*"])

    async def test_admin_user_id_sync_function_too(self) -> None:
        """동기 함수 ``_resolve_role_and_permissions`` 도 동일 폴백 (LSP)."""
        role, perms = self._svc._resolve_role_and_permissions("admin", "00000")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    async def test_explicit_env_disables_admin_fallback(self) -> None:
        """env='other-admin' 명시 시 ``admin`` 은 더 이상 분기 2 슈퍼유저가 아님."""
        os.environ["BLS_ADMIN_USER_IDS"] = "other-admin"
        # 분기 1·2 모두 실패 → 분기 3 (Fxx 어댑터) 시도하나 실DB 없음 → 분기 4 폴백
        # web_admin.json 의 admin 매핑이 있으면 admin role 부여, 없으면 ('', [])
        # 이 테스트는 *적어도* 분기 2 가 의도적으로 비활성화되었음을 확인한다.
        ids = self._svc._admin_whitelist_ids()
        self.assertEqual(ids, {"other-admin"})


# ────────────────────────────────────────────────────────────────────────────
# 안전망 #3 — admin_service _empty_state() / _ensure_admin_role_mapping()
# ────────────────────────────────────────────────────────────────────────────
class AdminAutoSeedAndBackfillTest(TestCase):
    """``_empty_state()`` 가 admin 자동 시드 + 기존 환경에 자동 보정."""

    def setUp(self) -> None:
        # WEB_ADMIN_PATH 를 임시 경로로 격리
        self._tmpdir = tempfile.TemporaryDirectory()
        self._tmppath = Path(self._tmpdir.name) / "web_admin.json"
        self._prev_path_env = os.environ.get("BLS_WEB_ADMIN_PATH")
        os.environ["BLS_WEB_ADMIN_PATH"] = str(self._tmppath)
        # 모듈 재로딩 — 모듈 레벨 ``WEB_ADMIN_PATH`` 가 env 를 한 번만 읽음
        import app.services.admin_service as _svc  # noqa: PLC0415
        self._svc = importlib.reload(_svc)
        # _NORMALIZED_ONCE 도 리셋
        self._svc._NORMALIZED_ONCE = False

    def tearDown(self) -> None:
        if self._prev_path_env is not None:
            os.environ["BLS_WEB_ADMIN_PATH"] = self._prev_path_env
        else:
            os.environ.pop("BLS_WEB_ADMIN_PATH", None)
        # 다음 테스트를 위해 모듈을 다시 원래 경로로 복원
        import app.services.admin_service as _svc  # noqa: PLC0415
        importlib.reload(_svc)
        self._tmpdir.cleanup()

    def test_empty_state_seeds_admin_with_role(self) -> None:
        """신규 환경 시드: ``admin`` 사용자 + ``role-admin`` 매핑 자동 생성."""
        state = self._svc._empty_state()
        users = state["web_users"]
        admin = next((u for u in users if u["login_id"] == "admin"), None)
        self.assertIsNotNone(admin, "_empty_state() 가 admin 사용자를 시드하지 않음")
        self.assertEqual(admin["status"], "active")
        bindings = state["web_user_roles"]
        admin_id = admin["id"]
        admin_binding = next(
            (b for b in bindings if b.get("user_id") == admin_id and b.get("role_id") == "role-admin"),
            None,
        )
        self.assertIsNotNone(admin_binding, "_empty_state() 가 admin → role-admin 매핑을 시드하지 않음")

    def test_load_state_creates_admin_binding_for_new_environment(self) -> None:
        """파일이 없는 신규 환경 → ``_load_state()`` 가 자동으로 admin 시드된 파일 생성."""
        self.assertFalse(self._tmppath.exists())
        state = self._svc._load_state()
        admin = next((u for u in state["web_users"] if u["login_id"] == "admin"), None)
        self.assertIsNotNone(admin, "신규 환경 _load_state() 후 admin 사용자 누락")
        roles, perms = self._svc.list_user_roles_and_permissions("admin")
        self.assertIn("admin", roles, "admin 사용자가 role-admin 으로 매핑되지 않음")
        self.assertIn("*", perms, "role-admin 의 '*' 권한이 admin 에게 부여되지 않음")

    def test_ensure_admin_role_mapping_backfills_legacy_state(self) -> None:
        """기존 환경에 admin 사용자만 있고 매핑 누락 시 자동 보정 (idempotent)."""
        legacy_state = {
            "schema_version": 1,
            "web_users": [
                {
                    "id": "u-legacy-admin",
                    "login_id": "admin",
                    "status": "active",
                    "created_at": "2026-04-21T00:00:00+00:00",
                },
            ],
            "web_user_servers": [],
            "web_roles": [
                {"id": "role-admin", "code": "admin", "name": "관리자", "permissions": ["*"]},
            ],
            "web_user_roles": [],
            "legacy_permission_map": [],
            "application_settings": [],
            "application_settings_history": [],
        }
        self._tmppath.write_text(json.dumps(legacy_state, ensure_ascii=False), encoding="utf-8")

        state = self._svc._load_state()
        bindings = state["web_user_roles"]
        admin_binding = next(
            (b for b in bindings if b.get("user_id") == "u-legacy-admin" and b.get("role_id") == "role-admin"),
            None,
        )
        self.assertIsNotNone(admin_binding, "기존 admin 사용자에 role-admin 자동 보정 실패")

        # idempotent — 한 번 더 호출해도 중복 추가 없음
        bindings_count = len(state["web_user_roles"])
        state2 = self._svc._load_state()
        self.assertEqual(len(state2["web_user_roles"]), bindings_count, "재호출 시 중복 binding 추가됨")

    def test_ensure_admin_role_mapping_skips_when_admin_user_removed(self) -> None:
        """운영자가 admin 사용자를 의도적으로 제거한 환경 → 자동 시드 안함 (의사 존중)."""
        state_no_admin = {
            "schema_version": 1,
            "web_users": [
                {"id": "u-other", "login_id": "other-user", "status": "active", "created_at": "2026-04-22T00:00:00+00:00"},
            ],
            "web_user_servers": [],
            "web_roles": [
                {"id": "role-admin", "code": "admin", "name": "관리자", "permissions": ["*"]},
            ],
            "web_user_roles": [],
            "legacy_permission_map": [],
            "application_settings": [],
            "application_settings_history": [],
        }
        self._tmppath.write_text(json.dumps(state_no_admin, ensure_ascii=False), encoding="utf-8")
        state = self._svc._load_state()
        # 의사 존중 — 새 admin 사용자를 자동으로 추가하지 않음
        admin = next((u for u in state["web_users"] if u.get("login_id") == "admin"), None)
        self.assertIsNone(admin, "운영자 의사를 거슬러 admin 사용자가 다시 추가됨")


# ────────────────────────────────────────────────────────────────────────────
# 안전망 #3 — 운영 web_admin.json 시드 검증 (기존 데이터)
# ────────────────────────────────────────────────────────────────────────────
class CurrentWebAdminJsonAdminBindingTest(TestCase):
    """현재 ``data/web_admin.json`` 의 admin 사용자 매핑이 적재되어 있는지 검증."""

    def test_admin_user_has_role_admin_binding(self) -> None:
        path = _BACKEND_ROOT / "data" / "web_admin.json"
        if not path.exists():
            self.skipTest("web_admin.json 미존재 (CI 일부 환경)")
        state = json.loads(path.read_text(encoding="utf-8"))
        users = state.get("web_users", [])
        admin = next((u for u in users if u.get("login_id") == "admin"), None)
        if admin is None:
            # admin 이 시드되지 않은 환경(별도 부트스트랩)이면 본 테스트 스킵
            self.skipTest("web_admin.json 에 admin 사용자 미시드 (별도 환경)")
        admin_user_id = admin.get("id")
        bindings = state.get("web_user_roles", [])
        admin_binding = next(
            (
                b
                for b in bindings
                if b.get("user_id") == admin_user_id and b.get("role_id") == "role-admin"
            ),
            None,
        )
        self.assertIsNotNone(
            admin_binding,
            "data/web_admin.json 의 admin 사용자에 role-admin 매핑이 적재되어 있지 않음 — DEC-056 보강 #3 회귀",
        )
        # role-admin 의 permissions 에 '*' 포함 확인
        roles = state.get("web_roles", [])
        admin_role = next((r for r in roles if r.get("id") == "role-admin"), None)
        self.assertIsNotNone(admin_role, "role-admin 정의 누락")
        assert admin_role is not None  # mypy
        self.assertIn("*", admin_role.get("permissions", []), "role-admin 권한 '*' 누락")


if __name__ == "__main__":
    main(verbosity=2)
