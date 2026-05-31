"""
Sobo14 도서 목록 — 검색 필터 확장 회귀 가드 (minimal 세트).

대상
----
``masters_service.list_books`` 에 추가된 필터 인자
(``gubun`` / ``jubun`` / ``exclude_shipping_stop``) 가 SELECT·COUNT 두 쿼리에
**동일하게** WHERE 절로 합성되고, params 순서/길이가 일관되는지 service
레벨에서 검증한다 (페이지네이션 total 정합 보장).
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


class _Capture:
    """execute_query 의 (sql, params) 호출을 순서대로 모아두는 stub."""

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
    with patch.object(masters_service, "execute_query", new=cap):
        asyncio.run(
            masters_service.list_books(
                server_id="remote_1", limit=50, offset=0, **kwargs
            )
        )
    return cap


class BookListFilterTests(TestCase):
    def test_no_filters_baseline(self) -> None:
        cap = _run()
        self.assertEqual(len(cap.calls), 2)
        select_sql, select_params = cap.select
        self.assertNotIn("Gubun=%s", select_sql)
        self.assertNotIn("Jubun LIKE", select_sql)
        self.assertNotIn("Grat9", select_sql)
        self.assertEqual(select_params, (50, 0))

    def test_gubun_exact_match(self) -> None:
        cap = _run(gubun="B01")
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("Gubun=%s", select_sql)
        self.assertIn("Gubun=%s", count_sql)
        self.assertIn("B01", select_params)
        self.assertIn("B01", count_params)
        self.assertEqual(select_params[-2:], (50, 0))

    def test_gubun_blank_ignored(self) -> None:
        cap = _run(gubun="   ")
        self.assertNotIn("Gubun=%s", cap.select[0])

    def test_jubun_like(self) -> None:
        cap = _run(jubun="입고")
        select_sql, select_params = cap.select
        self.assertIn("Jubun LIKE %s", select_sql)
        self.assertIn("%입고%", select_params)
        self.assertIn("Jubun LIKE %s", cap.count[0])

    def test_exclude_shipping_stop(self) -> None:
        cap = _run(exclude_shipping_stop=True)
        select_sql, _ = cap.select
        self.assertIn("IFNULL(Grat9,'') NOT IN ('1','True','true')", select_sql)
        self.assertIn("IFNULL(Grat9,'') NOT IN ('1','True','true')", cap.count[0])

    def test_exclude_shipping_stop_off_default(self) -> None:
        cap = _run(exclude_shipping_stop=False)
        self.assertNotIn("Grat9", cap.select[0])

    def test_all_filters_combined(self) -> None:
        cap = _run(
            q="도서",
            gubun="B01",
            jubun="입고",
            exclude_shipping_stop=True,
        )
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count

        for sql in (select_sql, count_sql):
            self.assertIn("Gisbn", sql)
            self.assertIn("Gubun=%s", sql)
            self.assertIn("Jubun LIKE %s", sql)
            self.assertIn("IFNULL(Grat9,'') NOT IN ('1','True','true')", sql)

        self.assertEqual(select_params[-2:], (50, 0))
        self.assertEqual(list(select_params[:-2]), list(count_params))
        self.assertEqual(len(count_params), 5)

    def test_where_consistency_select_vs_count(self) -> None:
        cap = _run(gubun="B01", jubun="출고", exclude_shipping_stop=True)
        _, select_params = cap.select
        _, count_params = cap.count
        self.assertEqual(list(select_params[:-2]), list(count_params))


if __name__ == "__main__":
    main()
