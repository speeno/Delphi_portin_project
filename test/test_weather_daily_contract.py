"""중기 regId 매핑 데이터 회귀 가드 (헤더 5일 기온)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
MID_REG_MAP = ROOT / "도서물류관리프로그램" / "backend" / "data" / "kma" / "mid_fcst_reg_map.json"


class WeatherDailyContractTests(TestCase):
    def test_mid_fcst_reg_map_covers_seoul_grid(self) -> None:
        data = json.loads(MID_REG_MAP.read_text(encoding="utf-8"))
        self.assertEqual(data.get("60,127"), "11B10101")


if __name__ == "__main__":
    main()
