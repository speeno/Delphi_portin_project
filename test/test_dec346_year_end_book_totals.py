"""DEC-346 — 도서별년말집계 하단 합계 (2026-09-30, 교문사 경리부 「하단 합계 표기 요청」).

합계는 쪽·정렬·상한과 무관하게 **검색 결과 전체** 기준(도서별판매 DEC-146 · 거래처별판매 DEC-197 과 같은 규칙).
화면 하단 합계 줄과 엑셀 마지막 「합계」 행이 같은 값을 쓴다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import reports_service as rs

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _row(bcode: str, *, gubun: str = "출고", pubun: str = "", scode: str = "X",
         gsqut: int = 1, gssum: int = 100, gdate: str = "2026.09.15") -> dict[str, Any]:
    return {"bcode": bcode, "gdate": gdate, "scode": scode, "gubun": gubun, "pubun": pubun,
            "gsqut": gsqut, "gssum": gssum}


class TotalsCoverWholeResult(IsolatedAsyncioTestCase):
    DETAIL = [
        _row("B1", gsqut=10, gssum=1000),
        _row("B2", gsqut=5, gssum=500),
        _row("B3", gsqut=7, gssum=700),
        _row("B3", pubun="증정", gsqut=2, gssum=0),
        _row("B4", scode="Y", gubun="입고", gsqut=50, gssum=5000),
    ]

    async def _run(self, **kw: Any) -> dict[str, Any]:
        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            return list(self.DETAIL) if "S1_Ssub" in sql else []

        with patch.object(rs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(rs, "in_clause_lookup", AsyncMock(return_value=[])), \
             patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)):
            return await rs.get_year_end_book_aggregate(
                server_id="remote_153", hcode="5019",
                date_from="2026-09", date_to="2026-09", **kw,
            )

    async def test_totals_equal_sum_of_all_rows(self) -> None:
        res = await self._run(limit=2000)
        rows, totals = res["rows"], res["totals"]
        self.assertEqual(len(rows), 4)
        for key in ("giqut", "goqut", "gjqut", "gbqut", "gpqut", "gosum", "gbsum", "gpsum",
                    "sale_qty", "sale_amt"):
            self.assertEqual(totals[key], sum(int(r.get(key) or 0) for r in rows), key)
        self.assertEqual(totals["goqut"], 22)
        self.assertEqual(totals["gjqut"], 2)
        self.assertEqual(totals["giqut"], 50)

    async def test_totals_do_not_depend_on_page(self) -> None:
        whole = (await self._run(limit=2000))["totals"]
        first = await self._run(limit=2, offset=0)
        last = await self._run(limit=2, offset=2)
        self.assertEqual(len(first["rows"]), 2)
        self.assertEqual(first["totals"], whole)
        self.assertEqual(last["totals"], whole)

    async def test_totals_do_not_depend_on_sort(self) -> None:
        a = (await self._run(sort_by="goqut", sort_dir="desc"))["totals"]
        b = (await self._run(sort_by="gname", sort_dir="asc"))["totals"]
        self.assertEqual(a, b)

    async def test_totals_survive_row_cap(self) -> None:
        with patch.object(rs, "BOOK_SALES_MAX", 2):
            res = await self._run(limit=2000)
        self.assertTrue(res["truncated"])
        self.assertEqual(len(res["rows"]), 2)
        self.assertEqual(res["totals"]["goqut"], 22, "합계는 상한으로 잘리기 전 전체")


class Wiring(TestCase):
    def test_response_model_and_router_carry_totals(self) -> None:
        model = (BACK / "models" / "inquiry.py").read_text(encoding="utf-8")
        self.assertIn("class YearEndBookTotals(BaseModel):", model)
        self.assertIn("totals: YearEndBookTotals | None = None", model)
        router = (BACK / "routers" / "reports.py").read_text(encoding="utf-8")
        block = router.split('@router.get("/year-end-book", response_model=YearEndBookResponse)')[1]
        block = block.split("@router.get(")[0]
        self.assertIn("totals=YearEndBookTotals.model_validate(totals) if totals else None", block)

    def test_screen_shows_totals_row(self) -> None:
        src = (FRONT / "app/(app)/reports/year-end-book/page.tsx").read_text(encoding="utf-8")
        self.assertIn("setTotals(res.totals ?? null);", src)
        grid = src.split("<DataGrid<YearEndBookGridRow>")[1].split("/>")[0]
        self.assertIn("totals={gridTotals}", grid)
        self.assertIn('totalsLabel="합계"', grid)
        totals_block = src.split("const gridTotals = useMemo")[1].split("}, [totals")[0]
        for key in ("giqut", "goqut", "gjqut", "gbqut", "sale_qty", "gosum", "gbsum", "sale_amt"):
            self.assertIn(f"{key}: totals.{key}", totals_block, key)
        self.assertNotIn("gdang", totals_block, "정가는 합산하지 않는다")

    def test_excel_ends_with_totals_row(self) -> None:
        from app.routers import reports

        cols = [("년도", "gdate"), ("도서명", "gname"), ("출고수량", "goqut"),
                ("판매수량", reports._YEAR_END_DERIVED_FIELDS["sale_qty"])]
        row = reports._totals_export_row(cols, {"goqut": 22, "gbqut": -2})
        self.assertEqual(row["gdate"], "합계")
        self.assertEqual(row["goqut"], 22)
        self.assertNotIn("gname", row)
        self.assertEqual(cols[3][1](row), 20, "파생 컬럼(판매 = 출고 + 반품)도 합계 행에서 계산된다")
        router = (BACK / "routers" / "reports.py").read_text(encoding="utf-8")
        export = router.split('@router.get("/year-end-book/export.xlsx")')[1].split("@router.get(")[0]
        self.assertIn("rows = [*rows, _totals_export_row(cols, totals_box)]", export)


if __name__ == "__main__":
    main()
