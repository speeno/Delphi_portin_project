"""DEC-396 — 자동출력: 바로출고 한 번에 같은 명세서가 두 장 나오던 문제.

교문사 2026-10-12 Render 로그(KST)
- 08:56:16 바로출고 1건(부곡리(본관)) → 08:56:18 ``…|0||00001.html``(바로출고 키) 인쇄 · 완료
  → 08:56:27 ``…|9|출고|00001.html``(접수 목록 키) **다시 인쇄**.
- 08:38 바로출고 8건(자동출력 창 없음) → 08:41:58 창이 열리며 접수 목록 키로 8건 인쇄 → 08:42:14 바로출고 키로 8건 **다시**.
원인: 출고현황의 바로출고 키(전표번호 0 · 구분 '')와 접수 목록 키(전표번호 · 「출고」)는 같은 전표인데 문자열이 달라
자동출력 창의 중복 확인(키 문자열)을 통과했다.

가드
----
- 같은 전표 판정: 일자 · 회사 · 차수 · 지점 · 거래처 + (한쪽이 0/빈 값이면 포함) 전표번호 · 구분.
- 인쇄 라우트(source=auto)는 다른 키로 120초 안에 자동출력된 전표를 뺀다. 바로출고/바로재출고 키는 요청 10초 전 이후 인쇄만 본다.
  전부 빠지면 print() 를 막는 빈 문서(구 번들 창도 빈 장 없음) · X-Printed-Keys = [].
- 이미 인쇄된 바로출고 키는 전달(claim)하지 않고 큐에서 뺀다 · 접수 스트림/폴은 방금 인쇄 · 전달된 전표를 넘기지 않는다(다음 확인 때 다시 봄).
- 같은 키 재요청(실패 재시도) · 서로 다른 전표번호 · 120초 지난 인쇄 · 인쇄 뒤 누른 바로재출고는 그대로 찍힌다.
"""

from __future__ import annotations

import asyncio
import base64
import json
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.deps import get_user_context
from app.main import app
from app.routers.auth import get_current_user
from app.services import print_log_db, tenant_print_assets, transactions_service as tsvc

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
_SID = "remote_153"
_GJISA = "2.부곡리(본관)"
_GJISA_ENC = "2.%EB%B6%80%EA%B3%A1%EB%A6%AC(%EB%B3%B8%EA%B4%80)"
# 출고현황 바로출고 키(전표번호 0 · 구분 '') — 운영 로그 그대로
URGENT = f"2026.10.12|5019|1|{_GJISA_ENC}|0||00001"
# 접수 목록(received-today · 스트림) 키 — 같은 전표
RECEIVED = f"2026.10.12|5019|1|{_GJISA_ENC}|9|%EC%B6%9C%EA%B3%A0|00001"
RECEIVED_OK = {"gdate": "2026.10.12", "hcode": "5019", "jubun": "1", "gjisa": _GJISA, "idnum": 9, "gubun": "출고", "gcode": "00001"}
OTHER = "2026.10.12|5019|1||8|%EC%B6%9C%EA%B3%A0|3332"


def _reset() -> None:
    tsvc._urgent_print_queue.clear()
    tsvc._auto_print_beats.clear()
    tsvc._auto_printed.clear()


def _age_records(sec: float) -> None:
    for recs in tsvc._auto_printed.values():
        for r in recs:
            r["t"] -= sec


def _decode(v: str) -> list[str]:
    return json.loads(base64.b64decode(v).decode("utf-8"))


def _slips(v: str) -> list[tuple]:
    """X-Printed-Keys → 전표 축(테스트 클라이언트가 경로의 %xx 를 한 번 더 풀어도 같은 판정)."""
    return [tsvc._slip_identity(k)["base"] + (tsvc._slip_identity(k)["idnum"],) for k in _decode(v)]


def _slip(k: str) -> tuple:
    i = tsvc._slip_identity(k)
    return i["base"] + (i["idnum"],)


class SameSlip(unittest.TestCase):
    def test_urgent_and_received_keys_are_the_same_slip(self) -> None:
        u, r = tsvc._slip_identity(URGENT), tsvc._slip_identity(RECEIVED)
        self.assertTrue(tsvc._same_slip(u, r))
        self.assertTrue(tsvc._same_slip(tsvc._slip_identity(RECEIVED_OK), u))  # dict(order_key) 도 같은 판정

    def test_different_slips(self) -> None:
        r9 = tsvc._slip_identity(RECEIVED)
        self.assertFalse(tsvc._same_slip(r9, tsvc._slip_identity(RECEIVED.replace("|9|", "|8|"))))  # 다른 전표번호
        self.assertFalse(tsvc._same_slip(r9, tsvc._slip_identity(RECEIVED.replace("|00001", "|00002"))))  # 다른 거래처
        self.assertFalse(tsvc._same_slip(r9, tsvc._slip_identity(RECEIVED.replace("2026.10.12", "2026.10.13"))))
        self.assertIsNone(tsvc._slip_identity("2026.10.12|5019|1|"))  # 거래처 없는 구 키는 판정 안 함


class Filter(unittest.TestCase):
    def setUp(self) -> None:
        _reset()

    def test_0856_received_after_urgent_is_skipped(self) -> None:
        tsvc.enqueue_urgent_print("5019", [URGENT])
        tsvc.record_auto_print_beat("5019", "ap-1")
        self.assertEqual(tsvc._urgent_for_listener("5019", "ap-1"), [URGENT])
        self.assertTrue(tsvc.received_already_covered(RECEIVED_OK))  # 전달(claim)된 바로출고 키에 포함
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [True])
        tsvc.record_auto_printed([URGENT])
        tsvc.ack_urgent_print("5019", [URGENT])
        self.assertTrue(tsvc.received_already_covered(RECEIVED_OK))  # 방금 인쇄됨
        self.assertEqual(tsvc.auto_print_filter([RECEIVED, OTHER]), [False, True])

    def test_0842_urgent_after_received_print_is_dropped(self) -> None:
        tsvc.enqueue_urgent_print("5019", [URGENT])
        tsvc._urgent_print_queue["5019"][0]["ts"] -= 200  # 창이 없을 때 적재(08:38)
        tsvc.record_auto_printed([RECEIVED])  # 창이 열리며 접수 목록으로 인쇄(08:41:58)
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [False])
        tsvc.record_auto_print_beat("5019", "ap-1")
        self.assertEqual(tsvc._urgent_for_listener("5019", "ap-1"), [])  # 다시 주지 않고
        self.assertNotIn("5019", tsvc._urgent_print_queue)  # 큐에서도 뺀다

    def test_received_first_then_urgent_within_same_moment(self) -> None:
        tsvc.record_auto_printed([RECEIVED])  # 출고요청 직후 접수 스트림이 먼저 넘긴 경우
        tsvc.enqueue_urgent_print("5019", [URGENT])  # 0.2초 뒤 바로출고 적재
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [False])

    def test_reprint_pressed_after_seeing_print_is_printed(self) -> None:
        tsvc.record_auto_printed([RECEIVED])
        _age_records(30)  # 30초 전 인쇄를 보고
        tsvc.enqueue_urgent_print("5019", [URGENT])  # 바로재출고
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [True])
        tsvc.record_auto_print_beat("5019", "ap-1")
        self.assertEqual(tsvc._urgent_for_listener("5019", "ap-1"), [URGENT])

    def test_same_key_retry_is_printed(self) -> None:
        tsvc.record_auto_printed([URGENT])  # 문서는 받아 갔지만 창에서 인쇄 실패 → 같은 키 재시도
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [True])
        _reset()
        tsvc.record_auto_printed([RECEIVED])
        self.assertEqual(tsvc.auto_print_filter([RECEIVED]), [True])

    def test_other_slip_number_and_expiry(self) -> None:
        tsvc.record_auto_printed([RECEIVED])
        self.assertEqual(tsvc.auto_print_filter([RECEIVED.replace("|9|", "|8|")]), [True])  # 같은 거래처 다른 전표
        _age_records(tsvc._AUTO_PRINT_DEDUP_SEC + 1)
        self.assertEqual(tsvc.auto_print_filter([URGENT]), [True])
        self.assertFalse(tsvc.received_already_covered(RECEIVED_OK))

    def test_same_slip_twice_in_one_request(self) -> None:
        self.assertEqual(tsvc.auto_print_filter([URGENT, RECEIVED, OTHER, OTHER]), [True, False, True, False])

    def test_unclaimed_urgent_does_not_hide_received(self) -> None:
        tsvc.enqueue_urgent_print("5019", [URGENT])  # 받아 갈 창이 아직 없다 → 접수 목록은 종전대로
        self.assertFalse(tsvc.received_already_covered(RECEIVED_OK))


class Stream(unittest.TestCase):
    def setUp(self) -> None:
        _reset()

    def _events(self, items):
        async def run():
            out = []
            # DEC-409 — 접수 전표는 모두 웹 출고요청분으로 본다(요청 기록 필터는 test_dec409 에서).
            with patch.object(tsvc, "list_sales_statements", AsyncMock(return_value=(items, len(items)))), \
                    patch.object(tsvc, "web_requested_only", AsyncMock(side_effect=lambda **kw: kw["items"])):
                async for ev in tsvc._received_statement_ticks(
                    server_id=_SID, hcode="5019", date_from="2026-10-06", day="2026-10-12",
                    interval=2, max_ticks=1, seen=seen,
                ):
                    out.append(ev)
            return out

        seen: set[str] = set()
        return asyncio.run(run()), seen

    def test_stream_holds_back_just_printed_slip(self) -> None:
        tsvc.record_auto_printed([URGENT])
        other = {"status": "received", "order_key": {**RECEIVED_OK, "gcode": "00002", "idnum": 3}}
        events, seen = self._events([{"status": "received", "order_key": RECEIVED_OK}, other])
        received = [e for e in events if e["type"] == "received"]
        self.assertEqual([it["order_key"]["gcode"] for it in received[0]["items"]], ["00002"])
        self.assertEqual(len(seen), 1)  # 건너뛴 전표는 seen 에 넣지 않는다(다음 tick 에 다시 본다)


class Routes(unittest.TestCase):
    def setUp(self) -> None:
        _reset()
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        auth = lambda: {"user_id": "u1", "server_id": _SID, "hcode": "5019", "role": "operator", "permissions": ["outbound.write"]}  # noqa: E731
        app.dependency_overrides[get_current_user] = auth
        app.dependency_overrides[get_user_context] = auth
        self.client = TestClient(app)
        self.hdr = {"Authorization": "Bearer t"}

    def tearDown(self) -> None:
        _reset()
        for dep, prev in self._prev.items():
            if prev is None:
                app.dependency_overrides.pop(dep, None)
            else:
                app.dependency_overrides[dep] = prev

    def _print(self, path: str):
        detail = {"order_key": {"gdate": "2026.10.12", "hcode": "5019", "jubun": "1", "gjisa": ""},
                  "customer": {"hcode": "5019", "gname": "거래처"},
                  "lines": [{"gcode": "1", "bcode": "B1", "product_name": "도서", "gsqut": 1, "gdang": 1000, "grat1": 70, "gssum": 700}]}
        self.detail = AsyncMock(return_value=detail)
        with patch.object(tsvc, "get_sales_statement_detail", self.detail), \
                patch.object(tenant_print_assets, "hydrate_seal_from_db", AsyncMock(return_value=None)), \
                patch.object(print_log_db, "record_printed", AsyncMock(return_value=1)):
            return self.client.get(path, headers=self.hdr)

    @staticmethod
    def _enc(key: str) -> str:
        return key.replace("%", "%25").replace("|", "%7C")

    def test_auto_print_of_duplicate_is_blank_and_never_prints(self) -> None:
        r1 = self._print(f"/api/v1/print/sales-statement/{self._enc(URGENT)}.html?serverId={_SID}&layout=legacy_triplicate&source=auto")
        self.assertEqual(r1.status_code, 200, r1.text[:200])
        self.assertEqual(_slips(r1.headers["X-Printed-Keys"]), [_slip(URGENT)])
        r2 = self._print(f"/api/v1/print/sales-statement/{self._enc(RECEIVED)}.html?serverId={_SID}&layout=legacy_triplicate&source=auto")
        self.assertEqual(r2.status_code, 200, r2.text[:200])
        self.assertEqual(_decode(r2.headers["X-Printed-Keys"]), [])
        self.assertIn("window.print=function(){}", r2.text)  # 구 번들 창이 print() 를 불러도 빈 장이 나오지 않는다
        self.assertIn("<html", r2.text)
        self.detail.assert_not_awaited()  # 상세 조회도 하지 않는다
        r3 = self._print(f"/api/v1/print/sales-statement/{self._enc(RECEIVED)}.pdf?serverId={_SID}&source=auto")
        self.assertEqual(r3.status_code, 409)
        r4 = self._print(f"/api/v1/print/sales-statement/{self._enc(RECEIVED)}.html?serverId={_SID}&layout=legacy_triplicate")
        self.assertEqual(_slips(r4.headers["X-Printed-Keys"]), [_slip(RECEIVED)])  # 수동 인쇄는 그대로

    def test_batch_keeps_only_new_slips_and_acks_skipped_urgent(self) -> None:
        tsvc.enqueue_urgent_print("5019", [URGENT])
        tsvc.record_auto_printed([RECEIVED])
        keys = ",".join(self._enc(k) for k in (URGENT, OTHER))
        r = self._print(f"/api/v1/print/sales-statement/batch.html?serverId={_SID}&keys={keys}&layout=legacy_triplicate&source=auto")
        self.assertEqual(r.status_code, 200, r.text[:200])
        self.assertEqual(_slips(r.headers["X-Printed-Keys"]), [_slip(OTHER)])
        self.assertEqual(self.detail.await_count, 1)
        self.assertNotIn("5019", tsvc._urgent_print_queue)

    def test_received_today_hides_just_printed_slip(self) -> None:
        tsvc.record_auto_printed([URGENT])
        items = [{"status": "received", "order_key": RECEIVED_OK},
                 {"status": "received", "order_key": {**RECEIVED_OK, "gcode": "00002"}}]
        with patch.object(tsvc, "list_sales_statements", AsyncMock(return_value=(items, 2))), \
                patch.object(tsvc, "web_requested_only", AsyncMock(side_effect=lambda **kw: kw["items"])):  # DEC-409 — 모두 웹 출고요청분
            r = self.client.get(f"/api/v1/transactions/sales-statement/received-today?serverId={_SID}&days=7", headers=self.hdr)
        self.assertEqual(r.status_code, 200, r.text[:200])
        self.assertEqual([it["order_key"]["gcode"] for it in r.json()["items"]], ["00002"])


class Frontend(unittest.TestCase):
    def test_empty_printed_keys_skip_print(self) -> None:
        api = (FE / "lib" / "print-api.ts").read_text(encoding="utf-8")
        body = api.split("export async function printHtmlFromUrl", 1)[1]
        self.assertLess(body.index("printedKeys.length === 0) return printedKeys"), body.index("iframe.srcdoc = html"))
        page = (FE / "app" / "(app)" / "transactions" / "sales-statement" / "auto-print" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("if (done.length === 0) return new Set();", page)


if __name__ == "__main__":
    unittest.main()
