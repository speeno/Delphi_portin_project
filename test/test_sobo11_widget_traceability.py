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
        # DEC-412: 프론트 재설계 운영 반영 — 실제로 렌더되는 파일만 본다. 「신규 등록」은 공용 헤더,
        # 지점 관리는 팝업(M-DEC-4), 구분 수정 · 삭제 패널은 단독 「거래처구분」 화면(customer-category).
        pages = [
            FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx",
            FRONT / "app" / "(app)" / "master" / "customer" / "new" / "page.tsx",
            FRONT / "components" / "master" / "customer-detail-form.tsx",
            FRONT / "components" / "master" / "customer-master-list-header.tsx",
            FRONT / "components" / "master" / "customer-category-panel.tsx",
            FRONT / "components" / "master" / "customer-branch-dialog.tsx",
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
            "Sobo11.Button007",
            "Seok10.DBGrid101",
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
        """거래처구분 CRUD 는 목록 탭에 없다. DEC-412: 프론트 재설계 M-DEC-22 · M-DEC-4 — 의도적 제거(접이식 패널) —
        상세/신규는 구분 드롭다운에서 바로 추가(allowCreate), 수정 · 삭제는 단독 「거래처구분」 화면,
        지점은 상세 「지점 관리」 팝업."""
        list_page = FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx"
        detail_page = FRONT / "app" / "(app)" / "master" / "customer" / "[gcode]" / "page.tsx"
        new_page = FRONT / "app" / "(app)" / "master" / "customer" / "new" / "page.tsx"
        list_src = _read(list_page)
        self.assertNotIn("CustomerCategoryCollapsible", list_src)
        self.assertNotIn("CustomerCategoryPanel", list_src)
        self.assertNotIn("setTab(", list_src)
        detail_src = _read(detail_page)
        new_src = _read(new_page)
        for src in (detail_src, new_src):
            self.assertIn("<CustomerDetailForm", src)
            self.assertIn("gbunReloadKey", src)
        self.assertIn("allowCreate={fieldsEditable}", _read(FRONT / "components" / "master" / "customer-detail-form.tsx"))
        self.assertIn("<CustomerBranchDialog", detail_src)
        self.assertIn(
            "<CustomerCategoryCollapsible",
            _read(FRONT / "app" / "(app)" / "master" / "customer-category" / "page.tsx"),
        )

    def test_gbun_select_uses_master_list_only(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-gbun-select.tsx")
        self.assertNotIn("hasCurrent", src)
        self.assertIn("customerCategoryList", src)

    def test_list_search_filter_bar(self) -> None:
        """목록 검색 필터(minimal): 구분 · 출고 정지 제외 체크 · 검색어 지우기 (지역 input 은 DEC-292 로 제거).

        DEC-412: 프론트 재설계 M-DEC-1 · M-DEC-17 — 의도적 제거(LocalComboField · 초기화 버튼 · 돋보기 검색 팝업):
        구분 필터는 검색칸 왼쪽
        「검색 기준」 메뉴의 「거래처 구분」 하위 목록, 초기화 버튼 대신 검색칸 X(onClear), 돋보기 검색 팝업 삭제.
        """
        list_src = _read(
            FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx"
        )
        header = _read(FRONT / "components" / "master" / "customer-master-list-header.tsx")
        for kw in ('aria-label="거래처 구분"', 'excludeCheckboxId = "f-exterm"', "onExcludeTerminatedChange", "onClear"):
            self.assertIn(kw, header, kw)
        for kw in (
            "customerCategoryList",
            "gubun: gubunV || undefined",
            "excludeTerminated: exTerm || undefined",
            "onClear={() => {",
        ):
            self.assertIn(kw, list_src, kw)
        # DEC-292(2026-09-22 사용자) — 지역 검색 입력은 불필요: 입력칸·요청 파라미터 모두 제거.
        self.assertNotIn("f-jubun", list_src)
        self.assertNotIn("jubun:", list_src.split("const columns")[0])
