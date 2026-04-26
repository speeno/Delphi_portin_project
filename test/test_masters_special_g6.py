"""
Sobo16 특별관리 — G6_Ggeo list / PATCH 서비스 회귀 (special_master.yaml v1.0.0).

DB 미연결 — ``masters_service.execute_query`` / ``execute_in_transaction`` patch.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import masters_service  # noqa: E402


class _ExecCapture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        u = sql.upper()
        if "COUNT(*)" in u:
            return [{"row_count": 1}]
        if "FROM G6_GGEO" in u and "LEFT JOIN" in u:
            return [
                {
                    "id": 42,
                    "hcode": "H01",
                    "gcode": "G01",
                    "bcode": "B01",
                    "grat1": "10",
                    "gssum": 100.0,
                    "bname": "Bn",
                    "gname": "Gn",
                }
            ]
        if "SELECT ID FROM G6_GGEO" in u:
            return [{"ID": 42}]
        return []


class _TxCapture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, ops: list):  # noqa: ARG002
        for sql, params in ops:
            self.calls.append((sql, tuple(params)))
        return [1]


class MastersSpecialG6Tests(TestCase):
    def test_list_builds_join_and_paging(self) -> None:
        cap = _ExecCapture()
        with patch.object(masters_service, "execute_query", new=cap):
            out = asyncio.run(
                masters_service.list_special_master(
                    server_id="remote_1",
                    mode="customer",
                    hcode="H01",
                    gcode="G01",
                    limit=10,
                    offset=0,
                )
            )
        self.assertEqual(len(out["items"]), 1)
        self.assertEqual(out["items"][0]["id"], 42)
        self.assertEqual(out["items"][0]["gname"], "Gn")
        sqls = [c[0] for c in cap.calls]
        self.assertTrue(any("COUNT(*)" in s.upper() for s in sqls))
        self.assertTrue(any("LEFT JOIN G4_Book" in s for s in sqls))
        self.assertTrue(any("LEFT JOIN G1_Ggeo" in s for s in sqls))
        self.assertTrue(any("LIMIT %s OFFSET %s" in s for s in sqls))

    def test_list_invalid_mode_raises(self) -> None:
        with self.assertRaises(ValueError):
            asyncio.run(
                masters_service.list_special_master(
                    server_id="remote_1",
                    mode="invalid",
                    hcode="H",
                )
            )

    def test_update_sets_grat_columns(self) -> None:
        q = _ExecCapture()
        tx = _TxCapture()
        with (
            patch.object(masters_service, "execute_query", new=q),
            patch.object(masters_service, "execute_in_transaction", new=tx),
        ):
            out = asyncio.run(
                masters_service.update_special_master(
                    server_id="remote_1",
                    row_id=42,
                    hcode="H01",
                    payload={"grat1": "5", "gssum": 20.0},
                )
            )
        self.assertIsNotNone(out)
        assert out is not None
        self.assertIn("grat1", out["updated_fields"])
        self.assertTrue(any("UPDATE G6_Ggeo SET" in c[0] for c in tx.calls))
        self.assertTrue(any("Grat1=%s" in c[0] and "Gssum=%s" in c[0] for c in tx.calls))


if __name__ == "__main__":
    main()
