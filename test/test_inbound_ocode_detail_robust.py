"""입고 조회 회귀 (2026-06-21).

(A) 입고 LIST Ocode 필터 — 창고/지사/NULL 규약이 섞여 있어 단일값 강제 시 0건이 되던 회귀.
    Gubun='입고'+Scode='Y' 로 입고를 정의하고 Ocode 는 NULL/'A'/'B' 전부 허용.
(B) 입고 상세 — 메모(S1_Memo) 스키마 드리프트로 실패해도 라인 상세는 반환(500 방지).
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

import app.services.inbound_service as inb  # noqa: E402


class InboundListOcodeTest(TestCase):
    def test_list_where_accepts_null_a_b_ocode(self) -> None:
        captured: dict[str, object] = {}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            if "FROM S1_Ssub WHERE" in sql and "GROUP BY" in sql:
                captured["sql"] = sql
                captured["params"] = tuple(params)
            return []

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "count_grouped", new=AsyncMock(return_value=0)), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})):
            asyncio.run(inb.list_receipts(
                server_id="remote_153", date_from="2026.06.01", date_to="2026.06.21",
            ))
        sql = captured.get("sql", "")
        # 기본 호출(입고접수/입고명세서) 은 Gubun='입고' 유지 — 2026-08-22 부터 바인딩 파라미터.
        # (입고현황 facade 만 gubun=None 으로 레거시 Subu25 무필터를 재현한다.)
        self.assertIn("Gubun = %s", sql)
        self.assertIn("입고", captured.get("params", ()))
        self.assertIn("Scode = 'Y'", sql)
        # NULL/'A'/'B' 전부 허용 — 단일 Ocode 강제 금지
        self.assertIn("IFNULL(Ocode,'') IN ('', 'A', 'B')", sql)


class InboundReportHcodeIsolationTest(TestCase):
    """일별/기간 입고내역서 멀티테넌트 격리(보안, 2026-06-22).

    비-슈퍼(hcode 지정)는 ``Hcode=%s`` 로 로그인 출판사 입고만, 슈퍼(None)는 전사.
    파라미터 수 == ``%s`` 수 정합. ``{hcode_clause}`` 토큰 잔여 금지.
    """

    def _capture(self, fn_name: str, hcode, **kwargs):
        seen: list = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            seen.append((sql, params))
            return []

        async def fake_in(server_id, **kw):  # noqa: ANN001
            return []

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "in_clause_lookup", new=AsyncMock(side_effect=fake_in)):
            asyncio.run(getattr(inb, fn_name)(server_id="remote_153", hcode=hcode, **kwargs))
        return seen

    def test_daily_filters_by_hcode_for_non_super(self) -> None:
        for sql, params in self._capture("daily_report", "5019", gdate="2026-06-11"):
            self.assertNotIn("{hcode_clause}", sql)        # 토큰 완전 치환
            self.assertEqual(sql.count("%s"), len(params))  # 파라미터 정합
        main_sql, main_params = self._capture("daily_report", "5019", gdate="2026-06-11")[0]
        self.assertIn("Hcode=%s", main_sql)                 # 격리 적용
        self.assertIn("5019", main_params)

    def test_daily_no_filter_for_super(self) -> None:
        main_sql, main_params = self._capture("daily_report", None, gdate="2026-06-11")[0]
        self.assertNotIn("Hcode=%s", main_sql)              # 슈퍼 → 전사
        self.assertNotIn("{hcode_clause}", main_sql)
        self.assertEqual(main_sql.count("%s"), len(main_params))

    def test_period_filters_by_hcode_for_non_super(self) -> None:
        main_sql, main_params = self._capture(
            "period_report", "5019", date_from="2026-06-01", date_to="2026-06-21")[0]
        self.assertIn("Hcode=%s", main_sql)
        self.assertIn("5019", main_params)
        self.assertEqual(main_sql.count("%s"), len(main_params))


class InboundDetailMemoTolerantTest(TestCase):
    def test_detail_returns_lines_when_memo_query_fails(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            s = sql.upper()
            if "FROM S1_MEMO" in s:
                raise RuntimeError("Unknown column 'Gpost' (스키마 드리프트)")
            if "BCODE" in s and "FROM S1_SSUB" in s:
                return [{
                    "Gdate": params[0], "Hcode": params[1], "Gcode": params[2], "Jubun": params[3],
                    "Bcode": "B1", "Pubun": "입고", "Gsqut": 5, "Gdang": 1000,
                    "Grat1": 0, "Gssum": 5000, "Gbigo": "", "Yesno": "0",
                }]
            return []

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_fetch_product_names", new=AsyncMock(return_value={"B1": "도서1"})), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})):
            d = asyncio.run(inb.get_receipt_detail(
                server_id="remote_153", gdate="2026.06.19", hcode="5019", gcode="V1", jubun="3",
            ))
        self.assertIsNotNone(d)  # 500/None 아님
        self.assertEqual(len(d["lines"]), 1)
        self.assertIsNone(d["memo"])  # 메모는 None 으로 강등


class InboundReportGrat1TypeTest(TestCase):
    """일별/기간 입고내역서 — grat1 이 bytes/특수타입(연결 charset) 이어도 TypeError 500 금지.

    회귀(2026-06-21): ``_row_vendor`` 등이 raw ``float(grat1)`` 라 grat1 bytes 시 500.
    ``_safe_num`` 으로 교체해 견고화.
    """

    def _run(self, fn_name: str, **kwargs):
        # 집계는 IFNULL(SUM)+COUNT, 평균은 Python — grat1 은 bytes(연결 charset) 로 둬도 안전.
        ven = {"gcode": "V1", "idnum": "1", "pubun": "입", "bcode": "B1",
               "gsqut": 5, "gdang_sum": b"2000", "grat1_sum": b"160.0",
               "gssum": 400000, "cnt": b"2"}  # 평균 gdang=1000, grat1=80
        pub = {"gdate": "2026.06.19", "hcode": "5019", "gcode": "V1", "idnum": "1",
               "pubun": "입", "bcode": "B1", "gsqut": 5, "gdang_sum": b"2000", "cnt": b"2"}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            s = sql.upper().replace(" ", "")
            if "GRAND" in s:
                return [{"qty": 5, "amount": 400000}]
            if "GRAT1_SUM" in s:
                return [ven]
            if "GDANG_SUM" in s:
                return [pub]
            return []

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_product_names", new=AsyncMock(return_value={})):
            return asyncio.run(getattr(inb, fn_name)(server_id="remote_153", **kwargs))

    def test_daily_report_grat1_bytes_no_typeerror(self) -> None:
        d = self._run("daily_report", gdate="2026.06.19")
        self.assertEqual(len(d["by_vendor"]), 1)
        self.assertEqual(d["by_vendor"][0]["grat1"], 80)  # bytes b'80.0' → 80

    def test_period_report_grat1_bytes_no_typeerror(self) -> None:
        p = self._run("period_report", date_from="2026.06.01", date_to="2026.06.21")
        self.assertEqual(len(p["by_vendor"]), 1)


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
