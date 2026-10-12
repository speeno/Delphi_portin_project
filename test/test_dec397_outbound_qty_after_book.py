"""DEC-397 — 출고 줄 수량: 새 줄은 빈칸, 도서를 고른 뒤 1.

요청(교문사 2026-10-12): 「출고명세서 작성 중 다음 라인으로 엔터를 하면 수량에 1 이 표기되어 있다. 도서 검색 후 1 이 생성되게」.

가드
----
- 출고 축(`OUTBOUND_LINE_AXIS`) 새 줄 수량 0 + `qtyOnBook: 1`, 도서 선택(목록 · 인라인) · 직접 친 코드 확정(blur) 때 수량이 비어 있으면 1.
- 도서 없는 빈 수량은 0 대신 빈칸으로 보인다. 먼저 쳐 둔 수량은 덮지 않는다.
- 출고 접수 첫 줄 · 거래명세서 수정 대화상자 새 줄도 같은 규칙. 입고 · 반품/폐기 축 기본값은 그대로(DEC-380).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
GRID = FE / "components" / "outbound" / "order-line-grid.tsx"
NEW_PAGE = FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
DIALOG = FE / "components" / "transactions" / "sales-statement-edit-dialog.tsx"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def _axis(src: str, name: str) -> str:
    return src.split(f"export const {name}: SlipLineAxis = {{", 1)[1].split("\n};", 1)[0]


class OutboundAxis(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read(GRID)

    def test_new_line_blank_then_one_after_book(self) -> None:
        out = _axis(self.src, "OUTBOUND_LINE_AXIS")
        self.assertIn("newLine: { gsqut: 0 },", out)
        self.assertIn("qtyOnBook: 1,", out)

    def test_other_axes_unchanged(self) -> None:
        self.assertIn("newLine: { gsqut: 1 },", _axis(self.src, "INBOUND_LINE_AXIS"))
        self.assertNotIn("qtyOnBook", _axis(self.src, "INBOUND_LINE_AXIS"))
        self.assertIn("newLine: { gsqut: -1, grat1: RETURN_GRAT1_DEFAULT },", _axis(self.src, "RETURN_LINE_AXIS"))

    def test_book_selection_paths_fill_qty_only_when_empty(self) -> None:
        self.assertIn("return axis.qtyOnBook && !Number(cur?.gsqut) ? { gsqut: axis.qtyOnBook } : {};", self.src)
        # 목록 선택 · 인라인 선택 둘 다
        self.assertEqual(len(re.findall(r"\.\.\.qtyAfterBook\(lines\[idx\]\)", self.src)), 2)
        # 직접 친 코드(blur) — 목록 선택 직후의 blur 는 건너뛰고(선택이 이미 채움), 최신 라인 기준으로
        body = self.src.split("async function lookupTypedBook(idx: number) {", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("if (!pickedRef.current[idx] && (typed?.bcode ?? \"\").trim()", body)
        self.assertLess(body.index("setAt(idx, qtyAfterBook(typed), linesRef.current)"), body.index("if (!onLookupBook || pickedRef.current[idx]) return;"))

    def test_blank_qty_shows_empty_until_book(self) -> None:
        self.assertIn('value={axis.qtyOnBook && !Number(line.gsqut) && !(line.bcode ?? "").trim() ? "" : line.gsqut}', self.src)


class OtherEntryPoints(unittest.TestCase):
    def test_outbound_new_first_line(self) -> None:
        src = _read(NEW_PAGE)
        body = src.split("function newDraftLine(", 1)[1].split("\n}", 1)[0]
        self.assertIn("gsqut: 0,", body)

    def test_statement_edit_dialog(self) -> None:
        src = _read(DIALOG)
        body = src.split('function newLine(pubun = "위탁"): DraftLine {', 1)[1].split("\n}", 1)[0]
        self.assertIn("gsqut: 0,", body)
        self.assertIn("const qty = Number(linesRef.current[idx]?.gsqut) ? {} : { gsqut: 1 };", src)
        self.assertIn('patchLine(idx, { bcode, product_name: productName, gisbn: isbn ?? "", ...qty });', src)
        self.assertIn('value={!Number(line.gsqut) && !line.bcode.trim() ? "" : line.gsqut}', src)


if __name__ == "__main__":
    unittest.main()
