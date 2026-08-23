"""DEC-145 — 거래처판매 수금행 최종거래일 + 상세 패널 sticky 회귀 가드.

2026-08-11 15:24 영업팀 화면 보고: "거래처 수금액은 있는데 거래 종수 등이 모두 0".
진단 — 집계는 정상. 수금(H1_Ssub)은 Gcode 단위라 본사행(gjisa='')에 적재되는데
(레거시 Subu62 Locate('Gcode;Gjisa',[Gcode,'']) 1:1), 그 행의 최종거래일(gdate)이
빈값이라 기본 정렬(최종거래일 asc)에서 수금 전용 행이 전부 목록 최상단에 몰려
"전부 0" 화면으로 보였다.

수정 — H1_Ssub 집계에 MAX(Gdate) 를 포함해 수금도 최종거래일에 반영한다.
+ 우측 도서별 상세 패널 sticky 플로팅(스크롤 추종, 사용자 요청 2026-08-13).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import reports_service as rpt  # noqa: E402

S1_ROWS = [
    # 판매는 지사행에만 — 본사행(gjisa='') 없음 (교문사 00001 교보문고 실제 형상).
    {"Hcode": "5019", "Gcode": "00001", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "부곡리(매장)", "Gdate": "2026.08.01", "Gsqut": 2570, "Gssum": 68457500},
    # 본사행에 판매가 있는 거래처 — 수금일이 더 늦으면 gdate 갱신 검증용.
    {"Hcode": "5019", "Gcode": "00227", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "", "Gdate": "2026.07.20", "Gsqut": 4, "Gssum": 95200},
]

H1_ROWS = [
    {"Hcode": "5019", "Gcode": "00001", "Gubun": "입금", "Gdate": "2026.08.05",
     "Gssum": 24_837_100},
    {"Hcode": "5019", "Gcode": "00227", "Gubun": "입금", "Gdate": "2026.08.03",
     "Gssum": 1_700_000},
]


def _fake_db(h1_rows):
    async def fake_exec(server_id, sql, params=()):
        if "FROM H1_Ssub" in sql:
            assert "MAX(Gdate)" in sql, "H1 수금 집계는 최종 수금일(MAX Gdate) 포함"
            return h1_rows
        if "FROM S1_Ssub" in sql:
            return S1_ROWS
        return []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
        return [{"hcode": "5019", "gcode": k, "gname": f"거래처{k}"} for k in keys]

    return patch.object(rpt, "execute_query", fake_exec), \
        patch.object(rpt, "in_clause_lookup", fake_in)


class SugumGdateTests(IsolatedAsyncioTestCase):
    async def _run(self, h1_rows, **kw):
        p1, p2 = _fake_db(h1_rows)
        with p1, p2:
            return await rpt.get_customer_sales(
                server_id="remote_1", hcode="5019",
                date_from="2026.07.11", date_to="2026.08.11", scope="X", **kw,
            )

    async def test_collection_only_hq_row_gets_last_payment_date(self) -> None:
        res = await self._run(H1_ROWS)
        hq = next(r for r in res["rows"] if r["gcode"] == "00001" and r["gjisa"] == "")
        self.assertEqual(hq["gjsum"], 24_837_100)
        self.assertEqual(hq["gdate"], "2026.08.05", "수금 전용 본사행도 최종거래일 표기")

    async def test_hq_row_with_sales_takes_max_of_sale_and_payment(self) -> None:
        res = await self._run(H1_ROWS)
        row = next(r for r in res["rows"] if r["gcode"] == "00227")
        self.assertEqual((row["goqut"], row["gjsum"]), (4, 1_700_000))
        self.assertEqual(row["gdate"], "2026.08.03", "수금일 > 판매일이면 수금일")

    async def test_sale_date_kept_when_newer_than_payment(self) -> None:
        res = await self._run([
            {"Hcode": "5019", "Gcode": "00227", "Gubun": "입금", "Gdate": "2026.07.01",
             "Gssum": 500},
        ])
        row = next(r for r in res["rows"] if r["gcode"] == "00227")
        self.assertEqual(row["gdate"], "2026.07.20", "판매일이 더 최신이면 유지")

    async def test_gdate_asc_no_longer_piles_collection_rows_first(self) -> None:
        res = await self._run(H1_ROWS, sort_by="gdate", sort_dir="asc")
        gdates = [r["gdate"] for r in res["rows"]]
        self.assertNotIn("", gdates, "빈 최종거래일 행이 남지 않는다")
        self.assertEqual(gdates, sorted(gdates))


class DetailPanelStickyGuard(TestCase):
    """우측 도서별 상세 패널 — 스크롤 추종(sticky) 클래스 가드."""

    PAGE = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
            / "reports" / "customer-sales" / "page.tsx")

    def test_detail_pane_moved_below_master_grid(self) -> None:
        """DEC-188 (운영 요청 2026-08-23) — 상세를 **우측 sticky 패널 → 하단**으로 옮겼다.

        레거시 Subu62 가 상·하단 2단이라 그 구성에 맞춘다. sticky 는 이제 공통
        `DataGrid` 가 헤더/합계행에 제공하므로 패널 자체 sticky 클래스는 불필요하다.
        """
        src = self.PAGE.read_text(encoding="utf-8")
        # 상세가 상단 그리드 «뒤»에 온다(좌우 분할이 아니라 세로 배치).
        self.assertLess(
            src.index('legacyId="Sobo62.DBGrid101"'),
            src.index('legacyId="Sobo62.DBGrid201"'),
            "상세가 상단 목록보다 앞에 오면 2단 배치가 깨진 것",
        )
        self.assertNotIn("xl:grid-cols-[minmax(0,1.15fr)", src, "좌우 2분할 잔존")
        # 공통 DataGrid 로 렌더 — 정렬·컬럼설정·sticky 헤더/합계를 함께 얻는다.
        self.assertIn("<DataGrid<CustomerDetailGridRow>", src)
        self.assertIn("totals={detailTotals}", src)


if __name__ == "__main__":
    main()
