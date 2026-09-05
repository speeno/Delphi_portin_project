"""폐기 접수 — 입고/출고 접수와 동일한 입력 컨트롤·목록 방식 회귀 (DEC-193, 2026-08-24 운영 요청).

요청 원문
--------
"폐기 접수 화면의 목록을 공통 컴포넌트로 변경해줘 / 입고접수나 출고접수처럼 입력 컨트롤
및 목록 기능 및 방식이 적용되도록 한다."

검증 대상 (정적 — 프론트 소스 배선)
---------------------------------
1. 라인 목록(`ReturnLineGrid`, 반품 접수와 공용) 이 C2/C3 접수 화면과 같은 공용 부품을
   쓰는가: `MasterLookupField(book)` 인라인 자동완성 · `LocalComboField` 픽 필드 ·
   `handleGridArrowKey`(DEC-168) · `focusNextGridCell`(DEC-191) · `useGridPrefs` +
   `GridColumnSettings`(DEC-191) · 공용 목록표 토큰(list-table-card).
2. 합계 행이 **표시 중인 컬럼을 따라가는가** — 컬럼 숨김/순서 변경 시 수량·금액 합계가
   다른 칸 밑으로 밀리던 고정 colSpan 마크업이 남아 있지 않아야 한다.
3. 컬럼 기본 순서가 입고 접수 라인 표와 같은가(구분이 맨 앞).
4. 폐기 접수 페이지: 「목록」 = 폐기 현황 이동 · 출판사코드 공용 룩업(+출판사명 표기) ·
   진입 시 입력 대기 1행 · 저장 시 빈 행 제외.
5. 출판사코드는 **인라인 자동완성을 켜지 않는다** — `publisher` kind 의 인라인 조회는
   거래처(G1) 를 돌려주는데 폐기는 그 값을 `S1_Ssub.Hcode`(=출판사)로 저장하므로 축이
   다르면 안 된다(검색 팝업 `publisherList` 만 실제 출판사 목록).
6. 직접 입력한 도서코드 보충은 공용 리졸버(`resolveBookByCode`) 한 곳으로 — 자동완성과
   같은 `masters/products` 를 먼저 쓴다(교문사 remote_153 은 `masters/book/{code}` 가
   404 라 상세만 믿으면 도서명·정가가 영영 비어 있었다).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
# DEC-240 — 반품·폐기 라인 편집기는 공용 SlipLineGrid(출고·입고와 한 벌). 내부는 여기서 검증한다.
GRID = SRC / "components" / "outbound" / "order-line-grid.tsx"
WRAPPER = SRC / "components" / "returns" / "return-line-grid.tsx"
SCRAP_PAGE = SRC / "app" / "(app)" / "returns" / "scrap" / "new" / "page.tsx"
RETURN_PAGE = SRC / "app" / "(app)" / "returns" / "receipts" / "new" / "page.tsx"
RESOLVER = SRC / "lib" / "book-code-resolve.ts"


class ReturnLineGridCommonPartsTests(TestCase):
    """§1 라인 목록이 입고/출고 접수와 같은 공용 부품·규약을 쓴다."""

    def setUp(self) -> None:
        self.src = GRID.read_text(encoding="utf-8")

    def test_book_code_uses_shared_lookup_field(self) -> None:
        """도서코드 = 공용 MasterLookupField(book) 인라인 자동완성 + 검색 팝업."""
        self.assertIn('from "@/components/master/master-lookup-field"', self.src)
        self.assertIn('lookupKind="book"', self.src)
        self.assertIn("useInlineAutocomplete", self.src)
        # 선택 payload(자동완성/팝업) 양쪽 모두 도서명·ISBN·정가를 채운다.
        self.assertIn("onInlineSelect", self.src)
        self.assertIn("onSelect", self.src)

    def test_pubun_is_pick_field(self) -> None:
        """구분 = LocalComboField 픽 필드(입고 접수와 동일 키 흐름)."""
        self.assertIn("LocalComboField", self.src)
        self.assertIn("onSelectAdvance", self.src)

    def test_keyboard_conventions(self) -> None:
        """↑↓←→ 셀 이동(DEC-168) + Enter=다음 칸(DEC-191) 공용 헬퍼 배선."""
        self.assertIn("handleGridArrowKey", self.src)
        self.assertIn("focusNextCell", self.src)

    def test_column_prefs_wired(self) -> None:
        """컬럼 표시/순서/너비 계정 저장(DEC-191)."""
        self.assertIn("useGridPrefs", self.src)
        self.assertIn("GridColumnSettings", self.src)
        self.assertIn("applyOrder", self.src)

    def test_uses_shared_list_table_tokens(self) -> None:
        """표 마크업/색은 공용 목록표 토큰 — 하드코딩 gray 팔레트 금지(Design.md)."""
        # DEC-240 — 공용 그리드: 표 카드는 HScrollBox(DEC-218 가로 스크롤 힌트), 합계 행은 공용 상수.
        self.assertIn("<HScrollBox", self.src)
        self.assertIn("LIST_TABLE_FOOTER_ROW_CLASS", self.src)
        for banned in ("bg-gray-50", "text-gray-700", "border-gray-200", "text-gray-400", "bg-red-50"):
            self.assertNotIn(banned, self.src, f"하드코딩 색 잔존: {banned}")

    def test_footer_totals_follow_visible_columns(self) -> None:
        """합계 행은 visibleCols 를 map 한다 — 고정 colSpan 마크업이 남아 있으면 안 된다."""
        foot = self.src[self.src.index("<tfoot"):]
        self.assertIn("visibleCols.map", foot, "합계 행이 표시 컬럼을 따라가지 않는다")
        for banned in ("colSpan={5}", "colSpan={2}", "colSpan={3}"):
            self.assertNotIn(banned, foot, f"고정 colSpan 합계 마크업 잔존: {banned}")

    def test_default_column_order_matches_inbound(self) -> None:
        """기본 컬럼 순서 = 구분·도서코드·도서명·ISBN·수량·단가·할인율·금액·비고·상태."""
        wanted = [
            "pubun", "bcode", "bname", "isbn", "gsqut",
            "gdang", "grat1", "gssum", "gbigo", "yesno",
        ]
        # DEC-240 — 반품 축(RETURN_LINE_AXIS.columnOrder)이 표시 순서를 정한다. 도서명 컬럼 id = product_name.
        axis = self.src[self.src.index("export const RETURN_LINE_AXIS"):self.src.index("export const SCRAP_LINE_AXIS")]
        order = re.search(r"columnOrder:\s*\[([^\]]*)\]", axis).group(1)
        positions = []
        for col in wanted:
            marker = f'"{"product_name" if col == "bname" else col}"'
            idx = order.find(marker)
            self.assertNotEqual(idx, -1, f"컬럼 정의 누락: {col}")
            positions.append(idx)
        self.assertEqual(positions, sorted(positions), "기본 컬럼 순서가 입고 접수와 다르다")

    def test_typed_code_lookup_on_blur(self) -> None:
        """DEC-169 — 직접 타이핑한 도서코드는 blur 보충(도서명·ISBN·정가). 공용 그리드 onLookupBook.
        도서명·ISBN 은 행(line.product_name/isbn)에 담겨 행 삭제·재정렬에도 밀리지 않는다."""
        self.assertIn("onLookupBook", self.src)
        self.assertIn("lookupTypedBook", self.src)
        wrapper = WRAPPER.read_text(encoding="utf-8")
        self.assertIn("export default function ReturnLineGrid", wrapper)
        self.assertIn("axis={axis}", wrapper)


class ScrapReceiptPageTests(TestCase):
    """§4·5 폐기 접수 화면 — 입고/출고 접수와 동일한 헤더·목록 진입."""

    def setUp(self) -> None:
        self.src = SCRAP_PAGE.read_text(encoding="utf-8")

    def test_list_button_goes_to_scrap_status(self) -> None:
        """「목록」 = 폐기 현황(입고/출고 접수의 목록 버튼과 동일 자리·동작)."""
        # DEC-240 — 「목록」 은 공용 골격(SlipEntryLayout listHref)이 그린다.
        self.assertIn('listHref="/returns/scrap/status"', self.src)
        # 종전 router.back() 「뒤로」 는 제거.
        self.assertNotIn("router.back()", self.src)

    def test_publisher_uses_shared_lookup_without_inline(self) -> None:
        """출판사코드 = 공용 룩업(검색 팝업). 인라인 자동완성은 축이 달라 켜지 않는다."""
        self.assertIn('lookupKind="publisher"', self.src)
        self.assertIn("applyPublisherToHcode", self.src)
        self.assertNotIn("useInlineAutocomplete", self.src)
        # 확정 시 출판사명 표기(읽기 전용, 이동 대상 제외).
        self.assertIn("setHname", self.src)
        # 출판사명은 입력칸 아래 보조 텍스트(입고·출고·반품과 동형) — 입력 대상이 아니다.
        self.assertIn("{hname}({hcode})", self.src)

    def test_starts_with_one_blank_line(self) -> None:
        """진입 시 빈 표가 아니라 입력 대기 1행(입고/출고 접수 동형)."""
        self.assertIn("useState<ReturnLineInput[]>([blankLine()])", self.src)
        self.assertIn("createReturnLine", self.src)

    def test_save_drops_blank_rows(self) -> None:
        """저장은 빈 행을 제외하고 보낸다 — 대기 1행 때문에 저장이 막히면 안 된다."""
        self.assertIn("lines.filter((l) => l.bcode?.trim())", self.src)
        self.assertIn("returnLines: filled", self.src)


class BookCodeResolverTests(TestCase):
    """§6 직접 입력 도서코드 보충 = 공용 리졸버(products 우선 · book 상세 폴백)."""

    def test_resolver_prefers_products_search(self) -> None:
        src = RESOLVER.read_text(encoding="utf-8")
        products_at = src.index("mastersApi.products")
        detail_at = src.index("masterApi.bookDetail")
        self.assertLess(products_at, detail_at, "products 검색이 상세보다 먼저여야 한다")
        self.assertIn('(b.bcode ?? "").trim() === code', src, "정확 일치 bcode 로 골라야 한다")

    def test_both_receipt_pages_use_the_resolver(self) -> None:
        """반품 접수·폐기 접수가 같은 경로를 쓴다(드리프트 방지)."""
        for page in (SCRAP_PAGE, RETURN_PAGE):
            src = page.read_text(encoding="utf-8")
            self.assertIn("resolveBookByCode", src, page.name)
            self.assertNotIn("masterApi.bookDetail", src, page.name)


if __name__ == "__main__":
    main()
