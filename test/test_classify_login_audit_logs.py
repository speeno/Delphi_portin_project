"""감사 로그 분류기 회귀 가드 (DSN-DEC-12 phase1).

[tools/classify_login_audit_logs.py] 의 카테고라이즈 로직을 단위로 검증.
실제 운영 로그가 없어도 본 가드가 사고 패턴 분류 정확도를 보장한다.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "classify_login_audit_logs.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "classify_login_audit_logs", TOOL_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("classify_login_audit_logs", mod)
    spec.loader.exec_module(mod)
    return mod


class ClassifyLoginAuditLogsTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def _classify(self, rec) -> str:
        return self.tool._classify_record(rec)

    def test_ownership_violation_wins(self):
        rec = {
            "result": "success",
            "ownership_violation": True,
            "ambiguous_narrowed": True,  # 다른 신호와 동시 발생해도 E 가 우선
            "lazy_refreshed": True,
        }
        self.assertEqual(self._classify(rec), "E_OWNERSHIP_VIOLATION")

    def test_token_build_failed_classifies_as_F(self):
        self.assertEqual(
            self._classify({"result": "failure", "reason": "token_build_failed"}),
            "F_TOKEN_BUILD_FAILED",
        )

    def test_seed_mismatch_classifies_as_A(self):
        self.assertEqual(
            self._classify({"result": "success", "seed_mismatch": True}),
            "A_SEED_MISMATCH",
        )

    def test_strict_ambiguous_failure_classifies_as_H(self):
        self.assertEqual(
            self._classify(
                {"result": "failure", "ambiguous_strict": True, "reason": "ambiguous_route"}
            ),
            "H_AMBIGUOUS_STRICT",
        )

    def test_lazy_refresh_success_classifies_as_B(self):
        self.assertEqual(
            self._classify({"result": "success", "lazy_refreshed": True}),
            "B_INDEX_STALE",
        )

    def test_directory_sweep_success_classifies_as_D(self):
        self.assertEqual(
            self._classify({"result": "success", "directory_sweep": True}),
            "D_DIRECTORY_SWEEP_HIT",
        )

    def test_ambiguous_narrowed_with_attempts_classifies_as_C(self):
        self.assertEqual(
            self._classify(
                {"result": "success", "ambiguous_narrowed": True, "candidate_attempts": 3}
            ),
            "C_AMBIGUOUS_NARROWING",
        )

    def test_invalid_credentials_classifies_as_G(self):
        self.assertEqual(
            self._classify(
                {"result": "failure", "reason": "invalid_credentials_after_probe"}
            ),
            "G_INVALID_CREDENTIALS",
        )

    def test_classify_iterable_aggregates_counts(self):
        lines = [
            'auth.login {"result":"success","ownership_violation":true}',
            'auth.login {"result":"success","lazy_refreshed":true}',
            'auth.login {"result":"failure","reason":"invalid_credentials"}',
            "garbage line ignored",
            'auth.login {"result":"success","directory_sweep":true}',
        ]
        result = self.tool.classify(iter(lines))
        self.assertEqual(result.counts["E_OWNERSHIP_VIOLATION"], 1)
        self.assertEqual(result.counts["B_INDEX_STALE"], 1)
        self.assertEqual(result.counts["G_INVALID_CREDENTIALS"], 1)
        self.assertEqual(result.counts["D_DIRECTORY_SWEEP_HIT"], 1)
        self.assertEqual(result.parse_failures, 1)


if __name__ == "__main__":
    main()
