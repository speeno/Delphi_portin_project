"""DEC-305 — 폐기 현황(= 폐기 접수 「목록」): 반품 현황과 같은 구성 + 거래처명(G5 기타거래처) 표시 (2026-09-23).

원문(캡처): "[반품/폐기관리] 폐기현황 — 기존 「00현황」과 동일한 기능, 동일한 이미지로 요청 / 도서코드, 전표, 거래구분,
바로출고: 불필요" + "폐기접수, 폐기현황이 동일한 화면이다"(폐기 접수의 「목록」이 폐기 현황 — DEC-192 별도 목록 없음).

- 축: slimFilters·noDispatch·docLabel 「폐기 명세서」(반품 현황 DEC-302/303 과 동일).
- 이름: 폐기 전표는 Scode='Z' + 기타거래처(G5_Ggeo, 예 05210 애플2) — 현황 리졸버 ``name_source='etc'`` 와
  전표 상세의 G1 미스 → G5 폴백으로 「애플2」를 띄운다(종전 G1 조회라 코드 05210 만 떴다).
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import g1_geo_lookup, transactions_service  # noqa: E402

FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BE = ROOT / "도서물류관리프로그램" / "backend" / "app"


class ScrapAxisLikeReturns(unittest.TestCase):
    def test_scrap_axis_flags(self) -> None:
        src = (FE / "components" / "transactions" / "transaction-status-screen.tsx").read_text(encoding="utf-8")
        i = src.index("export const SCRAP_STATUS_AXIS")
        block = src[i : src.index("};", i)]
        for flag in ("slimFilters: true,", "noDispatch: true,", 'docLabel: "폐기 명세서",'):
            self.assertIn(flag, block)

    def test_scrap_route_uses_etc_names(self) -> None:
        router = (BE / "routers" / "transactions.py").read_text(encoding="utf-8")
        i = router.index('axis_label="Scrap"')
        self.assertIn('name_source="etc"', router[i : i + 500])


class EtcNameResolver(unittest.IsolatedAsyncioTestCase):
    async def test_status_resolver_reads_g5_with_shared_fallback(self) -> None:
        seen: list[str] = []

        async def fake_query(server_id, sql, params=None):
            seen.append(sql)
            if "FROM G5_Ggeo" in sql:
                return [
                    {"Hcode": "", "Gcode": "05210", "Gname": "애플2"},
                    {"Hcode": "5019", "Gcode": "80001", "Gname": "애플"},
                ]
            return []

        with patch.object(g1_geo_lookup, "execute_query", AsyncMock(side_effect=fake_query)):
            name_of = await transactions_service._party_name_resolver(
                "remote_153",
                [{"hcode": "5019", "gcode": "05210"}, {"hcode": "5019", "gcode": "80001"}],
                name_source="etc",
                hcode="5019",
            )
        self.assertEqual(name_of("5019", "05210"), "애플2")  # 공용(Hcode='') 폴백
        self.assertEqual(name_of("5019", "80001"), "애플")   # 전표 Hcode 정확 일치
        self.assertTrue(all("G1_Ggeo" not in q for q in seen), "폐기 축은 G1 을 보지 않는다")
        self.assertTrue(any("(Hcode=%s AND Gcode=%s)" in q for q in seen), "Hcode 스코프 바인딩")

    def test_detail_falls_back_to_g5_when_g1_misses(self) -> None:
        src = (BE / "services" / "outbound_service.py").read_text(encoding="utf-8")
        i = src.index("cust_gname = g1_gname_for_slip(hcode, stmt_gcode, pair_map)")
        block = src[i : i + 700]
        self.assertIn("if not cust_gname and stmt_gcode:", block)
        self.assertIn("fetch_g5_etc_gnames(server_id, [(hcode, stmt_gcode)])", block)


if __name__ == "__main__":
    unittest.main()
