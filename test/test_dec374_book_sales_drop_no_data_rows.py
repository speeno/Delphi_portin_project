"""DEC-374 — 도서별판매 · 도서별년말집계: 자료가 없는 도서(기본 표시 측정치 전부 0)는 목록에서 뺀다.

요청(교문사, 2026-10-05 캡처)
----------------------------
"[통계관리] 1. 도서별판매 — 날짜 2026년 4월 23일 — 출고가 없던 도서들이 반영되어 공란으로 되어있습니다.
출고, 입고, 반품, 증정, 폐기, 변경, 금액 등 데이터가 없는 자료는 다 삭제해주세요."

원인
----
DEC-137 의 «전 측정치 0 제외»가 **기본 숨김 컬럼인 폐기액(gpsum = Sg_Csum 재고변경 합)** 과 화면에 없는
입고금액(gisum)까지 «자료 있음»으로 쳤다. 그날 재고변경(Sg_Csum)만 있던 도서가 전 칸 0 으로 남고,
도서명 조회가 S1_Ssub 에 나온 코드만 대상으로 해 도서명도 공란이었다.

가드
----
- 판정 키 = 기본 표시 측정치(입고 · 출고 · 증정 · 반품 · 폐기 수량, 출고 · 반품 금액).
- 자료가 있는 도서의 폐기액 · 합계 계산은 종전 그대로.
- 도서별년말집계도 같은 판정(분기표 밖 전표 · Sg_Csum 만 있는 도서 제외).
"""

from __future__ import annotations

from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import reports_service as rs


class KeepKeys(TestCase):
    def test_keep_keys_are_default_visible_measures(self) -> None:
        self.assertEqual(
            set(rs._BOOK_SALES_ROW_KEEP_KEYS),  # noqa: SLF001
            {"giqut", "goqut", "gjqut", "gbqut", "gpqut", "gosum", "gbsum"},
        )
        self.assertNotIn("gpsum", rs._BOOK_SALES_ROW_KEEP_KEYS)  # noqa: SLF001
        self.assertIn("gpsum", rs._BOOK_SALES_MEASURE_KEYS)  # noqa: SLF001 — 합계 · 표시용은 유지


class BookSalesDropsNoDataRows(IsolatedAsyncioTestCase):
    S1 = [
        {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "Gdate": "2026.04.23", "Gsqut": 4, "Gssum": 98600},
        # 분기표 밖 전표만 있는 도서 — 전 칸 0
        {"Bcode": "B2", "Scode": "X", "Gubun": "변경", "Pubun": "", "Gdate": "2026.04.23", "Gsqut": 3, "Gssum": 0},
    ]
    CSUM = [
        {"Gcode": "B1", "Gdate": "2026.04.23", "Gbsum": 7},
        # 재고변경(Sg_Csum)만 있는 도서 — 종전엔 폐기액(기본 숨김)만 0 이 아니어서 빈 행으로 남았다
        {"Gcode": "80037", "Gdate": "2026.04.23", "Gbsum": 5},
    ]

    async def _run(self) -> dict[str, Any]:
        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "FROM S1_Ssub" in sql:
                return list(self.S1)
            if "FROM Sg_Csum" in sql:
                return list(self.CSUM)
            return []

        with patch.object(rs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(rs, "in_clause_lookup", AsyncMock(return_value=[{"bcode": "B1", "gname": "가정과수업 디자인", "gdang": 29000}])), \
             patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)):
            return await rs.get_book_sales(
                server_id="remote_153", hcode="5019",
                date_from="2026-04-23", date_to="2026-04-23", limit=2000,
            )

    async def test_only_books_with_visible_data_remain(self) -> None:
        res = await self._run()
        codes = [r["gcode"] for r in res["rows"]]
        self.assertEqual(codes, ["B1"])
        row = res["rows"][0]
        self.assertEqual((row["goqut"], row["gosum"], row["gpsum"]), (4, 98600, 7))
        # 합계도 남은 도서 기준 — 빠진 도서의 폐기액(5)은 들어가지 않는다.
        self.assertEqual(res["totals"]["gpsum"], 7)
        self.assertEqual(res["page"]["total"], 1)


class YearEndDropsNoDataRows(IsolatedAsyncioTestCase):
    DETAIL = [
        {"bcode": "B1", "gdate": "2026.04.23", "scode": "X", "gubun": "출고", "pubun": "위탁", "gsqut": 4, "gssum": 98600},
        {"bcode": "B2", "gdate": "2026.04.23", "scode": "X", "gubun": "변경", "pubun": "", "gsqut": 3, "gssum": 0},
    ]

    async def test_zero_rows_removed(self) -> None:
        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "S1_Ssub" in sql:
                return list(self.DETAIL)
            if "Sg_Csum" in sql:
                return [{"gcode": "80037", "gdate": "2026.04.23", "gbsum": 5}]
            return []

        with patch.object(rs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(rs, "in_clause_lookup", AsyncMock(return_value=[])), \
             patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)):
            res = await rs.get_year_end_book_aggregate(
                server_id="remote_153", hcode="5019", date_from="2026-04", date_to="2026-04", limit=2000,
            )
        self.assertEqual([r["gcode"] for r in res["rows"]], ["B1"])
        self.assertEqual(res["totals"]["goqut"], 4)


if __name__ == "__main__":
    main()
