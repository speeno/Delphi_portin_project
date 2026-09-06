"""테마 텍스트 가독성 가드 — themes.css 전 테마 WCAG AA(4.5:1) 강제.

배경: 계정별 컬러 테마 10종에서 보조 텍스트/링크/버튼 텍스트 등 36곳이
4.5:1 미달로 가독성 저하 보고(2026-07-04). 색조는 유지하고 명도만 교정했다.
본 가드는 테마 추가/수정 시 대비 회귀를 차단한다.

주의: color-mix()·투명값은 검사 대상이 아니다(단색 hex 토큰 쌍만).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

_THEMES_CSS = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램" / "frontend" / "src" / "app" / "themes.css"
)

# (라벨, 전경 토큰, 배경 토큰) — 텍스트가 실제로 올라가는 쌍.
_PAIRS = (
    ("본문", "foreground", "background"),
    ("본문/card", "card-foreground", "card"),
    ("보조텍스트/배경", "muted-foreground", "background"),
    ("보조텍스트/muted", "muted-foreground", "muted"),
    ("보조텍스트/card", "muted-foreground", "card"),
    ("버튼 텍스트", "primary-foreground", "primary"),
    ("링크/배경", "link", "background"),
    ("사이드바 텍스트", "sidebar-foreground", "sidebar"),
    ("사이드바 활성버튼", "sidebar-primary-foreground", "sidebar-primary"),
    ("destructive 텍스트", "destructive", "background"),
    ("primary 텍스트/배경", "primary", "background"),
    ("secondary 텍스트", "secondary-foreground", "secondary"),
    ("accent 텍스트", "accent-foreground", "accent"),
    # DEC-246 — CTA/활성 메뉴 pill. --nav-active 는 :root 에서 var(--vivid-lime) 이고
    # 버튼 brand-primary 도 같은 짝(--nav-active-foreground)을 쓴다.
    ("CTA/활성 텍스트", "nav-active-foreground", "vivid-lime"),
)

_MIN_RATIO = 4.5  # WCAG AA 본문 기준


def _lum(hexs: str) -> float:
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def f(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ratio(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _parse_themes() -> dict[str, dict[str, str]]:
    css = _THEMES_CSS.read_text(encoding="utf-8")
    out: dict[str, dict[str, str]] = {}
    for m in re.finditer(r'\[data-theme="([^"]+)"\]\s*\{([^}]+)\}', css):
        out[m.group(1)] = dict(
            re.findall(r'--([a-z-]+):\s*(#[0-9a-fA-F]{6})', m.group(2))
        )
    return out


class ThemePreviewSwatchGuard(TestCase):
    """내정보 테마 미리보기 스와치 — 배경 토큰마다 짝 전경 토큰 필수(상속 금지).

    어두운 사이드바/주요 스와치에서 라벨이 파묻히는 회귀 방지(2026-07-04 보고).
    """

    def test_swatches_pair_bg_with_foreground(self) -> None:
        page = (
            _THEMES_CSS.parents[1] / "app" / "(app)" / "settings" / "my-profile" / "page.tsx"
        ).read_text(encoding="utf-8")
        for pair in (
            "bg-background text-foreground",
            "bg-card text-card-foreground",
            "bg-primary text-primary-foreground",
            "bg-secondary text-secondary-foreground",
            "bg-sidebar text-sidebar-foreground",
            "bg-accent text-accent-foreground",
        ):
            self.assertIn(pair, page, f"미리보기 스와치 전경 토큰 누락: {pair}")


class ThemeContrastGuard(TestCase):
    def test_themes_css_exists_and_has_themes(self) -> None:
        themes = _parse_themes()
        self.assertGreaterEqual(len(themes), 16, "테마 수가 줄었습니다 — 의도한 변경인지 확인")

    def test_themes_declare_chained_tokens_directly(self) -> None:
        """DEC-248 — `:root` 에서 var() 체인인 토큰은 테마가 **직접** 선언해야 한다.

        `--nav-active: var(--vivid-lime)` 처럼 체인으로 선언된 값은 선언된 요소(:root)에서 치환된 뒤
        상속되므로, 테마 블록을 **하위 요소**에 걸어도(내정보 테마 카드 미리보기) 다시 계산되지 않는다.
        그래서 카드마다 CTA 가 현재 적용 테마 색으로 굳어 «어떤 테마인지» 구분이 안 됐다.
        """
        css = _THEMES_CSS.read_text(encoding="utf-8")
        root = (_THEMES_CSS.parent / "globals.css").read_text(encoding="utf-8")
        chained = set(re.findall(r"^\s+(--[a-z0-9-]+):\s*var\(", root, re.M))
        self.assertIn("--nav-active", chained, ":root 체인 토큰 목록이 바뀌었다 — 가드 갱신 필요")
        for name, toks in _parse_themes().items():
            if "vivid-lime" not in toks:
                continue
            for t in ("nav-active", "tab-active", "tab-active-foreground"):
                self.assertIn(t, toks, f"{name}: --{t} 를 직접 선언해야 미리보기가 테마색으로 보인다")
            self.assertEqual(toks["nav-active"], toks["vivid-lime"], f"{name}: CTA 색 불일치")

    def test_all_text_pairs_meet_wcag_aa(self) -> None:
        themes = _parse_themes()
        violations: list[str] = []
        for name, toks in themes.items():
            for label, fg, bg in _PAIRS:
                if fg not in toks or bg not in toks:
                    continue  # color-mix 등 비-hex 는 제외
                r = _ratio(toks[fg], toks[bg])
                if r < _MIN_RATIO:
                    violations.append(
                        f"{name}: {label} {toks[fg]} on {toks[bg]} = {r:.2f} (< {_MIN_RATIO})"
                    )
        self.assertEqual(
            violations, [],
            "테마 텍스트 대비 미달 — 색조 유지 + 명도 조정으로 4.5:1 이상 확보하세요:\n"
            + "\n".join(violations),
        )
