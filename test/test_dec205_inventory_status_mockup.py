"""DEC-205 — 재고현황 목업: 도서 단위 단일 표 + 번호형 페이저 (2026-08-25 15:06~15:07).

- 기본 = 도서 단위 단일 표(도서코드·도서명·ISBN·정가·입고·출고·반품·폐기·잔량), 「분류별 집계」 체크로
  분류 롤업(2026-08-22 분류→도서 흐름은 분류 행 클릭으로 유지).
- 하단 가운데 번호형 페이저(현재 페이지 라임 원) — DataGridPager compact 변형, 모든 표 공통.
- 도서 행 ISBN 은 백엔드 attach_book_meta 로 부착(실패 무시).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class InventoryStatusScreen(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/inventory/status/page.tsx")

    def test_default_single_book_table_with_mockup_columns(self) -> None:
        self.assertNotIn("<SplitListPanes", self.src, "2단 분할 대신 단일 표")
        self.assertIn('const BOOK_DEFAULT_HIDDEN = ["gsumx", "gisum", "gjqut", "gpsum", "gssum"];', self.src)
        self.assertIn('"inventory.status.book.v2"', self.src, "저장 설정이 새 기본을 덮지 않도록 키 v2")
        self.assertIn('key: "gisbn",\n    label: "ISBN"', self.src)
        # 2026-08-25 17:08 사용자: 목업의 「잔량」 대신 레거시 용어 「현재고」 유지
        self.assertIn('label: "현재고"', self.src)
        self.assertNotIn('label: "잔량"', self.src)

    def test_empty_hint_section_header_and_class_toggle(self) -> None:
        self.assertIn("<EmptyHint>거래일자와 도서명으로 검색하세요</EmptyHint>", self.src)
        self.assertIn("<SectionHeader", self.src)
        self.assertIn('data-legacy-id="Sobo34.ClassView"', self.src)
        self.assertIn("분류별 집계", self.src)
        # 도서 1종 → 「도서명 코드」, 분류 선택 → 「분류 · 이름」, 아니면 「전체 기간」
        self.assertIn('data && data.by_book.length === 1 ? data.by_book[0] : null', self.src)
        self.assertIn('"전체 기간"', self.src)
        # 분류 행 클릭 → 그 분류 도서 표로
        self.assertIn("setSelectedClass(r.class_code);\n              setClassView(false);", self.src)

    def test_client_pagination_and_export(self) -> None:
        self.assertIn("pager={{ page: pageState, onChange: setPage }}", self.src)
        self.assertIn("toolbarTop={<DataGridPager page={pageState} onChange={setPage} />}", self.src)
        self.assertIn("bookSort.sortedRows.slice(safeOffset, safeOffset + page.limit)", self.src)
        self.assertIn("exportTableXlsx", self.src)
        self.assertIn("printTable", self.src)
        # 엑셀 컬럼 = 현재 보이는 컬럼(사용자 규칙)
        self.assertIn("const exportColumns = viewCols.map(", self.src)


class NumberedPager(TestCase):
    def test_compact_variant_is_numbered_with_lime_current(self) -> None:
        src = _read("components/data-grid/data-grid-pager.tsx")
        i = src.index('if (variant === "compact")')
        block = src[i : i + 3500]
        self.assertIn('data-slot="data-grid-pager"', block)
        self.assertIn('aria-label="첫 페이지"', block)
        self.assertIn('aria-label="마지막 페이지"', block)
        self.assertIn("bg-nav-active font-semibold text-nav-active-foreground", block, "현재 페이지 라임 원")
        self.assertIn('aria-current={p === currentPage ? "page" : undefined}', block)
        self.assertNotIn(">\n          이전\n", block)

    def test_data_grid_footer_centers_pager(self) -> None:
        src = _read("components/data-grid/data-grid.tsx")
        self.assertIn('<span className="flex flex-1 items-center justify-center">', src)
        self.assertIn('<DataGridPager {...pager} variant="compact" />', src)


class BackendIsbn(TestCase):
    def test_stock_ledger_attaches_isbn_best_effort(self) -> None:
        src = (BACK / "services" / "inventory_service.py").read_text(encoding="utf-8")
        i = src.index("async def get_stock_ledger(")
        body = src[i : i + 12000]
        self.assertIn('await attach_book_meta(server_id, norm_hcode or "", by_book, bcode_key="bcode", price_key=None, isbn_key="gisbn")', body)
        self.assertIn("ISBN 부착 실패", body)
        api = _read("lib/inquiry-api.ts")
        j = api.index("export interface StockLedgerRow {")
        self.assertIn("gisbn?: string;", api[j : api.index("}", j)])


if __name__ == "__main__":
    main()
