"""
목록·통계 화면 페이징 UI 가 공통 표 영역 상단에 오도록 하는 정적 회귀 가드.

정책 (CMS 스타일 정렬 플랜):
  - `<DataGridPager` 가 파일 내에서 해당 화면의 첫 `<table` 또는 첫 `<DataGrid` 보다 *앞에* 오거나,
  - `DataGrid` 의 `toolbarTop={ ... <DataGridPager ... /> ...}` 패턴으로 표 카드 위에 붙인 경우.

사용:
  python3 -m pytest test/test_list_top_pager_order.py -v
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
APP_PAGES = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"

# 예외적으로 순서 검사에서 제외할 상대 경로 (POSIX). 현재 없음.
ALLOWLIST: set[str] = set()


def _posix_rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


class ListTopPagerOrder(TestCase):
    def test_app_pages_with_datagrid_pager_place_pager_above_grid_or_toolbar(self):
        pages = sorted(APP_PAGES.rglob("page.tsx"))
        self.assertTrue(pages, "expected app (app) page.tsx files")

        toolbar_rx = re.compile(r"toolbarTop\s*=\s*\{[\s\S]*?<DataGridPager\b", re.MULTILINE)
        # `<DataGrid` 로 시작하지만 `DataGridPager` 는 제외 (find("<DataGrid") 오탐 방지)
        datagrid_open_rx = re.compile(r"<DataGrid(?:<|\s|>)")

        failures: list[str] = []
        for page in pages:
            rel = _posix_rel(page)
            src = page.read_text(encoding="utf-8")
            if "<DataGridPager" not in src:
                continue
            if rel in ALLOWLIST:
                continue

            if toolbar_rx.search(src):
                continue

            pi = src.find("<DataGridPager")
            ti = src.find("<table")
            m_grid = datagrid_open_rx.search(src)
            gi = m_grid.start() if m_grid else -1

            candidates = [idx for idx in (ti, gi) if idx >= 0]
            if not candidates:
                failures.append(f"{rel}: has DataGridPager but no <table / <DataGrid")
                continue
            first_grid = min(candidates)

            if pi >= first_grid:
                failures.append(
                    f"{rel}: DataGridPager at {pi} should be before first table/grid at {first_grid}",
                )

        self.assertEqual(
            failures,
            [],
            "pager must appear above first table/DataGrid or use toolbarTop={...DataGridPager...}:\n"
            + "\n".join(failures),
        )


if __name__ == "__main__":
    main(verbosity=2)
