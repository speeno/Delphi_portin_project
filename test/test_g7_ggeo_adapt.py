"""G7_Ggeo DDL 어댑터 단위 테스트 (SHOW COLUMNS 없이 순수 표현식만)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.g7_ggeo_adapt import (  # noqa: E402
    select_chek3_yesno_sql,
    update_targets,
)


class G7GgeoAdaptExprTests(TestCase):
    def test_select_uses_scode_when_present(self) -> None:
        cols = {"gcode", "gname", "chek3", "scode"}
        exact = {"gcode": "Gcode", "gname": "Gname", "chek3": "Chek3", "scode": "Scode"}
        sql = select_chek3_yesno_sql(cols, exact)
        self.assertIn("Chek3", sql)
        self.assertIn("Scode", sql)
        self.assertIn("yesno", sql)

    def test_select_fallback_yesno_when_no_scode(self) -> None:
        cols = {"gcode", "gname", "chek3", "yesno"}
        exact = {"gcode": "Gcode", "gname": "Gname", "chek3": "Chek3", "yesno": "Yesno"}
        sql = select_chek3_yesno_sql(cols, exact)
        self.assertIn("Yesno", sql)

    def test_select_literal_when_optional_missing(self) -> None:
        cols = {"gcode", "gname", "scode"}
        exact = {"gcode": "Gcode", "gname": "Gname", "scode": "Scode"}
        sql = select_chek3_yesno_sql(cols, exact)
        self.assertIn("'' AS chek3", sql)

    def test_update_targets(self) -> None:
        cols = {"chek3", "scode"}
        exact = {"chek3": "Chek3", "scode": "Scode"}
        t = update_targets(cols, exact)
        self.assertEqual(t["chek3"], "Chek3")
        self.assertEqual(t["yesno"], "Scode")


if __name__ == "__main__":
    main(verbosity=2)
