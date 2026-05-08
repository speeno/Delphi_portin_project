"""
C9 Sobo17 출판사 마스터 CRUD 회귀 — v1.4.0 (G7_Ggeo).

- POST/PATCH/DELETE 라우트 + ``require_permission('master.write')`` 가드
- 서비스는 monkeypatch 로 DB 부작용 없이 검증
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import masters_service  # noqa: E402

_SID = "remote_138"


def _user_write() -> dict:
    return {
        "user_id": "t_pub",
        "server_id": _SID,
        "role": "operator",
        "hcode": "BR01",
        "permissions": ["master.write"],
    }


async def _override_user() -> dict:
    return _user_write()


async def _override_ctx() -> dict:
    u = _user_write()
    return {
        "user_id": u["user_id"],
        "server_id": u["server_id"],
        "role": u["role"],
        "hcode": u["hcode"],
        "branch_id": u["hcode"],
        "permissions": list(u["permissions"]),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "",
        "dist_hcode": "",
    }


async def _override_user_no_write() -> dict:
    u = _user_write()
    return {**u, "permissions": ["master.customer.read"]}


async def _override_ctx_no_write() -> dict:
    u = await _override_user_no_write()
    return {
        "user_id": u["user_id"],
        "server_id": u["server_id"],
        "role": u["role"],
        "hcode": u["hcode"],
        "branch_id": u["hcode"],
        "permissions": list(u["permissions"]),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "",
        "dist_hcode": "",
    }


class PublisherCrudRouterTests(TestCase):
    def setUp(self) -> None:
        self._prev_user = app.dependency_overrides.get(get_current_user)
        self._prev_ctx = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _override_user
        app.dependency_overrides[get_user_context] = _override_ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev_user is not None:
            app.dependency_overrides[get_current_user] = self._prev_user
        else:
            app.dependency_overrides.pop(get_current_user, None)
        if self._prev_ctx is not None:
            app.dependency_overrides[get_user_context] = self._prev_ctx
        else:
            app.dependency_overrides.pop(get_user_context, None)

    def test_post_publisher_calls_service(self) -> None:
        async def fake_create(*, server_id: str, payload: dict) -> dict:  # noqa: ARG001
            self.assertEqual(server_id, _SID)
            self.assertEqual(payload.get("gcode"), "P999")
            return {"gcode": "P999", "created_at": "2026-05-08T00:00:00Z"}

        with patch.object(masters_service, "create_publisher_master", side_effect=fake_create):
            r = self.client.post(
                "/api/v1/masters/publisher",
                json={"serverId": _SID, "gcode": "P999", "gname": "테스트출판"},
            )
        self.assertEqual(r.status_code, 201, r.text)
        self.assertEqual(r.json().get("gcode"), "P999")

    def test_post_forbidden_without_master_write(self) -> None:
        prev_u = app.dependency_overrides.get(get_current_user)
        prev_c = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _override_user_no_write
        app.dependency_overrides[get_user_context] = _override_ctx_no_write
        try:
            r = self.client.post(
                "/api/v1/masters/publisher",
                json={"serverId": _SID, "gcode": "P998", "gname": "x"},
            )
        finally:
            if prev_u is not None:
                app.dependency_overrides[get_current_user] = prev_u
            else:
                app.dependency_overrides.pop(get_current_user, None)
            if prev_c is not None:
                app.dependency_overrides[get_user_context] = prev_c
            else:
                app.dependency_overrides.pop(get_user_context, None)
        self.assertEqual(r.status_code, 403, r.text)


class PublisherCrudStatic(TestCase):
    def test_router_tokens(self) -> None:
        src = (BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        for token in (
            '@router.get("/publisher/{gcode}"',
            "async def create_publisher_master_route",
            "async def update_publisher_master_route",
            "async def delete_publisher_master_route",
            "require_permission",
            "_MASTER_WRITE_PERM",
        ):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
