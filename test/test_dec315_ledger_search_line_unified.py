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
            "flex w-full min-w-0 flex-wrap items-center justify-end gap-3 xl:flex-nowrap",
            "flex h-9 min-w-max items-center rounded-2xl border border-border bg-control-surface px-1.5",
            "mx-3 hidden h-10 w-px shrink-0 bg-border xl:block",
            "h-10 min-w-24 rounded-2xl px-6 text-sm font-semibold",
        ):
            self.assertIn(cls, ref, f"기준 화면: {cls}")
            self.assertIn(cls, shared, f"공용 조각: {cls}")


class ReceivableShowsBothPanes(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/ledger/receivable/page.tsx")

    def test_both_panes_shown_after_search_all_customers(self) -> None:
        # DEC-316 — 첫 구분 자동 선택 대신 레거시처럼 조회 직후 하단 = 전 거래처(구분 미선택), 하단은 항상 표시.
        self.assertNotIn("autoPickRef", self.src)
        self.assertNotIn("secondaryVisible=", self.src)
        self.assertIn("showAll || selGubun === null", self.src)

    def test_show_all_checkbox_on_top_header(self) -> None:
        top = self.src.split('title="거래처구분별"')[1].split('legacyId="Sobo33.DBGrid101"')[0]
        self.assertIn('data-legacy-id="Sobo33.ShowAll"', top, "상단 표 머리에 「내용 전체 보기」")
        self.assertEqual(self.src.count('data-legacy-id="Sobo33.ShowAll"'), 1)

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
