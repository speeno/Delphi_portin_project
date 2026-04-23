"""DEC-056 Wave B 분기 0 회귀 가드 — admin role 매핑 우선.

배경 (사용자 룰 — 일반화)
-----------------------
DEC-056 Wave A 의 Id_Logn Fxx 어댑터(분기 3) 가 admin 사용자에 대해
``operator`` role 을 합성하면 분기 4 (web_admin.json 의 admin 매핑) 가
평가되지 않는 lacuna 가 존재했다. Wave B 의 분기 0 은 이를 원천 차단:
``admin_service.list_user_roles_and_permissions`` 가 ``role-admin`` 또는
``admin`` role 을 반환하는 사용자에 대해 *어떤 분기보다도 먼저* admin/['*']
반환을 보장.

가드 대상
---------
- 동기 함수 ``_resolve_role_and_permissions`` (legacy/test 경로)
- 비동기 함수 ``_resolve_role_and_permissions_async`` (정공법 로그인 경로)

두 경로 모두에 분기 0 을 적용한 이유: LSP — sync/async 두 진입점이 동일한
admin 우선 정책을 공유해야 한다.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))


class AdminResolverBranch0PriorityTest(TestCase):
    """분기 0 가 분기 1·2·3 모두 우회하는지 검증."""

    def setUp(self) -> None:
        self._prev_env = os.environ.pop("BLS_ADMIN_USER_IDS", None)
        os.environ["BLS_ADMIN_USER_IDS"] = ""
        from app.services import auth_service  # noqa: PLC0415
        self._auth = auth_service

    def tearDown(self) -> None:
        os.environ.pop("BLS_ADMIN_USER_IDS", None)
        if self._prev_env is not None:
            os.environ["BLS_ADMIN_USER_IDS"] = self._prev_env

    def _mock_admin_role(self, user_id: str = "tester"):
        """admin_service 가 ``role-admin`` 만 반환하도록 mock."""
        return patch(
            "app.services.admin_service.list_user_roles_and_permissions",
            return_value=(["role-admin"], set()),
        )

    def test_sync_branch0_overrides_non_admin_hcode(self) -> None:
        """admin role 매핑 + hcode='99999' (분기 1 미적용) → admin/['*']."""
        with self._mock_admin_role():
            role, perms = self._auth._resolve_role_and_permissions("tester", "99999")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    def test_sync_branch0_overrides_empty_whitelist(self) -> None:
        """BLS_ADMIN_USER_IDS='' (분기 2 비활성) 에도 분기 0 발효."""
        os.environ["BLS_ADMIN_USER_IDS"] = ""
        with self._mock_admin_role():
            role, perms = self._auth._resolve_role_and_permissions("tester", "12345")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    def test_async_branch0_overrides_fxx_operator(self) -> None:
        """분기 3 의 Id_Logn Fxx 가 operator 를 합성해도 분기 0 가 우선."""

        async def _fake_fxx_matrix(server_id, user_id):
            return {"F02": "O", "F03": "R"}  # 분기 3 가 operator 합성

        with self._mock_admin_role():
            with patch(
                "app.core.auth_provider.select_provider",
                return_value=type("P", (), {"fetch_fxx_matrix": staticmethod(_fake_fxx_matrix)})(),
            ):
                role, perms = asyncio.get_event_loop().run_until_complete(
                    self._auth._resolve_role_and_permissions_async(
                        "tester", "12345", "remote_152",
                    )
                )
        self.assertEqual(role, "admin", "분기 0 이 분기 3 보다 먼저 발효해야 함")
        self.assertEqual(perms, ["*"])

    def test_branch0_non_admin_unaffected(self) -> None:
        """일반 사용자(role-admin 미매핑) 는 영향 받지 않음 — 부작용 없음."""
        with patch(
            "app.services.admin_service.list_user_roles_and_permissions",
            return_value=(["role-operator"], {"books.read"}),
        ):
            role, perms = self._auth._resolve_role_and_permissions("op-1", "11111")
        self.assertEqual(role, "role-operator")
        self.assertEqual(perms, ["books.read"])

    def test_branch0_admin_role_code_also_recognized(self) -> None:
        """role 코드가 'admin' (외부 통합) 인 경우도 분기 0 발효."""
        with patch(
            "app.services.admin_service.list_user_roles_and_permissions",
            return_value=(["admin"], set()),
        ):
            role, perms = self._auth._resolve_role_and_permissions("ext-admin", "")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])


if __name__ == "__main__":
    main()
