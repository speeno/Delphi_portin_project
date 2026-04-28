"""회귀: 거래명세서 ``layout=legacy_triplicate`` HTML 및 프로필."""
from __future__ import annotations

import base64
import unittest
from unittest.mock import patch

_MINI_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
    "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
)


class SalesStatementTriplicateTests(unittest.TestCase):
    def _detail(self) -> dict:
        return {
            "order_key": {
                "gdate": "2026.04.01",
                "hcode": "H01",
                "jubun": "99",
                "gjisa": "",
            },
            "customer": {"hcode": "H01", "gname": "테스트서점"},
            "lines": [
                {
                    "gcode": "G1",
                    "bcode": "BOOK1",
                    "product_name": "도서A",
                    "shelf": "A-1",
                    "pubun": "정간",
                    "gsqut": 2,
                    "gssum": 10000,
                    "gbigo": "",
                    "gdang": 5000,
                    "grat1": 10,
                },
            ],
        }

    def test_default_layout_still_renders_two_copy_statement(self) -> None:
        from app.services.transactions_service import render_sales_statement_html

        html = render_sales_statement_html(
            self._detail(),
            layout="default",
            server_id="remote_test",
        )
        self.assertIn("Sobo21.Print.Copy.buyer", html)
        self.assertIn("Sobo21.Print.Copy.seller", html)
        self.assertIn("공급받는자보관용", html)
        self.assertIn("공급자보관용", html)
        self.assertLess(html.index("공급자보관용"), html.index("공급받는자보관용"))
        self.assertIn("statement-cut-line", html)
        self.assertIn("Sobo21.Print.StatementPage", html)
        self.assertIn("<th>구분</th>", html)
        self.assertIn("소계부수", html)
        self.assertIn("소계금액", html)
        self.assertIn("Sobo21.Header.PageFraction", html)
        self.assertNotIn("Sobo21.Print.Triplicate.receipt", html)
        self.assertNotIn("Sobo21.Triplicate.SealOverlay", html)

    def test_default_layout_pagination_respects_a4_dual_block_rows(self) -> None:
        """A4 표준은 YAML ``a4_dual_block_rows_per_page``(기본 16)로 청크 분할한다."""
        from app.services.transactions_service import render_sales_statement_html

        lines = []
        for i in range(17):
            lines.append(
                {
                    "gcode": f"G{i}",
                    "bcode": "B",
                    "product_name": f"도서{i}",
                    "gsqut": 1,
                    "gssum": 1000,
                    "gdang": 1000,
                    "grat1": 0,
                    "gbigo": "",
                },
            )
        detail = {**self._detail(), "lines": lines}
        html = render_sales_statement_html(
            detail,
            layout="default",
            server_id="remote_test",
        )
        self.assertEqual(html.count("Sobo21.Print.StatementPage"), 2)
        self.assertIn("Sobo21.Header.PageFraction", html)
        self.assertIn("1/2", html)
        self.assertIn("2/2", html)

    def test_legacy_triplicate_contains_three_sections_and_columns(self) -> None:
        from app.services.barcode_svg_service import is_barcode_engine_available
        from app.services.transactions_service import render_sales_statement_html

        html = render_sales_statement_html(
            self._detail(),
            layout="legacy_triplicate",
            server_id="remote_test",
        )
        self.assertIn("Sobo21.Print.Triplicate.supplier", html)
        self.assertIn("Sobo21.Print.Triplicate.buyer", html)
        self.assertIn("Sobo21.Print.Triplicate.receipt", html)
        self.assertIn("(공급자 보관용)", html)
        self.assertIn("(공급받는자 보관용)", html)
        self.assertIn("(인수증)", html)
        self.assertIn("<th>No.</th>", html)
        self.assertIn("서가번호", html)
        self.assertIn("supplier-vlabel", html)
        self.assertIn("공<br>급<br>자", html)
        self.assertIn("국민은행 009-25-0000-648", html)
        self.assertIn("※반품처 천일화물 파주광탄", html)
        self.assertIn("Sobo21.Triplicate.FooterBank", html)
        self.assertIn("Sobo21.Triplicate.VerticalNote", html)
        if is_barcode_engine_available():
            self.assertIn("Sobo21.Triplicate.SlipBarcode", html)

    def test_legacy_triplicate_seal_overlay_when_bytes_present(self) -> None:
        from app.services.transactions_service import render_sales_statement_html

        with patch(
            "app.services.tenant_print_assets.read_seal_bytes",
            return_value=_MINI_PNG,
        ):
            html = render_sales_statement_html(
                self._detail(),
                layout="legacy_triplicate",
                server_id="remote_test",
            )
        self.assertIn("Sobo21.Triplicate.SealOverlay", html)
        self.assertIn("data:image/png;base64,", html)

    def test_legacy_triplicate_pagination_over_ten_lines(self) -> None:
        from app.services.transactions_service import render_sales_statement_html

        lines = []
        for i in range(11):
            lines.append(
                {
                    "gcode": f"G{i}",
                    "bcode": "B",
                    "product_name": f"도서{i}",
                    "gsqut": 1,
                    "gssum": 1000,
                    "gdang": 1000,
                    "grat1": 0,
                    "gbigo": "",
                },
            )
        detail = {
            **self._detail(),
            "lines": lines,
        }
        html = render_sales_statement_html(
            detail,
            layout="legacy_triplicate",
            server_id="remote_test",
        )
        self.assertEqual(html.count("<div class='triplicate-sheet'"), 2)
        self.assertIn("총 2장 중 1장", html)
        self.assertIn("총 2장 중 2장", html)

    def test_bank_footer_from_user_preferences_over_yaml(self) -> None:
        from app.services.transactions_service import render_sales_statement_html

        with patch(
            "app.services.user_profile_service.get_profile",
            return_value={
                "preferences": {
                    "sales_statement_bank_footer_lines": [
                        "우리은행 123-456-789 예금주:테스트",
                    ],
                },
                "logo_relpath": "",
            },
        ):
            html = render_sales_statement_html(
                self._detail(),
                layout="legacy_triplicate",
                server_id="remote_test",
                user_id="user1",
            )
        self.assertIn("우리은행 123-456-789 예금주:테스트", html)
        self.assertNotIn("국민은행 009-25-0000-648", html)

    def test_supplier_fields_from_user_preferences_over_yaml(self) -> None:
        from app.services.transactions_service import render_sales_statement_html

        with patch(
            "app.services.user_profile_service.get_profile",
            return_value={
                "preferences": {
                    "sales_statement_supplier_fields": {
                        "등록번호": "111-22-33333",
                        "상호": "(주)사용자서점",
                        "성명": "홍길동",
                        "사업장주소": "서울시 테스트구 1",
                        "업태": "도소매",
                        "종목": "서적",
                        "전화번호": "02-111-2222",
                        "팩스": "02-333-4444",
                    },
                    "sales_statement_vertical_note": "※사용자 반품 안내",
                },
                "logo_relpath": "",
            },
        ):
            html = render_sales_statement_html(
                self._detail(),
                layout="legacy_triplicate",
                server_id="remote_test",
                user_id="user1",
            )
        self.assertIn("111-22-33333", html)
        self.assertIn("(주)사용자서점", html)
        self.assertIn("※사용자 반품 안내", html)
        self.assertNotIn("102-81-23967", html)


if __name__ == "__main__":
    unittest.main()
