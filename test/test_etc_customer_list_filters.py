"""
Sobo15 기타거래처 목록 — 검색 필터 확장 회귀 가드.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

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

    @property
    def count(self) -> tuple[str, tuple[Any, ...]]:
        return self.calls[1]


def _meta() -> tuple[AsyncMock, AsyncMock]:
    ggeo_cols = {
        "gcode",
        "gname",
        "hcode",
        "gubun",
        "jubun",
        "guper",
        "gtel1",
        "gtel2",
        "gpost",
        "gadd1",
        "gadd2",
    }
    ggeo_exact = {
        "gcode": "Gcode",
        "gname": "Gname",
        "hcode": "Hcode",
        "gubun": "Gubun",
        "jubun": "Jubun",
        "guper": "Guper",
        "gtel1": "Gtel1",
        "gtel2": "Gtel2",
        "gpost": "Gpost",
        "gadd1": "Gadd1",
        "gadd2": "Gadd2",
    }
    gbun_cols = {"gcode", "gname"}
    gbun_exact = {"gcode": "Gcode", "gname": "Gname"}
    return (
        AsyncMock(return_value=(ggeo_cols, ggeo_exact)),
        AsyncMock(return_value=(gbun_cols, gbun_exact)),
    )


def _run(**kwargs) -> _Capture:
    cap = _Capture()
    ggeo_mock, gbun_mock = _meta()
    with (
        patch.object(masters_service, "execute_query", new=cap),
        patch.object(masters_service, "g5_ggeo_column_meta", ggeo_mock),
        patch.object(masters_service, "g5_gbun_column_meta", gbun_mock),
    ):
        asyncio.run(
            masters_service.list_etc_customers(
                server_id="remote_1", limit=50, offset=0, **kwargs
            )
        )
    return cap


class EtcCustomerListFilterTests(TestCase):
    def test_gubun_exact_match(self) -> None:
        cap = _run(gubun="E01")
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("g.Gubun=%s", select_sql)
        self.assertIn("g.Gubun=%s", count_sql)
        self.assertIn("E01", select_params)
        self.assertIn("E01", count_params)

    def test_jubun_like_filter(self) -> None:
        cap = _run(jubun="부산")
        select_sql, select_params = cap.select
        self.assertIn("g.Jubun LIKE %s", select_sql)
        self.assertTrue(any("%부산%" in str(p) for p in select_params))

    def test_q_search_includes_phone_columns(self) -> None:
        cap = _run(q="02")
        select_sql, _ = cap.select
        self.assertIn("g.Gtel1 LIKE", select_sql)
        self.assertIn("g.Guper LIKE", select_sql)

    def test_list_select_includes_gbun_join(self) -> None:
        cap = _run()
        select_sql, _ = cap.select
        self.assertIn("LEFT JOIN G5_Gbun", select_sql)
        self.assertIn("gbun_name", select_sql)
        self.assertIn("gjuso", select_sql)


if __name__ == "__main__":
    main(verbosity=2)
