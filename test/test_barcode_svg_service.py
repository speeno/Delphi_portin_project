"""회귀: ``barcode_svg_service`` (다중 심볼) + IR 컨텍스트 치환 후 바코드 div 업그레이드."""
from __future__ import annotations

import unittest


class BarcodeSvgServiceTests(unittest.TestCase):
    def test_normalize_barcode_payload_strips_space_hyphen(self) -> None:
        from app.services.barcode_svg_service import normalize_barcode_payload

        self.assertEqual(normalize_barcode_payload(" 978-89-3643-426-0 "), "978-89-3643-426-0")

    def test_list_supported_symbologies(self) -> None:
        from app.services.barcode_svg_service import list_supported_symbologies

        s = list_supported_symbologies()
        self.assertIn("code128", s)
        self.assertIn("ean13", s)
        self.assertIn("qr", s)

    def test_prepare_ean13_rejects_short(self) -> None:
        from app.services.barcode_svg_service import prepare_barcode_payload

        p, err = prepare_barcode_payload("ean13", "12345")
        self.assertIsNone(p)
        self.assertIsNotNone(err)

    def test_prepare_qr_accepts_utf8(self) -> None:
        from app.services.barcode_svg_service import prepare_barcode_payload

        p, err = prepare_barcode_payload("qr", " 한글 테스트 ")
        self.assertEqual(err, None)
        assert p is not None
        self.assertTrue(p.startswith("한글"))

    def test_render_barcode_svg_for_print_returns_svg_or_none(self) -> None:
        from app.services.barcode_svg_service import (
            is_barcode_engine_available,
            render_barcode_svg_for_print,
        )

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        svg = render_barcode_svg_for_print("9788936434260", 40.0, 12.0, symbology="code128")
        self.assertIsNotNone(svg)
        assert svg is not None
        self.assertIn("<svg", svg)
        self.assertIn("viewBox=", svg)
        self.assertIn('width="40.0mm"', svg)
        self.assertIn('height="12.0mm"', svg)
        self.assertIn("preserveAspectRatio", svg)
        self.assertIn("data-frf-symbology", svg)

    def test_render_ean13_svg(self) -> None:
        from app.services.barcode_svg_service import (
            is_barcode_engine_available,
            render_barcode_svg_for_print,
        )

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        svg = render_barcode_svg_for_print("590123412345", 42.0, 16.0, symbology="ean13")
        self.assertIsNotNone(svg)
        assert svg is not None
        self.assertIn("data-frf-symbology=\"ean13\"", svg)

    def test_render_qr_svg_when_segno(self) -> None:
        from app.services.barcode_svg_service import (
            is_qr_engine_available,
            render_barcode_svg_for_print,
        )

        if not is_qr_engine_available():
            self.skipTest("segno 미설치")
        svg = render_barcode_svg_for_print("https://example.com/x", 24.0, 24.0, symbology="qr")
        self.assertIsNotNone(svg)
        assert svg is not None
        self.assertIn("data-frf-symbology=\"qr\"", svg)

    def test_upgrade_frp_barcode_div_plain_text(self) -> None:
        from app.services.barcode_svg_service import (
            is_barcode_engine_available,
            upgrade_frp_barcode_div_plain_text,
        )

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        html = (
            "<div class='frf-barcode' data-legacy-id='X' "
            "style='left:1mm; top:1mm; width:35mm; height:10mm;'>9788936434260</div>"
        )
        out = upgrade_frp_barcode_div_plain_text(html)
        self.assertIn("frf-barcode--svg", out)
        self.assertIn("<svg", out)
        self.assertNotIn("9788936434260</div>", out)

    def test_upgrade_respects_data_frp_symbology_ean13(self) -> None:
        from app.services.barcode_svg_service import (
            is_barcode_engine_available,
            upgrade_frp_barcode_div_plain_text,
        )

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        html = (
            "<div class='frf-barcode' data-frf-symbology=\"ean13\" data-legacy-id='X' "
            "style='left:1mm; top:1mm; width:40mm; height:14mm;'>590123412345</div>"
        )
        out = upgrade_frp_barcode_div_plain_text(html)
        self.assertIn("frf-barcode--svg", out)
        self.assertIn("data-frf-symbology=\"ean13\"", out)

    def test_upgrade_frp_barcode_div_double_quoted_class(self) -> None:
        from app.services.barcode_svg_service import (
            is_barcode_engine_available,
            upgrade_frp_barcode_div_plain_text,
        )

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        html = (
            '<div class="frf-barcode" data-legacy-id="X" '
            'style="left:1mm; top:1mm; width:35mm; height:10mm;">9788936434260</div>'
        )
        out = upgrade_frp_barcode_div_plain_text(html)
        self.assertIn("frf-barcode--svg", out)
        self.assertIn("<svg", out)

    def test_embedded_barcode_html_fragment(self) -> None:
        from app.services.barcode_svg_service import (
            embedded_barcode_html_fragment,
            is_barcode_engine_available,
        )

        self.assertEqual(embedded_barcode_html_fragment("", 40.0, 12.0), "")

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        frag = embedded_barcode_html_fragment(
            "SHIP-001",
            44.0,
            11.0,
            legacy_id="Print.Test.Slip",
            svg_container_class="print-slip-barcode",
            fallback_container_class="print-slip-fallback",
        )
        self.assertIn("data-legacy-id='Print.Test.Slip'", frag)
        self.assertIn("print-slip-barcode", frag)
        self.assertIn("<svg", frag)

    def test_outbound_statement_html_includes_slip_barcode(self) -> None:
        from app.services.barcode_svg_service import is_barcode_engine_available
        from app.services.outbound_service import render_outbound_statement_html

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        detail = {
            "customer": {"gname": "테스트", "hcode": "H001"},
            "order_key": {"gdate": "2026.04.01", "jubun": "J999"},
            "lines": [
                {
                    "gcode": "G1",
                    "product_name": "BOOK",
                    "pubun": "",
                    "gsqut": 1,
                    "gssum": 1000,
                },
            ],
        }
        html = render_outbound_statement_html(detail)
        self.assertIn("Sobo27.Header.SlipBarcode", html)
        self.assertIn("<svg", html)

    def test_render_template_with_context_upgrades_barcode(self) -> None:
        from app.services.barcode_svg_service import is_barcode_engine_available
        from app.services.print_ir_compiler import render_template_with_context

        if not is_barcode_engine_available():
            self.skipTest("python-barcode 미설치")
        html = (
            "<div class='frf-barcode' style='left:0mm; top:0mm; width:30mm; height:8mm;'>"
            "{{ ctx.isbn }}</div>"
        )
        out = render_template_with_context(html, {"isbn": "9788936434260"})
        self.assertIn("<svg", out)
        self.assertIn("frf-barcode--svg", out)

    def test_decode_returns_empty_without_pyzbar(self) -> None:
        from app.services.barcode_svg_service import (
            decode_barcodes_from_image_bytes,
            is_decode_engine_available,
        )

        if is_decode_engine_available():
            self.skipTest("pyzbar 설치됨 — 빈 입력만 검증")
        self.assertEqual(decode_barcodes_from_image_bytes(b"\x89PNG\r\n\x1a\n"), [])


if __name__ == "__main__":
    unittest.main()
