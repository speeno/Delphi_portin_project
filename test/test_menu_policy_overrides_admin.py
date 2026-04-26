"""admin menu-policy overrides API 회귀 가드."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import get_user_context
from app.main import app
from app.services import menu_policy_overrides_service


def _ctx_user() -> dict:
    return {
        "user_id": "u-user",
        "server_id": "remote_153",
        "tenant_id": "tenant_a",
        "role": "operator",
        "hcode": "D100",
        "permissions": ["admin.user.read", "admin.user.write"],
        "account_type": "T2_PUB",
    }


def _ctx_super() -> dict:
    return {
        "user_id": "u-admin",
        "gcode": "admin",
        "server_id": "remote_153",
        "tenant_id": "tenant_a",
        "role": "admin",
        "hcode": "0000",
        "permissions": ["*"],
        "account_type": "T1",
    }


def _client_with_ctx(ctx_func):
    app.dependency_overrides[get_user_context] = ctx_func
    return TestClient(app)


def _cleanup_client(client: TestClient) -> None:
    client.close()
    app.dependency_overrides.pop(get_user_context, None)


def test_menu_policy_overrides_super_only(tmp_path, monkeypatch):
    monkeypatch.setattr(menu_policy_overrides_service, "OVERRIDES_PATH", tmp_path / "overrides.json")
    c = _client_with_ctx(_ctx_user)
    try:
        res = c.get("/api/v1/admin/menu-policy/overrides")
        assert res.status_code == 403
        assert res.json()["detail"]["code"] == "PERMISSION_DENIED"
    finally:
        _cleanup_client(c)


def test_menu_policy_overrides_roundtrip_and_audit(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(menu_policy_overrides_service, "OVERRIDES_PATH", tmp_path / "overrides.json")
    c = _client_with_ctx(_ctx_super)
    payload = {
        "schema_version": "1.0.0",
        "rows": [
            {
                "menu_id": "ACC-MENU-NAV-01",
                "account_type": "T2_PUB",
                "visibility": "deny",
                "crud": {"read": "deny", "create": "inherit"},
            }
        ],
    }
    try:
        with caplog.at_level(logging.INFO, logger="audit.admin"):
            put = c.put("/api/v1/admin/menu-policy/overrides", json=payload)
        assert put.status_code == 200
        body = put.json()
        assert body["success"] is True
        assert body["row_count"] == 1
        assert body["doc"]["rows"][0]["crud"] == {"read": "deny"}
        assert "admin.menu_policy.override.save" in caplog.text

        get = c.get("/api/v1/admin/menu-policy/overrides")
        assert get.status_code == 200
        assert get.json()["rows"] == body["doc"]["rows"]
        saved = json.loads((tmp_path / "overrides.json").read_text(encoding="utf-8"))
        assert saved["rows"] == body["doc"]["rows"]
    finally:
        _cleanup_client(c)


def test_menu_policy_overrides_invalid_visibility_422(tmp_path, monkeypatch):
    monkeypatch.setattr(menu_policy_overrides_service, "OVERRIDES_PATH", tmp_path / "overrides.json")
    c = _client_with_ctx(_ctx_super)
    try:
        res = c.put(
            "/api/v1/admin/menu-policy/overrides",
            json={
                "rows": [
                    {
                        "menu_id": "ACC-MENU-NAV-01",
                        "account_type": "T2_PUB",
                        "visibility": "yes",
                    }
                ]
            },
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "INVALID_MENU_POLICY_OVERRIDES"
    finally:
        _cleanup_client(c)


def test_menu_policy_overrides_empty_doc_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(menu_policy_overrides_service, "OVERRIDES_PATH", tmp_path / "overrides.json")
    c = _client_with_ctx(_ctx_super)
    try:
        put = c.put("/api/v1/admin/menu-policy/overrides", json={"schema_version": "1.0.0", "rows": []})
        assert put.status_code == 200
        assert put.json()["row_count"] == 0
        get = c.get("/api/v1/admin/menu-policy/overrides")
        assert get.status_code == 200
        assert get.json() == {"schema_version": "1.0.0", "rows": []}
    finally:
        _cleanup_client(c)
