"""경리부 full-CRUD 부여 회귀 (운영 요청 2026-06-20).

검증 범위
---------
1. ``full_crud_effective_fxx`` 가 대상 계정("경리부")의 업무 Fxx 를 전부 ``O`` 로
   승격하고, 관리자 플랫폼 Fxx(F18/F50/F5xe/F90~F92)는 건드리지 않으며, 원본 dict
   을 변형하지 않는다(비대상 계정은 무영향).
2. 효과 매트릭스 → permissions 합성이 업무 write 코드(master.write·return.write·
   settlement.write 등)를 포함하고 admin.* 는 제외 → 관리자 권한 상승이 없다.
3. 효과 매트릭스 → fxx_caps 가 업무 셀 write=True 를 산출(화면 단 canWrite).
4. ``BLS_FULL_CRUD_LOGIN_IDS`` env 정책(미설정/빈/콤마) 이 ``_admin_whitelist_ids``
   와 동일하게 동작.
5. **불변식**: 승격은 메뉴 구성에 쓰이는 ``infer_login_profile`` 결과를 바꾸지
   않는다(login_profile 은 *원본* 매트릭스로 산출 — 호출자 책임). 부서계정 원본
   매트릭스(F51~F55)는 그대로 ``department_accounting`` 로 분류된다.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import TestCase, main

_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.core.fxx_caps import build_fxx_caps_from_matrix  # noqa: E402
from app.services import auth_service  # noqa: E402

_ADMIN_PLATFORM_FXX = {"F18", "F18r", "F50", "F51e", "F52e", "F53e", "F90", "F91", "F92"}


class FullCrudEffectiveFxxTest(TestCase):
    def test_non_target_account_unchanged(self) -> None:
        orig = {"F11": "X", "F51": "O"}
        out = auth_service.full_crud_effective_fxx("교문사", orig)
        self.assertEqual(out, orig)
        # 원본 비파괴 — 새 dict 반환.
        self.assertIsNot(out, orig)

    def test_keiri_business_cells_all_open(self) -> None:
        orig = {"F11": "X", "F51": "O", "F52": "O", "F53": "O", "F54": "O", "F55": "O"}
        out = auth_service.full_crud_effective_fxx("경리부", orig)
        for fkey in auth_service._FULL_CRUD_BUSINESS_FXX:
            self.assertEqual(out.get(fkey), "O", f"{fkey} 가 O 로 승격되지 않음")
        # X 였던 마스터 셀도 O 로 승격.
        self.assertEqual(out.get("F11"), "O")

    def test_admin_platform_fxx_not_granted(self) -> None:
        out = auth_service.full_crud_effective_fxx("경리부", {"F51": "O"})
        for fkey in _ADMIN_PLATFORM_FXX:
            self.assertNotEqual(
                out.get(fkey), "O", f"관리자 플랫폼 키 {fkey} 가 승격되어 권한 상승 위험"
            )

    def test_original_matrix_not_mutated(self) -> None:
        orig = {"F11": "X", "F51": "O"}
        snapshot = dict(orig)
        auth_service.full_crud_effective_fxx("경리부", orig)
        self.assertEqual(orig, snapshot, "원본 매트릭스가 in-place 변형됨")

    def test_permissions_include_business_write_exclude_admin(self) -> None:
        eff = auth_service.full_crud_effective_fxx("경리부", {"F51": "O"})
        catalog = auth_service._load_legacy_permission_index()
        role, perms = auth_service._merge_fxx_to_permissions(eff, catalog)
        self.assertEqual(role, "operator")
        # 업무 write 코드 포함.
        for code in ("master.write", "return.write", "settlement.write", "outbound.write"):
            self.assertIn(code, perms, f"{code} 가 경리부 권한에 없음")
        # 관리자 코드 제외 (권한 상승 차단).
        for code in ("admin.user.write", "admin.audit.read", "admin.stats.sales"):
            self.assertNotIn(code, perms, f"{code} 가 경리부에 부여됨(권한 상승)")

    def test_fxx_caps_grant_write(self) -> None:
        eff = auth_service.full_crud_effective_fxx("경리부", {"F51": "O"})
        caps = build_fxx_caps_from_matrix(eff)
        for fkey in ("F11", "F21", "F23", "F31", "F41", "F55"):
            self.assertTrue(caps.get(fkey, {}).get("write"), f"{fkey} write 캡 누락")

    def test_login_profile_preserved_on_original(self) -> None:
        # 부서계정 원본(F51~F55=O)은 승격과 무관하게 department_accounting.
        orig = {"F51": "O", "F52": "O", "F53": "O", "F54": "O", "F55": "O"}
        self.assertEqual(auth_service.infer_login_profile(orig), "department_accounting")


class FullCrudLoginIdsEnvPolicyTest(TestCase):
    def setUp(self) -> None:
        self._saved = os.environ.get("BLS_FULL_CRUD_LOGIN_IDS")

    def tearDown(self) -> None:
        if self._saved is None:
            os.environ.pop("BLS_FULL_CRUD_LOGIN_IDS", None)
        else:
            os.environ["BLS_FULL_CRUD_LOGIN_IDS"] = self._saved

    def test_unset_defaults_to_keiri(self) -> None:
        os.environ.pop("BLS_FULL_CRUD_LOGIN_IDS", None)
        self.assertEqual(auth_service._full_crud_login_ids(), {"경리부"})
        self.assertTrue(auth_service.is_full_crud_account("경리부"))
        self.assertFalse(auth_service.is_full_crud_account("교문사"))

    def test_empty_disables(self) -> None:
        os.environ["BLS_FULL_CRUD_LOGIN_IDS"] = ""
        self.assertEqual(auth_service._full_crud_login_ids(), set())
        self.assertFalse(auth_service.is_full_crud_account("경리부"))

    def test_csv_overrides_default(self) -> None:
        os.environ["BLS_FULL_CRUD_LOGIN_IDS"] = "경리부, 회계팀"
        ids = auth_service._full_crud_login_ids()
        self.assertEqual(ids, {"경리부", "회계팀"})
        self.assertTrue(auth_service.is_full_crud_account("회계팀"))


if __name__ == "__main__":
    main()
