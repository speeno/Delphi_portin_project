from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
MAPPING = ROOT / "analysis" / "layout_mappings" / "Sobo15.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Sobo15WidgetTraceability(TestCase):
    def test_core_ids_exist_in_frontend(self) -> None:
        pages = [
            FRONT / "app" / "(app)" / "master" / "etc-customer" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "etc-customer" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "etc-customer" / "new" / "page.tsx",
            FRONT / "components" / "master" / "etc-customer-detail-form.tsx",
            FRONT / "components" / "master" / "etc-customer-category-panel.tsx",
        ]
        merged = "\n".join(_read(p) for p in pages)
        for legacy_id in (
            "Sobo15.DBGrid101",
            "Sobo15.DBGrid201",
            "Sobo15.Edit101",
            "Sobo15.Edit103",
            "Sobo15.Edit116",
            "Sobo15.Edit124",
            "Sobo15.CheckBox1",
            "Sobo15.Button101",
            "Sobo15.Button102",
            "Sobo15.Button103",
            "Sobo15.Button201",
            "Sobo15.Button202",
            "Sobo15.Button203",
        ):
            self.assertIn(legacy_id, merged, legacy_id)

    def test_detail_uses_gbun_select(self) -> None:
        form = _read(FRONT / "components" / "master" / "etc-customer-detail-form.tsx")
        self.assertIn("MasterGbunSelect", form)
        self.assertIn("Sobo15.Edit101", form)
        self.assertIn("etcCustomerApi.categoryList", form)

    def test_category_panel_on_detail_not_list(self) -> None:
        list_page = FRONT / "app" / "(app)" / "master" / "etc-customer" / "page.tsx"
        detail_page = FRONT / "app" / "(app)" / "master" / "etc-customer" / "[gcode]" / "page.tsx"
        new_page = FRONT / "app" / "(app)" / "master" / "etc-customer" / "new" / "page.tsx"
        list_src = _read(list_page)
        self.assertNotIn("EtcCustomerCategoryCollapsible", list_src)
        self.assertNotIn("EtcCustomerCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(detail_page)
        new_src = _read(new_page)
        self.assertIn("EtcCustomerCategoryCollapsible", detail_src)
        self.assertIn("EtcCustomerCategoryCollapsible", new_src)
        self.assertIn("gbunReloadKey", detail_src)
