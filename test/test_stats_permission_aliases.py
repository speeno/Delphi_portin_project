"""admin.stats.* ↔ report.* 권한 alias 회귀."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.deps import _has_permission  # noqa: E402
from app.core.permission_aliases import STAT_PERMISSION_ALIASES, permission_matches  # noqa: E402


class StatsPermissionAliasesTest(TestCase):
    def test_alias_table_has_all_stats_codes(self) -> None:
        self.assertEqual(
            set(STAT_PERMISSION_ALIASES.keys()),
            {
                "admin.stats.sales",
                "admin.stats.customer",
                "admin.stats.book",
                "admin.stats.quarterly",
            },
        )

    def test_permission_matches_customer_by_report_kpi(self) -> None:
        self.assertTrue(permission_matches("admin.stats.customer", {"report.kpi.read"}))

    def test_permission_matches_sales_by_report_kpi(self) -> None:
        self.assertTrue(permission_matches("admin.stats.sales", {"report.kpi.read"}))

    def test_permission_matches_book_by_report_book(self) -> None:
        self.assertTrue(permission_matches("admin.stats.book", {"report.book.read"}))

    def test_deps_has_permission_uses_alias(self) -> None:
        ctx = {"permissions": ["report.kpi.read"], "role": "operator", "hcode": "5019"}
        self.assertTrue(_has_permission(ctx, "admin.stats.customer"))
        self.assertTrue(_has_permission(ctx, "admin.stats.book"))


if __name__ == "__main__":
    main(verbosity=2)

