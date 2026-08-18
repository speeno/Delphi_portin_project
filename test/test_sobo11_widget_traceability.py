from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
MAPPING = ROOT / "analysis" / "layout_mappings" / "Sobo11.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Sobo11WidgetTraceability(TestCase):
    """Sobo11 매핑노트의 핵심 legacy id가 실제 DOM에 부착됐는지 확인."""

    def test_core_ids_exist_in_frontend(self) -> None:
        pages = [
            FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "customer" / "new" / "page.tsx",
            FRONT / "components" / "master" / "customer-detail-form.tsx",
            FRONT / "components" / "master" / "customer-category-panel.tsx",
            FRONT / "components" / "master" / "customer-branch-panel.tsx",
            FRONT / "components" / "master" / "customer-branch-collapsible.tsx",
        ]
        merged = "\n".join(_read(p) for p in pages)
        for legacy_id in (
            "Sobo11.DBGrid101",
            "Sobo11.DBGrid201",
            "Sobo11.Edit101",
            "Sobo11.Edit103",
            "Sobo11.Edit116",
            "Sobo11.Edit124",
            "Sobo11.Edit130",
            "Sobo11.CheckBox1",
            "Sobo11.CheckBox2",
            "Sobo11.Button101",
            "Sobo11.Button102",
            "Sobo11.Button103",
            "Sobo11.Button201",
            "Sobo11.Button202",
            "Sobo11.Button203",
        ):
            self.assertIn(legacy_id, merged, legacy_id)

    def test_mapping_mentions_category_panel(self) -> None:
        text = _read(MAPPING)
        self.assertIn("DBGrid201", text)
        self.assertIn("Edit201/202", text)
        self.assertIn("거래처구분", text)

    def test_detail_uses_gbun_select(self) -> None:
        """상세 폼 거래처구분(Edit101)이 자유 텍스트가 아닌 G1_Gbun 목록 선택이어야 함."""
        select = FRONT / "components" / "master" / "master-gbun-select.tsx"
        form = FRONT / "components" / "master" / "customer-detail-form.tsx"
        self.assertTrue(select.exists(), select)
        self.assertIn("customerCategoryList", _read(select))
        form_text = _read(form)
        self.assertIn("MasterGbunSelect", form_text)
        self.assertIn("Sobo11.Edit101", form_text)

    def test_category_panel_on_detail_not_list_tab(self) -> None:
        """거래처구분 CRUD는 상세/신규에만 있고 목록 탭에는 없어야 함."""
        list_page = FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx"
        detail_page = FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx"
        new_page = FRONT / "app" / "(app)" / "master" / "customer" / "new" / "page.tsx"
        list_src = _read(list_page)
        self.assertNotIn("CustomerCategoryCollapsible", list_src)
        self.assertNotIn("CustomerCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(detail_page)
        new_src = _read(new_page)
        self.assertIn("CustomerCategoryCollapsible", detail_src)
        self.assertIn("CustomerCategoryCollapsible", new_src)
        self.assertIn("CustomerBranchCollapsible", detail_src)
        self.assertIn("CustomerBranchCollapsible", new_src)
        self.assertIn("onChanged", detail_src)
        self.assertIn("gbunReloadKey", detail_src)
        self.assertIn("CustomerCategoryCollapsible", detail_src)

    def test_gbun_select_uses_master_list_only(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-gbun-select.tsx")
        self.assertNotIn("hasCurrent", src)
        self.assertIn("customerCategoryList", src)

    def test_list_search_filter_bar(self) -> None:
        """목록 검색 필터 확장(minimal): 구분 select·지역 input·거래종료 제외 체크."""
        list_src = _read(
            FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx"
        )
        # 거래처구분 필터는 DEC-119(2026-07-21)로 네이티브 <select id="f-gubun"> →
        # LocalComboField(픽 필드, data-legacy-id 는 내부 input 에 보존) 로 전환됨.
        for kw in (
            "LocalComboField",
            'inputLegacyId="Sobo11.Filter.Gubun"',
            "f-jubun",
            "f-exterm",
            "excludeTerminated",
            "resetFilters",
        ):
            self.assertIn(kw, list_src, kw)
