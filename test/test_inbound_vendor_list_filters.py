"""
Sobo12 입고처 목록 — 검색 필터 확장 회귀 가드.

``masters_service.list_inbound_vendors`` 의 ``gubun`` / ``jubun`` / ``q`` 확장 검색이
SELECT·COUNT 에 동일 WHERE 로 합성되는지 service 레벨에서 검증(DB 미연결).
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
    ggwo_cols = {
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
    ggwo_exact = {
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
    gbun_cols = {"gcode", "gname", "hcode"}
    gbun_exact = {"gcode": "Gcode", "gname": "Gname", "hcode": "Hcode"}
    return (
        AsyncMock(return_value=(ggwo_cols, ggwo_exact)),
        AsyncMock(return_value=(gbun_cols, gbun_exact)),
    )


def _run(**kwargs) -> _Capture:
    cap = _Capture()
    ggwo_mock, gbun_mock = _meta()
    with (
        patch.object(masters_service, "execute_query", new=cap),
        patch.object(masters_service, "g2_ggwo_column_meta", ggwo_mock),
        patch.object(masters_service, "g2_gbun_column_meta", gbun_mock),
    ):
        asyncio.run(
            masters_service.list_inbound_vendors(
                server_id="remote_1", limit=50, offset=0, **kwargs
            )
        )
    return cap


class InboundVendorListFilterTests(TestCase):
    def test_gubun_exact_match(self) -> None:
        cap = _run(gubun="V01")
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("g.Gubun=%s", select_sql)
        self.assertIn("g.Gubun=%s", count_sql)
        self.assertIn("V01", select_params)
        self.assertIn("V01", count_params)
        self.assertNotIn(50, count_params)

    def test_jubun_like_filter(self) -> None:
        cap = _run(jubun="서울")
        select_sql, select_params = cap.select
        self.assertIn("g.Jubun LIKE %s", select_sql)
        self.assertTrue(any("%서울%" in str(p) for p in select_params))

    def test_q_search_includes_phone_columns(self) -> None:
        cap = _run(q="021")
        select_sql, _ = cap.select
        self.assertIn("g.Gtel1 LIKE", select_sql)
        self.assertIn("g.Guper LIKE", select_sql)

    def test_list_applies_scope_hcode_when_provided(self) -> None:
        cap = _Capture()
        ggwo_mock, gbun_mock = _meta()
        with (
            patch.object(masters_service, "execute_query", new=cap),
            patch.object(masters_service, "g2_ggwo_column_meta", ggwo_mock),
            patch.object(masters_service, "g2_gbun_column_meta", gbun_mock),
        ):
            asyncio.run(
                masters_service.list_inbound_vendors(
                    server_id="remote_1",
                    limit=50,
                    offset=0,
                    scope_hcode="PUB01",
                )
            )
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("g.Hcode=%s", select_sql)
        self.assertIn("g.Hcode=%s", count_sql)
        self.assertIn("PUB01", select_params)
        self.assertIn("PUB01", count_params)

    def test_list_select_uses_scalar_gbun_subquery_not_join(self) -> None:
        """Sobo12 — G2_Ggwo 단독 목록. Gubun 단독 JOIN 시 행 곱셈(82→574) 회귀 방지."""
        cap = _run()
        select_sql, count_sql = cap.select[0], cap.count[0]
        self.assertNotIn("LEFT JOIN G2_Gbun", select_sql)
        self.assertNotIn("LEFT JOIN G2_Gbun", count_sql)
        self.assertIn("FROM G2_Ggwo g", select_sql)
        self.assertIn("FROM G2_Ggwo g", count_sql)
        self.assertIn("gbun_name", select_sql)
        self.assertIn("(SELECT COALESCE(b.Gname,'') FROM G2_Gbun b", select_sql)
        self.assertIn("b.Gcode=g.Gubun", select_sql)
        self.assertIn("b.Hcode=g.Hcode", select_sql)
        self.assertIn("gjuso", select_sql)


if __name__ == "__main__":
    main(verbosity=2)
