"""DEC-391 — 바로출고 긴급 키: 문서를 받아 갈 때까지 큐에 남기고(ack), 생존 신호가 있는 창에만 전달.

교문사 2026-10-07 21:55 — 1건은 3초 안에 인쇄됐지만 곧이은 5건은 모니터가 문서를 요청조차 하지 않았다(Render 로그에 batch.html 없음).
서버는 «먼저 tick 한 스트림 연결»에 키를 주고 잊었고, 재로그인(21:54)으로 닫힌 이전 창의 스트림 연결이 프록시 뒤에서 살아남아 키를 삼켰다.

가드
----
- claim: 미전달 · 전달 후 15초 안에 ack 없는 항목만 준다 → ack(인쇄 라우트 source=auto) 로 제거.
- 생존 신호(beat)가 없는 client 연결엔 주지 않는다 · client 없는 구독(구 번들)은 종전대로.
- 인쇄 라우트가 ack 한다 · 스트림 라우트 `client` 파라미터 · 프론트 clientId 배선 · 조회 전용 계정도 urgent-print 허용.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.deps import get_user_context
from app.main import app
from app.routers.auth import get_current_user
from app.services import account_write_policy as awp
from app.services import print_log_db, tenant_print_assets, transactions_service as tsvc

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"
_SID = "remote_1"
_KEY = "2026.10.07|H1|00001|"


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class ClaimAck(unittest.TestCase):
    def setUp(self) -> None:
        tsvc._urgent_print_queue.clear()
        tsvc._auto_print_beats.clear()

    def test_claim_stays_until_ack(self) -> None:
        self.assertEqual(tsvc.enqueue_urgent_print("H1", ["a", "b"]), 2)
        tsvc.record_auto_print_beat("H1", "c1")
        self.assertEqual(tsvc._urgent_for_listener("H1", "c1"), ["a", "b"])
        self.assertEqual(tsvc._urgent_for_listener("H1", "c1"), [])  # 15초 안엔 다시 주지 않는다
        for e in tsvc._urgent_print_queue["H1"]:
            e["claimed_at"] -= tsvc._URGENT_CLAIM_TTL_SEC + 1  # 받아 가지 않은 채 15초 경과
        self.assertEqual(tsvc._urgent_for_listener("H1", "c1"), ["a", "b"])
        self.assertEqual(tsvc.ack_urgent_print("H1", ["a"]), 1)
        for e in tsvc._urgent_print_queue["H1"]:
            e["claimed_at"] -= tsvc._URGENT_CLAIM_TTL_SEC + 1
        self.assertEqual(tsvc._urgent_for_listener("H1", "c1"), ["b"])
        self.assertEqual(tsvc.ack_urgent_print("H1", ["b"]), 1)
        self.assertNotIn("H1", tsvc._urgent_print_queue)

    def test_stale_connection_gets_nothing(self) -> None:
        tsvc.enqueue_urgent_print("H1", ["a"])
        self.assertEqual(tsvc._urgent_for_listener("H1", "dead-window"), [])  # 생존 신호 없음
        tsvc.record_auto_print_beat("H1", "live")
        self.assertEqual(tsvc._urgent_for_listener("H1", "live"), ["a"])
        tsvc.record_auto_print_beat("H1", "live", stop=True)
        tsvc.enqueue_urgent_print("H1", ["z"])
        self.assertEqual(tsvc._urgent_for_listener("H1", "live"), [])  # 정지한 창
        self.assertEqual(tsvc._urgent_for_listener("H1", None), ["z"])  # 구 번들(client 없음)은 종전대로

    def test_drain_compat(self) -> None:
        tsvc.enqueue_urgent_print("H1", ["a"])
        self.assertEqual(tsvc._drain_urgent_print("H1"), ["a"])
        self.assertEqual(tsvc._drain_urgent_print("H1"), [])


class PrintRouteAcks(unittest.TestCase):
    def setUp(self) -> None:
        tsvc._urgent_print_queue.clear()
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        auth = lambda: {"user_id": "u1", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": ["outbound.write"]}  # noqa: E731
        app.dependency_overrides[get_current_user] = auth
        app.dependency_overrides[get_user_context] = auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in self._prev.items():
            if prev is None:
                app.dependency_overrides.pop(dep, None)
            else:
                app.dependency_overrides[dep] = prev

    def _get(self, source: str) -> int:
        detail = {"order_key": {"gdate": "2026.10.07", "hcode": "H1", "jubun": "00001", "gjisa": ""},
                  "customer": {"hcode": "H1", "gname": "거래처"},
                  "lines": [{"gcode": "1", "bcode": "B1", "product_name": "도서", "gsqut": 1, "gdang": 1000, "grat1": 70, "gssum": 700}]}
        with patch.object(tsvc, "get_sales_statement_detail", AsyncMock(return_value=detail)), \
                patch.object(tenant_print_assets, "hydrate_seal_from_db", AsyncMock(return_value=None)), \
                patch.object(print_log_db, "record_printed", AsyncMock(return_value=1)):
            r = self.client.get(
                f"/api/v1/print/sales-statement/{_KEY.replace('|', '%7C')}.html?serverId={_SID}&layout=legacy_triplicate&source={source}",
                headers={"Authorization": "Bearer t"},
            )
        return r.status_code

    def test_auto_fetch_acks_queue(self) -> None:
        tsvc.enqueue_urgent_print("H1", [_KEY, "other"])
        self.assertEqual(self._get("manual"), 200)
        self.assertEqual([e["key"] for e in tsvc._urgent_print_queue["H1"]], [_KEY, "other"])  # 수동 인쇄는 ack 아님
        self.assertEqual(self._get("auto"), 200)
        self.assertEqual([e["key"] for e in tsvc._urgent_print_queue["H1"]], ["other"])


class Wiring(unittest.TestCase):
    def test_stream_client_param_and_frontend(self) -> None:
        router = (BACK / "routers" / "transactions.py").read_text(encoding="utf-8")
        self.assertIn("client_id=client,", router)
        self.assertIn('"urgent-print queued=%d listeners=%d active=%d hcode=%s user=%s"', router)
        self.assertIn("client: params.clientId,", _read("lib/auto-print-stream.ts"))
        self.assertIn("clientId: beatIdRef.current,", _read("app/(app)/transactions/sales-statement/auto-print/page.tsx"))

    def test_read_only_account_may_request_urgent_print(self) -> None:
        awp.reload_for_tests()
        claims = {"hcode": "5019", "login_profile": "publisher_main", "rdb": "chul_09_db"}
        self.assertTrue(awp.is_read_only_account(claims))
        self.assertFalse(awp.blocks(claims, "POST", "/api/v1/transactions/sales-statement/urgent-print"))
        self.assertTrue(awp.blocks(claims, "POST", "/api/v1/transactions/sales-statement"))


if __name__ == "__main__":
    unittest.main()
