import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from dfm_grid_columns import extract_grid_columns  # noqa: E402
from dfm_parser import parse_dfm_layout  # noqa: E402


class TestExtractGridColumns(unittest.TestCase):
    def test_sample_blob(self):
        blob = """<
        item
          FieldName = 'HCODE'
          Title.Caption = 'ColA'
        end
        item
          FieldName = 'HNAME'
          Title.Caption = 'ColB'
        end>"""
        cols = extract_grid_columns(blob)
        self.assertEqual(len(cols), 2)
        self.assertEqual(cols[0]["field_name"], "HCODE")
        self.assertEqual(cols[0]["title"], "ColA")
        self.assertEqual(cols[1]["title"], "ColB")

    def test_parse_dfm_layout_exports_grid_columns(self):
        import os
        import tempfile

        content = """object F: TForm
  ClientWidth = 400
  ClientHeight = 300
  object Grid1: TDBGridEh
    Left = 0
    Top = 0
    Width = 100
    Height = 100
    Columns = <
      item
        FieldName = 'A'
        Title.Caption = 'Alpha'
      end
      item
        FieldName = 'B'
        Title.Caption = 'Beta'
      end>
  end
end
"""
        fd, path = tempfile.mkstemp(suffix=".dfm", text=True)
        os.close(fd)
        try:
            Path(path).write_text(content, encoding="utf-8")
            doc = parse_dfm_layout(path)
            root = doc["root"]
            grid = root["children"][0]
            gc = grid["layout"].get("grid_columns")
            self.assertIsNotNone(gc)
            self.assertEqual(len(gc), 2)
            self.assertEqual(gc[0]["title"], "Alpha")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
