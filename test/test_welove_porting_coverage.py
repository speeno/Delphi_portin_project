"""WeLove_FTP 전체 계정 포팅 커버리지 회귀 가드."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


class WeLovePortingCoverageTests(TestCase):
    def test_dpr_closure_inventory_covers_all_known_projects_without_secret_keys(self) -> None:
        closures = _json("analysis/welove_dpr_closures.json")

        self.assertGreaterEqual(closures["totals"]["dpr_count"], 468)
        self.assertEqual(closures["totals"]["secret_adjacent_path_count"], 0)
        bad_keys = [
            k for k in _walk_keys(closures)
            if k.lower() in {"password", "passwd", "db_password", "username", "user_name"}
        ]
        self.assertEqual(bad_keys, [])

    def test_all_active_tenants_have_build_and_closure_trace(self) -> None:
        matrix = _json("analysis/welove_tenant_build_routing_matrix.json")

        self.assertEqual(matrix["totals"]["active_build_id_missing"], 0)
        self.assertEqual(matrix["totals"]["trace_status_counts"], {"ok": 40})
        for row in matrix["rows"]:
            with self.subTest(tenant=row["tenant_id"]):
                self.assertTrue(row["active_build_id"])
                self.assertTrue(row["closure_hashes"], row)
                self.assertTrue(row["execution_types"], row)

    def test_completed_screen_mappings_have_build_variant_sources(self) -> None:
        coverage = _json("analysis/welove_screen_contract_coverage.json")
        by_form = {row["form_id"]: row for row in coverage["forms"]}
        totals = coverage["totals"]

        self.assertEqual(totals["uncovered_mapping_note_count"], 0)
        self.assertEqual(totals["covered_mapping_note_count"], totals["mapping_note_count"])
        for form_id in ("Sobo11", "Sobo14", "Sobo39", "Sobo45_billing"):
            with self.subTest(form_id=form_id):
                row = by_form[form_id]
                self.assertGreater(row["variant_count"], 0)
                variant = row["customer_variants"][0]
                self.assertTrue(variant["build_id"])
                self.assertTrue(variant["dpr_closure_hash"])
                self.assertTrue(variant["source_pas_path"])
                self.assertTrue(variant["source_dfm_path"])

        for form_id in ("Id_Logn", "c8_scan_match"):
            with self.subTest(form_id=form_id):
                row = by_form[form_id]
                self.assertGreater(row["variant_count"], 0, msg=f"{form_id} uses LAYOUT_NOTE_EXTRA_UNIT_ALIASES for closure match")
                variant = row["customer_variants"][0]
                self.assertTrue(variant["source_pas_path"])
                self.assertTrue(variant["source_dfm_path"])

    def test_build_forced_hidden_menu_keys_match_seeded_tenant_builds(self) -> None:
        tenants = _json("도서물류관리프로그램/backend/data/tenants_directory_seed.json")
        active_ids = {str(t["active_build_id"]).strip() for t in tenants.get("tenants") or [] if t.get("active_build_id")}
        forced = yaml.safe_load((ROOT / "migration/contracts/build_forced_hidden_menus.yaml").read_text(encoding="utf-8"))
        for build_id in (forced.get("builds") or {}).keys():
            with self.subTest(build_id=build_id):
                self.assertIn(str(build_id), active_ids)

    def test_rbac_source_build_aliases_match_known_welove_builds(self) -> None:
        contract = yaml.safe_load((ROOT / "migration/contracts/welove_build_coverage.yaml").read_text(encoding="utf-8"))
        self.assertEqual(contract["artifacts"]["tenant_build_routing"], "analysis/welove_tenant_build_routing_matrix.json")

        rbac = yaml.safe_load((ROOT / "migration/contracts/rbac_menu_matrix.yaml").read_text(encoding="utf-8"))
        known_aliases = {"D-STD", "P-STD", "D-KBT", "P-KBT", "WH-WL", "WH-MS", "WH-BB"}
        aliases = {
            alias
            for menu in rbac.get("menus") or []
            for alias in (menu.get("source_builds") or [])
        }
        self.assertTrue(aliases)
        self.assertFalse(aliases - known_aliases)

    def test_backend_auth_model_preserves_active_build_id_claim(self) -> None:
        from app.models.auth import UserInfo

        user = UserInfo(
            user_id="u",
            active_build_id="BLD-PUB-WAREHOUSE-WELOVE",
            build_role="warehouse_publisher",
        )
        self.assertEqual(user.active_build_id, "BLD-PUB-WAREHOUSE-WELOVE")


if __name__ == "__main__":
    main(verbosity=2)
