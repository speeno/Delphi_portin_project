"""layout_ir(Anchors·TabOrder·z-index) 보강."""

import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from dfm_layout_ir import enrich_layout_document  # noqa: E402


class TestEnrichLayoutIr(unittest.TestCase):
    def test_tab_order_sorts_z_index(self):
        doc = {
            "form_name": "F",
            "form_class": "TForm",
            "root": {
                "name": "Form1",
                "type": "TForm",
                "depth": 0,
                "layout": {"ClientWidth": "100", "ClientHeight": "100"},
                "events": {},
                "children": [
                    {
                        "name": "A",
                        "type": "TPanel",
                        "depth": 1,
                        "layout": {"Left": "0", "Top": "0", "Width": "10", "Height": "10", "TabOrder": "2"},
                        "events": {},
                        "children": [],
                    },
                    {
                        "name": "B",
                        "type": "TPanel",
                        "depth": 1,
                        "layout": {"Left": "10", "Top": "0", "Width": "10", "Height": "10", "TabOrder": "0"},
                        "events": {},
                        "children": [],
                    },
                ],
            },
        }
        enrich_layout_document(doc)
        ch = doc["root"]["children"]
        z_by_name = {c["name"]: c["layout_ir"]["z_index"] for c in ch}
        self.assertLess(z_by_name["B"], z_by_name["A"])

    def test_anchors_parsed(self):
        doc = {
            "form_name": "F",
            "form_class": "TForm",
            "root": {
                "name": "Form1",
                "type": "TForm",
                "depth": 0,
                "layout": {},
                "events": {},
                "children": [
                    {
                        "name": "P1",
                        "type": "TPanel",
                        "depth": 1,
                        "layout": {"Anchors": "[akLeft, akTop, akRight]", "TabOrder": "0"},
                        "events": {},
                        "children": [],
                    }
                ],
            },
        }
        enrich_layout_document(doc)
        ir = doc["root"]["children"][0]["layout_ir"]
        self.assertIn("akRight", ir["anchors"])


if __name__ == "__main__":
    unittest.main()
