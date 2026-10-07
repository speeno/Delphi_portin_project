"""DEC-383 — 자동출력 창 «동작 중» 판정 = 창이 보내는 신호(정지하면 꺼짐) · 헤더 20초 확인.

보고(2026-10-07): 「자동출력 창 동작 중 메시지가 자동출력 상태가 정지인 상태에서도 자동출력 중인 것으로 처리된다」 · 「확인 간격 20초」.
원인: DEC-382 가 서버의 스트림 연결 수를 봤는데, 프록시(Vercel rewrite) 뒤에서는 창을 «정지»해 연결을 끊어도 서버 쪽 연결이 한동안 남는다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

from app.services import transactions_service as ts

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class BeatRegistry(TestCase):
    def setUp(self) -> None:
        ts._auto_print_beats.clear()  # noqa: SLF001

    def test_beat_stop_and_ttl(self) -> None:
        ts.record_auto_print_beat("5019", "win-a")
        ts.record_auto_print_beat("5019", "win-b")
        self.assertEqual(ts.auto_print_active_count("5019"), 2)
        ts.record_auto_print_beat("5019", "win-a", stop=True)  # 정지
        self.assertEqual(ts.auto_print_active_count("5019"), 1)
        self.assertEqual(ts.auto_print_active_count("9018"), 0)  # 회사별
        real = ts.time.monotonic
        with patch.object(ts.time, "monotonic", lambda: real() + ts._AUTO_PRINT_BEAT_TTL + 1):  # noqa: SLF001
            self.assertEqual(ts.auto_print_active_count("5019"), 0)  # 신호가 끊기면 동작 중 아님

    def test_empty_inputs_ignored(self) -> None:
        ts.record_auto_print_beat("", "x")
        ts.record_auto_print_beat("5019", "")
        self.assertEqual(ts.auto_print_active_count("5019"), 0)


class Wiring(TestCase):
    def test_monitor_sends_beat_only_while_running(self) -> None:
        src = (FE / "app" / "(app)" / "transactions" / "sales-statement" / "auto-print" / "page.tsx").read_text(encoding="utf-8")
        i = src.index("transactionsApi.autoPrintStatus({ serverId: sid, beat: beatId, stop })")
        block = src[i - 200 : i + 700]
        self.assertIn("if (!running) {\n      send(true);", block)
        self.assertIn("window.setInterval(() => send(false), 15_000)", block)

    def test_header_uses_active_every_20s(self) -> None:
        src = (FE / "components" / "app-shell" / "header.tsx").read_text(encoding="utf-8")
        self.assertIn("const AUTO_PRINT_STATUS_POLL_MS = 20_000;", src)
        self.assertIn("window.setInterval(poll, AUTO_PRINT_STATUS_POLL_MS)", src)
        self.assertIn("fetchAutoPrintActive(sid)", src)


if __name__ == "__main__":
    main()
