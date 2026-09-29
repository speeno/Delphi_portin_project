"""DEC-315 — 원장관리 세부 화면 한 줄 검색 통일 + 기간별미수원장 상/하단 자동 출력 + 도서별재고금액 상단 구성 (2026-09-24)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

FRONT = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class LedgerScreensShareOneLineSearch(TestCase):
    SHARED = (
        "app/(app)/ledger/receivable/page.tsx",
        "app/(app)/inventory/ledger/page.tsx",
        "app/(app)/inventory/value/page.tsx",
    )

    def test_screens_use_shared_pieces_on_title_row(self) -> None:
        for rel in self.SHARED:
            src = _read(rel)
            self.assertIn("filtersBelow={false}", src, rel)
            for piece in ("<LedgerSearchLine", "<LedgerDatePill", "<LedgerSearchDivider", "<LedgerNamePill", "<LedgerSearchButton"):
                self.assertIn(piece, src, f"{rel}: {piece}")

    def test_shared_pieces_copy_reference_markup(self) -> None:
        shared = _read("components/shared/ledger-search-line.tsx")
        ref = _read("app/(app)/ledger/customer/page.tsx")
        for cls in (
            "flex h-9 min-w-max items-center rounded-2xl border border-border bg-control-surface px-1.5",
            "mx-3 hidden h-10 w-px shrink-0 bg-border xl:block",
            "h-10 min-w-24 rounded-2xl px-6 text-sm font-semibold",
        ):
            self.assertIn(cls, ref, f"기준 화면: {cls}")
            self.assertIn(cls, shared, f"공용 조각: {cls}")
        # 줄 컨테이너 — DEC-353(2026-09-30) 부터 기준 화면은 왼쪽 정렬(justify-start). 공용 조각은 기본 클래스에
        # `align="start"` 를 얹는다. DEC-329 — 한 줄 고정(xl:flex-nowrap)은 기본값이고 `wrap` 선택 시에만 빠진다.
        self.assertIn("flex w-full min-w-0 flex-wrap items-center justify-start gap-3 xl:flex-nowrap", ref)
        self.assertIn("flex w-full min-w-0 flex-wrap items-center justify-end gap-3", shared)
        self.assertIn('align === "start" && "justify-start"', shared)
        self.assertIn('wrap ? "" : " xl:flex-nowrap"', shared)
        self.assertIn("wrap = false", shared)


class ReceivableShowsBothPanes(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/ledger/receivable/page.tsx")

    def test_both_panes_shown_after_search_all_customers(self) -> None:
        # DEC-316 — 첫 구분 자동 선택 대신 레거시처럼 조회 직후 하단 = 전 거래처(구분 미선택), 하단은 항상 표시.
        self.assertNotIn("autoPickRef", self.src)
        self.assertNotIn("secondaryVisible=", self.src)
        self.assertIn("selGubun === null || (r.gubun || \"\") === selGubun", self.src)

    def test_show_all_checkbox_removed(self) -> None:
        # DEC-355(2026-09-30 교문사 「"내용 전체보기" 삭제, 불필요」) — 조회 직후가 이미 전 거래처이고
        # 「구분 해제」로 전체로 돌아가므로 체크박스는 같은 일을 하는 중복이었다.
        self.assertNotIn("내용 전체 보기", self.src)
        self.assertNotIn("showAll", self.src)
        self.assertNotIn("Sobo33.ShowAll", self.src)
        self.assertIn("구분 해제", self.src, "전체로 돌아가는 경로는 남는다")
        self.assertIn('"거래처별 (전체)"', self.src)

    def test_blank_gubun_key_round_trip(self) -> None:
        self.assertIn('setSelGubun(key === "(none)" ? "" : String(key))', self.src)


class StockValueTopLikeInventoryStatus(TestCase):
    def test_empty_hint_section_header_and_show_all_fix(self) -> None:
        src = _read("app/(app)/inventory/value/page.tsx")
        self.assertIn("<EmptyHint>거래일자와 도서명으로 검색하세요</EmptyHint>", src)
        self.assertEqual(src.count("<SectionHeader"), 2)
        # DEC-316 — 조회 직후(구분 미선택)·내용 전체 보기 = 전 도서, 하단은 항상 표시.
        self.assertIn("showAll || selectedClass === null", src)
        self.assertNotIn("secondaryVisible=", src)


if __name__ == "__main__":
    main()
