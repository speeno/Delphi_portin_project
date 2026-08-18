"""dfm2html 레이아웃 어댑터 vs legacy 스키마 호환."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))
sys.path.insert(0, str(_REPO / "tools"))

from dfm_parser import parse_dfm_layout  # noqa: E402

# 선택 엔진 — 외부 dfm2html_project(별도 체크아웃, 허브 저장소 미포함) 가 없으면 어댑터
# import 자체가 ModuleNotFoundError. 실행 환경에 프로젝트가 있을 때만 검증한다.
_DFM2HTML_PROJECT = _REPO / "tools" / "dfm2html_project"


@unittest.skipUnless(
    _DFM2HTML_PROJECT.is_dir(),
    "tools/dfm2html_project 미체크아웃 — dfm2html 선택 엔진 테스트 건너뜀",
)
class TestDfm2HtmlAdapter(unittest.TestCase):
    def test_engine_dfm2html_matches_form_meta(self):
        from dfm2html_layout_adapter import parse_dfm_layout_via_dfm2html  # noqa: E402

        content = """object F: TForm
  ClientWidth = 400
  ClientHeight = 300
  object Btn: TButton
    Left = 10
    Top = 10
    Width = 75
    Height = 25
    Caption = 'OK'
  end
end
"""
        fd, path = tempfile.mkstemp(suffix=".dfm", text=True)
        os.close(fd)
        try:
            Path(path).write_text(content, encoding="utf-8")
            d2 = parse_dfm_layout_via_dfm2html(path)
            leg = parse_dfm_layout(path)
            self.assertEqual(d2["form_name"], leg["form_name"])
            self.assertEqual(d2["engine"], "dfm2html")
            btn = d2["root"]["children"][0]
            self.assertEqual(btn["layout"].get("Caption"), "OK")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
