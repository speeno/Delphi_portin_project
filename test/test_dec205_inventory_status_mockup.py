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
        # DEC-316(2026-09-24 사용자 「다른 원장과 동일하게 좌우 화면」) — 목업의 단일 표 규칙을 대체: 좌 도서구분별 / 우 도서별.
        self.assertIn("<SplitListPanes", self.src)
        self.assertIn('orientation="horizontal"', self.src)
        self.assertIn('const BOOK_DEFAULT_HIDDEN = ["gsumx", "gisum", "gjqut", "gpsum", "gssum"];', self.src)
        self.assertIn('"inventory.status.book.v2"', self.src, "저장 설정이 새 기본을 덮지 않도록 키 v2")
        self.assertIn('key: "gisbn",\n    label: "ISBN"', self.src)
        # 2026-08-25 17:08 사용자: 목업의 「잔량」 대신 레거시 용어 「현재고」 유지
        self.assertIn('label: "현재고"', self.src)
        self.assertNotIn('label: "잔량"', self.src)

    def test_empty_hint_section_header_and_class_toggle(self) -> None:
        self.assertIn("<EmptyHint>거래일자와 도서명으로 검색하세요</EmptyHint>", self.src)
        self.assertEqual(self.src.count("<SectionHeader"), 2, "좌·우 각각 섹션 헤더")
        # DEC-316 — 「도서구분별 집계」 토글 제거, 좌측 머리에 「내용 전체 보기」, 조회 직후 우측 = 전 도서.
        self.assertNotIn("Sobo34.ClassView", self.src)
        self.assertIn('data-legacy-id="Sobo34.ShowAll"', self.src)
        self.assertIn("showAll || selectedClass === null", self.src)
        self.assertIn('"도서별 (전체)"', self.src)
        self.assertIn("구분 해제", self.src)

    def test_client_pagination_and_export(self) -> None:
        self.assertIn("pager={{ page: pageState, onChange: setPage }}", self.src)
        self.assertIn("toolbarTop={<DataGridPager page={pageState} onChange={setPage} />}", self.src)
        self.assertIn("bookSort.sortedRows.slice(safeOffset, safeOffset + page.limit)", self.src)
        self.assertIn("exportTableXlsx", self.src)
        self.assertIn("printTable", self.src)
        # 엑셀 컬럼 = 현재 보이는 컬럼(사용자 규칙) — 표마다(DEC-316).
        self.assertIn("const cols = which === \"class\" ? visibleClassCols : visibleBookCols;", self.src)


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
        """번호형 페이저는 표 하단 가운데, 왼쪽 «총 N 건», 오른쪽 footerRight.

        DEC-412: 프론트 재설계(M-DEC-1) 운영 반영 — 3칸 flex-1 대신 1fr·auto·1fr 격자로 가운데 정렬.
        재설계가 하단 건수를 통째로 지웠던 것은 재설계 안 한 화면(약 60곳)의 건수가 사라지는 회귀라
        되돌리고, 표 위에 건수를 따로 두는 피그마 기초관리 목록만 `hideFooterTotal` 로 끈다.
        """
        src = _read("components/data-grid/data-grid.tsx")
        i = src.index('data-slot="data-grid-footer"')
        footer = src[i : i + 1800]
        self.assertIn("grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center", footer)
        self.assertIn('<span className="flex items-center justify-center">', footer)
        self.assertIn('<DataGridPager {...pager} variant="compact" />', footer)
        self.assertIn("총 ${footerTotal.toLocaleString()} 건", footer)
        self.assertIn("const footerTotal = hideFooterTotal ? undefined : (pagerPage?.total ?? total);", src)
        self.assertIn("showBottomPager || footerRight != null || footerTotal !== undefined", src)
        self.assertIn("hideFooterTotal = false,", src, "기본은 하단 건수 표시(종전 화면 동작 유지)")


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
