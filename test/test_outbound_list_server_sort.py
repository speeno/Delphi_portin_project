"""출고 목록 서버 정렬(sort_by/sort_dir) 회귀 — 전체 결과 정렬 후 페이징.

사용자 보고(2026-07-05): 정렬 가능한 표에서 여러 페이지가 있을 때 정렬하면 로딩된
페이지만 정렬되던 문제(클라이언트 정렬). 서버가 전체 조건 결과를 ORDER BY 로 정렬 후
LIMIT/OFFSET 하도록 변경. 본 가드는 방출 SQL 의 ORDER BY 절을 캡처해 검증한다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import outbound_service  # noqa: E402


async def _capture_list_sql(*, sort_by, sort_dir, mysql3=False) -> str:
    captured: dict = {}

    async def fake_exec(_sid, sql, _params=()):
        captured["sql"] = sql
        return []

    async def fake_count(*a, **kw):
        return 0

    async def fake_names(*a, **kw):
        return {}

    with patch.object(outbound_service, "mysql3_protocol", return_value=mysql3), \
         patch.object(outbound_service, "execute_query", side_effect=fake_exec), \
         patch.object(outbound_service, "count_grouped", side_effect=fake_count), \
         patch.object(outbound_service, "fetch_g1_customer_gnames", side_effect=fake_names):
        await outbound_service.list_orders(
            server_id="remote_138", hcode=None,
            date_from="2026-04-01", date_to="2026-04-30", limit=10, offset=0,
            sort_by=sort_by, sort_dir=sort_dir,
        )
    return captured["sql"]


class OutboundListServerSortTest(IsolatedAsyncioTestCase):
    async def test_default_order_by_when_no_sort(self) -> None:
        sql = await _capture_list_sql(sort_by=None, sort_dir=None)
        self.assertIn("ORDER BY Gdate DESC, Hcode, Gcode,", sql)
        # LIMIT/OFFSET 치환 대상 리터럴이 ORDER BY 뒤에 그대로 남아야 한다.
        self.assertIn("LIMIT %s OFFSET %s", sql)

    async def test_amount_desc_sort_orders_by_alias(self) -> None:
        sql = await _capture_list_sql(sort_by="amount", sort_dir="desc")
        self.assertIn("ORDER BY amount DESC", sql)

    async def test_qty_asc_sort(self) -> None:
        sql = await _capture_list_sql(sort_by="qty", sort_dir="asc")
        self.assertIn("ORDER BY qty ASC", sql)

    async def test_jubun_sort_is_numeric(self) -> None:
        """전표번호는 문자열 컬럼이라 숫자 정렬(``+0``)해야 13 > 2 가 올바르다."""
        sql = await _capture_list_sql(sort_by="jubun", sort_dir="asc")
        self.assertIn("+0 ASC", sql)

    async def test_unknown_sort_key_falls_back_to_default(self) -> None:
        sql = await _capture_list_sql(sort_by="__evil__ DROP TABLE", sort_dir="desc")
        # 화이트리스트 밖 → 기본 정렬(주입 차단).
        self.assertIn("ORDER BY Gdate DESC, Hcode, Gcode,", sql)
        self.assertNotIn("DROP TABLE", sql)

    async def test_sort_uses_ifnull_on_mysql3(self) -> None:
        sql = await _capture_list_sql(sort_by="jubun", sort_dir="asc", mysql3=True)
        self.assertIn("IFNULL", sql)
        self.assertNotIn("COALESCE", sql)


if __name__ == "__main__":
    main()
