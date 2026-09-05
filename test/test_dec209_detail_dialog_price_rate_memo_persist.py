"""DEC-209 — 거래 명세서 상세 팝업: 단가 편집 + 기존 라인의 단가·공급율·비고 변경 저장 (2026-08-26 01:02).

원문: "팝업 내 추가 수정 가능 값 및 팝업 창 이동 가능하도록 요".

발견/결정
--------
- `outbound_service.update_order` 의 기존 라인 UPDATE 가 Pubun/Gsqut/Gssum 만 비교·갱신해 상세 팝업에서
  고친 공급율(Grat1)·비고(Gbigo)·단가(Gdang)가 **조용히 버려졌다**. → 존재 컬럼(`_OPTIONAL_LINE_COLS`)을
  SELECT 에 넣어 비교하고 UPDATE SET 에 포함한다(DDL 드리프트 서버는 컬럼 없으면 제외).
- 라인 그리드의 단가는 읽기 전용 텍스트였다 → 입력 셀(콤마 표시, 변경 시 금액 자동 재계산).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import outbound_service as svc  # noqa: E402

CURRENT = [
    {"Gdate": "2026.08.25", "Hcode": "5019", "Jubun": "3", "Gcode": "00047", "Bcode": "208", "Pubun": "위탁",
     "Gsqut": 1, "Gssum": 0, "Yesno": "", "Gjisa": "", "Gubun": "출고", "Ocode": "A", "Scode": "X", "Idnum": 72,
     "Gdang": 18000, "Grat1": 0, "Gbigo": "메모"},
]
COLS = {"gdate", "hcode", "jubun", "gjisa", "gcode", "bcode", "gubun", "ocode", "scode", "yesno", "pubun", "gsqut", "gssum", "idnum", "gdang", "grat1", "gbigo"}


class UpdateOrderOptionalColumns(IsolatedAsyncioTestCase):
    def _patches(self, cols=COLS):
        calls: list = []

        async def fake_query(server_id, sql, params=()):
            calls.append(("Q", sql, params))
            return list(CURRENT)

        async def fake_tx(server_id, statements):
            calls.append(("TX", statements))

        async def fake_cols(server_id):
            return set(cols)

        return calls, patch.object(svc, "execute_query", fake_query), patch.object(svc, "execute_in_transaction", fake_tx), patch.object(svc, "s1_column_names", fake_cols)

    async def test_rate_and_memo_change_is_persisted(self) -> None:
        calls, p1, p2, p3 = self._patches()
        with p1, p2, p3:
            res = await svc.update_order(
                server_id="remote_153", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 1, "gssum": 15840,
                                "gdang": 18000, "grat1": 88, "gbigo": "신간출고"}],
            )
        self.assertEqual(res["diff"]["updated"] if "diff" in res else res.get("updated"), 1)
        sel = [c for c in calls if c[0] == "Q"][0][1]
        self.assertIn(", Gdang, Grat1, Gbigo", sel, "존재 컬럼을 읽어 비교")
        stmts = [c for c in calls if c[0] == "TX"][0][1]
        upd = stmts[0]
        self.assertIn("SET Pubun=%s, Gsqut=%s, Gssum=%s, Gdang=%s, Grat1=%s, Gbigo=%s, Time3=NOW()", upd[0])
        self.assertEqual(upd[1][:6], ("위탁", 1, 15840, 18000, 88.0, "신간출고"))

    async def test_unit_price_change_alone_triggers_update(self) -> None:
        calls, p1, p2, p3 = self._patches()
        with p1, p2, p3:
            await svc.update_order(
                server_id="remote_153", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 1, "gssum": 0,
                                "gdang": 20000, "grat1": 0, "gbigo": "메모"}],
            )
        txs = [c for c in calls if c[0] == "TX"]
        self.assertEqual(len(txs), 1, "단가만 바뀌어도 UPDATE")
        self.assertEqual(txs[0][1][0][1][3], 20000)

    async def test_no_change_no_update(self) -> None:
        calls, p1, p2, p3 = self._patches()
        with p1, p2, p3:
            await svc.update_order(
                server_id="remote_153", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 1, "gssum": 0,
                                "gdang": 18000, "grat1": 0, "gbigo": "메모"}],
            )
        self.assertEqual([c for c in calls if c[0] == "TX"], [])

    async def test_ddl_drift_without_optional_columns(self) -> None:
        """Gdang/Grat1/Gbigo 컬럼이 없는 서버 — SELECT/UPDATE 에서 제외되고 종전 3컬럼 비교."""
        calls, p1, p2, p3 = self._patches(cols=COLS - {"gdang", "grat1", "gbigo"})
        with p1, p2, p3:
            await svc.update_order(
                server_id="remote_1", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 2, "gssum": 0,
                                "gdang": 99999, "grat1": 50, "gbigo": "x"}],
            )
        sel = [c for c in calls if c[0] == "Q"][0][1]
        self.assertNotIn("Gdang", sel)
        upd = [c for c in calls if c[0] == "TX"][0][1][0]
        self.assertIn("SET Pubun=%s, Gsqut=%s, Gssum=%s, Time3=NOW()", upd[0])
        self.assertEqual(upd[1][:3], ("위탁", 2, 0))


class LineGridPriceEditable(TestCase):
    def test_price_cell_is_input(self) -> None:
        src = (FRONT / "components" / "outbound" / "order-line-grid.tsx").read_text(encoding="utf-8")
        i = src.index('case "gdang":')
        block = src[i : src.index('case "gssum":', i)]
        # DEC-239 — legacy id 는 축 데이터(axis.legacy.gdang); 출고 축 값은 그대로 Sobo27.Line.Gdang.
        self.assertIn("data-legacy-id={axis.legacy.gdang}", block)
        self.assertIn('gdang: "Sobo27.Line.Gdang"', src)
        self.assertIn("setAt(idx, { gdang:", block, "변경 시 금액 자동 재계산 경로(setAt)")
        self.assertIn("onKeyDown={focusNextCell}", block, "Enter 흐름에 단가 포함")


if __name__ == "__main__":
    main()
