"""상세 조회 — 7세그먼트 키 + idnum=1 시 라인 surface 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _line_row(bcode: str) -> dict:
    return {
        "Gcode": "00405",
        "Bcode": bcode,
        "Gubun": "출고",
        "Pubun": "위탁",
        "Gsqut": 1,
        "Gssum": 1000,
        "Gbigo": "",
        "Yesno": "1",
        "Gdang": 1000,
        "Grat1": 85,
        "idnum": 1,
        "Gjisa": "",
        "Ocode": "A",
    }


class DetailIdnumLinesTest(IsolatedAsyncioTestCase):
    async def test_detail_returns_four_lines_with_idnum_slip_no(self) -> None:
        from app.services import transactions_service as svc

        bcodes = ["3417", "00914", "3280", "3375"]
        line_rows = [_line_row(bc) for bc in bcodes]

        async def fake_exec(_sid, sql, _params=()):
            if "FROM S1_Memo" in sql:
                return []
            if "FROM S1_Ssub" in sql and "GROUP BY" not in sql:
                return line_rows
            return []

        async def fake_book_meta(_sid, _hc, _bcodes):
            return {bc: {"gname": f"book-{bc}", "shelf": ""} for bc in _bcodes}

        async def fake_profile(*_a, **_k):
            return {"gname": "경남대[마산]"}

        async def fake_gnames(_sid, _pairs):
            return {("5019", "00405"): "경남대[마산]"}

        async def fake_stock(*_a, **_k):
            return 955

        async def fake_select_sql(_sid):
            return (
                "Gcode, Bcode, Gubun, Pubun, Gsqut, Gssum, Gbigo, Yesno, "
                "Gdang, Grat1, idnum AS Idnum, Gjisa, Ocode"
            )

        with patch.object(svc, "execute_query", new=fake_exec), \
             patch.object(svc, "_fetch_book_line_meta", new=fake_book_meta), \
             patch.object(svc, "fetch_g1_customer_profile", new=fake_profile), \
             patch.object(svc, "fetch_g1_customer_gnames", new=fake_gnames), \
             patch.object(svc, "compute_sales_statement_stock_qty", new=fake_stock), \
             patch(
                 "app.services.s1_ssub_adapt.detail_lines_select_sql",
                 new=fake_select_sql,
             ), \
             patch(
                 "app.services.s1_memo_adapt.s1_memo_column_meta",
                 new=AsyncMock(return_value=(set(), False)),
             ), \
             patch(
                 "app.services.s1_memo_adapt.memo_preview_select_sql",
                 return_value="Gbigo, Sbigo",
             ):
            detail = await svc.get_sales_statement_detail(
                server_id="remote_153",
                gdate="2026-06-04",
                hcode="5019",
                jubun="11",
                gjisa="",
                idnum=1,
                gubun="출고",
                gcode="00405",
            )

        self.assertIsNotNone(detail)
        assert detail is not None
        self.assertEqual(len(detail["lines"]), 4)
        self.assertEqual(detail["slip_no"], "00001")
        self.assertEqual(detail["order_key"]["idnum"], 1)
        self.assertEqual(
            [ln["bcode"] for ln in detail["lines"]],
            bcodes,
        )
        # detail WHERE 에 Ocode A (chul_09).
        # fake_exec 가 line_rows 를 반환했다면 WHERE 가 통과한 것.


if __name__ == "__main__":
    from unittest import main

    main()
