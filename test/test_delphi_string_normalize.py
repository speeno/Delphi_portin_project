import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from delphi_string_normalize import normalize_delphi_display_string  # noqa: E402


class TestNormalizeDelphiDisplayString(unittest.TestCase):
    def test_adjacent_quoted_chunks(self):
        s = "'a'#13#10'b'"
        out = normalize_delphi_display_string(s)
        self.assertEqual(out, "a\r\nb")

    def test_double_single_quote(self):
        self.assertEqual(normalize_delphi_display_string("'a''b'"), "a'b")


if __name__ == "__main__":
    unittest.main()
