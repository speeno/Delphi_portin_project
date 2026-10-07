"""DEC-385 — 서버 시각 = 서울(KST).

사용자(2026-10-07) 「서버 출력 시간을 현지 서울 기준 시간으로 변경해줘」. Render 컨테이너는 UTC 라 출력 이력(PrintedAt) ·
로그 · 「오늘」 판정(자동출력 스트림 · 반품 기본 일자 · CJ 접수일)이 9시간 어긋났다(KST 00~09시는 전날).
정본 = Dockerfile ``TZ=Asia/Seoul`` + tzdata, 다른 실행 환경은 main.py 가 미설정 시 같은 값으로 정한다.
"""

from __future__ import annotations

import os
import time
import unittest
from datetime import datetime
from pathlib import Path

import app.main  # noqa: F401 — 시간대 설정 부작용

BACK = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "backend"


class ServerTimeKst(unittest.TestCase):
    def test_dockerfile_pins_seoul(self) -> None:
        src = (BACK / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("TZ=Asia/Seoul", src)
        self.assertIn("    tzdata", src)

    def test_main_defaults_tz(self) -> None:
        src = (BACK / "app" / "main.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.setdefault("TZ", "Asia/Seoul")', src)
        self.assertIn("time.tzset()", src)

    def test_process_local_time_is_kst(self) -> None:
        if os.environ.get("TZ") != "Asia/Seoul":
            self.skipTest("실행 환경이 TZ 를 따로 정함(명시값 우선)")
        self.assertEqual(datetime.now().astimezone().utcoffset().total_seconds(), 9 * 3600)
        self.assertIn("KST", time.tzname)

    def test_today_not_forced_utc(self) -> None:
        for rel in ("app/services/returns_service.py", "app/services/cj_booking_service.py"):
            self.assertNotIn("datetime.now(timezone.utc)", (BACK / rel).read_text(encoding="utf-8"), rel)


if __name__ == "__main__":
    unittest.main()
