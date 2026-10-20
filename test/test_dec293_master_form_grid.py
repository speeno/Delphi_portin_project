"""DEC-293 — 거래처·입고처 등록/상세 폼 4열 균등 칸 + 주소 한 줄 + 거래처현황 신규 거래처 위치 (2026-09-22).

사용자 요청: 「신규거래처 등록 화면: 입력칸이 불규칙적인 사이즈, 불필요한 공백 → 실용적 배치(입력 정보 동일)」,
「신규거래처 버튼을 검색 입력창 앞으로」. 실측(harness, 1154px): 모든 행 우측 끝 일치, 높이 36px, 칸 280px, 라벨 112px.

DEC-412: 프론트 재설계(M-DEC-1 · M-DEC-3 · M-DEC-15) 운영 반영 — Figma 폼: 4열(lg) · 라벨 55px · 주소는
우편번호 · 주소 · 상세를 한 칸 입력(검색은 같은 칸 우측 텍스트 버튼) + 이메일과 한 줄(주소 3칸 + 이메일 1칸).
「신규 등록」은 공용 헤더의 제목 옆(검색보다 앞). 입고처 폼 배치는 DEC-269 가드(test_dec269_*)가 본다.
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
LIST = (FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx").read_text(encoding="utf-8")


class FormGrid(TestCase):
    def test_grid_is_four_equal_columns_with_uniform_labels(self) -> None:
        line = GRID[GRID.index("export const FORM_GRID"): GRID.index(";", GRID.index("export const FORM_GRID"))]
        self.assertIn("grid-cols-1", line)
        self.assertRegex(line, r"\b(lg|xl):grid-cols-4\b", "넓은 화면 4열")
        self.assertIn("[--form-label-w:", line, "라벨 폭 통일")
        self.assertIn("<div className={FORM_GRID} data-form-grid=\"\">", CUST)

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
        self.assertIn('cn("col-span-full space-y-1", className)', body, "기본 전폭 · 호출측이 칸 수 지정")
        self.assertEqual(body.count("<Input"), 1, "우편번호 · 주소 · 상세 한 칸(Figma)")
        self.assertIn("<PostcodeSearchButton", body)
        self.assertIn("data-address-field", body)

    def test_rows_fill_width_without_gaps(self) -> None:
        # 기본정보 4칸 × 3행 + (주소 3칸 + 이메일 1칸) × 2행 = 4열이 빈칸 없이 찬다.
        grid = CUST[CUST.index("<div className={FORM_GRID} data-form-grid=\"\">"): CUST.index("</section>")]
        singles = grid.count("<Field") + grid.count("<PhoneField") + grid.count("<MasterGbunSelect")
        self.assertEqual(singles, 14, "1칸 항목 12 + 이메일 2")
        self.assertEqual(grid.count("<AddressGroup"), 2)
        self.assertEqual(grid.count('className="lg:col-span-3"'), 2, "주소 3칸 + 이메일 1칸")
        self.assertNotIn("md:col-span-2", grid)
        # 비고2 는 전폭 텍스트영역.
        self.assertIn('data-legacy-id="Sobo11.Edit126"', CUST)

    def test_no_legacy_widget_lost(self) -> None:
        # 재설계 폼이 그대로 가진 레거시 위젯(값 · 의미 동일). 주소 그룹의 우편번호(Edit111) · 상세주소 id 는
        # AddressGroup 에 넘기고 한 칸 입력에 합쳐진다.
        for lid in ("Sobo11.Edit101", "Sobo11.Edit102", "Sobo11.Edit103", "Sobo11.Edit105", "Sobo11.Edit106",
                    "Sobo11.Edit107", "Sobo11.Edit108", "Sobo11.Edit109", "Sobo11.Edit110", "Sobo11.Edit132",
                    "Sobo11.Edit112", "Sobo11.Edit113", "Sobo11.Edit114", "Sobo11.Edit115",
                    "Sobo11.Edit111", "Sobo11.Edit116", "Sobo11.Ext.Add1Detail", "Sobo11.Edit129",
                    "Sobo11.Ext.Zip2", "Sobo11.Edit117", "Sobo11.Ext.Add2Detail", "Sobo11.Ext.Email2",
                    "Sobo11.Edit118", "Sobo11.Edit119", "Sobo11.Edit120", "Sobo11.Edit121", "Sobo11.Edit122",
                    "Sobo11.Edit123", "Sobo11.Edit124", "Sobo11.Edit130", "Sobo11.Edit131",
                    "Sobo11.CheckBox1", "Sobo11.Edit127", "Sobo11.CheckBox2", "Sobo11.Edit125", "Sobo11.Edit126"):
            self.assertIn(lid, CUST, lid)
        # 레거시 정본(Subu11 출판 · New 빌드): Edit127 = Name2(담당), 출판 Edit130 = Grat7(한도, DEC-408).
        self.assertIn('onChange={(v) => onChange("name2", v)}\n            legacyId="Sobo11.Edit127"', CUST)
        self.assertIn('onChange={(v) => onChange("grat7", v)} legacyId="Sobo11.Edit130"', CUST)
        # DEC-412: 프론트 재설계 M-DEC-3 — 의도적 제거(정지 사유 · 유선전화2 · 팩스2 · 휴대전화2 · 담당자 연락처 · 메모 ·
        # 계산서 구분 Pubun · 추가번호 Gnum1). 바인딩 · id 는 숨김 블록에 남기고(입고처 · 도서 폼 방식), 상세 저장은
        # 불러온 값을 그대로 다시 보낸다 — 값이 지워지지 않는다.
        i = CUST.index('<div hidden data-hidden-fields="figma-customer">')
        hidden = CUST[i: CUST.index("</div>", i)]
        for lid, key in (("Sobo11.Ext.StopReason", "stop_reason"), ("Sobo11.Ext.Tel2", "tel2"), ("Sobo11.Ext.Fax2", "fax2"),
                         ("Sobo11.Ext.Phon2", "phon2"), ("Sobo11.Ext.Contact1", "contact1"), ("Sobo11.Edit128", "pubun"),
                         ("Sobo11.Gnum1", "gnum1"), ("Sobo11.Ext.Memo", "memo")):
            self.assertIn(f'onChange("{key}", v)}} legacyId="{lid}"', hidden, lid)
        detail = (FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx").read_text(encoding="utf-8")
        for k in ("stop_reason", "tel2", "fax2", "phon2", "contact1", "memo", "pubun", "gnum1"):
            self.assertRegex(detail, rf"\b{k}: data\.{k}\b", k)


class ListNewButton(TestCase):
    def test_new_customer_button_before_search(self) -> None:
        header = (FRONT / "components" / "master" / "customer-master-list-header.tsx").read_text(encoding="utf-8")
        title = header.index("거래처 관리\n        </h1>")
        btn = header.index('data-legacy-id="Sobo11.Button101"')
        search = header.index("<MasterSearchQueryField")
        self.assertLess(title, btn, "제목 바로 옆")
        self.assertLess(btn, search, "검색 입력창 앞")
        self.assertIn("<CustomerMasterListHeader", LIST)


if __name__ == "__main__":
    main()
