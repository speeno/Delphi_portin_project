"""시각 회귀: 기본은 HTML 생성 검증만(Playwright는 선택)."""

import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools"))
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from dfm_layout_to_html import build_html  # noqa: E402


class TestDfmHtmlBuild(unittest.TestCase):
    def test_pagecontrol_emits_tabstrip(self):
        doc = {
            "form_name": "F",
            "form_class": "TForm",
            "root": {
                "name": "Form1",
                "type": "TForm",
                "depth": 0,
                "layout": {"ClientWidth": "400", "ClientHeight": "300"},
                "events": {},
                "children": [
                    {
                        "name": "PageControl1",
                        "type": "TPageControl",
                        "depth": 1,
                        "layout": {"Left": "0", "Top": "0", "Width": "400", "Height": "300", "TabOrder": "0"},
                        "events": {},
                        "children": [
                            {
                                "name": "TabSheet1",
                                "type": "TTabSheet",
                                "depth": 2,
                                "layout": {"Caption": "TabA", "TabOrder": "0"},
                                "events": {},
                                "children": [],
                            },
                            {
                                "name": "TabSheet2",
                                "type": "TTabSheet",
                                "depth": 2,
                                "layout": {"Caption": "TabB", "TabOrder": "1"},
                                "events": {},
                                "children": [],
                            },
                        ],
                    }
                ],
            },
        }
        html_out = build_html(doc)
        self.assertIn("delphi-pagecontrol", html_out)
        self.assertIn("delphi-tabstrip", html_out)
        self.assertIn("TabA", html_out)
        self.assertIn("TabB", html_out)

    def test_grid_has_header_row(self):
        doc = {
            "form_name": "G",
            "form_class": "TForm",
            "root": {
                "name": "Form1",
                "type": "TForm",
                "depth": 0,
                "layout": {"ClientWidth": "200", "ClientHeight": "150"},
                "events": {},
                "children": [
                    {
                        "name": "Grid1",
                        "type": "TStringGrid",
                        "depth": 1,
                        "layout": {"Left": "0", "Top": "0", "Width": "200", "Height": "150", "TabOrder": "0"},
                        "events": {},
                        "children": [],
                    }
                ],
            },
        }
        html_out = build_html(doc)
        self.assertIn("delphi-grid-header", html_out)
        self.assertIn("delphi-grid-body", html_out)


if __name__ == "__main__":
    unittest.main()
