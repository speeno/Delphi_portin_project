from __future__ import annotations

from unittest import TestCase

from app.services.g3_gjeo_adapt import (
    author_detail_select_sql,
    author_patch_targets,
    g3_gbun_code_column,
    g3_gbun_name_column,
)


class G3GjeoAdaptUnit(TestCase):
    def test_detail_select_sql_fallback_for_missing_columns(self) -> None:
        # gposa(저자명)/gname(직장명) 존재, 나머지 상세 컬럼 일부 누락.
        cols = {"gcode", "gposa", "gname", "hcode", "gtel1"}
        exact = {
            "gcode": "Gcode",
            "gposa": "Gposa",
            "gname": "Gname",
            "hcode": "Hcode",
            "gtel1": "Gtel1",
        }
        sql = author_detail_select_sql(cols, exact, alias="g")
        # 존재 컬럼은 COALESCE, 누락 컬럼은 '' fallback (전부 텍스트).
        self.assertIn("COALESCE(g.Gposa,'') AS gposa", sql)
        self.assertIn("COALESCE(g.Gtel1,'') AS gtel1", sql)
        self.assertIn("'' AS gjice", sql)
        self.assertIn("'' AS oadd2", sql)
        # gbun_name 표현식 기본값.
        self.assertIn("'' AS gbun_name", sql)

    def test_detail_select_sql_custom_gbun_name_expr(self) -> None:
        cols = {"gcode", "gposa"}
        exact = {"gcode": "Gcode", "gposa": "Gposa"}
        sql = author_detail_select_sql(
            cols, exact, alias="g", gbun_name_expr="COALESCE(b.Gname,'') AS gbun_name"
        )
        self.assertIn("COALESCE(b.Gname,'') AS gbun_name", sql)

    def test_patch_targets_excludes_gcode_and_missing(self) -> None:
        cols = {"gcode", "gposa", "gname", "hcode", "gtel1", "gadd1"}
        exact = {
            "gcode": "Gcode",
            "gposa": "Gposa",
            "gname": "Gname",
            "hcode": "Hcode",
            "gtel1": "Gtel1",
            "gadd1": "Gadd1",
        }
        targets = author_patch_targets(cols, exact)
        # gcode 는 WHERE 전용 → patch 대상 제외.
        self.assertNotIn("gcode", targets)
        self.assertEqual(targets["gposa"], "Gposa")
        self.assertEqual(targets["gname"], "Gname")
        self.assertEqual(targets["gtel1"], "Gtel1")
        self.assertEqual(targets["gadd1"], "Gadd1")
        # 미존재 컬럼 제외.
        self.assertNotIn("oadd2", targets)
        self.assertNotIn("gbigo", targets)

    def test_gbun_column_helpers(self) -> None:
        exact = {"gcode": "Gcode", "gname": "Gname"}
        self.assertEqual(g3_gbun_name_column(exact), "Gname")
        self.assertEqual(g3_gbun_code_column(exact), "Gcode")
