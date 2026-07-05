"""
Sobo11 거래처 목록 — 검색 필터 확장 회귀 가드 (minimal 세트).

대상
----
``masters_service.list_customer_master`` 에 추가된 필터 인자
(``gubun`` / ``jubun`` / ``exclude_terminated``) 가 SELECT·COUNT 두 쿼리에
**동일하게** WHERE 절로 합성되고, params 순서/길이가 일관되는지 service
레벨에서 검증한다 (페이지네이션 total 정합 보장).

설계
----
- DB 미연결 — ``masters_service.execute_query`` 만 patch 하여 SQL/params 캡처
  (test_masters_q_search.py 의 _Capture 패턴 재사용).
- 4서버 호환: 표준 ``=`` / ``LIKE`` / ``IFNULL`` 만 사용하므로 MySQL 3.x
  지장 없음 — multi-db-compat 룰 §2 준수.
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


async def _fake_geo_meta(server_id: str):  # noqa: ARG001
    # 목록 선택 컬럼 DDL 메타 stub — 실제 SHOW COLUMNS(DB) 회피. gubun 존재(구분명 해석) 가정.
    cols = {"gubun", "jubun", "gposa", "gnumb", "guper", "gjomo", "gfax1", "gbigo", "email"}
    return cols, {c: c.capitalize() for c in cols}


async def _fake_gbun_map(server_id: str, *, scope_hcode=None):  # noqa: ARG001
    return {}


def _run(**kwargs) -> _Capture:
    cap = _Capture()
    with patch.object(masters_service, "execute_query", new=cap), \
            patch.object(masters_service, "g1_geo_column_meta", new=_fake_geo_meta), \
            patch.object(masters_service, "_gbun_code_name_map", new=_fake_gbun_map):
        asyncio.run(
            masters_service.list_customer_master(
                server_id="remote_1", limit=50, offset=0, **kwargs
            )
        )
    return cap


class CustomerListFilterTests(TestCase):
    # ── 개별 필터 ───────────────────────────────────────────────────────────
    def test_no_filters_baseline(self) -> None:
        cap = _run()
        self.assertEqual(len(cap.calls), 2)
        select_sql, select_params = cap.select
        self.assertNotIn("Gubun=%s", select_sql)
        self.assertNotIn("Jubun LIKE", select_sql)
        self.assertNotIn("Gname NOT LIKE", select_sql)
        # LIMIT/OFFSET 만
        self.assertEqual(select_params, (50, 0))

    def test_gubun_exact_match(self) -> None:
        cap = _run(gubun="A01")
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count
        self.assertIn("Gubun=%s", select_sql)
        self.assertIn("Gubun=%s", count_sql)
        self.assertIn("A01", select_params)
        self.assertIn("A01", count_params)
        self.assertEqual(select_params[-2:], (50, 0))

    def test_gubun_blank_ignored(self) -> None:
        cap = _run(gubun="   ")
        self.assertNotIn("Gubun=%s", cap.select[0])

    def test_jubun_like(self) -> None:
        cap = _run(jubun="서울")
        select_sql, select_params = cap.select
        self.assertIn("Jubun LIKE %s", select_sql)
        self.assertIn("%서울%", select_params)
        # COUNT 도 동일 절
        self.assertIn("Jubun LIKE %s", cap.count[0])

    def test_exclude_terminated(self) -> None:
        cap = _run(exclude_terminated=True)
        select_sql, select_params = cap.select
        self.assertIn("Gname NOT LIKE %s", select_sql)
        self.assertIn("IFNULL(Gubun,'')<>%s", select_sql)
        self.assertIn("[X]%", select_params)
        self.assertIn("X 거래종료", select_params)
        # COUNT 정합
        count_sql, count_params = cap.count
        self.assertIn("Gname NOT LIKE %s", count_sql)
        self.assertIn("[X]%", count_params)

    def test_exclude_terminated_off_default(self) -> None:
        cap = _run(exclude_terminated=False)
        self.assertNotIn("Gname NOT LIKE", cap.select[0])

    # ── 결합 (q + 3필터) — params 길이/정합 ────────────────────────────────
    def test_all_filters_combined(self) -> None:
        cap = _run(q="도서", gubun="A01", jubun="서울", exclude_terminated=True)
        select_sql, select_params = cap.select
        count_sql, count_params = cap.count

        for sql in (select_sql, count_sql):
            self.assertIn("LIKE %s OR Gname LIKE %s", sql)  # q
            self.assertIn("Gubun=%s", sql)
            self.assertIn("Jubun LIKE %s", sql)
            self.assertIn("Gname NOT LIKE %s", sql)
            self.assertIn("IFNULL(Gubun,'')<>%s", sql)

        # SELECT params = WHERE params + (limit, offset)
        # WHERE: q,q, gubun, jubun, [X]%, 'X 거래종료' = 6개
        self.assertEqual(select_params[-2:], (50, 0))
        self.assertEqual(list(select_params[:-2]), list(count_params))
        self.assertEqual(len(count_params), 6)

    def test_where_consistency_select_vs_count(self) -> None:
        """SELECT 와 COUNT 의 WHERE params 는 항상 동일해야 페이징 total 이 맞다."""
        cap = _run(gubun="A01", jubun="부산", exclude_terminated=True)
        _, select_params = cap.select
        _, count_params = cap.count
        self.assertEqual(list(select_params[:-2]), list(count_params))


class CustomerListResponseModelTests(TestCase):
    """response_model 회귀 — 서비스가 채운 목록 선택 컬럼을 FastAPI 가 잘라내지 않아야 한다.

    CustomerListItem(Pydantic response_model)에 필드가 없으면 서비스가 sname 등을 채워도
    응답에서 제거돼 화면 컬럼이 빈값으로 나온다(2026-07-05 거래처구분 미표시 버그).
    """

    def test_response_model_declares_new_columns(self) -> None:
        from app.models.master import CustomerListItem

        fields = set(CustomerListItem.model_fields.keys())
        for f in ("sname", "jubun", "gposa", "gnumb", "guper", "gjomo", "gfax1", "gbigo", "email"):
            self.assertIn(f, fields, f"CustomerListItem 에 {f} 누락 → 응답에서 잘림")

    def test_model_round_trips_values(self) -> None:
        from app.models.master import CustomerListItem

        m = CustomerListItem(gcode="00000", gname="창고", sname="교문사 관련", jubun="서울")
        dumped = m.model_dump()
        self.assertEqual(dumped["sname"], "교문사 관련")
        self.assertEqual(dumped["jubun"], "서울")


if __name__ == "__main__":
    main()
