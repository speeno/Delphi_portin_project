"""debug/generate_incomplete_features_inventory.py 산출물 구조 회귀 가드."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "debug" / "generate_incomplete_features_inventory.py"
JSON_PATH = ROOT / "analysis" / "audit" / "incomplete-features-inventory.json"


class IncompleteFeaturesInventoryTests(TestCase):
    def test_generator_script_exists(self) -> None:
        self.assertTrue(SCRIPT.is_file(), msg=str(SCRIPT))

    def test_generator_produces_valid_json(self) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=str(ROOT))
        raw = JSON_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
        self.assertIn("criteria", data)
        self.assertIn("sources", data)
        src = data["sources"]
        self.assertIn("ui_placeholder_pages", src)
        self.assertIn("phase2_screen_cards_tasks", src)
        self.assertIn("form_registry_preview_or_stub", src)
        self.assertIn("backend_generic_stub", src)
        self.assertIn("crud_backlog_section_2_6", src)
        # 계획서 스냅샷: ScreenPlaceholder 페이지 ≥ 4
        self.assertGreaterEqual(len(src["ui_placeholder_pages"]), 4)
        # form-registry placeholder 는 매트릭스 3건
        ids = [x.get("id") for x in src["form_registry_preview_or_stub"]]
        self.assertEqual(
            sorted(ids),
            ["MenuBillingStatements", "MenuShippingReturnsInventory", "MenuYearMonthStats"],
        )


if __name__ == "__main__":
    main()
