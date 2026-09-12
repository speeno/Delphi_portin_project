"""DEC-276 — `fillHeight` 표 카드의 «뷰포트 바닥» 상한 (합계 행 화면 고정, 2026-09-12).

교문사 보고: 도서별수불원장에서 검색 직후 하단 「합계」가 화면에 없다(표 끝까지 스크롤해야 보임).
원인 — `fillHeight` 는 상위가 높이를 줄 때만 성립하는데, 상세 미선택이면 `SplitListPanes` 가
`disabled` 라 상위가 높이를 주지 않는다. `flex-1` 이 «내용 높이» 로 풀려 카드가 화면 밖까지 자라고,
카드가 스크롤 컨테이너인데 스크롤이 없어 `sticky top-0` 헤더·`sticky bottom-0` 합계가 표 맨 끝에
머문다. 고정 상한(`100dvh-14rem`)은 표가 화면 위쪽에서 시작하는 화면(재고현황)에서만 맞는다 —
브라우저 실측: 표 시작 250px → 38px, 300px → 88px 모자람. `SplitListPanes` 와 같은 실측 방식으로
«여기부터 뷰포트 바닥까지» 를 상한으로 잡는다(상위가 더 작은 높이를 주면 무해).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

_HUB = Path(__file__).resolve().parents[1]
_GRID = _HUB / "도서물류관리프로그램" / "frontend" / "src" / "components" / "data-grid" / "data-grid.tsx"


class FillHeightViewportCapTests(TestCase):
    def setUp(self) -> None:
        self.src = _GRID.read_text(encoding="utf-8")

    def test_measures_viewport_bottom_for_fill_height(self) -> None:
        self.assertIn("FILL_BOTTOM_GAP_PX", self.src)
        self.assertIn("getBoundingClientRect().top", self.src)
        self.assertRegex(
            self.src,
            re.compile(r"window\.innerHeight\s*-\s*top\s*-\s*FILL_BOTTOM_GAP_PX"),
            "상한 = 뷰포트 높이 − 카드 상단 − 하단 여백",
        )
        self.assertIn("el.style.maxHeight", self.src, "레이아웃만 동기화(상태 렌더 캐스케이드 금지)")

    def test_cap_applies_only_to_fill_height_and_not_unbounded(self) -> None:
        """unbounded(「내용 전체 보기」)는 페이지 스크롤 기준 sticky — 상한을 걸면 안 된다."""
        self.assertRegex(self.src, re.compile(r"if\s*\(!fillHeight\s*\|\|\s*unbounded\)"))

    def test_follows_layout_changes(self) -> None:
        """필터 바 접힘·배너 표시로 표 시작 위치가 바뀌면 다시 잰다."""
        self.assertIn('window.addEventListener("resize", measure)', self.src)
        self.assertIn("ResizeObserver", self.src)
        self.assertIn("ro?.disconnect()", self.src)

    def test_sticky_totals_and_header_remain(self) -> None:
        """상한은 sticky 헤더·합계(DEC-151/146)를 살리기 위한 것 — 둘 다 그대로여야 한다."""
        self.assertIn("sticky top-0", self.src)
        self.assertIn("sticky bottom-0", self.src)


if __name__ == "__main__":
    main()
