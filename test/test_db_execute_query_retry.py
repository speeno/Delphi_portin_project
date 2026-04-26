"""execute_query — stale pooled MySQL/SSH connection retry guard."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from pymysql.err import OperationalError

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core import db


class _FakeCursor:
    def __init__(self, *, fail_once: bool):
        self.fail_once = fail_once

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def execute(self, sql, params):
        if self.fail_once:
            raise OperationalError(2013, "Lost connection to MySQL server during query")

    async def fetchall(self):
        return [{"ok": 1}]


class _FakeConn:
    def __init__(self, *, fail_once: bool):
        self.fail_once = fail_once

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def cursor(self, _cursor_cls):
        return _FakeCursor(fail_once=self.fail_once)


class _FakePool:
    def __init__(self, *, fail_once: bool):
        self.fail_once = fail_once
        self.closed = False
        self.waited = False

    def acquire(self):
        return _FakeConn(fail_once=self.fail_once)

    def close(self):
        self.closed = True

    async def wait_closed(self):
        self.waited = True


def test_execute_query_reopens_pool_and_tunnel_once_on_stale_connection(monkeypatch):
    pools = [_FakePool(fail_once=True), _FakePool(fail_once=False)]
    invalidated: list[str] = []

    async def fake_get_pool(server_id: str):
        return pools.pop(0)

    monkeypatch.setattr(db, "get_server_profile", lambda sid: {"id": sid})
    monkeypatch.setattr(db, "get_pool", fake_get_pool)
    monkeypatch.setattr(db, "invalidate_server_tunnel", lambda sid: invalidated.append(sid))
    monkeypatch.setitem(db._pools, "remote_test", pools[0])

    rows = asyncio.run(db.execute_query("remote_test", "SELECT 1", ()))

    assert rows == [{"ok": 1}]
    assert invalidated == ["remote_test"]
