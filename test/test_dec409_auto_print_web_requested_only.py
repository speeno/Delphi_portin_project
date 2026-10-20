"""DEC-409 — 자동출력이 출고요청하지 않은 전표를 인쇄 · 완료한 문제(교문사 2026-10-20).

운영 기록(remote_153 · 5019, Render 로그 KST)
- 08:34~08:38 출고 접수 1~5번 입력(DEC-406 자동저장: 첫 줄 POST · 둘째 줄부터 PUT).
- 08:39:52 자동출력 창 열림 → 08:39:57 received-today(7일) 7건 → 08:40:01 한 문서 인쇄 → 08:40:12 7건 완료.
  · 오늘 3 · 4 · 5번 — PUT(update_order)이 새 줄을 Yesno='0'(접수)으로 넣어 줄이 2개 이상인 전표가 입력 도중 접수가 됐다.
    첫 줄만 '' 로 남았다(1 · 2번은 한 줄 전표라 대기 — 08:48:51 사용자가 바로출고).
  · 10/15 반품 3건 · 10/14 출고 1건 — 레거시(위러브)는 새 줄을 '0' 으로 넣는다(Time3 빈 값). 웹은 '0' 을 접수로 보아
    7일 창 안의 레거시 입력 전표를 인쇄 · 완료('1')했다(위러브로 이미 출력한 전표).

가드
- update_order 새 줄 Yesno = 전표 현재 상태(MAX). 대기 전표에 줄을 더해도 대기.
- 출고요청(request_dispatch — 바로출고 · 일괄 출고요청 공통)은 전이 직전에 전표 축을 Web_Dispatch_Request 에 남긴다.
- received-today · received-stream 은 기록이 있는 접수 전표만 넘긴다. 조회 실패는 빈 목록(fail-closed). 빠진 전표는 스트림 seen 에 넣지 않는다.
"""

from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.deps import get_user_context
from app.main import app
from app.routers.auth import get_current_user
from app.services import dispatch_request_db as drq
from app.services import outbound_service as osvc
from app.services import transactions_service as tsvc

_SID = "remote_test"


def _run(coro):
    return asyncio.run(coro)


def _item(gdate: str, jubun: str, gjisa: str, idnum: int, gubun: str, gcode: str) -> dict:
    return {"status": "received", "order_key": {
        "gdate": gdate, "hcode": "5019", "jubun": jubun, "gjisa": gjisa, "idnum": idnum, "gubun": gubun, "gcode": gcode}}


# 08:39:57 received-today 가 돌려준 7건(운영 로그 키 그대로)
TODAY_3 = _item("2026.10.20", "1", "온라인", 3, "출고", "00004")
TODAY_4 = _item("2026.10.20", "1", "", 4, "출고", "00431")
TODAY_5 = _item("2026.10.20", "2", "", 5, "출고", "09002")
LEGACY = [
    _item("2026.10.15", "21", "스타필드수원점", 1, "반품", "00004"),
    _item("2026.10.15", "21", "", 3, "반품", "00378"),
    _item("2026.10.15", "21", "", 2, "반품", "09068"),
    _item("2026.10.14", "11", "", 25, "출고", "1017"),
]
SEVEN = [TODAY_3, TODAY_4, TODAY_5, *LEGACY]


def _key(it: dict) -> tuple:
    k = it["order_key"]
    return drq.slip_key(k["hcode"], k["gdate"], k["jubun"], k["gjisa"], k["gcode"])


class UpdateOrderNewLineYesno(unittest.TestCase):
    """PUT 새 줄은 전표의 현재 Yesno 를 따른다(종전 '0' 고정)."""

    def _insert_yesno(self, current_yesno: list[str]) -> str:
        rows = [
            {"Gdate": "2026.10.20", "Hcode": "5019", "Jubun": "1", "Gcode": "00431", "Bcode": f"B{i}", "Pubun": "",
             "Gsqut": 1, "Gssum": 1000, "Yesno": y, "Gjisa": "", "Gubun": "출고", "Ocode": "A", "Scode": "X"}
            for i, y in enumerate(current_yesno)
        ]
        captured: list = []

        async def fake_tx(server_id, statements):  # noqa: ARG001
            captured.extend(statements)
            return [1] * len(statements)

        desired = [{"gcode": "00431", "bcode": r["Bcode"], "pubun": "", "gsqut": 1, "gssum": 1000} for r in rows]
        desired.append({"gcode": "00431", "bcode": "NEW", "pubun": "", "gsqut": 2, "gssum": 2000})
        with patch.object(osvc, "execute_query", AsyncMock(return_value=rows)), \
                patch.object(osvc, "execute_in_transaction", side_effect=fake_tx), \
                patch.object(osvc, "s1_column_names", AsyncMock(return_value=set())):
            res = _run(osvc.update_order(server_id=_SID, gdate="2026.10.20", hcode="5019", jubun="1",
                                         desired_lines=desired, gcode="00431"))
        self.assertEqual(res["diff"]["inserted"], 1)
        (sql, params), = [st for st in captured if st[0].lstrip().upper().startswith("INSERT")]
        cols = sql[sql.index("(") + 1: sql.index(")")].replace(" ", "").split(",")
        return params[cols.index("Yesno")]

    def test_pending_slip_stays_pending(self) -> None:
        # 자동저장 둘째 줄 — 첫 줄(POST)이 '' 이면 새 줄도 ''(종전 '0' → 전표가 접수로 바뀌어 자동출력됨).
        self.assertEqual(self._insert_yesno([""]), "")
        self.assertEqual(self._insert_yesno(["", ""]), "")

    def test_requested_and_done_slips_keep_their_state(self) -> None:
        self.assertEqual(self._insert_yesno(["0", "0"]), "0")
        self.assertEqual(self._insert_yesno(["", "1"]), "1")  # 3~5번처럼 섞인 전표는 MAX(상태 판정과 같은 규칙)
        self.assertEqual(self._insert_yesno(["2"]), "2")


class RequestDispatchRecords(unittest.TestCase):
    def _request(self, rows: list[dict], record: AsyncMock):
        order: list[str] = []
        record.side_effect = lambda *a, **k: order.append("record") or 1

        async def fake_q(server_id, sql, params):  # noqa: ARG001
            return rows

        async def fake_tx(server_id, statements):  # noqa: ARG001
            order.append("update")
            return [1]

        with patch.object(osvc, "execute_query", side_effect=fake_q), \
                patch.object(osvc, "execute_in_transaction", side_effect=fake_tx), \
                patch.object(osvc.dispatch_request_db, "record", record):
            res = _run(osvc.request_dispatch(server_id=_SID, gdate="2026.10.20", hcode="5019", jubun="1",
                                             gcode="00004", gjisa="온라인"))
        return res, order

    def test_records_slip_axes_before_transition(self) -> None:
        rows = [{"Yesno": "", "Gdate": "2026.10.20", "Jubun": "1", "Gjisa": "온라인", "Gcode": "00004"}] * 2
        record = AsyncMock()
        res, order = self._request(rows, record)
        self.assertIsNotNone(res)
        self.assertEqual(order, ["record", "update"])
        server_id, slips = record.call_args.args
        self.assertEqual(server_id, _SID)
        self.assertEqual({drq.slip_key(**s) for s in slips}, {_key(TODAY_3)})

    def test_legacy_zero_slip_requested_on_web_is_recorded(self) -> None:
        # 위러브 입력('0') 전표도 웹에서 출고요청하면 사용자가 고른 것 — 기록해 자동출력 대상이 된다.
        rows = [{"Yesno": "0", "Gdate": "2026.10.14", "Jubun": "11", "Gjisa": "", "Gcode": "1017"}]
        record = AsyncMock()
        res, order = self._request(rows, record)
        self.assertIsNotNone(res)
        self.assertEqual(order[0], "record")

    def test_missing_slip_records_nothing(self) -> None:
        record = AsyncMock()
        res, _order = self._request([], record)
        self.assertIsNone(res)
        record.assert_not_called()


class SideTable(unittest.TestCase):
    def setUp(self) -> None:
        drq._ensured.clear()

    def test_date_and_key_normalization(self) -> None:
        self.assertEqual(drq.date8("2026.10.20"), "20261020")
        self.assertEqual(drq.date8("2026-10-20"), "20261020")
        self.assertEqual(drq.date8("2026.10"), "")
        self.assertEqual(drq.slip_key(" 5019", "2026-10-20", "1 ", " 온라인", "00004"),
                         ("5019", "20261020", "1", "온라인", "00004"))

    def test_record_dedupes_and_skips_incomplete(self) -> None:
        q = AsyncMock(return_value=[])
        with patch.object(drq, "execute_query", q):
            n = _run(drq.record(_SID, [
                {"hcode": "5019", "gdate": "2026.10.20", "jubun": "1", "gjisa": "", "gcode": "00431"},
                {"hcode": "5019", "gdate": "2026-10-20", "jubun": "1", "gjisa": "", "gcode": "00431"},  # 같은 전표
                {"hcode": "", "gdate": "2026.10.20", "jubun": "1", "gjisa": "", "gcode": "x"},  # 회사 없음
            ]))
        self.assertEqual(n, 1)
        sqls = [c.args[1] for c in q.call_args_list]
        self.assertTrue(sqls[0].startswith("CREATE TABLE IF NOT EXISTS Web_Dispatch_Request"))
        self.assertEqual(q.call_args_list[1].args[2][:5], ("5019", "20261020", "1", "", "00431"))

    def test_record_failure_is_swallowed(self) -> None:
        with patch.object(drq, "execute_query", AsyncMock(side_effect=RuntimeError("db down"))):
            self.assertEqual(_run(drq.record(_SID, [{"hcode": "5019", "gdate": "2026.10.20", "jubun": "1"}])), 0)

    def test_lookup_scopes_by_hcode_and_fails_closed(self) -> None:
        q = AsyncMock(side_effect=[[], [{"Hcode": "5019", "Gdate": "20261020", "Jubun": "1", "Gjisa": "", "Gcode": "00431"}]])
        with patch.object(drq, "execute_query", q):
            keys = _run(drq.requested_keys(_SID, "5019", "2026-10-14", "2026-10-20"))
        self.assertEqual(keys, {_key(TODAY_4)})
        sql, params = q.call_args_list[1].args[1:]
        self.assertIn("Hcode=%s", sql)
        self.assertEqual(params, ("5019", "20261014", "20261020"))
        with patch.object(drq, "execute_query", AsyncMock(side_effect=RuntimeError("db down"))):
            self.assertIsNone(_run(drq.requested_keys(_SID, "5019", "2026-10-14", "2026-10-20")))


class Filter(unittest.TestCase):
    def _filter(self, keys):
        with patch.object(drq, "requested_keys", AsyncMock(return_value=keys)):
            return _run(tsvc.web_requested_only(server_id=_SID, hcode="5019", items=SEVEN,
                                                date_from="2026-10-14", date_to="2026-10-20"))

    def test_0840_seven_slips_none_requested(self) -> None:
        # 그날 웹에서 출고요청한 것은 08:48:51 의 1 · 2번뿐 — 7건 중 어느 것도 자동출력 대상이 아니다.
        requested = {drq.slip_key("5019", "2026.10.20", "1", "", "2232"), drq.slip_key("5019", "2026.10.20", "1", "", "09002")}
        self.assertEqual(self._filter(requested), [])

    def test_requested_slip_passes_legacy_does_not(self) -> None:
        out = self._filter({_key(TODAY_4)})
        self.assertEqual([it["order_key"]["idnum"] for it in out], [4])

    def test_lookup_failure_prints_nothing(self) -> None:
        self.assertEqual(self._filter(None), [])


class Routes(unittest.TestCase):
    def setUp(self) -> None:
        tsvc._urgent_print_queue.clear()
        tsvc._auto_printed.clear()
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        auth = lambda: {"user_id": "교문사", "server_id": _SID, "hcode": "5019", "role": "operator", "permissions": ["outbound.write"]}  # noqa: E731
        app.dependency_overrides[get_current_user] = auth
        app.dependency_overrides[get_user_context] = auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in self._prev.items():
            if prev is None:
                app.dependency_overrides.pop(dep, None)
            else:
                app.dependency_overrides[dep] = prev

    def test_received_today_returns_only_requested(self) -> None:
        lookup = AsyncMock(return_value={_key(TODAY_5)})
        with patch.object(tsvc, "list_sales_statements", AsyncMock(return_value=(SEVEN, 7))), \
                patch.object(drq, "requested_keys", lookup):
            r = self.client.get(f"/api/v1/transactions/sales-statement/received-today?serverId={_SID}&days=7&today=2026-10-20",
                                headers={"Authorization": "Bearer t"})
        self.assertEqual(r.status_code, 200, r.text[:200])
        self.assertEqual([it["order_key"]["idnum"] for it in r.json()["items"]], [5])
        self.assertEqual(lookup.call_args.args, (_SID, "5019", "2026-10-14", "2026-10-20"))


class Stream(unittest.TestCase):
    def setUp(self) -> None:
        tsvc._urgent_print_queue.clear()
        tsvc._auto_printed.clear()

    def test_unrequested_slip_not_seen_until_requested(self) -> None:
        lookups = [set(), {_key(TODAY_3)}]

        async def fake_keys(*a, **k):  # noqa: ARG001
            return lookups.pop(0)

        async def run():
            out = []
            seen: set[str] = set()
            with patch.object(tsvc, "list_sales_statements", AsyncMock(return_value=(SEVEN, 7))), \
                    patch.object(drq, "requested_keys", side_effect=fake_keys), \
                    patch.object(tsvc.asyncio, "sleep", AsyncMock()):
                async for ev in tsvc._received_statement_ticks(
                    server_id=_SID, hcode="5019", date_from="2026-10-14", day="2026-10-20",
                    interval=2, max_ticks=2, seen=seen,
                ):
                    out.append(ev)
            return out, seen

        events, seen = _run(run())
        received = [e for e in events if e["type"] == "received"]
        self.assertEqual(len(received), 1, events)
        self.assertEqual([it["order_key"]["idnum"] for it in received[0]["items"]], [3])
        self.assertEqual(len(seen), 1)  # 나머지 6건은 seen 에 없다 — 나중에 출고요청되면 그때 넘긴다
        self.assertEqual(events[0]["type"], "heartbeat")  # 첫 tick: 접수 7건이지만 요청 기록 0 → 인쇄 없음


class Guards(unittest.TestCase):
    def test_update_order_insert_has_no_fixed_received_yesno(self) -> None:
        import inspect
        src = inspect.getsource(osvc.update_order)
        body = src.split("for key in desired_map.keys() - current_map.keys():", 1)[1].split("inserted += 1", 1)[0]
        self.assertNotIn('"0",', body)
        self.assertIn("slip_yesno", body)

    def test_received_paths_filter_by_request_record(self) -> None:
        import inspect
        from app.routers import transactions as tr
        self.assertIn("web_requested_only", inspect.getsource(tr.list_received_today_sales_statements))
        self.assertIn("web_requested_only", inspect.getsource(tsvc._received_statement_ticks))


if __name__ == "__main__":
    unittest.main()
