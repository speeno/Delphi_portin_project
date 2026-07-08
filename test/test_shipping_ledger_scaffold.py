"""발송비 내역·현황 API — GET shipping-ledger / shipping-status (DEC-091 T1_Ssub).

레거시 Subu43/44 = T1_Ssub 발송비. W2 scaffold(빈 목록) → 실 쿼리 이식.
- 테이블 보유 테넌트: 실 데이터 + scaffold=False.
- T1_Ssub 미보유 테넌트: 빈 목록 + scaffold=True (500 방지).
- SQL 정합: T1_Ssub / 일자키 / 출판사 스코프 / Yesno 절 없음 / 정렬 화이트리스트.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import shipping_ledger_service as svc  # noqa: E402

_SID = "remote_138"


def _pick_list_sql(cap):
    """캡처된 SQL 중 목록(SELECT, 비-COUNT, 비-SHOW) 쿼리."""
    for s, _ in cap:
        up = s.strip().upper()
        if up.startswith("SELECT") and not up.startswith("SELECT COUNT("):
            return s
    raise AssertionError("list SQL not captured")

_T1_COLS = [
    {"Field": c}
    for c in ("Gdate", "Hcode", "Gcode", "Gname", "Name1", "Name2", "Gssum")
]


class ShippingLedgerServiceTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        svc.clear_t1_column_cache_for_tests()

    def tearDown(self) -> None:
        svc.clear_t1_column_cache_for_tests()

    async def _run(self, fn, captured, *, table_exists=True, **kw):
        async def fake_execute(server_id, sql, params=()):  # noqa: ARG001
            captured.append((sql, params))
            up = sql.strip().upper()
            if up.startswith("SHOW COLUMNS"):
                if not table_exists:
                    raise RuntimeError("1146 Table 'T1_Ssub' doesn't exist")
                return list(_T1_COLS)
            if up.startswith("SELECT COUNT("):
                return [{"cnt": 2}]
            # list SQL
            return [
                {"Gdate": "20260701", "Hcode": "P001", "Hname": "가출판",
                 "Gcode": "C001", "Gname": "가서점", "Name1": "택배", "Name2": "",
                 "Gssum": 3000, "Total_Gssum": 3000, "Line_Count": 2},
                {"Gdate": "20260702", "Hcode": "P002", "Hname": "나출판",
                 "Gcode": "C002", "Gname": "나서점", "Name1": "화물", "Name2": "",
                 "Gssum": 5000, "Total_Gssum": 5000, "Line_Count": 1},
            ]

        with patch.object(svc, "execute_query", side_effect=fake_execute):
            return await fn(server_id=_SID, **kw)

    async def test_ledger_real_query(self) -> None:
        cap: list = []
        items, total, truncated, scaffold = await self._run(
            svc.list_shipping_ledger, cap,
            scope_hcode="", date_from="2026.07.01", date_to="2026.07.31",
        )
        self.assertFalse(scaffold)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["gssum"], 3000)
        # SQL from T1_Ssub, day-key, no Yesno filter
        list_sql = _pick_list_sql(cap)
        self.assertIn("T1_Ssub", list_sql)
        self.assertNotIn("Yesno", list_sql)
        self.assertIn("Hcode", list_sql)

    async def test_ledger_missing_table_scaffold(self) -> None:
        cap: list = []
        items, total, truncated, scaffold = await self._run(
            svc.list_shipping_ledger, cap, table_exists=False,
        )
        self.assertTrue(scaffold)
        self.assertEqual(items, [])
        self.assertEqual(total, 0)

    async def test_ledger_sort_whitelist_rejects_injection(self) -> None:
        cap: list = []
        await self._run(
            svc.list_shipping_ledger, cap,
            sort_by="gssum; DROP TABLE", sort_dir="desc",
        )
        list_sql = _pick_list_sql(cap)
        self.assertNotIn("DROP TABLE", list_sql)

    async def test_ledger_sort_gssum_desc(self) -> None:
        cap: list = []
        await self._run(svc.list_shipping_ledger, cap, sort_by="gssum", sort_dir="desc")
        list_sql = _pick_list_sql(cap)
        self.assertIn("ORDER BY", list_sql.upper())
        self.assertIn("Gssum", list_sql)
        self.assertIn("DESC", list_sql.upper())

    async def test_status_real_query_aggregates(self) -> None:
        cap: list = []
        rows, total, truncated, scaffold = await self._run(
            svc.list_shipping_status, cap,
            date_from="2026.07.01", date_to="2026.07.31",
        )
        self.assertFalse(scaffold)
        self.assertEqual(len(rows), 2)
        list_sql = _pick_list_sql(cap)
        self.assertIn("GROUP BY", list_sql.upper())
        self.assertNotIn("Yesno", list_sql)

    async def test_status_missing_table_scaffold(self) -> None:
        cap: list = []
        rows, total, truncated, scaffold = await self._run(
            svc.list_shipping_status, cap, table_exists=False,
        )
        self.assertTrue(scaffold)
        self.assertEqual(rows, [])


if __name__ == "__main__":
    main()
