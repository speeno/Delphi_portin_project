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
        self.assertIn(".tri-lines td { height: 6.2mm; }", html)

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
        self.assertEqual(
            tx._preprinted_calibration_css(
                {"preprinted_calibration": {"offset_top_mm": "abc"}},
                line_row_selector=".x td",
            ),
            "",
        )
        self.assertEqual(
            tx._preprinted_calibration_css({}, line_row_selector=".x td"), "",
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
