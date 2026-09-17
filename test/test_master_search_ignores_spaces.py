"""
마스터 검색어 공백 무시 매칭 — 사용자 요청(2026-09-17).

대상
----
- 거래처(Sobo11) 대표자 ``G1_Ggeo.Gposa``
- 도서(Sobo14) / 도서코드(Sobo38) 제목 ``G4_Book.Gname``
- 도서 인라인 자동완성 ``search_products``

규칙
----
검색어와 컬럼 양쪽의 공백을 제거하고 LIKE 비교한다("김 길 동" ↔ "김길동").
컬럼 쪽은 MySQL 3.22+ 내장 ``REPLACE(col,' ','')`` 만 사용(4서버 공통 · DEC-033),
검색어 쪽은 ``_strip_all_spaces`` (전각 공백 U+3000 포함).
공백 제거 매칭은 원문 매칭의 상위집합이라 기존 결과가 줄지 않는다.
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


async def _fake_geo_meta(server_id: str):  # noqa: ARG001
    cols = {"gubun", "jubun", "gposa"}
    return cols, {c: c.capitalize() for c in cols}


async def _fake_gbun_map(server_id: str, *, scope_hcode=None):  # noqa: ARG001
    return {}


def _capture(coro_factory) -> _Capture:
    cap = _Capture()
    with patch.object(masters_service, "execute_query", new=cap), \
            patch.object(masters_service, "g1_geo_column_meta", new=_fake_geo_meta), \
            patch.object(masters_service, "_gbun_code_name_map", new=_fake_gbun_map):
        asyncio.run(coro_factory())
    return cap


class StripHelperTests(TestCase):
    def test_strips_all_whitespace_kinds(self) -> None:
        self.assertEqual(masters_service._strip_all_spaces("김 길 동"), "김길동")
        self.assertEqual(masters_service._strip_all_spaces("김　길동"), "김길동")
        self.assertEqual(masters_service._strip_all_spaces("  해리 \t포터 "), "해리포터")
        self.assertEqual(masters_service._strip_all_spaces(None), "")

    def test_spaceless_search_pair(self) -> None:
        expr, pat = masters_service._spaceless_search("Gname", "해리 포터")
        self.assertEqual(expr, "REPLACE(Gname,' ','')")
        self.assertEqual(pat, "%해리포터%")

    def test_spaceless_search_blank_falls_back_to_plain_expr(self) -> None:
        # 빈/공백 검색어는 애초에 검색 절이 생기지 않으므로 표현식 그대로 반환.
        self.assertEqual(masters_service._spaceless_search("Gname", "   "), "Gname")


class CustomerRepNameTests(TestCase):
    def test_customer_gposa_spaceless(self) -> None:
        cap = _capture(
            lambda: masters_service.list_customer_master(
                server_id="remote_1", q="김 길 동", limit=10, offset=0
            )
        )
        sql, params = cap.select
        self.assertIn("REPLACE(Gposa,' ','') LIKE %s", sql)
        self.assertIn("%김길동%", params)
        # 코드/거래처명은 원문 패턴 유지
        self.assertIn("%김 길 동%", params)


class BookTitleTests(TestCase):
    def test_book_list_title_spaceless(self) -> None:
        cap = _capture(
            lambda: masters_service.list_books(
                server_id="remote_1", q="해리 포터", limit=10, offset=0
            )
        )
        sql, params = cap.select
        self.assertIn("REPLACE(Gname,' ','') LIKE %s", sql)
        self.assertIn("%해리포터%", params)
        # 코드/ISBN 은 원문 패턴
        self.assertIn("Gcode LIKE %s", sql)
        self.assertIn("COALESCE(Gisbn,'') LIKE %s", sql)

    def test_book_code_list_title_spaceless(self) -> None:
        cap = _capture(
            lambda: masters_service.list_book_codes(
                server_id="remote_1", q="해리 포터", limit=10, offset=0
            )
        )
        sql, params = cap.select
        self.assertIn("REPLACE(Gname,' ','') LIKE %s", sql)
        self.assertIn("%해리포터%", params)

    def test_book_inline_autocomplete_spaceless(self) -> None:
        cap = _capture(
            lambda: masters_service.search_products(server_id="remote_1", q="해리 포터", limit=10)
        )
        sql, params = cap.select
        self.assertIn("REPLACE(Gname,' ','') LIKE %s", sql)
        self.assertIn("%해리포터%", params)

    def test_count_and_select_share_where(self) -> None:
        """페이지 total 정합 — SELECT/COUNT WHERE params 동일."""
        cap = _capture(
            lambda: masters_service.list_books(
                server_id="remote_1", q="해리 포터", limit=10, offset=0
            )
        )
        select_params = list(cap.calls[0][1])[:-2]
        count_params = list(cap.calls[1][1])
        self.assertEqual(select_params, count_params)


if __name__ == "__main__":
    main()
