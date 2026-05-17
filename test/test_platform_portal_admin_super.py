"""플랫폼 공지 관리 API — 수퍼관리자 가드."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import platform_portal_service as pps  # noqa: E402


def _super_ctx() -> dict:
    return {
        "user_id": "super1",
        "server_id": "remote_138",
        "role": "admin",
        "hcode": "0000",
        "branch_id": "0000",
        "permissions": ["admin.user.write"],
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "T1",
        "dist_hcode": "",
    }


def _operator_ctx() -> dict:
    return {
        "user_id": "op1",
        "server_id": "remote_138",
        "role": "operator",
        "hcode": "H0001",
        "branch_id": "H0001",
        "permissions": [],
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "T3",
        "dist_hcode": "",
    }


class PlatformPortalAdminTests(TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self._path = Path(self._tmpdir.name) / "platform_portal.json"
        self._prev = pps.PORTAL_PATH
        pps.PORTAL_PATH = self._path
        pps._save(pps._empty_state())

        self._prev_user = app.dependency_overrides.get(get_current_user)
        self._prev_ctx = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = lambda: {"user_id": "super1"}
        app.dependency_overrides[get_user_context] = lambda: _super_ctx()
        self.client = TestClient(app)

    def tearDown(self) -> None:
        pps.PORTAL_PATH = self._prev
        self._tmpdir.cleanup()
        if self._prev_user is not None:
            app.dependency_overrides[get_current_user] = self._prev_user
        else:
            app.dependency_overrides.pop(get_current_user, None)
        if self._prev_ctx is not None:
            app.dependency_overrides[get_user_context] = self._prev_ctx
        else:
            app.dependency_overrides.pop(get_user_context, None)

    def test_non_super_forbidden(self) -> None:
        app.dependency_overrides[get_user_context] = lambda: _operator_ctx()
        r = self.client.get("/api/v1/admin/platform-portal")
        self.assertEqual(r.status_code, 403, r.text)
        app.dependency_overrides[get_user_context] = lambda: _super_ctx()

    def test_slogan_and_notice_crud(self) -> None:
        r = self.client.put(
            "/api/v1/admin/platform-portal/slogan",
            json={"headline": "새 슬로건", "subline": "새 부제"},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["headline"], "새 슬로건")

        r2 = self.client.post(
            "/api/v1/admin/platform-portal/notices",
            json={
                "title": "신규 공지",
                "summary": "요약",
                "body": "본문",
                "severity": "info",
                "is_published": True,
            },
        )
        self.assertEqual(r2.status_code, 201, r2.text)
        nid = r2.json()["id"]

        r3 = self.client.get("/api/v1/public/notices/" + nid)
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(r3.json()["title"], "신규 공지")

        r4 = self.client.delete(f"/api/v1/admin/platform-portal/notices/{nid}")
        self.assertEqual(r4.status_code, 204)
        r5 = self.client.get("/api/v1/public/notices/" + nid)
        self.assertEqual(r5.status_code, 404)


if __name__ == "__main__":
    main()
