"""양식지(미리 인쇄 용지) 위치 보정(preprinted_calibration) 회귀 — DEC-074.

물리 양식지와 텍스트 위치가 어긋나는 문제: 보정은 계약 yaml
(migration/contracts/print_sales_statement.yaml → profiles.<key>.preprinted_calibration)
데이터로만 제어한다(코드 분기 0). 삼련·A4 두 빌더 모두 동일 적용,
borders on/off 지오메트리 단일화(시험 인쇄 측정값이 양식지 모드에 그대로 유효).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

import yaml  # noqa: E402

from app.services import sales_statement_print_profile, transactions_service as tx  # noqa: E402

_SID = "remote_1"


def _detail() -> dict:
    return {
        "order_key": {"gdate": "2026.07.04", "hcode": "H1", "jubun": "00001", "gjisa": ""},
        "customer": {"hcode": "H1", "gname": "테스트거래처"},
        "lines": [
            {"gcode": "00001", "bcode": "B1", "product_name": "도서A", "shelf": "",
             "pubun": "위탁", "gsqut": 3, "gdang": 10000, "grat1": 70, "gssum": 21000, "gbigo": ""},
        ],
    }


def _profile_with_cal(**cal) -> dict:
    base = sales_statement_print_profile.resolve_profile(_SID)
    return {**base, "preprinted_calibration": cal}


class CalibrationCssTests(TestCase):
    def tearDown(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()

    def test_triplicate_applies_offsets_and_row_height(self) -> None:
        prof = _profile_with_cal(offset_top_mm=-2, offset_left_mm=1.5, line_row_height_mm=6.2)
        with patch.object(tx, "resolve_profile", return_value=prof, create=True), \
                patch("app.services.sales_statement_print_profile.resolve_profile",
                      return_value=prof):
            html = tx.render_sales_statement_html(
                _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=False,
            )
        self.assertIn("transform: translate(1.5mm, -2.0mm)", html)
        self.assertIn(".tri-lines tbody td { height: 6.2mm; box-sizing: border-box; }", html)

    def test_triplicate_borders_on_shares_same_geometry(self) -> None:
        """테두리 ON 시험 인쇄로 측정한 보정값이 양식지 모드와 동일 적용."""
        prof = _profile_with_cal(offset_top_mm=3)
        with patch("app.services.sales_statement_print_profile.resolve_profile",
                   return_value=prof):
            on = tx.render_sales_statement_html(
                _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=True,
            )
            off = tx.render_sales_statement_html(
                _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=False,
            )
        for html in (on, off):
            self.assertIn("transform: translate(0.0mm, 3.0mm)", html)

    def test_zero_calibration_emits_nothing(self) -> None:
        prof = _profile_with_cal(offset_top_mm=0, offset_left_mm=0, line_row_height_mm=0)
        with patch("app.services.sales_statement_print_profile.resolve_profile",
                   return_value=prof):
            html = tx.render_sales_statement_html(
                _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=False,
            )
        self.assertNotIn("transform: translate", html)

    def test_helper_graceful_on_bad_values(self) -> None:
        css = tx._preprinted_calibration_css(
            {"preprinted_calibration": {"offset_top_mm": "abc", "line_row_height_mm": 5}},
            layout="triplicate",
        )
        self.assertIn("height: 5.0mm", css)  # 불량 키만 0 처리, 나머지 유효
        self.assertEqual(tx._preprinted_calibration_css({}, layout="triplicate"), "")
        self.assertEqual(
            tx._preprinted_calibration_css({"preprinted_calibration": {}}, layout="unknown"), "",
        )

    def test_default_profile_measured_geometry_emitted(self) -> None:
        """실측 정본(172.6mm 표폭·컬럼·행높이)이 기본 프로필로 렌더에 반영된다."""
        sales_statement_print_profile.clear_profile_cache_for_tests()
        html = tx.render_sales_statement_html(
            _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=False,
        )
        # 스캔 실측 정본 + PDF 검증 루프 확정값 (2026-07-04 — 전 항목 물리 ±0.35mm)
        self.assertIn(
            ".tri-lines { width: 182.9mm; margin-left: 3.5mm; height: auto; }", html,
        )
        self.assertIn(".tri-lines tbody td { height: 4.52mm; box-sizing: border-box; }", html)
        # 섹션 피치 99.7mm — 2·3련 누적 어긋남 방지의 핵심
        self.assertIn(".triplicate-section { height: 99.7mm; margin-bottom: 0.0mm; }", html)
        self.assertIn("@page { margin-top: 0.0mm; margin-bottom: 0.0mm; }", html)
        # 3x99.7mm=299.1mm > 297mm(A4) — 마지막 련은 고정 피치가 아닌 내용 높이만
        # 차지해야 1페이지에 3련이 모두 들어간다 (2026-07-04 2페이지 분할 회귀, DEC-075).
        # WeasyPrint 실측: auto-height 만으로는 border-box 98.43mm > 잔여 97.6mm 로
        # 0.83mm 초과해 여전히 2페이지 — 물리 양식지에 대응 기준선이 없는 하단
        # padding/border 도 제거해야 1페이지에 들어간다(DEC-075 보강).
        self.assertIn(
            ".triplicate-section:last-child { margin-bottom: 0; height: auto; "
            "padding-bottom: 0; border-bottom-width: 0; }",
            html,
        )
        self.assertIn(".tri-lines thead th { height: 6.0mm; box-sizing: border-box; }", html)
        self.assertIn(".camount { width: 26.0mm; }", html)
        self.assertIn(".cno { width: 3.8mm; }", html)
        self.assertIn("transform: translate(0.65mm, 1.35mm)", html)
        # 필드 블록 · 푸터 세로 위치 — DEC-387 보정값(2026-10-07 실물 사진)
        self.assertIn(".cust-mini { margin-top: 5.6mm; }", html)
        # DEC-387 (2026-10-07 교문사 실물 사진) — 라벨 칸 20mm(값이 라벨 칸 안에 찍히던 것) · 숫자 오른쪽 여백 2.3mm ·
        # 총부수 · 합계 4.5mm 위로 · 양식지 모드 거래처명 한 줄.
        self.assertIn(".cust-mini .clab { width: 20.0mm; }", html)
        self.assertIn(".tri-lines td.num { padding-right: 2.3mm; }", html)
        self.assertIn(".foot3 { margin-top: 0.3mm; }", html)
        self.assertIn(".preprinted .cust-mini td:not(.clab) { white-space: nowrap; overflow: visible; }", html)
        self.assertIn("<td class='num' style='text-align:right' data-legacy-id='Sobo21.Triplicate.Gssum'>", html)
        # DEC-389 (실물 2차) — 발행일 · 거래처명 값만 3mm 아래(괘선은 그대로) · 표 9pt · 필드 9pt · 값 700 · 칸 안에서 자름.
        # DEC-389 정정(실물 3차) — 발행일 3mm 위 · 거래처명 2mm 위 → date 0(미출력) · name 1mm.
        self.assertNotIn("tr.r-date .cval", html)
        self.assertIn(".cust-mini tr.r-name .cval { position: relative; top: 1mm; }", html)
        self.assertNotIn("tr.r-code .cval", html)
        self.assertIn(".tri-lines tbody td { font-size: 9pt; }", html)
        self.assertIn(".tri-lines tbody td.shelf { font-size: 8pt; }", html)  # DEC-393 서가 칸 1pt 작게
        self.assertIn(".cust-mini td:not(.clab) { font-size: 9pt; }", html)
        self.assertIn(".tri-lines tbody td, .cust-mini td:not(.clab), .foot3 strong { font-weight: 700; }", html)
        self.assertIn(".foot3 strong { font-size: 9.5pt; }", html)  # 총부수 · 합계 숫자도 키움
        self.assertIn(".tri-lines tbody td { white-space: nowrap; overflow: hidden; }", html)
        self.assertIn("<tr class='r-name'><td class='clab'>거래처명</td>", html)
        self.assertIn(".body-flex { flex: 0 0 auto; } .foot3 { margin-top: 0.3mm; }", html)  # DEC-387
        # 헤더(거래처코드/공급자)·푸터도 표와 동일 폭·좌측 정렬 — 스캔상 3블록 좌단 14.2mm 일치
        # (표만 margin-left 를 받아 헤더·푸터가 3.5mm 좌측으로 어긋나던 문제, 2026-07-05).
        self.assertIn(".hdr3 { width: 182.9mm; margin-left: 3.5mm; align-self: flex-start; }", html)
        self.assertIn(
            ".foot3 { width: 182.9mm; margin-left: 3.5mm; align-self: flex-start; "
            "box-sizing: border-box; }",
            html,
        )


class ContractYamlTests(TestCase):
    def test_default_profile_has_calibration_block(self) -> None:
        data = yaml.safe_load(
            (ROOT / "migration" / "contracts" / "print_sales_statement.yaml")
            .read_text(encoding="utf-8")
        )
        cal = data["profiles"]["default"].get("preprinted_calibration")
        self.assertIsInstance(cal, dict)
        for k in ("offset_top_mm", "offset_left_mm", "line_row_height_mm"):
            self.assertIn(k, cal)

    def test_triplicate_first_two_sections_fit_within_a4_page(self) -> None:
        """마지막 련은 auto-height 라 제외해도, 앞의 2련(고정 피치)만으로 A4 297mm 를
        넘으면 마지막 련이 어차피 2페이지로 밀린다 — 회귀 시 반드시 함께 확인.
        """
        data = yaml.safe_load(
            (ROOT / "migration" / "contracts" / "print_sales_statement.yaml")
            .read_text(encoding="utf-8")
        )
        cal = data["profiles"]["default"]["preprinted_calibration"]
        pitch = float(cal["section_pitch_mm"])
        margin_v = float(cal.get("page_margin_v_mm") or 0)
        usable = 297.0 - 2 * margin_v
        self.assertLessEqual(2 * pitch, usable)
