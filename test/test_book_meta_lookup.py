"""DEC-169 — 도서 메타(정가·ISBN) 공통 lookup 헬퍼 회귀 가드."""
import unittest
from unittest.mock import patch

from app.services import book_meta_lookup as m


class TestBookMetaLookup(unittest.IsolatedAsyncioTestCase):
    async def _fake_meta(self, server_id):
        return ({"gcode", "gname", "gdang", "gisbn"}, {"gdang": "Gdang", "gisbn": "Gisbn"})

    async def test_fetch_prefers_hcode_then_shared_fallback(self):
        calls = []

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            calls.append((tuple(prefix_params), tuple(keys)))
            if prefix_params == ("5019",):
                return [{"bcode": "A", "gname": "책A", "gdang": 10000, "gisbn": "978A"}]
            return [{"bcode": "B", "gname": "책B", "gdang": 20000, "gisbn": "978B"}]

        with patch.object(m, "in_clause_lookup", fake_lookup), \
             patch.object(m, "g4_book_column_meta", self._fake_meta):
            out = await m.fetch_book_meta("remote_153", "5019", ["A", "B", "B", " ", None])
        self.assertEqual(out["A"]["gisbn"], "978A")
        self.assertEqual(out["B"]["gdang"], 20000)
        self.assertEqual(calls[0][0], ("5019",))
        self.assertEqual(calls[1], (("",), ("B",)))  # 못 찾은 코드만 공용 폴백

    async def test_attach_keeps_slip_price_and_fills_isbn(self):
        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            return [{"bcode": "A", "gname": "책A", "gdang": 10000, "gisbn": "978A"}]

        rows = [{"bcode": "A", "gdang": 8000}, {"bcode": "A", "gdang": 0}, {"bcode": "Z"}]
        with patch.object(m, "in_clause_lookup", fake_lookup), \
             patch.object(m, "g4_book_column_meta", self._fake_meta):
            await m.attach_book_meta("remote_153", "5019", rows)
        self.assertEqual(rows[0]["gdang"], 8000)      # 전표 단가 보존
        self.assertEqual(rows[0]["gisbn"], "978A")
        self.assertEqual(rows[1]["gdang"], 10000)     # 0 이면 마스터 정가로 보충
        self.assertEqual(rows[2]["gisbn"], "")        # 미존재 코드 → 빈값, gdang 0
        self.assertEqual(rows[2]["gdang"], 0)

    async def test_missing_columns_use_literal_defaults(self):
        async def meta(server_id):
            return ({"gcode", "gname"}, {})
        seen = {}

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            seen["sql"] = sql_template
            return []

        with patch.object(m, "in_clause_lookup", fake_lookup), patch.object(m, "g4_book_column_meta", meta):
            await m.fetch_book_meta("remote_155", "1", ["A"])
        self.assertIn("0 AS gdang", seen["sql"])
        self.assertIn("'' AS gisbn", seen["sql"])
        self.assertNotIn("COALESCE", seen["sql"])


if __name__ == "__main__":
    unittest.main()
