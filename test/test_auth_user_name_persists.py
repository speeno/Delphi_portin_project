"""헤더 표시 조직명(user_name=Id_Logn.Hname)이 토큰 갱신·/me 후에도 유지 (2026-06-22).

회귀: refresh 경로와 ``get_current_user`` 가 ``user_name`` 을 복원하지 않아, 로그인 직후엔
조직명(예: 교문사)이 보이다가 토큰 갱신/페이지 새로고침(/me) 후 헤더 배지가 hcode(5019)
로 "원복" 되던 문제. → ``hname`` 클레임을 JWT 에 실어 access/refresh 양쪽에서 복원한다.

헤더 배지 식: ``user_name || display_name || hcode`` — user_name 이 유지되어야 코드가
아닌 이름이 표시된다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _login_user() -> dict:
    return {
        "user_id": "kyomun01",
        "server_id": "remote_153",
        "user_name": "교문사",   # Id_Logn.Hname (조직명/출판사명)
        "hcode": "5019",
        "role": "user",
        "permissions": [],
        "gname": "홍길동",
    }


class TokenCarriesHnameClaim(TestCase):
    def test_access_and_refresh_tokens_carry_hname(self) -> None:
        from app.routers.auth import _make_token_pair, decode_token

        pair = _make_token_pair(_login_user())
        self.assertEqual(decode_token(pair.access_token).get("hname"), "교문사")
        # refresh 토큰도 실어야 갱신 경로에서 복원 가능(원복 차단의 핵심).
        self.assertEqual(decode_token(pair.refresh_token).get("hname"), "교문사")


class CurrentUserRestoresUserName(IsolatedAsyncioTestCase):
    async def test_get_current_user_restores_user_name(self) -> None:
        from app.routers.auth import _make_token_pair, get_current_user
        from fastapi.security import HTTPAuthorizationCredentials

        token = _make_token_pair(_login_user()).access_token
        cred = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        ctx = await get_current_user(cred)
        # /me 는 이 ctx 로 UserInfo 를 만든다 → user_name 이 채워져야 헤더가 이름 표시.
        self.assertEqual(ctx.get("user_name"), "교문사")
        self.assertNotEqual(ctx.get("user_name"), ctx.get("hcode"))  # 코드 아님


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
