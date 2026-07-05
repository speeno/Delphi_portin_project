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

    async def test_update_preserves_customer_gcode_and_idnum(self) -> None:
        """회귀(2026-07-05): hcode(테넌트)≠Gcode(거래처) 전표 수정 시 거래처·전표번호(Idnum) 보존.

        이전 버그: desired 를 (hcode,bcode)/gcode=hcode 로 키잉 → 현재 라인((Gcode,bcode))과
        키가 어긋나 전 라인 DELETE+INSERT(gcode=hcode)로 거래처가 소실되고 Idnum 이 사라졌다.
        상세 편집 팝업 저장 후 목록에서 거래처=hcode, 전표번호='–' 로 표시되던 문제.
        """
        cols = set(_S1_COLS) | {"idnum"}
        current = [{
            "Gcode": "00001", "Bcode": "3411", "Gjisa": "", "Gubun": "출고",
            "Ocode": "B", "Scode": "X", "Pubun": "위탁",
            "Gsqut": 1, "Gssum": 25500, "Gdang": 30000, "Grat1": 85, "Gbigo": "",
            "Idnum": "42",
        }]
        # 기존 도서(3411) 수량 변경 → UPDATE, 새 도서(9999) 추가 → INSERT.
        desired = [
            {"bcode": "3411", "pubun": "위탁", "gsqut": 5, "gdang": 30000, "grat1": 85},
            {"bcode": "9999", "pubun": "위탁", "gsqut": 2, "gdang": 10000, "grat1": 80},
        ]
        captured: dict = {"statements": None}

        async def fake_exec_query(_sid, _sql, _params=()):
            return current

        async def fake_cols(_sid):
            return cols

        async def fake_tx(_sid, statements):
            captured["statements"] = statements

        with patch.object(svc, "execute_query", side_effect=fake_exec_query), \
             patch.object(svc, "s1_column_names", side_effect=fake_cols), \
             patch.object(svc, "execute_in_transaction", side_effect=fake_tx), \
             patch.object(svc, "mysql3_protocol", return_value=False):
            res = await svc.update_sales_statement(
                server_id="remote_1", gdate="2026-06-11", hcode="5019",
                jubun="00001", lines=desired,
            )
        stmts = captured["statements"] or []
        # 기존 도서는 UPDATE(삭제 안 됨), 새 도서만 INSERT — 전 라인 DELETE 회귀 차단.
        self.assertEqual(res["diff"], {"inserted": 1, "updated": 1, "deleted": 0})
        self.assertNotIn("DELETE FROM S1_Ssub", " ".join(s[0] for s in stmts))
        ins = [s for s in stmts if s[0].startswith("INSERT")]
        self.assertEqual(len(ins), 1)
        p = ins[0][1]
        # (Gdate, Hcode, Jubun, Gjisa, Gcode, Bcode, Gubun, Ocode, Scode, Yesno, Pubun, Gsqut, Gssum, Idnum, ...)
        self.assertEqual(p[1], "5019", "Hcode = 테넌트")
        self.assertEqual(p[4], "00001", "Gcode(거래처) 보존 — hcode 로 덮이면 안 됨")
        self.assertEqual(p[5], "9999", "새 도서 Bcode")
        self.assertEqual(p[13], "42", "전표번호(Idnum) 슬립 공통값 재사용")

    async def test_update_moves_slip_when_new_gdate_given(self) -> None:
        """거래일자 변경(DEC-078) — 새 일자로 슬립 이동 UPDATE 선행 + 라인 diff 는 새 일자 키.

        이동은 이 슬립 거래처(Gcode)로 스코프해 다른 거래처를 건드리지 않는다. 전표번호(Idnum)
        는 유지(중복 허용, 사용자 합의). 라인 diff(UPDATE/INSERT)는 새 일자 기준으로 나간다.
        """
        cols = set(_S1_COLS) | {"idnum"}
        current = [{
            "Gcode": "00001", "Bcode": "3411", "Gjisa": "", "Gubun": "출고",
            "Ocode": "B", "Scode": "X", "Pubun": "위탁",
            "Gsqut": 1, "Gssum": 25500, "Gdang": 30000, "Grat1": 85, "Gbigo": "",
            "Idnum": "42",
        }]
        desired = [{"bcode": "3411", "pubun": "위탁", "gsqut": 2, "gdang": 30000, "grat1": 85}]
        captured: dict = {"statements": None}

        async def fake_exec_query(_sid, _sql, _params=()):
            return current

        async def fake_cols(_sid):
            return cols

        async def fake_tx(_sid, statements):
            captured["statements"] = statements

        with patch.object(svc, "execute_query", side_effect=fake_exec_query), \
             patch.object(svc, "s1_column_names", side_effect=fake_cols), \
             patch.object(svc, "execute_in_transaction", side_effect=fake_tx), \
             patch.object(svc, "mysql3_protocol", return_value=False):
            res = await svc.update_sales_statement(
                server_id="remote_1", gdate="2026-06-11", hcode="00001",
                jubun="00001", lines=desired, new_gdate="2026-06-20",
            )
        stmts = captured["statements"] or []
        # 첫 문장 = 일자 이동 UPDATE(Gdate SET), Gcode 스코프 포함.
        move = stmts[0]
        self.assertIn("SET Gdate=%s", move[0])
        self.assertIn("AND Gcode=%s", move[0])
        # params: (신일자, 구일자, hcode, jubun, gcode)
        self.assertEqual(move[1][0], "2026.06.20")  # SET 새 일자(정규화 . 구분)
        self.assertEqual(move[1][1], "2026.06.11")  # WHERE 구 일자
        self.assertEqual(move[1][-1], "00001")       # Gcode 스코프
        # 라인 UPDATE 는 새 일자 키로 나가야 한다.
        line_upd = [s for s in stmts if s[0].startswith("UPDATE") and "SET Gdate" not in s[0]]
        self.assertTrue(line_upd)
        self.assertIn("2026.06.20", [str(p) for p in line_upd[0][1]])
        # 응답 order_key 는 새 일자.
        self.assertEqual(res["order_key"]["gdate"], "2026.06.20")

    async def test_update_no_move_when_new_gdate_same(self) -> None:
        """new_gdate 가 기존과 같으면(정규화 후) 이동 UPDATE 를 내지 않는다."""
        current = [_cur_row("3411", 1, 25500, 30000, 85)]
        desired = [{"bcode": "3411", "pubun": "위탁", "gsqut": 3, "gdang": 30000, "grat1": 85}]
        captured: dict = {"statements": None}

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
            await svc.update_sales_statement(
                server_id="remote_1", gdate="2026-06-11", hcode="00001",
                jubun="00001", lines=desired, new_gdate="2026.06.11",
            )
        joined = " ".join(s[0] for s in (captured["statements"] or []))
        self.assertNotIn("SET Gdate=%s", joined)

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
        async def fake_update(*, server_id, gdate, hcode, jubun, lines, new_gdate=None):  # noqa: ARG001
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
        async def fake_none(*, server_id, gdate, hcode, jubun, lines, new_gdate=None):  # noqa: ARG001
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
