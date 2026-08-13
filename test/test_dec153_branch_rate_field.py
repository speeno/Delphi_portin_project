"""DEC-153 — 지점 공급율 전용 칸(H2_Gbun.Gsum1) + 라인 공급율 실반영 가드.

2026-08-13 사용자: "지사관리에 공급율 기입 칸을 별도로 추가 + 공급율이 반영되게"
(지점명에 '75%' 기입 → 출고 라인 공급율이 거래처 비율(85) 그대로라는 보고).

설계:
- 저장소 = H2_Gbun.Gsum1 (double) — 레거시 전 빌드 참조 0건 + 라이브 전 테넌트
  비영 0행 확인한 여유 컬럼. 컬럼 부재 테넌트는 기능 자동 비활성(0/미노출).
- 반영(거래명세서): resolve_line_defaults 2.5단계 — 지사 선택 + 율>0 이면
  거래처(G1)/도서(G4) 비율을 덮어쓰고, 특가(G6)·직전거래가(4단계)는 계속 상위.
- 반영(출고접수 신규): 선택 지사 grate>0 → 라인 기본 공급율/구분별 맵 전면 대체
  + 지사 변경 시 기존 라인 일괄 갱신(수기 수정은 이후에도 가능).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import h2_gbun_adapt as h2  # noqa: E402
from app.services import masters_service as ms  # noqa: E402
from app.services import sales_statement_create_service as ssc  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

_H2_COLS = ["id", "hcode", "scode", "gcode", "gname", "oname", "jubun",
            "gdate", "gnum1", "gsum1", "gbigo"]


def _meta(cols: list[str]) -> tuple[set[str], dict[str, str]]:
    lower = {c.lower() for c in cols}
    exact = {c.lower(): c.capitalize() if c != "id" else "ID" for c in cols}
    exact["gsum1"] = "Gsum1"
    return lower, exact


class AdapterGuard(TestCase):
    def test_select_includes_grate_when_column_exists(self) -> None:
        cols, exact = _meta(_H2_COLS)
        sql = h2.branch_list_select_sql(cols, exact)
        self.assertIn("COALESCE(h.Gsum1,0) AS grate", sql)

    def test_select_zero_literal_when_column_missing(self) -> None:
        cols, exact = _meta([c for c in _H2_COLS if c != "gsum1"])
        sql = h2.branch_list_select_sql(cols, exact)
        self.assertIn("0 AS grate", sql)

    def test_row_to_api_carries_grate(self) -> None:
        row = {"id": 1, "gname": "50%", "jubun": "B2B/C", "grate": 50}
        api = h2.branch_row_to_api(row)
        self.assertEqual(api["grate"], 50.0)
        self.assertEqual(api["label"], "B2B/C|50%")


class BranchCrudGrateTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        h2.clear_h2_column_cache_for_tests()
        self.addCleanup(h2.clear_h2_column_cache_for_tests)

    async def test_create_inserts_gsum1(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_meta_exec(server_id, sql, params=()):
            if "SHOW COLUMNS" in sql:
                return [{"Field": c if c != "gsum1" else "Gsum1"} for c in _H2_COLS]
            if "MAX" in sql:
                return [{"nid": 7}]
            return []

        async def fake_tx(server_id, statements):
            captured.extend(statements)
            return [1]

        with patch.object(h2, "execute_query", fake_meta_exec), \
                patch.object(ms, "execute_query", fake_meta_exec), \
                patch.object(ms, "execute_in_transaction", fake_tx):
            await ms.create_customer_branch(
                server_id="remote_1", gcode="0010",
                payload={"gname": "50%", "jubun": "B2B/C", "grate": 50},
                scope_hcode="5097",
            )
        sql, params = captured[0]
        self.assertIn("Gsum1", sql)
        self.assertIn(50.0, params)

    async def test_update_sets_gsum1_numeric(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_meta_exec(server_id, sql, params=()):
            if "SHOW COLUMNS" in sql:
                return [{"Field": c if c != "gsum1" else "Gsum1"} for c in _H2_COLS]
            return []

        async def fake_tx(server_id, statements):
            captured.extend(statements)
            return [1]

        with patch.object(h2, "execute_query", fake_meta_exec), \
                patch.object(ms, "execute_query", fake_meta_exec), \
                patch.object(ms, "execute_in_transaction", fake_tx):
            res = await ms.update_customer_branch(
                server_id="remote_1", gcode="0010", branch_id=12475,
                payload={"grate": 75}, scope_hcode="5097",
            )
        self.assertIn("grate", res["updated_fields"])
        sql, params = captured[0]
        self.assertIn("Gsum1=%s", sql)
        self.assertIn(75.0, params)


class ResolveLineDefaultsBranchRateTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        h2.clear_h2_column_cache_for_tests()
        self.addCleanup(h2.clear_h2_column_cache_for_tests)

    def _fake_exec(self, *, branch_rate, g6_rows=None):
        async def fake(server_id, sql, params=()):
            if "SHOW COLUMNS" in sql:
                return [{"Field": c if c != "gsum1" else "Gsum1"} for c in _H2_COLS]
            if "FROM G1_Ggeo" in sql:
                return [{"grat1": 85, "grat2": 0, "grat3": 0, "grat4": 0,
                         "grat5": 0, "grat6": 0, "grat7": 0}]
            if "FROM G4_Book" in sql:
                return [{"gname": "고급영양학", "gjeja": "", "gdang": 30000,
                         "grat1": 0, "grat2": 0, "grat3": 0, "grat4": 0,
                         "grat5": 0, "grat6": 0, "grat7": 0}]
            if "FROM H2_Gbun" in sql:
                return [{"grate": branch_rate}]
            if "FROM G6_Ggeo" in sql:
                return g6_rows or []
            if "G7_Ggeo" in sql or "Chek3" in sql:
                return []
            return []
        return fake

    async def _resolve(self, *, gjisa, branch_rate, g6_rows=None):
        with patch.object(ssc, "execute_query", self._fake_exec(branch_rate=branch_rate, g6_rows=g6_rows)), \
                patch.object(h2, "execute_query", self._fake_exec(branch_rate=branch_rate)), \
                patch.object(ssc, "load_price_reuse_config",
                             side_effect=None, create=True) as cfg:
            cfg.side_effect = None
            async def _cfg(server_id, hcode):
                return {"mode": "", "jisa_keyed": False}
            cfg.side_effect = _cfg
            return await ssc.resolve_line_defaults(
                "remote_1", company_hcode="5019", customer="00001",
                bcode="3411", pubun="위탁", gjisa=gjisa,
            )

    async def test_branch_rate_overrides_customer_rate(self) -> None:
        out = await self._resolve(gjisa="75%", branch_rate=75)
        self.assertEqual(out["grat1"], 75.0, "지점율 75 가 거래처 위탁 85 를 대체")
        self.assertEqual(out["source"], "H2_Gbun:branch")

    async def test_zero_branch_rate_keeps_chain(self) -> None:
        out = await self._resolve(gjisa="부곡리(매장)", branch_rate=0)
        self.assertEqual(out["grat1"], 85, "율 미지정 지점은 기존 체인(G1) 유지")

    async def test_special_price_still_wins(self) -> None:
        out = await self._resolve(
            gjisa="75%", branch_rate=75,
            g6_rows=[{"grat1": 60, "gssum": 25000}],
        )
        self.assertEqual(out["grat1"], 60, "특가(G6)는 지점율보다 상위")
        self.assertEqual(out["source"], "G6_Ggeo")

    async def test_no_gjisa_skips_branch_lookup(self) -> None:
        out = await self._resolve(gjisa="", branch_rate=75)
        self.assertEqual(out["grat1"], 85)


class ScreenGuard(TestCase):
    def test_branch_panel_has_rate_field_and_column(self) -> None:
        src = (FRONTEND / "components" / "master" / "customer-branch-panel.tsx"
               ).read_text(encoding="utf-8")
        self.assertIn('label: "공급율(%)"', src)
        self.assertIn('htmlFor="branch-grate"', src)
        self.assertIn('placeholder="비우면 거래처 비율 사용"', src)

    def test_outbound_new_applies_branch_rate(self) -> None:
        src = (FRONTEND / "app" / "(app)" / "outbound" / "orders" / "new"
               / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("const branchRate = useMemo", src)
        self.assertIn("branchRate > 0 ? branchRate : defaultRate", src)
        self.assertIn("defaultRate={effectiveRate}", src)
        self.assertIn("customerRateMap={effectiveRateMap}", src)
        self.assertIn("grat1: branchRate", src, "지사 변경 시 기존 라인 일괄 갱신")


if __name__ == "__main__":
    main()
