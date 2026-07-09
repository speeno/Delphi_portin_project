"""DEC-095 — 테넌트 DB 요청 컨텍스트 회귀 가드.

사고: 비-기본 DB 테넌트(도서출판 배움 = remote_153/chul_05_db, hcode 1002)로 로그인
시 전 화면 0건 — JWT ``rdb``(resolved_db) 클레임이 있는데 데이터 API 가 서버 프로필
기본 DB(chul_09_db)로만 접속(라이브 검증: chul_09_db 0건 vs chul_05_db 444,262건).

수정: get_current_user 가 rdb 를 요청 범위 ContextVar 에 바인딩,
_effective_database 우선순위 = inspect > tenant(서버 일치 시) > 프로필 기본.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.db import _effective_database  # noqa: E402
from app.core.inspect_context import clear_inspect_context, set_inspect_context  # noqa: E402
from app.core.tenant_db_context import (  # noqa: E402
    clear_tenant_db_context_for_tests,
    get_tenant_db_context,
    set_tenant_db_context,
)

_PROFILE = {"database": "chul_09_db"}


class EffectiveDatabaseTests(TestCase):
    def setUp(self) -> None:
        clear_tenant_db_context_for_tests()
        clear_inspect_context()

    def tearDown(self) -> None:
        clear_tenant_db_context_for_tests()
        clear_inspect_context()

    def test_default_without_context(self) -> None:
        self.assertEqual(_effective_database("remote_153", _PROFILE), "chul_09_db")

    def test_tenant_context_overrides_default(self) -> None:
        set_tenant_db_context("remote_153", "chul_05_db")
        self.assertEqual(_effective_database("remote_153", _PROFILE), "chul_05_db")

    def test_tenant_context_ignored_for_other_server(self) -> None:
        # 다른 소유 서버 조회에 잘못된 DB 를 강제하지 않는다.
        set_tenant_db_context("remote_153", "chul_05_db")
        self.assertEqual(_effective_database("remote_138", _PROFILE), "chul_09_db")

    def test_inspect_overlay_wins_over_tenant(self) -> None:
        set_tenant_db_context("remote_153", "chul_05_db")
        set_inspect_context(server_id="remote_153", db_name="book_11_db", reason="test")
        self.assertEqual(_effective_database("remote_153", _PROFILE), "book_11_db")

    def test_empty_values_do_not_bind(self) -> None:
        set_tenant_db_context("", "chul_05_db")
        set_tenant_db_context("remote_153", "")
        self.assertIsNone(get_tenant_db_context())


class GetCurrentUserBindingTests(TestCase):
    def setUp(self) -> None:
        clear_tenant_db_context_for_tests()

    def tearDown(self) -> None:
        clear_tenant_db_context_for_tests()

    def test_jwt_rdb_claim_binds_context(self) -> None:
        # ContextVar 는 태스크 범위 — 검증을 동일 코루틴 안에서 수행
        # (실서비스에서 요청 task 하나가 인증 의존성과 쿼리를 모두 실행하는 구조와 동일).
        import asyncio

        from app.core.security import create_access_token
        from app.routers.auth import get_current_user

        token = create_access_token({
            "sub": "배움", "sid": "remote_153", "hcode": "1002",
            "role": "operator", "permissions": [], "rdb": "chul_05_db",
        })

        class _Cred:
            credentials = token

        async def flow() -> tuple[dict, tuple[str, str] | None, str]:
            user = await get_current_user(_Cred())
            ctx = get_tenant_db_context()
            eff = _effective_database("remote_153", _PROFILE)
            return user, (ctx.server_id, ctx.db_name) if ctx else None, eff

        user, ctx_pair, eff = asyncio.run(flow())
        self.assertEqual(user["resolved_db"], "chul_05_db")
        self.assertEqual(ctx_pair, ("remote_153", "chul_05_db"))
        self.assertEqual(eff, "chul_05_db", "쿼리 경로가 테넌트 DB 로 라우팅")

    def test_no_rdb_claim_leaves_context_unbound(self) -> None:
        import asyncio

        from app.core.security import create_access_token
        from app.routers.auth import get_current_user

        token = create_access_token({
            "sub": "admin", "sid": "remote_153", "hcode": "0000",
            "role": "admin", "permissions": ["*"],
        })

        class _Cred:
            credentials = token

        async def flow():
            await get_current_user(_Cred())
            return get_tenant_db_context(), _effective_database("remote_153", _PROFILE)

        ctx, eff = asyncio.run(flow())
        self.assertIsNone(ctx)
        self.assertEqual(eff, "chul_09_db", "rdb 없는 계정은 프로필 기본 DB 유지")


if __name__ == "__main__":
    main()
