"""DEC-293 — 거래처·입고처 등록/상세 폼 4열 균등 칸 + 주소 한 줄 + 거래처현황 신규 거래처 위치 (2026-09-22).

사용자 요청: 「신규거래처 등록 화면: 입력칸이 불규칙적인 사이즈, 불필요한 공백 → 실용적 배치(입력 정보 동일)」,
「신규거래처 버튼을 검색 입력창 앞으로」. 실측(harness, 1154px): 모든 행 우측 끝 일치, 높이 36px, 칸 280px, 라벨 112px.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
GRID = (FRONT / "components" / "master" / "form-grid.tsx").read_text(encoding="utf-8")
CSS = (FRONT / "app" / "globals.css").read_text(encoding="utf-8")
CUST = (FRONT / "components" / "master" / "customer-detail-form.tsx").read_text(encoding="utf-8")
INB = (FRONT / "components" / "master" / "inbound-vendor-detail-form.tsx").read_text(encoding="utf-8")
LIST = (FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx").read_text(encoding="utf-8")


class FormGrid(TestCase):
    def test_grid_is_four_equal_columns_with_uniform_labels(self) -> None:
        self.assertIn('"grid grid-cols-1 gap-x-3 gap-y-2.5 md:grid-cols-2 xl:grid-cols-4 [--form-label-w:7rem]"', GRID)

    def test_css_fills_cells_and_beats_pill_width(self) -> None:
        i = CSS.index('.attached-field-scope [data-form-grid] div:has(> [data-slot="label"]:first-child)')
        rule = CSS[i: CSS.index("}", i)]
        self.assertIn("width: 100%;", rule)
        self.assertIn("justify-self: stretch;", rule)
        # 동점 특이도 규칙(36rem·suffix 30rem)도 이기도록 알약 규칙들보다 뒤에 둔다.
        self.assertGreater(i, CSS.index("width: min(100%, 36rem);"))
        self.assertGreater(i, CSS.index("width: min(100%, 30rem);"))
        self.assertIn("width: var(--form-label-w, auto);", CSS)

    def test_address_is_one_line_group(self) -> None:
        body = GRID[GRID.index("export function AddressGroup"):GRID.index("export function FormCheckCell")]
        self.assertIn('className="col-span-full space-y-1"', body)
        self.assertIn("md:flex-nowrap", body)
        self.assertEqual(body.count("<Input"), 3, "우편번호·주소·상세주소")

    def test_rows_fill_width_without_gaps(self) -> None:
        # 4열 칸 합: 기본정보 1~2행 4칸, 3행 한도·거래정지(1)+사유(2), 주소 전폭.
        self.assertRegex(CUST, r'legacyId="Sobo11\.Ext\.StopReason"[^\n]*className="md:col-span-2"')
        self.assertRegex(INB, r'legacyId="Sobo12\.Edit129"[^\n]*className="md:col-span-2"')
        for src, lid in ((CUST, "Sobo11.Edit125"), (CUST, "Sobo11.Edit126"), (INB, "Sobo12.Edit125"), (INB, "Sobo12.Edit126")):
            self.assertRegex(src, rf'legacyId="{re.escape(lid)}"[^\n]*className="md:col-span-2"', lid)
        self.assertEqual(CUST.count('className="col-span-full space-y-1"'), 1, "메모 전폭")
        self.assertEqual(INB.count('className="col-span-full space-y-1"'), 1, "메모 전폭")

    def test_no_legacy_widget_lost(self) -> None:
        for lid in ("Sobo11.Edit101", "Sobo11.Edit102", "Sobo11.Edit103", "Sobo11.Edit105", "Sobo11.Edit106",
                    "Sobo11.Edit107", "Sobo11.Edit108", "Sobo11.Edit109", "Sobo11.Edit131", "Sobo11.CheckBox2",
                    "Sobo11.Ext.StopReason", "Sobo11.Edit111", "Sobo11.Edit116", "Sobo11.Ext.Add1Detail",
                    "Sobo11.Edit112", "Sobo11.Edit114", "Sobo11.Edit132", "Sobo11.Edit129", "Sobo11.Ext.Zip2",
                    "Sobo11.Edit117", "Sobo11.Ext.Add2Detail", "Sobo11.Ext.Tel2", "Sobo11.Ext.Fax2",
                    "Sobo11.Ext.Phon2", "Sobo11.Ext.Email2", "Sobo11.Edit118", "Sobo11.Edit124", "Sobo11.Edit127",
                    "Sobo11.Edit127.Etc", "Sobo11.CheckBox1", "Sobo11.Edit110", "Sobo11.Ext.Contact1",
                    "Sobo11.Edit125", "Sobo11.Edit128", "Sobo11.Edit130", "Sobo11.Edit126", "Sobo11.Ext.Memo"):
            self.assertIn(lid, CUST, lid)


class ListNewButton(TestCase):
    def test_new_customer_button_before_search(self) -> None:
        i = LIST.index("<PageHeader")
        band_start = LIST.index("      >\n", LIST.index("actions={", i))  # PageHeader 여는 태그 끝 = 필터 띠 시작
        btn = LIST.index('data-legacy-id="Sobo11.Button101"')
        search = LIST.index('label="검색"')
        self.assertLess(band_start, btn, "액션 줄이 아니라 필터 띠 안")
        self.assertLess(btn, search, "검색 입력창 앞")
        actions = LIST[LIST.index("actions={", i): band_start]
        self.assertNotIn("Sobo11.Button101", actions)


if __name__ == "__main__":
    main()
