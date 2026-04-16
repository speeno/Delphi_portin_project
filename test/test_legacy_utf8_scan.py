"""legacy_source_utf8_scan / delphi_source_encoding UTF-8 분류."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


class TestClassifyDelphiBytes(unittest.TestCase):
    def test_utf8_no_bom_skip(self):
        sys.path.insert(0, str(_REPO / "tools" / "parsers"))
        from delphi_source_encoding import classify_delphi_source_bytes  # noqa: E402

        raw = "unit U;\nend.\n".encode("utf-8")
        c = classify_delphi_source_bytes(raw)
        self.assertEqual(c["action"], "skip")

    def test_cp949_korean_convert(self):
        sys.path.insert(0, str(_REPO / "tools" / "parsers"))
        from delphi_source_encoding import classify_delphi_source_bytes  # noqa: E402

        text = "unit U;\n// 한글\nend.\n"
        raw = text.encode("cp949")
        c = classify_delphi_source_bytes(raw)
        self.assertEqual(c["action"], "convert")
        self.assertIn(c["inferred_encoding"], ("cp949", "euc-kr"))


class TestLegacyUtf8ScanCli(unittest.TestCase):
    def test_scan_writes_manifest(self):
        script = _REPO / "tools" / "legacy_source_utf8_scan.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "src"
            root.mkdir()
            (root / "U.pas").write_bytes("unit U;\nend.\n".encode("utf-8"))
            (root / "Data").mkdir()
            (root / "Data" / "K.pas").write_bytes("// 한글\n".encode("cp949"))
            out = Path(tmp) / "manifest.json"
            r = subprocess.run(
                [sys.executable, str(script), "--root", str(root), "--out", str(out)],
                cwd=str(_REPO),
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(r.returncode, 0, msg=r.stderr + r.stdout)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["skip"], 1)
            self.assertEqual(data["summary"]["convert"], 1)
            paths = {f["path"]: f for f in data["files"]}
            self.assertEqual(paths["U.pas"]["tier"], 2)
            self.assertEqual(paths["Data/K.pas"]["tier"], 1)
            self.assertEqual(paths["Data/K.pas"]["action"], "convert")

    def test_apply_dest_mirror(self):
        script = _REPO / "tools" / "legacy_source_utf8_scan.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "src"
            root.mkdir()
            (root / "a.pas").write_bytes("// 한글\n".encode("cp949"))
            out = Path(tmp) / "m.json"
            dest = Path(tmp) / "mirror"
            subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--root",
                    str(root),
                    "--out",
                    str(out),
                    "--apply",
                    "--dest-root",
                    str(dest),
                ],
                cwd=str(_REPO),
                check=True,
                timeout=30,
            )
            self.assertTrue((dest / "a.pas").is_file())
            self.assertEqual((dest / "a.pas").read_bytes(), "// 한글\n".encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
