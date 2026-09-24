"""DEC-310 — 기간별재고원장 검색 줄 = 거래처거래원장과 같은 디자인(사용자 2026-09-24 캡처 2건).

「거래 일자 [시작 ~ 기준]」 | 「도서명 | 코드 또는 도서명」 「검색」(h-10 min-w-24 rounded-2xl), 제목과 한 줄(filtersBelow=false).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"


class InventoryStatusSearchLine(TestCase):
    def setUp(self) -> None:
        self.src = (FRONT / "inventory" / "status" / "page.tsx").read_text(encoding="utf-8")
        self.ref = (FRONT / "ledger" / "customer" / "page.tsx").read_text(encoding="utf-8")

    def test_same_building_blocks_as_customer_ledger(self) -> None:
        for needle in (
            'aria-label="거래 일자 기간"',
            ">거래 일자</span>",
            'className="mx-3 hidden h-10 w-px shrink-0 bg-border xl:block"',
            'className="h-10 min-w-24 rounded-2xl px-6 text-sm font-semibold"',
            "filtersBelow={false}",
        ):
            self.assertIn(needle, self.ref, f"기준 화면에 있어야 한다: {needle}")
            self.assertIn(needle, self.src, f"기간별재고원장도 같아야 한다: {needle}")
        self.assertIn('placeholder="코드 또는 도서명"', self.src)
        self.assertIn("검색\n          </Button>", self.src.replace("\r\n", "\n"))

    def test_legacy_ids_and_enter_order_follow_the_new_layout(self) -> None:
        for wid in ("Sobo44.Edit101", "Sobo44.Edit102", "Sobo44.Edit103", "Sobo44.dxButton1"):
            self.assertIn(wid, self.src)
        stops = self.src.split("const FILTER_STOP_IDS = [")[1].split("];")[0]
        order = [stops.index(w) for w in ('"Sobo44.Edit101"', '"Sobo44.Edit102"', '"Sobo44.Edit103"', '"Sobo44.dxButton1"')]
        self.assertEqual(order, sorted(order), "Enter 순서 = 화면 순서(기간 → 도서 → 검색)")

    def test_book_confirm_searches_once(self) -> None:
        self.assertIn("void fetchData({ bcode: code });", self.src, "도서 확정 = 곧바로 조회")
        self.assertIn("closest?.('[data-legacy-id=\"Sobo44.Edit103\"]')) return;", self.src,
                      "필터 줄 Enter 처리가 검색 버튼을 또 눌러 중복 조회하지 않게")


if __name__ == "__main__":
    main()
