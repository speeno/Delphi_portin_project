"""DEC-375 — 자동출력 창이 재클릭 · 새로고침 · 재로그인에도 죽지 않게.

Render 로그로 확인한 2026-10-02 교문사 「여러 건 중 한두 건만 출력」의 경위
--------------------------------------------------------------------------
- 08:33 서버 재시작(배포). 08:43~08:44 경리부가 5건 출고요청 + 바로출고 — 이때 연결된 자동출력 창 0개.
- 08:45 교문사 재로그인, 08:47:44 자동출력 창 연결 → 바로출고 1건(마산대) 인쇄.
- 08:48:58 자동출력 창이 **다시 로드**(헤더 버튼 재클릭 = `window.open(url, 이름)` 이 열린 창을 재이동) →
  받아 둔 나머지 바로출고 요청이 사라짐(서버 큐는 전달과 동시에 비워진다).
- 09:08 교보문고 1건 정상 인쇄. 09:13 같은 PC 에서 다시 로그인 → 3분 폴이 끊기고 창이 되살아나지 않음 →
  이후 출고요청(09:13 · 09:21 …)은 전부 미출력(델파이 처리).

가드
----
1. 이미 떠 있는 모니터는 다시 불러오지 않는다(빈 주소로 이름만 찾고, 모니터가 아닐 때만 이동).
2. 받은 바로출고 요청은 인쇄를 시도할 때까지 브라우저에 보관 — 다시 열리면 이어서 인쇄(10분 유효).
3. 모니터 생존 신호 → 헤더 버튼이 「자동출력 켜짐 / 꺼짐 · 열기」로 알린다.
4. 다른 탭의 로그인 · 로그아웃을 따라가고(storage), 로그인 화면은 원래 화면(next, 내부 경로만)으로 돌아간다 →
   만료 · 로그아웃으로 멈춘 자동출력 창이 본 창 재로그인만으로 되살아난다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class MonitorWindow(TestCase):
    def setUp(self) -> None:
        self.src = _read("lib/auto-print-window.ts")

    def test_open_does_not_reload_running_monitor(self) -> None:
        fn = self.src[self.src.index("export function openAutoPrintMonitor") :]
        fn = fn[: fn.index("\n}\n")]
        self.assertIn('window.open("", WINDOW_NAME,', fn)
        self.assertNotIn("window.open(url, WINDOW_NAME", fn)
        self.assertIn("win.location.pathname.startsWith(AUTO_PRINT_ROUTE)", fn)
        self.assertIn("if (!onMonitor) win.location.href = url;", fn)

    def test_heartbeat_and_pending_helpers(self) -> None:
        for name in ("writeMonitorBeat", "isMonitorAlive", "loadPendingUrgentKeys",
                     "addPendingUrgentKeys", "removePendingUrgentKey"):
            self.assertIn(f"export function {name}(", self.src, name)
        self.assertIn("const PENDING_TTL_MS = 10 * 60 * 1000;", self.src)


class MonitorPage(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/transactions/sales-statement/auto-print/page.tsx")

    def test_urgent_keys_persist_until_tried(self) -> None:
        start = self.src.index("const printUrgentKeys = useCallback(")
        body = self.src[start : self.src.index("[printFreshKeys],", start)]
        self.assertLess(body.index("addPendingUrgentKeys(fresh);"), body.index("printFreshKeys(fresh, removePendingUrgentKey)"))
        self.assertIn("onKeyTried?.(key);", self.src)
        self.assertIn("printUrgentKeys(keys);", self.src)

    def test_resume_and_heartbeat(self) -> None:
        self.assertIn("printUrgentKeys(loadPendingUrgentKeys());", self.src)
        self.assertIn("writeMonitorBeat(true)", self.src)
        self.assertIn("window.setInterval(() => writeMonitorBeat(true), MONITOR_BEAT_MS)", self.src)
        self.assertIn('window.addEventListener("pagehide", off);', self.src)


class HeaderAndSession(TestCase):
    def test_header_shows_monitor_state(self) -> None:
        src = _read("components/app-shell/header.tsx")
        self.assertIn("setMonitorAlive(isMonitorAlive())", src)
        # DEC-382 — 다른 PC 의 창(서버 연결 수)도 본다 · 「켜짐/꺼짐」은 설정으로 오해돼 «창» 상태로 표기.
        self.assertIn("const printerRunning = monitorAlive || (remoteListeners ?? 0) > 0;", src)
        self.assertIn("fetchAutoPrintListeners(sid)", src)
        self.assertIn('{printerRunning ? "자동출력 창 동작 중" : "자동출력 창 없음 · 열기"}', src)

    def test_cross_tab_session_sync(self) -> None:
        src = _read("contexts/auth-context.tsx")
        block = src[src.index("const onStorage = (e: StorageEvent) => {") :]
        block = block[: block.index("window.addEventListener")]
        self.assertIn('if (e.key !== "access_token") return;', block)
        self.assertIn("setUser(null);", block)
        self.assertIn("refreshUser().catch(() => setUser(null));", block)

    def test_login_returns_to_next_internal_only(self) -> None:
        src = _read("app/(public)/login/page.tsx")
        self.assertIn('const safe = next.startsWith("/") && !next.startsWith("//") && !next.startsWith("/login");', src)
        self.assertIn('router.replace(safe ? next : "/dashboard");', src)
        layout = _read("app/(app)/layout.tsx")
        self.assertIn("router.replace(embed && pathname ? `/login?next=${encodeURIComponent(here)}` : \"/login\");", layout)


if __name__ == "__main__":
    main()
