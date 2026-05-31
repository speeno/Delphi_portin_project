from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.g1_ggeo_adapt import customer_detail_select_sql, customer_patch_targets


class G1GeoAdaptTests(TestCase):
    def test_detail_select_fallback_when_columns_missing(self) -> None:
        sql = customer_detail_select_sql(set(), {}, alias="g", gbun_name_expr="'' AS gbun_name")
        self.assertIn("'' AS gname", sql)
        self.assertIn("0 AS grat1", sql)
        self.assertIn("'' AS gbun_name", sql)

    def test_patch_targets_only_exposes_existing_columns(self) -> None:
        cols = {"gname", "gadd1", "grat9", "yesno"}
        exact = {"gname": "Gname", "gadd1": "Gadd1", "grat9": "Grat9", "yesno": "Yesno"}
        out = customer_patch_targets(cols, exact)
        self.assertEqual(out["gname"], "Gname")
        self.assertEqual(out["gadd1"], "Gadd1")
        self.assertEqual(out["grat9"], "Grat9")
        self.assertEqual(out["yesno"], "Yesno")
        self.assertNotIn("gadd2", out)
