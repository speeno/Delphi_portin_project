"""DEC-360 — 「바로출고」: 받아서 인쇄할 자동출력 PC 가 없으면 사실대로 알린다.

배경(2026-10-01 교문사 「바로출고가 안 됩니다」): 바로출고는 접수 전이 + 긴급 출력 큐 적재까지만 하고,
인쇄·완료는 자동출력 탭(received-stream 구독)이 한다. 연결된 탭이 없으면 아무것도 인쇄되지 않는데
화면은 늘 「곧 인쇄됩니다」라고 안내했다(인쇄 기록상 교문사 웹 자동출력은 8월 13일 이후 0건).

가드: 구독자 수 집계(연결·해제) / 긴급 출력 큐 TTL / urgent-print·auto-print-status 응답 /
프론트 5곳이 공용 안내(`auto-print-notice`)를 쓴다.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))


class ListenerCountTests(unittest.IsolatedAsyncioTestCase):
    async def test_listener_counted_while_stream_open_and_released_after(self) -> None:
        from app.services import transactions_service as tsvc

        self.assertEqual(tsvc.auto_print_listener_count("L001"), 0)
        during: list[int] = []
        with patch.object(
            tsvc, "list_sales_statements", new=AsyncMock(return_value=([], 0))
        ), patch.object(tsvc.asyncio, "sleep", new=AsyncMock()):
            async for _ev in tsvc.stream_received_statements(
                server_id="srv", hcode="L001", today="2026-10-01", max_ticks=2
            ):
                during.append(tsvc.auto_print_listener_count("L001"))
                # 다른 회사 집계에 섞이지 않는다(hcode 스코프).
                self.assertEqual(tsvc.auto_print_listener_count("L999"), 0)
        self.assertEqual(during, [1, 1])
        self.assertEqual(tsvc.auto_print_listener_count("L001"), 0)  # 정상 종료 후 해제

    async def test_listener_released_when_client_disconnects(self) -> None:
        """탭을 닫으면(제너레이터 aclose) 집계에서 빠진다 — 유령 구독자가 남으면 영영 「곧 인쇄됩니다」."""
        from app.services import transactions_service as tsvc

        with patch.object(
            tsvc, "list_sales_statements", new=AsyncMock(return_value=([], 0))
        ), patch.object(tsvc.asyncio, "sleep", new=AsyncMock()):
            gen = tsvc.stream_received_statements(server_id="srv", hcode="L002", today="2026-10-01")
            await gen.__anext__()
            self.assertEqual(tsvc.auto_print_listener_count("L002"), 1)
            await gen.aclose()
        self.assertEqual(tsvc.auto_print_listener_count("L002"), 0)


class UrgentQueueTtlTests(unittest.TestCase):
    def test_stale_urgent_requests_are_dropped(self) -> None:
        """자동출력 PC 가 꺼진 동안 쌓인 요청이 몇 시간 뒤 한꺼번에 인쇄되지 않게 TTL 로 버린다."""
        from app.services import transactions_service as tsvc

        with patch.object(tsvc.time, "monotonic", return_value=1000.0):
            self.assertEqual(tsvc.enqueue_urgent_print("T001", ["old"]), 1)
        with patch.object(tsvc.time, "monotonic", return_value=1000.0 + tsvc._URGENT_PRINT_TTL_SEC - 1):
            self.assertEqual(tsvc.enqueue_urgent_print("T001", ["new"]), 1)
        with patch.object(tsvc.time, "monotonic", return_value=1000.0 + tsvc._URGENT_PRINT_TTL_SEC + 1):
            self.assertEqual(tsvc._drain_urgent_print("T001"), ["new"])
        self.assertEqual(tsvc._drain_urgent_print("T001"), [])


class RouterTests(unittest.TestCase):
    def setUp(self) -> None:
        from fastapi.testclient import TestClient

        from app.main import app
        from app.core.deps import get_user_context

        self.app = app
        self.dep = get_user_context
        self._prev = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_user_context] = lambda: {
            "user_id": "u1", "server_id": "remote_1", "hcode": "R001", "role": "user",
        }
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev is not None:
            self.app.dependency_overrides[self.dep] = self._prev
        else:
            self.app.dependency_overrides.pop(self.dep, None)

    def test_status_and_urgent_report_listeners(self) -> None:
        from app.services import transactions_service as tsvc

        r = self.client.get("/api/v1/transactions/sales-statement/auto-print-status?serverId=remote_1")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json(), {"listeners": 0})

        with patch.dict(tsvc._auto_print_listeners, {"R001": 2}):
            r = self.client.get("/api/v1/transactions/sales-statement/auto-print-status?serverId=remote_1")
            self.assertEqual(r.json(), {"listeners": 2})
            r = self.client.post(
                "/api/v1/transactions/sales-statement/urgent-print?serverId=remote_1",
                json={"keys": ["k1"]},
            )
            self.assertEqual(r.status_code, 200, r.text)
            self.assertEqual(r.json(), {"queued": 1, "listeners": 2})
        tsvc._drain_urgent_print("R001")  # 테스트 잔여 정리

    def test_status_route_not_swallowed_by_order_key_route(self) -> None:
        """정적 경로가 `/sales-statement/{order_key}` 보다 먼저 등록돼 있어야 한다."""
        r = self.client.get("/api/v1/transactions/sales-statement/auto-print-status?serverId=remote_1")
        self.assertIn("listeners", r.json())


class FrontendNoticeGuards(unittest.TestCase):
    def test_helper_tells_the_truth_when_no_listener(self) -> None:
        src = (FE / "lib/auto-print-notice.ts").read_text(encoding="utf-8")
        self.assertIn("listeners === 0", src)
        self.assertIn("지금 자동출력이 켜진 PC가 없어 인쇄되지 않습니다", src)
        self.assertIn("autoPrintStatus", src)

    def test_all_dispatch_spots_use_helper(self) -> None:
        for rel in (
            "app/(app)/outbound/orders/new/page.tsx",
            "components/outbound/order-detail-dialog.tsx",
            "components/transactions/transaction-status-screen.tsx",
        ):
            src = (FE / rel).read_text(encoding="utf-8")
            self.assertIn('from "@/lib/auto-print-notice"', src, rel)
            self.assertIn("autoPrintNotice(", src, rel)
        status = (FE / "components/transactions/transaction-status-screen.tsx").read_text(encoding="utf-8")
        # 단건 바로출고 · 배치 바로출고 · 바로재출고 3곳.
        self.assertEqual(status.count("autoPrintNotice("), 3)
        # 받아 줄 PC 가 없으면 선택을 남겨, 안내대로 곧바로 「거래 명세서 출력」을 누를 수 있다.
        self.assertIn("if (res.listeners !== 0) setCheckedKeys(new Set());", status)

    def test_probe_matrix_registers_status_route(self) -> None:
        probe = (ROOT / "debug/probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("sales-statement/auto-print-status", probe)


if __name__ == "__main__":
    unittest.main()
