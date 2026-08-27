"""DEC-229 — 제목 옆 메뉴 계층 경로 전 화면 자동 표시 (2026-08-27 사용자 요청)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class MenuTrailWiring(TestCase):
    def test_resolver_uses_registry_single_source(self) -> None:
        src = (FRONT / "lib" / "menu-trail.ts").read_text(encoding="utf-8")
        self.assertIn("export function resolveMenuTrail(pathname: string, search = \"\")", src)
        self.assertIn("import { FORM_REGISTRY, MENU_GROUPS, SIDEBAR_LAYOUTS", src)
        for tail in ('"신규 등록"', '"상세"', '"인쇄"'):
            self.assertIn(tail, src)

    def test_page_header_renders_trail_at_60_percent(self) -> None:
        src = (FRONT / "components" / "shared" / "page-header.tsx").read_text(encoding="utf-8")
        self.assertIn('"use client"', src)
        self.assertIn('data-slot="menu-trail"', src)
        self.assertIn("text-xs leading-tight text-muted-foreground", src, "제목 text-xl(20px)의 60% ≈ 12px")
        self.assertIn("trail?: false | MenuTrailCrumb[];", src)
        self.assertIn("{crumbs && crumbs.length > 0 && <MenuTrail crumbs={crumbs} />}", src)
        # 제목 바로 옆(같은 행)에 온다
        self.assertLess(src.index("</h1>"), src.index("<MenuTrail crumbs={crumbs} />"))
        self.assertLess(src.index("<MenuTrail crumbs={crumbs} />"), src.index("{titleAside}"))


if __name__ == "__main__":
    main()
