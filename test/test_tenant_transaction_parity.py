"""tenant transaction parity probe/manifest 회귀."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase, main

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migration" / "contracts" / "tenant_transaction_parity_manifest.yaml"
PROBE = ROOT / "debug" / "probe_tenant_transaction_parity.py"


class TenantTransactionParityTest(TestCase):
    def test_manifest_has_b4_windows(self) -> None:
        doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cases = doc.get("cases") or []
        b4 = next((c for c in cases if c.get("case") == "B4"), None)
        self.assertIsNotNone(b4)
        self.assertEqual(b4.get("date_windows_days"), [30, 90, 365])
        self.assertIn("stats_customer_analysis", (b4.get("endpoints") or {}))

    def test_probe_writes_report_without_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "tx-parity.json"
            proc = subprocess.run(
                [
                    "python3",
                    str(PROBE),
                    "--manifest",
                    str(MANIFEST),
                    "--case",
                    "B4",
                    "--api-base",
                    "http://localhost:8000",
                    "--out",
                    str(out),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out.exists(), "probe output file missing")
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("summary", report)
            self.assertIn("result", report)
            self.assertTrue(report["summary"].get("skipped"))


if __name__ == "__main__":
    main(verbosity=2)

