"""
Sobo13 저자 목록 — 검색 필터 확장 회귀 가드 (minimal 세트).

``masters_service.list_authors`` 의 ``gubun`` / ``workplace`` / ``q`` 확장이
SELECT·COUNT 에 동일 WHERE 로 합성되는지 service 레벨에서 검증한다.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import masters_service  # noqa: E402

_GJEO_COLS = frozenset(
    {"gcode", "gposa", "gname", "hcode", "gubun", "gtel1", "gtel2", "date1", "gjice"}
)
_GJEO_EXACT = {
    "gcode": "Gcode",
    "gposa": "Gposa",
    "gname": "Gname",
    "hcode": "Hcode",
    "gubun": "Gubun",
    "gtel1": "Gtel1",
    "gtel2": "Gtel2",
    "date1": "Date1",
    "gjice": "Gjice",
}
_GBUN_COLS = frozenset({"gcode", "gname"})
_GBUN_EXACT = {"gcode": "Gcode", "gname": "Gname"}


async def _mock_gjeo_meta(server_id: str):  # noqa: ARG001
    return set(_GJEO_COLS), dict(_GJEO_EXACT)


async def _mock_gbun_meta(server_id: str):  # noqa: ARG001
    return set(_GBUN_COLS), dict(_GBUN_EXACT)


class _Capture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        if "COUNT(*)" in sql.upper():
            return [{"row_count": 0}]
        return []

    @property
    def select(self) -> tuple[str, tuple[Any, ...]]:
        return self.calls[0]

    @property
    def count(self) -> tuple[str, tuple[Any, ...]]:
        return self.calls[1]


def _run(**kwargs) -> _Capture:
    cap = _Capture()
    with (
        patch.object(masters_service, "execute_query", new=cap),
        patch.object(masters_service, "g3_gjeo_column_meta", new=_mock_gjeo_meta),
        patch.object(masters_service, "g3_gbun_column_meta", new=_mock_gbun_meta),
    ):
        asyncio.run(
            masters_service.list_authors(
                server_id="remote_1", limit=50, offset=0, **kwargs
            )
        )
    return cap


class AuthorListFilterTests(TestCase):
    def test_no_filters_baseline(self) -> None:
        cap = _run()
        self.assertEqual(len(cap.calls), 2)
        select_sql, select_params = cap.select
        self.assertIn("G3_Gjeo g", select_sql)
        self.assertIn("G3_Gbun", select_sql)
        self.assertIn("gbun_name", select_sql)
        self.assertNotIn("g.Gubun=%s", select_sql)
        self.assertNotIn("g.Gname LIKE", select_sql)
        self.assertEqual(select_params[-2:], (50, 0))

    def test_gubun_exact_match(self) -> None:
        cap = _run(gubun="5019")
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("g.Gubun=%s", select_sql)
        self.assertIn("g.Gubun=%s", count_sql)
        self.assertIn("5019", select_params)
        self.assertIn("5019", count_params)

    def test_gubun_blank_ignored(self) -> None:
        cap = _run(gubun="   ")
        self.assertNotIn("g.Gubun=%s", cap.select[0])

    def test_workplace_like(self) -> None:
        cap = _run(workplace="대학")
        select_sql, select_params = cap.select
        self.assertIn("g.Gname LIKE %s", select_sql)
        self.assertIn("%대학%", select_params)
        self.assertIn("g.Gname LIKE %s", cap.count[0])

    def test_q_search_includes_gposa_and_gname(self) -> None:
        cap = _run(q="김")
        select_sql, select_params = cap.select
        self.assertIn("g.Gposa LIKE %s", select_sql)
        self.assertIn("g.Gname LIKE %s", select_sql)
        self.assertIn("%김%", select_params)

    def test_combined_filters(self) -> None:
        cap = _run(q="김", gubun="5019", workplace="출판")
        select_sql, select_params = cap.select
        self.assertIn("g.Gposa LIKE %s", select_sql)
        self.assertIn("g.Gubun=%s", select_sql)
        self.assertIn("g.Gname LIKE %s", select_sql)
        self.assertIn("5019", select_params)
        self.assertIn("%출판%", select_params)


if __name__ == "__main__":
    main()
