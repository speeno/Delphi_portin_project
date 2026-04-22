"""DEC-056 Wave A — `_resolve_role_and_permissions_async` 6 분기 회귀.

검증 항목 (분기 1~6 + R/W 페어 + LSP 보존)
------------------------------------------
1. 분기 1: ``hcode == '0000'`` → admin / ['*']
2. 분기 2: ``BLS_ADMIN_USER_IDS`` 화이트리스트 → admin / ['*']
3. 분기 3a: Id_Logn Fxx 매트릭스 (O 셀만) → operator / 매핑된 permission_code
4. 분기 3b: Id_Logn Fxx 매트릭스 (R 셀 + ``*.write`` 카탈로그) → R/W 페어 자동 변환
5. 분기 4: Id_Logn Fxx 매트릭스 빈 dict → web_admin.json 폴백
6. 어댑터 예외 시 분기 4 로 fail-safe 폴백 (운영 가용성 우선)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.services import auth_service  # noqa: E402


class ResolveRoleAndPermissionsAsyncTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # BLS_ADMIN_USER_IDS 가 외부 환경에 설정되어 있을 수 있으므로 격리
        self._prev_admin_ids = os.environ.pop("BLS_ADMIN_USER_IDS", None)
        self._prev_default_role = os.environ.pop("BLS_DEFAULT_ROLE", None)

    def tearDown(self) -> None:
        if self._prev_admin_ids is not None:
            os.environ["BLS_ADMIN_USER_IDS"] = self._prev_admin_ids
        if self._prev_default_role is not None:
            os.environ["BLS_DEFAULT_ROLE"] = self._prev_default_role

    async def test_branch1_super_user_hcode_0000(self) -> None:
        role, perms = await auth_service._resolve_role_and_permissions_async(
            "any-user", "0000", "remote_138"
        )
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    async def test_branch2_admin_whitelist(self) -> None:
        os.environ["BLS_ADMIN_USER_IDS"] = "alice,bob"
        role, perms = await auth_service._resolve_role_and_permissions_async(
            "alice", "1234", "remote_138"
        )
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    async def test_branch3a_id_logn_fxx_O_cells(self) -> None:
        # Fxx 'O' 셀이 카탈로그에 등록된 경우 → operator + 매핑된 permission_code
        fake_fxx = {"F11": "O", "F21": "O", "F36": "O"}
        with patch.object(
            auth_service, "_load_legacy_permission_index",
            return_value={
                "F11": "master.customer.read",
                "F21": "outbound.write",
                "F36": "report.read",
            },
        ), patch("app.core.auth_provider.LegacyIdLognProvider.fetch_fxx_matrix",
                 new=AsyncMock(return_value=fake_fxx)):
            role, perms = await auth_service._resolve_role_and_permissions_async(
                "user-x", "1234", "remote_138"
            )
        self.assertEqual(role, "operator")
        self.assertEqual(perms, ["master.customer.read", "outbound.write", "report.read"])

    async def test_branch3b_id_logn_fxx_R_cell_pairs_to_read(self) -> None:
        # F21='R' + catalog 의 F21='outbound.write' → 자동 'outbound.read' 페어 변환
        fake_fxx = {"F21": "R", "F11": "R"}
        with patch.object(
            auth_service, "_load_legacy_permission_index",
            return_value={
                "F21": "outbound.write",            # *.write → R 페어로 *.read 자동 부여
                "F11": "master.customer.read",      # 이미 *.read → R 그대로 부여
            },
        ), patch("app.core.auth_provider.LegacyIdLognProvider.fetch_fxx_matrix",
                 new=AsyncMock(return_value=fake_fxx)):
            role, perms = await auth_service._resolve_role_and_permissions_async(
                "user-r", "1234", "remote_138"
            )
        self.assertEqual(role, "operator")
        self.assertEqual(perms, ["master.customer.read", "outbound.read"])

    async def test_branch4_falls_back_to_web_admin_when_fxx_empty(self) -> None:
        # Fxx 가 빈 dict → 분기 4 로 폴백 (web_admin.json — 대부분의 환경에서 사용자 매핑 없음)
        with patch("app.core.auth_provider.LegacyIdLognProvider.fetch_fxx_matrix",
                   new=AsyncMock(return_value={})):
            role, perms = await auth_service._resolve_role_and_permissions_async(
                "ghost-user", "1234", "remote_138"
            )
        # 시드되지 않은 사용자 → ('', []) — DEC-047 정상 폴백
        self.assertEqual(role, "")
        self.assertEqual(perms, [])

    async def test_branch3_adapter_exception_fails_safe(self) -> None:
        # 어댑터가 raise 해도 분기 4 로 자연 폴백 (운영 가용성)
        with patch("app.core.auth_provider.LegacyIdLognProvider.fetch_fxx_matrix",
                   new=AsyncMock(side_effect=RuntimeError("network down"))):
            role, perms = await auth_service._resolve_role_and_permissions_async(
                "user-y", "1234", "remote_138"
            )
        self.assertEqual(role, "")
        self.assertEqual(perms, [])

    async def test_lsp_sync_function_signature_unchanged(self) -> None:
        """기존 동기 ``_resolve_role_and_permissions(user_id, hcode)`` 무회귀."""
        # 분기 1 동기 동작이 비동기와 동일한지
        sync_role, sync_perms = auth_service._resolve_role_and_permissions("any", "0000")
        self.assertEqual((sync_role, sync_perms), ("admin", ["*"]))


if __name__ == "__main__":
    main(verbosity=2)
