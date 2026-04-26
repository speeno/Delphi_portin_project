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
                "tenant_labels": ["교문사"],
                "account_types": ["T3"],
                "build_roles": ["warehouse_publisher"],
                "account_families": ["chul_09"],
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
