"""DEC-218 — 목록표 가로 스크롤 힌트 (2026-08-26 23:26 사용자 요청).

"목록표의 필드 항목이 많아서 좌우 스크롤이 생겼을 때 좌우로 감춰진 필드가 존재한다는 것을 간단한 애니메이션으로
사용자에게 표시" — 공용 DataGrid 와 남은 수동 <table> 래퍼 전부에 붙어 있어야 한다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class SharedHint(TestCase):
    def test_hook_and_overlays(self) -> None:
        src = _read("components/shared/h-scroll-hint.tsx")
        self.assertIn("export function useHorizontalOverflowHint", src)
        self.assertIn("addEventListener(\"scroll\", update", src)
        self.assertIn("new ResizeObserver(update)", src)
        self.assertIn("new MutationObserver(update)", src)
        self.assertIn('data-slot="hscroll-hint-left"', src)
        self.assertIn('data-slot="hscroll-hint-right"', src)
        self.assertIn("hscroll-hint-badge", src)
        self.assertIn("scrollBy({ left: dir *", src, "배지 클릭 = 그쪽으로 스크롤")
        self.assertIn("export function HScrollBox", src)
        # DEC-224 — 배지는 카드 전체가 아니라 뷰포트 가시 구간의 세로 중앙(페이지 스크롤로 길어진 표에서도 보이게)
        self.assertIn("function useVisibleBand(", src)
        self.assertIn('document.addEventListener("scroll", schedule, { capture: true, passive: true })', src)
        self.assertIn("const band = useVisibleBand(scrollRef, hint.left || hint.right);", src)
        self.assertIn('(band ? "" : " inset-y-0")', src)

    def test_animation_css(self) -> None:
        css = _read("app/globals.css")
        self.assertIn("@keyframes hscroll-nudge-right", css)
        self.assertIn("@keyframes hscroll-nudge-left", css)
        self.assertIn("  .hscroll-hint-badge {\n    animation: hscroll-nudge-right", css)
        self.assertIn("(prefers-reduced-motion: reduce) {\n    .hscroll-hint-badge { animation: none; }", css)


class DataGridWired(TestCase):
    def test_scroll_card_has_ref_and_hint(self) -> None:
        src = _read("components/data-grid/data-grid.tsx")
        self.assertIn("useHorizontalOverflowHint(scrollRef)", src)
        self.assertIn("ref={scrollRef}", src)
        self.assertIn("{!unbounded && <HScrollEdgeHints hint={overflowHint} scrollRef={scrollRef} />}", src)
        # relative 래퍼가 fillHeight 의 flex 체인을 이어야 분할 패널 높이가 유지된다
        self.assertIn('"relative w-full min-w-0" + (fillHeight && !unbounded ? " flex min-h-0 flex-1 flex-col" : "")', src)


class ManualTablesWrapped(TestCase):
    """수동 <table> 스크롤 래퍼는 전부 HScrollBox — 새로 생기는 `overflow-x-auto bg-card` div 도 잡는다."""

    def test_no_bare_scroll_wrapper_left(self) -> None:
        pat = re.compile(r"<(div|section)\b[^>]*className=\"[^\"]*overflow-(x-)?auto bg-card")
        bare: list[str] = []
        for f in sorted(list((FRONT / "app" / "(app)").glob("**/*.tsx")) + list((FRONT / "components").glob("**/*.tsx"))):
            rel = str(f.relative_to(FRONT))
            if rel.startswith("components/data-grid/") or rel.startswith("components/shared/h-scroll-hint"):
                continue
            src = f.read_text(encoding="utf-8")
            if pat.search(src):
                bare.append(rel)
        self.assertEqual(bare, [], "HScrollBox 로 감싸세요")

    def test_expected_files_use_hscrollbox(self) -> None:
        for rel in (
            "app/(app)/ledger/customer-integrated/page.tsx",
            "app/(app)/admin/audit/page.tsx",
            "app/(app)/admin/signup-requests/page.tsx",
            "app/(app)/admin/id-logn/page.tsx",
            "app/(app)/transactions/status/page.tsx",
            "app/(app)/inbound/receipts/new/page.tsx",
            "app/(app)/inbound/receipts/[receiptKey]/page.tsx",
            "app/(app)/returns/receipts/[returnKey]/page.tsx",
        ):
            src = _read(rel)
            self.assertIn('import { HScrollBox } from "@/components/shared/h-scroll-hint";', src, rel)
            self.assertEqual(src.count("<HScrollBox"), src.count("</HScrollBox>"), rel)
            self.assertGreaterEqual(src.count("<HScrollBox"), 1, rel)


if __name__ == "__main__":
    main()
