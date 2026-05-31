from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services.g1_ggeo_adapt import gbun_code_column, gbun_name_column


class CustomerGbunResolveTests(TestCase):
    """get_customer_master G1_Gbun 이중 조인 SQL 조각 회귀."""

    def test_dual_join_uses_code_and_name(self) -> None:
        gbun_exact = {"gcode": "Gcode", "gname": "Gname"}
        b_name = gbun_name_column(gbun_exact)
        b_code = gbun_code_column(gbun_exact)
        join = (
            f"LEFT JOIN G1_Gbun b ON g.Gubun=b.{b_code} "
            f"LEFT JOIN G1_Gbun b2 ON g.Gubun=b2.{b_name} "
        )
        self.assertIn("b.Gcode", join)
        self.assertIn("b2.Gname", join)
        expr = (
            f"COALESCE(NULLIF(b.{b_name},''),NULLIF(b2.{b_name},''),'') AS gbun_name"
        )
        self.assertNotIn("Sname", expr)

    def test_master_gbun_select_no_orphan_injection(self) -> None:
        src = (FRONT / "components" / "master" / "master-gbun-select.tsx").read_text(
            encoding="utf-8",
        )
        self.assertNotIn("hasCurrent", src)
        self.assertIn("gubunCode", src)
        self.assertIn("gbunName", src)

    def test_collapsible_on_detail_pages(self) -> None:
        for rel in (
            "app/(app)/master/customer/[gcode]/page.tsx",
            "app/(app)/master/customer/new/page.tsx",
        ):
            src = (FRONT / rel).read_text(encoding="utf-8")
            self.assertIn("CustomerCategoryCollapsible", src)
