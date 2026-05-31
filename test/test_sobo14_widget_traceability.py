from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
MAPPING = ROOT / "analysis" / "layout_mappings" / "Sobo14.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Sobo14WidgetTraceability(TestCase):
    """Sobo14 매핑노트의 핵심 legacy id가 실제 DOM에 부착됐는지 확인."""

    def test_core_ids_exist_in_frontend(self) -> None:
        pages = [
            FRONT / "app" / "(app)" / "master" / "book" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "book" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "book" / "new" / "page.tsx",
            FRONT / "components" / "master" / "book-detail-form.tsx",
            FRONT / "components" / "master" / "book-category-panel.tsx",
        ]
        merged = "\n".join(_read(p) for p in pages)
        for legacy_id in (
            "Sobo14.DBGrid101",
            "Sobo14.DBGrid201",
            "Sobo14.Edit101",
            "Sobo14.Edit103",
            "Sobo14.Edit105",
            "Sobo14.Edit110",
            "Sobo14.CheckBox1",
            "Sobo14.CheckBox2",
            "Sobo14.Button101",
            "Sobo14.Button102",
            "Sobo14.Button103",
            "Sobo14.Button201",
            "Sobo14.Button202",
            "Sobo14.Button203",
        ):
            self.assertIn(legacy_id, merged, legacy_id)

    def test_detail_uses_gbun_select(self) -> None:
        form = _read(FRONT / "components" / "master" / "book-detail-form.tsx")
        self.assertIn("MasterGbunSelect", form)
        self.assertIn("bookCategoryList", form)
        self.assertIn("Sobo14.Edit101", form)

    def test_category_panel_on_detail_not_list_tab(self) -> None:
        list_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "page.tsx")
        self.assertNotIn("BookCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "[gcode]" / "page.tsx")
        new_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "new" / "page.tsx")
        self.assertIn("MasterCategoryCollapsible", detail_src)
        self.assertIn("MasterCategoryCollapsible", new_src)
        self.assertIn("onChanged", detail_src)
        self.assertIn("gbunReloadKey", detail_src)

    def test_mapping_mentions_category_integration(self) -> None:
        text = _read(MAPPING)
        self.assertIn("MasterGbunSelect", text)
        self.assertIn("G4_Gbun", text)

    def test_list_search_filter_bar(self) -> None:
        """목록 검색 필터 확장(minimal): 구분 select·처리 input·출고정지 제외 체크."""
        list_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "page.tsx")
        for kw in (
            "f-gubun",
            "f-jubun",
            "f-exship",
            "excludeShippingStop",
            "resetFilters",
        ):
            self.assertIn(kw, list_src, kw)

    def test_detail_delete_wiring(self) -> None:
        detail_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "[gcode]" / "page.tsx")
        self.assertIn("onDelete={handleDelete}", detail_src)
        self.assertIn("masterApi.bookDelete", detail_src)
