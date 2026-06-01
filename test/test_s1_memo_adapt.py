from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.s1_memo_adapt import (
    append_memo_button301_filters,
    memo_preview_select_sql,
)


class S1MemoAdaptTests(TestCase):
    def test_preview_select_omits_missing_gpost(self) -> None:
        cols = {"gbigo", "sbigo", "gtel1", "gtel2", "gname"}
        exact = {k: k for k in cols}
        sql = memo_preview_select_sql(cols, exact)
        self.assertIn("'' AS gpost", sql)
        self.assertNotIn("gpost,", sql.replace("'' AS gpost", ""))

    def test_button301_where_skips_missing_ocode(self) -> None:
        cols = {
            "gdate",
            "gubun",
            "jubun",
            "gcode",
            "hcode",
            "scode",
            "gjisa",
        }
        exact = {k: k for k in cols}
        where: list[str] = []
        params: list[str] = []
        append_memo_button301_filters(
            where,
            params,
            cols,
            exact,
            gdate="2026.05.14",
            gcode="00001",
            hcode="",
            gubun="출고",
            jubun="00001",
            gjisa="광화문점",
        )
        joined = " AND ".join(where)
        self.assertNotIn("ocode", joined)
        self.assertIn("scode=%s", joined)
        self.assertIn("gdate=%s", joined)


if __name__ == "__main__":
    import unittest

    unittest.main()
