"""g1_geo_lookup — LIST 와 상세 간 stmt_gcode 일치 회귀."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class G1ProfileRowSqlTests(TestCase):
    def test_fetch_profile_row_uses_table_alias(self) -> None:
        """_text_expr 기본 alias=g — FROM 절에 ``g`` 별칭 필수 (1054 회귀)."""
        import asyncio
        from unittest.mock import AsyncMock, patch

        from app.services.g1_geo_lookup import _fetch_g1_profile_row

        captured: list[str] = []

        async def fake_meta(_server_id: str):
            return (
                {"gname", "gadd1", "gadd2", "gtel1", "gtel2", "gposa", "gfax1", "gfax2", "gpost"},
                {
                    "gname": "Gname",
                    "gadd1": "Gadd1",
                    "gadd2": "Gadd2",
                    "gtel1": "Gtel1",
                    "gtel2": "Gtel2",
                    "gposa": "Gposa",
                    "gfax1": "Gfax1",
                    "gfax2": "Gfax2",
                    "gpost": "Gpost",
                },
            )

        async def fake_query(_server_id, sql, _params=None):
            captured.append(sql)
            return [{"gname": "교보문고", "gadd1": "", "gadd2": "", "gtel1": "", "gtel2": "", "gposa": "", "gfax1": "", "gfax2": "", "gpost": ""}]

        with patch(
            "app.services.g1_geo_lookup.g1_geo_column_meta",
            new=AsyncMock(side_effect=fake_meta),
        ), patch(
            "app.services.g1_geo_lookup.execute_query",
            new=AsyncMock(side_effect=fake_query),
        ):
            row = asyncio.run(_fetch_g1_profile_row("remote_138", "", "00001"))

        self.assertIsNotNone(row)
        self.assertEqual(len(captured), 1)
        self.assertIn("FROM G1_Ggeo g WHERE", captured[0])
        self.assertIn("g.Gname", captured[0])


class G1ProfileMappingTests(TestCase):
    def test_profile_from_row_remark_fields(self) -> None:
        from app.services.g1_geo_lookup import _profile_from_row

        row = {
            "gname": "(주)영풍문고",
            "gadd1": "서울특별시 강남구 강남대로 542",
            "gadd2": "보조",
            "gtel1": "02",
            "gtel2": "399-6423",
            "gfax1": "02",
            "gfax2": "399-6415",
            "gbigo": "ypacct@ypbooks.co.kr",
            "name1": "이전사업자102-81-30788",
            "memos": "",
        }
        p = _profile_from_row(row)
        self.assertEqual(p["address"], "서울특별시 강남구 강남대로 542")
        self.assertEqual(p["remark1"], "ypacct@ypbooks.co.kr")
        self.assertEqual(p["remark2"], "이전사업자102-81-30788")
        self.assertEqual(p["phone"], "02-399-6423")
        self.assertEqual(p["fax"], "02-399-6415")
        self.assertEqual(p["customer_memo_format"], "plain")

    def test_profile_rtf_memos_html(self) -> None:
        from app.services.g1_geo_lookup import _profile_from_row

        row = {
            "gname": "T",
            "gadd1": "",
            "gadd2": "",
            "gtel1": "",
            "gtel2": "",
            "gbigo": "",
            "name1": "",
            "memos": "{\\rtf1\\ansi\\pard \\'b0\\'a1\\par}",
        }
        p = _profile_from_row(row)
        self.assertEqual(p["customer_memo_format"], "rtf")
        self.assertIn("가", p["customer_memo"])
        self.assertIn("가", p["customer_memo_html"])


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
