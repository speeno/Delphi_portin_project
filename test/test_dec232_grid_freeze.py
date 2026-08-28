"""DEC-232 — 목록표 틀고정(지정 컬럼까지 왼쪽 고정) 전 화면 배선 (2026-08-28 사용자 요청)."""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class DataGridFreeze(TestCase):
    def test_grid_implements_sticky_left(self) -> None:
        src = (FRONT / "components" / "data-grid" / "data-grid.tsx").read_text(encoding="utf-8")
        self.assertIn("frozenUntil?: string | null;", src)
        self.assertIn("const frozenCount = useMemo(", src)
        self.assertIn("ths[i].getBoundingClientRect().width", src, "헤더 실폭 누적으로 left 산출")
        self.assertIn('"sticky z-[5] bg-inherit "', src, "본문 셀 sticky + 행 배경 승계")
        self.assertIn('(ci < frozenCount ? "z-20 "', src, "헤더/합계 셀 top+left 이중 sticky")
        self.assertIn('"border-t border-border/70 bg-card "', src, "행 기본 불투명 배경")

    def test_prefs_and_settings(self) -> None:
        hook = (FRONT / "components" / "data-grid" / "use-grid-prefs.ts").read_text(encoding="utf-8")
        self.assertIn("frozenUntil: string | null;", hook)
        self.assertIn("if (frozenUntil) prefs.frozenUntil = frozenUntil;", hook)
        self.assertIn("setFrozenUntilState(null);", hook, "전체 초기화에 포함")
        settings = (FRONT / "components" / "data-grid" / "grid-column-settings.tsx").read_text(encoding="utf-8")
        self.assertIn('data-slot="grid-freeze-select"', settings)
        self.assertIn("고정 안 함", settings)

    def test_every_grid_wired(self) -> None:
        missing_grid: list[str] = []
        missing_settings: list[str] = []
        for f in sorted(list((FRONT / "app" / "(app)").glob("**/*.tsx")) + list((FRONT / "components").glob("**/*.tsx"))):
            rel = str(f.relative_to(FRONT))
            if rel.startswith("components/data-grid/"):
                continue
            src = f.read_text(encoding="utf-8")
            for m in re.finditer(r"columnWidths=\{(\w+)\.widths\}", src):
                if f"frozenUntil={{{m.group(1)}.frozenUntil}}" not in src:
                    missing_grid.append(f"{rel}: {m.group(1)}")
            for blk in re.findall(r"<GridColumnSettings\b[\s\S]*?/>", src):
                m = re.search(r"hidden=\{(\w+)\.hidden\}", blk)
                if m and f"onFrozenChange={{{m.group(1)}.setFrozenUntil}}" not in blk:
                    missing_settings.append(f"{rel}: {m.group(1)}")
        self.assertEqual(missing_grid, [], "DataGrid 에 frozenUntil 배선 누락")
        self.assertEqual(missing_settings, [], "컬럼 설정에 틀고정 배선 누락")


if __name__ == "__main__":
    main()
