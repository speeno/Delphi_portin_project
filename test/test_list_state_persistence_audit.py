"""DEC-055 — list 화면 상태 보존 회귀 가드.

대상 스크립트
-------------
- ``tools/audit_list_state_persistence.py`` —
  ``frontend/src/app/(app)/**/page.tsx`` 중 ``DataGridPager`` 를 import 하는
  모든 list 화면이 ``useListSession`` (``@/lib/use-list-session``) 을 함께
  import 하는지 정적 grep 으로 검증.

검증 3축 (plan §3.4)
--------------------
1. ``violations`` 0          — DataGridPager 사용 화면 중 hook 미도입 0
   (allowlist 외).
2. 17쪽 baseline 커버리지     — plan §1 의 list 화면 17건이 모두 covered.
3. CLI ``--check`` exit 0    — baseline 상태에서 회귀 없음.

격리
-----
- 실파일(``frontend/src/app/(app)/**/page.tsx`` /
  ``legacy-analysis/list-state-allowlist.yaml``) 그대로 읽음. DB·네트워크 0.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import TestCase

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from audit_list_state_persistence import (  # noqa: E402  (sys.path 보강 후 import)
    discover_pages,
    find_covered,
    run_audit,
)

# plan §1 ‑ 17 list 화면 baseline (route_key 기준).
EXPECTED_COVERED_KEYS = {
    # master 5 (구 6 — master_data.yaml v1.2.0 정정으로 logistics-cost 제외)
    "master.customer",
    "master.book",
    "master.publisher",
    "master.book-code",
    "master.discount",
    # C2/C3/C4/C6 — 5
    "outbound.orders",
    "outbound.status",
    "inbound.receipts",
    "returns.receipts",
    "transactions.sales-statement",
    # inquiry 6
    "inventory.status",
    "ledger.book",
    "ledger.book-integrated",
    "reports.book-sales",
    "reports.customer-sales",
    "reports.year-end-book",
}


class ListStatePersistenceAuditTests(TestCase):
    """plan §3.4 — 3 핵심 가드 + 보조 정합성 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run_audit()

    # ── 핵심 3축 (plan §3.4) ─────────────────────────────────────

    def test_no_violations_outside_allowlist(self) -> None:
        v = self.report["violations"]
        self.assertEqual(
            [],
            v,
            f"useListSession 미도입 list 화면 발견 — hook 도입 또는 "
            f"list-state-allowlist.yaml 에 reason+until 등록 필요: "
            f"{[e['route_key'] for e in v]}",
        )

    def test_baseline_17_pages_covered(self) -> None:
        covered_keys = {e["route_key"] for e in self.report["covered"]}
        missing = EXPECTED_COVERED_KEYS - covered_keys
        self.assertEqual(
            set(),
            missing,
            f"baseline 17 화면 중 covered 누락 — useListSession 회귀 의심: {sorted(missing)}",
        )
        self.assertGreaterEqual(
            self.report["summary"]["covered"],
            len(EXPECTED_COVERED_KEYS),
            "covered count regression",
        )

    def test_cli_check_exits_zero_when_baseline_clean(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOLS_DIR / "audit_list_state_persistence.py"),
                "--check",
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            0,
            proc.returncode,
            f"--check 가 baseline 상태에서 비-0 exit (stderr={proc.stderr!r})",
        )
        self.assertIn("[list-state-coverage]", proc.stdout)

    # ── 보조 (코어 helper · 정합성) ───────────────────────────────

    def test_summary_keys_present(self) -> None:
        s = self.report["summary"]
        for key in ("total_pages", "covered", "violations", "allowed", "skipped"):
            self.assertIn(key, s)

    def test_no_truly_stale_allowlist(self) -> None:
        stale = self.report.get("stale_allowlist", [])
        self.assertEqual(
            [],
            stale,
            f"allowlist 에 실제 위반 페이지가 없는 엔트리 — 정리 필요: {stale}",
        )

    def test_covered_entries_have_route_key_and_file(self) -> None:
        for row in self.report["covered"]:
            self.assertIn("route_key", row)
            self.assertIn("file", row)
            self.assertTrue(
                row["file"].endswith("page.tsx"),
                f"covered file 이 page.tsx 가 아님: {row}",
            )

    def test_specific_critical_pages_covered(self) -> None:
        # master/customer 와 reports/year-end-book 은 plan §4 수동 시나리오의
        # 대표 화면 — 회귀 시 즉시 실패하도록 단건 명시.
        for key in ("master.customer", "outbound.orders", "reports.year-end-book"):
            self.assertIsNotNone(
                find_covered(self.report, key),
                f"plan §4 대표 시나리오 화면 미커버: {key}",
            )

    # ── discovery 정합성 ─────────────────────────────────────────

    def test_discover_pages_finds_some_pagers(self) -> None:
        pages = discover_pages()
        pager_pages = [p for p in pages if p.has_pager]
        self.assertGreaterEqual(
            len(pager_pages),
            len(EXPECTED_COVERED_KEYS),
            "DataGridPager import 검출이 baseline(17)보다 적음 — discovery regex 회귀 의심.",
        )

    def test_report_file_round_trip(self) -> None:
        report_path = (
            REPO_ROOT / "analysis" / "audit" / "list-state-coverage-report.json"
        )
        self.assertTrue(
            report_path.exists(), "audit --check 후 report 파일 미생성."
        )
        loaded = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(self.report["summary"], loaded["summary"])
