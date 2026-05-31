"""Phase A — probe_account_fxx_caps 순수 함수 회귀 (DB 불요)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "debug"))

from probe_account_fxx_caps import (  # noqa: E402
    _CATALOG_FKEYS_FALLBACK,
    _diff_fxx,
    audit_tenant_registration_gaps,
    build_four_key,
    derive_account_derivation,
    derive_fkey_caps,
    inventory_f_columns,
)


class FkeyCapsTests(TestCase):
    def test_o_r_x_caps(self):
        self.assertEqual(
            derive_fkey_caps("O"),
            {"read": True, "write": True, "print": True},
        )
        self.assertEqual(
            derive_fkey_caps("R"),
            {"read": True, "write": False, "print": True},
        )
        self.assertEqual(
            derive_fkey_caps("X"),
            {"read": False, "write": False, "print": False},
        )


class FourKeyTests(TestCase):
    def test_gpass_fingerprint_not_plaintext(self):
        fk = build_four_key({"hcode": "5019", "gname": "u1", "gcode": "교문사", "gpass": "secret"})
        self.assertEqual(fk["hcode"], "5019")
        self.assertEqual(fk["gcode"], "교문사")
        self.assertNotIn("secret", json.dumps(fk))
        self.assertNotEqual(fk["gpass_fingerprint"], "empty")
        self.assertEqual(len(fk["gpass_fingerprint"]), 16)


class DeriveAccountTests(TestCase):
    def test_gyeongri_style_accounting_profile(self):
        catalog = {
            "F51": "report.kpi.read",
            "F52": "report.kpi.write",
            "F11": "master.customer.read",
        }
        fxx = {"F51": "O", "F52": "R", "F11": "X"}
        d = derive_account_derivation(fxx, catalog)
        self.assertEqual(d["login_profile"], "department_accounting")
        self.assertIn("F51", d["license_keys"])
        self.assertNotIn("F11", d["license_keys"])
        self.assertEqual(d["caps_by_fkey"]["F51"]["write"], True)
        self.assertEqual(d["caps_by_fkey"]["F52"]["write"], False)

    def test_gyomunsa_publisher_main_when_f11_present(self):
        catalog = {"F11": "master.customer.read", "F51": "report.kpi.read"}
        fxx = {"F11": "R", "F51": "R"}
        d = derive_account_derivation(fxx, catalog)
        self.assertEqual(d["login_profile"], "publisher_main")


class InventoryTests(TestCase):
    def test_catalog_alignment(self):
        cols = [{"Field": "f11"}, {"Field": "f51"}, {"Field": "f99"}]
        inv = inventory_f_columns(cols, _CATALOG_FKEYS_FALLBACK)
        self.assertIn("F11", inv["normalized_fkeys"])
        self.assertIn("F99", inv["catalog_alignment"]["in_db_not_in_catalog"])


class DiffTests(TestCase):
    def test_fxx_diff_value_and_only(self):
        left = {"F11": "R", "F51": "O"}
        right = {"F11": "O", "F52": "R"}
        d = _diff_fxx(left, right)
        self.assertEqual(d["value_diff"]["F11"], {"left": "R", "right": "O"})
        self.assertEqual(d["only_left"], {"F51": "O"})
        self.assertEqual(d["only_right"], {"F52": "R"})


class TenantGapTests(TestCase):
    def test_5097_gap_structure_offline(self):
        gap = audit_tenant_registration_gaps(hcode="5097", login_id="교문사 전자책", hname="(주)교문사")
        self.assertEqual(gap["hcode"], "5097")
        registries = {g["registry"] for g in gap["gaps"]}
        self.assertIn("tenants_directory_overlay", registries)
        self.assertIn("tenant_master_parity_manifest", registries)
        self.assertIn("account_directory_overlay", registries)


if __name__ == "__main__":
    main()
