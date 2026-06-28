"""DEC-033 회귀 가드 — 출고/입고 LIST 가 mysql3 서버에서 COALESCE(1064) 대신 IFNULL 사용.

적대적 리뷰(DEC-065) 확정 findings #1: ``list_orders``/``list_receipts`` 가 mysql3_protocol
서버에서 raw COALESCE 를 방출해 1064→HTTP 500 발생. ``mysql3_protocol`` 분기
패턴(mysql3 시 IFNULL)으로 수정. 본 가드는 실제 방출 SQL 문자열을 캡처해 검증한다
(기존 테스트는 SQL 을 모킹해 이 결함을 놓쳤다).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import inbound_service, outbound_service  # noqa: E402


class OutboundListMysql3Test(IsolatedAsyncioTestCase):
    async def test_list_orders_uses_ifnull_on_mysql3(self) -> None:
        captured: dict = {}

        async def fake_exec(_sid, sql, _params=()):
            captured["sql"] = sql
            return []

        async def fake_count(*a, **kw):
            captured["group_by"] = kw.get("group_by")
            return 0

        async def fake_names(*a, **kw):
            return {}

        with patch.object(outbound_service, "mysql3_protocol", return_value=True), \
             patch.object(outbound_service, "execute_query", side_effect=fake_exec), \
             patch.object(outbound_service, "count_grouped", side_effect=fake_count), \
             patch.object(outbound_service, "fetch_g1_customer_gnames", side_effect=fake_names):
            await outbound_service.list_orders(
                server_id="remote_154", hcode=None,
                date_from="2026-04-01", date_to="2026-04-30", limit=10, offset=0,
            )
        self.assertIn("IFNULL", captured["sql"])
        self.assertNotIn("COALESCE", captured["sql"])
        self.assertNotIn("COALESCE", captured.get("group_by") or "")

    async def test_list_orders_keeps_coalesce_on_modern(self) -> None:
        captured: dict = {}

        async def fake_exec(_sid, sql, _params=()):
            captured["sql"] = sql
            return []

        async def fake_count(*a, **kw):
            return 0

        async def fake_names(*a, **kw):
            return {}

        with patch.object(outbound_service, "mysql3_protocol", return_value=False), \
             patch.object(outbound_service, "execute_query", side_effect=fake_exec), \
             patch.object(outbound_service, "count_grouped", side_effect=fake_count), \
             patch.object(outbound_service, "fetch_g1_customer_gnames", side_effect=fake_names):
            await outbound_service.list_orders(
                server_id="remote_138", hcode=None,
                date_from="2026-04-01", date_to="2026-04-30", limit=10, offset=0,
            )
        # 모던 서버는 COALESCE 유지(동작 동일, 회귀 0).
        self.assertIn("COALESCE", captured["sql"])


class InboundListMysql3Test(IsolatedAsyncioTestCase):
    async def test_list_receipts_uses_ifnull_on_mysql3(self) -> None:
        captured: dict = {}

        async def fake_exec(_sid, sql, _params=()):
            captured["sql"] = sql
            return []

        async def fake_count(*a, **kw):
            captured["group_by"] = kw.get("group_by")
            return 0

        async def fake_pub(*a, **kw):
            return {}

        async def fake_ven(*a, **kw):
            return {}

        with patch.object(inbound_service, "mysql3_protocol", return_value=True), \
             patch.object(inbound_service, "execute_query", side_effect=fake_exec), \
             patch.object(inbound_service, "count_grouped", side_effect=fake_count), \
             patch.object(inbound_service, "_fetch_publisher_names", side_effect=fake_pub), \
             patch.object(inbound_service, "_fetch_vendor_names", side_effect=fake_ven):
            await inbound_service.list_receipts(
                server_id="remote_155", hcode=None, gcode=None,
                date_from="2026-04-01", date_to="2026-04-30", limit=10, offset=0,
            )
        self.assertIn("IFNULL", captured["sql"])
        self.assertNotIn("COALESCE", captured["sql"])
        self.assertNotIn("COALESCE", captured.get("group_by") or "")


if __name__ == "__main__":
    main()
