"""마스터 Hcode 행 격리 회귀 가드."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.hcode_isolation import resolve_scope_hcode  # noqa: E402
from app.services import masters_service  # noqa: E402


class _Capture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    async def __call__(self, _server_id: str, sql: str, params=()):
        self.calls.append((sql, tuple(params or ())))
        if "COUNT(*)" in sql.upper():
            return [{"row_count": 0}]
        return []


class MastersHcodeIsolationTests(TestCase):
    def test_list_books_adds_hcode_clause_when_scoped(self) -> None:
        cap = _Capture()
        with patch.object(masters_service, "execute_query", new=cap):
            asyncio.run(
                masters_service.list_books(
                    server_id="remote_138",
                    q="도서",
                    limit=50,
                    offset=0,
                    scope_hcode="PUB01",
                )
            )
        select_sql, select_params = cap.calls[0]
        count_sql, count_params = cap.calls[1]
        self.assertIn("Hcode=%s", select_sql)
        self.assertIn("Hcode=%s", count_sql)
        self.assertEqual(select_params[0], "PUB01")
        self.assertEqual(count_params[0], "PUB01")

    def test_list_books_no_hcode_clause_without_scope(self) -> None:
        cap = _Capture()
        with patch.object(masters_service, "execute_query", new=cap):
            asyncio.run(
                masters_service.list_books(
                    server_id="remote_138",
                    q="도서",
                    limit=50,
                    offset=0,
                    scope_hcode=None,
                )
            )
        select_sql, _ = cap.calls[0]
        self.assertNotIn("Hcode=%s", select_sql)

    def test_resolve_scope_hcode_dist_returns_login_hcode(self) -> None:
        ctx = {
            "role": "operator",
            "hcode": "1001",
            "permissions": ["master.read"],
            "account_type": "T2_DIST",
            "account_family": "kbt",
        }
        self.assertEqual(resolve_scope_hcode(ctx), "1001")

    def test_resolve_scope_hcode_super_returns_none(self) -> None:
        ctx = {
            "role": "admin",
            "hcode": "0000",
            "permissions": ["*"],
            "account_type": "T1",
            "account_family": "",
        }
        self.assertIsNone(resolve_scope_hcode(ctx))


if __name__ == "__main__":
    main()
