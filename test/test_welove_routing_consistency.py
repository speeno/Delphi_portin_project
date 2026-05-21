"""WeLove 라우팅 매트릭스 ↔ 시드 정합 감사 도구 회귀 가드 (DSN-DEC-12).

본 테스트는 ``tools/audit_welove_routing_consistency.py`` 의 분류 로직을 픽스처
기반으로 검증한다. 실제 시드(``backend/data/tenants_directory_seed.json``) 의
충돌 카운트는 운영 환경에 따라 달라지므로 수치 강제는 하지 않는다 — 본 사이클은
"공유 DB 케이스가 분류로 잡힌다" 만 확정한다.

운영 정착 후 ``tools/audit_welove_routing_consistency.py --strict`` 로 PR 단계
회귀 가드(SHARED_DB_NO_HCODE_GUARD = 0) 를 추가할 예정 (DSN-DEC-12 phase2).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "audit_welove_routing_consistency.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "audit_welove_routing_consistency", TOOL_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("audit_welove_routing_consistency", mod)
    spec.loader.exec_module(mod)
    return mod


class WeLoveRoutingConsistencyTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_shared_db_without_isolation_key_is_flagged(self):
        """공유 DB 인데 hcode_pattern/parent_tenant_id 부재 → SHARED_DB_NO_HCODE_GUARD."""
        matrix = {
            "routes": [
                {
                    "server_id": "remote_153",
                    "tenant_name_kor": "위러브3",
                    "account_family": "chul_09",
                    "db_name_logical": "chul_09_db",
                },
                {
                    "server_id": "remote_153",
                    "tenant_name_kor": "교문사",
                    "account_family": "chul_09",
                    "db_name_logical": "chul_09_db",
                },
            ]
        }
        seed = {
            "tenants": [
                {
                    "tenant_id": "T1",
                    "tenant_label_kor": "위러브3",
                    "account_family": "chul_09",
                    "primary_server": "remote_153",
                    "db_name_logical": "chul_09_db",
                    "default_account_type": "T3",
                    "is_active": True,
                },
                {
                    "tenant_id": "T2",
                    "tenant_label_kor": "교문사",
                    "account_family": "chul_09",
                    "primary_server": "remote_153",
                    "db_name_logical": "chul_09_db",
                    "default_account_type": "T3",
                    "is_active": True,
                },
            ]
        }
        report = self.tool.audit(matrix, seed)
        codes = {f.code for f in report.findings}
        self.assertIn("SHARED_DB_NO_HCODE_GUARD", codes)

    def test_shared_db_with_hcode_pattern_is_not_flagged(self):
        """격리 키(hcode_pattern) 가 있으면 SHARED_DB_NO_HCODE_GUARD 미발생."""
        matrix = {
            "routes": [
                {
                    "server_id": "remote_153",
                    "tenant_name_kor": "위러브3",
                    "account_family": "chul_09",
                    "db_name_logical": "chul_09_db",
                },
                {
                    "server_id": "remote_153",
                    "tenant_name_kor": "교문사",
                    "account_family": "chul_09",
                    "db_name_logical": "chul_09_db",
                },
            ]
        }
        seed = {
            "tenants": [
                {
                    "tenant_id": "T1",
                    "tenant_label_kor": "위러브3",
                    "account_family": "chul_09",
                    "primary_server": "remote_153",
                    "db_name_logical": "chul_09_db",
                    "default_account_type": "T3",
                    "hcode_pattern": r"^9\d+$",
                    "is_active": True,
                },
                {
                    "tenant_id": "T2",
                    "tenant_label_kor": "교문사",
                    "account_family": "chul_09",
                    "primary_server": "remote_153",
                    "db_name_logical": "chul_09_db",
                    "default_account_type": "T3",
                    "hcode_pattern": r"^[A-Za-z].*$",
                    "is_active": True,
                },
            ]
        }
        report = self.tool.audit(matrix, seed)
        codes = {f.code for f in report.findings}
        self.assertNotIn("SHARED_DB_NO_HCODE_GUARD", codes)

    def test_primary_server_mismatch_is_flagged(self):
        matrix = {
            "routes": [
                {
                    "server_id": "remote_154",
                    "tenant_name_kor": "북앤북",
                    "account_family": "book_07",
                    "db_name_logical": "book_07_db",
                }
            ]
        }
        seed = {
            "tenants": [
                {
                    "tenant_id": "T1",
                    "tenant_label_kor": "북앤북",
                    "account_family": "book_07",
                    "primary_server": "remote_999",  # 의도적 mismatch
                    "db_name_logical": "book_07_db",
                    "default_account_type": "T3",
                    "is_active": True,
                }
            ]
        }
        report = self.tool.audit(matrix, seed)
        codes = {f.code for f in report.findings}
        self.assertIn("PRIMARY_SERVER_MISMATCH", codes)

    def test_seed_only_label_is_flagged_as_seed_not_in_matrix(self):
        matrix = {"routes": []}
        seed = {
            "tenants": [
                {
                    "tenant_id": "T1",
                    "tenant_label_kor": "신규운영_2026",
                    "account_family": "new_xyz",
                    "primary_server": "remote_153",
                    "db_name_logical": "new_xyz_db",
                    "default_account_type": "T3",
                    "is_active": True,
                }
            ]
        }
        report = self.tool.audit(matrix, seed)
        codes = {f.code for f in report.findings}
        self.assertIn("SEED_NOT_IN_MATRIX", codes)

    def test_real_seed_runs_without_exception(self):
        """실제 시드/매트릭스에 대해서도 도구가 예외 없이 분류 결과를 만든다."""
        report = self.tool.audit(
            self.tool._load_json(self.tool._DEFAULT_MATRIX_PATH),
            self.tool._load_json(self.tool._DEFAULT_SEED_PATH),
        )
        self.assertGreater(report.matrix_count, 0)
        self.assertGreater(report.seed_count, 0)
        # 본 사이클은 SHARED_DB_NO_HCODE_GUARD 가 0이 아닐 수 있음. 도구가 동작만 확인.
        codes = {f.code for f in report.findings}
        self.assertTrue(
            codes.issubset(
                {
                    "SHARED_DB_NO_HCODE_GUARD",
                    "MATRIX_NOT_IN_SEED",
                    "SEED_NOT_IN_MATRIX",
                    "PRIMARY_SERVER_MISMATCH",
                    "DB_NAME_LOGICAL_MISMATCH",
                    "DB_NAME_LOGICAL_MISSING",
                }
            )
        )


if __name__ == "__main__":
    main()
