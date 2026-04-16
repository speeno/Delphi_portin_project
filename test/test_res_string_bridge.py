import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools"))

from res_string_bridge import (  # noqa: E402
    extract_resourcestrings_from_pas,
    parse_rc_stringtable_entries,
)


class TestRcStringtable(unittest.TestCase):
    def test_parse_lines(self):
        rc = """
STRINGTABLE
BEGIN
  100, "Hello"
  200, "Second"
END
"""
        d = parse_rc_stringtable_entries(rc)
        self.assertEqual(d.get(100), "Hello")
        self.assertEqual(d.get(200), "Second")


class TestPasResourcestring(unittest.TestCase):
    def test_extract_from_pas_text(self):
        import os

        pas = (
            "unit U;\ninterface\nresourcestring\n"
            "SHello = 'Hi';\n"
            "SBye = 'Bye';\n"
            "implementation\nend.\n"
        )
        fd, path = tempfile.mkstemp(suffix=".pas", text=True)
        os.close(fd)
        try:
            Path(path).write_text(pas, encoding="utf-8")
            out = extract_resourcestrings_from_pas(path)
            self.assertEqual(out.get("SHello"), "Hi")
            self.assertEqual(out.get("SBye"), "Bye")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
