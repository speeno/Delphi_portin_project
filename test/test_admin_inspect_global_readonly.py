from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

from fastapi import HTTPException
from starlette.requests import Request

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))


def _request(method: str = "GET", path: str = "/api/v1/reports/book-sales", query: bytes = b"serverId=remote_153") -> Request:
    return Request(
        {
            "type": "http",
            "method": method,
            "path": path,
            "headers": [],
            "query_string": query,
            "path_params": {},
        }
    )


class AdminInspectContextTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        from app.core import deps
        from app.core.inspect_context import clear_inspect_context

        self.deps = deps
        clear_inspect_context()
        self.old_get_server_profile = deps.get_server_profile
        deps.get_server_profile = lambda server_id: {"id": server_id, "database": "main_db"}

    async def asyncTearDown(self) -> None:
        from app.core.inspect_context import clear_inspect_context

        self.deps.get_server_profile = self.old_get_server_profile
        clear_inspect_context()

    async def test_super_admin_get_sets_inspect_context_and_ownership_bypass(self) -> None:
        from app.core.inspect_context import get_inspect_context

        header = json.dumps(
            {
                "inspect_mode": True,
                "inspect_server_id": "remote_153",
                "inspect_db_name": "chul_05_db",
                "inspect_reason": "장애 점검",
            }
        )
        ctx = await self.deps.get_user_context(
            _request("GET"),
            current={"user_id": "admin", "server_id": "remote_138", "role": "admin", "hcode": "0000", "permissions": ["*"]},
            x_auth_context=header,
        )
        inspect = get_inspect_context()
        self.assertIsNotNone(inspect)
        self.assertEqual(inspect.server_id, "remote_153")
        dep = self.deps.require_server_ownership("serverId")
        await dep(_request("GET"), ctx)

    async def test_super_admin_write_sets_inspect_context_and_ownership_bypass(self) -> None:
        from app.core.inspect_context import get_inspect_context

        header = json.dumps(
            {
                "inspect_mode": True,
                "inspect_server_id": "remote_153",
                "inspect_db_name": "chul_05_db",
                "inspect_reason": "장애 점검",
            }
        )
        ctx = await self.deps.get_user_context(
            _request("PATCH", "/api/v1/masters/book/0014", query=b"serverId=remote_153"),
            current={"user_id": "admin", "server_id": "remote_138", "role": "admin", "permissions": ["*"]},
            x_auth_context=header,
        )
        inspect = get_inspect_context()
        self.assertIsNotNone(inspect)
        self.assertEqual(inspect.server_id, "remote_153")
        dep = self.deps.require_server_ownership("serverId")
        await dep(_request("PATCH", "/api/v1/masters/book/0014", query=b"serverId=remote_153"), ctx)

    async def test_inspect_mode_rejects_non_super_user(self) -> None:
        header = json.dumps(
            {
                "inspect_mode": True,
                "inspect_server_id": "remote_153",
                "inspect_db_name": "chul_05_db",
                "inspect_reason": "장애 점검",
            }
        )
        with self.assertRaises(HTTPException) as user_err:
            await self.deps.get_user_context(
                _request("GET"),
                current={"user_id": "u1", "server_id": "remote_138", "role": "operator", "permissions": []},
                x_auth_context=header,
            )
        self.assertEqual(user_err.exception.status_code, 403)

    async def test_inspect_subject_keeps_subject_scope_but_uses_actor_permission_for_read(self) -> None:
        from app.core import db as core_db
        from app.services import auth_service, tenants_directory_service

        old_execute_query = core_db.execute_query
        old_role = auth_service._resolve_role_and_permissions_async
        old_account = auth_service._resolve_account_type
        old_tenants = tenants_directory_service.list_tenants

        async def fake_execute_query(server_id: str, sql: str, params: tuple = ()):
            self.assertEqual(server_id, "remote_153")
            self.assertIn("Id_Logn", sql)
            self.assertEqual(params[0], "u1")
            return [{"gcode": "u1", "hcode": "BR01", "hname": "지점", "gname": "사용자"}]

        async def fake_role(user_id: str, hcode: str, server_id: str):
            return "operator", ["report.read"]

        def fake_account(user_id: str, hcode: str, server_id: str, **kwargs):
            return {
                "account_type": "T3",
                "tenant_id": "tenant-1",
                "account_family": "chul_05",
                "build_role": "publisher",
                "dist_hcode": None,
                "warehouse_menu_tier": "",
                "license_keys": [],
            }

        try:
            core_db.execute_query = fake_execute_query
            auth_service._resolve_role_and_permissions_async = fake_role
            auth_service._resolve_account_type = fake_account
            tenants_directory_service.list_tenants = lambda is_active=True: [
                {
                    "tenant_id": "tenant-1",
                    "tenant_label_kor": "테스트",
                    "primary_server": "remote_153",
                    "db_name_logical": "chul_05_db",
                    "is_active": True,
                }
            ]
            header = json.dumps(
                {
                    "inspect_mode": True,
                    "inspect_server_id": "remote_153",
                    "inspect_db_name": "chul_05_db",
                    "inspect_subject_login_id": "u1",
                    "inspect_subject_hcode": "BR01",
                    "inspect_reason": "사용자 관점 점검",
                }
            )
            ctx = await self.deps.get_user_context(
                _request("GET"),
                current={
                    "user_id": "admin",
                    "server_id": "remote_138",
                    "role": "admin",
                    "hcode": "0000",
                    "permissions": ["*"],
                },
                x_auth_context=header,
            )
        finally:
            core_db.execute_query = old_execute_query
            auth_service._resolve_role_and_permissions_async = old_role
            auth_service._resolve_account_type = old_account
            tenants_directory_service.list_tenants = old_tenants

        self.assertEqual(ctx["user_id"], "u1")
        self.assertEqual(ctx["permissions"], ["report.read"])
        self.assertEqual(ctx["inspect_actor_user_id"], "admin")
        self.assertTrue(ctx["inspect_actor_is_super"])
        self.assertTrue(self.deps._has_permission(ctx, "admin.user.write"))

    def test_inspect_actor_super_signal_allows_ownership_bypass_after_subject_overlay(self) -> None:
        ctx = {
            "user_id": "u1",
            "server_id": "remote_153",
            "role": "operator",
            "hcode": "BR01",
            "permissions": ["report.read"],
            "inspect_actor_is_super": True,
            "inspect_actor": {
                "user_id": "admin",
                "server_id": "remote_138",
                "role": "admin",
                "hcode": "0000",
                "permissions": ["*"],
            },
        }
        self.deps.assert_server_ownership(ctx, "remote_138", allow_super=True, operation="GET /api/v1/example")


class AdminInspectStaticTests(TestCase):
    def test_db_override_and_frontend_get_only_context_are_present(self) -> None:
        db_src = (BACKEND / "app" / "core" / "db.py").read_text(encoding="utf-8")
        api_src = (FE / "lib" / "api-client.ts").read_text(encoding="utf-8")
        inspect_ctx_src = (FE / "lib" / "admin-inspect-context.ts").read_text(encoding="utf-8")
        print_src = (FE / "lib" / "print-api.ts").read_text(encoding="utf-8")
        dashboard_src = (FE / "lib" / "dashboard-widget-advanced.ts").read_text(encoding="utf-8")
        super_src = (FE / "app" / "(app)" / "admin" / "super" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("_effective_database", db_src)
        self.assertIn("get_inspect_context", db_src)
        self.assertIn("shouldAttachInspectContext", api_src)
        self.assertIn('p.startsWith("/api/v1/auth/")', api_src)
        self.assertIn('p.startsWith("/api/v1/admin/")', api_src)
        self.assertIn("rewriteServerIdForInspect", api_src)
        self.assertIn("rewriteBodyServerIdsForInspect", api_src)
        self.assertIn("adminInspectHeaders", print_src)
        self.assertIn("rewriteServerIdForInspect", print_src)
        self.assertIn("adminInspectHeaders", dashboard_src)
        self.assertIn("rewriteServerIdForInspect", dashboard_src)
        self.assertIn("inspect_subject_login_id", inspect_ctx_src)
        self.assertIn("/admin/account-directory", super_src)
        self.assertIn("listInspectLoginCandidates", super_src)
        self.assertIn("이 계정 관점으로 점검", (FE / "app" / "(app)" / "admin" / "account-directory" / "page.tsx").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(verbosity=2)

