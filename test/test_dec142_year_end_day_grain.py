"""DEC-142 — 도서별년말집계 일(day) grain + 파지→폐기 라벨 + 도서명 표기 회귀 가드.

2026-08-11 영업팀: ① 시작/종료에 "일" 추가 요청, ② "파지" 단어를 "폐기"로 모두
수정, ③ 도서 검색 선택 시 도서명도 함께 표기.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.routers.reports import _YEAR_END_EXPORT_COLUMNS  # noqa: E402
from app.services import reports_service as rpt  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class GrainKeyTests(TestCase):
    def test_day_month_year_keys(self) -> None:
        self.assertEqual(rpt._grain_key("2026.08.11", mode="day"), "2026.08.11")
        self.assertEqual(rpt._grain_key("2026.08.11", mode="month"), "2026.08")
        self.assertEqual(rpt._grain_key("2026.08.11", mode="year"), "2026")


class DayGrainAggregateTests(IsolatedAsyncioTestCase):
    async def test_day_grain_buckets_and_bounds(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            if "FROM S1_Ssub" in sql:
                return [
                    {"bcode": "B1", "gdate": "2026.08.01", "scode": "X",
                     "gubun": "출고", "pubun": "", "gsqut": 2, "gssum": 200},
                    {"bcode": "B1", "gdate": "2026.08.02", "scode": "X",
                     "gubun": "출고", "pubun": "", "gsqut": 3, "gssum": 300},
                ]
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            return [{"bcode": k, "gname": f"도서{k}"} for k in keys]

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            res = await rpt.get_year_end_book_aggregate(
                server_id="srv", hcode="5019",
                date_from="2026-08-01", date_to="2026-08-10",
                grain="day", limit=50,
            )
        self.assertEqual(res["grain"], "day")
        keys = [(r["gdate"], r["gcode"]) for r in res["rows"]]
        self.assertIn(("2026.08.01", "B1"), keys)
        self.assertIn(("2026.08.02", "B1"), keys, "일 단위 버킷 분리")
        # 일 정밀 경계 — 'YYYY.MM.DD' 는 .00/.99 래핑 없이 그대로.
        s1_params = next(p for s, p in captured if "FROM S1_Ssub" in s)
        self.assertIn("2026.08.01", s1_params)
        self.assertIn("2026.08.10", s1_params)
        self.assertNotIn("2026.08.01.00", s1_params)

    async def test_month_input_keeps_wrap(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            return []

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            await rpt.get_year_end_book_aggregate(
                server_id="srv", hcode=None,
                date_from="2026-01", date_to="2026-08", grain="month",
            )
        s1_params = next(p for s, p in captured if "FROM S1_Ssub" in s)
        self.assertIn("2026.01.00", s1_params, "월 입력은 종전 래핑 유지")
        self.assertIn("2026.08.99", s1_params)


class LabelAndSourceGuards(TestCase):
    def test_export_headers_use_pyegi(self) -> None:
        labels = [h for h, _ in _YEAR_END_EXPORT_COLUMNS]
        self.assertIn("폐기수", labels)
        self.assertIn("폐기액", labels)
        self.assertNotIn("파지수", labels, "'파지' 라벨 부활 — DEC-142 회귀")
        self.assertNotIn("파지액", labels)

    def test_page_source_guards(self) -> None:
        src = (FRONT / "app" / "(app)" / "reports" / "year-end-book" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('label: "파지수"', src, "'파지' 라벨 부활 — DEC-142 회귀")
        self.assertNotIn('label: "파지액"', src)
        self.assertIn('"year" | "month" | "day"', src)
        self.assertIn('switchGrain("day")', src)
        self.assertIn('monthOnly={grain !== "day"}', src)
        self.assertIn("bcodeFromName", src, "선택 도서명 표기 회귀")


if __name__ == "__main__":
    main()
