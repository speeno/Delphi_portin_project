from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
MAPPING = ROOT / "analysis" / "layout_mappings" / "Sobo13.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Sobo13WidgetTraceability(TestCase):
    """Sobo13 매핑노트의 핵심 legacy id가 실제 DOM에 부착됐는지 확인."""

    def test_core_ids_exist_in_frontend(self) -> None:
        pages = [
            FRONT / "app" / "(app)" / "master" / "author" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "author" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "author" / "new" / "page.tsx",
            FRONT / "components" / "master" / "author-detail-form.tsx",
            FRONT / "components" / "master" / "author-category-panel.tsx",
        ]
        merged = "\n".join(_read(p) for p in pages)
        for legacy_id in (
            "Sobo13.DBGrid101",
            "Sobo13.DBGrid201",
            "Sobo13.Edit101",
            "Sobo13.Edit103",
            "Sobo13.Edit104",
            "Sobo13.Edit121",
            "Sobo13.Button101",
            "Sobo13.Button102",
            "Sobo13.Button103",
            "Sobo13.Button201",
            "Sobo13.Button202",
            "Sobo13.Button203",
        ):
            self.assertIn(legacy_id, merged, legacy_id)

    def test_detail_uses_gbun_select(self) -> None:
        form = _read(FRONT / "components" / "master" / "author-detail-form.tsx")
        self.assertIn("MasterGbunSelect", form)
        self.assertIn("authorApi.categoryList", form)
        self.assertIn("Sobo13.Edit101", form)

    def test_category_panel_on_detail_not_list_tab(self) -> None:
        list_src = _read(FRONT / "app" / "(app)" / "master" / "author" / "page.tsx")
        self.assertNotIn("AuthorCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(FRONT / "app" / "(app)" / "master" / "author" / "[gcode]" / "page.tsx")
        new_src = _read(FRONT / "app" / "(app)" / "master" / "author" / "new" / "page.tsx")
        self.assertIn("AuthorCategoryCollapsible", detail_src)
        self.assertIn("AuthorCategoryCollapsible", new_src)
        self.assertIn("gbunReloadKey", detail_src)

    def test_list_search_filter_bar(self) -> None:
        list_src = _read(FRONT / "app" / "(app)" / "master" / "author" / "page.tsx")
        # 저자구분 필터는 DEC-119(2026-07-21)로 <select id="f-gubun"> → LocalComboField 전환.
        for kw in (
            "LocalComboField",
            'inputLegacyId="Sobo13.Filter.Gubun"',
            "f-workplace",
            "workplace",
            "resetFilters",
            "gbun_name",
        ):
            self.assertIn(kw, list_src, kw)

    def test_list_grid_extra_columns(self) -> None:
        list_src = _read(FRONT / "app" / "(app)" / "master" / "author" / "page.tsx")
        for legacy_id in (
            "Sobo13.DBGrid101.GNAME",
            "Sobo13.DBGrid101.GTELS",
            "Sobo13.DBGrid101.DATE1",
            "Sobo13.DBGrid101.GJICE",
        ):
            self.assertIn(legacy_id, list_src, legacy_id)

    def test_mapping_mentions_category_integration(self) -> None:
        text = _read(MAPPING)
        self.assertIn("MasterGbunSelect", text)
        self.assertIn("G3_Gbun", text)
        self.assertIn("3.1 목록 검색 필터", text)
