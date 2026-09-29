"""DEC-353/354 — 원장관리 공통 (2026-09-30, 교문사 경리부 요청 문서).

DEC-353 「날짜 및 검색 창이 우측 상단에 있는 것을 좌측으로 이동」
  거래처거래원장 · 도서별수불원장 · 기간별미수원장 · 기간별재고원장 · 도서별재고금액 (+ 같은 메뉴의 원장변경):
  제목과 같은 줄에서 제목·경로 바로 뒤, 왼쪽 정렬(통계관리 DEC-350 과 같은 배치).

DEC-354 「"검색" 클릭 후 프로그램이 돌아가는지 확인할 수가 없어서 여러 번 클릭 … 검색되고 있다는 표시가 나와야 …
  원장관리뿐 아니라 모든 검색창에 적용」
  화면마다 버튼을 고치지 않고 한 곳에서: api-client 가 «사용자 조작에서 비롯된 요청»의 시작/끝을 알리고
  루트 레이아웃의 ApiBusyIndicator 가 진행 띠 · 「검색 중…」 알림 · 누른 버튼 안의 표시를 그린다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

SRC = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (SRC / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class LedgerSearchLineOnTheLeft(TestCase):
    SHARED = (
        "app/(app)/inventory/ledger/page.tsx",     # 도서별수불원장
        "app/(app)/ledger/receivable/page.tsx",    # 기간별미수원장
        "app/(app)/inventory/status/page.tsx",     # 기간별재고원장
        "app/(app)/inventory/value/page.tsx",      # 도서별재고금액
    )

    def test_shared_line_screens(self) -> None:
        for rel in self.SHARED:
            src = _read(rel)
            header = src.split("<PageHeader")[1].split("</PageHeader>")[0]
            self.assertIn("filtersBelow={false}", header, f"{rel}: 제목과 같은 줄")
            lines = re.findall(r"<LedgerSearchLine\b([^>]*)>", header)
            self.assertEqual(len(lines), 1, rel)
            self.assertIn('align="start"', lines[0], f"{rel}: 왼쪽 정렬")

    def test_customer_ledger_reference_screen(self) -> None:
        src = _read("app/(app)/ledger/customer/page.tsx")
        header = src.split("<PageHeader")[1].split("</PageHeader>")[0]
        self.assertIn("filtersBelow={false}", header)
        self.assertIn("flex w-full min-w-0 flex-wrap items-center justify-start gap-3 xl:flex-nowrap", header)
        self.assertNotIn("justify-end gap-3", header)

    def test_adjustment_ledger_page_placement(self) -> None:
        src = _read("components/ledger/adjustment-ledger-screen.tsx")
        block = src.split('placement === "page"\n          ? "')[1].split('"')[0]
        self.assertIn("justify-start", block)
        self.assertNotIn("justify-end", block)

    def test_no_search_line_is_right_aligned_anymore(self) -> None:
        """제목 줄에 검색 줄을 둔 화면(filtersBelow 끔)은 전부 왼쪽 정렬이다."""
        offenders = []
        for p in SRC.rglob("*.tsx"):
            text = p.read_text(encoding="utf-8")
            if "filtersBelow={false}" not in text:
                continue
            for attrs in re.findall(r"<LedgerSearchLine\b([^>]*)>", text):
                if 'align="start"' not in attrs:
                    offenders.append(str(p.relative_to(SRC)))
            if re.search(r"items-center justify-end gap-3 xl:flex-nowrap", text):
                offenders.append(str(p.relative_to(SRC)))
        self.assertEqual(sorted(set(offenders)), [])


class SearchBusySignal(TestCase):
    def test_api_client_reports_start_and_end(self) -> None:
        src = _read("lib/api-client.ts")
        self.assertIn('import { beginApiActivity } from "@/lib/api-activity";', src)
        body = src.split("async function request<T = unknown>(")[1].split("\n}\n")[0]
        self.assertIn("const endActivity = beginApiActivity();", body)
        tail = body.rsplit("} finally {", 1)[1]
        self.assertIn("endActivity();", tail, "끝 신호는 finally — 실패·타임아웃에도 표시가 남지 않는다")
        self.assertLess(body.index("beginApiActivity()"), body.index("await fetch("))

    def test_only_requests_following_a_user_gesture_count(self) -> None:
        src = _read("lib/api-activity.ts")
        self.assertIn("export function noteUserGesture(", src)
        self.assertIn("export function beginApiActivity(): () => void", src)
        self.assertIn("t - lastGestureAt <= GESTURE_WINDOW_MS", src)
        self.assertIn("if (!foreground) return () => {};", src, "주기 조회·자동완성은 세지 않는다")
        self.assertIn("chainUntil = now() + CHAIN_WINDOW_MS;", src, "목록 → 상세로 이어지는 요청은 같은 조작")
        self.assertIn("if (done) return;", src, "끝 신호 중복 방지")
        self.assertRegex(src, r"SEARCH_LABEL_RE = /검색\|조회/")

    def test_indicator_mounted_once_in_root_layout(self) -> None:
        layout = _read("app/layout.tsx")
        self.assertIn('import { ApiBusyIndicator } from "@/components/app-shell/api-busy-indicator";', layout)
        self.assertEqual(layout.count("<ApiBusyIndicator />"), 1)

    def test_indicator_behaviour(self) -> None:
        src = _read("components/app-shell/api-busy-indicator.tsx")
        self.assertIn('document.addEventListener("click", onClick, true)', src)
        self.assertIn('e.key === "Enter" && !e.isComposing', src)
        self.assertIn("SHOW_DELAY_MS", src)
        self.assertIn('origin.setAttribute("data-busy", "1")', src)
        self.assertIn('removeAttribute("data-busy")', src)
        self.assertIn('kind === "search" ? "검색 중…" : "불러오는 중…"', src)
        self.assertIn('role="status"', src)
        self.assertIn("pointer-events-none", src, "표시가 화면 조작을 막지 않는다")

    def test_styles(self) -> None:
        css = _read("app/globals.css")
        for needle in (
            "@keyframes api-busy-slide",
            "@keyframes api-busy-spin",
            "button[data-busy]:not([data-busy-managed])::before",
            '[data-slot="data-grid-scroll"][data-loading] tbody',
        ):
            self.assertIn(needle, css)

    def test_grid_marks_stale_rows_while_reloading(self) -> None:
        grid = _read("components/data-grid/data-grid.tsx")
        self.assertIn('data-slot="data-grid-scroll"', grid)
        self.assertIn('data-loading={loading && rows.length > 0 ? "" : undefined}', grid)


class SearchButtonsShowProgress(TestCase):
    def test_shared_button(self) -> None:
        src = _read("components/shared/ledger-search-line.tsx")
        body = src.split("export function LedgerSearchButton(")[1]
        self.assertIn("loading = false,", body)
        self.assertIn("disabled={disabled || loading}", body, "조회 중에는 다시 누를 수 없다")
        self.assertIn("검색 중…", body)
        self.assertIn('data-busy-managed=""', body, "버튼이 직접 표시 — 공용 data-busy 표시와 겹치지 않게")

    def test_every_shared_button_passes_loading(self) -> None:
        missing = []
        for p in SRC.rglob("*.tsx"):
            if p.name == "ledger-search-line.tsx":
                continue
            for tag in re.findall(r"<LedgerSearchButton\b[\s\S]*?/>", p.read_text(encoding="utf-8")):
                if "loading={" not in tag:
                    missing.append(str(p.relative_to(SRC)))
        self.assertEqual(missing, [])

    def test_custom_ledger_buttons(self) -> None:
        for rel in ("app/(app)/ledger/customer/page.tsx", "components/ledger/adjustment-ledger-screen.tsx"):
            src = _read(rel)
            self.assertIn("검색 중…", src, rel)
            self.assertIn('data-busy-managed=""', src, rel)


if __name__ == "__main__":
    main()
