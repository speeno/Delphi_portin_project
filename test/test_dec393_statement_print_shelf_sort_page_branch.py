"""DEC-393 — 거래명세서 인쇄: 서가 폰트 1pt 축소 · 서가번호 순 정렬 · 발행일 옆 n/N · 거래처명-지점 (2026-10-08).

사용자 실물 사진(레거시 출력) 기준:
  - 서가번호 칸 글자가 커서 칸을 넘침 → 서가 칸만 line_font_pt − 1 (계약 ``shelf_font_pt``).
  - 창고에서 서가 위치 순서대로 찾도록 명세 라인을 서가번호 알파벳(자연) 순으로 (계약 ``line_sort``).
  - 발행일 뒤 「2/3」 처럼 현재/전체 페이지 — 양식지 모드에서도 찍힌다(page-indicator 는 숨김).
  - 거래처명 뒤에 지점 「(주)교보문고-2 부곡리(본관)」 (전표 Gjisa = ``Jubun|Gname``).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import sales_statement_print_profile, transactions_service as tx  # noqa: E402

_SID = "remote_1"


def _line(shelf: str, name: str, gcode: str = "G1") -> dict:
    return {
        "gcode": gcode, "bcode": f"B-{name}", "product_name": name, "shelf": shelf,
        "pubun": "", "gsqut": 1, "gdang": 1000, "grat1": 0, "gssum": 1000, "gbigo": "",
    }


def _detail(lines: list[dict], *, gjisa: str = "", gname: str = "테스트서점") -> dict:
    return {
        "order_key": {"gdate": "2026.10.07", "hcode": "H1", "jubun": "00013", "gjisa": gjisa},
        "customer": {"hcode": "H1", "gname": gname},
        "lines": lines,
    }


def _tri(detail: dict, *, borders: bool = False) -> str:
    return tx.render_sales_statement_html(
        detail, layout="legacy_triplicate", server_id=_SID, user_id="u", borders=borders,
    )


class ShelfSortTests(TestCase):
    """서가번호 알파벳(자연) 순 — 사진의 열 순서(AB사이·B21·BC사이·F22·다·B32·I33·I41·k32)를 정렬."""

    def test_natural_alpha_order_case_insensitive_empty_last(self) -> None:
        lines = [
            _line("k32,L3-1", "k"), _line("B21", "b21"), _line("다", "da"), _line("", "none"),
            _line("F22,E23", "f"), _line("B32, 갤15", "b32"), _line("AB사이, E", "ab"),
            _line("I41", "i41"), _line("I33, 3-4", "i33"), _line("B2", "b2"), _line("BC사이", "bc"),
        ]
        out = tx.sort_sales_statement_lines_for_print(lines)
        self.assertEqual(
            [ln["product_name"] for ln in out],
            ["ab", "b2", "b21", "b32", "bc", "f", "i33", "i41", "k", "da", "none"],
        )

    def test_stable_for_equal_shelf_and_legacy_mode_keeps_input_order(self) -> None:
        lines = [_line("A1", "x", "G2"), _line("A1", "y", "G1"), _line("", "z")]
        self.assertEqual(
            [ln["product_name"] for ln in tx.sort_sales_statement_lines_for_print(lines)],
            ["x", "y", "z"],
        )
        legacy = [_line("B", "1"), _line("A", "2")]
        self.assertEqual(
            [ln["product_name"] for ln in tx.sort_sales_statement_lines_for_print(legacy, mode="legacy")],
            ["1", "2"],
        )

    def test_render_prints_sorted_rows_without_mutating_detail(self) -> None:
        detail = _detail([_line("B21", "BOOK-TWO"), _line("A1", "BOOK-ONE")])
        html = _tri(detail)
        self.assertLess(html.index("BOOK-ONE"), html.index("BOOK-TWO"))
        self.assertEqual(detail["lines"][0]["product_name"], "BOOK-TWO")  # 입력 detail 은 그대로
        a4 = tx.render_sales_statement_html(detail, layout="default", server_id=_SID, user_id="u")
        self.assertLess(a4.index("BOOK-ONE"), a4.index("BOOK-TWO"))

    def test_contract_declares_line_sort_shelf(self) -> None:
        for rel in (
            "migration/contracts/print_sales_statement.yaml",
            "도서물류관리프로그램/backend/data/contracts/print_sales_statement.yaml",
        ):
            data = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
            self.assertEqual(data["profiles"]["default"]["line_sort"], "shelf", rel)


class ShelfFontTests(TestCase):
    def tearDown(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()

    def test_shelf_cell_one_point_smaller_than_line_font(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()
        html = _tri(_detail([_line("A1", "도서A")]))
        self.assertIn("<td class='shelf' data-legacy-id='Sobo21.Triplicate.Shelf'>A1</td>", html)
        self.assertIn(".tri-lines tbody td { font-size: 9pt; }", html)
        self.assertIn(".tri-lines tbody td.shelf { font-size: 8pt; }", html)
        # 서가 규칙은 공통 행 규칙 뒤에 와야 이긴다(선택자 특이도도 높지만 순서도 보장).
        self.assertLess(
            html.index(".tri-lines tbody td { font-size: 9pt; }"),
            html.index(".tri-lines tbody td.shelf { font-size: 8pt; }"),
        )
        for rel in (
            "migration/contracts/print_sales_statement.yaml",
            "도서물류관리프로그램/backend/data/contracts/print_sales_statement.yaml",
        ):
            cal = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))["profiles"]["default"][
                "preprinted_calibration"
            ]
            self.assertEqual(float(cal["shelf_font_pt"]), float(cal["line_font_pt"]) - 1, rel)

    def test_no_shelf_font_key_emits_no_rule(self) -> None:
        css = tx._preprinted_calibration_css(
            {"preprinted_calibration": {"line_font_pt": 9}}, layout="triplicate",
        )
        self.assertIn(".tri-lines tbody td { font-size: 9pt; }", css)
        self.assertNotIn("td.shelf", css)


class PageFractionTests(TestCase):
    def test_date_cell_carries_current_over_total_on_every_copy_and_page(self) -> None:
        lines = [_line(f"A{i}", f"도서{i}") for i in range(11)]  # 10행 고정 → 2장
        html = _tri(_detail(lines), borders=False)
        frac = "data-legacy-id='Sobo21.Triplicate.PageFraction'>"
        self.assertEqual(html.count(frac + "1/2</span>"), 3)  # 공급자 · 공급받는자 · 인수증
        self.assertEqual(html.count(frac + "2/2</span>"), 3)
        # 발행일 값 바로 뒤, 같은 칸 안에.
        self.assertIn(
            "<td data-legacy-id='Sobo21.Triplicate.Gdate'><span class='cval'>2026.10.07</span>"
            "<span class='cval cfrac' data-legacy-id='Sobo21.Triplicate.PageFraction'>1/2</span></td>",
            html,
        )
        # 양식지 모드에서도 숨기지 않는다(page-indicator 만 숨김) · 한 줄 유지.
        self.assertNotIn(".preprinted .cfrac", html)
        self.assertIn(
            ".cust-mini tr.r-date td:not(.clab), .cust-mini tr.r-name td:not(.clab) "
            "{ white-space: nowrap; overflow: visible; }",
            html,
        )
        self.assertIn(".cfrac { margin-left: 3mm; }", html)

    def test_single_page_is_one_over_one(self) -> None:
        html = _tri(_detail([_line("A1", "도서A")]), borders=True)
        self.assertEqual(html.count("Sobo21.Triplicate.PageFraction'>1/1</span>"), 3)
        self.assertIn("총 1장 중 1장", html)  # 테두리 모드의 상단 표시는 유지


class CustomerBranchLabelTests(TestCase):
    def test_label_appends_branch_from_gjisa_combo(self) -> None:
        f = tx.sales_statement_print_customer_label
        self.assertEqual(
            f(_detail([], gjisa="2|부곡리(본관)", gname="(주)교보문고")), "(주)교보문고-2 부곡리(본관)",
        )
        self.assertEqual(f(_detail([], gjisa="부곡리(본관)")), "테스트서점-부곡리(본관)")
        self.assertEqual(f(_detail([], gjisa="")), "테스트서점")
        self.assertEqual(f(_detail([], gjisa="  ")), "테스트서점")
        # 거래처명이 비면 종전처럼 hcode, 지점은 그 뒤에.
        self.assertEqual(f(_detail([], gjisa="2|부곡리", gname="")), "H1-2 부곡리")
        # 이미 지점으로 끝나는 이름엔 두 번 붙이지 않는다.
        self.assertEqual(f(_detail([], gjisa="2|부곡리", gname="교보-2 부곡리")), "교보-2 부곡리")

    def test_triplicate_and_a4_print_customer_with_branch(self) -> None:
        detail = _detail([_line("A1", "도서A")], gjisa="2|부곡리(본관)", gname="(주)교보문고")
        tri = _tri(detail)
        self.assertIn(
            "<td data-legacy-id='Sobo21.Triplicate.Gname'><span class='cval'>(주)교보문고-2 부곡리(본관)</span></td>",
            tri,
        )
        a4 = tx.render_sales_statement_html(detail, layout="default", server_id=_SID, user_id="u")
        self.assertIn("data-legacy-id='Sobo21.Header.Customer'>(주)교보문고-2 부곡리(본관)<", a4)

    def test_no_branch_keeps_plain_name(self) -> None:
        tri = _tri(_detail([_line("A1", "도서A")]))
        self.assertIn("<span class='cval'>테스트서점</span>", tri)
