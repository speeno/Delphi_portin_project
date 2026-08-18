from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services.g4_book_adapt import g4_gbun_code_column, g4_gbun_name_column


class BookGbunResolveTests(TestCase):
    """get_book G4_Gbun 이중 조인 SQL 조각 회귀."""

    def test_dual_join_uses_code_and_name(self) -> None:
        gbun_exact = {"gcode": "Gcode", "gname": "Gname"}
        b_name = g4_gbun_name_column(gbun_exact)
        b_code = g4_gbun_code_column(gbun_exact)
        join = (
            f"LEFT JOIN G4_Gbun b ON g.Gubun=b.{b_code} "
            f"LEFT JOIN G4_Gbun b2 ON g.Gubun=b2.{b_name} "
        )
        self.assertIn("b.Gcode", join)
        self.assertIn("b2.Gname", join)
        expr = (
            f"COALESCE(NULLIF(b.{b_name},''),NULLIF(b2.{b_name},''),'') AS gbun_name"
        )
        self.assertNotIn("Sname", expr)

    def test_master_gbun_select_loader_prop(self) -> None:
        src = (FRONT / "components" / "master" / "master-gbun-select.tsx").read_text(
            encoding="utf-8",
        )
        self.assertIn("loader", src)
        self.assertIn("defaultLoader", src)
        self.assertNotIn("hasCurrent", src)

    def test_book_detail_uses_gbun_select(self) -> None:
        form = (FRONT / "components" / "master" / "book-detail-form.tsx").read_text(
            encoding="utf-8",
        )
        self.assertIn("MasterGbunSelect", form)
        self.assertIn("bookCategoryList", form)
        self.assertIn("Sobo14.Edit101", form)
        self.assertNotIn('label="도서분류" value={data.gbun_name}', form)

    def test_collapsible_on_detail_not_list_tab(self) -> None:
        list_src = (FRONT / "app/(app)/master/book/page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("BookCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        # 종전 `">도서분류<" 부재` 검사는 탭 UI 부재를 뜻했으나, DEC-151(2026-08-13) 이후
        # 목록 필터/컬럼 라벨 "도서분류" 가 정상적으로 존재하므로 탭 표식(setTab/Panel)만 본다.
        for rel in (
            "app/(app)/master/book/[gcode]/page.tsx",
            "app/(app)/master/book/new/page.tsx",
        ):
            src = (FRONT / rel).read_text(encoding="utf-8")
            self.assertIn("MasterCategoryCollapsible", src)
            self.assertIn("BookCategoryPanel", src)
            self.assertIn("gbunReloadKey", src)
            self.assertIn("onChanged", src)
