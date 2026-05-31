"""프론트 PermissionGuard alias 정적 회귀."""
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class PermissionGuardAliasStaticTest(TestCase):
    def test_alias_file_contains_stats_mapping(self) -> None:
        src = (FE / "lib" / "permission-aliases.ts").read_text(encoding="utf-8")
        for code in (
            "admin.stats.sales",
            "admin.stats.customer",
            "admin.stats.book",
            "admin.stats.quarterly",
            "report.kpi.read",
            "report.month.read",
            "report.book.read",
        ):
            self.assertIn(code, src)

    def test_permission_guard_uses_has_aliased_permission(self) -> None:
        src = (FE / "components" / "auth" / "permission-guard.tsx").read_text(encoding="utf-8")
        self.assertIn('import { hasAliasedPermission } from "@/lib/permission-aliases"', src)
        self.assertIn("return hasAliasedPermission(code, perms);", src)


if __name__ == "__main__":
    main(verbosity=2)

