"""플랫폼 지역 동기화 정적 회귀 가드."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACKEND = ROOT / "도서물류관리프로그램" / "backend"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PlatformRegionSyncStaticTests(TestCase):
    def test_platform_region_store_migrates_legacy_header_key(self) -> None:
        src = _read(FE_SRC / "lib" / "stores" / "platform-region-store.ts")
        self.assertIn("portal_platform_region_v1", src)
        self.assertIn("headerWeatherPresetStorageKey", src)
        self.assertIn("setManualPreset", src)
        self.assertIn("setGeolocationRegion", src)

    def test_widget_merge_respects_explicit_opt_out(self) -> None:
        src = _read(FE_SRC / "lib" / "platform-region-merge.ts")
        self.assertIn("config.usePlatformRegion === false", src)
        self.assertIn("regionValueDiffersFromDefault", src)
        self.assertIn("delivery-route-risk", src)
        self.assertIn("fuel-cost", src)

    def test_header_daily_weather_icons_are_wired(self) -> None:
        header = _read(FE_SRC / "components" / "app-shell" / "header-clock-weather.tsx")
        api = _read(FE_SRC / "lib" / "dashboard-api.ts")
        backend = _read(BACKEND / "app" / "services" / "dashboard_external_service.py")
        self.assertIn("DailyWeatherStatusIcon", header)
        self.assertIn("weather_icon", api)
        self.assertIn('"weather_icon": weather_icon', backend)


if __name__ == "__main__":
    main()
