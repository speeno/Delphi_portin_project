"""DEC-349 — 표 아래 페이지 줄이 화면 밖으로 밀리지 않게 (2026-09-30 사용자 「화면 하단에 페이지 번호가 반이 가려진다」).

합계 줄이 있는 표는 페이지 줄이 화면 하단 고정(sticky)이 아니라 카드 **아래** 흐름에 놓인다(2026-08-23 — 합계를 덮지 않게).
그런데 `fillHeight` 상한(DEC-276)은 «카드 상단 ~ 뷰포트 바닥»만 재서 카드가 바닥까지 차고, 그 아래 페이지 줄이
절반쯤 화면 밖으로 밀렸다(도서별년말집계에 합계 줄이 생기며 드러남, DEC-346). 상한에서 그 줄 높이를 뺀다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "data-grid" / "data-grid.tsx"
YEAR_END = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "reports" / "year-end-book" / "page.tsx"


class FooterBelowCardIsReserved(TestCase):
    def setUp(self) -> None:
        self.src = GRID.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.effect = self.src.split("const measure = () => {")[1].split("}, [fillHeight")[0]

    def test_cap_subtracts_in_flow_footer(self) -> None:
        self.assertIn("footerRef.current", self.effect)
        self.assertIn("footer.offsetHeight + FILL_FOOTER_GAP_PX", self.effect)
        self.assertRegex(
            self.effect,
            re.compile(r"window\.innerHeight\s*-\s*top\s*-\s*FILL_BOTTOM_GAP_PX\s*-\s*below"),
        )

    def test_sticky_footer_is_not_subtracted(self) -> None:
        """sticky 페이지 줄은 카드 위에 떠 있다 — 빼면 합계 없는 화면의 표가 괜히 짧아진다."""
        self.assertIn("footer && !stickyBottomPager ?", self.effect)
        self.assertIn("const stickyBottomPager = showBottomPager && !totals;", self.src)

    def test_remeasures_when_footer_appears_or_changes_mode(self) -> None:
        deps = self.src.split("}, [fillHeight")[1].split("]);")[0]
        self.assertIn("showFooter", deps)
        self.assertIn("stickyBottomPager", deps)

    def test_footer_element_is_the_measured_one(self) -> None:
        footer = self.src.split("{showFooter && (")[1].split("</div>")[0]
        self.assertIn("ref={footerRef}", footer)
        self.assertIn('data-slot="data-grid-footer"', footer)


class YearEndBookTotalsFit(TestCase):
    def test_amount_columns_are_wide_enough_for_totals(self) -> None:
        src = YEAR_END.read_text(encoding="utf-8")
        for key in ("gosum", "gbsum", "sale_amt"):
            line = next(ln for ln in src.splitlines() if f'key: "{key}"' in ln)
            m = re.search(r"minWidthPx:\s*(\d+)", line)
            self.assertIsNotNone(m, f"{key}: 합계(억 단위)가 잘리지 않게 최소 폭 지정")
            self.assertGreaterEqual(int(m.group(1)), 130, key)


if __name__ == "__main__":
    main()
