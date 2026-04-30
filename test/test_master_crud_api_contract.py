"""
C9 마스터 CRUD 보강 정적/단위 회귀.

범위: Sobo11(거래처)·Sobo14(도서) 기존 PATCH 경로에 POST/DELETE API를 추가해
차기 CRUD 갭을 줄인다. 실제 DB 삭제 위험을 피하기 위해 service 호출은 monkeypatch로 검증한다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"

sys.path.insert(0, str(BACKEND))


class MasterCrudServiceUnit(IsolatedAsyncioTestCase):
    async def test_customer_create_checks_duplicate_then_inserts(self):
        from app.services import masters_service

        queries: list[tuple[str, tuple]] = []
        txs: list[list[tuple[str, tuple]]] = []

        async def fake_query(_server_id, sql, params=None):
            queries.append((sql, tuple(params or ())))
            return []

        async def fake_tx(_server_id, statements):
            txs.append(statements)
            return [1]

        old_query = masters_service.execute_query
        old_tx = masters_service.execute_in_transaction
        masters_service.execute_query = fake_query
        masters_service.execute_in_transaction = fake_tx
        try:
            res = await masters_service.create_customer_master(
                server_id="remote_138",
                payload={"gcode": "C001", "gname": "거래처", "gjuso": "주소"},
            )
        finally:
            masters_service.execute_query = old_query
            masters_service.execute_in_transaction = old_tx

        self.assertEqual(res["gcode"], "C001")
        self.assertIn("SELECT Gcode FROM G1_Ggeo", queries[0][0])
        self.assertIn("INSERT INTO G1_Ggeo", txs[0][0][0])

    async def test_book_delete_returns_none_when_missing(self):
        from app.services import masters_service

        async def fake_query(_server_id, _sql, _params=None):
            return []

        old_query = masters_service.execute_query
        masters_service.execute_query = fake_query
        try:
            res = await masters_service.delete_book(server_id="remote_138", gcode="B404")
        finally:
            masters_service.execute_query = old_query

        self.assertIsNone(res)


class MasterCrudStaticContract(TestCase):
    def test_router_exposes_customer_and_book_post_delete(self):
        router = (BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        for token in (
            '@router.post("/customer"',
            '@router.delete("/customer/{gcode}"',
            '@router.post("/book"',
            '@router.delete("/book/{gcode}"',
            "MASTER_DUPLICATE",
            "audit.master",
        ):
            self.assertIn(token, router)

    def test_frontend_client_exports_create_delete_methods(self):
        src = (FE / "lib" / "master-api.ts").read_text(encoding="utf-8")
        for token in (
            "customerCreate",
            "customerDelete",
            "bookCreate",
            "bookDelete",
            "CustomerCreatePayload",
            "BookCreatePayload",
        ):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
