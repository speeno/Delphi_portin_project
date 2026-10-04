"""DEC-377 — 성능 계측(요청별 소요 시간 · DB 조회 횟수) + 화면 열 때 중복 요청 제거.

배경(사용자 2026-10-05 「서비스 성능을 높이기 위해 할 수 있는 일 — 3 · 5번 바로 실행」)
- 같은 도서 목록 조회가 로컬 0.42초 · 운영 약 7초. 백엔드(싱가포르) ↔ DB(한국) 왕복이 조회 횟수만큼 쌓인다.
  어느 화면이 느린지 수치가 없어 감으로 고치고 있었다 → 요청마다 `perf … 1234ms db=12/980ms` 한 줄 + `Server-Timing` 헤더.
- 워크스페이스는 창(iframe)마다 사용자 정보 · 내정보 · 메뉴 정책을 다시 불렀다(운영 로그: 3초 동안 /auth/me 5회 ·
  /me/profile 4회 · 메뉴 정책 2회) → 같은 탭의 창들이 함께 쓰는 짧은 캐시(sessionStorage, 토큰별 키).
"""

from __future__ import annotations

import logging
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core import db, perf_context
from app.main import app

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class DbStats(IsolatedAsyncioTestCase):
    async def test_execute_query_counts_round_trips(self) -> None:
        stats = perf_context.begin()
        with patch.object(db, "_execute_query", AsyncMock(return_value=[{"a": 1}])):
            self.assertEqual(await db.execute_query("remote_153", "SELECT 1", ()), [{"a": 1}])
            await db.execute_query("remote_153", "SELECT 2", ())
        self.assertEqual(int(stats["n"]), 2)
        self.assertGreaterEqual(stats["ms"], 0.0)

    async def test_failed_query_is_still_counted(self) -> None:
        stats = perf_context.begin()
        with patch.object(db, "_execute_query", AsyncMock(side_effect=RuntimeError("boom"))):
            with self.assertRaises(RuntimeError):
                await db.execute_query("remote_153", "SELECT 1", ())
        self.assertEqual(int(stats["n"]), 1)

    def test_no_request_context_is_noop(self) -> None:
        perf_context._stats.set(None)  # noqa: SLF001
        perf_context.add_db(12.0)  # 예외 없이 무시


class PerfMiddleware(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_server_timing_header_and_log_line(self) -> None:
        with self.assertLogs("perf", level=logging.INFO) as cm:
            r = self.client.get("/api/v1/auth/login-policy")
        self.assertIn("app;dur=", r.headers.get("server-timing", ""))
        self.assertIn("db;dur=", r.headers.get("server-timing", ""))
        line = cm.output[-1]
        self.assertRegex(line, r"perf GET /api/v1/auth/login-policy \d+ \d+ms db=\d+/\d+ms")

    def test_health_check_is_not_logged(self) -> None:
        logger = logging.getLogger("perf")
        with self.assertLogs("perf", level=logging.INFO) as cm:
            logger.info("marker")  # assertLogs 는 로그가 0건이면 실패하므로 표식 하나를 남긴다
            r = self.client.get("/api/v1/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual([m for m in cm.output if "/api/v1/health" in m], [])
        self.assertNotIn("server-timing", {k.lower() for k in r.headers})


class SharedGetCacheWiring(TestCase):
    def test_cache_is_token_scoped_and_tab_shared(self) -> None:
        src = _read("lib/shared-get-cache.ts")
        self.assertIn('localStorage.getItem("access_token") || "").slice(-16)', src)  # 계정이 바뀌면 다른 칸
        self.assertIn("sessionStorage.setItem(key", src)  # 같은 탭의 iframe 과 공유
        self.assertIn("const pending = inflight.get(key);", src)  # 같은 문서의 동시 요청 합치기
        for fn in ("cachedGet", "seedCachedGet", "invalidateCachedGet"):
            self.assertIn(f"export {'async ' if fn == 'cachedGet' else ''}function {fn}", src)

    def test_user_profile_menu_policy_use_cache(self) -> None:
        auth = _read("contexts/auth-context.tsx")
        self.assertIn("cachedGet<UserInfo>(ME_PATH, ME_TTL_MS, { force })", auth)
        self.assertIn("loadUser(false)", auth)  # 창을 열 때는 함께 쓰는 값
        self.assertIn("const refreshUser = useCallback(() => loadUser(true), [loadUser]);", auth)  # 명시적 새로고침은 서버
        self.assertGreaterEqual(auth.count("invalidateCachedGet();"), 3)  # 복원 실패 · 로그인 · 로그아웃
        self.assertIn("seedCachedGet(ME_PATH, res.user);", auth)
        me = _read("lib/me-api.ts")
        self.assertIn("cachedGet<MyProfileResponse>(PROFILE_PATH, PROFILE_TTL_MS, { force: opts.fresh })", me)
        self.assertEqual(me.count("profileChanged(await api."), 3)  # 저장 · 로고 올리기 · 로고 지우기
        admin = _read("lib/admin-api.ts")
        self.assertIn('cachedGet<MenuPolicyOverridesDoc>("/api/v1/admin/menu-policy/runtime"', admin)
        self.assertIn('invalidateCachedGet("/api/v1/admin/menu-policy/runtime");', admin)

    def test_profile_editor_reads_fresh(self) -> None:
        self.assertIn("getMyProfile({ fresh: true })", _read("app/(app)/settings/my-profile/page.tsx"))


if __name__ == "__main__":
    main()
