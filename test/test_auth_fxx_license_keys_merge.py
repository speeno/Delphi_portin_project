"""사용자 Id_Logn Fxx → JWT license_keys union 회귀 (교문사/경리부 부서 계정)."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.services import auth_service  # noqa: E402


class FxxLicenseKeysMergeTest(TestCase):
    def test_fxx_to_license_keys_O_and_R_only(self) -> None:
        fxx = {"F11": "O", "F12": "R", "F13": "X", "F14": ""}
        self.assertEqual(auth_service._fxx_to_license_keys(fxx), ["F11", "F12"])

    def test_merge_preserves_tenant_and_adds_user_fxx(self) -> None:
        merged = auth_service.merge_license_keys(
            ["F90"],
            {"F51": "O", "F52": "X"},
        )
        self.assertEqual(merged, ["F51", "F90"])

    def test_gyomunsa_vs_accounting_department_profile(self) -> None:
        """레거시 chul_09_db 실측 — 교문사(F11~) vs 경리부(F51~)."""
        gyomunsa = {
            "F11": "O",
            "F12": "R",
            "F14": "O",
            "F17": "O",
            "F51": "X",
        }
        accounting = {
            "F51": "O",
            "F52": "O",
            "F53": "O",
            "F54": "O",
            "F55": "O",
        }
        gy_keys = set(auth_service._fxx_to_license_keys(gyomunsa))
        ac_keys = set(auth_service._fxx_to_license_keys(accounting))
        self.assertIn("F11", gy_keys)
        self.assertNotIn("F51", gy_keys)
        self.assertIn("F51", ac_keys)
        self.assertNotIn("F11", ac_keys)
        self.assertTrue(gy_keys.isdisjoint({"F51", "F52", "F53", "F54", "F55"}))
        self.assertEqual(
            auth_service.infer_login_profile(gyomunsa),
            "publisher_main",
        )
        self.assertEqual(
            auth_service.infer_login_profile(accounting),
            "department_accounting",
        )

    def test_infer_login_profile_unconfigured_when_empty(self) -> None:
        self.assertEqual(auth_service.infer_login_profile({}), "unconfigured")
        self.assertEqual(auth_service.infer_login_profile(None), "unconfigured")


if __name__ == "__main__":
    main(verbosity=2)
