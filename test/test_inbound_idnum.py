"""입고 전표번호(Idnum) 채번·표시 회귀 — 출고(거래명세서) 방식 정합.

DB 부작용 없이 s1_column_names / allocate_idnum / execute_query /
execute_in_transaction / count_grouped 를 monkeypatch 로 막아 SQL/응답만 검증.
사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import inbound_service as ib  # noqa: E402

_SID = "remote_1"
_HDR = {"gdate": "2026-06-28", "hcode": "H1", "gcode": "V1", "jubun": "1"}
_LINES = [{"bcode": "B1", "gsqut": 2, "gdang": 1000, "grat1": 100}]


class CreateIdnumTests(IsolatedAsyncioTestCase):
    async def test_create_allocates_and_inserts_idnum(self) -> None:
        captured: dict = {}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001 — period-lock 등
            return []

        async def fake_tx(server_id, statements):  # noqa: ANN001, ARG001
            captured["statements"] = statements

        with patch.object(ib, "s1_column_names",
                          AsyncMock(return_value={"idnum", "gdate", "hcode", "gcode", "jubun"})), \
                patch.object(ib, "allocate_idnum", AsyncMock(return_value=7)), \
                patch.object(ib, "execute_query", side_effect=fake_eq), \
                patch.object(ib, "execute_in_transaction", side_effect=fake_tx):
            res = await ib.create_receipt(server_id=_SID, header=dict(_HDR), memo=None, lines=_LINES)

        self.assertEqual(res["idnum"], 7)
        sql, params = captured["statements"][0]
        self.assertIn("Idnum,", sql)         # INSERT 컬럼에 Idnum 포함
        self.assertEqual(params[0], 7)        # 첫 바인딩 = 채번된 Idnum
        self.assertEqual(res["receipt_key"]["jubun"], "1")  # 키는 그대로(Jubun)

    async def test_create_without_idnum_column_skips(self) -> None:
        captured: dict = {}
        alloc = AsyncMock(return_value=99)

        async def fake_tx(server_id, statements):  # noqa: ANN001, ARG001
            captured["statements"] = statements

        with patch.object(ib, "s1_column_names",
                          AsyncMock(return_value={"gdate", "hcode", "gcode", "jubun"})), \
                patch.object(ib, "allocate_idnum", alloc), \
                patch.object(ib, "execute_query", AsyncMock(return_value=[])), \
                patch.object(ib, "execute_in_transaction", side_effect=fake_tx):
            res = await ib.create_receipt(server_id=_SID, header=dict(_HDR), memo=None, lines=_LINES)

        self.assertEqual(res["idnum"], 0)
        alloc.assert_not_awaited()            # Idnum 컬럼 없으면 채번 안 함
        sql, _params = captured["statements"][0]
        self.assertNotIn("Idnum", sql)        # 기존 INSERT(컬럼 변경 0) 유지


class ListIdnumTests(IsolatedAsyncioTestCase):
    async def test_list_surfaces_idnum(self) -> None:
        captured: dict = {}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            captured["sql"] = sql
            return [{
                "Gdate": "2026.06.28", "Hcode": "H1", "Gcode": "V1", "Jubun": "1",
                "line_count": 2, "qty": 5, "amount": 5000, "idnum": 7, "yesno_max": "0",
            }]

        with patch.object(ib, "s1_column_names", AsyncMock(return_value={"idnum"})), \
                patch.object(ib, "execute_query", side_effect=fake_eq), \
                patch.object(ib, "_fetch_publisher_names", AsyncMock(return_value={})), \
                patch.object(ib, "_fetch_vendor_names", AsyncMock(return_value={})), \
                patch.object(ib, "count_grouped", AsyncMock(return_value=1)):
            items, total = await ib.list_receipts(
                server_id=_SID, date_from="2026-06-28", date_to="2026-06-28"
            )

        self.assertIn("MAX(Idnum+0) AS idnum", captured["sql"])
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["idnum"], 7)
        self.assertEqual(items[0]["receipt_key"]["jubun"], "1")  # 키 불변

    async def test_list_without_idnum_column_zero(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            return [{
                "Gdate": "2026.06.28", "Hcode": "H1", "Gcode": "V1", "Jubun": "1",
                "line_count": 1, "qty": 1, "amount": 1, "idnum": 0, "yesno_max": "0",
            }]

        with patch.object(ib, "s1_column_names", AsyncMock(return_value=set())), \
                patch.object(ib, "execute_query", side_effect=fake_eq), \
                patch.object(ib, "_fetch_publisher_names", AsyncMock(return_value={})), \
                patch.object(ib, "_fetch_vendor_names", AsyncMock(return_value={})), \
                patch.object(ib, "count_grouped", AsyncMock(return_value=1)):
            items, _total = await ib.list_receipts(
                server_id=_SID, date_from="2026-06-28", date_to="2026-06-28"
            )
        self.assertEqual(items[0]["idnum"], 0)


if __name__ == "__main__":
    main()
