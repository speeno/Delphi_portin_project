"""inspect/login-candidates — 페이지 행만 account 메타 해석 (전량 수집 시 resolve 남발 방지)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import get_user_context
from app.main import app
from app.routers import admin as admin_router
from app.services import auth_service


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


@pytest.fixture
def inspect_candidates_mocks(monkeypatch):
    """인덱스 비우고 단일 DB에서 Id_Logn 120행 반환."""

    async def fake_ready(_sid: str):
        return ["book_db"]

    async def fake_execute(sid: str, sql: str, params: object | None = None):
        s = sql or ""
        if "FROM `book_db`.Id_Logn" in s:
            return [
                {"gcode": f"u{i:03}", "hcode": "H1", "hname": "", "gname": ""} for i in range(120)
            ]
        return []

    monkeypatch.setattr(admin_router, "_account_directory_ready_db_names", fake_ready)
    monkeypatch.setattr(admin_router, "execute_query", fake_execute)
    monkeypatch.setattr(
        admin_router.login_id_index_service,
        "list_candidates_by_server",
        lambda server_id, q="", limit=500: [],
    )
    monkeypatch.setattr(
        admin_router.tenants_directory_service,
        "list_tenants",
        lambda **kw: [
            {
                "tenant_id": "t1",
                "tenant_label_kor": "테넌트",
                "account_family": "af",
                "primary_server": "서버3",
                "db_name_logical": "book_db",
                "is_active": True,
            }
        ],
    )


def test_resolve_account_type_only_per_page_rows(inspect_candidates_mocks, monkeypatch):
    """페이지 크기만큼만 _resolve_account_type 호출 (offset 변경 시에도 수집 건수만큼이 아님)."""
    calls = {"n": 0}

    def fake_resolve(gcode: str, hcode: str, server_id: str, resolved_db: str = ""):
        calls["n"] += 1
        return {
            "tenant_id": "t1",
            "account_family": "af",
            "account_type": "T3",
            "build_role": "publisher",
            "warehouse_menu_tier": "",
            "dist_hcode": None,
        }

    monkeypatch.setattr(auth_service, "_resolve_account_type", fake_resolve)

    c = _client()
    try:
        r1 = c.get(
            "/api/v1/admin/inspect/login-candidates",
            params={"serverId": "remote_153", "offset": 0, "limit": 10},
        )
        assert r1.status_code == 200
        assert r1.json()["total"] == 120
        assert calls["n"] == 10

        calls["n"] = 0
        r2 = c.get(
            "/api/v1/admin/inspect/login-candidates",
            params={"serverId": "remote_153", "offset": 50, "limit": 10},
        )
        assert r2.status_code == 200
        assert r2.json()["total"] == 120
        assert calls["n"] == 10
    finally:
        _cleanup(c)
