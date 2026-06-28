"""목록 테이블 사용자 설정(hcode 종속) 회귀 — grid_prefs 서비스 + 라우터.

- 컬럼 너비/표시여부 prefs 를 Web_Grid_Prefs 사이드 테이블에 hcode 격리 저장.
- DB 는 in-memory fake execute_query 로 대체(부작용 없음).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import grid_prefs_service  # noqa: E402

_SID = "remote_138"


async def _ctx() -> dict:
    return {"user_id": "u", "server_id": _SID, "hcode": "BR01", "role": "operator", "permissions": []}


class GridKeyValidationTests(TestCase):
    def test_valid_keys(self) -> None:
        for k in ("master.customer", "master_book", "a.b-c.1"):
            self.assertTrue(grid_prefs_service.is_valid_grid_key(k))

    def test_invalid_keys(self) -> None:
        for k in ("", "a b", "a/b", "x" * 65, "drop table;"):
            self.assertFalse(grid_prefs_service.is_valid_grid_key(k))


class GridPrefsServiceTests(IsolatedAsyncioTestCase):
    async def test_put_then_get_round_trip(self) -> None:
        store: dict[tuple[str, str], str] = {}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            if sql.strip().upper().startswith("CREATE TABLE"):
                return []
            if sql.strip().upper().startswith("REPLACE"):
                store[(params[0], params[1])] = params[2]
                return []
            if sql.strip().upper().startswith("DELETE"):
                store.pop((params[0], params[1]), None)
                return []
            if "SELECT Prefs" in sql:
                raw = store.get((params[0], params[1]))
                return [{"Prefs": raw}] if raw is not None else []
            return []

        with patch.object(grid_prefs_service, "execute_query", side_effect=fake_eq):
            grid_prefs_service._ensured.discard(_SID)
            ok = await grid_prefs_service.put_prefs(
                server_id=_SID,
                hcode="BR01",
                grid_key="master.customer",
                prefs={"widths": {"gcode": 120}, "hidden": ["gjuso"]},
            )
            self.assertTrue(ok)
            got = await grid_prefs_service.get_prefs(
                server_id=_SID, hcode="BR01", grid_key="master.customer"
            )
        self.assertEqual(got["widths"]["gcode"], 120)
        self.assertEqual(got["hidden"], ["gjuso"])
        # 다른 hcode 는 격리되어 빈 dict.
        with patch.object(grid_prefs_service, "execute_query", side_effect=fake_eq):
            other = await grid_prefs_service.get_prefs(
                server_id=_SID, hcode="BR99", grid_key="master.customer"
            )
        self.assertEqual(other, {})

    async def test_empty_prefs_deletes(self) -> None:
        calls: list[str] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            calls.append(sql.strip().split()[0].upper())
            return []

        with patch.object(grid_prefs_service, "execute_query", side_effect=fake_eq):
            grid_prefs_service._ensured.discard(_SID)
            ok = await grid_prefs_service.put_prefs(
                server_id=_SID, hcode="BR01", grid_key="master.book", prefs={}
            )
        self.assertTrue(ok)
        self.assertIn("DELETE", calls)


class GridPrefsRouterTests(TestCase):
    def setUp(self) -> None:
        self._prev = app.dependency_overrides.get(get_user_context)
        self._prev_u = app.dependency_overrides.get(get_current_user)
        app.dependency_overrides[get_user_context] = _ctx
        app.dependency_overrides[get_current_user] = _ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in ((get_user_context, self._prev), (get_current_user, self._prev_u)):
            if prev is not None:
                app.dependency_overrides[dep] = prev
            else:
                app.dependency_overrides.pop(dep, None)

    def test_get_returns_prefs(self) -> None:
        async def fake_get(*, server_id, hcode, grid_key):  # noqa: ANN001, ARG001
            return {"widths": {"gcode": 99}}

        with patch.object(grid_prefs_service, "get_prefs", side_effect=fake_get):
            r = self.client.get(f"/api/v1/grid-prefs/master.customer?serverId={_SID}")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["prefs"]["widths"]["gcode"], 99)

    def test_put_saves(self) -> None:
        captured: dict = {}

        async def fake_put(*, server_id, hcode, grid_key, prefs):  # noqa: ANN001, ARG001
            captured.update({"hcode": hcode, "grid_key": grid_key, "prefs": prefs})
            return True

        with patch.object(grid_prefs_service, "put_prefs", side_effect=fake_put):
            r = self.client.put(
                f"/api/v1/grid-prefs/master.book?serverId={_SID}",
                json={"prefs": {"hidden": ["gpost"]}},
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(captured["hcode"], "BR01")  # JWT hcode 격리
        self.assertEqual(captured["grid_key"], "master.book")
        self.assertEqual(captured["prefs"], {"hidden": ["gpost"]})

    def test_bad_grid_key_400(self) -> None:
        r = self.client.get(f"/api/v1/grid-prefs/bad%20key?serverId={_SID}")
        self.assertEqual(r.status_code, 400, r.text)


if __name__ == "__main__":
    main()
