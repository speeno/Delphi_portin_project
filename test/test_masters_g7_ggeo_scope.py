"""G7_Ggeo 출판사 lookup scope 회귀 — Seak80 / Subu59 정본.

레거시 Seak80.FilterTing 은 ``G7_Ggeo`` 에서 ``Gcode``/``Gname`` 검색 후
선택한 ``Gcode`` 를 S1_Ssub ``Hcode`` 필터에 사용한다(Subu59_1 Button701).
``G7_Ggeo.Hcode`` 컬럼은 별도 마스터 필드이므로 목록 scope 에 쓰면 0건 회귀.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.hcode_isolation import (  # noqa: E402
    resolve_g7_ggeo_list_scope,
    resolve_scope_hcode,
)
from app.services import masters_service  # noqa: E402


class _Capture:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    async def __call__(self, _server_id: str, sql: str, params=()):
        self.calls.append((sql, tuple(params or ())))
        if "COUNT(*)" in sql.upper():
            return [{"row_count": 3}]
        return [{"gcode": "P1", "gname": "출판사", "hcode": "", "chek1": "", "chek2": ""}]


class G7GgeoListScopeTests(TestCase):
    def test_list_publishers_scopes_on_gcode_not_hcode(self) -> None:
        cap = _Capture()
        with patch.object(masters_service, "execute_query", new=cap):
            asyncio.run(
                masters_service.list_publishers(
                    server_id="remote_138",
                    q=None,
                    limit=50,
                    offset=0,
                    scope_hcode="5019",
                )
            )
        select_sql, select_params = cap.calls[0]
        self.assertIn("Gcode=%s", select_sql)
        self.assertNotIn("Hcode=%s", select_sql)
        self.assertEqual(select_params[0], "5019")

    def test_resolve_g7_scope_t2_pub_returns_login_hcode(self) -> None:
        ctx = {
            "role": "operator",
            "hcode": "5019",
            "permissions": ["master.read"],
            "account_type": "T2_PUB",
            "account_family": "",
        }
        self.assertEqual(resolve_g7_ggeo_list_scope(ctx), "5019")

    def test_resolve_g7_scope_t2_dist_returns_none_for_seak80_broad_list(self) -> None:
        ctx = {
            "role": "operator",
            "hcode": "1001",
            "permissions": ["master.read"],
            "account_type": "T2_DIST",
            "account_family": "kbt",
        }
        self.assertIsNone(resolve_g7_ggeo_list_scope(ctx))
        # 거래 데이터 scope 는 여전히 login hcode 적용(정책 분리).
        self.assertEqual(resolve_scope_hcode(ctx), "1001")

    def test_resolve_g7_scope_super_returns_none(self) -> None:
        ctx = {
            "role": "admin",
            "hcode": "0000",
            "permissions": ["*"],
            "account_type": "T1",
            "account_family": "",
        }
        self.assertIsNone(resolve_g7_ggeo_list_scope(ctx))


class SearchCustomersG1ScopeTests(TestCase):
    """출고접수/거래명세서 거래처 자동완성 — G1_Ggeo(거래처관리와 동일 소스).

    거래처(서점/상대처)는 ``거래처관리 = G1_Ggeo``(Hcode=소유 계정, Gcode=거래처코드)
    에서 관리되며, 거래처 검색 팝업(customerList)도 G1_Ggeo 를 쓴다. 인라인
    자동완성도 동일 소스를 로그인 계정 ``Hcode`` 스코프로 조회해야 한다.

    회귀: 이전엔 G7_Ggeo(출판사 테이블)를 조회해, 창고 DB(chul_09)처럼 G7_Ggeo 에
    본인 출판사(5019)만 있는 계정에서 거래처를 골라도 본인 hcode 가 등록됐다.
    """

    def _run(self, scope):
        calls: list[tuple[str, tuple[object, ...]]] = []

        async def _cap(_sid: str, sql: str, params=()):
            calls.append((sql, tuple(params or ())))
            return []

        with patch.object(masters_service, "execute_query", new=_cap):
            asyncio.run(
                masters_service.search_customers(
                    server_id="remote_153", q="교보", limit=10, scope_hcode=scope
                )
            )
        return calls[0]

    def test_queries_g1_ggeo_not_g7(self) -> None:
        sql, _ = self._run("5019")
        self.assertIn("FROM G1_Ggeo", sql)
        self.assertNotIn("G7_Ggeo", sql)

    def test_scopes_on_hcode_owner(self) -> None:
        # G1_Ggeo 격리 키 = Hcode(소유 계정). scope 가 Hcode 컬럼에 적용돼야 한다.
        sql, params = self._run("5019")
        self.assertIn("Hcode=%s", sql)
        self.assertIn("5019", params)

    def test_like_group_parenthesized_so_scope_does_not_leak_via_or(self) -> None:
        sql, _ = self._run("5019")
        self.assertIn("(Gcode LIKE %s OR Gname LIKE %s)", sql)
        self.assertNotEqual(sql.find(") AND "), -1, "scope 필터가 LIKE 그룹 밖 AND 로 결합돼야 한다")


if __name__ == "__main__":
    main(verbosity=2)
