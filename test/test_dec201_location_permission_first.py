"""DEC-201 — 시계·날짜·날씨는 브라우저 위치 권한을 받은 뒤 그 위치를 반영한다 (2026-08-25 사용자 규칙).

원문: "시간, 날짜 정보 관련해서는 현재 브라우저 위치 정보 접근 허가를 득한 뒤 위치정보를 반영해야한다."

종전 결함
--------
- 수동 프리셋(source "manual")이 위치를 **영구 차단**했고, 구 프리셋 키를 옮겨 온 계정은 모두
  "manual" 로 굳어 브라우저 권한이 granted 여도 헤더가 「서울」 고정이었다.
- 「나중에」가 localStorage 영구 «dismissed» 라 권한 요청 자체가 다시 뜨지 않았다.

수정
----
- 저장소: setGeolocationRegion 의 manual 가드 제거 — 권한 허용 시 위치 우선.
- 부트스트랩: navigator.permissions.query 로 상태 확인 → granted 면 묻지 않고 반영(onchange 재반영),
  denied 면 조용히 유지, prompt 면 배너. 「나중에」는 sessionStorage(이번 접속만).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class StorePolicy(TestCase):
    def test_geolocation_overrides_manual_preset(self) -> None:
        src = _read("lib/stores/platform-region-store.ts")
        i = src.index("setGeolocationRegion: (input, serverId, userId) => {")
        body = src[i : i + 900]
        self.assertNotIn('if (prev.source === "manual") return;', body, "수동 프리셋이 위치를 차단하면 안 된다")
        self.assertIn('source: "geolocation"', body)


class BootstrapFlow(TestCase):
    def setUp(self) -> None:
        self.src = _read("components/app-shell/location-permission-bootstrap.tsx")

    def test_uses_permissions_api_and_reacts_to_change(self) -> None:
        self.assertIn('.query({ name: "geolocation" })', self.src)
        self.assertIn("s.onchange = () => decide(s.state, true)", self.src)
        self.assertIn('if (state === "granted")', self.src)
        self.assertIn('if (state === "denied")', self.src)

    def test_granted_applies_without_asking(self) -> None:
        self.assertIn("refreshFromGrantedPermission", self.src)
        self.assertIn("navigator.geolocation.getCurrentPosition", self.src)
        self.assertIn("weatherGridFromPoint", self.src)
        self.assertIn("setGeolocationRegion", self.src)

    def test_manual_no_longer_suppresses_prompt(self) -> None:
        self.assertNotIn('platformRegion.source === "manual"', self.src)

    def test_dismiss_is_session_scoped(self) -> None:
        self.assertIn("writeLocationPermissionSessionDismissed(serverId, userId)", self.src)
        self.assertIn("readLocationPermissionSessionDismissed(serverId, userId)", self.src)
        # 영구 dismissed 기록은 더 이상 쓰지 않는다
        self.assertNotIn('writePermissionFlag(serverId, userId, "dismissed")', self.src)
        storage = _read("lib/location-permission-storage.ts")
        self.assertIn("sessionStorage", storage)
        self.assertIn("portal_location_permission_dismissed_session_v1", storage)

    def test_effect_has_no_sync_set_state(self) -> None:
        """react-hooks 규칙 — effect 본문의 동기 setState 금지 (마이크로태스크로)."""
        self.assertIn("queueMicrotask", self.src)

    def test_banner_copy_mentions_clock_and_date(self) -> None:
        self.assertIn("시계·날짜·날씨", self.src)

    def test_mounted_in_app_shell(self) -> None:
        layout = _read("app/(app)/layout.tsx")
        self.assertIn("<LocationPermissionBootstrap />", layout)


if __name__ == "__main__":
    main()
