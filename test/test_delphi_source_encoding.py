"""delphi_source_encoding: CP949·UTF-8 폴백."""
import tempfile
import unittest
from pathlib import Path

import sys

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))
from delphi_source_encoding import read_delphi_source  # noqa: E402


class TestReadDelphiSource(unittest.TestCase):
    def test_cp949_korean_string(self):
        # "Excel이 설치되어 있지 않습니다." in CP949 (same bytes as legacy Base01.pas snippet)
        raw = (
            b"MessageDlg('Excel\xc0\xcc \xbc\xb3\xc4\xa1\xb5\xc7\xbe\xee "
            b"\xc0\xd6\xc1\xf6 \xbe\xca\xbd\xc0\xb4\xcf\xb4\xd9.',0);\r\n"
        )
        with tempfile.NamedTemporaryFile(suffix=".pas", delete=False) as f:
            f.write(raw)
            path = f.name
        try:
            text = read_delphi_source(path)
            self.assertIn("Excel이 설치되어 있지 않습니다.", text)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_utf8_with_bom(self):
        raw = b"\xef\xbb\xbfunit Foo;\n"
        with tempfile.NamedTemporaryFile(suffix=".pas", delete=False) as f:
            f.write(raw)
            path = f.name
        try:
            text = read_delphi_source(path)
            self.assertTrue(text.startswith("unit Foo"))
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
