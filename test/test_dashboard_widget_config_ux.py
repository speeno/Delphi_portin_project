"""
대시보드 위젯 설정 UX 회귀 가드.

목적
----
- 교통 ETA/지도/배송리스크 위젯이 bbox 숫자를 직접 JSON 으로 입력하는 방식으로
  되돌아가지 않도록 막는다.
- 지역명 프리셋 선택 → minX/maxX/minY/maxY 설정 헬퍼가 유지되는지 정적으로 확인한다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"

REGION_PRESETS = FE_SRC / "lib" / "dashboard-region-presets.ts"
CONFIG_DIALOG = FE_SRC / "components" / "dashboard" / "dashboard-widget-config-dialog.tsx"
ROLE_VIEW = FE_SRC / "components" / "dashboard" / "role-dashboard-view.tsx"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DashboardWidgetConfigUxTests(TestCase):
    def test_region_preset_helper_exports_bounds_and_weather_fields(self) -> None:
        src = _read(REGION_PRESETS)
        self.assertIn("DASHBOARD_REGION_PRESETS", src)
        self.assertIn("applyDashboardRegionPreset", src)
        self.assertIn('id: "seoul"', src)
        for key in ("minX", "maxX", "minY", "maxY", "lat", "lon", "nx", "ny"):
            self.assertIn(key, src, f"region preset field missing: {key}")

    def test_config_dialog_uses_region_select_for_traffic_widgets(self) -> None:
        src = _read(CONFIG_DIALOG)
        self.assertIn("DASHBOARD_REGION_PRESETS.map", src)
        self.assertIn("applyDashboardRegionPreset", src)
        for kind in (
            "external.traffic_eta",
            "external.traffic_forecast",
            "external.traffic_map",
            "external.delivery_route_risk",
        ):
            self.assertIn(kind, src, f"traffic widget kind missing from dialog: {kind}")

    def test_role_dashboard_view_no_longer_uses_window_prompt_json_config(self) -> None:
        src = _read(ROLE_VIEW)
        self.assertNotIn("window.prompt", src)
        self.assertIn("DashboardWidgetConfigDialog", src)
        self.assertIn("saveDashboardWidgetConfig", src)


if __name__ == "__main__":
    main(verbosity=2)
