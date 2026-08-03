"""영업팀 1차 반영(A 배치, 2026-08-03) 회귀 가드 — DEC-132.

A3 라벨 정정 — 레거시 Subu61.dfm 정본: GJQUT=증정수량(구 웹 "재고수/잔량" 오라벨),
GPQUT=폐기수량(구 "파지수"). 화면·XLSX 헤더 동시 정정.
A1 검색 팝업 행 단일 클릭 즉시 확정(onRowClick).
A2/A4 단일 코드 필터 — bcode/gcode 지정 시 range 보다 우선, 미지정=전체.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))

from app.services import reports_service as rs  # noqa: E402


class SingleCodeFilterTests(IsolatedAsyncioTestCase):
    """A2/A4 — 단일 bcode/gcode 필터 SQL."""

    async def _capture_book(self, **kw) -> list[tuple[str, tuple[Any, ...]]]:
        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id, sql, params):  # noqa: ARG001
            captured.append((sql, tuple(params)))
            return []

        with patch.object(rs, "execute_query", new=fake_exec), patch.object(
            rs, "in_clause_lookup", new=AsyncMock(return_value=[])
        ):
            await rs.get_book_sales(
                server_id="srv", hcode="H1",
                date_from="2026-07-01", date_to="2026-07-31", **kw,
            )
        return captured

    async def test_book_single_bcode_equals(self) -> None:
        captured = await self._capture_book(bcode="2340")
        s1 = next(s for s, _ in captured if "S1_Ssub" in s)
        self.assertIn("Bcode = %s", s1)
        self.assertNotIn("BETWEEN", s1)
        waste = next(s for s, _ in captured if "Sg_Csum" in s)
        self.assertIn("Gcode = %s", waste)

    async def test_book_bcode_overrides_range(self) -> None:
        captured = await self._capture_book(
            bcode="2340", bcode_from="0001", bcode_to="9999",
        )
        s1, p1 = next((s, p) for s, p in captured if "S1_Ssub" in s)
        self.assertIn("Bcode = %s", s1)
        self.assertNotIn("BETWEEN", s1)
        self.assertIn("2340", p1)

    async def test_book_range_still_works_without_bcode(self) -> None:
        captured = await self._capture_book(bcode_from="0001", bcode_to="9999")
        s1 = next(s for s, _ in captured if "S1_Ssub" in s)
        self.assertIn("Bcode BETWEEN %s AND %s", s1)

    async def test_customer_single_gcode_equals(self) -> None:
        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id, sql, params):  # noqa: ARG001
            captured.append((sql, tuple(params)))
            return []

        with patch.object(rs, "execute_query", new=fake_exec), patch.object(
            rs, "in_clause_lookup", new=AsyncMock(return_value=[])
        ):
            await rs.get_customer_sales(
                server_id="srv", hcode="H1",
                date_from="2026-07-01", date_to="2026-07-31",
                gcode="00023", gcode_from="0", gcode_to="Z",
            )
        s1 = next(s for s, _ in captured if "S1_Ssub" in s)
        self.assertIn("Gcode = %s", s1)
        self.assertNotIn("Gcode BETWEEN", s1)


class LabelCorrectionTests(TestCase):
    """A3 — 레거시 Subu61 정본 라벨 (GJQUT=증정수량, GPQUT=폐기수량)."""

    def test_xlsx_export_labels(self) -> None:
        from app.routers.reports import _BOOK_SALES_EXPORT_COLUMNS

        cols = dict((k, label) for label, k in _BOOK_SALES_EXPORT_COLUMNS)
        self.assertEqual(cols["gjqut"], "증정수")
        self.assertEqual(cols["gpqut"], "폐기수")
        self.assertEqual(cols["gpsum"], "폐기액")
        labels = [label for label, _ in _BOOK_SALES_EXPORT_COLUMNS]
        self.assertNotIn("재고수", labels)
        self.assertNotIn("파지수", labels)
        self.assertNotIn("파지액", labels)

    def test_book_sales_page_labels(self) -> None:
        src = (FRONTEND / "src/app/(app)/reports/book-sales/page.tsx").read_text("utf-8")
        for needle in ('label: "증정수"', 'label: "폐기수"', 'label: "폐기액"'):
            self.assertIn(needle, src)
        self.assertNotIn('label: "재고수"', src)
        self.assertNotIn('label: "파지수"', src)

    def test_stats_book_page_labels(self) -> None:
        src = (FRONTEND / "src/app/(app)/stats/book/page.tsx").read_text("utf-8")
        self.assertIn('label: "증정"', src)
        self.assertNotIn('label: "잔량"', src)


class LookupDialogClickSelectTests(TestCase):
    """A1 — 검색 팝업 행 단일 클릭 즉시 확정."""

    def test_dialog_wires_on_row_click(self) -> None:
        src = (FRONTEND / "src/components/master/master-lookup-dialog.tsx").read_text("utf-8")
        self.assertIn("onRowClick={chooseRow}", src)


class SingleFilterUiTests(TestCase):
    """A2/A4 — 코드 시작/끝 → 단일 검색 + 전체 체크박스 (Enter 스톱 포함, DEC-116)."""

    def test_book_sales_filter_ui(self) -> None:
        src = (FRONTEND / "src/app/(app)/reports/book-sales/page.tsx").read_text("utf-8")
        self.assertIn("Sobo61.Chk_AllBooks", src)
        # 실사용 제거 확인(설명 주석의 과거형 언급은 허용).
        self.assertNotIn("<Label>도서코드 시작</Label>", src)
        self.assertNotIn("setBcodeFrom", src)
        self.assertNotIn("bcodeFrom:", src)

    def test_customer_sales_filter_ui(self) -> None:
        src = (FRONTEND / "src/app/(app)/reports/customer-sales/page.tsx").read_text("utf-8")
        self.assertIn("Sobo62.Chk_AllCustomers", src)
        self.assertNotIn("<Label>거래처코드 시작</Label>", src)
        self.assertNotIn("setGcodeFrom", src)
        self.assertNotIn("gcodeFrom:", src)


if __name__ == "__main__":
    main()
