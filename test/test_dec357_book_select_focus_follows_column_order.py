"""DEC-357 — 출고접수: 도서 확정 후 포커스는 수량·공급율 중 표시 순서상 먼저 오는 칸.

사용자가 컬럼 설정으로 「수량」을 공급율 앞에 두면 종전엔 축 기본(출고=공급율) 고정이라
수량(기본 1)을 건너뛰었다(2026-10-01 교문사 경리부 보고).
"""
from __future__ import annotations

import unittest
from pathlib import Path

GRID = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램/frontend/src/components/outbound/order-line-grid.tsx"
)


class TestBookSelectFocusFollowsColumnOrder(unittest.TestCase):
    def setUp(self) -> None:
        src = GRID.read_text(encoding="utf-8")
        start = src.index("function afterBookSelect(idx: number)")
        self.fn = src[start : src.index("\n  }\n", start)]

    def test_uses_visible_column_order(self) -> None:
        self.assertIn("visibleCols.map((c) => c.id)", self.fn)
        self.assertIn('indexOf("gsqut")', self.fn)
        self.assertIn('indexOf("grat1")', self.fn)
        self.assertIn('qi < ri ? "gsqut" : "grat1"', self.fn)

    def test_axis_default_only_as_fallback(self) -> None:
        # 축 기본값은 둘 다 숨김일 때만 쓴다 — 무조건 분기 금지.
        self.assertNotIn('if (axis.afterBookSelect === "gsqut") setFocusQtyIdx(idx);', self.fn)
        self.assertIn("qi < 0 && ri < 0 ? axis.afterBookSelect", self.fn)


if __name__ == "__main__":
    unittest.main()
