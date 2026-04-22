"""DEC-056 (Wave A) — LegacyIdLognProvider.fetch_fxx_matrix 단위 회귀.

검증 항목
---------
1. 행이 없으면 빈 dict 반환 (조용히 폴백).
2. 단일 행 + F11~F89 셀이 'O'/'R' 로 채워져 있으면 정규화된 dict 반환.
3. 빈 문자열/None/' ' (공백) 셀은 키 자체에서 누락.
4. 소문자 셀('o','r','x') 도 대문자로 정규화.
5. mysql3 bytes 응답 (euc-kr) 도 안전 디코딩.
6. SamlProvider/OidcProvider 는 ``hasattr(provider, 'fetch_fxx_matrix') == False`` —
   호출자 측 hasattr 분기로 안전 폴백.
7. ``execute_query`` 가 raise 하면 예외 전파 (호출자 측 try/except 책임).
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.core.auth_provider import (  # noqa: E402
    LegacyIdLognProvider,
    OidcProvider,
    SamlProvider,
    select_provider,
)


class FetchFxxMatrixTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.provider = LegacyIdLognProvider()

    async def test_empty_when_no_row(self) -> None:
        with patch("app.core.db.execute_query", new=AsyncMock(return_value=[])):
            result = await self.provider.fetch_fxx_matrix("remote_138", "ghost-user")
        self.assertEqual(result, {})

    async def test_single_row_normalized(self) -> None:
        row = {"F11": "O", "F12": "R", "F18": "X", "F26": "O", "gcode": "admin"}
        with patch("app.core.db.execute_query", new=AsyncMock(return_value=[row])):
            result = await self.provider.fetch_fxx_matrix("remote_138", "admin")
        self.assertEqual(
            result,
            {"F11": "O", "F12": "R", "F18": "X", "F26": "O"},
            "Fxx 셀이 정규화되어 반환되어야 함",
        )

    async def test_blank_and_none_cells_dropped(self) -> None:
        # 빈 문자열 / None / ' ' (공백) 셀은 누락 — 카탈로그 §2 의 ' ' = X 정책 동등
        row = {"F11": "O", "F12": "", "F13": None, "F14": " ", "F15": "R"}
        with patch("app.core.db.execute_query", new=AsyncMock(return_value=[row])):
            result = await self.provider.fetch_fxx_matrix("remote_138", "u1")
        self.assertEqual(result, {"F11": "O", "F15": "R"})

    async def test_lowercase_normalized_to_uppercase(self) -> None:
        row = {"F21": "o", "F22": "r", "F23": "x"}
        with patch("app.core.db.execute_query", new=AsyncMock(return_value=[row])):
            result = await self.provider.fetch_fxx_matrix("remote_138", "u1")
        self.assertEqual(result, {"F21": "O", "F22": "R", "F23": "X"})

    async def test_bytes_eucKR_decoded(self) -> None:
        # mysql3 raw 경로에서 bytes 가 섞일 수 있는 회귀 — auth_service._safe_str 패턴
        row = {"F11": "O".encode("euc-kr"), "F12": b"R"}
        with patch("app.core.db.execute_query", new=AsyncMock(return_value=[row])):
            result = await self.provider.fetch_fxx_matrix("remote_138", "u1")
        self.assertEqual(result, {"F11": "O", "F12": "R"})

    async def test_saml_oidc_no_method(self) -> None:
        # 호출자 측 안전 폴백 (hasattr 체크) 의 전제가 유효한지 확인
        self.assertFalse(hasattr(SamlProvider(), "fetch_fxx_matrix"))
        self.assertFalse(hasattr(OidcProvider(), "fetch_fxx_matrix"))
        self.assertTrue(hasattr(LegacyIdLognProvider(), "fetch_fxx_matrix"))
        self.assertTrue(hasattr(select_provider("legacy_id_logn"), "fetch_fxx_matrix"))

    async def test_execute_query_exception_propagates(self) -> None:
        with patch("app.core.db.execute_query", new=AsyncMock(side_effect=RuntimeError("boom"))):
            with self.assertRaises(RuntimeError):
                await self.provider.fetch_fxx_matrix("remote_138", "u1")


if __name__ == "__main__":
    main(verbosity=2)
