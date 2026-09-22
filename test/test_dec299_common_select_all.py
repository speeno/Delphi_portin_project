"""DEC-299 — 목록표 공통 「선택」 헤더 체크박스(전 행 선택/해제) + 출고 현황 검색 줄 간소화 (2026-09-22).

원문: "출고 현황 화면에서 도서코드, 전표, 거래구분 박스는 제거해줘, 전체선택, 선택해제 버튼은 제거하고, 목록표에
선택 필드에 체크박스를 두고 전체 대상으로 선택 및 해제 기능을 수행하도록 목록표에 공통 기능을 추가해줘 (다른 화면에
전체선택 기능이 필드에 추가되는 경우, 전체선택, 선택해제 등 관련 버튼은 제거해)"

- 공통: `components/data-grid/select-column.tsx` `makeSelectColumn` — 행 체크박스 + 헤더 체크박스(전부=체크,
  일부=indeterminate, 없음=해제; 클릭 = 전부 선택 ↔ 전부 해제). DataGridColumn.header 로 헤더 칸에 그린다.
- 적용 5화면(체크박스 선택 열이 있던 전부): 현황 공용(출고·입고·신간·반품·폐기), 거래명세서, 반품 재고, 택배, 출고검증.
- 헤더 체크박스를 쓰는 화면에는 「전체선택/선택해제/전체해제」 버튼·라디오를 두지 않는다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
APP = FE / "app" / "(app)"
STATUS = FE / "components" / "transactions" / "transaction-status-screen.tsx"

SCREENS = [
    STATUS,
    APP / "transactions" / "sales-statement" / "page.tsx",
    APP / "returns" / "inventory" / "page.tsx",
    APP / "shipping" / "courier" / "page.tsx",
    APP / "transactions" / "verification" / "page.tsx",
]

# JSX 텍스트로 쓰인 버튼/라벨(주석은 제외 — 태그 사이 텍스트만).
SELECT_ALL_TEXT = re.compile(r">\s*(전체\s?선택|선택\s?해제|전체\s?해제)\s*<")


def _src(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class CommonSelectColumn(TestCase):
    def test_helper_renders_header_checkbox_with_indeterminate(self) -> None:
        src = _src(FE / "components" / "data-grid" / "select-column.tsx")
        self.assertIn("export function makeSelectColumn", src)
        self.assertIn('data-slot="data-grid-select-all"', src)
        self.assertIn("ref.current.indeterminate = indeterminate", src)
        self.assertIn("if (allOn) targets.forEach((k) => next.delete(k));", src)
        self.assertIn("else targets.forEach((k) => next.add(k));", src)

    def test_data_grid_supports_header_content(self) -> None:
        src = _src(FE / "components" / "data-grid" / "data-grid.tsx")
        self.assertIn("header?: ReactNode;", src)
        self.assertIn("{c.header !== undefined ? (", src)


class ScreensUseCommonSelectAll(TestCase):
    def test_every_checkbox_select_screen_uses_helper(self) -> None:
        for p in SCREENS:
            self.assertIn("makeSelectColumn", _src(p), p.name)

    def test_no_separate_select_all_buttons_where_helper_used(self) -> None:
        """헤더 체크박스를 쓰는 화면(현재·앞으로 모두)에는 전체선택/선택해제 버튼을 두지 않는다."""
        offenders = []
        for p in sorted(list(APP.glob("**/*.tsx")) + list((FE / "components").glob("**/*.tsx"))):
            src = _src(p)
            if "makeSelectColumn(" not in src and "makeSelectColumn<" not in src:
                continue
            m = SELECT_ALL_TEXT.search(src)
            if m:
                offenders.append(f"{p.relative_to(FE)}: {m.group(1)}")
        self.assertEqual(offenders, [], offenders)

    def test_status_screen_header_targets_filtered_rows(self) -> None:
        src = _src(STATUS)
        i = src.index("const requestSelectCol = makeSelectColumn")
        self.assertIn("rows: filteredSlips,", src[i : i + 300])
        self.assertNotIn("function selectAllFiltered", src)

    def test_courier_radios_absorbed_into_header(self) -> None:
        src = _src(APP / "shipping" / "courier" / "page.tsx")
        self.assertIn('headerLegacyId: "RadioButton4"', src)
        self.assertNotIn('data-legacy-id="RadioButton5"', src)
        md = _src(ROOT / "analysis" / "layout_mappings" / "Sobo28.md")
        self.assertIn("(흡수) 같은 헤더 체크박스 해제", md)


class OutboundStatusSlimFilters(TestCase):
    def setUp(self) -> None:
        self.src = _src(STATUS)

    def test_outbound_axis_is_slim(self) -> None:
        i = self.src.index("export const OUTBOUND_STATUS_AXIS")
        self.assertIn("slimFilters: true,", self.src[i : self.src.index("};", i)])
        # 간소화 축 = 출고(DEC-299) + 반품(DEC-302). 입고·신간·폐기는 종전 검색 줄 유지.
        self.assertEqual(self.src.count("slimFilters: true,"), 2)

    def test_bcode_jubun_and_gubun_hidden_and_not_sent(self) -> None:
        self.assertIn("{!axis.slimFilters && (\n          <>", self.src)
        self.assertIn('const eBcode = axis.slimFilters ? "" : (overrides.bcode ?? bcode);', self.src)
        self.assertIn('const eJubun = axis.slimFilters ? "" : (overrides.jubun ?? jubun);', self.src)
        gubun = self.src.index('<span className="text-xs text-muted-foreground">거래구분</span>')
        self.assertIn("{!axis.slimFilters && (", self.src[gubun - 300 : gubun])



class ReturnsStatusMatchesOutbound(TestCase):
    """DEC-302 — 반품 현황: 도서코드·전표·거래구분·바로출고 불필요, 출고·입고 현황과 같은 구성 (2026-09-22)."""

    def setUp(self) -> None:
        self.src = _src(STATUS)

    def test_returns_axis_slim_and_no_dispatch(self) -> None:
        i = self.src.index("export const RETURNS_STATUS_AXIS")
        block = self.src[i : self.src.index("};", i)]
        self.assertIn("slimFilters: true,", block)
        self.assertIn("noDispatch: true,", block)

    def test_dispatch_buttons_gated_by_show_dispatch(self) -> None:
        self.assertIn("const showDispatch = isOutbound && !axis.noDispatch;", self.src)
        for lid in ("Sobo24.BatchImmediateDispatch", "Sobo24.BatchReprint", "Sobo24.ImmediateDispatch"):
            j = self.src.index(f'data-legacy-id="{lid}"')
            gate = self.src.rfind("showDispatch", 0, j)
            self.assertNotEqual(gate, -1, lid)
            self.assertLess(j - gate, 1600, f"{lid} 는 showDispatch 조건 안에 있어야 한다")


if __name__ == "__main__":
    main()
