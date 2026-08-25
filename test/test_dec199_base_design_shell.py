"""DEC-199 — 기본 화면 디자인 1차 적용 (2026-08-25 목업): 셸 구조·토큰 회귀 가드.

목업: 최상단 전폭 흰 헤더(워드마크 · 「회사 | 사용자」 칩) / 어두운 사이드바(진회색 접기
박스, 밝은 글자) / 회색 탭 바(라임 pill 활성 탭) / 연회색 콘텐츠 캔버스 + 흰 카드.

원칙(Design.md §8): 하드코딩 HEX 금지 — 토큰만. 구조 변경은 셸 4파일로 한정, 화면 페이지는
토큰 회전으로만 영향받는다(OCP).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


def _root_block(css: str) -> str:
    i = css.index("\n:root {")
    return css[i : css.index("\n}", i)]


class TokenTests(TestCase):
    def setUp(self) -> None:
        self.css = _read("app/globals.css")
        self.root = _root_block(self.css)

    def _tok(self, name: str) -> str:
        m = re.search(rf"--{re.escape(name)}:\s*([^;]+);", self.root)
        self.assertIsNotNone(m, name)
        return m.group(1).strip()

    def test_sidebar_is_dark_with_light_text(self) -> None:
        sb = self._tok("sidebar"); fg = self._tok("sidebar-foreground")
        self.assertLess(float(re.search(r"oklch\(([\d.]+)", sb).group(1)), 0.5, "사이드바 배경은 어두운 톤")
        self.assertGreater(float(re.search(r"oklch\(([\d.]+)", fg).group(1)), 0.9, "사이드바 글자는 밝은 톤")

    def test_new_shell_tokens_defined_and_mapped(self) -> None:
        for t in ("sidebar-header", "tabbar", "tab-active", "tab-active-foreground"):
            self._tok(t)
            self.assertIn(f"--color-{t}: var(--{t});", self.css, f"@theme inline 매핑 누락: {t}")
        # 다크 블록에도 정의(미정의 fallback 방지)
        dark = self.css[self.css.index("\n.dark {"):]
        for t in ("sidebar-header", "tabbar", "tab-active"):
            self.assertIn(f"--{t}:", dark, f".dark 에 {t} 누락")

    def test_canvas_is_neutral_gray_and_card_white(self) -> None:
        self.assertIn("0.97", self._tok("background"))
        self.assertIn("oklch(1 0 0)", self._tok("card"))

    def test_active_tab_uses_vivid_lime_token_only(self) -> None:
        self.assertEqual(self._tok("tab-active"), "var(--vivid-lime)")


class ShellStructureTests(TestCase):
    def test_header_is_top_full_width(self) -> None:
        src = _read("app/(app)/layout.tsx")
        body = src[src.index("if (embed)"):]
        self.assertLess(body.index("<Header />"), body.index("<Sidebar />"), "헤더가 사이드바보다 먼저(최상단 전폭)")
        self.assertIn('className="flex h-screen flex-col overflow-hidden bg-background"', body)

    def test_header_wordmark_and_user_chip(self) -> None:
        src = _read("components/app-shell/header.tsx")
        self.assertIn('<Logo variant="wordmark"', src)
        self.assertIn("tenantLabel", src)
        self.assertIn("bg-card", src)
        # 화면 제목 표기는 탭이 대신 — 헤더 본문에서 제거
        self.assertNotIn("북이오웍스 · 도서물류 운영", src)

    def test_sidebar_has_no_light_background_assumptions(self) -> None:
        src = _read("components/app-shell/sidebar.tsx")
        for bad in ("text-muted-foreground", "text-foreground\"", "bg-muted/40", "bg-muted/30", "PanelLeft"):
            self.assertNotIn(bad, src, f"어두운 사이드바에 밝은 배경 전제 클래스 잔존: {bad}")
        self.assertIn("bg-sidebar-header", src)
        self.assertIn("ChevronsLeft", src)

    def test_tabbar_is_one_gray_row_with_lime_active_pill(self) -> None:
        toolbar = _read("components/workspace/workspace-toolbar.tsx")
        canvas = _read("components/workspace/workspace-canvas.tsx")
        self.assertIn("bg-tabbar", toolbar)
        self.assertIn("left?: ReactNode", toolbar)
        self.assertIn('<WorkspaceToolbar left={mode === "tabs" ? <TabStrip /> : null} />', canvas)
        self.assertIn("bg-tab-active font-semibold text-tab-active-foreground", canvas)
        self.assertIn("rounded-full", canvas)

    def test_no_hardcoded_hex_in_shell_tsx(self) -> None:
        for rel in ("components/app-shell/sidebar.tsx", "components/app-shell/header.tsx",
                    "components/workspace/workspace-toolbar.tsx", "components/workspace/workspace-canvas.tsx",
                    "app/(app)/layout.tsx"):
            self.assertIsNone(re.search(r"#[0-9a-fA-F]{6}\b", _read(rel)), rel)


if __name__ == "__main__":
    main()
