"""Sobo21 Label104 — PrinJing / _Sv_Ghng_ 누적 회귀."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.services.prinjing_service import (  # noqa: E402
    _StockState,
    _apply_s1_ssub_row,
    _apply_sg_csum_row,
    _apply_sv_ghng_agg,
    accumulate_prinjing_from_rows,
    compute_warehouse_stock_qty,
)


class PrinjingAccumulateTest(TestCase):
    def test_sv_ghng_gsusu_minus_gsqut(self) -> None:
        state = _StockState()
        _apply_sv_ghng_agg(
            state,
            {"Gcode": "BK01", "Gsusu": 100, "Gsqut": 30, "Obqut": 5},
        )
        bk = state.by_gcode["BK01"]
        self.assertEqual(bk.gsumx, 70.0)
        self.assertEqual(bk.gbqut, 5.0)

    def test_s1_outbound_reduces_gsumx(self) -> None:
        state = _StockState()
        _apply_s1_ssub_row(
            state,
            {
                "Bcode": "BK01",
                "Scode": "X",
                "Gubun": "출고",
                "Pubun": "",
                "Gsqut": 10,
            },
        )
        self.assertEqual(state.by_gcode["BK01"].gsumx, -10.0)

    def test_sg_csum_adds_gbsum(self) -> None:
        state = _StockState()
        _apply_sg_csum_row(state, {"Gcode": "BK01", "Scode": "B", "Gbsum": 694})
        self.assertEqual(state.by_gcode["BK01"].gsumx, 694.0)

    def test_pipeline_sum_label104_style(self) -> None:
        state = accumulate_prinjing_from_rows(
            sv_rows=[{"Gcode": "BK01", "Gsusu": 700, "Gsqut": 0, "Obqut": 0}],
            s1_open_rows=[],
            s1_all_rows=[],
            sg_rows=[],
        )
        self.assertEqual(int(round(state.by_gcode["BK01"].gsumx)), 700)


class PrinjingServiceAsyncTest(IsolatedAsyncioTestCase):
    async def test_missing_bcode_returns_none(self) -> None:
        from app.services import prinjing_service as svc

        qty = await svc.compute_warehouse_stock_qty(
            "remote_138", ocode="B", bcode="", hcode="5019"
        )
        self.assertIsNone(qty)

    async def test_compute_calls_opening_and_pipeline(self) -> None:
        from app.services import prinjing_service as svc

        calls: list[tuple[str, tuple]] = []

        async def fake_query(_sid, sql, params=None):
            calls.append((sql, tuple(params or ())))
            if "MAX(Gdate)" in sql:
                return [{"opening_date": "2026.01.01"}]
            if "FROM Sv_Ghng" in sql:
                return [{"Gcode": "B001", "Gsusu": 100, "Gsqut": 0, "Obqut": 0}]
            return []

        old = svc.execute_query
        svc.execute_query = fake_query
        try:
            qty = await svc.compute_warehouse_stock_qty(
                "remote_138", ocode="B", bcode="B001", hcode="5019"
            )
        finally:
            svc.execute_query = old

        self.assertEqual(qty, 100)
        self.assertTrue(any("MAX(Gdate)" in c[0] for c in calls))


if __name__ == "__main__":
    from unittest import main

    main()
