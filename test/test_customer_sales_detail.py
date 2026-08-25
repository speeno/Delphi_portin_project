"""거래처별 판매 도서별 상세(get_customer_sales_detail) — 레거시 Sobo62 DBGrid201 동등.

선택 거래처(gcode+gjisa) 고정 + GROUP BY Bcode 집계가 get_customer_sales 와 동일한
출고/반품/증정 분기 규칙으로 누적되고, 합계(totals)·도서명 lookup 이 실리는지 검증.
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


def _agg(bcode: str, gubun: str, pubun: str, qty: int, amt: int) -> dict[str, Any]:
    return {"Bcode": bcode, "Gubun": gubun, "Pubun": pubun, "Gsqut": qty, "Gssum": amt}


class CustomerSalesDetailTests(unittest.IsolatedAsyncioTestCase):
    async def test_accumulation_branches_and_totals(self) -> None:
        from app.services import reports_service as rsvc

        rows = [
            _agg("B001", "출고", "위탁", 10, 100_000),   # 출고 → goqut/gosum + 판매
            _agg("B001", "반품", "위탁", 2, 20_000),      # 반품 → gbqut/gbsum + 판매
            _agg("B001", "출고", "증정", 1, 0),           # 증정 → gjqut (판매수량 제외)
            _agg("B002", "출고", "위탁", 5, 50_000),
        ]
        with patch.object(rsvc, "execute_query", new=AsyncMock(return_value=rows)), patch.object(
            rsvc,
            "in_clause_lookup",
            new=AsyncMock(
                return_value=[
                    {"bcode": "B001", "gname": "도서A"},
                    {"bcode": "B002", "gname": "도서B"},
                ]
            ),
        ) as lookup_mock:
            res = await rsvc.get_customer_sales_detail(
                server_id="srv",
                hcode="H001",
                date_from="2026-07-01",
                date_to="2026-07-21",
                gcode="00004",
                gjisa="온라인",
            )

        by = {r["bcode"]: r for r in res["rows"]}
        self.assertEqual(len(by), 2)
        # B001 — 출고 10/100000 + 반품 2/20000 + 증정 1
        self.assertEqual(by["B001"]["bname"], "도서A")
        self.assertEqual(by["B001"]["goqut"], 10)
        self.assertEqual(by["B001"]["gosum"], 100_000)
        self.assertEqual(by["B001"]["gbqut"], 2)
        self.assertEqual(by["B001"]["gbsum"], 20_000)
        self.assertEqual(by["B001"]["gjqut"], 1)
        # 판매수량(gsusu)=출고+반품(증정 제외), 판매금액(gssum)=출고+반품+증정금액
        self.assertEqual(by["B001"]["gsusu"], 12)
        self.assertEqual(by["B001"]["gssum"], 120_000)
        # totals = 행 합
        self.assertEqual(res["totals"]["goqut"], 15)
        self.assertEqual(res["totals"]["gssum"], 170_000)
        self.assertFalse(res["truncated"])
        # 도서명 lookup 은 hcode 스코프 G4_Book 템플릿 사용
        tmpl = lookup_mock.await_args.kwargs["sql_template"]
        self.assertIn("G4_Book", tmpl)
        self.assertIn("Hcode='H001'", tmpl)

    async def test_where_includes_gcode_and_gjisa_scope_when_by_branch(self) -> None:
        """지점별검색(by_branch)일 때만 WHERE 에 지점(Gjisa) 스코프가 실린다."""
        from app.services import reports_service as rsvc

        exec_mock = AsyncMock(return_value=[])
        with patch.object(rsvc, "execute_query", new=exec_mock):
            await rsvc.get_customer_sales_detail(
                server_id="srv",
                hcode=None,
                date_from="2026-07-01",
                date_to="2026-07-21",
                gcode="00004",
                gjisa="종각 종로점",
                by_branch=True,
            )
        sql, params = exec_mock.await_args.args[1], exec_mock.await_args.args[2]
        self.assertIn("Gcode = %s", sql)
        self.assertIn("COALESCE(Gjisa,'') = %s", sql)
        self.assertIn("GROUP BY Bcode, Gubun, Pubun", sql)
        self.assertIn("00004", params)
        self.assertIn("종각 종로점", params)

    async def test_default_detail_is_whole_customer(self) -> None:
        """기본(지점별검색 해제) = 거래처 전체 — 레거시 Button201Click 은 Gjisa 절이 없다.

        2026-08-25 사용자 리포트("일부 거래처 자료 미반영")의 상세 쪽 — 상단이 거래처
        단위로 합산되면 하단도 같은 범위여야 한다(DEC-196).
        """
        from app.services import reports_service as rsvc

        exec_mock = AsyncMock(return_value=[])
        with patch.object(rsvc, "execute_query", new=exec_mock):
            await rsvc.get_customer_sales_detail(
                server_id="srv", hcode=None,
                date_from="2026-07-01", date_to="2026-07-21",
                gcode="00004", gjisa="종각 종로점",
            )
        sql, params = exec_mock.await_args.args[1], exec_mock.await_args.args[2]
        self.assertIn("Gcode = %s", sql)
        self.assertNotIn("Gjisa", sql)
        self.assertNotIn("종각 종로점", params)


if __name__ == "__main__":
    unittest.main()
