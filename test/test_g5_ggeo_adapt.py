from __future__ import annotations

from unittest import TestCase

from app.services.g5_ggeo_adapt import (
    etc_customer_detail_select_sql,
    etc_customer_list_select_sql,
    etc_customer_patch_targets,
    g5_gbun_code_column,
    g5_gbun_name_column,
)


class G5GgeoAdaptUnit(TestCase):
    def test_detail_select_sql_fallback_for_missing_columns(self) -> None:
        # 텍스트 일부 + 숫자 일부만 존재, 나머지는 fallback.
        cols = {"gcode", "gname", "hcode", "gtel1", "gpper", "grat1"}
        exact = {
            "gcode": "Gcode",
            "gname": "Gname",
            "hcode": "Hcode",
            "gtel1": "Gtel1",
            "gpper": "Gpper",
            "grat1": "Grat1",
        }
        sql = etc_customer_detail_select_sql(cols, exact, alias="g")
        # 존재 텍스트 → COALESCE … '' / 존재 숫자 → COALESCE … 0.
        self.assertIn("COALESCE(g.Gname,'') AS gname", sql)
        self.assertIn("COALESCE(g.Gtel1,'') AS gtel1", sql)
        self.assertIn("COALESCE(g.Gpper,0) AS gpper", sql)
        self.assertIn("COALESCE(g.Grat1,0) AS grat1", sql)
        # 누락 텍스트 → '' fallback / 누락 숫자 → 0 fallback.
        self.assertIn("'' AS gposa", sql)
        self.assertIn("'' AS name2", sql)
        self.assertIn("0 AS grat6", sql)
        self.assertIn("0 AS gqut1", sql)
        # gbun_name 기본 표현식.
        self.assertIn("'' AS gbun_name", sql)

    def test_detail_select_sql_custom_gbun_name_expr(self) -> None:
        cols = {"gcode", "gname"}
        exact = {"gcode": "Gcode", "gname": "Gname"}
        sql = etc_customer_detail_select_sql(
            cols, exact, alias="g", gbun_name_expr="COALESCE(b.Gname,'') AS gbun_name"
        )
        self.assertIn("COALESCE(b.Gname,'') AS gbun_name", sql)

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
        sql = etc_customer_list_select_sql(
            cols, exact, alias="g", gbun_name_expr="COALESCE(b.Gname,'') AS gbun_name"
        )
        self.assertIn("COALESCE(b.Gname,'') AS gbun_name", sql)
        self.assertIn("AS gjuso", sql)
        self.assertIn("AS jubun", sql)

    def test_patch_targets_excludes_gcode_and_missing(self) -> None:
        cols = {"gcode", "gname", "hcode", "gtel1", "gpper", "grat1"}
        exact = {
            "gcode": "Gcode",
            "gname": "Gname",
            "hcode": "Hcode",
            "gtel1": "Gtel1",
            "gpper": "Gpper",
            "grat1": "Grat1",
        }
        targets = etc_customer_patch_targets(cols, exact)
        # gcode 는 WHERE 전용 → patch 대상 제외.
        self.assertNotIn("gcode", targets)
        self.assertEqual(targets["gname"], "Gname")
        self.assertEqual(targets["gtel1"], "Gtel1")
        self.assertEqual(targets["gpper"], "Gpper")
        self.assertEqual(targets["grat1"], "Grat1")
        # 미존재 컬럼 제외.
        self.assertNotIn("gposa", targets)
        self.assertNotIn("gqut1", targets)

    def test_gbun_column_helpers(self) -> None:
        exact = {"gcode": "Gcode", "gname": "Gname"}
        self.assertEqual(g5_gbun_name_column(exact), "Gname")
        self.assertEqual(g5_gbun_code_column(exact), "Gcode")
