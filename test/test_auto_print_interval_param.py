"""자동출력 모니터 폴링 간격 파라미터(?intervalSec=) 정적 가드.

키오스크 바로가기 URL 로 폴링 간격을 조절한다(기본 3분, 30~1800초 클램프).
백엔드 폭주 방지 하한(30초)과 파라미터 자체가 제거되지 않도록 가드한다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase

_PAGE = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
    / "transactions" / "sales-statement" / "auto-print" / "page.tsx"
)


class AutoPrintIntervalParamTests(TestCase):
    def setUp(self) -> None:
        self.src = _PAGE.read_text(encoding="utf-8")

    def test_interval_param_exists(self) -> None:
        self.assertIn('get("intervalSec")', self.src)

    def test_interval_clamped_min_30_max_1800(self) -> None:
        # 하한 30초 = 폴링 폭주로 원격 DB/Render 를 때리는 사고 방지.
        self.assertIn("Math.max(30", self.src)
        self.assertIn("Math.min(1800", self.src)

    def test_poll_loop_uses_dynamic_interval(self) -> None:
        self.assertIn("setInterval(run, pollMs)", self.src)

    def test_countdown_display_present(self) -> None:
        # 다음 자동 트리거까지 남은 시간(분/초) 표시 — 사용자 요청(2026-07-03).
        self.assertIn("formatCountdown", self.src)
        self.assertIn("nextRunAtRef", self.src)
        self.assertIn("다음 확인까지", self.src)
