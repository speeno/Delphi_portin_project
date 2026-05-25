"""계정 디렉토리 admin API — Id_Logn 없는 DB는 목록에서 제외 (1146 회귀 방지)."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import get_user_context
from app.main import app
from app.routers import admin as admin_router


def _ctx_super() -> dict:
    return {
        "user_id": "u-admin",
        "gcode": "admin",
        "server_id": "remote_153",
        "tenant_id": "tenant_a",
        "role": "admin",
        "hcode": "0000",
        "permissions": ["admin.user.read", "admin.user.write"],
        "account_type": "T1",
    }


def _client() -> TestClient:
    app.dependency_overrides[get_user_context] = _ctx_super
    return TestClient(app)


def _cleanup(client: TestClient) -> None:
    client.close()
    app.dependency_overrides.pop(get_user_context, None)


async def _fake_execute_account_directory_dbs(sid: str, sql: str, params: object | None = None):
    s = (sql or "").strip()
    if s.upper().startswith("SHOW DATABASES"):
        return [{"Database": "good_db"}, {"Database": "bad_db"}]
    if "SHOW TABLES FROM `bad_db`" in s:
        return [{"Tables_in_bad": "orders"}]
    if "SHOW TABLES FROM `good_db`" in s:
        return [{"Tables_in_good": "Id_Logn"}]
    return []


def test_account_directory_databases_only_lists_schemas_with_id_logn(monkeypatch):
    monkeypatch.setattr(admin_router, "get_server_profile", lambda sid: {"database": "bad_db"})
    monkeypatch.setattr(
        admin_router.tenants_directory_service,
        "list_tenants",
        lambda **kw: [
            {
                "tenant_label_kor": "교문사",
                "primary_server": "서버3",
                "db_name_logical": "good_db",
                "default_account_type": "T3",
                "build_role": "warehouse_publisher",
                "account_family": "chul_09",
                "is_active": True,
            },
            {
                "tenant_label_kor": "없는 DB",
                "primary_server": "서버3",
                "db_name_logical": "bad_db",
                "default_account_type": "T3",
                "build_role": "publisher",
                "account_family": "book_01",
                "is_active": True,
            },
        ],
    )
    monkeypatch.setattr(admin_router.account_directory_overlay_service, "list_overrides", lambda **kw: [])
    monkeypatch.setattr(admin_router, "execute_query", _fake_execute_account_directory_dbs)

    c = _client()
    try:
        res = c.get("/api/v1/admin/account-directory/databases", params={"serverId": "remote_153"})
        assert res.status_code == 200
        body = res.json()
        assert body["databases"] == ["good_db"]
        assert body["database_meta"] == [
            {
                "db_name": "good_db",
                "server_id": "remote_153",
                "tenant_labels": ["교문사"],
                "account_types": ["T3"],
                "build_roles": ["warehouse_publisher"],
                "account_families": ["chul_09"],
                "has_id_logn": True,
            }
        ]
    finally:
        _cleanup(c)


async def _fake_execute_users_friendly_1146(sid: str, sql: str, params: object | None = None):
    if "Id_Logn" in (sql or ""):
        raise Exception('(1146, "Table \'book_01_db.Id_Logn\' doesn\'t exist")')
    return []


def test_account_directory_users_maps_1146_to_clear_message(monkeypatch):
    monkeypatch.setattr(admin_router, "execute_query", _fake_execute_users_friendly_1146)

    c = _client()
    try:
        res = c.get(
            "/api/v1/admin/account-directory/users",
            params={"serverId": "remote_153", "dbName": "book_01_db"},
        )
        assert res.status_code == 422
        msg = res.json()["detail"]["message"]
        assert "Id_Logn" in msg
        assert "1146" not in msg
    finally:
        _cleanup(c)


def test_account_directory_override_accepts_login_profile(monkeypatch):
    captured: dict[str, object] = {}

    def _fake_upsert_override(**kwargs):
        captured.update(kwargs)
        return kwargs

    monkeypatch.setattr(
        admin_router.account_directory_overlay_service,
        "upsert_override",
        _fake_upsert_override,
    )
    monkeypatch.setattr(
        admin_router.publisher_whitelist_service,
        "count_active_children",
        lambda *_args, **_kwargs: 0,
    )

    c = _client()
    try:
        res = c.patch(
            "/api/v1/admin/account-directory/users/%EA%B2%BD%EB%A6%AC%EB%B6%80",
            json={
                "serverId": "remote_153",
                "dbName": "chul_09_db",
                "hcode": "5039",
                "accountType": "T3",
                "buildRole": "warehouse_publisher",
                "loginProfile": "department_accounting",
                "notes": "menu profile override",
            },
        )
        assert res.status_code == 200
        assert captured["login_profile"] == "department_accounting"
        assert captured["gcode"] == "경리부"
    finally:
        _cleanup(c)


def test_id_logn_menu_profile_preview_returns_inferred_profile(monkeypatch):
    monkeypatch.setattr(
        admin_router.id_logn_service,
        "get_user",
        lambda hcode: {"hcode": hcode, "permissions": {"F51": "R", "F11": ""}},
    )
    monkeypatch.setattr(
        admin_router.auth_service,
        "infer_login_profile",
        lambda matrix: "department_accounting" if matrix.get("F51") else "publisher_main",
    )
    monkeypatch.setattr(
        admin_router.auth_service,
        "menu_shell_hint_for_login_profile",
        lambda profile: "accounting_only" if profile == "department_accounting" else "default",
    )

    c = _client()
    try:
        res = c.get("/api/v1/admin/id-logn/5039/menu-profile-preview")
        assert res.status_code == 200
        body = res.json()
        assert body["inferred_login_profile"] == "department_accounting"
        assert body["effective_login_profile"] == "department_accounting"
        assert body["menu_shell_hint"] == "accounting_only"
    finally:
        _cleanup(c)
