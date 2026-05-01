from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class _Cursor:
    def __init__(self, conn: "_Conn") -> None:
        self.conn = conn
        self.rowcount = 1

    async def __aenter__(self) -> "_Cursor":
        return self

    async def __aexit__(self, *_exc: object) -> None:
        return None

    async def execute(self, sql: str, params: object | None = None) -> None:
        self.conn.executed.append((sql, params, self.conn.current_db))


class _Conn:
    def __init__(self) -> None:
        self.current_db = "default_db"
        self.selected: list[str] = []
        self.executed: list[tuple[str, object | None, str]] = []
        self.began = False
        self.committed = False

    async def select_db(self, db_name: str) -> None:
        self.current_db = db_name
        self.selected.append(db_name)

    async def begin(self) -> None:
        self.began = True

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        return None

    def cursor(self, *_args: object, **_kwargs: object) -> _Cursor:
        return _Cursor(self)


class _Acquire:
    def __init__(self, conn: _Conn) -> None:
        self.conn = conn

    async def __aenter__(self) -> _Conn:
        return self.conn

    async def __aexit__(self, *_exc: object) -> None:
        return None


class _Pool:
    def __init__(self, conn: _Conn) -> None:
        self.conn = conn

    def acquire(self) -> _Acquire:
        return _Acquire(self.conn)


class InspectTransactionDbTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        from app.core import db
        from app.core.inspect_context import clear_inspect_context

        self.db = db
        clear_inspect_context()
        self.old_get_server_profile = db.get_server_profile
        self.old_get_pool = db.get_pool
        self.conn = _Conn()
        db.get_server_profile = lambda server_id: {
            "id": server_id,
            "database": "default_db",
            "user": "u",
            "password": "p",
        }

        async def fake_get_pool(_server_id: str) -> _Pool:
            return _Pool(self.conn)

        db.get_pool = fake_get_pool

    async def asyncTearDown(self) -> None:
        from app.core.inspect_context import clear_inspect_context

        self.db.get_server_profile = self.old_get_server_profile
        self.db.get_pool = self.old_get_pool
        clear_inspect_context()

    async def test_execute_in_transaction_uses_inspect_database_and_restores_default(self) -> None:
        from app.core.inspect_context import set_inspect_context

        set_inspect_context(
            server_id="remote_153",
            db_name="chul_05_db",
            reason="저장 대상 정합성 테스트",
        )

        out = await self.db.execute_in_transaction(
            "remote_153",
            [("UPDATE G4_Book SET Gname=%s WHERE Gcode=%s", ("새제목", "0014"))],
        )

        self.assertEqual(out, [1])
        self.assertTrue(self.conn.began)
        self.assertTrue(self.conn.committed)
        self.assertEqual(self.conn.selected, ["chul_05_db", "default_db"])
        self.assertEqual(self.conn.executed[0][2], "chul_05_db")


if __name__ == "__main__":
    main(verbosity=2)
