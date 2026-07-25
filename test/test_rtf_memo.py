"""G7_Ggeo.Memos RTF 변환 — `rtf_memo` 회귀 가드 (DEC-129 계약 메모장).

레거시 TRichEdit RTF(cp949 \\'xx) ↔ 플레인/HTML. 골든: book_kb 0013 실데이터 검증
(2026-07-25). 함정: ``\\pard`` 는 ``\\par`` 보다 먼저 제거해야 'd' 잔여물이 없다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services.rtf_memo import (  # noqa: E402
    html_to_rtf,
    rtf_to_html,
    rtf_to_text,
    text_to_rtf,
)

# 레거시 실데이터 축약형(cp949 이스케이프 + \pard 경계 + \par 개행)
_LEGACY_RTF = (
    "{\\rtf1\\ansi\\ansicpg949\\deff0{\\fonttbl{\\f0\\fnil\\fcharset129 \\'b1\\'bc\\'b8\\'b2;}}\r\n"
    "\\viewkind4\\uc1\\pard\\f0\\fs20 2018.3.12\\'c3\\'d6\\'c3\\'ca\\'b0\\'e8\\'be\\'e0.\\par\r\n"
    "\\b \\'b0\\'ad\\'c1\\'b6\\b0 \\par\r\n}\r\n"
)


class RtfTextTests(TestCase):
    def test_legacy_parse_no_pard_residue(self) -> None:
        txt = rtf_to_text(_LEGACY_RTF)
        self.assertTrue(txt.startswith("2018.3.12최초계약."), txt)  # 'd' 잔여물 없음
        self.assertIn("강조", txt)

    def test_text_roundtrip(self) -> None:
        sample = "2026.1.1 재고비2원 인상 적용함.\n다음 줄 {특수}\\문자"
        self.assertEqual(rtf_to_text(text_to_rtf(sample)), sample)

    def test_plain_passthrough(self) -> None:
        self.assertEqual(rtf_to_text("그냥 텍스트"), "그냥 텍스트")


class RtfHtmlTests(TestCase):
    def test_legacy_bold_to_html(self) -> None:
        html = rtf_to_html(_LEGACY_RTF)
        self.assertIn("2018.3.12최초계약.", html)
        self.assertIn("<b>강조</b>", html)
        self.assertIn("<br>", html)

    def test_html_roundtrip_biu(self) -> None:
        h = "첫줄 <b>굵게</b> 그리고 <u>밑줄</u><br>둘째줄 <i>기울임</i> {특수}\\문자"
        back = rtf_to_html(html_to_rtf(h))
        for frag in ("<b>굵게</b>", "<u>밑줄</u>", "<i>기울임</i>", "<br>", "{특수}\\문자"):
            self.assertIn(frag, back)

    def test_contenteditable_divs_become_newlines(self) -> None:
        # contentEditable 은 줄을 <div>…</div> 로 감싼다 — \par 로 변환돼야.
        rt = html_to_rtf("<div>첫줄</div><div>둘째줄</div>")
        self.assertEqual(rtf_to_text(rt), "첫줄\n둘째줄")

    def test_html_escape_on_display(self) -> None:
        # 플레인 저장분에 태그 문자가 있어도 escape 되어 표시.
        self.assertEqual(rtf_to_html("a<b>&c"), "a&lt;b&gt;&amp;c")


if __name__ == "__main__":
    main()
