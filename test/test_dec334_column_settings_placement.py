"""
DEC-334 — 컬럼 설정(「표시할 컬럼」) 창: 화면 안에 다 보이게 위/아래 자동 배치 + 「전체 선택」(사용자 2026-09-25).

- 트리거 아래 공간이 패널 높이(320)보다 작고 위가 더 넓으면 위로(bottom 기준) 펼친다. 높이는 남은 공간으로 제한(목록은 안에서 스크롤).
- 목록 맨 위 「전체 선택」: 전부 표시 ↔ 첫 컬럼만 남기고 해제(최소 1개 표시 규칙), 일부 선택이면 indeterminate.
- 공용 컴포넌트 1곳 수정 — GridColumnSettings 를 쓰는 전 목록 화면에 적용(호출부 prop 변경 없음).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

SRC = (Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
       / "components" / "data-grid" / "grid-column-settings.tsx").read_text(encoding="utf-8")


class ColumnSettingsPlacement(TestCase):
    def test_flips_above_when_no_room_below(self):
        self.assertIn("const PANEL_HEIGHT = 320;", SRC)
        self.assertIn("if (below >= wanted || below >= above)", SRC)
        self.assertIn("bottom: window.innerHeight - rect.top + GAP", SRC)
        self.assertIn("maxHeight: menuPosition.maxHeight", SRC)
        self.assertIn('data-placement={menuPosition.bottom !== undefined ? "top" : "bottom"}', SRC)
        self.assertNotIn("max-h-[80vh]", SRC)  # 뷰포트 비율 상한 대신 실제 남은 공간

    def test_select_all(self):
        self.assertIn('data-slot="grid-column-select-all"', SRC)
        self.assertIn("columns.slice(1).forEach((c) => onToggle(c.key))", SRC)
        self.assertIn("allCheckRef.current.indeterminate = visibleCount > 0 && !allVisible", SRC)
        # 「전체 선택」은 목록(스크롤 영역)보다 위.
        self.assertLess(SRC.index("grid-column-select-all"), SRC.index("flex-1 space-y-1 overflow-y-auto"))


if __name__ == "__main__":
    main(verbosity=2)
