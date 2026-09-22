"""DEC-303 — 전표 상세 팝업(반품 현황): 바로출고 제거 + 출판사 → 거래처명 + 머리 칸 정렬 (2026-09-22).

원문: "반품현황에서 팝업 반품 명세서 화면에서 — 팝업 명세서 「바로출고」: 불필요 / 출판사 -> 거래처명으로 변경요청:
코드번호보다 거래처명이 중요 -> 코드 출력은 거래처명 출력으로 변경, 컨트롤들의 정렬도 좀 틀리다."

- 팝업(OrderDetailDialog)은 출고 현황·반품 현황 공용. `allowDispatch`(기본 true)·`docLabel`(기본 「거래 명세서」) 신설.
  반품 현황은 축 `noDispatch`(DEC-302) → allowDispatch=false, docLabel 「반품 명세서」.
- 머리 「출판사 5019 (5019)」(로그인 회사 코드) → 「거래처명 <이름>」(상대 거래처, 코드는 툴팁) — 두 화면 공통.
- 머리 4칸 min-h-10 + items-center — 일자 입력칸과 나머지 텍스트가 같은 세로 가운데(실측 라벨 중심 y 동일).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
DIALOG = FE / "components" / "outbound" / "order-detail-dialog.tsx"
STATUS = FE / "components" / "transactions" / "transaction-status-screen.tsx"


class DetailDialog(TestCase):
    def setUp(self) -> None:
        self.src = DIALOG.read_text(encoding="utf-8")

    def test_dispatch_is_optional(self) -> None:
        self.assertIn("allowDispatch = true,", self.src)
        self.assertIn('{allowDispatch && detail && !isCancelled && detail.status !== "done" && (', self.src)

    def test_doc_label_drives_title_and_pdf(self) -> None:
        self.assertIn('docLabel = "거래 명세서",', self.src)
        self.assertIn("{docLabel} 상세</h2>", self.src)
        self.assertIn("`${docLabel} PDF`", self.src)

    def test_header_shows_customer_name_not_publisher_code(self) -> None:
        self.assertIn('<span className="shrink-0 text-muted-foreground">거래처명</span>', self.src)
        self.assertIn("{detail.customer.gname || detail.customer.gcode || \"—\"}", self.src)
        self.assertNotIn('<span className="text-muted-foreground">출판사</span>', self.src)
        self.assertNotIn("publisher_name", self.src)

    def test_header_cells_share_height_and_center(self) -> None:
        i = self.src.index('<section className="grid grid-cols-2 items-center gap-3')
        block = self.src[i : self.src.index("</section>", i)]
        self.assertEqual(block.count("min-h-10"), 4)


class StatusScreenPassesReturnsOptions(TestCase):
    def test_returns_axis_label_and_dispatch_wiring(self) -> None:
        src = STATUS.read_text(encoding="utf-8")
        i = src.index("export const RETURNS_STATUS_AXIS")
        self.assertIn('docLabel: "반품 명세서",', src[i : src.index("};", i)])
        j = src.index("<OrderDetailDialog")
        call = src[j : src.index("/>", j)]
        self.assertIn("allowDispatch={showDispatch}", call)
        self.assertIn('docLabel={axis.docLabel ?? "거래 명세서"}', call)


class PillLookupInputFillsWidth(TestCase):
    """거래처 입력창 안내 문구 「비우면 전체」가 「비우면 전」으로 잘림(사용자 캡처 2026-09-22) —
    알약 안 검색 입력은 화면별 좁은 폭(w-24 등)과 무관하게 알약 칸을 꽉 채운다."""

    def test_pill_rule_forces_full_width(self) -> None:
        css = (FE / "app" / "globals.css").read_text(encoding="utf-8")
        i = css.index('> [data-slot="local-combo-field"] [data-slot="input"] {')
        block = css[i : css.index("}", i)]
        self.assertIn("width: 100% !important;", block)


if __name__ == "__main__":
    main()
