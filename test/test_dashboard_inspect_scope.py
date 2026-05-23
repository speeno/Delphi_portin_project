"""
대시보드 KPI — 관리자 타사 DB 점검 모드 hcode 스코프 회귀 가드.

점검 모드에서 수퍼 hcode(0000)가 쿼리에 실리면 KPI가 전부 0으로 보이는 회귀를 막는다.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.core.inspect_context import InspectContext, set_inspect_context, clear_inspect_context  # noqa: E402
from app.routers.stats import _effective_dashboard_hcode  # noqa: E402


class EffectiveDashboardHcodeTests(unittest.TestCase):
    def tearDown(self) -> None:
        clear_inspect_context()

    def test_inspect_subject_hcode_overrides_super_query(self) -> None:
        set_inspect_context(
            server_id="remote_138",
            db_name="tenant_a",
            reason="test",
            subject_login_id="user01",
            subject_hcode="0123",
        )
        self.assertEqual(_effective_dashboard_hcode("0000", {}), "0123")

    def test_super_hcode_0000_means_no_filter(self) -> None:
        self.assertIsNone(_effective_dashboard_hcode("0000", {}))
        self.assertIsNone(_effective_dashboard_hcode(" 0000 ", {}))

    def test_normal_tenant_hcode_preserved(self) -> None:
        self.assertEqual(_effective_dashboard_hcode("0456", {}), "0456")

    def test_ctx_inspect_subject_hcode_fallback(self) -> None:
        self.assertEqual(
            _effective_dashboard_hcode(None, {"inspect_subject_hcode": "0789"}),
            "0789",
        )


class DashboardInspectFrontendScopeTests(unittest.TestCase):
    def test_role_dashboard_uses_resolve_scope_and_inspect_listener(self) -> None:
        src = (FE_SRC / "components" / "dashboard" / "role-dashboard-view.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn("resolveDashboardApiScope", src)
        self.assertIn("admin-inspect-changed", src)

    def test_admin_inspect_context_exports_scope_helper(self) -> None:
        src = (FE_SRC / "lib" / "admin-inspect-context.ts").read_text(encoding="utf-8")
        self.assertIn("resolveDashboardApiScope", src)
        self.assertIn('rawHcode !== "0000"', src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
