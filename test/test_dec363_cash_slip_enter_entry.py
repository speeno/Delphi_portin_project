"""DEC-363 — 입출금전표 거래처: 입력 줄 항상 · 마지막 칸 Enter = 저장 후 다음 줄 · 팝업 선택 시 거래처명 · 메뉴 맨 위.

요청(2026-10-01 교문사 경리부 문서 · 레거시 캡처):
「신규 데이터 입력하려고 하니 상단 "행추가" → 코드 검색하면 거래처명이 자동입력이 안 되네요.
행추가 말고 "엔터"로 행추가 및 입력 코드 정상 반영 요청합니다.」
같은 날 사용자: 「입출금 전표 메뉴를 가장 상단으로 이동해줘」.

레거시 정본 — `한국도서유통출판/출판/Subu41.pas`:
- 그리드 맨 아래에 입력 줄(`*`)이 항상 있다. `DBGrid101KeyDown` SIndexs=9(비고) Enter → `nSqry.Append`
  (그 줄 저장 + 새 줄), 새 줄 거래일자 = 직전 거래일자(`T4_Sub11NewRecord`).
- `DBGrid101KeyPress` SIndexs=1(코드) Enter → `Seek10` 1건이면 바로, 아니면 팝업 — 어느 쪽이든 코드와 거래처명을 함께 넣는다.
- `Button101Click` 끝 `DBGrid101.SetFocus` — 검색이 끝나면 그리드로.

원인(거래처명 미입력): 화면이 `MasterLookupField` 에 `onInlineSelect`(자동완성)만 주고 `onSelect`(검색 팝업)를
주지 않아, 팝업에서 고르면 `onValueChange(code)` 만 실행됐다.

런타임 없이 소스만 본다(실화면 검증은 DEC-363 본문). 사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PAGE = FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx"
REGISTRY = FRONT / "lib" / "form-registry.ts"


class CashSlipEnterEntryTest(TestCase):
    def setUp(self) -> None:
        self.page = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")

    def _code_cell(self) -> str:
        """코드 칸 MasterLookupField 블록(편집 행)."""
        end = self.page.index('inputLegacyId="Sobo41.Edit_GCODE"')
        start = self.page.rindex("<MasterLookupField", 0, end)
        return self.page[start:end]

    # ── 거래처명 반영 ────────────────────────────────────────────────
    def test_popup_selection_fills_code_and_name(self) -> None:
        cell = self._code_cell()
        self.assertIn("onSelect={(selection) => applyCustomer(selection.code, selection.name)}", cell,
                      "검색 팝업 선택 콜백이 없으면 코드만 들어오고 거래처명이 빈다")

    def test_inline_selection_still_fills_code_and_name(self) -> None:
        cell = self._code_cell()
        self.assertIn("onInlineSelect=", cell)
        # DEC-155 — 거래처 아이템의 코드는 hcode 필드.
        self.assertIn("applyCustomer(item.hcode, item.gname)", cell)

    def test_apply_customer_sets_both_fields(self) -> None:
        i = self.page.index("const applyCustomer = useCallback")
        block = self.page[i:i + 420]
        self.assertIn("gcode:", block)
        self.assertIn("gname:", block)

    # ── 입력 줄이 항상 있다 ──────────────────────────────────────────
    def test_input_row_always_exists(self) -> None:
        self.assertNotIn("setEditing(null)", self.page, "편집 상태가 비면 입력 줄이 사라진다")
        self.assertNotRegex(self.page, r"useState<\{ id: number; form: RowForm \} \| null>")
        self.assertRegex(
            self.page,
            r"useState<\{ id: number; form: RowForm \}>\(\(\) => \(\{\s*id: DRAFT_ID,",
            "처음부터 신규 입력 줄로 시작",
        )
        # 조회가 끝나면 새 입력 줄.
        self.assertIn("setEditing({ id: DRAFT_ID, form: emptyForm(opts.draftDate || eFrom) });", self.page)

    def test_add_row_button_goes_to_the_input_row(self) -> None:
        """「행 추가」는 남기되 줄을 새로 만들지 않는다 — 빈 줄이 겹치지 않게(DEC-356 #4 와 같은 처리)."""
        i = self.page.index("행 추가\n")
        block = self.page[i - 420:i]
        self.assertIn("onClick={() => setFocusTick((t) => t + 1)}", block)
        self.assertIn("disabled={loading || editingExisting}", block)

    # ── Enter ────────────────────────────────────────────────────────
    def test_enter_on_last_cell_saves(self) -> None:
        i = self.page.index("isLastEditCell(e.target as HTMLElement)")
        block = self.page[i - 200:i + 260]
        self.assertIn('e.key === "Enter"', block)
        self.assertIn("void saveEditing();", block)
        self.assertIn("advanceFocusOnEnter(e);", block, "나머지 칸은 다음 칸으로")
        # IME 조합 중 · 이미 처리된 Enter 는 건드리지 않는다.
        self.assertIn("if (e.defaultPrevented || e.nativeEvent.isComposing) return;", block)

    def test_last_cell_follows_the_row_not_a_fixed_column(self) -> None:
        """컬럼 순서를 바꾸거나 숨겨도 «줄의 마지막 입력칸»이 저장 칸이다."""
        i = self.page.index("function isLastEditCell")
        block = self.page[i:i + 520]
        self.assertIn('target.closest("tr")', block)
        self.assertIn("cells[cells.length - 1] === target", block)
        self.assertNotIn("Sobo41.Edit_GBIGO", block)

    def test_save_moves_to_next_input_row_same_date(self) -> None:
        self.assertIn("await fetchData({}, { draftDate: f.gdate, focus: true });", self.page)
        # 재조회가 실패해도 같은 값이 한 번 더 저장되지 않게 먼저 비운다.
        i = self.page.index("await fetchData({}, { draftDate: f.gdate, focus: true });")
        self.assertIn("setEditing({ id: DRAFT_ID, form: emptyForm(f.gdate) });", self.page[i - 260:i])

    def test_double_submit_guard(self) -> None:
        i = self.page.index("async function saveEditing()")
        self.assertIn("|| saving) return;", self.page[i:i + 120])

    # ── 포커스 ──────────────────────────────────────────────────────
    def test_search_moves_to_input_row_but_first_load_does_not(self) -> None:
        # DEC-381 — 검색 버튼이 공용 LedgerSearchButton(legacyId prop)으로 바뀌었다.
        i = self.page.index('legacyId="Sobo41.dxButton1"')
        self.assertIn("fetchData({}, { focus: true })", self.page[i:i + 420], "검색 버튼 → 입력 줄로")
        # 화면을 처음 열 때(자동 조회)는 스크롤 · 포커스를 뺏지 않는다.
        j = self.page.index("if (!hydrated || !user?.server_id) return;")
        self.assertIn("void fetchData({});", self.page[j:j + 120])

    def test_focus_runs_only_on_signal(self) -> None:
        self.assertIn("if (focusTick === 0) return;", self.page)
        self.assertIn("}, [focusTick]);", self.page)

    # ── 적던 내용 보호 ──────────────────────────────────────────────
    def test_row_actions_locked_while_typing(self) -> None:
        self.assertIn("const rowActionsLocked = saving || editingExisting || draftTouched;", self.page)
        self.assertEqual(self.page.count("disabled={rowActionsLocked}"), 2, "수정 · 삭제 버튼 둘 다")

    def test_untouched_input_row_shows_no_save_bar(self) -> None:
        i = self.page.index("footerRight={")
        self.assertIn("editingExisting || draftTouched ?", self.page[i:i + 120])


class SettlementMenuOrderTest(TestCase):
    """정산관리는 배치표 없이 등록 순서대로 나온다 — 입출금전표 거래처가 그룹의 첫 항목이어야 한다."""

    def setUp(self) -> None:
        self.src = REGISTRY.read_text(encoding="utf-8").replace("\r\n", "\n")

    def test_no_layout_table_for_settlement(self) -> None:
        block = re.search(r"export const SIDEBAR_LAYOUTS:[\s\S]*?=\s*\{(?P<body>[\s\S]*?)\};", self.src)
        self.assertIsNotNone(block)
        self.assertNotIn("settlement:", block.group("body"),
                         "배치표가 생기면 순서는 배치표가 정한다 — 이 가드를 배치표 기준으로 바꿀 것")

    def test_cash_slip_is_first_settlement_entry(self) -> None:
        body = self.src.split("export const FORM_REGISTRY: FormMeta[] = [", 1)[1]
        ids = []
        for blk in re.split(r"\n  \{\n", body):
            head = blk.split("\n  },")[0]
            if 'menuGroup: "settlement"' not in head:
                continue
            fid = re.search(r'id:\s*"([^"]+)"', head)
            if fid:
                ids.append(fid.group(1))
        self.assertGreaterEqual(len(ids), 5)
        self.assertEqual(ids[0], "Sobo42_cash", f"정산관리 등록 순서: {ids}")

    def test_cash_slip_registered_once(self) -> None:
        self.assertEqual(len(re.findall(r'id:\s*"Sobo42_cash"', self.src)), 1)


if __name__ == "__main__":
    main()
