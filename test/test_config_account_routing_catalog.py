"""Config.Ini → 계정 라우팅 카탈로그 도구 회귀 가드 (DSN-DEC-12 보조)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "build_config_account_routing_catalog.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "build_config_account_routing_catalog", TOOL_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("build_config_account_routing_catalog", mod)
    spec.loader.exec_module(mod)
    return mod


def _seed_doc():
    return {
        "tenants": [
            {
                "tenant_id": "t-chul-03",
                "tenant_label_kor": "한강도서",
                "account_family": "chul_03",
                "build_role": "distributor",
                "default_account_type": "T2_DIST",
                "primary_server": "서버3",
                "db_name_logical": "chul_03_db",
                "is_active": True,
            },
            {
                "tenant_id": "t-chul-09-a",
                "tenant_label_kor": "위러브1",
                "account_family": "chul_09",
                "primary_server": "서버1",
                "db_name_logical": "chul_09_db",
                "is_active": True,
            },
            {
                "tenant_id": "t-chul-09-b",
                "tenant_label_kor": "위러브2",
                "account_family": "chul_09",
                "primary_server": "서버1",
                "db_name_logical": "chul_09_db",
                "is_active": True,
            },
        ]
    }


def _matrix_doc():
    return {
        "routes": [
            {
                "server_id": "서버3",
                "tenant_name_kor": "한강도서",
                "db_name_logical": "chul_03_db",
                "account_family": "chul_03",
            },
            {
                "server_id": "서버1",
                "tenant_name_kor": "위러브1",
                "db_name_logical": "chul_09_db",
                "account_family": "chul_09",
            },
        ]
    }


class LabelToRemoteIdTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_korean_label_mapping(self):
        self.assertEqual(self.tool.label_to_remote_id("서버3"), "remote_153")
        self.assertEqual(self.tool.label_to_remote_id("서버4"), "remote_138")

    def test_remote_passthrough(self):
        self.assertEqual(self.tool.label_to_remote_id("remote_153"), "remote_153")

    def test_unknown_returns_none(self):
        self.assertIsNone(self.tool.label_to_remote_id(""))
        self.assertIsNone(self.tool.label_to_remote_id("서버99"))


class ClassifyRowTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()
        self.matrix_by_family = self.tool._matrix_routes_by_family(_matrix_doc())
        self.seed_by_family = self.tool._seed_tenants_by_family(_seed_doc(), None)
        self.seed_label_pool = self.tool._seed_labels(_seed_doc(), None)
        self.shared_index = self.tool._shared_db_index(self.seed_by_family)

    def _classify(self, row: dict) -> dict:
        return self.tool.classify_row(
            row,
            matrix_by_family=self.matrix_by_family,
            seed_by_family=self.seed_by_family,
            seed_label_pool=self.seed_label_pool,
            chul_by_subpath={},
            shared_index=self.shared_index,
        )

    def test_family_matrix_seed_matched_high(self):
        row = {
            "config_path": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)/Config.Ini",
            "config_kind": "customer_build",
            "account_family_inferred": "chul_03",
            "build_subpath": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)",
            "name": "한강도서",
            "uses": "한강도서",
            "customer_folder": "한강도서",
        }
        result = self._classify(row)
        self.assertEqual(result["match"]["status"], "matched")
        self.assertEqual(result["match"]["confidence"], "high")
        self.assertIn("matrix", result["match"]["sources"])
        self.assertIn("seed", result["match"]["sources"])
        self.assertEqual(result["routing"]["remote_id"], "remote_153")
        self.assertEqual(result["routing"]["db_name_logical"], "chul_03_db")
        self.assertEqual(result["routing"]["tenant_id"], "t-chul-03")

    def test_infra_kind_skipped(self):
        row = {
            "config_path": "도서유통-출판/MySQL/Config.Ini",
            "config_kind": "infra_mysql",
            "account_family_inferred": None,
            "build_subpath": "도서유통-출판/MySQL",
            "name": "",
            "uses": "",
            "customer_folder": "MySQL",
        }
        result = self._classify(row)
        self.assertEqual(result["match"]["status"], "infra_skip")
        self.assertEqual(result["routing"]["remote_id"], "")
        self.assertEqual(result["routing"]["db_name_logical"], "")

    def test_family_only_partial(self):
        row = {
            "config_path": "도서유통-출판/MySQL/도서유통/chul_99(미지)/Config.Ini",
            "config_kind": "customer_build",
            "account_family_inferred": "chul_99",
            "build_subpath": "도서유통-출판/MySQL/도서유통/chul_99(미지)",
            "name": "미지",
            "uses": "미지",
            "customer_folder": "미지",
        }
        result = self._classify(row)
        self.assertEqual(result["match"]["status"], "partial")
        self.assertEqual(result["match"]["confidence"], "low")
        self.assertIn("family_not_in_matrix_or_seed", result["match"]["reasons"])

    def test_label_fuzzy_only_review(self):
        row = {
            "config_path": "Welove_인수인계/한강도서/Chulpan.Net/Config.Ini",
            "config_kind": "customer_build",
            "account_family_inferred": None,
            "build_subpath": "Welove_인수인계/한강도서/Chulpan.Net",
            "name": "(주)한강도서",
            "uses": "한강도서",
            "customer_folder": "Chulpan.Net",
        }
        result = self._classify(row)
        self.assertEqual(result["match"]["status"], "review")
        self.assertIn("label_fuzzy", result["match"]["sources"])
        self.assertIn("label_fuzzy_only", result["match"]["reasons"])

    def test_no_family_no_label_review(self):
        row = {
            "config_path": "Welove_인수인계/x/Chulpan.Net/Config.Ini",
            "config_kind": "customer_build",
            "account_family_inferred": None,
            "build_subpath": "Welove_인수인계/x/Chulpan.Net",
            "name": "전혀다른업체",
            "uses": "AAA",
            "customer_folder": "Chulpan.Net",
        }
        result = self._classify(row)
        self.assertEqual(result["match"]["status"], "review")
        self.assertIn("no_family_no_label_match", result["match"]["reasons"])

    def test_shared_db_flagged(self):
        row = {
            "config_path": "x/chul_09(위러브)/Config.Ini",
            "config_kind": "customer_build",
            "account_family_inferred": "chul_09",
            "build_subpath": "x/chul_09(위러브)",
            "name": "위러브",
            "uses": "위러브",
            "customer_folder": "위러브",
        }
        result = self._classify(row)
        self.assertTrue(result["shared_db"]["is_shared"])
        self.assertTrue(result["shared_db"]["needs_hcode_guard"])
        self.assertIn("shared_db_no_hcode_guard", result["match"]["reasons"])


class ChulMismatchTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_chul_remote_id_mismatch_emits_overlay_proposal(self):
        seed = _seed_doc()
        matrix = _matrix_doc()
        chul = {
            "rows": [
                {
                    "rel_path": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)/Chul.pas",
                    "remote_id": "remote_138",
                    "database": "chul_03_db",
                    "host_ip": "115.68.7.138",
                    "account_family": "chul_03",
                }
            ]
        }
        catalog, _, _ = self.tool.build_catalog(
            [
                {
                    "config_path": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)/Config.Ini",
                    "config_kind": "customer_build",
                    "account_family_inferred": "chul_03",
                    "build_subpath": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)",
                    "name": "한강도서",
                    "uses": "한강도서",
                    "customer_folder": "한강도서",
                }
            ],
            matrix_doc=matrix,
            seed_doc=seed,
            overlay_doc=None,
            chul_doc=chul,
        )
        self.assertEqual(len(catalog), 1)
        self.assertIn("chul_remote_id_mismatch", catalog[0]["match"]["reasons"])
        proposals = self.tool.emit_overlay_proposals(catalog)
        self.assertEqual(len(proposals), 0)
        # high → medium 으로 강등됐는지 (reasons 가 있으면 medium)
        self.assertEqual(catalog[0]["match"]["confidence"], "medium")


class FullInventoryIntegrationTests(TestCase):
    """591행 인벤토리 전량으로 회귀 가드 — CI 1차 정책."""

    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_catalog_row_count_equals_inventory_count(self):
        inv_path = ROOT / "analysis" / "welove_config_ini_inventory.json"
        if not inv_path.exists():
            self.skipTest("inventory not generated yet")
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        catalog, review_queue, summary = self.tool.build_catalog(
            list(inv.get("items") or []),
            matrix_doc=json.loads(
                (ROOT / "analysis" / "welove_db_route_matrix.json").read_text(encoding="utf-8")
            ),
            seed_doc=json.loads(
                (
                    ROOT
                    / "도서물류관리프로그램"
                    / "backend"
                    / "data"
                    / "tenants_directory_seed.json"
                ).read_text(encoding="utf-8")
            ),
            overlay_doc=None,
            chul_doc=None,
        )
        self.assertEqual(len(catalog), inv.get("count"))
        # status 합집합은 카탈로그 행 수와 동일.
        statuses = {"matched", "partial", "review", "infra_skip"}
        self.assertEqual(
            sum(summary["status_counts"].get(s, 0) for s in statuses), len(catalog)
        )
        # review_queue 는 status==review 행과 동일.
        self.assertEqual(len(review_queue), summary["status_counts"].get("review", 0))

    def test_secrets_policy_no_credentials_in_output(self):
        """카탈로그·overlay 제안은 자격증명 키를 포함하면 안 된다 (G3)."""
        inv = [
            {
                "config_path": "x/chul_03(한강도서)/Config.Ini",
                "config_kind": "customer_build",
                "account_family_inferred": "chul_03",
                "build_subpath": "x/chul_03(한강도서)",
                "name": "한강도서",
                "uses": "한강도서",
                "customer_folder": "한강도서",
            }
        ]
        catalog, _, _ = self.tool.build_catalog(
            inv,
            matrix_doc=_matrix_doc(),
            seed_doc=_seed_doc(),
            overlay_doc=None,
            chul_doc=None,
        )
        text = json.dumps(catalog, ensure_ascii=False).lower()
        for forbidden in ("password", "username", "gpass", "user_pw", "_pw", "secret"):
            self.assertNotIn(forbidden, text, f"forbidden key leaked: {forbidden}")


if __name__ == "__main__":
    main()
