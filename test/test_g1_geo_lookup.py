"""g1_geo_lookup — LIST 와 상세 간 stmt_gcode 일치 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class StmtGcodeFromLinesTests(TestCase):
    def test_empty_rows(self) -> None:
        from app.services.g1_geo_lookup import stmt_gcode_from_s1_lines

        self.assertEqual(stmt_gcode_from_s1_lines([]), "")
        self.assertEqual(stmt_gcode_from_s1_lines([{"Bcode": "x"}]), "")

    def test_matches_sql_max_gcode_string_order(self) -> None:
        from app.services.g1_geo_lookup import stmt_gcode_from_s1_lines

        rows = [
            {"Gcode": "1001", "Bcode": "A"},
            {"Gcode": "9999", "Bcode": "B"},
            {"Gcode": "2000", "Bcode": "C"},
        ]
        self.assertEqual(stmt_gcode_from_s1_lines(rows), "9999")


if __name__ == "__main__":
    main()
