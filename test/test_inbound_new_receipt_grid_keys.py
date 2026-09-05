"""입고 접수 신규 — 헤더 3필드 · 라인 편집기(공용 SlipLineGrid 입고 축) 정적 가드.

2026-08-22/24 운영 요청(헤더 = 거래 일자 · 입고처 코드 · 입고처, 라인 컬럼 순서, 구분 픽 필드,
도서명 표기 전용, ↑/↓ 는 이동) 은 그대로 유효하다. DEC-239(2026-09-06) 로 라인 편집기가
페이지 안 인라인 `<table>` 에서 **출고와 같은 `SlipLineGrid` + `INBOUND_LINE_AXIS`** 로 옮겨졌으므로
검사 위치만 페이지 → 축 데이터/그리드 파일로 따라간다.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
PAGE = FRONTEND / "src" / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
OUT_PAGE = FRONTEND / "src" / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
GRID = FRONTEND / "src" / "components" / "outbound" / "order-line-grid.tsx"
LAYOUT = FRONTEND / "src" / "components" / "transactions" / "slip-entry-layout.tsx"
NAV_TS = FRONTEND / "src" / "lib" / "grid-arrow-nav.ts"


def _axis_block(src: str, name: str) -> str:
    start = src.index(f"export const {name}: SlipLineAxis = {{")
    end = src.index("};", start)
    return src[start:end]


class InboundNewReceiptHeaderTest(unittest.TestCase):
    """§1 헤더 = 거래 일자 · 입고처 코드 · 입고처(보조 텍스트)."""

    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")

    def test_header_fields(self) -> None:
        self.assertIn(">거래 일자<", self.src)
        self.assertIn(">입고처 코드<", self.src)
        # 상대명은 출고와 같은 꼴 — 입력칸 아래 「입고처명(코드)」 보조 텍스트(Edit23 id 보존).
        self.assertIn('data-legacy-id="Edit23"', self.src)
        # 종전 표기/불필요 항목 제거 — '입고 일자', 붙여쓴 '거래일자', 지사 입력칸.
        self.assertNotIn("입고 일자", self.src)
        self.assertNotIn(">거래일자<", self.src)
        self.assertNotIn('htmlFor="gjisa"', self.src)

    def test_uses_shared_skeleton_and_inbound_axis(self) -> None:
        """DEC-239 — 출고 신규와 같은 골격(SlipEntryLayout) + 같은 라인 편집기(입고 축)."""
        self.assertIn("<SlipEntryLayout", self.src)
        self.assertIn("axis={INBOUND_LINE_AXIS}", self.src)
        self.assertNotIn("<table", self.src, "인라인 라인 표는 제거됐다")
        # dfm 위젯 id 보존(DEC-028)
        for lid in ("TSobo22_new", "BitBtn35", "Panel_header", "Edit22", "DBGrid101", "BitBtn34", "Panel_memo", "MaskEdit21"):
            self.assertIn(f'"{lid}"', self.src, lid)

    def test_vendor_defaults_still_applied(self) -> None:
        """입고처 선택 → 기본 비율·구분 자동 적용(loadVendorDefaults) 은 축 데이터/콜백으로 유지."""
        self.assertIn("loadVendorDefaults", self.src)
        self.assertIn("defaultPubun={vendorPubun}", self.src)
        self.assertIn("customerRateMap={vendorRateMap}", self.src)


class InboundLineAxisTest(unittest.TestCase):
    """§2 라인 편집기 입고 축 — 컬럼 순서 · 구분 픽 목록 · 도서 확정→수량 · 키보드 이동."""

    def setUp(self) -> None:
        self.grid = GRID.read_text(encoding="utf-8")
        self.axis = _axis_block(self.grid, "INBOUND_LINE_AXIS")

    def test_line_columns_in_order(self) -> None:
        """라인 컬럼 = 구분 · 도서코드 · 도서명 · (ISBN) · 수량 · 단가 · 비율 · 금액 · 비고 (이 순서).
        2026-08-22 2차 요청으로 「구분」(Pubun)이 **맨 앞에 복원**됐다.
        """
        m = re.search(r"columnOrder:\s*\[([^\]]*)\]", self.axis)
        self.assertIsNotNone(m)
        order = [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]
        wanted = ["pubun", "bcode", "product_name", "gsqut", "gdang", "grat1", "gssum", "gbigo"]
        positions = [order.index(k) for k in wanted]
        self.assertEqual(positions, sorted(positions), f"컬럼 순서 불일치: {order}")

    def test_pubun_is_pick_field_with_inbound_options(self) -> None:
        """구분은 자유 입력이 아니라 픽 필드(LocalComboField) — 입고 축 8종 목록."""
        self.assertIn("pubunOptions: INBOUND_PUBUN_COMBO_OPTIONS", self.axis)
        self.assertIn('ariaLabel="구분"', self.grid)
        self.assertIn("options={axis.pubunOptions}", self.grid)

    def test_book_select_moves_to_qty_on_inbound(self) -> None:
        """도서 확정 후 포커스 = 수량(입고, 사용자 요청 2026-08-24) / 공급율(출고)."""
        self.assertIn('afterBookSelect: "gsqut"', self.axis)
        out = _axis_block(self.grid, "OUTBOUND_LINE_AXIS")
        self.assertIn('afterBookSelect: "grat1"', out)

    def test_bname_is_display_only(self) -> None:
        """도서명은 표기 전용 — 입력/이동 대상이 아닌 span."""
        self.assertIn('case "product_name":', self.grid)
        self.assertIn('<span className="text-muted-foreground">{line.product_name ?? ""}</span>', self.grid)

    def test_grid_arrow_nav_wired(self) -> None:
        """↑/↓/←/→ 는 셀 이동(DEC-168 공통 헬퍼) — 수량 스피너 ±1 아님."""
        self.assertIn("<tbody onKeyDown={handleGridArrowKey}>", self.grid)
        nav = NAV_TS.read_text(encoding="utf-8")
        self.assertIn("export function handleGridArrowKey", nav)

    def test_legacy_ids_on_inbound_axis(self) -> None:
        for lid in ("Sobo22.DBGrid101.PUBUN", "Sobo22.DBGrid101.BCODE", "Sobo22.DBGrid101.GRAT1", "Sobo22.DBGrid101.GDANG"):
            self.assertIn(lid, self.axis, lid)


class SharedSkeletonTest(unittest.TestCase):
    """§3 두 신규 화면이 같은 골격·같은 어휘를 쓴다."""

    def test_both_pages_use_layout_and_same_date_label(self) -> None:
        for path in (PAGE, OUT_PAGE):
            src = path.read_text(encoding="utf-8")
            self.assertIn("<SlipEntryLayout", src, path.name)
            self.assertIn(">거래 일자<", src, path.name)
            self.assertNotIn("<PageHeader", src, f"{path.name}: 띠는 골격이 그린다")
        self.assertNotIn(">주문 일자<", OUT_PAGE.read_text(encoding="utf-8"))

    def test_layout_owns_band_save_and_lines_card(self) -> None:
        src = LAYOUT.read_text(encoding="utf-8")
        self.assertIn("<PageHeader", src)
        self.assertIn('data-enter-scope=""', src)
        self.assertIn("advanceFocusOnEnter(e)", src)
        self.assertIn('className="space-y-3 rounded-2xl border border-border bg-card p-4 shadow-sm"', src)

    def test_order_line_grid_is_thin_wrapper(self) -> None:
        grid = GRID.read_text(encoding="utf-8")
        self.assertIn("export function SlipLineGrid<", grid)
        self.assertIn("export function OrderLineGrid<", grid)
        self.assertIn("axis={OUTBOUND_LINE_AXIS} {...props}", grid)


if __name__ == "__main__":
    unittest.main()
