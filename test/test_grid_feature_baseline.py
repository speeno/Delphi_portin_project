"""표(목록) 기능 기준선 가드 — DEC-212 (2026-08-26 사용자 규칙).

"이번 디자인 변경으로 이런 기존 기능에 대한 누락이나 제거는 이후에 꼭 확인 과정을 거쳐서 진행해야 한다."
화면별 표 기능 지표(DataGrid·컬럼 설정·정렬·좌우 이동·리사이즈·키보드·페이저)가
`analysis/audit/grid-feature-baseline.json` 기준선보다 **어느 화면에서든 줄면 실패**한다.
의도한 변경이면 `python3 tools/grid_feature_baseline.py` 로 기준선을 재생성해 승인한다.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "grid_feature_baseline.py"
BASELINE = ROOT / "analysis" / "audit" / "grid-feature-baseline.json"


class GridFeatureBaseline(TestCase):
    def test_no_screen_lost_grid_features(self) -> None:
        res = subprocess.run([sys.executable, str(TOOL), "--check"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_ledger_screens_now_use_data_grid(self) -> None:
        files = json.loads(BASELINE.read_text(encoding="utf-8"))["files"]
        for rel in ("app/(app)/inventory/ledger/page.tsx", "app/(app)/ledger/customer/page.tsx"):
            m = files[rel]
            self.assertGreaterEqual(m["data_grid"], 2, rel)
            self.assertGreaterEqual(m["column_settings"], 2, rel)
            self.assertGreaterEqual(m["reorder"], 2, rel)
            self.assertGreaterEqual(m["resize"], 2, rel)
            self.assertGreaterEqual(m["sortable"], 15, rel)
            self.assertGreaterEqual(m["keyboard"], 1, rel)


if __name__ == "__main__":
    main()
