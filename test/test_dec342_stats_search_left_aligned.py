"""DEC-342 → DEC-350 — 통계관리 메뉴 전 화면: 검색 관련 컴포넌트 왼쪽 정렬 (2026-09-30).

사용자: 「통계관리 메뉴에 포함된 모든 화면들에 대해서 거래일자, 거래처명 등 모든 검색 관련 컴포넌트들을
왼쪽 정렬로 이동」 → (같은 날 확정) 「제목과 같은 줄에서 왼쪽으로 붙이는 형식으로」.

- DEC-342 는 DEC-268 기본 규칙(제목 줄 **다음 줄**)으로 옮겼으나, DEC-350 에서 **제목과 같은 줄**(제목·경로 바로 뒤)로 확정.
- 알약 구성·위젯 id·Enter 순서는 DEC-320 그대로. 원장관리(DEC-315)는 범위 밖 — 공용 조각의 기본 정렬("end")은 그대로.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

SRC = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"

# 자체 검색 줄을 가진 화면 / 공용 필터 바 화면 / 공용 매트릭스(년·월 세분화 판매 6종) 라우트
DIRECT = (
    "app/(app)/reports/book-sales/page.tsx",
    "app/(app)/reports/customer-sales/page.tsx",
    "app/(app)/reports/year-end-book/page.tsx",
    "app/(app)/stats/monthly/page.tsx",
    "app/(app)/stats/customer/page.tsx",
    "app/(app)/stats/book/page.tsx",
)
BAR = (
    "app/(app)/stats/sales-period/page.tsx",
    "app/(app)/stats/customer-analysis/page.tsx",
    "app/(app)/stats/book-turnover/page.tsx",
    "app/(app)/stats/quarterly-summary/page.tsx",
    "app/(app)/stats/publisher/page.tsx",
)
MATRIX_ROUTES = (
    "book-sales-monthly",
    "customer-sales-monthly",
    "book-sales-daily",
    "customer-sales-daily",
    "sales-by-book-monthly",
    "sales-by-customer-monthly",
)
SEARCH_LINE = re.compile(r"<LedgerSearchLine\b([^>]*)>")


def _read(rel: str) -> str:
    return (SRC / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def _header(src: str) -> str:
    return src.split("<PageHeader")[1].split("</PageHeader>")[0]


class SharedPieceHasAlignOption(TestCase):
    def test_default_stays_right_for_ledger_screens(self) -> None:
        src = _read("components/shared/ledger-search-line.tsx")
        self.assertIn('align = "end"', src, "기본값은 종전(오른쪽) — 원장관리 화면 불변")
        self.assertIn('align?: "start" | "end"', src)
        self.assertIn('align === "start" && "justify-start"', src)
        self.assertIn("cn(", src, "justify-end ↔ justify-start 충돌은 tailwind-merge 로 해소")

    def test_ledger_screens_not_touched(self) -> None:
        for rel in (
            "app/(app)/ledger/receivable/page.tsx",
            "app/(app)/inventory/ledger/page.tsx",
            "app/(app)/inventory/value/page.tsx",
            "app/(app)/inventory/status/page.tsx",
        ):
            src = _read(rel)
            self.assertIn("filtersBelow={false}", src, rel)
            self.assertNotIn('align="start"', src, rel)


class StatsScreensAreLeftAlignedOnTitleRow(TestCase):
    def _assert_all_lines_start(self, rel: str, src: str, expected: int | None = None) -> None:
        lines = SEARCH_LINE.findall(src)
        self.assertTrue(lines, f"{rel}: 검색 줄 없음")
        if expected is not None:
            self.assertEqual(len(lines), expected, rel)
        for attrs in lines:
            self.assertIn('align="start"', attrs, f"{rel}: 검색 줄은 왼쪽 정렬")

    def _assert_on_title_row(self, rel: str, src: str) -> None:
        opening = src.split("<PageHeader")[1].split(">")[0]
        self.assertIn("filtersBelow={false}", opening, f"{rel}: 제목과 같은 줄(DEC-350)")

    def test_direct_screens(self) -> None:
        for rel in DIRECT:
            src = _read(rel)
            self._assert_on_title_row(rel, src)
            self._assert_all_lines_start(rel, _header(src), 1)

    def test_filter_bar_screens(self) -> None:
        bar = _read("components/stats/stats-filter-bar.tsx")
        self._assert_all_lines_start("stats-filter-bar", bar, 1)
        for rel in BAR:
            src = _read(rel)
            self._assert_on_title_row(rel, src)
            self.assertIn("<StatsFilterBar", _header(src), rel)

    def test_matrix_screens(self) -> None:
        screen = _read("components/stats/sales-matrix-screen.tsx")
        self._assert_on_title_row("sales-matrix-screen", screen)
        self._assert_all_lines_start("sales-matrix-screen", screen, 2)
        # 검색 줄이 여러 줄 — 제목은 가운데가 아니라 첫 줄에 맞춘다.
        opening = screen.split("<PageHeader")[1].split(">\n")[0]
        self.assertIn("md:items-start", opening)
        for route in MATRIX_ROUTES:
            page = _read(f"app/(app)/year-month-stats/{route}/page.tsx")
            self.assertIn("<SalesMatrixScreen", page, route)

    def test_no_stats_menu_screen_is_missed(self) -> None:
        """form-registry 의 통계관리(menuGroup statistics) 라우트가 전부 위 목록에 들어 있다."""
        registry = _read("lib/form-registry.ts")
        routes: set[str] = set()
        for block in re.split(r"\n  \{\n", registry):
            if 'menuGroup: "statistics"' not in block:
                continue
            body = block.split("\n  },")[0]
            if re.search(r"\bhidden:\s*true", body) or "hiddenReason" in body:
                continue
            m = re.search(r'route:\s*"([^"]+)"', body)
            if m:
                routes.add(m.group(1))
        covered = {"/" + rel.split("app/(app)/")[1].rsplit("/page.tsx", 1)[0] for rel in DIRECT + BAR}
        covered |= {f"/year-month-stats/{r}" for r in MATRIX_ROUTES}
        self.assertTrue(routes, "통계관리 라우트를 읽지 못함")
        self.assertEqual(sorted(routes - covered), [], "왼쪽 정렬 가드에 없는 통계관리 화면")


if __name__ == "__main__":
    main()
