"""DEC-222/223 — 반품 재고 처리 띠 정합 + 일별 반품내역서 오류 안내·상세 스코프·전표번호 (2026-08-27)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import returns_service as svc  # noqa: E402


class DailyDetailScope(IsolatedAsyncioTestCase):
    async def _run(self, **kw):
        cap: list = []

        async def fake(server_id, sql, params=()):  # noqa: ARG001
            cap.append((sql, params))
            return []

        with patch.object(svc, "execute_query", side_effect=fake), \
             patch.object(svc, "in_clause_lookup", return_value=[]), \
             patch.object(svc, "s1_column_names", new=AsyncMock(return_value=kw.pop("cols", {"idnum", "jubun"}))):
            await svc.daily_report(server_id="remote_153", date_from="2026-02-20", date_to="2026-08-27", **kw)
        return next((s, p) for s, p in cap if " AS idnum" in s)

    async def test_selected_day_narrows_detail(self) -> None:
        sql, params = await self._run(hcode="5019", detail_for_hcode="5019", detail_for_gdate="2026-08-20")
        self.assertIn("AND s.Hcode=%s AND s.Gdate=%s", sql)
        self.assertEqual(tuple(params), ("2026.02.20", "2026.08.27", "5019", "2026.08.20"))
        self.assertIn("s.Idnum AS idnum", sql)
        self.assertIn("ORDER BY s.Gdate, s.Hcode, s.Idnum, s.Bcode", sql)

    async def test_without_day_keeps_range(self) -> None:
        sql, params = await self._run(hcode="5019")
        self.assertNotIn("s.Gdate=%s", sql)
        self.assertEqual(tuple(params), ("2026.02.20", "2026.08.27", "5019"))

    async def test_ddl_drift_without_idnum(self) -> None:
        sql, _ = await self._run(hcode="5019", cols={"jubun"})
        self.assertIn("SELECT 0 AS idnum", sql)
        self.assertIn("ORDER BY s.Gdate, s.Hcode, s.Jubun, s.Bcode", sql)


class DailyRouterAndFrontend(TestCase):
    def test_router_passes_gdate_only_when_given(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers" / "returns.py").read_text(encoding="utf-8")
        self.assertIn('detail_for_gdate: str | None = Query(None, alias="detailForGdate")', src)
        self.assertIn('**({"detail_for_gdate": detail_for_gdate} if detail_for_gdate else {})', src)

    def test_frontend_report_page(self) -> None:
        src = (FRONT / "app" / "(app)" / "returns" / "reports" / "page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("`오류: ${e.status}`", src, "status 0 을 오류코드처럼 보이던 배너 제거")
        self.assertIn("<ApiErrorBanner", src)
        self.assertIn("detailForGdate: eDetail ? eDetailGdate ?? undefined : undefined", src)
        self.assertIn("formatIdnumDisplay(v as number)", src, "전표번호 5자리")
        self.assertNotIn("d.grat1 * 100", src, "할인율은 저장값이 이미 %")
        self.assertIn('legacyId="Sobo55.DBGrid201"', src)
        self.assertNotIn("<table", src)
        api = (FRONT / "lib" / "returns-api.ts").read_text(encoding="utf-8")
        self.assertIn("detailForGdate", api)
        self.assertIn("{ timeout: 60000 }", api)


class ReturnsInventoryBand(TestCase):
    def test_tabs_moved_into_band_and_labels_common(self) -> None:
        src = (FRONT / "app" / "(app)" / "returns" / "inventory" / "page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("TabsList", src)
        self.assertNotIn("text-gray-600", src)
        band = src[src.index("<PageHeader"): src.index("</PageHeader>")]
        self.assertIn('legacyId="Sobo24.TabStrip"', band)  # SegmentedRadio 가 data-legacy-id 로 렌더
        # DEC-241 — 라디오그룹은 공용 SegmentedRadio 가 그린다(role="radiogroup"·방향키 이동 내장).
        self.assertIn("<SegmentedRadio", band)
        self.assertIn("function selectTab(tab: TabKey)", src)


if __name__ == "__main__":
    main()
