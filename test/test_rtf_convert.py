"""G1 Memos RTF ↔ HTML 변환 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.rtf_convert import (  # noqa: E402
    html_to_rtf,
    rtf_to_html,
    rtf_to_plain,
    sanitize_html,
)


class RtfConvertTest(TestCase):
    def test_plain_passthrough(self) -> None:
        self.assertEqual(rtf_to_plain("hello"), "hello")

    def test_rtf_cp949_hex_line(self) -> None:
        # "가" in cp949 hex
        rtf = "{\\rtf1\\ansi\\pard \\'b0\\'a1\\par}"
        plain = rtf_to_plain(rtf)
        self.assertIn("가", plain)

    def test_html_roundtrip_smoke(self) -> None:
        html = "<p><strong>OK</strong></p>"
        blob = html_to_rtf(sanitize_html(html))
        self.assertTrue(blob.startswith(b"{\\rtf"))
        plain = rtf_to_plain(blob)
        self.assertIn("OK", plain)

    def test_sanitize_strips_script(self) -> None:
        dirty = '<p>ok</p><script>alert(1)</script>'
        clean = sanitize_html(dirty)
        self.assertNotIn("script", clean.lower())


if __name__ == "__main__":
    from unittest import main

    main()
