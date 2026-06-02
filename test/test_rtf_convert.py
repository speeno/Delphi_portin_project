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

    def test_rtf_bold_internal_html(self) -> None:
        rtf = r"{\rtf1\ansi\pard\b bold\b0 normal\par}"
        out = rtf_to_html(rtf)
        self.assertRegex(out, r"<strong>\s*bold\s*</strong>")
        self.assertIn("normal", out)

    def test_rtf_unicode_plain(self) -> None:
        rtf = r"{\\rtf1\\ansi\\pard \\u54861?\\par}"
        plain = rtf_to_plain(rtf)
        self.assertTrue(plain)

    def test_fonttbl_hex_not_in_plain(self) -> None:
        """fonttbl 의 폰트명 hex 가 본문 평문에 섞이지 않아야 함."""
        # 나눔바른고딕 (cp949) + 굴림 (cp949) in fonttbl only
        font_nanum = "".join(f"\\'{b:02x}" for b in "나눔바른고딕".encode("cp949"))
        font_gulim = "".join(f"\\'{b:02x}" for b in "굴림".encode("cp949"))
        body = "".join(f"\\'{b:02x}" for b in "안성점 오픈예정".encode("cp949"))
        rtf = (
            r"{\rtf1\ansi\deff0"
            r"{\fonttbl{\f0\fcharset129 " + font_nanum + r";"
            r"\f1\fcharset129 " + font_gulim + r";}}"
            r"\pard\f0 " + body + r"\par}"
        )
        plain = rtf_to_plain(rtf)
        self.assertIn("안성점", plain)
        self.assertNotIn("나눔바른고딕", plain)
        self.assertNotIn("굴림", plain)
        html_out = rtf_to_html(rtf)
        self.assertIn("안성점", html_out)
        self.assertNotIn("나눔바른고딕", html_out)

    def test_multiline_paragraphs(self) -> None:
        line1 = "".join(f"\\'{b:02x}" for b in "첫줄".encode("cp949"))
        line2 = "".join(f"\\'{b:02x}" for b in "둘째줄".encode("cp949"))
        rtf = r"{\rtf1\ansi\pard " + line1 + r"\par\pard " + line2 + r"\par}"
        plain = rtf_to_plain(rtf)
        self.assertIn("첫줄", plain)
        self.assertIn("둘째줄", plain)
        self.assertIn("\n", plain)


if __name__ == "__main__":
    from unittest import main

    main()
