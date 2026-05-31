from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
MAPPING = ROOT / "analysis" / "layout_mappings" / "Sobo12.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Sobo12WidgetTraceability(TestCase):
    """Sobo12 매핑노트의 핵심 legacy id가 실제 DOM에 부착됐는지 확인."""

    def test_core_ids_exist_in_frontend(self) -> None:
        pages = [
            FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "new" / "page.tsx",
            FRONT / "components" / "master" / "inbound-vendor-detail-form.tsx",
            FRONT / "components" / "master" / "inbound-vendor-category-panel.tsx",
        ]
        merged = "\n".join(_read(p) for p in pages)
        for legacy_id in (
            "Sobo12.DBGrid101",
            "Sobo12.DBGrid201",
            "Sobo12.Edit101",
            "Sobo12.Edit103",
            "Sobo12.Edit116",
            "Sobo12.Edit124",
            "Sobo12.Edit130",
            "Sobo12.CheckBox1",
            "Sobo12.CheckBox2",
            "Sobo12.Button101",
            "Sobo12.Button102",
            "Sobo12.Button103",
            "Sobo12.Button201",
            "Sobo12.Button202",
            "Sobo12.Button203",
        ):
            self.assertIn(legacy_id, merged, legacy_id)

    def test_mapping_mentions_category_panel(self) -> None:
        text = _read(MAPPING)
        self.assertIn("DBGrid201", text)
        self.assertIn("Edit201/202", text)
        self.assertIn("입고처구분", text)

    def test_detail_uses_gbun_select(self) -> None:
        form = FRONT / "components" / "master" / "inbound-vendor-detail-form.tsx"
        self.assertIn("MasterGbunSelect", _read(form))
        self.assertIn("Sobo12.Edit101", _read(form))
        self.assertIn("inboundVendorApi.categoryList", _read(form))

    def test_category_panel_on_detail_not_list(self) -> None:
        list_page = FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "page.tsx"
        detail_page = FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "[gcode]" / "page.tsx"
        new_page = FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "new" / "page.tsx"
        list_src = _read(list_page)
        self.assertNotIn("InboundVendorCategoryCollapsible", list_src)
        self.assertNotIn("InboundVendorCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(detail_page)
        new_src = _read(new_page)
        self.assertIn("InboundVendorCategoryCollapsible", detail_src)
        self.assertIn("InboundVendorCategoryCollapsible", new_src)
        self.assertIn("onChanged", detail_src)
        self.assertIn("gbunReloadKey", detail_src)
