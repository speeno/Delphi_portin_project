"""거래명세서 수정(PUT) — DEC-065 desired-state diff 검증.

레거시 Subu21 수정: 거래현황(상세) 검색 → 선택 → 폼 로드 → 라인 수정/추가/삭제 → 저장(같은 전표).
실 DB 없이 service 내부 execute_query/execute_in_transaction/s1_column_names 만 monkeypatch.
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

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import sales_statement_create_service as svc  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "hcode": "A0001", "role": "admin"}


app.dependency_overrides[get_current_user] = _override_auth


def _cur_row(bcode: str, gsqut: int, gssum: int, gdang: int = 0, grat1: int = 0):
    return {
        "Gcode": "00001", "Bcode": bcode, "Gjisa": "", "Gubun": "출고",
        "Ocode": "B", "Scode": "X", "Pubun": "위탁",
        "Gsqut": gsqut, "Gssum": gssum, "Gdang": gdang, "Grat1": grat1, "Gbigo": "",
    }


_S1_COLS = {"gdate", "hcode", "jubun", "gjisa", "gcode", "bcode", "gubun", "ocode",
            "scode", "yesno", "pubun", "gsqut", "gssum", "gdang", "grat1", "gbigo", "time3"}


class UpdateServiceDiffTests(IsolatedAsyncioTestCase):
    async def _run(self, current, desired_lines):
        captured = {"statements": None}

        async def fake_exec_query(_sid, _sql, _params=()):
            return current

        async def fake_cols(_sid):
            return set(_S1_COLS)

        async def fake_tx(_sid, statements):
            captured["statements"] = statements

        with patch.object(svc, "execute_query", side_effect=fake_exec_query), \
             patch.object(svc, "s1_column_names", side_effect=fake_cols), \
             patch.object(svc, "execute_in_transaction", side_effect=fake_tx), \
             patch.object(svc, "mysql3_protocol", return_value=False):
            res = await svc.update_sales_statement(
                server_id="remote_1", gdate="2026-06-11", hcode="00001",
                jubun="00001", lines=desired_lines,
            )
        return res, captured["statements"]

    async def test_update_changed_qty_emits_update(self) -> None:
        current = [_cur_row("3411", 1, 25500, 30000, 85)]
        desired = [{"bcode": "3411", "pubun": "위탁", "gsqut": 2, "gdang": 30000, "grat1": 85}]
        res, stmts = await self._run(current, desired)
        self.assertEqual(res["diff"], {"inserted": 0, "updated": 1, "deleted": 0})
        # 금액 서버 재계산: 30000*2*85/100 = 51000
        self.assertEqual(res["amount"], 51000)
        sql_joined = " ".join(s[0] for s in (stmts or []))
        self.assertIn("UPDATE S1_Ssub", sql_joined)

    async def test_update_insert_and_delete(self) -> None:
        current = [_cur_row("3411", 1, 25500, 30000, 85), _cur_row("3310", 1, 20400, 24000, 85)]
        # 3411 유지(동일), 3310 제거, 9999 추가.
        desired = [
            {"bcode": "3411", "pubun": "위탁", "gsqut": 1, "gdang": 30000, "grat1": 85, "gssum": 25500},
            {"bcode": "9999", "pubun": "위탁", "gsqut": 3, "gdang": 10000, "grat1": 80},
        ]
        res, stmts = await self._run(current, desired)
        self.assertEqual(res["diff"]["inserted"], 1)
        self.assertEqual(res["diff"]["deleted"], 1)
        sqls = " ".join(s[0] for s in (stmts or []))
        self.assertIn("INSERT INTO S1_Ssub", sqls)
        self.assertIn("DELETE FROM S1_Ssub", sqls)

    async def test_update_returns_none_when_slip_absent(self) -> None:
        res, _ = await self._run([], [{"bcode": "3411", "gsqut": 1, "gdang": 1, "grat1": 1}])
        self.assertIsNone(res)

    async def test_mysql3_uses_ifnull_in_where(self) -> None:
        captured = {"sql": []}

        async def fake_exec_query(_sid, sql, _params=()):
            captured["sql"].append(sql)
            return [_cur_row("3411", 1, 25500, 30000, 85)]

        async def fake_cols(_sid):
            return set(_S1_COLS)

        async def fake_tx(_sid, statements):
            captured["sql"].extend(s[0] for s in statements)

        with patch.object(svc, "execute_query", side_effect=fake_exec_query), \
             patch.object(svc, "s1_column_names", side_effect=fake_cols), \
             patch.object(svc, "execute_in_transaction", side_effect=fake_tx), \
             patch.object(svc, "mysql3_protocol", return_value=True):
            await svc.update_sales_statement(
                server_id="remote_154", gdate="2026-06-11", hcode="00001", jubun="00001",
                lines=[{"bcode": "3411", "pubun": "위탁", "gsqut": 9, "gdang": 30000, "grat1": 85}],
            )
        joined = " ".join(captured["sql"])
        self.assertIn("IFNULL(Jubun", joined)
        self.assertNotIn("COALESCE(Jubun", joined)


class UpdateHttpTests(TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_put_returns_200_with_diff(self) -> None:
        async def fake_update(*, server_id, gdate, hcode, jubun, lines):  # noqa: ARG001
            return {
                "order_key": {"gdate": "2026.06.11", "hcode": "00001", "jubun": "00001"},
                "lines": len(lines), "qty": 2, "amount": 51000,
                "updated_at": "2026-06-11T00:00:00+00:00",
                "diff": {"inserted": 0, "updated": 1, "deleted": 0},
            }

        with patch.object(svc, "update_sales_statement", side_effect=fake_update):
            res = self.client.put(
                "/api/v1/transactions/sales-statement/2026.06.11%7C00001%7C00001%7C",
                json={"serverId": "remote_1", "lines": [
                    {"bcode": "3411", "pubun": "위탁", "gsqut": 2, "gdang": 30000, "grat1": 85}]},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["diff"]["updated"], 1)
        self.assertEqual(body["amount"], 51000)

    def test_put_404_when_absent(self) -> None:
        async def fake_none(*, server_id, gdate, hcode, jubun, lines):  # noqa: ARG001
            return None

        with patch.object(svc, "update_sales_statement", side_effect=fake_none):
            res = self.client.put(
                "/api/v1/transactions/sales-statement/2026.06.11%7C00001%7C99999%7C",
                json={"serverId": "remote_1", "lines": [{"bcode": "3411", "gsqut": 1, "gdang": 1, "grat1": 1}]},
            )
        self.assertEqual(res.status_code, 404, res.text)
        self.assertEqual(res.json()["detail"]["code"], "INQ_NOT_FOUND")


if __name__ == "__main__":
    main()
