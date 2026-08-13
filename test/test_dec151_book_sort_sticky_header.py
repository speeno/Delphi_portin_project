"""DEC-151 — 도서 목록 전 컬럼 정렬·기본 순서·재고금액 + 전 목록 sticky 헤더 가드.

2026-08-13 사용자:
- 도서 마스터 목록 "모든 셀에 정렬" + 기본 표시 순서 확정(도서분류→도서처리→
  도서코드→도서명→저자명→ISBN→정가→재고→재고금액→서가위치→판형→위탁→쪽수→
  판수→발행일→비고), 나머지는 컬럼 설정에서 개별 선택(기본 숨김).
- (중요) 모든 목록표: 스크롤 시 헤더가 플로팅되어 컬럼명 항상 확인 가능.

구현 요점:
- 백엔드 `_book_sorts_for_columns` — 전 필드 화이트리스트를 SHOW COLUMNS 존재
  컬럼으로 필터(부재 컬럼 ORDER BY 1054 방지). 재고금액 = 파생
  (COALESCE(Gsqut,0)*COALESCE(Gdang,0)) — gsqut+gdang 존재 시에만.
- DataGrid 공통 — 카드 max-h+overflow-y-auto(내부 세로 스크롤) + th sticky
  top-0(불투명 bg) + 합계행(tfoot) sticky bottom-0.
- useGridPrefs defaultHidden — 저장 prefs 없을 때 코드 기본 숨김 적용.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import g4_book_adapt as adapt  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class BookSortWhitelistTests(TestCase):
    def test_filtered_by_existing_columns(self) -> None:
        cols = {"gcode", "gname", "sname", "gpage", "gsqut", "gdang"}
        sorts = ms._book_sorts_for_columns(cols)
        self.assertIn("sname", sorts)
        self.assertIn("gpage", sorts)
        self.assertNotIn("jego1", sorts, "부재 컬럼은 화이트리스트 제외(1054 방지)")
        self.assertEqual(
            sorts["stock_amount"], "(COALESCE(Gsqut,0)*COALESCE(Gdang,0))",
        )

    def test_stock_amount_requires_both_columns(self) -> None:
        self.assertNotIn(
            "stock_amount", ms._book_sorts_for_columns({"gcode", "gsqut"}),
        )

    def test_empty_meta_falls_back_to_legacy_seven(self) -> None:
        self.assertEqual(ms._book_sorts_for_columns(set()), ms._BOOK_SORTS)


class ListBooksOrderByTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        adapt.clear_g4_column_cache_for_tests()
        self.addCleanup(adapt.clear_g4_column_cache_for_tests)

    async def _captured_sql(self, *, cols: list[str], sort_by: str) -> str:
        captured: list[str] = []

        async def fake_adapt_exec(server_id, sql, params=()):
            return [{"Field": c} for c in cols]

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            if "COUNT(*)" in sql:
                return [{"row_count": 0}]
            return []

        with patch.object(adapt, "execute_query", fake_adapt_exec), \
                patch.object(ms, "execute_query", fake_exec):
            await ms.list_books(server_id="remote_1", sort_by=sort_by, sort_dir="desc")
        return next(s for s in captured if "COUNT(*)" not in s)

    async def test_detail_column_sort_applied_when_exists(self) -> None:
        sql = await self._captured_sql(
            cols=["Gcode", "Gname", "Sname", "Gsqut", "Gdang"], sort_by="sname",
        )
        self.assertIn("ORDER BY Sname DESC", sql)

    async def test_missing_column_sort_ignored(self) -> None:
        sql = await self._captured_sql(
            cols=["Gcode", "Gname"], sort_by="jego1",
        )
        self.assertIn("ORDER BY Gcode", sql)
        self.assertNotIn("Jego1", sql)

    async def test_stock_amount_expression_sort(self) -> None:
        sql = await self._captured_sql(
            cols=["Gcode", "Gname", "Gsqut", "Gdang"], sort_by="stock_amount",
        )
        self.assertIn("ORDER BY (COALESCE(Gsqut,0)*COALESCE(Gdang,0)) DESC", sql)


class BookPageGuard(TestCase):
    PAGE = FRONTEND / "app" / "(app)" / "master" / "book" / "page.tsx"

    def test_default_order_and_all_sortable(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        order = ["도서분류", "도서처리", "도서코드", "도서명", "저자명", "ISBN",
                 "정가", "재고", "재고금액", "서가위치", "판형", "위탁", "쪽수",
                 "판수", "발행일", "비고"]
        pos = [src.index(f'label: "{lbl}"') for lbl in order]
        self.assertEqual(pos, sorted(pos), "기본 표시 순서 = 사용자 확정 순서")
        # 전 데이터 컬럼 정렬 — sortable 미지정 데이터 컬럼 금지(NL 서지 액션 제외).
        import re
        for m in re.finditer(r'\{ key: "(\w+)"[^\n]*label: "([^"]+)"[^\n]*\}', src):
            self.assertIn("sortable: true", m.group(0), f"{m.group(2)} 정렬 누락")

    def test_stock_amount_derived_column(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn('id: "stock_amount"', src)
        self.assertIn('sortKey: "stock_amount"', src)
        self.assertIn("(row.gsqut ?? 0) * (row.gdang ?? 0)", src)

    def test_default_hidden_and_v2_key(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn('"master.book.v2"', src)
        self.assertIn("defaultHidden: BOOK_DEFAULT_HIDDEN", src)
        for k in ("jego1", "bigo1", "grat9", "price", "odang"):
            self.assertIn(f'"{k}"', src.split("BOOK_DEFAULT_HIDDEN")[1].split("]")[0])


class StickyHeaderGuard(TestCase):
    GRID = FRONTEND / "components" / "data-grid" / "data-grid.tsx"
    PREFS = FRONTEND / "components" / "data-grid" / "use-grid-prefs.ts"

    def test_card_scrolls_vertically_with_cap(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("max-h-[calc(100dvh-14rem)] overflow-y-auto", src)

    def test_header_cells_sticky_opaque(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn('"sticky top-0 z-10 bg-muted px-4 py-3', src)

    def test_totals_row_sticky_bottom(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn('"sticky bottom-0 z-10 border-t border-border bg-muted px-4', src)

    def test_grid_prefs_supports_default_hidden(self) -> None:
        src = self.PREFS.read_text(encoding="utf-8")
        self.assertIn("defaultHidden", src)
        self.assertIn("hasStored", src)
        # 전부-표시 선택 보존 — 기본 숨김 그리드는 빈 hidden 도 명시 저장.
        self.assertIn("defaultHiddenRef.current?.length", src)


if __name__ == "__main__":
    main()
