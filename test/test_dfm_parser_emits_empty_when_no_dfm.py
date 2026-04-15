"""dfm_parser: .dfm 이 없을 때도 #1/#2 산출 파일을 남기는지 검증."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "tools" / "parsers"))
import dfm_parser  # noqa: E402


class TestDfmParserEmptyTree(unittest.TestCase):
    def test_writes_empty_json_when_no_dfm(self):
        repo_root = Path(__file__).resolve().parents[1]
        script = repo_root / "tools" / "parsers" / "dfm_parser.py"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "analysis"
            out.mkdir()
            r = subprocess.run(
                [sys.executable, str(script), tmp, str(out)],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(r.returncode, 0, msg=r.stderr + r.stdout)
            inv = out / "form_inventory.json"
            flow = out / "event_flow.json"
            summ = out / "dfm_summary.json"
            self.assertTrue(inv.is_file(), msg="form_inventory.json missing")
            self.assertTrue(flow.is_file(), msg="event_flow.json missing")
            self.assertTrue(summ.is_file(), msg="dfm_summary.json missing")
            self.assertEqual(json.loads(inv.read_text(encoding="utf-8")), [])
            self.assertEqual(json.loads(flow.read_text(encoding="utf-8")), [])
            data = json.loads(summ.read_text(encoding="utf-8"))
            self.assertEqual(data.get("total_forms"), 0)


class TestParseDfmFileUnknownRoot(unittest.TestCase):
    """루트 object 라인이 없을 때도 form_inventory 빌드에 필요한 키가 있다."""

    def test_non_object_dfm_has_component_counts(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".dfm", delete=False, encoding="utf-8"
        ) as f:
            f.write("not a delphi form header\n")
            path = f.name
        try:
            d = dfm_parser.parse_dfm_file(path)
            self.assertEqual(d["component_count"], 0)
            self.assertEqual(d["event_count"], 0)
            self.assertEqual(d["form_class"], "unknown")
            self.assertIn("component_summary", d)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
