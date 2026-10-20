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
        """DEC-412: 프론트 재설계(M-DEC-22) 운영 반영 — 분류 관리 패널(DBGrid201·Button201~203)은
        「도서구분」 화면(/master/book-category)에만 두고, 상세/신규는 드롭다운 안에서 분류를 추가한다.
        상세/신규 접이식 패널은 「DEC-412: 프론트 재설계 M-DEC-22 — 의도적 제거」."""
        list_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "page.tsx")
        self.assertNotIn("BookCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        form = _read(FRONT / "components" / "master" / "book-detail-form.tsx")
        self.assertIn("createCategory={masterApi.bookCategoryCreate}", form)
        cat_page = _read(FRONT / "app" / "(app)" / "master" / "book-category" / "page.tsx")
        self.assertIn("MasterCategoryCollapsible", cat_page)
        self.assertIn("<BookCategoryPanel", cat_page)

    def test_mapping_mentions_category_integration(self) -> None:
        text = _read(MAPPING)
        self.assertIn("MasterGbunSelect", text)
        self.assertIn("G4_Gbun", text)

    def test_list_search_filter_bar(self) -> None:
        """목록 검색 띠.

        DEC-412: 프론트 재설계(M-DEC-10·17) 운영 반영 — 필터 바(LocalComboField 구분 · 출고정지 제외 · 발행일 기간 ·
        초기화)는 피그마 검색 띠(`BookMasterListHeader`)로 바뀌었다. 구분 필터는 검색 기준 메뉴의 「도서 분류」
        하위 목록(서버 `gubun`), 초기화는 검색칸 X(`onClear`). 출고정지 제외 · 발행일 기간 필터 · 도서 검색 팝업(LookupButton)은
        「DEC-412: 프론트 재설계 M-DEC-10·17 — 의도적 제거」.
        """
        list_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "page.tsx")
        chrome = _read(FRONT / "components" / "master" / "book-master-chrome.tsx")
        self.assertIn("<BookMasterListHeader", list_src)
        self.assertIn("gubun: gubunV || undefined", list_src, "도서 분류 필터 → 서버 gubun")
        self.assertIn("onClear={() => {", list_src)
        self.assertIn('data-legacy-id="Sobo14.Filter.Gubun"', chrome)
        self.assertIn("onSelectCategory(cat)", chrome)
        # DEC-296(2026-09-22 사용자) — 도서처리 검색칸 제거(요청 파라미터·세션 키 포함).
        self.assertNotIn("f-jubun", list_src)
        self.assertNotIn("jubun", list_src.split("const columns")[0])

    def test_detail_delete_wiring(self) -> None:
        # DEC-412: 프론트 재설계 운영 반영 — 삭제는 공통 확인 팝업(ConfirmPrompt) 뒤에 실행.
        detail_src = _read(FRONT / "app" / "(app)" / "master" / "book" / "[gcode]" / "page.tsx")
        self.assertIn("onDelete={requestDelete}", detail_src)
        self.assertIn("onConfirm={confirmDelete}", detail_src)
        self.assertIn("masterApi.bookDelete", detail_src)
        form = _read(FRONT / "components" / "master" / "book-detail-form.tsx")
        self.assertIn('data-legacy-id="Sobo14.Button103"', form)
