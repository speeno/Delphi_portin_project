"""자동출력 모니터 접근 경로 회귀 가드 (DEC-249).

모니터는 클라우드 백엔드가 현장 프린터에 직결할 수 없어(OQ-002) **브라우저 창이 프린터 드라이버**
역할을 한다(DEC-111). 그래서 워크스페이스 탭이 아니라 «떠 있는 별도 창»이어야 하고, 어디서든
바로 열 수 있어야 한다. 종전엔 내정보 안쪽 텍스트 링크뿐이라 찾기 어려웠다.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (SRC / rel).read_text(encoding="utf-8")


class AutoPrintWindowHelper(unittest.TestCase):
    def test_named_popup_and_embed(self) -> None:
        src = _read("lib/auto-print-window.ts")
        self.assertIn('const WINDOW_NAME = "bls-auto-print-monitor"', src, "이름 붙인 창 = 중복 창 방지")
        self.assertIn("win.focus()", src, "이미 열려 있으면 그 창으로 포커스")
        self.assertIn("?embed=1", src, "좁은 팝업이라 사이드바·헤더 없이 연다")
        self.assertIn('window.open(url, "_blank")', src, "팝업 차단 시 폴백")

    def test_pref_cache_is_observable_in_same_tab(self) -> None:
        """`storage` 이벤트는 다른 탭에만 오므로 같은 탭용 CustomEvent 가 필요하다."""
        src = _read("lib/auto-print-window.ts")
        self.assertIn("dispatchEvent(new CustomEvent", src)
        self.assertIn('window.addEventListener("storage"', src)


class AccessPoints(unittest.TestCase):
    def test_header_button_gated_on_pref(self) -> None:
        src = _read("components/app-shell/header.tsx")
        self.assertIn('data-legacy-id="Header.OpenAutoPrintMonitor"', src)
        self.assertIn("{autoPrintOn && (", src, "자동출력 ON 계정에만 노출")
        self.assertIn("subscribeAutoPrintEnabled", src, "내정보에서 켜고 끄면 즉시 반영")
        self.assertIn("openAutoPrintMonitor", src)

    def test_profile_uses_button_not_buried_link(self) -> None:
        src = _read("app/(app)/settings/my-profile/page.tsx")
        self.assertIn('data-legacy-id="MyProfile.OpenAutoPrintMonitor"', src)
        self.assertIn("openAutoPrintMonitor", src)
        self.assertNotIn('href="/transactions/sales-statement/auto-print"', src, "묻힌 텍스트 링크 제거")
        self.assertIn("cacheAutoPrintEnabled", src, "저장·로드 시 헤더 버튼 노출 캐시 갱신")

    def test_theme_sync_caches_flag_on_load(self) -> None:
        src = _read("components/shared/theme-sync.tsx")
        self.assertIn("cacheAutoPrintEnabled", src)
        self.assertIn("sales_statement_auto_print", src)


if __name__ == "__main__":
    unittest.main()
