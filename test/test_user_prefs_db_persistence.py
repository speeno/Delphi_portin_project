"""내정보 preferences DB 영속화(Web_User_Prefs) 회귀 가드.

배경: 파일 저장(backend/data/user_profiles.json)만으로는 Render 임시 FS 에서
재배포마다 설정이 리셋됨(2026-07-03 "자동출력 설정 저장 안 됨" 보고).
grid_prefs_service 패턴(사이드 테이블 + REPLACE INTO, 3.23 호환)으로 DB 정본화.

가드: (1) PATCH 이중 기록(파일+DB), (2) GET 시 DB 정본 → 파일 캐시 동기화,
(3) DB 무행 + 파일 저장분 존재 시 1회 back-fill, (4) SQL hcode 격리, (5) graceful 실패.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers import me as me_router  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import user_prefs_db, user_profile_service  # noqa: E402

_SID = "remote_1"


def _auth() -> dict:
    return {"user_id": "u1", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": []}


class ServiceSqlShapeTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        user_prefs_db.clear_ensured_for_tests()

    async def test_put_replace_into_with_hcode_isolation(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            captured.append((sql, params))
            return []

        with patch.object(user_prefs_db, "execute_query", side_effect=fake_eq):
            ok = await user_prefs_db.put_user_prefs(
                server_id=_SID, hcode="H1", user_id="u1", prefs={"sales_statement_auto_print": True},
            )
        self.assertTrue(ok)
        rep_sql, rep_params = captured[-1]
        self.assertIn("REPLACE INTO Web_User_Prefs", rep_sql)
        self.assertEqual(rep_params[0], "H1")  # hcode 격리
        self.assertEqual(rep_params[1], "u1")
        self.assertIn("auto_print", rep_params[2])

    async def test_get_select_filters_hcode_and_user(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            captured.append((sql, params))
            if sql.strip().upper().startswith("SELECT"):
                return [{"Prefs": '{"ui_theme":"lime"}'}]
            return []

        with patch.object(user_prefs_db, "execute_query", side_effect=fake_eq):
            prefs = await user_prefs_db.get_user_prefs(server_id=_SID, hcode="H1", user_id="u1")
        self.assertEqual(prefs, {"ui_theme": "lime"})
        sel = next(c for c in captured if c[0].strip().upper().startswith("SELECT"))
        self.assertIn("WHERE Hcode=%s AND UserId=%s", sel[0])
        self.assertEqual(sel[1], ("H1", "u1"))

    async def test_get_returns_none_on_db_failure(self) -> None:
        async def boom(*a, **k):  # noqa: ANN001, ARG001
            raise RuntimeError("db down")

        with patch.object(user_prefs_db, "execute_query", side_effect=boom):
            self.assertIsNone(
                await user_prefs_db.get_user_prefs(server_id=_SID, hcode="H1", user_id="u1")
            )

    async def test_put_false_on_db_failure(self) -> None:
        async def boom(*a, **k):  # noqa: ANN001, ARG001
            raise RuntimeError("db down")

        with patch.object(user_prefs_db, "execute_query", side_effect=boom):
            ok = await user_prefs_db.put_user_prefs(
                server_id=_SID, hcode="H1", user_id="u1", prefs={"a": 1},
            )
        self.assertFalse(ok)


class RouterDbSyncTests(TestCase):
    def setUp(self) -> None:
        self._prev = app.dependency_overrides.get(get_current_user)
        app.dependency_overrides[get_current_user] = _auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev is not None:
            app.dependency_overrides[get_current_user] = self._prev
        else:
            app.dependency_overrides.pop(get_current_user, None)

    def test_patch_writes_file_and_db(self) -> None:
        file_calls: list[tuple] = []
        db_put = AsyncMock(return_value=True)

        def fake_set(sid, uid, prefs):  # noqa: ANN001
            file_calls.append((sid, uid, prefs))

        with patch.object(me_router.user_profile_service, "set_preferences", side_effect=fake_set), \
                patch.object(me_router.user_profile_service, "get_profile",
                             return_value={"preferences": {}, "logo_relpath": ""}), \
                patch.object(me_router.user_prefs_db, "put_user_prefs", db_put):
            r = self.client.patch(
                "/api/v1/me/profile",
                json={"preferences": {"sales_statement_auto_print": True}},
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(file_calls[0][2], {"sales_statement_auto_print": True})
        db_put.assert_awaited_once()
        self.assertEqual(
            db_put.await_args.kwargs["prefs"], {"sales_statement_auto_print": True},
        )
        self.assertEqual(db_put.await_args.kwargs["hcode"], "H1")

    def test_get_db_hit_syncs_file_cache(self) -> None:
        synced: list[tuple] = []

        def fake_set(sid, uid, prefs):  # noqa: ANN001
            synced.append((sid, uid, prefs))

        with patch.object(me_router.user_prefs_db, "get_user_prefs",
                          AsyncMock(return_value={"sales_statement_auto_print": True})), \
                patch.object(me_router.user_profile_service, "set_preferences", side_effect=fake_set), \
                patch.object(me_router.user_profile_service, "get_profile",
                             return_value={"preferences": {"sales_statement_auto_print": True}, "logo_relpath": ""}):
            r = self.client.get("/api/v1/me/profile")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(synced[0][2], {"sales_statement_auto_print": True})  # DB → 파일 캐시
        self.assertTrue(r.json()["preferences"]["sales_statement_auto_print"])

    def test_get_backfills_db_from_legacy_file_prefs(self) -> None:
        db_put = AsyncMock(return_value=True)
        with patch.object(me_router.user_prefs_db, "get_user_prefs", AsyncMock(return_value=None)), \
                patch.object(me_router.user_prefs_db, "put_user_prefs", db_put), \
                patch.object(me_router.user_profile_service, "get_profile",
                             return_value={"preferences": {"ui_theme": "sky"}, "logo_relpath": ""}):
            r = self.client.get("/api/v1/me/profile")
        self.assertEqual(r.status_code, 200, r.text)
        db_put.assert_awaited_once()  # 파일 저장분 → DB 승격
        self.assertEqual(db_put.await_args.kwargs["prefs"], {"ui_theme": "sky"})

    def test_get_graceful_when_db_unavailable_and_file_empty(self) -> None:
        with patch.object(me_router.user_prefs_db, "get_user_prefs", AsyncMock(return_value=None)), \
                patch.object(me_router.user_prefs_db, "put_user_prefs", AsyncMock(return_value=False)), \
                patch.object(me_router.user_profile_service, "get_profile",
                             return_value={"preferences": {}, "logo_relpath": ""}):
            r = self.client.get("/api/v1/me/profile")
        self.assertEqual(r.status_code, 200, r.text)  # DB 불가 시에도 200 (파일 fallback)
