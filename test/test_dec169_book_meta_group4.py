"""DEC-169 GROUP 4 (입고) — 도서명이 있는 입고 목록에 ISBN(``gisbn``) 컬럼 덧붙임 회귀 가드.

- 입고접수 상세(B10, B13/B14 라인 지연조회 공용) 라인에 ``gisbn`` 이 붙는다.
- 일별 입고내역서(B11) 두 그리드(by_publisher/by_vendor)에 ``gisbn`` 이 붙는다 —
  by_vendor 는 hcode 컬럼이 없어 로그인 hcode 로 조회, 슈퍼(hcode=None)면 같은 페이지의
  by_publisher 결과로 보충한다.
- 목록 SELECT 는 바뀌지 않는다(G4_Book JOIN 금지) — 청크 lookup(book_meta_lookup) 경유.
- 정가(gdang)는 전표 단가 정본 → 건드리지 않는다(price_key=None).
- lookup 실패 시 목록은 깨지지 않고 ``gisbn=''`` 로 흡수된다.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

import app.services.book_meta_lookup as bml  # noqa: E402
import app.services.inbound_service as inb  # noqa: E402

_G4_COLS = ({"gcode", "gname", "gdang", "gisbn"}, {"gdang": "Gdang", "gisbn": "Gisbn"})
_BOOK_META = {"B1": ("도서1", 12000, "9788900000011"), "B2": ("도서2", 9000, "9788900000028")}


def _fake_book_lookup(calls: list):
    """book_meta_lookup.in_clause_lookup 대체 — (hcode, keys) 기록 + 정적 마스터 반환."""

    async def _fn(server_id, *, sql_template, keys, prefix_params=(), **kw):  # noqa: ANN001
        calls.append((prefix_params[0] if prefix_params else None, tuple(keys)))
        self_hcode = prefix_params[0] if prefix_params else ""
        if self_hcode == "":  # 공용 마스터 폴백은 비어 있음(테넌트 마스터만 있는 시나리오)
            return []
        return [
            {"bcode": k, "gname": _BOOK_META[k][0], "gdang": _BOOK_META[k][1], "gisbn": _BOOK_META[k][2]}
            for k in keys if k in _BOOK_META
        ]

    return _fn


class ReceiptDetailIsbnTest(TestCase):
    def test_detail_lines_carry_gisbn_without_touching_gdang(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            s = sql.upper()
            if "BCODE" in s and "FROM S1_SSUB" in s and "MAX(IDNUM" not in s:
                return [
                    {"Bcode": "B1", "Pubun": "B", "Gsqut": 5, "Gdang": 1000, "Grat1": 0.7,
                     "Gssum": 3500, "Gbigo": "", "Yesno": "0"},
                    {"Bcode": "B9", "Pubun": "B", "Gsqut": 1, "Gdang": 0, "Grat1": 0.7,
                     "Gssum": 0, "Gbigo": "", "Yesno": "0"},  # 마스터 없는 도서
                ]
            return []

        calls: list = []
        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_present_cols", new=AsyncMock(return_value=set())), \
             patch.object(inb, "_fetch_product_names", new=AsyncMock(return_value={"B1": "도서1"})), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})), \
             patch.object(bml, "g4_book_column_meta", new=AsyncMock(return_value=_G4_COLS)), \
             patch.object(bml, "in_clause_lookup", new=AsyncMock(side_effect=_fake_book_lookup(calls))):
            d = asyncio.run(inb.get_receipt_detail(
                server_id="remote_153", gdate="2026.08.18", hcode="5019", gcode="V1", jubun="3",
            ))

        self.assertIsNotNone(d)
        lines = d["lines"]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["gisbn"], "9788900000011")
        self.assertEqual(lines[0]["gdang"], 1000)     # 전표 단가 보존
        self.assertEqual(lines[1]["gisbn"], "")       # 마스터 부재 → ''
        self.assertEqual(lines[1]["gdang"], 0)        # 정가 미주입(price_key=None)
        # lookup 은 라인의 hcode(=전표 출판사) 로 먼저, 못 찾은 코드는 '' 공용 폴백.
        self.assertEqual(calls[0][0], "5019")
        self.assertEqual(calls[1], ("", ("B9",)))

    def test_detail_survives_isbn_lookup_failure(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            if "BCODE" in sql.upper() and "FROM S1_SSUB" in sql.upper():
                return [{"Bcode": "B1", "Pubun": "B", "Gsqut": 1, "Gdang": 100,
                         "Grat1": 0, "Gssum": 100, "Gbigo": "", "Yesno": "0"}]
            return []

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_present_cols", new=AsyncMock(return_value=set())), \
             patch.object(inb, "_fetch_product_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "attach_book_meta", new=AsyncMock(side_effect=RuntimeError("G4_Book gone"))):
            d = asyncio.run(inb.get_receipt_detail(
                server_id="remote_153", gdate="2026.08.18", hcode="5019", gcode="V1", jubun="3",
            ))
        self.assertEqual(d["lines"][0]["gisbn"], "")
        self.assertEqual(d["lines"][0]["gdang"], 100)


class DailyReportIsbnTest(TestCase):
    _PUB = {"gdate": "2026.08.18", "hcode": "5019", "gcode": "V1", "idnum": 1, "pubun": "B",
            "bcode": "B1", "gsqut": 5, "gdang_sum": 2000, "cnt": 2}
    _VEN = {"gcode": "V1", "idnum": 1, "pubun": "B", "bcode": "B1", "gsqut": 5,
            "gdang_sum": 2000, "grat1_sum": 1.4, "gssum": 7000, "cnt": 2}

    def _run(self, hcode):
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            s = sql.upper()
            if "GROUP BY" in s and "HCODE AS HCODE" in s:
                return [dict(self._PUB)]
            if "GROUP BY" in s:
                return [dict(self._VEN)]
            return [{"qty": 5, "amount": 7000}]

        calls: list = []
        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_present_cols", new=AsyncMock(return_value=set())), \
             patch.object(inb, "in_clause_lookup", new=AsyncMock(return_value=[])), \
             patch.object(bml, "g4_book_column_meta", new=AsyncMock(return_value=_G4_COLS)), \
             patch.object(bml, "in_clause_lookup", new=AsyncMock(side_effect=_fake_book_lookup(calls))):
            out = asyncio.run(inb.daily_report(server_id="remote_153", gdate="2026-08-18", hcode=hcode))
        return out, calls

    def test_both_grids_carry_gisbn_for_tenant(self) -> None:
        out, calls = self._run("5019")
        self.assertEqual(out["by_publisher"][0]["gisbn"], "9788900000011")
        self.assertEqual(out["by_vendor"][0]["gisbn"], "9788900000011")
        self.assertEqual(out["by_publisher"][0]["gdang"], 1000)   # 평균 전표 단가 그대로
        self.assertTrue(all(h == "5019" for h, _ in calls))       # 테넌트 hcode 로만 조회

    def test_super_vendor_grid_backfilled_from_publisher_grid(self) -> None:
        # 슈퍼(hcode=None): by_publisher 는 행 hcode(5019) 로, by_vendor 는 '' 공용 폴백(빈 결과)
        # → 같은 페이지 by_publisher 의 bcode→ISBN 으로 보충.
        out, calls = self._run(None)
        self.assertEqual(out["by_publisher"][0]["gisbn"], "9788900000011")
        self.assertEqual(out["by_vendor"][0]["gisbn"], "9788900000011")
        self.assertIn("5019", [h for h, _ in calls])
