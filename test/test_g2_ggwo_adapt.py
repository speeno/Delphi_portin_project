from __future__ import annotations

from unittest import TestCase

from app.services.g2_ggwo_adapt import (
    inbound_vendor_detail_select_sql,
    inbound_vendor_list_select_sql,
    inbound_vendor_patch_targets,
)


class G2GgwoAdaptUnit(TestCase):
    def test_detail_select_sql_fallback_for_missing_columns(self) -> None:
        cols = {"gcode", "gname", "hcode", "grat1"}
        exact = {"gcode": "Gcode", "gname": "Gname", "hcode": "Hcode", "grat1": "Grat1"}
        sql = inbound_vendor_detail_select_sql(cols, exact, alias="g")
        self.assertIn("COALESCE(g.Gcode,'') AS gcode", sql)
        self.assertIn("COALESCE(g.Grat1,0) AS grat1", sql)
        self.assertIn("'' AS gubun", sql)
        self.assertIn("0 AS grat2", sql)

    def test_list_select_sql_includes_extended_columns(self) -> None:
        cols = {"gcode", "gname", "hcode", "gubun", "jubun", "gtel1", "gadd1", "gadd2"}
        exact = {
            "gcode": "Gcode",
            "gname": "Gname",
            "hcode": "Hcode",
            "gubun": "Gubun",
            "jubun": "Jubun",
            "gtel1": "Gtel1",
            "gadd1": "Gadd1",
            "gadd2": "Gadd2",
        }
        sql = inbound_vendor_list_select_sql(
            cols, exact, alias="g", gbun_name_expr="COALESCE(b.Gname,'') AS gbun_name"
        )
        self.assertIn("COALESCE(b.Gname,'') AS gbun_name", sql)
        self.assertIn("AS gjuso", sql)
        self.assertIn("AS jubun", sql)

    def test_patch_targets_includes_only_existing_columns(self) -> None:
        cols = {"gname", "hcode", "grat1", "gadd1"}
        exact = {"gname": "Gname", "hcode": "Hcode", "grat1": "Grat1", "gadd1": "Gadd1"}
        targets = inbound_vendor_patch_targets(cols, exact)
        self.assertEqual(targets["gname"], "Gname")
        self.assertEqual(targets["hcode"], "Hcode")
        self.assertEqual(targets["grat1"], "Grat1")
        self.assertEqual(targets["gadd1"], "Gadd1")
        self.assertNotIn("gadd2", targets)
