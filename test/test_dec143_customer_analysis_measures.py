"""DEC-143 — 거래처별 판매분석 반품·판매 표기 + 거래처명 표기 회귀 가드.

2026-08-11 영업팀: "출고관련 자료만 잡힙니다. 반품수, 반품금액, 판매부수,
판매금액도 표기요청" + "거래처명도 표기 요청". 행 데이터(get_customer_sales)에는
필드가 이미 있었고 합계·화면 표기만 빠져 있었다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.routers.stats import _CUSTOMER_ANALYSIS_EXPORT_COLUMNS  # noqa: E402
from app.services import stats_service  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class AnalysisTotalsTests(IsolatedAsyncioTestCase):
    async def _run(self, **kw):
        captured: dict = {}

        async def fake_customer_sales(**kwargs):
            captured.update(kwargs)
            return {
                "rows": [
                    {"gcode": "00431", "gname": "알라딘", "goqut": 6275,
                     "gosum": 162894790, "gbqut": -251, "gbsum": -5308715,
                     "gsusu": 6024, "gssum": 157586075, "gjqut": 0, "gjsum": 0},
                ],
                "total": 1,
                "page": {"limit": 100, "offset": 0, "total": 1, "has_more": False},
            }

        with patch.object(stats_service.reports_service, "get_customer_sales",
                          new=fake_customer_sales):
            res = await stats_service.get_customer_analysis(
                server_id="srv", date_from="2026-01-01", date_to="2026-08-10", **kw,
            )
        return res, captured

    async def test_totals_include_returns_and_sales(self) -> None:
        res, _ = await self._run()
        t = res["totals"]
        self.assertEqual(t["bqut_total"], -251)
        self.assertEqual(t["bsum_total"], -5308715)
        self.assertEqual(t["sell_qut_total"], 6024)
        self.assertEqual(t["sell_sum_total"], 157586075)
        # 기존 키 하위 호환.
        self.assertEqual(t["qut_total"], 6275)

    async def test_single_gcode_filter_delegation(self) -> None:
        _, captured = await self._run(gcode_from="00431", gcode_to="")
        self.assertEqual(captured.get("gcode"), "00431",
                         "한쪽만 지정 시 단일 거래처 필터(A4 gcode)로 위임")
        self.assertIsNone(captured.get("gcode_from"))


class SourceGuards(TestCase):
    def test_export_headers(self) -> None:
        labels = [h for h, _ in _CUSTOMER_ANALYSIS_EXPORT_COLUMNS]
        for want in ("반품수량", "반품금액", "판매부수", "판매금액"):
            self.assertIn(want, labels, f"{want} 엑셀 헤더 누락 — DEC-143")

    def test_page_columns_and_cards(self) -> None:
        src = (FRONT / "app" / "(app)" / "stats" / "customer-analysis" / "page.tsx").read_text(
            encoding="utf-8"
        )
        for label in ("반품수량", "반품금액", "판매부수", "판매금액", "총 판매부수", "총 판매금액"):
            self.assertIn(label, src, f"{label} 누락 — DEC-143 회귀")

    def test_filter_bar_shows_customer_name(self) -> None:
        src = (FRONT / "components" / "stats" / "stats-filter-bar.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn("gcodeFromName", src, "거래처명 표기 회귀 — DEC-143")
        self.assertIn("gcodeToName", src)


if __name__ == "__main__":
    main()
