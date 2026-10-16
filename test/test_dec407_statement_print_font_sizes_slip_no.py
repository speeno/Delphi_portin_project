"""DEC-407 — 거래명세서(삼련) 인쇄: 거래처명 크게 · 서가번호 > 도서명 · 도서명 0.5pt 작게 · 글자 진하게 · 발행일 옆 «출고 N» (교문사 2026-10-16).

요청(위러브솔루션 실물 vs 북이오웍스 출력 대조 사진):
  1. 빨간색: 거래처명 — 크기를 더 크게(하단 글자들보다 크게)
  2. 하늘색: 서가번호 — 우측 도서명보다 크게
  3. 보라색: 글자 폰트를 0.3~0.5 작게(도서명)
  공통: 글자가 더 진하게. ** 출고 명세서 번호가 없다 — 「1/3」 옆 「출고 10」 이 출고명세서 번호.

구현 — 계약 ``print_sales_statement.yaml``(허브 · 번들 동시) ``preprinted_calibration`` 값 + 렌더 훅:
  line_font_pt 9 → 8.5 · shelf_font_pt 8 → 9 · field_font_pt 9 → 10 · name_font_pt 11(신설) · value_ink #000 ·
  value_text_stroke_pt 0.3(신설, -webkit-text-stroke — 0.2 에서 사용자 「1.5배」로) · 발행일 칸 «n/N» 뒤 «거래구분 전표번호»(`sales_statement_print_slip_no_html`,
  Idnum 자릿수 채움 없이 — 레거시 실물 「출고 10」) · slip_no_gap_mm / slip_no_inner_gap_mm.

런타임 없이 렌더 결과(HTML/CSS)와 계약값을 본다. 사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.services import sales_statement_print_profile, transactions_service as tx  # noqa: E402

_SID = "remote_1"
YAMLS = (
    "migration/contracts/print_sales_statement.yaml",
    "도서물류관리프로그램/backend/data/contracts/print_sales_statement.yaml",
)


def _line(shelf: str, name: str) -> dict:
    return {
        "gcode": "G1", "bcode": f"B-{name}", "product_name": name, "shelf": shelf,
        "pubun": "", "gsqut": 1, "gdang": 1000, "grat1": 0, "gssum": 1000, "gbigo": "",
    }


def _detail(lines: list[dict], *, idnum: int | str | None = 10, gubun: str = "출고") -> dict:
    key: dict = {"gdate": "2026.10.16", "hcode": "5019", "jubun": "1", "gjisa": "2|부곡리(본관)"}
    if idnum is not None:
        key["idnum"] = idnum
    if gubun is not None:
        key["gubun"] = gubun
    return {"order_key": key, "customer": {"hcode": "5019", "code": "00001", "gname": "(주)교보문고"}, "lines": lines}


def _tri(detail: dict, *, borders: bool = False) -> str:
    return tx.render_sales_statement_html(
        detail, layout="legacy_triplicate", server_id=_SID, user_id="u", borders=borders,
    )


class ContractValues(TestCase):
    def test_sizes_ordered_and_both_copies_equal(self) -> None:
        cals = []
        for rel in YAMLS:
            cal = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))["profiles"]["default"]["preprinted_calibration"]
            cals.append(cal)
            line, shelf, field, name = (float(cal[k]) for k in ("line_font_pt", "shelf_font_pt", "field_font_pt", "name_font_pt"))
            self.assertEqual(line, 8.5, rel)  # 도서명 0.5pt 작게(9 → 8.5)
            self.assertGreater(shelf, line, rel)  # 서가번호 > 도서명
            self.assertGreater(name, field, rel)  # 거래처명 > 거래처코드 · 발행일
            self.assertGreater(field, line, rel)  # 헤더 값 > 라인
            self.assertEqual(float(cal["value_text_stroke_pt"]), 0.3, rel)  # 0.2 → 1.5배(사용자 2026-10-16)
            self.assertEqual(str(cal["value_ink"]).lower(), "#000", rel)
            self.assertEqual(int(cal["value_font_weight"]), 700, rel)
            self.assertGreater(float(cal["slip_no_gap_mm"]), 0, rel)
            self.assertGreater(float(cal["slip_no_inner_gap_mm"]), 0, rel)
        self.assertEqual(cals[0], cals[1], "허브 · 번들 yaml 동기화")


class CalibrationCss(TestCase):
    def tearDown(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()

    def test_rules_emitted_in_overriding_order(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()
        html = _tri(_detail([_line("A31", "Rosen의 재정학 10판(SP)")]))
        line_rule = ".tri-lines tbody td { font-size: 8.5pt; }"
        shelf_rule = ".tri-lines tbody td.shelf { font-size: 9pt; }"
        field_rule = ".cust-mini td:not(.clab) { font-size: 10pt; }"
        name_rule = ".cust-mini tr.r-name td:not(.clab) { font-size: 11pt; }"
        for r in (line_rule, shelf_rule, field_rule, name_rule):
            self.assertIn(r, html, r)
        self.assertLess(html.index(line_rule), html.index(shelf_rule), "서가 규칙이 뒤에 와야 이긴다")
        self.assertLess(html.index(field_rule), html.index(name_rule), "거래처명 규칙이 뒤에 와야 이긴다")
        # 진하게 — 굵기 700 유지 + 순검정 + 획 덧그리기(세 값 선택자 공통).
        sel = ".tri-lines tbody td, .cust-mini td:not(.clab), .foot3 strong"
        self.assertIn(f"{sel} {{ font-weight: 700; }}", html)
        self.assertIn(f"{sel} {{ color: #000; }}", html)
        self.assertIn(f"{sel} {{ -webkit-text-stroke: 0.3pt currentColor; }}", html)
        # 전표번호 간격(보정값) — 기본 CSS 뒤에 와서 덮는다.
        self.assertIn(".cslip { margin-left: 6mm; }", html)
        self.assertIn(".cslip .cslip-no { margin-left: 3mm; }", html)
        self.assertLess(html.index(".cslip { margin-left: 5mm; }"), html.index(".cslip { margin-left: 6mm; }"))

    def test_missing_keys_emit_nothing(self) -> None:
        css = tx._preprinted_calibration_css({"preprinted_calibration": {"line_font_pt": 9}}, layout="triplicate")
        for frag in ("tr.r-name td:not(.clab) { font-size", "text-stroke", "color: #", ".cslip"):
            self.assertNotIn(frag, css, frag)

    def test_a4_layout_unaffected(self) -> None:
        css = tx._preprinted_calibration_css(
            {"preprinted_calibration": {"name_font_pt": 11, "value_text_stroke_pt": 0.2, "value_ink": "#000", "slip_no_gap_mm": 6}},
            layout="a4",
        )
        for frag in ("tr.r-name", "text-stroke", ".cslip"):
            self.assertNotIn(frag, css, frag)


class SlipNumberInDateCell(TestCase):
    def tearDown(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()

    def test_slip_no_follows_page_fraction_on_every_copy(self) -> None:
        html = _tri(_detail([_line("A31", "도서A")]))
        cell = (
            "<td data-legacy-id='Sobo21.Triplicate.Gdate'><span class='cval'>2026.10.16</span>"
            "<span class='cval cfrac' data-legacy-id='Sobo21.Triplicate.PageFraction'>1/1</span>"
            "<span class='cval cslip' data-legacy-id='Sobo21.Triplicate.SlipNo'>출고<span class='cslip-no'>10</span></span></td>"
        )
        self.assertEqual(html.count(cell), 3, "공급자 · 공급받는자 · 인수증")
        # 양식지 모드에서도 숨기지 않는다(page-indicator 만 숨김).
        self.assertNotIn(".preprinted .cslip", html)
        self.assertNotIn("00010", html, "레거시 실물처럼 자릿수 채움 없이 「10」")

    def test_slip_no_omitted_without_idnum(self) -> None:
        for d in (_detail([_line("A1", "x")], idnum=None), _detail([_line("A1", "x")], idnum=0), _detail([_line("A1", "x")], idnum="")):
            html = _tri(d)
            self.assertNotIn("Sobo21.Triplicate.SlipNo", html)
        # 종전 가드(DEC-393) 그대로 — 페이지 뒤에 바로 칸이 닫힌다.
        html = _tri(_detail([_line("A1", "x")], idnum=None))
        self.assertIn("data-legacy-id='Sobo21.Triplicate.PageFraction'>1/1</span></td>", html)

    def test_gubun_defaults_to_outbound_and_accepts_string_idnum(self) -> None:
        f = tx.sales_statement_print_slip_no_html
        self.assertIn(">출고<span class='cslip-no'>7</span>", f({"order_key": {"idnum": "00007", "gubun": ""}}))
        self.assertIn(">반품<span class='cslip-no'>3</span>", f({"order_key": {"idnum": 3, "gubun": "반품"}}))
        self.assertIn(">출고<span class='cslip-no'>5</span>", f({"idnum": 5}))  # 키가 없어도 상세 최상위 idnum/gubun
        self.assertEqual(f({"order_key": {"idnum": "abc"}}), "")
        self.assertEqual(f({}), "")

    def test_each_page_repeats_slip_no(self) -> None:
        html = _tri(_detail([_line(f"A{i}", f"도서{i}") for i in range(11)]))  # 10행 고정 → 2장
        self.assertEqual(html.count("Sobo21.Triplicate.SlipNo'>출고<span class='cslip-no'>10</span>"), 6)


if __name__ == "__main__":
    main()
