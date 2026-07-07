"""재고관리·재고원장 메뉴 서버 정렬(sortBy/sortDir) 회귀 — DEC-068 (D) 확장.

대상 함수
---------
- ``inventory_service.get_inventory_ledger``   (Sobo44_inv/Sobo33_ledger)
- ``reports_service.get_book_sales``           (Sobo33_1_ledger 통합 도서수불장)
- ``customer_ledger_service.get_customer_ledger``            (Sobo32)
- ``customer_ledger_service.get_integrated_customer_ledger`` (Sobo32_1)
- ``customer_ledger_service.list_publisher_settings``        (Sobo48)

검증 포인트
-----------
1. 화이트리스트 밖 sort_by (SQL 주입 시도 포함) 는 무시되고 기본 정렬 유지.
2. 페이지네이션 축 정렬(gdate/hcode)은 SQL ORDER BY 방향에 전역 반영.
3. 그 외 key 는 누적 완료 후 "페이지 내" Python 정렬만 수행 — 페이지 구성
   SQL(dates/hcodes page) 은 축 기본 방향(ASC) 을 유지한다 (Sobo32 잔량 누적
   불변식: R4 totalsCache 는 오름차순 순차 페이지 전제).
4. book-sales 는 전체 정렬 후 페이징 + ``BOOK_SALES_MAX`` 상한 truncated 신호.

격리
-----
- 각 서비스 모듈의 ``execute_query`` / ``in_clause_lookup`` 만 patch. 실 DB 의존 0.
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


def _date_str(idx: int) -> str:
    day = (idx % 28) + 1
    month = ((idx // 28) % 12) + 1
    return f"2026.{month:02d}.{day:02d}"


# ---------------------------------------------------------------
# 1) inventory_service.get_inventory_ledger
# ---------------------------------------------------------------

class InventoryLedgerSortTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        total_dates: int = 5,
        sort_by: str | None = None,
        sort_dir: str | None = None,
    ) -> tuple[dict[str, Any], list[str]]:
        from app.services import inventory_service as inv

        captured_sql: list[str] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "COUNT(DISTINCT Gdate)" in sql:
                return [{"cnt": total_dates}]
            if sql.lstrip().startswith("SELECT DISTINCT Gdate"):
                lim_p, off_p = params[-2], params[-1]
                end = min(off_p + lim_p, total_dates)
                idxs = range(off_p, end)
                dates = [_date_str(i) for i in idxs]
                if "ORDER BY Gdate DESC" in sql:
                    dates = list(reversed(dates))
                return [{"Gdate": d} for d in dates]
            return []

        async def fake_in_lookup(
            server_id: str, *, sql_template: str, keys: Any, prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "G4_Book" in sql_template:
                return []
            # 일자 idx 에 비례하는 출고 수량 — goqut 정렬 검증용.
            out: list[dict[str, Any]] = []
            for i, d in enumerate(list(keys)):
                out.append({
                    "Gdate": d, "Bcode": f"B{i:04d}", "Scode": "X",
                    "Gubun": "출고", "Pubun": "", "Gsqut": (i % 3) + 1, "Gssum": 100,
                })
            return out

        with patch("app.services.inventory_service.execute_query", new=fake_exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=fake_in_lookup):
            result = await inv.get_inventory_ledger(
                server_id="srv", hcode=None, bcode=None, bcode_to=None,
                date_from="2026-01-01", date_to="2026-12-31",
                limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
            )
        return result, captured_sql

    async def test_default_is_gdate_asc(self) -> None:
        result, captured = await self._run()
        gdates = [r["gdate"] for r in result["rows"]]
        self.assertEqual(gdates, sorted(gdates))
        dates_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
        self.assertTrue(all("ORDER BY Gdate ASC" in s for s in dates_sqls))

    async def test_gdate_desc_applies_to_dates_page_sql(self) -> None:
        result, captured = await self._run(sort_by="gdate", sort_dir="desc")
        dates_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
        self.assertTrue(any("ORDER BY Gdate DESC" in s for s in dates_sqls))
        gdates = [r["gdate"] for r in result["rows"]]
        self.assertEqual(gdates, sorted(gdates, reverse=True))

    async def test_non_axis_key_sorts_within_page_only(self) -> None:
        result, captured = await self._run(sort_by="goqut", sort_dir="desc")
        # 페이지 구성 SQL 은 기본 ASC 유지 (전역 아님).
        dates_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
        self.assertTrue(all("ORDER BY Gdate ASC" in s for s in dates_sqls))
        vals = [r["goqut"] for r in result["rows"]]
        self.assertEqual(vals, sorted(vals, reverse=True))

    async def test_injection_key_falls_back_to_default(self) -> None:
        result, captured = await self._run(sort_by="Gdate; DROP TABLE S1_Ssub", sort_dir="desc")
        gdates = [r["gdate"] for r in result["rows"]]
        self.assertEqual(gdates, sorted(gdates))
        self.assertTrue(all("DROP TABLE" not in s for s in captured))


# ---------------------------------------------------------------
# 2) reports_service.get_book_sales
# ---------------------------------------------------------------

class BookSalesSortTests(IsolatedAsyncioTestCase):
    async def _run(
        self,
        *,
        n_books: int = 6,
        sort_by: str | None = None,
        sort_dir: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        from app.services import reports_service as rpt

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            if "Sg_Csum" in sql:
                return []
            # 도서 n_books 종 — goqut 이 gcode 역순으로 증가하도록 시드.
            return [
                {
                    "Bcode": f"B{i:04d}", "Scode": "X", "Gubun": "출고", "Pubun": "",
                    "Gsqut": n_books - i, "Gssum": (n_books - i) * 100,
                }
                for i in range(n_books)
            ]

        async def fake_in_lookup(
            server_id: str, *, sql_template: str, keys: Any, prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            return []

        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=fake_in_lookup):
            return await rpt.get_book_sales(
                server_id="srv", hcode=None,
                date_from="2026-01-01", date_to="2026-12-31",
                limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir,
            )

    async def test_default_gcode_asc(self) -> None:
        result = await self._run()
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))
        self.assertFalse(result["truncated"])

    async def test_sort_whole_set_before_slicing(self) -> None:
        # goqut desc 전체 정렬 후 페이징 — 첫 페이지 첫 행이 전역 최대값.
        result = await self._run(n_books=6, sort_by="goqut", sort_dir="desc", limit=2)
        vals = [r["goqut"] for r in result["rows"]]
        self.assertEqual(vals, [6, 5])
        # 두 번째 페이지도 전역 정렬 연속.
        result2 = await self._run(n_books=6, sort_by="goqut", sort_dir="desc", limit=2, offset=2)
        self.assertEqual([r["goqut"] for r in result2["rows"]], [4, 3])

    async def test_unknown_sort_key_ignored(self) -> None:
        result = await self._run(sort_by="__evil__", sort_dir="desc")
        codes = [r["gcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes))

    async def test_truncated_when_over_book_sales_max(self) -> None:
        from app.services import reports_service as rpt
        with patch.object(rpt, "BOOK_SALES_MAX", 4):
            result = await self._run(n_books=6)
        self.assertTrue(result["truncated"])
        self.assertEqual(result["total"], 4)
        self.assertEqual(len(result["rows"]), 4)


# ---------------------------------------------------------------
# 3) customer_ledger_service — Sobo32 / Sobo32_1 / Sobo48
# ---------------------------------------------------------------

class CustomerLedgerSortTests(IsolatedAsyncioTestCase):
    async def _run_single(
        self, *, sort_by: str | None = None, sort_dir: str | None = None
    ) -> tuple[dict[str, Any], list[str]]:
        from app.services import customer_ledger_service as cls_

        captured_sql: list[str] = []
        total_dates = 4

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "Sb_Csum" in sql:
                return [{"qty": 100}]
            if "COUNT(DISTINCT Gdate)" in sql:
                return [{"cnt": total_dates}]
            if sql.lstrip().startswith("SELECT DISTINCT Gdate"):
                return [{"Gdate": _date_str(i)} for i in range(total_dates)]
            if "GROUP BY Scode, Gubun, Pubun" in sql:
                return []  # grand summary
            return []

        async def fake_in_lookup(
            server_id: str, *, sql_template: str, keys: Any, prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "Sb_Csum" in sql_template or "G7_Ggeo" in sql_template:
                return []
            return [
                {
                    "Gdate": d, "Scode": "X", "Gubun": "출고", "Pubun": "",
                    "Gsqut": (i % 3) + 1, "Gssum": 100,
                }
                for i, d in enumerate(list(keys))
            ]

        with patch("app.services.customer_ledger_service.execute_query", new=fake_exec), \
             patch("app.services.customer_ledger_service.in_clause_lookup", new=fake_in_lookup):
            result = await cls_.get_customer_ledger(
                server_id="srv", customer_code="5019",
                date_from="2026-01-01", date_to="2026-12-31",
                limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
            )
        return result, captured_sql

    async def test_single_pagination_axis_stays_ascending(self) -> None:
        # 잔량 누적 불변식 — 어떤 정렬이든 dates-page SQL 은 ASC 고정.
        for sb, sd in ((None, None), ("gdate", "desc"), ("goqut", "desc")):
            _, captured = await self._run_single(sort_by=sb, sort_dir=sd)
            dates_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Gdate")]
            self.assertTrue(all("DESC" not in s for s in dates_sqls), f"sort_by={sb}")

    async def test_single_gdate_desc_reverses_page_rows(self) -> None:
        result, _ = await self._run_single(sort_by="gdate", sort_dir="desc")
        gdates = [r["gdate"] for r in result["rows"]]
        self.assertEqual(gdates, sorted(gdates, reverse=True))
        # 잔량은 행에 붙은 채 유지 — 오름차순 누적(100-1,‑2,‑3,‑1)의 역순으로 노출.
        self.assertEqual([r["balance_qty"] for r in result["rows"]], [93, 94, 97, 99])

    async def test_single_qty_sort_within_page(self) -> None:
        result, _ = await self._run_single(sort_by="goqut", sort_dir="desc")
        vals = [r["goqut"] for r in result["rows"]]
        self.assertEqual(vals, sorted(vals, reverse=True))

    async def _run_integrated(
        self, *, sort_by: str | None = None, sort_dir: str | None = None
    ) -> tuple[dict[str, Any], list[str]]:
        from app.services import customer_ledger_service as cls_

        captured_sql: list[str] = []
        hcodes = [f"H{i:03d}" for i in range(4)]

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "COUNT(DISTINCT Hcode)" in sql:
                return [{"cnt": len(hcodes)}]
            if sql.lstrip().startswith("SELECT DISTINCT Hcode"):
                ordered = list(reversed(hcodes)) if "ORDER BY Hcode DESC" in sql else hcodes
                return [{"Hcode": h} for h in ordered]
            return []

        async def fake_in_lookup(
            server_id: str, *, sql_template: str, keys: Any, prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "Sb_Csum" in sql_template or "G7_Ggeo" in sql_template or "G1_Ggeo" in sql_template:
                return []
            return [
                {
                    "Hcode": h, "Scode": "X", "Gubun": "출고", "Pubun": "",
                    "Gsqut": (i % 3) + 1, "Gssum": 100,
                }
                for i, h in enumerate(list(keys))
            ]

        with patch("app.services.customer_ledger_service.execute_query", new=fake_exec), \
             patch("app.services.customer_ledger_service.in_clause_lookup", new=fake_in_lookup), \
             patch("app.services.customer_ledger_service._fetch_publisher_names",
                   new=fake_in_lookup_names):
            result = await cls_.get_integrated_customer_ledger(
                server_id="srv", date_from="2026-01-01", date_to="2026-12-31",
                limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
            )
        return result, captured_sql

    async def test_integrated_hcode_desc_is_sql_level(self) -> None:
        result, captured = await self._run_integrated(sort_by="hcode", sort_dir="desc")
        page_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Hcode")]
        self.assertTrue(any("ORDER BY Hcode DESC" in s for s in page_sqls))
        codes = [r["hcode"] for r in result["rows"]]
        self.assertEqual(codes, sorted(codes, reverse=True))

    async def test_integrated_qty_sort_within_page(self) -> None:
        result, captured = await self._run_integrated(sort_by="period_out", sort_dir="desc")
        page_sqls = [s for s in captured if s.lstrip().startswith("SELECT DISTINCT Hcode")]
        self.assertTrue(all("DESC" not in s for s in page_sqls))
        vals = [r["period_out"] for r in result["rows"]]
        self.assertEqual(vals, sorted(vals, reverse=True))


async def fake_in_lookup_names(server_id: str, hcodes: list[str]) -> dict[str, str]:
    return {}


class PublisherSettingsSortTests(IsolatedAsyncioTestCase):
    async def _run(
        self, *, sort_by: str | None = None, sort_dir: str | None = None
    ) -> tuple[dict[str, Any], list[str]]:
        from app.services import customer_ledger_service as cls_

        captured_sql: list[str] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            if "COUNT(*)" in sql:
                return [{"cnt": 2}]
            return [
                {"gcode": "P001", "gname": "가나", "chek3": "Y", "yesno": "N"},
                {"gcode": "P002", "gname": "다라", "chek3": "N", "yesno": "N"},
            ]

        async def fake_meta(server_id: str):
            return ({"Gcode", "Gname", "Chek3", "Scode"},
                    {"gcode": "Gcode", "gname": "Gname", "chek3": "Chek3", "scode": "Scode"})

        with patch("app.services.customer_ledger_service.execute_query", new=fake_exec), \
             patch("app.services.customer_ledger_service.g7_column_meta", new=fake_meta), \
             patch("app.services.customer_ledger_service.select_chek3_yesno_sql",
                   new=lambda cols, exact: "Chek3 AS chek3, Scode AS yesno"):
            result = await cls_.list_publisher_settings(
                server_id="srv", keyword=None, scope_hcode=None,
                limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
            )
        return result, captured_sql

    async def test_gname_desc_sql_order_by(self) -> None:
        _, captured = await self._run(sort_by="gname", sort_dir="desc")
        list_sqls = [s for s in captured if "FROM G7_Ggeo" in s and "COUNT(*)" not in s]
        self.assertTrue(any("ORDER BY Gname DESC, Gcode" in s for s in list_sqls))

    async def test_injection_key_ignored(self) -> None:
        _, captured = await self._run(sort_by="Gname; DROP TABLE G7_Ggeo", sort_dir="desc")
        list_sqls = [s for s in captured if "FROM G7_Ggeo" in s and "COUNT(*)" not in s]
        self.assertTrue(any("ORDER BY Gcode LIMIT" in s for s in list_sqls))
        self.assertTrue(all("DROP TABLE" not in s for s in captured))


if __name__ == "__main__":  # pragma: no cover
    main()
