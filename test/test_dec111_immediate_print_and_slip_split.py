"""DEC-111 — 거래명세서 즉시 출력(SSE 준실시간) + 전표 흡수 해소(출고 주문 목록).

두 축을 검증한다.

1. ``transactions_service.stream_received_statements`` — 접수 전표 SSE 제너레이터가
   **직전 tick 이후 새로 나타난 전표만** 방출하고(재방출 없음), 신규가 없으면 heartbeat 를
   내는지. 경리부 등 동일 hcode 다른 계정의 출고요청을 3분 폴 대기 없이 즉시 인쇄하는 근거.

2. ``outbound_service.list_orders`` — 출고 주문 목록 order_key 에 ``gjisa`` 가 실려,
   지점만 다른 전표(영풍문고 온라인·종각종로점)가 분리되는지(전표 2 흡수 해소, DEC-109 정합).
   GROUP BY 에 Gjisa·Idnum 포함은 test_list_count_grouped_mysql3 이 별도 검증.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

_PRODUCT_BACKEND = (
    Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
)
if str(_PRODUCT_BACKEND) not in sys.path:
    sys.path.insert(0, str(_PRODUCT_BACKEND))


def _received(gjisa: str, idnum: int) -> dict[str, Any]:
    return {
        "status": "received",
        "order_key": {
            "gdate": "2026.07.20",
            "hcode": "H001",
            "jubun": "J1",
            "gjisa": gjisa,
            "idnum": idnum,
        },
    }


_DONE = {"status": "done", "order_key": {"gdate": "2026.07.20", "hcode": "H001", "jubun": "J9"}}


class StreamReceivedStatementsTests(unittest.IsolatedAsyncioTestCase):
    async def test_emits_only_new_slips_then_heartbeat(self) -> None:
        from app.services import transactions_service as tsvc

        A = _received("온라인", 2)
        B = _received("종각종로점", 3)
        # tick1: A 접수 / tick2: A(기존)+B(신규) / tick3: 변화 없음
        list_mock = AsyncMock(
            side_effect=[
                ([A, _DONE], 2),
                ([A, B, _DONE], 3),
                ([A, B, _DONE], 3),
            ]
        )
        events: list[dict[str, Any]] = []
        with patch.object(tsvc, "list_sales_statements", new=list_mock), patch.object(
            tsvc.asyncio, "sleep", new=AsyncMock()
        ):
            async for ev in tsvc.stream_received_statements(
                server_id="srv", hcode="H001", today="2026-07-20", days=7, max_ticks=3
            ):
                events.append(ev)

        self.assertEqual(len(events), 3)
        # tick1 — A 만 방출(완료 건 제외)
        self.assertEqual(events[0]["type"], "received")
        self.assertEqual([it["order_key"]["idnum"] for it in events[0]["items"]], [2])
        # tick2 — B 만 방출(A 는 이미 방출됨 → 재방출 금지)
        self.assertEqual(events[1]["type"], "received")
        self.assertEqual([it["order_key"]["idnum"] for it in events[1]["items"]], [3])
        self.assertEqual(events[1]["items"][0]["order_key"]["gjisa"], "종각종로점")
        # tick3 — 신규 없음 → heartbeat
        self.assertEqual(events[2]["type"], "heartbeat")

    async def test_urgent_queue_emitted_and_scoped_by_hcode(self) -> None:
        """긴급 출력 큐(바로출고/바로재출고) 적재분이 hcode 스코프로 'urgent' 방출된다."""
        from app.services import transactions_service as tsvc

        # 다른 hcode 적재분은 방출되지 않아야(격리).
        self.assertEqual(tsvc.enqueue_urgent_print("H001", ["k1", "k2"]), 2)
        self.assertEqual(tsvc.enqueue_urgent_print("H999", ["z9"]), 1)
        self.assertEqual(tsvc.enqueue_urgent_print("H001", ["", "  "]), 0)  # 공백 제외

        events: list[dict[str, Any]] = []
        with patch.object(
            tsvc, "list_sales_statements", new=AsyncMock(return_value=([_DONE], 1))
        ), patch.object(tsvc.asyncio, "sleep", new=AsyncMock()):
            async for ev in tsvc.stream_received_statements(
                server_id="srv", hcode="H001", today="2026-07-20", max_ticks=2
            ):
                events.append(ev)

        # tick1 — 접수 신규 없음 + 긴급 큐 방출(k1,k2). tick2 — 큐 비었으니 heartbeat.
        self.assertEqual(events[0]["type"], "urgent")
        self.assertEqual(events[0]["keys"], ["k1", "k2"])
        self.assertEqual(events[1]["type"], "heartbeat")
        # H999 적재분은 H001 스트림에 새지 않음(격리 유지).
        self.assertEqual(tsvc._drain_urgent_print("H999"), ["z9"])


class ListOrdersGjisaOrderKeyTests(unittest.IsolatedAsyncioTestCase):
    async def test_order_key_includes_gjisa_and_splits_by_branch(self) -> None:
        """지점만 다른 두 전표 행이 각각 order_key.gjisa/idnum 을 실어 반환된다."""
        from app.services import outbound_service as osvc

        rows = [
            {
                "Gdate": "2026.07.20", "Hcode": "H001", "stmt_gcode": "00004",
                "Jubun": "J1", "gjisa": "온라인", "line_count": 1, "qty": 1,
                "amount": 1000, "yesno_max": "0", "idnum": 2,
            },
            {
                "Gdate": "2026.07.20", "Hcode": "H001", "stmt_gcode": "00004",
                "Jubun": "J1", "gjisa": "종각종로점", "line_count": 1, "qty": 1,
                "amount": 2000, "yesno_max": "0", "idnum": 3,
            },
        ]
        with patch.object(osvc, "execute_query", new=AsyncMock(return_value=rows)), patch.object(
            osvc, "fetch_g1_customer_gnames", new=AsyncMock(return_value={("H001", "00004"): "(주)영풍문고"})
        ), patch.object(osvc, "count_grouped", new=AsyncMock(return_value=2)), patch.object(
            osvc, "mysql3_protocol", return_value=True
        ):
            items, total = await osvc.list_orders(
                server_id="srv", date_from="2026-07-20", date_to="2026-07-20"
            )

        self.assertEqual(total, 2)
        self.assertEqual(len(items), 2)
        by_idnum = {it["order_key"]["idnum"]: it["order_key"] for it in items}
        self.assertEqual(by_idnum[2]["gjisa"], "온라인")
        self.assertEqual(by_idnum[3]["gjisa"], "종각종로점")
        # 두 전표 모두 같은 거래처·Jubun 이지만 지점(gjisa)으로 분리 — 흡수되지 않는다.
        self.assertEqual(by_idnum[2]["gcode"], "00004")
        self.assertEqual(by_idnum[3]["jubun"], "J1")


if __name__ == "__main__":
    unittest.main()
