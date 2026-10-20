from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services.g3_gjeo_adapt import g3_gbun_code_column, g3_gbun_name_column


class AuthorGbunResolveTests(TestCase):
    """get_author G3_Gbun 이중 조인 SQL 조각 회귀."""

    def test_dual_join_uses_code_and_name(self) -> None:
        gbun_exact = {"gcode": "Gcode", "gname": "Gname"}
        b_name = g3_gbun_name_column(gbun_exact)
        b_code = g3_gbun_code_column(gbun_exact)
        join = (
            f"LEFT JOIN G3_Gbun b ON g.Gubun=b.{b_code} "
            f"LEFT JOIN G3_Gbun b2 ON g.Gubun=b2.{b_name} "
        )
        self.assertIn("b.Gcode", join)
        self.assertIn("b2.Gname", join)
        expr = (
            f"COALESCE(NULLIF(b.{b_name},''),NULLIF(b2.{b_name},''),'') AS gbun_name"
        )
        self.assertNotIn("Sname", expr)

    def test_author_detail_uses_gbun_select(self) -> None:
        form = (FRONT / "components" / "master" / "author-detail-form.tsx").read_text(
            encoding="utf-8",
        )
        self.assertIn("MasterGbunSelect", form)
        self.assertIn("categoryList", form)
        self.assertIn("Sobo13.Edit101", form)
        self.assertNotIn('label="저자구분" value={data.gbun_name}', form)

    def test_collapsible_on_detail_not_list_tab(self) -> None:
        list_src = (FRONT / "app" / "(app)" / "master" / "author" / "page.tsx").read_text(
            encoding="utf-8",
        )
        self.assertNotIn("AuthorCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        # DEC-412: 프론트 재설계(M-DEC-9 · M-DEC-17) 운영 반영 — 목록 머리는 피그마 검색 한 칸(AuthorMasterListHeader).
        # 종전 저자구분 필터(LocalComboField · Sobo13.Filter.Gubun, DEC-119)는 시안에서 빠졌다.
        self.assertIn("<AuthorMasterListHeader", list_src)
        self.assertNotIn("Sobo13.Filter.Gubun", list_src)
        # DEC-412: 프론트 재설계 M-DEC-9 — 의도적 제거: 상세·신규 아래 저자구분 관리 패널(AuthorCategoryCollapsible).
        # 구분 추가는 M-DEC-22 드롭다운 안에서(allowCreate + authorApi.categoryCreate) 한다.
        form = (FRONT / "components" / "master" / "author-detail-form.tsx").read_text(encoding="utf-8")
        self.assertIn("allowCreate={fieldsEditable}", form)
        self.assertIn("createCategory={authorApi.categoryCreate}", form)
        self.assertIn("reloadKey={gbunReloadKey}", form)
        for rel in (
            "app/(app)/master/author/[gcode]/page.tsx",
            "app/(app)/master/author/new/page.tsx",
        ):
            src = (FRONT / rel).read_text(encoding="utf-8")
            self.assertIn("<AuthorDetailForm", src, rel)
