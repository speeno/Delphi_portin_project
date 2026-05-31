from __future__ import annotations

from unittest import TestCase

from app.services.g4_book_adapt import (
    book_detail_select_sql,
    book_patch_targets,
    g4_gbun_code_column,
    g4_gbun_name_column,
)


class G4BookAdaptUnit(TestCase):
    def test_detail_select_sql_fallback_for_missing_columns(self) -> None:
        cols = {"gcode", "gname", "gubun", "gisbn", "gdang", "price", "jego1"}
        exact = {
            "gcode": "Gcode",
            "gname": "Gname",
            "gubun": "Gubun",
            "gisbn": "Gisbn",
            "gdang": "Gdang",
            "price": "Price",
            "jego1": "Jego1",
        }
        sql = book_detail_select_sql(cols, exact, alias="g")
        # 존재 텍스트 → COALESCE … '' / 존재 숫자 → COALESCE … 0.
        self.assertIn("COALESCE(g.Gname,'') AS gname", sql)
        self.assertIn("COALESCE(g.Gisbn,'') AS gisbn", sql)
        self.assertIn("COALESCE(g.Gdang,0) AS gdang", sql)
        self.assertIn("COALESCE(g.Price,0) AS price", sql)
        self.assertIn("COALESCE(g.Jego1,0) AS jego1", sql)
        # 누락 텍스트 → '' fallback / 누락 숫자 → 0 fallback.
        self.assertIn("'' AS name2", sql)
        self.assertIn("'' AS gbjil", sql)
        self.assertIn("0 AS grat7", sql)
        self.assertIn("0 AS gsqut", sql)
        # gbun_name 기본 표현식.
        self.assertIn("'' AS gbun_name", sql)

    def test_detail_select_sql_custom_gbun_name_expr(self) -> None:
        cols = {"gcode", "gname"}
        exact = {"gcode": "Gcode", "gname": "Gname"}
        sql = book_detail_select_sql(
            cols, exact, alias="g", gbun_name_expr="COALESCE(b.Gname,'') AS gbun_name"
        )
        self.assertIn("COALESCE(b.Gname,'') AS gbun_name", sql)

    def test_patch_targets_excludes_pk_and_readonly_stock(self) -> None:
        # gcode(PK), 재고 계열(gsqut/jego1~4)은 PATCH 대상에서 제외.
        cols = {
            "gcode",
            "gname",
            "gisbn",
            "gdang",
            "price",
            "gsqut",
            "jego1",
            "jego2",
            "jego3",
            "jego4",
            "grat7",
        }
        exact = {c: c.capitalize() for c in cols}
        targets = book_patch_targets(cols, exact)
        self.assertNotIn("gcode", targets)
        self.assertNotIn("gsqut", targets)
        self.assertNotIn("jego1", targets)
        self.assertNotIn("jego4", targets)
        self.assertEqual(targets["gname"], "Gname")
        self.assertEqual(targets["gisbn"], "Gisbn")
        self.assertEqual(targets["price"], "Price")
        self.assertEqual(targets["grat7"], "Grat7")
        # 미존재 컬럼 제외.
        self.assertNotIn("odang", targets)

    def test_gbun_column_helpers(self) -> None:
        exact = {"gcode": "Gcode", "gname": "Gname"}
        self.assertEqual(g4_gbun_name_column(exact), "Gname")
        self.assertEqual(g4_gbun_code_column(exact), "Gcode")
