"""DEC-058 사이드바 권한 게이팅 — 정적 회귀 가드.

배경
----
- 본 레포는 프론트엔드 jest/vitest 러너를 두지 않는다 (Next.js 런타임 일체화 정책).
- 그러므로 ``sidebar.tsx`` 의 가시성 필터링 동작은 *정적 가드* 로 검증한다:
    1. ``form-registry.ts`` 의 모든 ``requiredPermission`` 값이 카탈로그
       (``permission-keys-catalog.md`` §1+§4) 의 정본 ``permission_code`` 부분집합.
    2. ``sidebar.tsx`` 가 ``usePermissions`` 를 호출하고 게이팅 필터를 사용함.
    3. ``use-permissions.ts`` 가 슈퍼유저 동등 분기 (``hcode === '0000'`` /
       ``role === 'admin'`` / ``permissions.includes('*')``) 를 모두 포함함.

검증 항목
---------
1. ``form-registry.ts::requiredPermission`` 모든 값 ⊆ catalog 의 permission_code 셋.
2. ``sidebar.tsx`` 가 ``usePermissions()`` 를 import + 호출 + 가시성 필터에 사용.
3. ``use-permissions.ts`` 가 isSuperUser 3 분기 모두 포함.
"""
from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main


_REPO_ROOT = Path(__file__).resolve().parent.parent
_FRONTEND_ROOT = _REPO_ROOT / "도서물류관리프로그램" / "frontend"
_FORM_REGISTRY = _FRONTEND_ROOT / "src" / "lib" / "form-registry.ts"
_SIDEBAR = _FRONTEND_ROOT / "src" / "components" / "app-shell" / "sidebar.tsx"
_USE_PERMS = _FRONTEND_ROOT / "src" / "lib" / "use-permissions.ts"
_CATALOG = _REPO_ROOT / "legacy-analysis" / "permission-keys-catalog.md"


def _catalog_codes() -> set[str]:
    """카탈로그 §1+§4 의 모든 permission_code 셋 (예약 행 제외)."""
    text = _CATALOG.read_text(encoding="utf-8")
    pattern = re.compile(r"^\|\s*F\d+\w*\s*\|\s*`([\w\.]+)`\s*\|", re.MULTILINE)
    return {m.group(1) for m in pattern.finditer(text)}


def _registered_required_permissions() -> set[str]:
    """form-registry.ts 의 모든 ``requiredPermission: "..."`` 값 추출."""
    text = _FORM_REGISTRY.read_text(encoding="utf-8")
    return set(re.findall(r'requiredPermission:\s*"([\w\.\*]+)"', text))


class SidebarPermissionGatingTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = _catalog_codes()
        cls.required = _registered_required_permissions()

    def test_all_required_permissions_in_catalog(self) -> None:
        """form-registry 의 모든 requiredPermission 이 카탈로그 정본."""
        unknown = self.required - self.catalog
        self.assertSetEqual(
            unknown, set(),
            f"카탈로그에 없는 permission_code 가 form-registry.ts 에 사용됨: "
            f"{sorted(unknown)}. permission-keys-catalog.md §1·§4 에 등록 필요.",
        )

    def test_form_registry_has_meaningful_seed(self) -> None:
        """phase1 정식 화면들이 가시성 게이팅을 받도록 최소 시드 가드."""
        # admin 그룹의 핵심 화면 4건이 모두 admin.user.write 게이팅
        text = _FORM_REGISTRY.read_text(encoding="utf-8")
        self.assertIn('"WebAdmRBAC"', text)
        self.assertIn('"WebAdmEnv"', text)
        self.assertIn('"Subu10_id_logn"', text)
        # admin.user.write 가 최소 3건 이상 사용됨 (관리 메뉴 가드)
        admin_write_uses = text.count('requiredPermission: "admin.user.write"')
        self.assertGreaterEqual(
            admin_write_uses, 3,
            "admin.user.write 게이팅이 관리 메뉴 다수에 적용되어야 함 (DEC-058)",
        )

    def test_sidebar_uses_usepermissions_hook(self) -> None:
        """sidebar.tsx 가 usePermissions 를 import + 호출 + 게이팅에 사용."""
        text = _SIDEBAR.read_text(encoding="utf-8")
        self.assertIn(
            'from "@/lib/use-permissions"', text,
            "sidebar.tsx 가 usePermissions hook 을 import 해야 함",
        )
        self.assertIn(
            "usePermissions()", text,
            "sidebar.tsx 가 usePermissions() 를 호출해야 함",
        )
        # 가시성 필터: requiredPermission + perms.has 패턴
        self.assertRegex(
            text,
            r"(requiredPermission|perms\.has\()",
            "sidebar.tsx 가 requiredPermission 게이팅 필터를 적용해야 함 (DEC-058)",
        )

    def test_use_permissions_super_user_three_branches(self) -> None:
        """use-permissions.ts 가 슈퍼유저 동등 3 분기 모두 포함."""
        text = _USE_PERMS.read_text(encoding="utf-8")
        # '*' 와일드카드
        self.assertIn('"*"', text, "와일드카드 '*' 분기 누락")
        # role === 'admin'
        self.assertRegex(text, r'role\s*===\s*"admin"', "role==='admin' 분기 누락")
        # hcode === '0000'
        self.assertRegex(text, r'hcode\s*===\s*"0000"', "hcode==='0000' 분기 누락")
        # PermissionsApi 인터페이스 export
        self.assertIn("PermissionsApi", text)
        self.assertIn("isSuperUser", text)


if __name__ == "__main__":
    main(verbosity=2)
