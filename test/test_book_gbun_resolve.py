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
        """DEC-412: 프론트 재설계(M-DEC-22) 운영 반영 — 상세/신규의 도서분류 접이식 관리 패널은 없어지고,
        분류 추가는 도서 분류 드롭다운 안(「카테고리 넣기」)에서 한다. 수정·삭제는 별도 「도서구분」 화면
        (/master/book-category, BookCategoryPanel) 그대로. 상세/신규 접이식 패널은 「DEC-412: 프론트 재설계 M-DEC-22 — 의도적 제거」.
        목록에 탭 UI 가 되살아나지 않는지는 종전대로 본다."""
        list_src = (FRONT / "app/(app)/master/book/page.tsx").read_text(encoding="utf-8")
        self.assertNotIn("BookCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        form = (FRONT / "components" / "master" / "book-detail-form.tsx").read_text(encoding="utf-8")
        self.assertIn("allowCreate={fieldsEditable}", form)
        self.assertIn("createCategory={masterApi.bookCategoryCreate}", form)
        cat_page = (FRONT / "app/(app)/master/book-category/page.tsx").read_text(encoding="utf-8")
        self.assertIn("MasterCategoryCollapsible", cat_page)
        self.assertIn("<BookCategoryPanel", cat_page)
