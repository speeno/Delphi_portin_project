"""DEC-054 — 레거시 포팅 누락 회귀 가드.

대상 스크립트
-------------
- ``tools/audit_legacy_coverage.py`` — DFM root caption 인벤토리 ↔ 프런트
  ``form-registry.ts`` 비교 (4 카테고리 분류 + JSON report + ``--check`` CLI).

검증 3축 (plan §3.4)
--------------------
1. 신규 missing 0       — allowlist 외 신규 누락 0.
2. 신규 caption mismatch 0 — allowlist 외 신규 캡션 불일치 0.
3. Sobo67 스모크         — 가드 살아있음 보장 (DFM='도서별년말집계' vs
   registry='출고현황' 비교가 실제로 기록되어 있는가).

격리
-----
- 실파일(``analysis/form_inventory.json`` / ``form-registry.ts`` /
  ``coverage-allowlist.yaml``) 그대로 읽음. DB·네트워크 0.
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

from audit_legacy_coverage import (  # noqa: E402  (sys.path 보강 후 import)
    derive_base_form,
    find_caption_diff,
    find_entry,
    map_registry_to_dfm,
    normalize_caption,
    parse_form_registry,
    run_audit,
    unallowed_mismatches,
    unallowed_missing,
)


class LegacyCoverageAuditTests(TestCase):
    """plan §3.4 — 3 핵심 가드 + helper 단위 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run_audit()

    # ── 핵심 3축 (plan §3.4) ─────────────────────────────────────

    def test_no_new_missing_forms_outside_allowlist(self) -> None:
        residual = unallowed_missing(self.report)
        self.assertEqual(
            [],
            residual,
            f"신규 missing 발견 — allowlist 등록 또는 포팅 plan 수립 필요: "
            f"{[e['form_name'] for e in residual]}",
        )

    def test_no_caption_mismatches_outside_allowlist(self) -> None:
        residual = unallowed_mismatches(self.report)
        self.assertEqual(
            [],
            residual,
            f"신규 caption mismatch 발견: "
            f"{[(e['form_name'], e['dfm_caption'], e['registry_caption']) for e in residual]}",
        )

    def test_sobo67_caption_mismatch_smoke(self) -> None:
        sobo67 = find_caption_diff(self.report, "Sobo67_status")
        self.assertIsNotNone(
            sobo67,
            "가드 죽음 — Sobo67_status (출고현황) ↔ DFM Sobo67 (도서별년말집계) "
            "비교가 어떤 카테고리에도 surface 되지 않음.",
        )
        self.assertEqual("도서별년말집계", sobo67["dfm_caption"])
        self.assertEqual("출고현황", sobo67["registry_caption"])

    # ── 추가 보조 (코어 helper · 회귀 안전망) ─────────────────────

    def test_summary_keys_present(self) -> None:
        s = self.report["summary"]
        for key in (
            "total_dfm_candidates",
            "registry_entries",
            "ok",
            "missing_forms",
            "caption_mismatches",
            "allowed",
        ):
            self.assertIn(key, s)

    def test_no_truly_stale_allowlist(self) -> None:
        stale = self.report.get("stale_allowlist", [])
        self.assertEqual(
            [],
            stale,
            f"allowlist 에 DFM·registry 어디에도 없는 엔트리 — 정리 필요: {stale}",
        )

    def test_intentional_new_form_includes_sobo67_yearbook(self) -> None:
        intent = self.report.get("intentional_new_forms", [])
        self.assertIn(
            "Sobo67_yearbook",
            intent,
            "Sobo67_yearbook 의도 deferral 누락 — coverage-allowlist.yaml 확인.",
        )

    # ── helper 단위 ───────────────────────────────────────────────

    def test_derive_base_form_strips_alpha_suffix(self) -> None:
        self.assertEqual("Sobo67", derive_base_form("Sobo67_status"))
        self.assertEqual("Sobo67", derive_base_form("Sobo67_yearbook"))
        self.assertEqual("Sobo32_1", derive_base_form("Sobo32_1_ledger"))
        # suffix 가 영문이 아니면 그대로
        self.assertEqual("Sobo32_1", derive_base_form("Sobo32_1"))
        self.assertEqual("Sobo11", derive_base_form("Sobo11"))

    def test_normalize_caption_strips_whitespace(self) -> None:
        self.assertEqual(normalize_caption("도서 별 년말 집계"), "도서별년말집계")
        self.assertEqual(normalize_caption(" \t입고\n명세서 "), "입고명세서")

    def test_map_registry_to_dfm_prefers_legacy_form(self) -> None:
        from audit_legacy_coverage import RegistryEntry  # local import — readability

        regs = [
            RegistryEntry(id="Sobo67_status", caption="출고현황", legacy_form="Sobo67"),
            RegistryEntry(id="Sobo67_yearbook", caption="도서별년말집계"),
            RegistryEntry(id="OnlyNew", caption="신규 화면"),
        ]
        mapping = map_registry_to_dfm(regs, {"Sobo67"})
        self.assertEqual("Sobo67", mapping["Sobo67_status"])  # legacy_form 우선
        self.assertEqual("Sobo67", mapping["Sobo67_yearbook"])  # base prefix
        self.assertIsNone(mapping["OnlyNew"])  # DFM 미존재

    def test_registry_parser_picks_up_caption_field(self) -> None:
        entries = parse_form_registry()
        captions = {e.id: e.caption for e in entries}
        self.assertIn("Sobo67_status", captions)
        self.assertEqual("출고현황", captions["Sobo67_status"])
        self.assertIn("Sobo67_yearbook", captions)
        self.assertEqual("도서별년말집계", captions["Sobo67_yearbook"])

    def test_find_entry_returns_match_or_none(self) -> None:
        rows = [{"form_name": "A"}, {"form_name": "B"}]
        self.assertEqual({"form_name": "A"}, find_entry(rows, "A"))
        self.assertIsNone(find_entry(rows, "Z"))

    # ── CLI smoke (--check exit code) ────────────────────────────

    def test_cli_check_exits_zero_when_baseline_clean(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "audit_legacy_coverage.py"), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            0,
            proc.returncode,
            f"--check 가 baseline 상태에서 비-0 exit (stderr={proc.stderr!r})",
        )
        # 진행 한 줄 stdout 확인
        self.assertIn("[legacy-coverage]", proc.stdout)

    def test_report_file_round_trip(self) -> None:
        report_path = REPO_ROOT / "analysis" / "audit" / "legacy-coverage-report.json"
        self.assertTrue(
            report_path.exists(), "audit --check 후 report 파일 미생성."
        )
        loaded = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(self.report["summary"], loaded["summary"])
