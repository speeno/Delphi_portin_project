"""DEC-404 — 출고 접수: 줄의 도서를 **다른 도서로 바꾸면** 수량 리셋 · 거래처를 바꾸면 앞 거래처 도서 줄 비우기 물음 (2026-10-15 교문사).

신고 원문
--------
1. "출고 시 가끔 출고불가한 도서가 발견되면 해당 라인에 도서명을 새로 입력해야 하는 경우가 있습니다.
   «도서코드: 도서명 입력» → «수량입력» → 공급율 불일치로 출고 불가 → 같은 칸에 «다른 도서명 입력» →
   수량이 리셋되어야 하는데 기존 입력한 수량이 그대로 남아있습니다."
2. "거래처 입력 → 첫줄에 도서명 입력: 출고 불가 → 저장되지 않았음으로 신규 거래처명을 다시 입력하면
   앞에 입력한 도서명이 리셋되어야 하는데 그대로 남아있네요."

결정
----
- 줄: 이미 도서가 있던 줄(도서명 있음)을 다른 도서로 확정하면 수량 = `qtyOnBook`(1). 앞 도서는 코드를 고쳐 쓰기
  시작할 때 `replacingBcode` 로 적어 둔다(타이핑으로 도서명이 비워진 뒤에도 남는다). 같은 도서 재선택·도서 없던
  줄에 먼저 쳐 둔 수량(DEC-397)은 그대로. 거래명세서 수정 대화상자도 같은 규칙.
- 헤더: 확정했던 거래처와 **다른** 거래처를 확정했는데 도서 줄이 남아 있으면 「비우고 새로 입력」(Enter) / 「줄 유지」
  를 묻는다 — 거래처를 잘못 골라 고치는 사람의 줄을 말없이 지우지 않는다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import unittest
from pathlib import Path

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
GRID = FE / "components" / "outbound" / "order-line-grid.tsx"
DIALOG = FE / "components" / "transactions" / "sales-statement-edit-dialog.tsx"
NEW_PAGE = FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
CONFIRM = FE / "components" / "shared" / "confirm-dialog.tsx"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


class LineBookReplaceResetsQty(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read(GRID)

    def test_draft_line_carries_replacing_marker(self) -> None:
        self.assertIn("replacingBcode?: string;", self.src)

    def test_qty_after_book_knows_next_code_and_resets_on_replace(self) -> None:
        body = self.src.split("function qtyAfterBook(", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("cur: DraftLine | undefined, nextCode: string", body)
        self.assertIn("const replaced = !!prevCode && prevCode !== nextCode.trim();", body)
        self.assertIn("return replaced || !Number(cur?.gsqut) ? { ...clear, gsqut: axis.qtyOnBook } : clear;", body)
        # 앞 도서 = 적어 둔 표식 또는(타이핑 없이 팝업) 현재 확정 도서
        self.assertIn('(cur?.replacingBcode ?? "").trim() ||', body)
        self.assertIn('((cur?.product_name ?? "").trim() ? (cur?.bcode ?? "").trim() : "")', body)

    def test_all_three_confirm_paths_pass_next_code(self) -> None:
        self.assertIn("...qtyAfterBook(lines[idx], selection.code)", self.src)
        self.assertIn('...qtyAfterBook(lines[idx], b.bcode ?? "")', self.src)
        self.assertIn("const qtyPatch = typedCode ? qtyAfterBook(typed, typedCode) : {};", self.src)

    def test_editing_code_of_confirmed_line_records_previous_book(self) -> None:
        self.assertIn('((line.product_name ?? "").trim() && (line.bcode ?? "").trim() ? (line.bcode ?? "").trim() : "")', self.src)
        self.assertIn('{ bcode: next, product_name: "", isbn: "", ...(replacing ? { replacingBcode: replacing } : {}) }', self.src)


class StatementDialogSameRule(unittest.TestCase):
    def test_dialog_resets_qty_when_book_replaced(self) -> None:
        src = _read(DIALOG)
        self.assertIn("replacingBcode?: string;", src)
        self.assertIn("const replaced = !!prevCode && prevCode !== bcode;", src)
        self.assertIn("const qty = replaced || !Number(cur?.gsqut) ? { gsqut: 1 } : {};", src)
        self.assertIn('replacingBcode: "", ...qty', src)
        self.assertIn("? { replacingBcode: line.bcode }", src)


class CustomerSwitchPrompt(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read(NEW_PAGE)

    def test_remembers_last_confirmed_customer_independently_of_typing(self) -> None:
        self.assertIn('const lastConfirmedCustomerRef = useRef("");', self.src)
        # 두 확정 경로(팝업 · 인라인) 모두 기록
        self.assertIn("noteCustomerConfirmed(code, selection.name);", self.src)
        self.assertIn("noteCustomerConfirmed(code, c.gname);", self.src)
        # 저장 후 초기화되면 기억도 비운다
        self.assertIn('lastConfirmedCustomerRef.current = "";', self.src)

    def test_prompt_only_when_customer_changed_and_lines_have_books(self) -> None:
        body = self.src.split("function noteCustomerConfirmed(", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("if (!prev || !code || prev === code) return;", body)
        self.assertIn('const count = lines.filter((l) => (l.bcode ?? "").trim()).length;', body)
        self.assertIn("if (count > 0) setCustomerSwitchPrompt({ name, count });", body)

    def test_dialog_defaults_to_clear_and_keeps_option(self) -> None:
        self.assertIn('confirmLabel="비우고 새로 입력"', self.src)
        self.assertIn('cancelLabel="줄 유지"', self.src)
        self.assertIn("autoFocusConfirm", self.src)
        self.assertIn("onConfirm={resetLinesForNewCustomer}", self.src)
        body = self.src.split("function resetLinesForNewCustomer(", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("setLines([newDraftLine(effectiveRate)]);", body)
        self.assertIn("setSelectedLineIdx(0);", body)

    def test_confirm_dialog_supports_autofocus(self) -> None:
        src = _read(CONFIRM)
        self.assertIn("autoFocusConfirm?: boolean;", src)
        self.assertIn("autoFocus={autoFocusConfirm}", src)


if __name__ == "__main__":
    unittest.main()
