"""로그인 공지·슬로건 로드 — 기동 레이스 재시도 + 환경별 안내 정적 가드.

배경: start.sh 는 백엔드/프론트를 동시에 띄우는데 uvicorn 기동이 더 느려,
로그인 페이지가 마운트 직후 1회 fetch 만 하면 일회성 실패로 실패 배너가
고착된다 (2026-07-03 로컬 신규 발생 보고). 또한 로컬 개발 실패에
"Vercel BLS_API_PROXY_TARGET" 안내가 떠 오진을 유도했다.

가드: (1) backoff 재시도 존재, (2) NODE_ENV 분기 dev/prod 메시지 분리.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase

_LOGIN_PAGE = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(public)" / "login" / "page.tsx"
)


class LoginPortalRetryStaticTests(TestCase):
    def setUp(self) -> None:
        self.src = _LOGIN_PAGE.read_text(encoding="utf-8")

    def test_portal_fetch_has_backoff_retry(self) -> None:
        self.assertIn("retryDelaysMs", self.src, "포털 fetch 재시도(backoff) 제거 금지 — 기동 레이스 배너 고착 회귀")
        self.assertIn("clearTimeout", self.src, "언마운트 시 재시도 타이머 정리 필요")

    def test_failure_hint_split_by_env(self) -> None:
        self.assertIn('process.env.NODE_ENV === "development"', self.src)
        self.assertIn("BLS_API_PROXY_TARGET", self.src)  # 배포(프록시) 안내는 prod 분기에 유지
        self.assertIn("uvicorn", self.src)  # 로컬 개발 안내
