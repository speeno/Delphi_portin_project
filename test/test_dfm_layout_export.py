"""parse_dfm_layout / 레이아웃 JSON에 좌표 속성이 포함되는지 검증."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))
from dfm_parser import parse_dfm_layout  # noqa: E402


class TestParseDfmLayout(unittest.TestCase):
    def test_subu36_has_client_and_child_left(self):
        dfm = _REPO / "legacy_delphi_source" / "legacy_source" / "Data" / "Subu36.dfm"
        if not dfm.is_file():
            self.skipTest("fixture dfm missing")
        data = parse_dfm_layout(str(dfm))
        self.assertIsNotNone(data.get("root"))
        root = data["root"]
        self.assertEqual(root["layout"].get("ClientWidth"), "901")
        self.assertEqual(root["layout"].get("ClientHeight"), "533")
        children = root.get("children") or []
        self.assertTrue(len(children) >= 1)
        first = children[0]
        self.assertIn("Left", first["layout"])
        self.assertIn("Top", first["layout"])

    def test_minimal_dfm(self):
        content = """object TestF: TTestForm
  Left = 0
  Top = 0
  Caption = 'Hi'
  ClientHeight = 200
  ClientWidth = 300
  object Btn1: TButton
    Left = 10
    Top = 20
    Width = 80
    Height = 25
    Caption = 'OK'
    TabOrder = 1
  end
end
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".dfm", delete=False, encoding="utf-8") as f:
            f.write(content)
            path = f.name
        try:
            data = parse_dfm_layout(path)
            self.assertEqual(data["form_name"], "TestF")
            self.assertEqual(data["root"]["layout"]["ClientWidth"], "300")
            btn = data["root"]["children"][0]
            self.assertEqual(btn["name"], "Btn1")
            self.assertEqual(btn["layout"]["Left"], "10")
            self.assertEqual(btn["layout_ir"]["tab_order"], 1)
            self.assertIn("z_index", btn["layout_ir"])
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
