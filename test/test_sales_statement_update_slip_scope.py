"""거래명세서/출고 수정 — 전표 단일성 스코프 회귀 (2026-07-04 대량 삭제 사고).

사고: PUT 수정이 전표를 (Gdate, Hcode, Jubun) 3키로만 식별 → 같은 일자·전표번호(Jubun)를
공유하는 **다른 거래처 라인 전부가 diff-DELETE** 됨 (h=5019, 7/2 46라인·12거래처 등).
레거시 Jubun 은 거래처별 시퀀스라 (Gdate,Hcode,Jubun) 은 거래처 간 공유 키다.

방지책(이 파일이 가드하는 계약):
1. gcode/idnum(7세그 order_key)이 오면 SELECT·쓰기를 해당 슬립으로 한정한다.
2. 스코프 없이 여러 거래처가 매칭되면 ValueError(SLIP_KEY_AMBIGUOUS/ORDER_KEY_AMBIGUOUS)
   — fail-closed, 아무 것도 쓰지 않는다.
3. PUT 라우터는 7세그 order_key 의 gcode/idnum 을 서비스로 전달한다.
4. outbound update 는 재삽입 라인의 전표번호(Idnum)를 슬립 공통값으로 보존한다.
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
from app.services import outbound_service as osvc  # noqa: E402
from app.services import sales_statement_create_service as svc  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "hcode": "5019", "role": "admin"}


_S1_COLS = {"gdate", "hcode", "jubun", "gjisa", "gcode", "bcode", "gubun", "ocode",
            "scode", "yesno", "pubun", "gsqut", "gssum", "gdang", "grat1", "gbigo",
            "time3", "idnum"}


def _row(gcode: str, bcode: str, *, idnum: str = "1", gsqut: int = 1,
         gssum: int = 25500, gdang: int = 30000, grat1: int = 85):
    return {
        "Gcode": gcode, "Bcode": bcode, "Gjisa": "", "Gubun": "출고",
        "Ocode": "A", "Scode": "X", "Pubun": "위탁", "Yesno": "0",
        "Gsqut": gsqut, "Gssum": gssum, "Gdang": gdang, "Grat1": grat1, "Gbigo": "",
        "Idnum": idnum,
    }


class UpdateSlipScopeTests(IsolatedAsyncioTestCase):
    """update_sales_statement — 사고 시나리오 직접 재현."""

    async def _run(self, current, desired_lines, *, gcode="", idnum=None):
        captured: dict = {"statements": None, "select": None}

        async def fake_exec_query(_sid, sql, params=()):
            captured["select"] = (sql, params)
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
                server_id="remote_1", gdate="2026-07-02", hcode="5019",
                jubun="11", lines=desired_lines, gcode=gcode, idnum=idnum,
            )
        return res, captured

    async def test_multi_customer_without_gcode_fails_closed(self) -> None:
        """사고 재현: (일자,회사,jubun) 공유 키에 12거래처 매칭 — 스코프 없으면 수정 거부.

        이전 동작: cur_rows[0] 의 거래처로 desired 를 키잉 → 나머지 11거래처 라인 전부
        diff-DELETE (2026-07-04 h=5019 46라인 삭제). 지금은 SLIP_KEY_AMBIGUOUS 로 거부하고
        **아무 문장도 실행하지 않는다**.
        """
        current = [
            _row("00011", "3416", idnum="11"),
            _row("00001", "2946", idnum="6"),
            _row("0961", "91184", idnum="7"),
        ]
        desired = [{"bcode": "3416", "pubun": "위탁", "gsqut": 1, "gdang": 35000, "grat1": 85}]
        with self.assertRaises(ValueError) as ctx:
            await self._run(current, desired)
        self.assertEqual(str(ctx.exception), "SLIP_KEY_AMBIGUOUS")

    async def test_multi_customer_ambiguous_writes_nothing(self) -> None:
        """fail-closed 검증 — 모호성 거부 시 execute_in_transaction 미호출."""
        current = [_row("00011", "3416", idnum="11"), _row("00001", "2946", idnum="6")]
        desired = [{"bcode": "3416", "pubun": "위탁", "gsqut": 1, "gdang": 35000, "grat1": 85}]
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
            with self.assertRaises(ValueError):
                await svc.update_sales_statement(
                    server_id="remote_1", gdate="2026-07-02", hcode="5019",
                    jubun="11", lines=desired,
                )
        self.assertIsNone(captured["statements"], "모호성 거부 시 어떤 SQL 도 실행 금지")

    async def test_gcode_scope_appended_to_select(self) -> None:
        """gcode 지정 시 SELECT WHERE 에 Gcode 스코프가 붙고 params 로 전달된다."""
        current = [_row("00011", "3416", idnum="11")]
        desired = [{"bcode": "3416", "pubun": "위탁", "gsqut": 2, "gdang": 35000, "grat1": 85}]
        res, cap = await self._run(current, desired, gcode="00011")
        sel_sql, sel_params = cap["select"]
        self.assertIn("AND Gcode=%s", sel_sql)
        self.assertIn("00011", sel_params)
        self.assertEqual(res["diff"], {"inserted": 0, "updated": 1, "deleted": 0})

    async def test_idnum_scope_appended_to_select_and_writes(self) -> None:
        """idnum 지정 + 컬럼 존재 시 SELECT·라인 쓰기(UPDATE/DELETE)에 Idnum 조건 부착.

        같은 거래처의 동일 Jubun 다른 전표(일자 이동 산물, DEC-078) 라인 불침범 가드.
        """
        current = [_row("00011", "3416", idnum="11"), _row("00011", "90608", idnum="11")]
        desired = [{"bcode": "3416", "pubun": "위탁", "gsqut": 1, "gdang": 35000, "grat1": 85}]
        res, cap = await self._run(current, desired, gcode="00011", idnum=11)
        sel_sql, sel_params = cap["select"]
        self.assertIn("COALESCE(Idnum,0)=%s", sel_sql)
        self.assertIn(11, sel_params)
        self.assertEqual(res["diff"]["deleted"], 1)
        dels = [s for s in cap["statements"] if s[0].startswith("DELETE")]
        self.assertEqual(len(dels), 1)
        self.assertIn("COALESCE(Idnum,0)=%s", dels[0][0])
        self.assertIn(11, dels[0][1])

    async def test_single_customer_without_gcode_still_works(self) -> None:
        """단일 거래처 매칭이면 4세그(legacy) 키로도 기존과 동일하게 동작 — backward-compat."""
        current = [_row("00011", "3416", idnum="11")]
        desired = [{"bcode": "3416", "pubun": "위탁", "gsqut": 3, "gdang": 35000, "grat1": 85}]
        res, _cap = await self._run(current, desired)
        self.assertEqual(res["diff"], {"inserted": 0, "updated": 1, "deleted": 0})


class UpdateHttpSlipScopeTests(TestCase):
    """PUT 라우터 — 7세그 order_key 의 gcode/idnum 전달 + 모호성 422."""

    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_put_passes_gcode_and_idnum_from_7seg_key(self) -> None:
        seen: dict = {}

        async def fake_update(*, server_id, gdate, hcode, jubun, lines, new_gdate=None,
                              gcode="", idnum=None):  # noqa: ARG001
            seen.update({"gcode": gcode, "idnum": idnum})
            return {
                "order_key": {"gdate": gdate, "hcode": hcode, "jubun": jubun},
                "lines": len(lines), "qty": 1, "amount": 29750,
                "updated_at": "2026-07-06T00:00:00+00:00",
                "diff": {"inserted": 0, "updated": 1, "deleted": 0},
            }

        with patch.object(svc, "update_sales_statement", side_effect=fake_update):
            res = self.client.put(
                # gdate|hcode|jubun|gjisa|idnum|gubun|gcode
                "/api/v1/transactions/sales-statement/2026.07.02%7C5019%7C11%7C%7C11%7C%EC%B6%9C%EA%B3%A0%7C00011",
                json={"serverId": "remote_1", "lines": [
                    {"bcode": "3416", "pubun": "위탁", "gsqut": 1, "gdang": 35000, "grat1": 85}]},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(seen["gcode"], "00011")
        self.assertEqual(seen["idnum"], 11)

    def test_put_ambiguous_returns_422_with_message(self) -> None:
        async def fake_update(**_kw):
            raise ValueError("SLIP_KEY_AMBIGUOUS")

        with patch.object(svc, "update_sales_statement", side_effect=fake_update):
            res = self.client.put(
                "/api/v1/transactions/sales-statement/2026.07.02%7C5019%7C11%7C",
                json={"serverId": "remote_1", "lines": [
                    {"bcode": "3416", "pubun": "위탁", "gsqut": 1, "gdang": 35000, "grat1": 85}]},
            )
        self.assertEqual(res.status_code, 422, res.text)
        self.assertIn("여러 거래처", res.json()["detail"]["message"])


class OutboundUpdateScopeTests(IsolatedAsyncioTestCase):
    """outbound_service.update_order — 동일 사고 벡터 가드 + Idnum 보존."""

    async def _run(self, current, desired_lines, *, gcode=""):
        captured: dict = {"statements": None}

        async def fake_exec_query(_sid, _sql, _params=()):
            return current

        async def fake_cols(_sid):
            return set(_S1_COLS)

        async def fake_tx(_sid, statements):
            captured["statements"] = statements

        with patch.object(osvc, "execute_query", side_effect=fake_exec_query), \
             patch.object(osvc, "s1_column_names", side_effect=fake_cols), \
             patch.object(osvc, "execute_in_transaction", side_effect=fake_tx):
            res = await osvc.update_order(
                server_id="remote_1", gdate="2026-07-02", hcode="5019",
                jubun="11", desired_lines=desired_lines, gcode=gcode,
            )
        return res, captured

    async def test_multi_customer_without_gcode_fails_closed(self) -> None:
        current = [_row("00011", "3416"), _row("00001", "2946")]
        desired = [{"gcode": "00011", "bcode": "3416", "pubun": "위탁", "gsqut": 1, "gssum": 29750}]
        with self.assertRaises(ValueError) as ctx:
            await self._run(current, desired)
        self.assertEqual(str(ctx.exception), "ORDER_KEY_AMBIGUOUS")

    async def test_insert_preserves_slip_idnum(self) -> None:
        """재삽입 라인이 전표번호(Idnum)를 슬립 공통값으로 유지 — 사고 잔존 행 Idnum=NULL 재발 방지."""
        current = [_row("00011", "3416", idnum="7")]
        desired = [
            {"gcode": "00011", "bcode": "3416", "pubun": "위탁", "gsqut": 1, "gssum": 25500,
             "gdang": 30000, "grat1": 85, "gbigo": ""},
            {"gcode": "00011", "bcode": "9999", "pubun": "위탁", "gsqut": 2, "gssum": 16000,
             "gdang": 10000, "grat1": 80, "gbigo": ""},
        ]
        res, cap = await self._run(current, desired, gcode="00011")
        self.assertEqual(res["lines"], 2)
        ins = [s for s in (cap["statements"] or []) if s[0].startswith("INSERT")]
        self.assertEqual(len(ins), 1)
        self.assertIn("Idnum", ins[0][0])
        # (Gdate, Hcode, Jubun, Gjisa, Gcode, Bcode, Gubun, Ocode, Scode, Yesno, Pubun,
        #  Gsqut, Gssum, Idnum, Gdang, Grat1, Gbigo)
        self.assertEqual(ins[0][1][13], 7, "Idnum 슬립 공통값 재사용")

    async def test_single_customer_without_gcode_still_works(self) -> None:
        current = [_row("00011", "3416", idnum="7")]
        desired = [{"gcode": "00011", "bcode": "3416", "pubun": "위탁", "gsqut": 9, "gssum": 99}]
        res, _cap = await self._run(current, desired)
        self.assertEqual(res["diff"]["updated"], 1)


if __name__ == "__main__":
    main()
