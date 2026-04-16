import sys
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))

from delphi_scalar import decode_delphi_string, layout_value_as_str  # noqa: E402


class TestDelphiScalar(unittest.TestCase):
    def test_decode_simple(self):
        self.assertEqual(decode_delphi_string("'x'"), "x")

    def test_layout_value_list(self):
        self.assertEqual(layout_value_as_str([1, 2]), "[1, 2]")


if __name__ == "__main__":
    unittest.main()
