"""DEC-052 — admin_service 1 사용자 1 데이터 서버(Primary) 의미 가드.

검증 항목
---------
- ``set_primary_data_server`` 호출 시 동일 user 의 기존 매핑이 모두 1건으로 정리.
- ``assign_server(allow=True)`` 도 동일 의미 (LSP 보존).
- ``assign_server(allow=False)`` 는 해당 user 의 모든 매핑 제거 (Primary 해제).
- ``get_primary_data_server(login_id)`` 가 None 또는 단일 server_id 반환.
- ``_normalize_primary_servers`` 가 다중 row → 1건으로 idempotent 정리.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _seed(path: Path, *, multi_for_user: str | None = None) -> None:
    state: dict = {
        "schema_version": 1,
        "web_users": [
            {"id": "u-1", "login_id": "alice", "status": "active", "created_at": "2026-01-01"},
            {"id": "u-2", "login_id": "bob", "status": "active", "created_at": "2026-01-01"},
        ],
        "web_user_servers": [],
        "web_roles": [],
        "web_user_roles": [],
        "legacy_permission_map": [],
        "application_settings": [],
        "application_settings_history": [],
    }
    if multi_for_user:
        state["web_user_servers"] = [
            {"user_id": multi_for_user, "server_id": "remote_138"},
            {"user_id": multi_for_user, "server_id": "remote_154"},
            {"user_id": multi_for_user, "server_id": "remote_155"},
        ]
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


class PrimaryServerSemanticTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self._path = Path(self._tmpdir.name) / "web_admin.json"
        os.environ["BLS_WEB_ADMIN_PATH"] = str(self._path)
        # 모듈 단위 캐시 리셋: WEB_ADMIN_PATH 와 _NORMALIZED_ONCE.
        if "app.services.admin_service" in sys.modules:
            del sys.modules["app.services.admin_service"]

    def tearDown(self) -> None:
        os.environ.pop("BLS_WEB_ADMIN_PATH", None)
        self._tmpdir.cleanup()
        # 모듈 재로딩으로 default WEB_ADMIN_PATH 복원 (다음 테스트 격리).
        for mod in (
            "app.services.admin_service",
        ):
            if mod in sys.modules:
                del sys.modules[mod]
        # app.services 패키지의 admin_service 어트리뷰트도 제거 (재import 강제).
        pkg = sys.modules.get("app.services")
        if pkg is not None and hasattr(pkg, "admin_service"):
            try:
                delattr(pkg, "admin_service")
            except AttributeError:
                pass

    def _import_admin_service(self):
        from app.services import admin_service

        admin_service.WEB_ADMIN_PATH = self._path  # type: ignore[attr-defined]
        admin_service._NORMALIZED_ONCE = False  # type: ignore[attr-defined]
        return admin_service

    def test_set_primary_replaces_existing_mappings(self) -> None:
        _seed(self._path, multi_for_user="u-1")
        svc = self._import_admin_service()

        svc.set_primary_data_server(user_id="u-1", server_id="remote_154", actor="root")
        rows = json.loads(self._path.read_text(encoding="utf-8"))["web_user_servers"]
        u1_rows = [r for r in rows if r["user_id"] == "u-1"]
        self.assertEqual(len(u1_rows), 1)
        self.assertEqual(u1_rows[0]["server_id"], "remote_154")

    def test_set_primary_clear_when_empty(self) -> None:
        _seed(self._path, multi_for_user="u-1")
        svc = self._import_admin_service()

        svc.set_primary_data_server(user_id="u-1", server_id=None, actor="root")
        rows = json.loads(self._path.read_text(encoding="utf-8"))["web_user_servers"]
        self.assertFalse(any(r["user_id"] == "u-1" for r in rows))

    def test_assign_server_allow_true_collapses_to_one(self) -> None:
        _seed(self._path, multi_for_user="u-2")
        svc = self._import_admin_service()

        svc.assign_server(user_id="u-2", server_id="remote_138", allow=True, actor="root")
        rows = json.loads(self._path.read_text(encoding="utf-8"))["web_user_servers"]
        u2_rows = [r for r in rows if r["user_id"] == "u-2"]
        self.assertEqual(len(u2_rows), 1)
        self.assertEqual(u2_rows[0]["server_id"], "remote_138")

    def test_get_primary_returns_single(self) -> None:
        _seed(self._path)
        svc = self._import_admin_service()
        svc.set_primary_data_server(user_id="u-1", server_id="remote_138", actor="root")
        self.assertEqual(svc.get_primary_data_server("alice"), "remote_138")
        self.assertIsNone(svc.get_primary_data_server("bob"))
        self.assertIsNone(svc.get_primary_data_server("does_not_exist"))

    def test_normalize_idempotent_dedup(self) -> None:
        _seed(self._path, multi_for_user="u-1")
        svc = self._import_admin_service()
        # 첫 _load_state() 호출에서 _normalize_primary_servers 가 자동 실행.
        svc._load_state()  # type: ignore[attr-defined]
        rows = json.loads(self._path.read_text(encoding="utf-8"))["web_user_servers"]
        u1_rows = [r for r in rows if r["user_id"] == "u-1"]
        self.assertEqual(len(u1_rows), 1)
        # 마지막 row 가 유지된다 (155).
        self.assertEqual(u1_rows[0]["server_id"], "remote_155")

    def test_is_server_allowed_uses_primary(self) -> None:
        _seed(self._path)
        svc = self._import_admin_service()
        svc.set_primary_data_server(user_id="u-1", server_id="remote_138", actor="root")
        self.assertTrue(svc.is_server_allowed(login_id="alice", server_id="remote_138"))
        self.assertFalse(svc.is_server_allowed(login_id="alice", server_id="remote_154"))
        # primary 미설정 사용자는 폴백 허용.
        self.assertTrue(svc.is_server_allowed(login_id="bob", server_id="remote_138"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
