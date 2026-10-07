"""DEC-378 — 거래명세서 상세(출고현황) 수정 · 반품접수 저장 (교문사 2026-10-07).

보고
----
1. 「도서코드 입력 시 칸이 너무 작아서 돋보기를 클릭해야 함」 — 좁은 팝업에서 표가 칸을 눌러 입력칸이 글자 하나 폭.
2. 「도서명은 입력이 안 됨」 — 도서명은 조회 전용(DEC-300). 이름 검색은 도서코드 칸(자동완성 · 돋보기). 직접 친 코드의 도서명 보충 조회가 팝업에 없었다.
3. 「신규 줄이 생기면 위 내용과 동일하게 공급율」 — 팝업의 거래처 비율이 ① 출판사(G7) 값이었고 ② "1"~"6" 키라 구분(위탁 …)과 안 맞아 새 줄이 늘 0%.
4. 「수정 명세서를 띄웠을 때 입력 순서가 아님」 — 상세 SELECT 가 `ORDER BY Gcode`(전표 안에서 무의미).
5. 「반품접수 저장 에러」 — 422 `lines[0].grat1 ≤ 1`. 비율은 % (DEC-301)인데 입력 모델에 le=1.0 이 남아 있었다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from pydantic import ValidationError

from app.models.returns import ReturnLineInput
from app.services import outbound_service as obs

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class ReturnRateIsPercent(TestCase):
    def test_85_percent_accepted(self) -> None:
        ln = ReturnLineInput(bcode="3411", gsqut=1, grat1=85)
        self.assertEqual(ln.grat1, 85)

    def test_bounds(self) -> None:
        with self.assertRaises(ValidationError):
            ReturnLineInput(bcode="3411", gsqut=1, grat1=101)
        with self.assertRaises(ValidationError):
            ReturnLineInput(bcode="3411", gsqut=1, grat1=-1)


class DetailOrderAndRates(IsolatedAsyncioTestCase):
    async def test_lines_in_input_order(self) -> None:
        with patch.object(obs, "s1_column_names", AsyncMock(return_value={"id", "gdang", "grat1", "gbigo", "idnum"})):
            sql = await obs._build_detail_lines_sql("remote_153", "00001", "")  # noqa: SLF001
        self.assertTrue(sql.rstrip().endswith("ORDER BY Id"))
        with patch.object(obs, "s1_column_names", AsyncMock(return_value={"gdang"})):
            sql2 = await obs._build_detail_lines_sql("remote_153", "", "")  # noqa: SLF001
        self.assertTrue(sql2.rstrip().endswith("ORDER BY Gcode"))  # Id 없는 서버는 종전대로

    async def test_customer_rates_from_g1_not_g7(self) -> None:
        rows = [{"Gdate": "2026.10.07", "Hcode": "5019", "Jubun": "1", "Gcode": "00004", "Bcode": "3411",
                 "Pubun": "위탁", "Gsqut": 1, "Gssum": 23000, "Yesno": "", "Gdang": 29000, "Grat1": 80, "Gbigo": "", "Idnum": 1}]

        async def fake_exec(server_id, sql, params=()):
            if "FROM S1_Ssub" in sql:
                return rows
            if "FROM G1_Ggeo" in sql:
                return [{"hcode": "", "grat1": 70}, {"hcode": "5019", "grat1": 80, "grat2": 60}]
            if "FROM G7_Ggeo" in sql:
                return [{"gname": "교문사", "pubun": "", "grat1": 0}]
            return []

        with patch.object(obs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(obs, "s1_column_names", AsyncMock(return_value={"id", "gdang", "grat1", "gbigo", "idnum"})), \
             patch.object(obs, "_fetch_product_names", AsyncMock(return_value={})), \
             patch.object(obs, "fetch_g1_customer_gnames", AsyncMock(return_value={})):
            res = await obs.get_order_detail(server_id="remote_153", gdate="2026.10.07", hcode="5019", jubun="1", gcode="00004")
        self.assertEqual(res["customer"]["grat1"], 80)  # 자사 행 우선
        self.assertEqual(res["customer"]["grat2"], 60)


class DialogWiring(TestCase):
    def test_rate_map_keyed_by_pubun_and_inherit(self) -> None:
        src = _read("components/outbound/order-detail-dialog.tsx")
        self.assertNotIn('"1": detail.customer.grat1', src)
        self.assertIn("for (const p of PUBUN_OPTIONS) out[p.value] = Number(rates[p.rateIndex - 1]) || 0;", src)
        self.assertIn("inheritPrevLine", src)
        self.assertIn("onLookupBook={(bcode) => resolveBookByCode(serverId, bcode)}", src)

    def test_grid_keeps_column_widths_and_inherits(self) -> None:
        src = _read("components/outbound/order-line-grid.tsx")
        self.assertIn('style={{ minWidth: `${tableMinWidth}px` }}', src)
        self.assertIn("const last = inheritPrevLine ? lines[lines.length - 1] : undefined;", src)


if __name__ == "__main__":
    main()
