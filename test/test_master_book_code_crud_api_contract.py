"""
C9 Sobo38 도서코드 — /masters/book-code thin alias 회귀 (v1.4.0).

신규 SQL 0 — 내부에서 G4_Book ``create_book`` / ``update_book`` / ``delete_book`` 재사용.
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
        "user_id": "t_bc",
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


class BookCodeAliasCrudTests(TestCase):
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

    def test_post_book_code_delegates_to_create_book(self) -> None:
        async def fake_create(*, server_id: str, payload: dict) -> dict:  # noqa: ARG001
            self.assertEqual(payload.get("gcode"), "B888")
            return {"gcode": "B888", "created_at": "2026-05-08T00:00:00Z"}

        with patch.object(masters_service, "create_book", side_effect=fake_create):
            r = self.client.post(
                "/api/v1/masters/book-code",
                json={"serverId": _SID, "gcode": "B888", "gname": "별칭등록테스트"},
            )
        self.assertEqual(r.status_code, 201, r.text)
        self.assertEqual(r.json().get("gcode"), "B888")


class BookCodeCrudStatic(TestCase):
    def test_router_tokens(self) -> None:
        src = (BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        for token in (
            '@router.get("/book-code/{gcode}"',
            "async def create_book_code",
            "async def update_book_code",
            "async def delete_book_code",
            'entity="book_code"',
            '"via": "book"',
        ):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
