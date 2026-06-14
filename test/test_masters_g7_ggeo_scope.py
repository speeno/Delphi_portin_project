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


if __name__ == "__main__":
    main(verbosity=2)
