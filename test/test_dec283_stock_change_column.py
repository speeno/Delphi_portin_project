"""DEC-283 — 재고현황 「변경」 컬럼 = 기간 내 Sg_Csum 합 (2026-09-12, 교문사 2025년 대조).

레거시 Subu34 는 기간 집계를 두 번 돈다: ① S1_Ssub 거래 라인(분기표) ② **Sg_Csum**
(`Select Gcode,Sum(Gbsum) ... Group By Gcode` → `Gpsum += T01`). 웹은 ②를 아예 읽지 않아
「변경」이 늘 0 이었고, 현재고 산식이 gpsum 을 더하므로 현재고까지 어긋났다.

라이브 대조(읽기 전용, remote_153/chul_09_db/5019, 2025-01-01~12-31) — 수정 후 10개 컬럼 전부 일치:
전재고 506,368 · 입고 127,404 · 반입 0 · 출고 144,581 · 증정 7,439 · 반품 −25,478 ·
폐기 −1,087 · **변경 −9,369** · 현재고 496,772 · 재고(반) 431 · 행 2,971.

Sg_Csum 은 재고변경 화면(Sobo52, DEC-282)이 쓰는 조정 테이블이다 — 그 화면의 저장분이 곧 「변경」.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import inventory_service as inv  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


S1_ROWS = [{"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 30}]
META = {"B1": {"Gcode": "B1", "Gname": "도서1", "Ocode": "", "Gubun": "C1", "Gdang": 1000},
        "B2": {"Gcode": "B2", "Gname": "도서2", "Ocode": "", "Gubun": "C1", "Gdang": 2000}}


def _call(*, sg_rows, scope="ALL", capture=None):
    async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
        if "FROM S1_Ssub" in sql and "GROUP BY Bcode" in sql:
            return list(S1_ROWS)
        if "FROM Sg_Csum" in sql and "SUM(Gbsum)" in sql and "GROUP BY Gcode" in sql:
            if capture is not None:
                capture.append((sql, tuple(params)))
            return list(sg_rows)
        if "MAX(Gdate)" in sql:
            return [{"d": "2024.12.31"}]
        return []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):  # noqa: ANN001
        if "G4_Book" in sql_template:
            return [META[k] for k in keys if k in META]
        if "G4_Gbun" in sql_template:
            return [{"Gcode": "C1", "Gname": "분류하나"}]
        return []

    with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
         patch.object(inv, "in_clause_lookup", new=AsyncMock(side_effect=fake_in)), \
         patch.object(inv, "_fetch_snapshot_bcodes", new=AsyncMock(return_value=[])), \
         patch.object(inv, "_fetch_carryover_bcodes", new=AsyncMock(return_value=[])), \
         patch.object(inv, "_fetch_return_stock_asof", new=AsyncMock(return_value={})), \
         patch("app.services.reports_service._fetch_stock_asof", new=AsyncMock(return_value={})):
        return _run(inv.get_stock_ledger(
            server_id="remote_153", hcode="5019", bcode=None,
            date_from="2025-01-01", date_to="2025-12-31", scope=scope,
        ))


class ChangeColumnTests(TestCase):
    def test_change_column_comes_from_sg_csum(self) -> None:
        out = _call(sg_rows=[{"Gcode": "B1", "q": -9369}])
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["gpsum"], -9369, "「변경」 = 기간 내 Sg_Csum SUM(Gbsum)")
        self.assertEqual(out["totals"]["gpsum"], -9369)

    def test_change_feeds_closing_stock(self) -> None:
        """현재고 = 전재고 + 입고 − 출고 − 증정 + 반입 + Gbsum + **변경**."""
        with_change = _call(sg_rows=[{"Gcode": "B1", "q": -100}])
        without = _call(sg_rows=[])
        b_with = next(r for r in with_change["by_book"] if r["bcode"] == "B1")
        b_without = next(r for r in without["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b_with["gsumy"] - b_without["gsumy"], -100)

    def test_adjustment_only_book_still_gets_a_row(self) -> None:
        """기간 거래가 없고 조정만 있는 도서도 행에 포함(레거시는 Sg_Csum 패스에서 Append)."""
        out = _call(sg_rows=[{"Gcode": "B2", "q": 5}])
        codes = [r["bcode"] for r in out["by_book"]]
        self.assertIn("B2", codes)
        self.assertEqual(next(r for r in out["by_book"] if r["bcode"] == "B2")["gpsum"], 5)

    def test_axis_scope_uses_paired_scodes(self) -> None:
        """본사 조회 = Scode A(정품)+C(반품 버킷), 창고 = B+D — Subu34_1 축 매핑."""
        cap: list = []
        _call(sg_rows=[], scope="A", capture=cap)
        self.assertTrue(cap, "본사 조회에서도 Sg_Csum 패스가 돈다")
        sql, params = cap[0]
        self.assertIn("(Scode = %s OR Scode = %s)", sql)
        self.assertIn("A", params)
        self.assertIn("C", params)
        cap.clear()
        _call(sg_rows=[], scope="B", capture=cap)
        self.assertIn("B", cap[0][1])
        self.assertIn("D", cap[0][1])

    def test_all_axis_reads_every_scode(self) -> None:
        cap: list = []
        _call(sg_rows=[], scope="ALL", capture=cap)
        self.assertNotIn("Scode", cap[0][0].split("GROUP BY")[0].split("WHERE")[1])

    def test_hcode_is_bound(self) -> None:
        cap: list = []
        _call(sg_rows=[], capture=cap)
        self.assertIn("Hcode = %s", cap[0][0])
        self.assertIn("5019", [str(p) for p in cap[0][1]])


if __name__ == "__main__":
    main()
