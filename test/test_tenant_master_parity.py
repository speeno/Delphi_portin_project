"""테넌트 마스터 패리티 회귀 가드 (DSN-DEC-12 / ACC-DATA-03).

본 테스트는 "교문사 같은 공유 DB 계정이 다른 계정(위러브3)으로 잘못 매핑" 되는
회귀를, **계정 무관 공통 규칙** 차원에서 막는다.

핵심 루트 원인
--------------
login_id_index 는 공유 DB 좌표(예: chul_09_db)의 모든 로그인을 **단일 tenant_id 로 붕괴**
시킨다(교문사 로그인 → 위러브3 UUID). 이전에는 auth 가 그 index tenant_id 를
ownership 가드의 단일화 힌트로 사용해 hcode 격리보다 먼저 잘못된 테넌트를 확정했다.

검증 항목
---------
1. 매니페스트 정합 — 각 케이스가 welove_login_routing_expectations.json 과 1:1.
2. 교문사 baseline golden — books=3437, customers=1289 + 스팟 키.
3. 일반화 수정(핵심) — index 가 잘못된 tenant_id 를 주어도:
   (a) 격리 키 부재 → ambiguous(fail-closed, tenant_id=None). 잘못된 테넌트로 매핑 금지.
   (b) hcode_in 격리 키 존재 → hcode 로 **올바른** 테넌트 해석(잘못된 index tid 무시).
   (c) 명시 tenantId(UI) → 그대로 신뢰.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

MANIFEST = ROOT / "migration" / "contracts" / "tenant_master_parity_manifest.yaml"
EXPECTATIONS = ROOT / "analysis" / "welove_login_routing_expectations.json"
BASELINE_DIR = ROOT / "debug" / "baselines"

from app.services import auth_service  # noqa: E402
from app.services import tenants_directory_service  # noqa: E402


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def _load_expectations() -> dict[str, dict]:
    doc = json.loads(EXPECTATIONS.read_text(encoding="utf-8"))
    return {s["case"]: s for s in doc.get("samples", [])}


class ManifestIntegrityTests(TestCase):
    def test_cases_align_with_routing_expectations(self):
        man = _load_manifest()
        exp = _load_expectations()
        cases = {c["case"]: c for c in man["cases"]}
        # B1~B6 + A1~A5 모두 존재.
        for cid in ("A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "B6"):
            self.assertIn(cid, cases, f"manifest 누락: {cid}")
            c = cases[cid]
            self.assertEqual(c["expectations_case"], cid)
            e = exp[cid]["expected"]
            for key in ("remote_id", "db_name", "account_family"):
                if e.get(key):
                    self.assertEqual(
                        c["expected"][key], e[key],
                        f"{cid}.{key}: manifest={c['expected'].get(key)} vs expectations={e[key]}",
                    )

    def test_only_remote153_chul09_is_runtime_shared(self):
        """런타임 공유 좌표는 remote_153/chul_09_db(B3·B4)만 — 나머지는 server_id 로 단일화."""
        man = _load_manifest()
        shared = {c["case"] for c in man["cases"] if c.get("shared_db")}
        self.assertEqual(shared, {"B3", "B4"})


class GyomunsaBaselineTests(TestCase):
    def test_baseline_counts_and_spot_keys(self):
        books = json.loads((BASELINE_DIR / "gyomunsa_books.json").read_text(encoding="utf-8"))
        customers = json.loads((BASELINE_DIR / "gyomunsa_customers.json").read_text(encoding="utf-8"))
        self.assertEqual(books["count"], 3437)
        self.assertEqual(customers["count"], 1289)
        # 스팟 키 — 레거시 Ground Truth.
        self.assertIn("0", customers["by_gcode_name"])
        self.assertIn("창고", customers["by_gcode_name"]["0"])
        self.assertIn("가정학원론", books["by_gcode_name"]["1"])


# 공유 DB 합성 시드 (서버3 = 두 테넌트 공유).
_SHARED = [
    {
        "tenant_id": "tid-correct", "tenant_label_kor": "교문사",
        "account_family": "chul_09", "primary_server": "서버3",
        "db_name_logical": "chul_09_db", "default_account_type": "T3",
        "build_role": "warehouse_publisher", "is_active": True,
    },
    {
        "tenant_id": "tid-other", "tenant_label_kor": "위러브3",
        "account_family": "chul_09", "primary_server": "서버3",
        "db_name_logical": "chul_09_db", "default_account_type": "T3",
        "build_role": "warehouse_publisher", "is_active": True,
    },
]


class GeneralizedSharedDbMappingTests(TestCase):
    """index 가 잘못된 tenant_id 를 줘도 타사로 매핑되지 않음 (모든 공유 DB 공통)."""

    def _patch_seed(self, tenants):
        return patch.object(tenants_directory_service, "_load_tenants", lambda: tenants)

    def _wrong_index_hint(self):
        # login_id_index 가 공유 좌표를 위러브3 으로 붕괴시킨 상황 재현.
        return patch.object(
            auth_service, "_login_index_route_hint",
            lambda *a, **k: {"tenant_id": "tid-other", "account_family": "chul_09"},
        )

    def test_no_isolation_keys_fail_closed_not_wrong_tenant(self):
        """(a) 격리 키 부재 + index 가 위러브3 → ambiguous, tenant_id=None (잘못된 매핑 금지)."""
        with self._patch_seed(_SHARED), self._wrong_index_hint():
            meta = auth_service._resolve_account_type(
                "교문사", "5019", "remote_153", resolved_db="chul_09_db", tenant_id_hint=None
            )
        self.assertIsNone(meta.get("tenant_id"))
        self.assertEqual(meta.get("_ownership_status"), "ambiguous")
        self.assertNotEqual(meta.get("tenant_id"), "tid-other")

    def test_hcode_in_resolves_correct_tenant_despite_wrong_index(self):
        """(b) hcode_in 격리 키 존재 → hcode 로 올바른 테넌트 해석 (잘못된 index tid 무시)."""
        tenants = [
            dict(_SHARED[0], hcode_in=["5019"]),          # 교문사 소관 hcode (라이브 도출 확정)
            dict(_SHARED[1], hcode_in=["0000", "5000"]),  # 위러브3 소관 hcode (배타적 로그인)
        ]
        with self._patch_seed(tenants), self._wrong_index_hint():
            meta = auth_service._resolve_account_type(
                "교문사", "5019", "remote_153", resolved_db="chul_09_db", tenant_id_hint=None
            )
        self.assertEqual(meta.get("tenant_id"), "tid-correct")
        self.assertEqual(meta.get("_ownership_status"), "unique")

    def test_explicit_tenant_id_is_trusted(self):
        """(c) UI 가 명시한 tenantId 는 신뢰."""
        with self._patch_seed(_SHARED), self._wrong_index_hint():
            meta = auth_service._resolve_account_type(
                "교문사", "5019", "remote_153",
                resolved_db="chul_09_db", tenant_id_hint="tid-correct",
            )
        self.assertEqual(meta.get("tenant_id"), "tid-correct")
        self.assertEqual(meta.get("_ownership_status"), "unique")


class RowHcodeFallbackTests(TestCase):
    """로그인 hcode 가 JWT 에 실리도록 보장 (마스터 row-level scope 루트 원인 가드).

    루트 원인: 일부 배포의 ``auth.query`` 가 표준 ``hcode AS hcode`` 컬럼을 누락하고
    hcode 를 ``auth_flags = CONCAT(hcode, ':', gname)`` 합성 문자열에만 노출 →
    ``row.get('hcode')`` 가 공백 → scope_hcode=None → 격리 계정이 창고 전체를 조회.
    ``_row_hcode`` 는 표준 컬럼이 비면 auth_flags 접두에서 hcode 를 복원한다.
    """

    def test_standalone_hcode_column_preferred(self):
        row = {"hcode": "5019", "auth_flags": "9999:something"}
        self.assertEqual(auth_service._row_hcode(row, "hcode", "auth_flags"), "5019")

    def test_recovers_hcode_from_auth_flags_when_column_missing(self):
        # servers.yaml 드리프트 재현: 표준 hcode 컬럼 부재, auth_flags 만 존재.
        row = {"auth_flags": "5019:교문사"}
        self.assertEqual(auth_service._row_hcode(row, "hcode", "auth_flags"), "5019")

    def test_recovers_hcode_when_column_empty_string(self):
        row = {"hcode": "", "auth_flags": "5000:위러브출판사"}
        self.assertEqual(auth_service._row_hcode(row, "hcode", "auth_flags"), "5000")

    def test_empty_when_no_signal(self):
        self.assertEqual(auth_service._row_hcode({}, "hcode", "auth_flags"), "")
        self.assertEqual(
            auth_service._row_hcode({"auth_flags": "no_colon"}, "hcode", "auth_flags"), ""
        )


if __name__ == "__main__":
    main()
