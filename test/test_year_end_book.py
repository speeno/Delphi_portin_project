"""DEC-033 (k+1) — Sobo67_yearbook 도서별년말집계 신규 포팅 회귀.

대상 함수
---------
- ``app.services.reports_service.get_year_end_book_aggregate`` — Subu67.pas
  Button101Click 동등 (S1_Ssub + Sg_Csum 2-pass + Korean literal 분류).

검증 5축 (포팅 계획 §5.3)
-------------------------
1. 분류 — POC apply_delphi_line 1:1 — 5종 Korean literal 분기 (Y+입고/Y+반품/
   X+폐기/Z+폐기/X+증정/X+출고).
2. book_mode 토글 — A/B/ALL 의 Ocode/Scode LIKE 절.
3. scode_filter on/off — Subu67 L317 추가 OR 절.
4. hcode/bcode 옵셔널 — 빈 값이면 WHERE 절 제거.
5. mysql3 호환 — SQL 본문에 derived table(``FROM (SELECT``) 미사용.
6. 드릴다운 — grain="month" + parent_bcode 인 경우 Bcode = %s 단일 절.

격리
-----
- ``execute_query`` + ``in_clause_lookup`` 만 patch (DB 무의존).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _row(
    *,
    bcode: str = "B0001",
    gdate: str = "2026.04.15",
    scode: str = "X",
    gubun: str = "출고",
    pubun: str = "",
    gsqut: int = 1,
    gssum: int = 100,
) -> dict[str, Any]:
    return {
        "bcode": bcode,
        "gdate": gdate,
        "scode": scode,
        "gubun": gubun,
        "pubun": pubun,
        "gsqut": gsqut,
        "gssum": gssum,
    }


class _Capture:
    """execute_query / in_clause_lookup 호출 추적용 헬퍼."""

    def __init__(self, detail_rows: list[dict[str, Any]] | None = None,
                 sg_rows: list[dict[str, Any]] | None = None) -> None:
        self.detail_rows = detail_rows or []
        self.sg_rows = sg_rows or []
        self.calls: list[tuple[str, tuple[Any, ...]]] = []
        self.lookup_spy = AsyncMock(return_value=[])

    async def fake_exec(self, server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
        self.calls.append((sql, tuple(params)))
        if "S1_Ssub" in sql:
            return list(self.detail_rows)
        return list(self.sg_rows)


async def _invoke(
    cap: _Capture,
    **overrides: Any,
) -> dict[str, Any]:
    from app.services import reports_service as rs

    kwargs: dict[str, Any] = {
        "server_id": "srv",
        "hcode": None,
        "date_from": "2026-04-01",
        "date_to": "2026-04-30",
    }
    kwargs.update(overrides)
    with patch("app.services.reports_service.execute_query", new=cap.fake_exec), \
         patch("app.services.reports_service.in_clause_lookup", new=cap.lookup_spy):
        return await rs.get_year_end_book_aggregate(**kwargs)


class ClassifierTests(IsolatedAsyncioTestCase):
    """축 1 — POC apply_delphi_line Korean literal 분기 1:1."""

    async def test_y_inbound_increments_giqut(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="Y", gubun="입고", gsqut=10)])
        out = await _invoke(cap)
        self.assertEqual(out["rows"][0]["giqut"], 10)
        self.assertEqual(out["rows"][0]["goqut"], 0)

    async def test_y_return_subtracts_giqut(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="Y", gubun="반품", gsqut=3)])
        out = await _invoke(cap)
        self.assertEqual(out["rows"][0]["giqut"], -3)

    async def test_x_pegi_increments_gbqut_and_gbsum(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="X", pubun="폐기", gsqut=5, gssum=500)])
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["gbqut"], 5)
        self.assertEqual(r["gbsum"], 500)
        self.assertEqual(r["gpqut"], 0)

    async def test_z_pegi_increments_gpqut_and_gbsum(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="Z", pubun="폐기", gsqut=2, gssum=200)])
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["gpqut"], 2)
        self.assertEqual(r["gbsum"], 200)
        self.assertEqual(r["gbqut"], 0)

    async def test_x_jeungjeong_uses_gjqut_and_gosum(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="X", pubun="증정", gsqut=1, gssum=10)])
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["gjqut"], 1)
        self.assertEqual(r["gosum"], 10)

    async def test_x_chulgo_uses_goqut_and_gosum(self) -> None:
        cap = _Capture(detail_rows=[_row(scode="X", gubun="출고", gsqut=4, gssum=400)])
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["goqut"], 4)
        self.assertEqual(r["gosum"], 400)

    async def test_pubun_return_uses_gbqut_and_gbsum(self) -> None:
        # Subu67.pas L371 — St4(Pubun)='반품' 분기 (Subu61 의 St3=Gubun 분기와 다름).
        cap = _Capture(detail_rows=[_row(scode="X", pubun="반품", gsqut=1, gssum=10)])
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["gbqut"], 1)
        self.assertEqual(r["gbsum"], 10)


class BookModeAndFilterTests(IsolatedAsyncioTestCase):
    """축 2-3 — book_mode + scode_filter WHERE 정합."""

    async def test_book_mode_a_uses_a_like(self) -> None:
        cap = _Capture()
        await _invoke(cap, book_mode="A")
        s1_sql, s1_params = cap.calls[0]
        self.assertIn("Ocode LIKE", s1_sql)
        self.assertIn("%A%", s1_params)

    async def test_book_mode_b_uses_b_like(self) -> None:
        cap = _Capture()
        await _invoke(cap, book_mode="B")
        s1_sql, s1_params = cap.calls[0]
        self.assertIn("%B%", s1_params)

    async def test_book_mode_all_uses_wildcard_like(self) -> None:
        cap = _Capture()
        await _invoke(cap, book_mode="ALL")
        _, s1_params = cap.calls[0]
        # ALL 은 LIKE '%' 만으로 본사+창고 모두 포함.
        self.assertIn("%", s1_params)

    async def test_scode_filter_on_adds_or_clause(self) -> None:
        cap = _Capture()
        await _invoke(cap, scode_filter=True)
        s1_sql, s1_params = cap.calls[0]
        # Subu67 L317-319 동등 — Scode='X' AND Gcode<>'00001' OR Y OR Z.
        self.assertIn("Scode='X'", s1_sql)
        self.assertIn("Scode='Y'", s1_sql)
        self.assertIn("Scode='Z'", s1_sql)
        self.assertIn("00001", s1_params)

    async def test_scode_filter_off_no_or_clause(self) -> None:
        cap = _Capture()
        await _invoke(cap, scode_filter=False)
        s1_sql, _ = cap.calls[0]
        self.assertNotIn("Scode='Y'", s1_sql)


class OptionalParamsTests(IsolatedAsyncioTestCase):
    """축 4 — hcode/bcode 옵셔널 (DEC-033 (f) 정책 일치)."""

    async def test_no_hcode_drops_clause(self) -> None:
        cap = _Capture()
        await _invoke(cap, hcode=None)
        s1_sql, _ = cap.calls[0]
        sg_sql, _ = cap.calls[1]
        self.assertNotIn("Hcode = %s", s1_sql)
        self.assertNotIn("Hcode = %s", sg_sql)

    async def test_blank_hcode_treated_as_none(self) -> None:
        cap = _Capture()
        await _invoke(cap, hcode="   ")
        s1_sql, _ = cap.calls[0]
        self.assertNotIn("Hcode = %s", s1_sql)

    async def test_present_hcode_keeps_clause(self) -> None:
        cap = _Capture()
        await _invoke(cap, hcode="H001")
        s1_sql, s1_params = cap.calls[0]
        self.assertIn("Hcode = %s", s1_sql)
        self.assertIn("H001", s1_params)

    async def test_bcode_range_applied(self) -> None:
        cap = _Capture()
        await _invoke(cap, bcode_from="B0001", bcode_to="B0100")
        s1_sql, s1_params = cap.calls[0]
        self.assertIn("Bcode >= %s", s1_sql)
        self.assertIn("Bcode <= %s", s1_sql)
        self.assertIn("B0001", s1_params)
        self.assertIn("B0100", s1_params)


class Mysql3CompatTests(IsolatedAsyncioTestCase):
    """축 5 — mysql3 호환 (derived table 미사용)."""

    async def test_no_derived_table_in_main(self) -> None:
        cap = _Capture()
        await _invoke(cap)
        s1_sql, _ = cap.calls[0]
        # mysql3 stall 회피 — derived table(FROM (SELECT ...) ) 사용 금지.
        self.assertNotIn("FROM (SELECT", s1_sql.upper().replace("FROM (SELECT ", "FROM (SELECT"))
        # GROUP BY 키는 Subu67.pas L326 와 동일.
        self.assertIn("GROUP BY s.Bcode, s.Gdate, s.Scode, s.Gubun, s.Pubun", s1_sql)

    async def test_no_derived_table_in_sg_csum(self) -> None:
        cap = _Capture()
        await _invoke(cap)
        sg_sql, _ = cap.calls[1]
        self.assertNotIn("FROM (SELECT", sg_sql)


class DrillDownAndGrainTests(IsolatedAsyncioTestCase):
    """축 6 — grain + 드릴다운."""

    async def test_year_grain_aggregates_to_year_prefix(self) -> None:
        cap = _Capture(detail_rows=[
            _row(gdate="2026.01.05", scode="X", gubun="출고", gsqut=2, gssum=20),
            _row(gdate="2026.07.20", scode="X", gubun="출고", gsqut=3, gssum=30),
        ])
        out = await _invoke(cap, grain="year")
        self.assertEqual(out["grain"], "year")
        self.assertEqual(len(out["rows"]), 1)
        r = out["rows"][0]
        self.assertEqual(r["gdate"], "2026")
        self.assertEqual(r["goqut"], 5)
        self.assertEqual(r["gosum"], 50)

    async def test_month_grain_with_parent_bcode_filter(self) -> None:
        cap = _Capture(detail_rows=[
            _row(gdate="2026.04.10", gsqut=1, gssum=10),
            _row(gdate="2026.05.10", gsqut=2, gssum=20),
        ])
        out = await _invoke(cap, grain="month", parent_bcode="B0001")
        s1_sql, s1_params = cap.calls[0]
        self.assertIn("Bcode = %s", s1_sql)
        self.assertIn("B0001", s1_params)
        self.assertEqual(out["grain"], "month")
        # 두 개의 월(04, 05) 버킷.
        self.assertEqual({r["gdate"] for r in out["rows"]}, {"2026.04", "2026.05"})

    async def test_month_grain_without_parent_includes_short_circuit_clause(self) -> None:
        # 부모 미지정 + 월 grid 진입 — POC grid2 정책에 따라 SQL WHERE 에 1=0 가드.
        # (mock 은 SQL 을 실제 실행하지 않으므로 결과 행 수가 아닌 SQL 본문을 검증.)
        cap = _Capture(detail_rows=[])
        out = await _invoke(cap, grain="month", parent_bcode=None)
        s1_sql, _ = cap.calls[0]
        sg_sql, _ = cap.calls[1]
        self.assertIn("1=0", s1_sql)
        self.assertIn("1=0", sg_sql)
        self.assertEqual(out["rows"], [])


class SgCsumMergeTests(IsolatedAsyncioTestCase):
    """Pass 2 (Sg_Csum) 가 gpsum 에 누적되는지 확인 (Subu67.pas L441 동등)."""

    async def test_sg_csum_adds_to_gpsum(self) -> None:
        cap = _Capture(
            detail_rows=[_row(scode="X", gubun="출고", gsqut=1, gssum=100)],
            sg_rows=[
                {"gcode": "B0001", "gdate": "2026.04.20", "gbsum": 999},
            ],
        )
        out = await _invoke(cap)
        r = out["rows"][0]
        self.assertEqual(r["gpsum"], 999)
        self.assertEqual(r["goqut"], 1)


if __name__ == "__main__":  # pragma: no cover
    main()
