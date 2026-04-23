"""admin 슈퍼유저의 정산/통계 전수 접근 회귀 가드 (DEC-058 Wave B 통합).

검증 흐름
---------
1. ``admin_service`` 가 사용자에 ``role-admin`` 매핑 (web_admin.json 시드)
2. ``auth_service._resolve_role_and_permissions`` (분기 0) → admin / ['*']
3. JWT ctx 합성: ``{"role": "admin", "permissions": ["*"]}``
4. ``deps._has_permission(ctx, code)`` 가 정산 7개 + 통계 4개 권한 코드 *모두*
   통과 — 사용자 룰: "admin 모든 메뉴와 데이터가 접근가능" 엔드 투 엔드 검증.

본 가드는 사용자 룰의 일반화 정신: 특정 메뉴 한정 패치가 아니라 admin role
매핑된 사용자가 모든 ``require_permission`` 게이트를 통과함을 보장.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))


# 정산(Settlement) — backend.log 4월 21~22일 실패/통과 endpoint 7화면 권한 코드
_SETTLEMENT_PERMISSIONS = [
    "settlement.billing.read",
    "settlement.billing.write",
    "settlement.cash.read",
    "settlement.cash.write",
    "settlement.outstanding.read",
    "settlement.tax.read",
    "settlement.tax.write",
]

# 통계(Stats) — backend.log 4월 22일 403 발생한 stats/customer-analysis,
# stats/sales-period 등 통계 4개 권한 코드 (legacy_permission_map 시드 포함).
_STATS_PERMISSIONS = [
    "admin.stats.sales",
    "admin.stats.customer",
    "admin.stats.book",
    "admin.stats.quarterly",
]


class AdminFullAccessTest(TestCase):
    """admin role 매핑 → 모든 require_permission 통과 (분기 0 + _has_permission '*')."""

    def test_branch0_resolves_admin_role_to_star_permissions(self) -> None:
        """Step 1~2: admin_service 매핑 + auth_service 분기 0 = admin/['*']."""
        from app.services import auth_service
        with patch(
            "app.services.admin_service.list_user_roles_and_permissions",
            return_value=(["role-admin"], set()),
        ):
            role, perms = auth_service._resolve_role_and_permissions("admin", "")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    def test_admin_passes_all_settlement_guards(self) -> None:
        """Step 3~4: admin ctx 가 정산 7개 권한 모두 통과 (_has_permission)."""
        from app.core import deps
        ctx = {"role": "admin", "permissions": ["*"], "hcode": "12345"}
        for code in _SETTLEMENT_PERMISSIONS:
            with self.subTest(code=code):
                self.assertTrue(
                    deps._has_permission(ctx, code),
                    f"admin 이 {code} 가드 실패 — 분기 0 / star 매칭 회귀",
                )

    def test_admin_passes_all_stats_guards(self) -> None:
        """통계 4개 권한도 모두 통과 — backend.log 403 회귀 가드."""
        from app.core import deps
        ctx = {"role": "admin", "permissions": ["*"], "hcode": "12345"}
        for code in _STATS_PERMISSIONS:
            with self.subTest(code=code):
                self.assertTrue(
                    deps._has_permission(ctx, code),
                    f"admin 이 {code} 가드 실패 — 통계 화면 403 회귀",
                )

    def test_non_admin_without_explicit_permission_blocked(self) -> None:
        """일반 사용자(분기 0 미발효) 는 명시 권한 없이 차단 — 부작용 없음."""
        from app.core import deps
        ctx = {"role": "operator", "permissions": ["books.read"], "hcode": "11111"}
        for code in _SETTLEMENT_PERMISSIONS + _STATS_PERMISSIONS:
            with self.subTest(code=code):
                self.assertFalse(
                    deps._has_permission(ctx, code),
                    f"일반 사용자가 {code} 통과 — 권한 모델 회귀",
                )


if __name__ == "__main__":
    main()
