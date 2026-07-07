"""통계관리 리포트 서버 정렬(sortBy/sortDir) + 상한 회귀 — DEC-082 확장.

대상 함수
---------
- ``reports_service.get_customer_sales``          (Sobo62 거래처판매)
- ``reports_service.get_year_end_book_aggregate`` (Sobo67_yearbook 도서별년말집계)

검증 포인트
-----------
1. 화이트리스트 정렬 — 전체 정렬 후 페이징(페이지 간 순서 연속), 동률 시 기본 키 보조 정렬.
2. 화이트리스트 밖 sort_by (주입 시도 포함) 는 방향까지 무시.
3. ``BOOK_SALES_MAX`` 상한 도달 시 truncated=True + 행 상한 절단.

격리
-----
- ``reports_service.execute_query`` / ``in_clause_lookup`` 만 patch. 실 DB 의존 0.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


async def _no_lookup(
    server_id: str, *, sql_template: str, keys: Any, prefix_params: tuple = (),
    chunk_size: int | None = None,
) -> list[dict[str, Any]]:
    return []


class CustomerSalesSortTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        n_customers: int = 6,
        sort_by: str | None = None,
        sort_dir: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        from app.services import reports_service as rpt

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            # 거래처 n 곳 — 출고수량(goqut)이 gcode 역순으로 증가하도록 시드.
            return [
                {
                    "Hcode": "5019", "Gcode": f"C{i:04d}", "Scode": "X",
                    "Gubun": "출고", "Pubun": "", "Gjisa": "",
                    "Gsqut": n_customers - i, "Gssum": (n_customers - i) * 100,
                }
                for i in range(n_customers)
            ]

        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=_no_lookup):
            return await rpt.get_customer_sales(
                server_id="srv", hcode="5019",
                date_from="2026-01-01", date_to="2026-12-31",
                limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir,
            )

    async def test_default_order_by_hcode_gcode(self) -> None:
        result = await self._run()
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))
        self.assertFalse(result["truncated"])

    async def test_sort_whole_set_before_slicing(self) -> None:
        r1 = await self._run(sort_by="goqut", sort_dir="desc", limit=2)
        self.assertEqual([r["goqut"] for r in r1["rows"]], [6, 5])
        r2 = await self._run(sort_by="goqut", sort_dir="desc", limit=2, offset=2)
        self.assertEqual([r["goqut"] for r in r2["rows"]], [4, 3])

    async def test_injection_key_ignored(self) -> None:
        result = await self._run(sort_by="Gcode; DROP TABLE S1_Ssub", sort_dir="desc")
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))

    async def test_truncated_over_cap(self) -> None:
        from app.services import reports_service as rpt
        with patch.object(rpt, "BOOK_SALES_MAX", 4):
            result = await self._run(n_customers=6)
        self.assertTrue(result["truncated"])
        self.assertEqual(result["total"], 4)


class YearEndBookSortTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        n_books: int = 5,
        sort_by: str | None = None,
        sort_dir: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        from app.services import reports_service as rpt

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            if "Sg_Csum" in sql:
                return []
            # 도서 n 종 × 연도 1 — 출고수량이 bcode 역순으로 증가.
            return [
                {
                    "bcode": f"B{i:04d}", "gdate": "2026.03.02", "scode": "X",
                    "gubun": "출고", "pubun": "",
                    "gsqut": n_books - i, "gssum": (n_books - i) * 100,
                }
                for i in range(n_books)
            ]

        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=_no_lookup):
            return await rpt.get_year_end_book_aggregate(
                server_id="srv", hcode="5019",
                date_from="2026-01-01", date_to="2026-12-31",
                limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir,
            )

    async def test_default_order_by_gcode_gdate(self) -> None:
        result = await self._run()
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))
        self.assertFalse(result["truncated"])
        self.assertEqual(result["grain"], "year")

    async def test_sort_goqut_desc_global(self) -> None:
        r1 = await self._run(sort_by="goqut", sort_dir="desc", limit=2)
        self.assertEqual([r["goqut"] for r in r1["rows"]], [5, 4])
        r2 = await self._run(sort_by="goqut", sort_dir="desc", limit=2, offset=2)
        self.assertEqual([r["goqut"] for r in r2["rows"]], [3, 2])

    async def test_injection_key_ignored(self) -> None:
        result = await self._run(sort_by="__evil__; DELETE", sort_dir="desc")
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))

    async def test_truncated_over_cap(self) -> None:
        from app.services import reports_service as rpt
        with patch.object(rpt, "BOOK_SALES_MAX", 3):
            result = await self._run(n_books=5)
        self.assertTrue(result["truncated"])
        self.assertEqual(result["total"], 3)


class StatsServiceFilterSortTests(IsolatedAsyncioTestCase):
    """stats_service 위임 확장 (DEC-082) — 필터 전달 + 정렬 화이트리스트."""

    async def test_customer_analysis_forwards_gcode_range_and_sort(self) -> None:
        from app.services import stats_service

        captured: dict[str, Any] = {}

        async def fake_customer_sales(**kwargs):
            captured.update(kwargs)
            return {"rows": [], "total": 0, "page": {"limit": 100, "offset": 0, "total": 0, "has_more": False}}

        old = stats_service.reports_service.get_customer_sales
        stats_service.reports_service.get_customer_sales = fake_customer_sales
        try:
            await stats_service.get_customer_analysis(
                server_id="srv", date_from="2026-01-01", date_to="2026-01-31",
                hcode=None, gcode_from="C000", gcode_to="C999",
                sort_by="goqut", sort_dir="desc",
            )
        finally:
            stats_service.reports_service.get_customer_sales = old

        self.assertEqual(captured["gcode_from"], "C000")
        self.assertEqual(captured["gcode_to"], "C999")
        self.assertEqual(captured["sort_by"], "goqut")
        self.assertEqual(captured["sort_dir"], "desc")

    async def test_sales_period_sorts_buckets_and_forwards_bcode(self) -> None:
        from app.services import stats_service

        captured_bcodes: list[tuple[Any, Any]] = []

        async def fake_book_sales(**kwargs):
            captured_bcodes.append((kwargs.get("bcode_from"), kwargs.get("bcode_to")))
            # 날짜 구간 시작일에 비례하는 출고 수량.
            day = int(kwargs["date_from"].split(".")[-1])
            return {"rows": [{"goqut": day, "gosum": day * 10}], "total": 1}

        old = stats_service.reports_service.get_book_sales
        stats_service.reports_service.get_book_sales = fake_book_sales
        try:
            res = await stats_service.get_sales_period(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-03", group_by="daily",
                bcode_from="B0", bcode_to="B9",
                sort_by="qut_total", sort_dir="desc",
            )
        finally:
            stats_service.reports_service.get_book_sales = old

        self.assertTrue(all(b == ("B0", "B9") for b in captured_bcodes))
        vals = [i["qut_total"] for i in res["items"]]
        self.assertEqual(vals, sorted(vals, reverse=True))

    async def test_book_turnover_sort_and_injection_guard(self) -> None:
        from app.services import stats_service

        async def fake_book_sales(**kwargs):
            return {
                "rows": [
                    {"gcode": "B1", "gname": "가", "giqut": 10, "goqut": 5},
                    {"gcode": "B2", "gname": "나", "giqut": 10, "goqut": 9},
                ],
                "total": 2,
            }

        old = stats_service.reports_service.get_book_sales
        stats_service.reports_service.get_book_sales = fake_book_sales
        try:
            res_sorted = await stats_service.get_book_turnover(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31",
                sort_by="gcode", sort_dir="asc",
            )
            res_evil = await stats_service.get_book_turnover(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-01-31",
                sort_by="gcode; DROP", sort_dir="desc",
            )
        finally:
            stats_service.reports_service.get_book_sales = old

        self.assertEqual([i["gcode"] for i in res_sorted["items"]], ["B1", "B2"])
        # 화이트리스트 밖 → 기본(회전율 내림차순) 유지.
        ratios = [i["turnover_ratio"] for i in res_evil["items"]]
        self.assertEqual(ratios, sorted(ratios, reverse=True))


if __name__ == "__main__":  # pragma: no cover
    main()
