"""DEC-347 — 도서별판매(일별)·거래처판매(일별): 기간은 선택한 그대로 (2026-09-30, 교문사 경리부).

「최대 검색일이 31일이라고 표기 — 날짜 기간은 선택 지정일로 조정 가능할까요?」
- 일별 기간 상한 31일 → 366일(1년). 31일 이하 조회는 종전과 완전히 같다.
- 표가 감당 못 할 크기는 «행 × 일» 셀 수로 막는다 — 도서·거래처 범위를 좁히면 긴 기간도 조회된다.
- 해를 넘기는 기간은 열 머리에 연도를 붙인다(같은 월일이 두 번 나올 수 있다).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import sales_matrix_service as sms

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class DailyRange(IsolatedAsyncioTestCase):
    async def _run(self, rows: list[dict[str, Any]], *, axis: str = "book", **kw: Any) -> dict[str, Any]:
        seen: dict[str, Any] = {}

        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            seen["sql"], seen["params"] = sql, tuple(params)
            return rows

        meta = "_book_meta" if axis == "book" else "_customer_meta"
        with patch.object(sms, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(sms, meta, AsyncMock(return_value={})):
            res = await sms.get_sales_matrix(
                server_id="remote_153", hcode="5019", axis=axis, period="daily",
                measure="out_qty", layout="items", **kw,
            )
        res["_seen"] = seen
        return res

    async def test_three_months_are_accepted(self) -> None:
        rows = [
            {"K": "B1", "B": "2026.07.01", "V": 3},
            {"K": "B1", "B": "2026.09.29", "V": 4},
            {"K": "B2", "B": "2026.08.15", "V": 5},
        ]
        res = await self._run(rows, date_from="2026-07-01", date_to="2026-09-29")
        self.assertEqual(len(res["columns"]), 91)
        self.assertEqual(res["columns"][0]["label"], "07.01")
        self.assertEqual(res["columns"][-1]["bucket"], "2026.09.29")
        self.assertEqual(res["_seen"]["params"][:2], ("2026.07.01", "2026.09.29"))
        by_code = {r["code"]: r for r in res["rows"]}
        self.assertEqual(by_code["B1"]["total"], 7)
        self.assertEqual(res["totals"]["total"], 12)
        self.assertIn("S.Hcode = %s", res["_seen"]["sql"], "계정 스코프 유지")

    async def test_customer_axis_too(self) -> None:
        rows = [{"K": "3313", "B": "2026.08.01", "V": 2}]
        res = await self._run(rows, axis="customer", date_from="2026-07-01", date_to="2026-09-29")
        self.assertEqual(len(res["columns"]), 91)
        self.assertEqual(res["rows"][0]["total"], 2)

    async def test_within_31_days_is_unchanged(self) -> None:
        rows = [{"K": "B1", "B": "2026.09.10", "V": 1}]
        res = await self._run(rows, date_from="2026-09-01", date_to="2026-09-30")
        self.assertEqual([c["label"] for c in res["columns"]][:2], ["09.01", "09.02"])
        self.assertEqual(len(res["columns"]), 30)

    async def test_labels_carry_year_when_range_crosses_years(self) -> None:
        rows = [{"K": "B1", "B": "2026.01.02", "V": 1}]
        res = await self._run(rows, date_from="2025-12-30", date_to="2026-01-02")
        self.assertEqual([c["label"] for c in res["columns"]], ["25.12.30", "25.12.31", "26.01.01", "26.01.02"])

    async def test_oversized_result_asks_to_narrow(self) -> None:
        rows = [{"K": f"B{i}", "B": "2026.07.01", "V": 1} for i in range(200)]
        with patch.object(sms, "DAILY_MAX_CELLS", 10_000):
            with self.assertRaises(sms.SalesMatrixValidationError) as cm:
                await self._run(rows, date_from="2026-07-01", date_to="2026-09-29")  # 200 × 91 = 18,200
        self.assertIn("기간을 줄이거나", str(cm.exception))
        self.assertIn("200행 × 91일", str(cm.exception))

    async def test_size_guard_never_hits_legacy_range(self) -> None:
        rows = [{"K": f"B{i}", "B": "2026.09.01", "V": 1} for i in range(2000)]
        with patch.object(sms, "DAILY_MAX_CELLS", 10_000):
            res = await self._run(rows, date_from="2026-09-01", date_to="2026-09-30")  # 2000 × 30 — 종전 허용
        self.assertEqual(res["row_count"], 2000)


class Limits(TestCase):
    def test_defaults(self) -> None:
        self.assertEqual(sms.DAILY_LEGACY_MAX, 31)
        self.assertGreaterEqual(sms.DAILY_MAX, 366)
        self.assertEqual(sms.MONTHLY_MAX, 24, "월별 상한은 그대로")

    def test_screen_text_no_longer_says_31_days(self) -> None:
        for rel in (
            "app/(app)/year-month-stats/book-sales-daily/page.tsx",
            "app/(app)/year-month-stats/customer-sales-daily/page.tsx",
            "app/(app)/year-month-stats/page.tsx",
        ):
            src = (FRONT / rel).read_text(encoding="utf-8")
            self.assertNotIn("최대 31일", src, rel)


if __name__ == "__main__":
    main()
