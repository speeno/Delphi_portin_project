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
        self.assertIn("@page { size: 210mm 297mm; margin: 6mm 8mm; }", html)
        self.assertIn("font-size: 7.8pt", html)
        self.assertIn("border: 1.4px solid #111", html)
        self.assertNotIn("#0b4f86", html)
        self.assertNotIn("#263f34", html)
        self.assertNotIn("#9c2726", html)
        self.assertNotIn("Sobo21.Print.Triplicate.receipt", html)
        self.assertNotIn("Sobo21.Triplicate.SealOverlay", html)

    def test_default_layout_pagination_respects_a4_dual_block_rows(self) -> None:
        """A4 표준은 YAML ``a4_dual_block_rows_per_page``(기본 14)로 청크 분할한다."""
        from app.services.transactions_service import render_sales_statement_html

        lines = []
        for i in range(15):
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
        # 세로쓰기 대체 — WeasyPrint 는 writing-mode/text-orientation 미지원(unknown property 로
        # 무시)이라 실제 PDF 에서 가로쓰기 줄바꿈으로 뒤섞여 보였다. 글자 단위 <br> 로 쌓아
        # 세로 한 줄 고정(2026-07-04 보고, DEC-075 보강).
        self.assertIn("※<br>반<br>품<br>처<br> <br>천<br>일<br>화<br>물<br> <br>파<br>주<br>광<br>탄", html)
        self.assertNotIn("writing-mode", html)
        self.assertNotIn("text-orientation", html)
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
        # 스캔 실측 재캘리브레이션(2026-07-05) — 도장 지름 18.5mm, 공급자 블록 우상단 기준
        # 음수 오프셋(위/오른쪽)으로 등록번호/성명 상단에 얹힘(중심 y≈12mm).
        self.assertIn("width:18.5mm", html)
        self.assertIn("top:-4.5mm", html)
        self.assertIn("right:-1.5mm", html)
        # 도장은 테두리 출력(borders=on)에서만 — 양식지(borders=off) 모드에선 supplier-stack 과
        # 함께 숨김. 강제 표시 예외가 없어야 한다(사용자 요청 2026-07-07).
        self.assertNotIn(".preprinted .seal-overlay { visibility: visible; }", html)
        # 세로문구는 표를 밀지 않도록 absolute + 스캔 중심(199.7mm) 정렬용 우측 이동.
        self.assertIn("right: -0.9mm", html)
        # 섹션 외곽 테두리는 투명 — 스캔엔 내용 블록별 테두리만 있고 감싸는 바깥 사각형이 없다.
        # (표 우측 197mm 을 지나 202mm 에 그려져 세로문구를 가두던 외곽선 제거, 2026-07-05)
        self.assertIn("border: 1.6px solid transparent", html)
        # 섹션 인라인 스타일에 border-color 가 없어야 CSS 투명이 안 덮인다(--ink 만 유지).
        # (인라인 border-color 는 ';border-color:' 패턴 — .preprinted CSS 의 '{ border-color:' 와 구분)
        self.assertNotIn(";border-color:", html)
        self.assertIn("class='triplicate-section' style='--ink:", html)

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

    def test_legacy_triplicate_renders_single_pdf_page(self) -> None:
        """삼련(공급자/공급받는자/인수증) 3련이 실제 PDF 1페이지에 모두 들어가야 한다.

        회귀: section_pitch_mm 이 물리 실측값으로 갱신되며 3x99.7mm=299.1mm 가 A4
        297mm 를 초과해 마지막 련(인수증)이 통째로 2페이지로 밀린 적이 있다
        (2026-07-04, DEC-075). HTML 문자열 검사만으로는 실제 페이지 분할 여부를
        알 수 없으므로 WeasyPrint 로 실제 렌더링해 페이지 수를 확인한다.
        """
        try:
            from weasyprint import HTML  # type: ignore[import-not-found]
        except (ImportError, OSError) as exc:
            self.skipTest(f"WeasyPrint native deps unavailable: {exc}")

        from app.services.transactions_service import render_sales_statement_html

        for borders in (True, False):
            html = render_sales_statement_html(
                self._detail(),
                layout="legacy_triplicate",
                server_id="remote_test",
                borders=borders,
            )
            doc = HTML(string=html).render()
            self.assertEqual(
                len(doc.pages),
                1,
                f"borders={borders}: 삼련 3종이 1페이지에 모두 출력되어야 함",
            )

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
        # 세로쓰기 대체 — 글자 단위 <br> 로 쌓는다(위 VerticalNote 테스트 참고).
        self.assertIn("※<br>사<br>용<br>자<br> <br>반<br>품<br> <br>안<br>내", html)
        self.assertNotIn("102-81-23967", html)


if __name__ == "__main__":
    unittest.main()
