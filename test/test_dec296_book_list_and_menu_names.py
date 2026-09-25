"""DEC-296 — 도서관리 도서처리 제거 + 신규 도서 위치 + 메뉴명 「(마스터)」 제거 (2026-09-22).

사용자 요청: 「도서관리 화면에서 도서처리 항목 제거하고, 신규도서 버튼도 검색입력창 앞으로 이동,
메뉴명에 (마스터)라고 붙은 텍스트 제거」.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BOOK = FRONT / "app" / "(app)" / "master" / "book" / "page.tsx"


class MenuNames(TestCase):
    def test_no_master_suffix_in_registry_or_titles(self) -> None:
        reg = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        self.assertNotIn("(마스터)", reg)
        for cap in ("거래처관리", "도서관리", "출판사·출고거래처", "도서코드", "입고처관리", "기타거래처관리", "저자관리"):
            self.assertIn(f'caption: "{cap}"', reg, cap)
        hits = [str(p.relative_to(FRONT)) for p in FRONT.rglob("*.tsx") if "(마스터)" in p.read_text(encoding="utf-8")]
        self.assertEqual(hits, [], "화면 제목·문구에도 (마스터) 없음")


class BookList(TestCase):
    def test_jubun_filter_and_column_removed(self) -> None:
        src = BOOK.read_text(encoding="utf-8")
        self.assertNotIn('label: "도서처리"', src)
        self.assertNotIn("f-jubun", src)
        self.assertNotIn("jubun", src.split("const columns")[0], "요청 파라미터·세션 키도 제거")

    def test_new_book_button_before_search(self) -> None:
        src = BOOK.read_text(encoding="utf-8")
        band_start = src.index("              >\n", src.index("actions={"))
        btn = src.index('data-legacy-id="Sobo14.Button101"')
        self.assertLess(band_start, btn, "필터 띠 안")
        # DEC-336 — 검색 줄 = 붙임형 알약(AttachedFilterField).
        self.assertLess(btn, src.index('id="q"'), "검색 입력 앞")


if __name__ == "__main__":
    main()
