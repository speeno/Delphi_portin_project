"""DFM 다중 줄 속성 병합 및 파서 회귀."""

import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from dfm_merge_blocks import merge_property_blocks  # noqa: E402
from dfm_parser import is_binary_dfm_text, parse_dfm_layout  # noqa: E402


class TestMergePropertyBlocks(unittest.TestCase):
    def test_items_strings_merged_to_one_logical_line(self):
        lines = [
            "  Items.Strings = (",
            "    'A'",
            "    'B')",
        ]
        out = merge_property_blocks(lines)
        self.assertEqual(len(out), 1)
        self.assertIn("Items.Strings", out[0])
        self.assertIn("'A'", out[0])
        self.assertIn("'B')", out[0])

    def test_columns_angle_block_merged(self):
        lines = [
            "      Columns = <",
            "        item",
            "          Title.Caption = 'A'",
            "        end",
            "        item",
            "          Title.Caption = 'B'",
            "        end>",
        ]
        out = merge_property_blocks(lines)
        self.assertEqual(len(out), 1)
        self.assertIn("Columns = <", out[0])
        self.assertIn("end>", out[0])

    def test_glyph_data_merged(self):
        lines = [
            "    Glyph.Data = {",
            "      0102",
            "      0304}",
            "    NumGlyphs = 2",
        ]
        out = merge_property_blocks(lines)
        self.assertEqual(len(out), 2)
        self.assertIn("Glyph.Data", out[0])
        self.assertIn("0304}", out[0])
        self.assertIn("NumGlyphs", out[1])


class TestParseDfmLayoutFixtures(unittest.TestCase):
    def test_fixture_items_strings_in_layout(self):
        dfm = _REPO / "test" / "fixtures" / "dfm_multiline_items.dfm"
        data = parse_dfm_layout(str(dfm))
        self.assertIsNotNone(data.get("root"))
        root = data["root"]
        combo = root["children"][0]
        self.assertEqual(combo["name"], "Combo1")
        items = combo["layout"].get("Items.Strings", "")
        self.assertIn("One", items)
        self.assertIn("Two", items)

    def test_fixture_glyph_and_numglyphs(self):
        dfm = _REPO / "test" / "fixtures" / "dfm_glyph_block.dfm"
        data = parse_dfm_layout(str(dfm))
        root = data["root"]
        btn = root["children"][0]
        self.assertEqual(btn["name"], "Btn1")
        self.assertIn("Glyph.Data", btn["layout"])
        self.assertIn("01020304", btn["layout"]["Glyph.Data"])
        self.assertEqual(btn["layout"].get("NumGlyphs"), "2")

    def test_binary_dfm_returns_error_doc(self):
        content = "TPF0" + "\n"
        self.assertTrue(is_binary_dfm_text(content))
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".dfm", delete=False, encoding="utf-8") as f:
            f.write(content)
            path = f.name
        try:
            data = parse_dfm_layout(path)
            self.assertIsNone(data.get("root"))
            self.assertIn("parse_error", data)
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
