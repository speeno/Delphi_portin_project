"""admin 사용자별 메뉴 노출(MENUVIS-DEC-07) API + Id_Logn 4-key gcode 가드 회귀."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import get_user_context
from app.main import app
from app.services import user_menu_visibility_service


def _ctx_user() -> dict:
    return {
        "user_id": "u-user",
        "server_id": "remote_153",
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
        "role": "admin",
        "hcode": "0000",
        "permissions": ["*"],
        "account_type": "T1",
    }


def _client(ctx_func) -> TestClient:
    app.dependency_overrides[get_user_context] = ctx_func
    return TestClient(app)


def _cleanup(client: TestClient) -> None:
    client.close()
    app.dependency_overrides.pop(get_user_context, None)


def _point_store(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(user_menu_visibility_service, "STORE_PATH", tmp_path / "umv.json")


def test_menu_visibility_requires_super(tmp_path, monkeypatch):
    _point_store(tmp_path, monkeypatch)
    c = _client(_ctx_user)
    try:
        res = c.get(
            "/api/v1/admin/users/menu-visibility",
            params={"serverId": "remote_153", "hcode": "5019", "gcode": "gyomunsa"},
        )
        assert res.status_code == 403
    finally:
        _cleanup(c)


def test_menu_visibility_put_get_and_clear(tmp_path, monkeypatch):
    _point_store(tmp_path, monkeypatch)
    c = _client(_ctx_super)
    try:
        put = c.put(
            "/api/v1/admin/users/menu-visibility",
            json={
                "serverId": "remote_153",
                "hcode": "5019",
                "gcode": "gyomunsa",
                "gname": "교문사",
                "hidden_menu_ids": ["ACC-MENU-MASTERS-02"],
            },
        )
        assert put.status_code == 200
        assert put.json()["hidden_menu_ids"] == ["ACC-MENU-MASTERS-02"]

        get = c.get(
            "/api/v1/admin/users/menu-visibility",
            params={"serverId": "remote_153", "hcode": "5019", "gcode": "gyomunsa"},
        )
        assert get.status_code == 200
        assert get.json()["hidden_menu_ids"] == ["ACC-MENU-MASTERS-02"]

        # 동일 hcode·다른 gcode 는 분리된다.
        other = c.get(
            "/api/v1/admin/users/menu-visibility",
            params={"serverId": "remote_153", "hcode": "5019", "gcode": "accounting"},
        )
        assert other.json()["hidden_menu_ids"] == []

        # 빈 목록 = 전체 노출 복귀 (행 제거)
        clr = c.put(
            "/api/v1/admin/users/menu-visibility",
            json={"serverId": "remote_153", "hcode": "5019", "gcode": "gyomunsa", "hidden_menu_ids": []},
        )
        assert clr.status_code == 200
        assert clr.json()["hidden_menu_ids"] == []
    finally:
        _cleanup(c)


def test_menu_visibility_rejects_bad_menu_id(tmp_path, monkeypatch):
    _point_store(tmp_path, monkeypatch)
    c = _client(_ctx_super)
    try:
        res = c.put(
            "/api/v1/admin/users/menu-visibility",
            json={"serverId": "r", "hcode": "h", "gcode": "g", "hidden_menu_ids": ["bad"]},
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "INVALID_USER_MENU_VISIBILITY"
    finally:
        _cleanup(c)


def test_id_logn_permissions_gcode_mismatch_blocked(monkeypatch):
    """4-key 정합 alias — 잘못된 gcode 로 동일 hcode 사용자를 수정하면 422."""
    import app.services.id_logn_service as id_logn_service

    importlib.reload(id_logn_service)
    seed = id_logn_service.get_user("BR01")
    assert seed is not None, "BR01 시드 사용자 필요"
    c = _client(_ctx_super)
    try:
        res = c.put(
            "/api/v1/admin/id-logn/BR01/permissions",
            params={"gcode": "wrong_gcode"},
            headers={"If-Match": seed["etag"]},
            json={"matrix": {"F11": "R"}},
        )
        assert res.status_code == 422
        assert res.json()["detail"]["code"] == "ID_LOGN_GCODE_MISMATCH"
    finally:
        _cleanup(c)
