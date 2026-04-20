"""
C15 Cut-over Phase 2 (T6) — adapters + cutover_run 회귀 테스트.

검증 범위
---------
- scripts/adapters/__init__.py + base.py + mysql.py + sqlserver.py
- scripts/cutover_validator.py (CLI: --dryrun, --legacy/--modern → live mode wiring)
- scripts/cutover_run.py (P1~P6 + GATE + 리포트 JSON + confirm 게이트)
- migration/contracts/cutover.yaml (phase2_runtime 섹션 — runner/adapter 등록)
- dashboard/data/porting-screens.json (C15.tasks.T6 = completed)
- legacy-analysis/decisions.md (DEC-CUT-4 — 실 DB 어댑터 정책 등록)

설계 정합 (사용자 룰)
---------------------
- C15 Phase 1 패턴 — InMemoryDataSource dry-run 만 단위 테스트.
- 외부 SaaS / DB 드라이버 import 0건 정적 가드 (DEC-044).
- adapters/* 모듈은 ``import`` 만으로 pymysql/pyodbc 미설치 환경에서도 동작 (lazy).
- 비즈니스 SQL 신규 0건 — adapters 도 시스템 쿼리만 (COUNT/INFORMATION_SCHEMA).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS_DIR = ROOT / "scripts" / "adapters"
CUTOVER_RUN = ROOT / "scripts" / "cutover_run.py"
CUTOVER_VAL = ROOT / "scripts" / "cutover_validator.py"
CONTRACT = ROOT / "migration" / "contracts" / "cutover.yaml"
DASHBOARD = ROOT / "dashboard" / "data" / "porting-screens.json"
DECISIONS = ROOT / "legacy-analysis" / "decisions.md"

sys.path.insert(0, str(ROOT))


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# S — 정적 인프라 회귀
# ============================================================================
class StaticAdaptersC15(TestCase):

    def test_S_01_adapters_module_present(self):
        for p in (
            ADAPTERS_DIR / "__init__.py",
            ADAPTERS_DIR / "base.py",
            ADAPTERS_DIR / "mysql.py",
            ADAPTERS_DIR / "sqlserver.py",
        ):
            self.assertTrue(p.exists(), f"missing adapter file: {p}")

    def test_S_02_adapters_import_safe_without_drivers(self):
        """pymysql/pyodbc 미설치 환경에서도 import 만으로는 실패하지 않아야 한다."""
        from scripts.adapters import (  # noqa: F401
            MysqlDataSource,
            SqlServerDataSource,
            resolve_profile,
            sanitize_identifier,
        )

    def test_S_03_identifier_sanitizer_blocks_injection(self):
        from scripts.adapters import sanitize_identifier
        self.assertEqual(sanitize_identifier("Id_Logn"), "Id_Logn")
        for bad in (
            "Id; DROP TABLE x",
            "1Id_Logn",      # leading digit
            "Id Logn",       # space
            "`evil`",
            "Id'Logn",
            "Id\nLogn",
            "",
            None,            # type: ignore[arg-type]
        ):
            with self.assertRaises(ValueError):
                sanitize_identifier(bad)  # type: ignore[arg-type]

    def test_S_04_no_business_sql_in_adapters(self):
        """adapters/* 는 INSERT/UPDATE/DELETE/CREATE/DROP 0건 + INFORMATION_SCHEMA 만 사용."""
        for fname in ("base.py", "mysql.py", "sqlserver.py", "__init__.py"):
            src = _read(ADAPTERS_DIR / fname)

            def strip(s: str) -> str:
                no_c = "\n".join(ln for ln in s.splitlines() if not ln.lstrip().startswith("#"))
                no_d = re.sub(r'"""[\s\S]*?"""', "", no_c)
                return re.sub(r"'''[\s\S]*?'''", "", no_d)

            stripped = strip(src)
            for pat in (
                r"\bINSERT\s+INTO\b",
                r"\bUPDATE\s+\w+\s+SET\b",
                r"\bDELETE\s+FROM\b",
                r"\bCREATE\s+TABLE\b",
                r"\bDROP\s+TABLE\b",
                r"\bTRUNCATE\b",
                r"\bALTER\s+TABLE\b",
            ):
                m = re.search(pat, stripped, re.IGNORECASE)
                self.assertIsNone(
                    m,
                    f"adapters/{fname} uses forbidden DML/DDL '{pat}': {m.group(0) if m else ''}",
                )

    def test_S_05_no_external_saas_in_adapters_or_runner(self):
        """boto3/azure/sentry/datadog 등 외부 SaaS SDK 0건 (DEC-044)."""
        sources = [_read(ADAPTERS_DIR / f) for f in ("base.py", "mysql.py", "sqlserver.py")]
        sources.append(_read(CUTOVER_RUN))
        for src in sources:
            for pat in (
                r"^import\s+boto3", r"^from\s+boto3",
                r"^import\s+azure", r"^from\s+azure",
                r"^import\s+sentry_sdk", r"^from\s+sentry_sdk",
                r"^import\s+datadog", r"^from\s+datadog",
                r"^import\s+requests", r"^from\s+requests",
            ):
                self.assertIsNone(
                    re.search(pat, src, re.MULTILINE),
                    f"forbidden external SaaS/network SDK '{pat}' present",
                )

    def test_S_06_validator_cli_lives_with_live_mode(self):
        """cutover_validator CLI 가 --profiles/--tables 와 _build_live_source 를 노출."""
        src = _read(CUTOVER_VAL)
        for token in (
            "--profiles",
            "--tables",
            "_build_live_source",
            "scripts.adapters",
            "MysqlDataSource",
            "SqlServerDataSource",
        ):
            self.assertIn(token, src, f"cutover_validator missing live-mode wiring: {token}")

    def test_S_07_runner_module_present_with_phases(self):
        src = _read(CUTOVER_RUN)
        for token in (
            "find_blocking_open_questions",
            '"P1"', '"P2"', '"P3"', '"P4"', '"P5"', '"P6"',
            "rollback_started_at",
            "rollback_elapsed_sec",
            "--confirm",
            "--ignore-oq-block",
            "--dryrun",
            "schema_version",
        ):
            self.assertIn(token, src, f"cutover_run missing token: {token}")


# ============================================================================
# R — Runtime (CLI dry-run + 분기)
# ============================================================================
class RuntimeRunnerC15(TestCase):

    def test_R_01_dryrun_smoke(self):
        """--dryrun 가 rc=0 + P1~P6 모두 PASS 리포트 생성."""
        out = ROOT / "test" / "_artifacts_c15_phase2_dry.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.unlink()
        rc = subprocess.run(
            [sys.executable, str(CUTOVER_RUN), "--dryrun", "--out", str(out)],
            cwd=ROOT,
            check=False,
        ).returncode
        self.assertEqual(rc, 0, "dryrun must succeed")
        self.assertTrue(out.exists())
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["mode"], "dryrun")
        self.assertTrue(data["success"], f"dryrun success expected, got {data}")
        ids = [s["id"] for s in data["steps"]]
        for stage in ("GATE", "P1", "P2", "P3", "P4", "P5", "P6"):
            self.assertIn(stage, ids, f"missing stage {stage}: {ids}")
        # validator 결과 동봉
        self.assertIsNotNone(data.get("validator"))
        self.assertEqual(data["validator"]["failed"], 0)

    def test_R_02_oq_block_in_live_mode(self):
        """live mode (--legacy/--modern 만) 는 OQ 차단으로 rc=3."""
        out = ROOT / "test" / "_artifacts_c15_phase2_live_block.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.unlink()
        rc = subprocess.run(
            [
                sys.executable, str(CUTOVER_RUN),
                "--legacy", "138_legacy", "--modern", "138_modern",
                "--out", str(out),
            ],
            cwd=ROOT,
            check=False,
        ).returncode
        self.assertEqual(rc, 3, "live mode must block on unresolved OQ")
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertFalse(data["success"])
        self.assertGreaterEqual(len(data["blocked_by"]), 3)
        for oq in ("OQ-IN-1", "OQ-DBL-001", "OQ-DBL-003"):
            self.assertIn(oq, data["blocked_by"], f"missing block: {oq}")

    def test_R_03_find_blocking_oq_function(self):
        """파서가 open_questions_handling 의 cutover_block:true 만 정확히 식별."""
        from scripts.cutover_run import find_blocking_open_questions
        blocks = find_blocking_open_questions()
        self.assertEqual(
            sorted(blocks),
            sorted({"OQ-IN-1", "OQ-DBL-001", "OQ-DBL-003"}),
            f"blocking OQ mismatch: {blocks}",
        )

    def test_R_04_validator_dryrun_via_cli(self):
        """cutover_validator --dryrun 도 여전히 정상 동작 (Phase 1 호환)."""
        rc = subprocess.run(
            [sys.executable, str(CUTOVER_VAL), "--dryrun", "--report", "json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(rc.returncode, 0, rc.stderr)
        body = json.loads(rc.stdout)
        self.assertEqual(body["failed"], 0)
        self.assertGreaterEqual(body["total"], 15)


# ============================================================================
# G — 거버넌스/계약 동기화
# ============================================================================
class GovernanceSyncC15(TestCase):

    def test_G_01_contract_phase2_runtime_section(self):
        c = _read(CONTRACT)
        for token in (
            "phase2_runtime:",
            "scripts/cutover_run.py",
            "scripts/adapters",
            "MysqlDataSource",
            "SqlServerDataSource",
            "--confirm",
            "--ignore-oq-block",
            "DEC-CUT-4",
        ):
            self.assertIn(token, c, f"cutover.yaml missing phase2 token: {token}")

    def test_G_02_dashboard_t6_completed(self):
        with DASHBOARD.open(encoding="utf-8") as fh:
            data = json.load(fh)
        screens = data.get("screens") or data.get("scenarios") or []
        if isinstance(screens, dict):
            screens = list(screens.values())
        c15 = next(
            (s for s in screens if "C15" in (s.get("id", "") + s.get("title", ""))),
            None,
        )
        self.assertIsNotNone(c15, "C15 entry missing in porting-screens.json")
        t6 = ((c15.get("tasks") or {}).get("T6") or {})
        self.assertEqual(
            t6.get("status"), "completed",
            f"C15.tasks.T6 must be completed (got {t6})",
        )

    def test_G_03_decisions_dec_cut_4_registered(self):
        c = _read(DECISIONS)
        self.assertIn("DEC-CUT-4", c, "DEC-CUT-4 missing in decisions.md")
        # 본 결정의 내용 키워드 (어댑터/시스템 쿼리 only) 도 등재
        idx = c.find("DEC-CUT-4")
        snippet = c[idx : idx + 800]
        for token in ("MysqlDataSource", "SqlServerDataSource", "시스템/구조 쿼리"):
            self.assertIn(token, snippet, f"DEC-CUT-4 detail missing: {token}")


if __name__ == "__main__":
    main(verbosity=2)
