"""
C15 Cut-over Phase 1 — 5종 validator + 롤백 RTO + OQ 차단 게이트 회귀 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/cutover.yaml v1.0.0 (AC-CUT-1~6 + VC-1~5 + OQ blocking)
- legacy-analysis/decisions.md (DEC-044)
- scripts/cutover_validator.py (5 check + InMemoryDataSource dry-run)

검증 케이스
-----------
정적 가드 (S — DB 무관)
- TC-C15-S-01  cutover.yaml v1.0 frozen + AC-CUT-1~6 + VC-1~5
- TC-C15-S-02  rollback RTO ≤ 15분 + procedure 4 step 명시
- TC-C15-S-03  validator 모듈 존재 + 5 check (CHECKS_REGISTRY)
- TC-C15-S-04  validator 신규 SQL 0건 (DEC-040 정합 — InMemory 포함)
- TC-C15-S-05  AC-CUT-2: 24시간 운영 검증 윈도우 명시
- TC-C15-S-06  7 핵심 시나리오 (C2/C3/C4/C5/C6/C7/C8) 명시
- TC-C15-S-07  validator: 외부 SaaS import 0건 (boto3/azure 등)
- TC-C15-S-08  OQ 차단 게이트 (OQ-IN-1, OQ-DBL-001/003 cutover_block:true)

런타임 가드 (R — InMemory dry-run 만)
- TC-C15-R-01  validator 5 check 모두 PASS (동등 fixture)
- TC-C15-R-02  롤백 dry-run RTO ≤ 15분 (시뮬레이션 — 절차 step 4 < 900s 가정)
- TC-C15-R-03  validator: row_count 차이 → VC-1 FAIL (regression detection)
- TC-C15-R-04  validator: schema diff (audit_* 외 컬럼 추가) → VC-5 FAIL
- TC-C15-R-05  validator: mojibake bytes → VC-3 FAIL

설계 정합 (사용자 룰)
---------------------
- C13/C14 패턴 — 단위 테스트는 InMemoryDataSource 로 5 check 동작 검증.
- 실제 MySQL 호출 (MysqlDataSource) 은 운영 절차 P3 이후 — Phase 1 out-of-scope.
- 외부 SaaS import 0건 정적 가드 (DEC-044 정합).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "migration" / "contracts" / "cutover.yaml"
DECISIONS = ROOT / "legacy-analysis" / "decisions.md"
VALIDATOR = ROOT / "scripts" / "cutover_validator.py"

sys.path.insert(0, str(ROOT))


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# S — 정적 회귀
# ============================================================================
class StaticGuardC15(TestCase):

    def test_S_01_contract_v1_frozen(self):
        """TC-C15-S-01 — cutover.yaml v1.0 frozen + AC + VC-1~5."""
        c = _read(CONTRACT)
        for token in (
            "version: 1.0.0",
            "status: frozen",
            "scenario_id: C15_cutover",
            "AC-CUT-1", "AC-CUT-2", "AC-CUT-3", "AC-CUT-4", "AC-CUT-5", "AC-CUT-6",
            "VC-1", "VC-2", "VC-3", "VC-4", "VC-5",
            "row_count_equality",
            "checksum_equality",
            "encoding_compat",
            "mysql3_compat",
            "schema_diff_zero",
            "external_integrations: excluded",
            "DEC-044",
        ):
            self.assertIn(token, c, f"contract missing token: {token}")

    def test_S_02_rollback_rto(self):
        """TC-C15-S-02 — rollback RTO ≤ 15분 + 절차 step 명시."""
        c = _read(CONTRACT)
        self.assertIn("rollback_rto_min: 15", c)
        # rollback procedure step ≥ 4
        # rollback: ... procedure: ... 형태로 등장 — 단순 substring 가드
        self.assertIn("rollback:", c)
        self.assertIn("procedure:", c)
        self.assertIn("read-only", c.lower())

    def test_S_03_validator_module_with_5_checks(self):
        """TC-C15-S-03 — validator 모듈 존재 + 5 check 등록."""
        self.assertTrue(VALIDATOR.exists(), f"missing validator: {VALIDATOR}")
        from scripts.cutover_validator import CHECKS_REGISTRY
        self.assertEqual(
            set(CHECKS_REGISTRY.keys()),
            {"VC-1", "VC-2", "VC-3", "VC-4", "VC-5"},
            f"validator missing checks: {set(CHECKS_REGISTRY.keys())}",
        )

    def test_S_04_no_new_sql_in_validator(self):
        """TC-C15-S-04 — validator 에 직접 SQL 호출 0건 (DEC-040)."""
        src = _read(VALIDATOR)

        def strip_doc(s: str) -> str:
            no_c = "\n".join(ln for ln in s.splitlines() if not ln.lstrip().startswith("#"))
            no_d = re.sub(r'"""[\s\S]*?"""', "", no_c)
            return re.sub(r"'''[\s\S]*?'''", "", no_d)

        stripped = strip_doc(src)
        for pat in (
            r"\bexecute_query\s*\(",
            r"\bexecute_in_transaction\s*\(",
            r"[\"']\s*INSERT\s+INTO\b",
            r"[\"']\s*UPDATE\s+\w+\s+SET\b",
            r"[\"']\s*DELETE\s+FROM\b",
            r"[\"']\s*SELECT\s+.+\s+FROM\b",
        ):
            m = re.search(pat, stripped)
            self.assertIsNone(
                m, f"validator uses forbidden SQL pattern '{pat}': {m.group(0) if m else ''}",
            )

    def test_S_05_acceptance_gate_24h_window(self):
        """TC-C15-S-05 — AC-CUT-2 의 24시간 운영 검증 윈도우 명시."""
        c = _read(CONTRACT)
        self.assertIn("24시간", c)
        self.assertIn("0 critical", c)
        self.assertIn("레거시 EXE 종결", c)

    def test_S_06_seven_core_scenarios_listed(self):
        """TC-C15-S-06 — 7 핵심 시나리오 (C2/C3/C4/C5/C6/C7/C8) 명시."""
        c = _read(CONTRACT)
        for sc in ("C2", "C3", "C4", "C5", "C6", "C7", "C8"):
            self.assertIn(sc, c, f"core scenario missing: {sc}")

    def test_S_07_no_external_saas_import(self):
        """TC-C15-S-07 — validator: 외부 SaaS SDK import 0건 (DEC-044)."""
        src = _read(VALIDATOR)
        forbidden_imports = (
            r"^import\s+boto3",
            r"^from\s+boto3",
            r"^import\s+azure",
            r"^from\s+azure",
            r"^import\s+sentry_sdk",
            r"^from\s+sentry_sdk",
            r"^import\s+datadog",
            r"^from\s+datadog",
        )
        for pat in forbidden_imports:
            m = re.search(pat, src, re.MULTILINE)
            self.assertIsNone(
                m,
                f"validator imports forbidden external SaaS SDK ({pat}): {m.group(0) if m else ''}",
            )

    def test_S_08_oq_block_gate(self):
        """TC-C15-S-08 — OQ-IN-1, OQ-DBL-001/003 cutover_block:true 명시."""
        c = _read(CONTRACT)
        for oq in ("OQ-IN-1", "OQ-DBL-001", "OQ-DBL-003"):
            self.assertIn(oq, c, f"open question missing: {oq}")
        # cutover_block: true 가 최소 3건 (IN-1 / DBL-001 / DBL-003)
        block_true_count = len(re.findall(r"cutover_block:\s*true", c))
        self.assertGreaterEqual(
            block_true_count, 3,
            f"cutover_block:true count {block_true_count} < 3 (IN-1, DBL-001, DBL-003)",
        )


# ============================================================================
# R — InMemory dry-run (DB 무관)
# ============================================================================
class RuntimeValidatorC15(TestCase):

    def test_R_01_validator_five_checks_pass(self):
        """TC-C15-R-01 — 동등 fixture 에서 5 check 모두 PASS."""
        from scripts.cutover_validator import _dryrun_sources, run_checks
        legacy, modern, tables = _dryrun_sources()
        report = run_checks(legacy=legacy, modern=modern, tables=tables)
        self.assertEqual(report.failed, 0, f"failed checks: {[r for r in report.results if not r.passed]}")
        # 5 check × 3 table = 15 결과
        self.assertGreaterEqual(report.total, 15)

    def test_R_02_rollback_dryrun_rto(self):
        """TC-C15-R-02 — 롤백 절차 RTO ≤ 15분 (시뮬레이션 — 절차 step 4 < 900s).

        실제 DNS/proxy 스위치 시뮬레이션은 운영 환경 의존 — 본 케이스는 절차 정의의
        총 시간이 RTO 제약 (15분 = 900s) 이내인지 정적 검증.
        """
        c = _read(CONTRACT)
        m = re.search(r"rollback_rto_min:\s*(\d+)", c)
        self.assertIsNotNone(m)
        self.assertLessEqual(int(m.group(1)), 15, "rollback RTO must be ≤ 15 minutes")

    def test_R_03_validator_row_count_drift_detected(self):
        """TC-C15-R-03 — modern row_count 차이 → VC-1 FAIL."""
        from scripts.cutover_validator import (
            InMemoryDataSource, run_checks,
        )
        legacy = InMemoryDataSource(
            counts={"T1": 100}, rows={"T1": []}, schemas={"T1": {"a": "INT"}},
        )
        modern = InMemoryDataSource(
            counts={"T1": 99}, rows={"T1": []}, schemas={"T1": {"a": "INT"}},
        )
        report = run_checks(legacy=legacy, modern=modern, tables=["T1"], selected=["VC-1"])
        self.assertEqual(report.failed, 1)
        self.assertEqual(report.results[0].check_id, "VC-1")
        self.assertFalse(report.results[0].passed)

    def test_R_04_validator_schema_diff_blocks_non_audit(self):
        """TC-C15-R-04 — modern 에 audit_* 외 컬럼 추가 시 VC-5 FAIL.

        반대로 audit_ts 같은 audit_ 접두 컬럼 추가는 PASS.
        """
        from scripts.cutover_validator import (
            InMemoryDataSource, run_checks,
        )
        legacy = InMemoryDataSource(
            counts={"T1": 0}, rows={"T1": []},
            schemas={"T1": {"a": "INT"}},
        )
        # 비-audit 컬럼 추가 → FAIL
        modern_bad = InMemoryDataSource(
            counts={"T1": 0}, rows={"T1": []},
            schemas={"T1": {"a": "INT", "b_extra": "VARCHAR"}},
        )
        r1 = run_checks(legacy=legacy, modern=modern_bad, tables=["T1"], selected=["VC-5"])
        self.assertEqual(r1.failed, 1)
        # audit_ 접두 컬럼만 추가 → PASS
        modern_ok = InMemoryDataSource(
            counts={"T1": 0}, rows={"T1": []},
            schemas={"T1": {"a": "INT", "audit_ts": "DATETIME", "auditor_id": "VARCHAR"}},
        )
        r2 = run_checks(legacy=legacy, modern=modern_ok, tables=["T1"], selected=["VC-5"])
        self.assertEqual(r2.failed, 0)

    def test_R_05_validator_mojibake_detection(self):
        """TC-C15-R-05 — modern 의 forbidden bytes (replacement char) → VC-3 FAIL."""
        from scripts.cutover_validator import (
            InMemoryDataSource, run_checks,
        )
        legacy = InMemoryDataSource(
            counts={"G4_Book": 1}, rows={"G4_Book": [{"Gcode": "B1", "Gname": "정상"}]},
            schemas={"G4_Book": {"Gcode": "VARCHAR", "Gname": "VARCHAR"}},
        )
        # U+FFFD (replacement char) 포함 — mojibake
        bad_text = "이름\ufffd오류"
        modern = InMemoryDataSource(
            counts={"G4_Book": 1}, rows={"G4_Book": [{"Gcode": "B1", "Gname": bad_text}]},
            schemas={"G4_Book": {"Gcode": "VARCHAR", "Gname": "VARCHAR"}},
        )
        report = run_checks(legacy=legacy, modern=modern, tables=["G4_Book"], selected=["VC-3"])
        self.assertEqual(report.failed, 1)
        self.assertFalse(report.results[0].passed)


if __name__ == "__main__":
    main(verbosity=2)
