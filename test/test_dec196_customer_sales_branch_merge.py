"""DEC-196 — 거래처별판매 기본 집계는 거래처(Gcode) 단위, 「지점별검색」일 때만 지점 분리.

2026-08-25 사용자 리포트: "일부 거래처의 자료가 미반영 … 거래처세부내용들이 보인다".
원인: 모던이 항상 (Gcode, Gjisa) 로 행을 만들어 교보문고가 「본사 0 / 매장 30 / 본관 458」
3행이 되고 거래처 행이 0 으로 보였다. 레거시 Subu62 L330~335 는 CheckBox1(지점별검색)이
켜졌을 때만 Gjisa 로 Locate 하고 아니면 '' — 기본은 거래처 단위 합산이다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services import reports_service as rpt  # noqa: E402

# 교문사 00001 교보문고 실제 형상(2026-08): 판매는 지점행에만, 수금(H1)은 본사행.
S1_ROWS = [
    {"Hcode": "5019", "Gcode": "00001", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "2.부곡리(매장)", "Gdate": "2026.08.10", "Gsqut": 30, "Gssum": 834_090},
    {"Hcode": "5019", "Gcode": "00001", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "2.부곡리(본관)", "Gdate": "2026.08.20", "Gsqut": 458, "Gssum": 13_577_360},
    {"Hcode": "5019", "Gcode": "00001", "Scode": "X", "Gubun": "반품", "Pubun": "정품",
     "Gjisa": "2.부곡리(본관)", "Gdate": "2026.08.21", "Gsqut": -3, "Gssum": -90_000},
    # 지점이 없는 거래처 — 형상 불변 확인용.
    {"Hcode": "5019", "Gcode": "3333", "Scode": "X", "Gubun": "출고", "Pubun": "위탁",
     "Gjisa": "", "Gdate": "2026.08.05", "Gsqut": 3, "Gssum": 61_875},
]
H1_ROWS = [
    {"Hcode": "5019", "Gcode": "00001", "Gubun": "입금", "Gdate": "2026.08.15", "Gssum": 85_629_320},
]


def _fake_db():
    async def fake_exec(server_id, sql, params=()):
        if "FROM S1_Ssub" in sql:
            return S1_ROWS
        if "FROM H1_Ssub" in sql:
            return H1_ROWS
        return []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
        return [{"hcode": "5019", "gcode": "00001", "gname": "(주)교보문고"},
                {"hcode": "5019", "gcode": "3333", "gname": "#글로리아북[광주]"}]

    async def fake_class(server_id, hcode, rows, table="G1_Ggeo"):
        return None

    return (patch.object(rpt, "execute_query", fake_exec),
            patch.object(rpt, "in_clause_lookup", fake_in),
            patch.object(rpt, "_attach_customer_class_soft", fake_class))


class BranchMergeTests(IsolatedAsyncioTestCase):
    async def _run(self, **kw):
        p1, p2, p3 = _fake_db()
        with p1, p2, p3:
            return await rpt.get_customer_sales(
                server_id="remote_1", hcode="5019",
                date_from="2026.08.01", date_to="2026.08.25", scope="X", **kw,
            )

    async def test_default_merges_branches_into_customer_row(self) -> None:
        res = await self._run()
        kb = [r for r in res["rows"] if r["gcode"] == "00001"]
        self.assertEqual(len(kb), 1, "기본은 거래처 1행 — 지점으로 쪼개지면 거래처 행이 0 으로 보인다")
        row = kb[0]
        self.assertEqual(row["gjisa"], "")
        self.assertEqual(row["goqut"], 488)
        self.assertEqual(row["gbqut"], -3)
        self.assertEqual(row["gsusu"], 485)                       # 판매수량 = 출고 + 반품
        self.assertEqual(row["gssum"], 834_090 + 13_577_360 - 90_000)
        self.assertEqual(row["gjsum"], 85_629_320)                # 수금은 같은 행에
        self.assertEqual(row["gdate"], "2026.08.21")
        self.assertEqual(res["total"], 2)

    async def test_by_branch_splits_like_legacy_checkbox1(self) -> None:
        res = await self._run(by_branch=True)
        kb = sorted((r["gjisa"], r["goqut"], r["gjsum"]) for r in res["rows"] if r["gcode"] == "00001")
        # 본사행(수금 전용) + 지점 2행 — 종전 형상(레거시 지점별검색 ON).
        self.assertEqual(kb, [("", 0, 85_629_320), ("2.부곡리(매장)", 30, 0), ("2.부곡리(본관)", 458, 0)])
        self.assertEqual(res["total"], 4)

    async def test_customer_without_branch_unchanged(self) -> None:
        for bb in (False, True):
            res = await self._run(by_branch=bb)
            row = next(r for r in res["rows"] if r["gcode"] == "3333")
            self.assertEqual((row["gjisa"], row["goqut"], row["gssum"]), ("", 3, 61_875))


class ScreenWiringTests(IsolatedAsyncioTestCase):
    PAGE = FRONT / "app" / "(app)" / "reports" / "customer-sales" / "page.tsx"

    def test_checkbox_and_title(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn('data-legacy-id="Sobo62.CheckBox1"', src)     # 레거시 지점별검색
        self.assertIn("지점별검색", src)
        self.assertIn(">거래처별판매<", src)
        # 조회·상세·엑셀 세 경로 모두 같은 플래그를 싣는다.
        self.assertGreaterEqual(src.count("byBranch,"), 3)

    def test_registry_caption(self) -> None:
        reg = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        self.assertIn('caption: "거래처별판매"', reg)


if __name__ == "__main__":
    main()
