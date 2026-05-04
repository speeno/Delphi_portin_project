"""debug/generate_incomplete_features_inventory.py 산출물 회귀 가드.

- 스크립트 존재·실행 OK
- 산출 JSON 의 sources 키·필드 안정 (스키마)
- ScreenPlaceholder 페이지 ≥ 4
- form-registry preview/STUB 매트릭스 3건 (Menu* placeholder)
- form-registry phase1+R/RU/STUB 의 분류 카운트 ≥ 1 (현 시점 상당수)
- backend_stub_grep 에 _stub.py 라인이 포함됨
- --check 모드: 방금 생성한 직후라 exit 0
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "debug" / "generate_incomplete_features_inventory.py"
JSON_PATH = ROOT / "analysis" / "audit" / "incomplete-features-inventory.json"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class IncompleteFeaturesInventoryTests(TestCase):
    def setUp(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        proc = _run([])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    def test_top_level_schema(self) -> None:
        self.assertIn("criteria", self.data)
        src = self.data["sources"]
        for key in (
            "ui_placeholder_pages",
            "phase2_screen_cards_tasks",
            "form_registry_preview_or_stub",
            "form_registry_phase1_partial",
            "backend_stub_grep",
            "crud_backlog_section_2_6",
        ):
            self.assertIn(key, src, msg=f"missing source key: {key}")

    def test_ui_placeholder_pages_has_known_routes(self) -> None:
        hints = {x["route_hint"] for x in self.data["sources"]["ui_placeholder_pages"]}
        for expected in (
            "/billing/statements",
            "/year-month-stats",
            "/shipping/returns-inventory",
        ):
            self.assertIn(expected, hints)

    def test_form_registry_placeholder_matrix_three(self) -> None:
        ids = sorted(
            x["id"] for x in self.data["sources"]["form_registry_preview_or_stub"]
        )
        self.assertEqual(
            ids,
            ["MenuBillingStatements", "MenuShippingReturnsInventory", "MenuYearMonthStats"],
        )
        # 캡션·crudNotes 도 함께 잡혔는지
        for entry in self.data["sources"]["form_registry_preview_or_stub"]:
            self.assertTrue(entry["caption"], msg=entry)
            self.assertTrue(entry["crudNotes"], msg=entry)

    def test_phase1_partial_groups_by_parity(self) -> None:
        partial = self.data["sources"]["form_registry_phase1_partial"]
        self.assertGreaterEqual(len(partial), 1)
        parities = {x["crudParity"] for x in partial}
        self.assertTrue(parities.issubset({"R", "RU", "STUB"}), parities)

    def test_backend_stub_grep_includes_stub_router(self) -> None:
        files = {x["file"] for x in self.data["sources"]["backend_stub_grep"]}
        self.assertIn(
            "도서물류관리프로그램/backend/app/routers/_stub.py", files
        )

    def test_check_mode_passes_after_regen(self) -> None:
        # 방금 main 으로 갱신했으므로 --check 통과
        proc = _run(["--check"])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)


if __name__ == "__main__":
    main()
