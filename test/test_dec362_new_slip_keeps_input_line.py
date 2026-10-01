"""DEC-362 — 신규 전표 입력(출고·입고·반품): 마지막 줄을 지워도 빈 입력 줄 1개가 남는다.

배경(2026-10-01 교문사): 신규 출고 접수에서 품절 도서 줄을 지운 뒤 같은 화면에서 새 거래처를 입력하면
지사에서 Enter 가 넘어가지 않았다. 지사 Enter 는 첫 줄 「구분」 칸으로 포커스를 옮기는데, 줄이 0개라
옮길 칸이 없었다(「라인이 없습니다」 상태).
"""
from __future__ import annotations

import unittest
from pathlib import Path

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
GRID = FE / "components/outbound/order-line-grid.tsx"
OUT_NEW = FE / "app/(app)/outbound/orders/new/page.tsx"
NEW_PAGES = [
    OUT_NEW,
    FE / "app/(app)/inbound/receipts/new/page.tsx",
    FE / "app/(app)/returns/receipts/new/page.tsx",
]


class NewSlipKeepsInputLine(unittest.TestCase):
    def test_grid_remove_leaves_blank_line_when_opted_in(self) -> None:
        src = GRID.read_text(encoding="utf-8")
        self.assertIn("keepInputLine?: boolean;", src)
        self.assertIn("keepInputLine = false,", src)  # 기본은 종전 동작(상세·수정 화면은 0줄 허용)
        fn = src[src.index("function remove(idx: number)"):]
        fn = fn[: fn.index("\n  }\n")]
        self.assertIn("next.length === 0 && keepInputLine ? [newLine()] : next", fn)

    def test_all_new_entry_pages_opt_in(self) -> None:
        for p in NEW_PAGES:
            self.assertIn("keepInputLine", p.read_text(encoding="utf-8"), str(p))

    def test_outbound_branch_enter_never_dead_ends(self) -> None:
        """줄이 없어도(방어) 줄을 만들고 「구분」으로 간다 — 포커스가 지사에 갇히지 않는다."""
        src = OUT_NEW.read_text(encoding="utf-8")
        fn = src[src.index("function focusFirstPubunEl()"):]
        fn = fn[: fn.index("\n  }\n")]
        self.assertIn("setLines((ls) => (ls.length ? ls : [newDraftLine(effectiveRate)]));", fn)
        self.assertIn("requestAnimationFrame", fn)

    def test_blank_lines_follow_new_customer_rate(self) -> None:
        """남긴 빈 줄에 앞 거래처 공급율이 보이지 않게 — 도서가 없는 줄만 새 거래처 값으로."""
        src = OUT_NEW.read_text(encoding="utf-8")
        self.assertIn('if ((l.bcode ?? "").trim()) return l;', src)
        self.assertIn("}, [effectiveRate, effectiveRateMap]);", src)


if __name__ == "__main__":
    unittest.main()
