"""DEC-384 — 조회 전용 계정(교문사 류) 화면 구성: 반품/폐기 · 출고관리 · 정산관리는 읽기 전용으로 보이고, 웹관리는 제거.

사용자(2026-10-07)
- 「교문사 계정에서 반품재고 메뉴 그룹과 출고관리 메뉴, 정산관리 메뉴가 readonly 로 보여야 된다」
- 「교문사 류의 계정은 웹관리 메뉴 제거」

결정 — 계약 ``account_write_policy.yaml`` 의 규칙별 ``view`` (코드 분기 없음):
- ``grant_permissions`` — 세 영역 화면의 조회 권한을 더한다(쓰기는 DEC-370 미들웨어가 그대로 403).
- ``revoke_permission_prefixes: [admin.]`` — 웹관리 조회 권한 제거(URL 직접 진입도 서버가 거절).
- ``hide_menu_groups: [admin]`` — 사이드바 「웹관리」 그룹을 그리지 않는다(슈퍼 권한이어도).
- 요청마다 ``get_user_context`` 에서 적용 → 이미 받은 토큰도 즉시 반영. ``/auth/me`` 도 같은 결과.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from app.services import account_write_policy as awp

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"

GYOMUNSA = {
    "hcode": "5019", "account_type": "T3", "build_role": "warehouse_publisher",
    "account_family": "chul_09", "login_profile": "publisher_main", "resolved_db": "chul_09_db",
}
GYEONGRI = {**GYOMUNSA, "login_profile": "department_accounting"}


class ViewPolicy(unittest.TestCase):
    def setUp(self) -> None:
        awp.reload_for_tests()

    def test_grants_area_read_and_revokes_admin(self) -> None:
        perms = awp.effective_permissions(GYOMUNSA, ["master.book.read", "admin.user.read", "admin.audit.read"])
        for p in ("outbound.read", "return.read", "settlement.read", "settlement.misc", "settlement.deposit"):
            self.assertIn(p, perms)
        self.assertNotIn("admin.user.read", perms)
        self.assertNotIn("admin.audit.read", perms)
        self.assertIn("master.book.read", perms)
        self.assertEqual(awp.read_only_view(GYOMUNSA)["hide_menu_groups"], ["admin"])

    def test_other_accounts_unchanged(self) -> None:
        src = ["admin.user.read", "outbound.write"]
        self.assertEqual(awp.effective_permissions(GYEONGRI, src), src)
        self.assertEqual(awp.effective_permissions(GYOMUNSA, ["*"]), ["*"])
        self.assertEqual(awp.read_only_view(GYEONGRI)["hide_menu_groups"], [])

    def test_wiring(self) -> None:
        deps = (BACK / "core" / "deps.py").read_text(encoding="utf-8")
        self.assertIn('ctx["permissions"] = effective_permissions(ctx, ctx["permissions"])', deps)
        auth = (BACK / "routers" / "auth.py").read_text(encoding="utf-8")
        self.assertIn('out["permissions"] = effective_permissions(out, out.get("permissions"))', auth)
        self.assertIn('out["read_only_hidden_menu_groups"]', auth)
        model = (BACK / "models" / "auth.py").read_text(encoding="utf-8")
        self.assertIn("read_only_hidden_menu_groups: list[str] = []", model)
        side = (FE / "components" / "app-shell" / "sidebar.tsx").read_text(encoding="utf-8")
        self.assertIn("user?.read_only_hidden_menu_groups", side)
        self.assertIn("if (hiddenGroups.has(group.id)) {", side)


if __name__ == "__main__":
    unittest.main()
