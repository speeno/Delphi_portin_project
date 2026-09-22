"""DEC-292 — 거래처현황 목록 필드 구성 + 엑셀 전 필드 저장 + 지역 검색칸 제거 (2026-09-22).

사용자 요청: 필드표(지역, 구분, 정지, (코드), 거래처명, …, 비고2)에서 괄호(푸른색) 항목 = 기본 표시,
나머지(빨간색) = 컬럼 설정(필드 추가/숨김)으로 제어. 라벨은 줄일 수 있는 만큼 약식.
엑셀 저장은 화면 표시 여부와 무관하게 모든 필드. 거래처 검색 필터의 지역 입력칸 제거.
"""

from __future__ import annotations

import re
import sys
from io import BytesIO
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "master" / "customer" / "page.tsx"

from app.services import masters_excel as mx  # noqa: E402
from app.services.g1_ggeo_adapt import customer_detail_select_sql  # noqa: E402

# 사용자 필드표 순서 — (key, 라벨, 기본표시=괄호 항목)
SPEC: list[tuple[str, str, bool]] = [
    ("jubun", "지역", False), ("sname", "구분", False), ("grat9", "정지", False),
    ("gcode", "코드", True), ("gname", "거래처명", False), ("gnumb", "사업자등록번호", False),
    ("gposa", "대표자", False), ("gpost", "우편번호", True), ("gjuso", "주소", False),
    ("guper", "업태", True), ("gjomo", "종목", True), ("gssum", "한도액", False),
    ("gtel1", "전화", False), ("gfax1", "팩스", False), ("email", "E-mail", False),
    ("gphon", "핸드폰", False), ("grat1", "위탁", False), ("grat2", "현매", True),
    ("grat3", "매절", True), ("grat4", "납품", True), ("grat5", "특별", True),
    ("grat7", "한도", True), ("grat6", "기타", True), ("gqut1", "신간수량", True),
    ("pubun", "계산서", False), ("yesno", "발행유무", True), ("gpper", "담당자1", False),
    ("name2", "담당자2", False), ("gbigo", "비고1", False), ("name1", "비고2", False),
]
# 그리드 키 → 엑셀 카탈로그 키(합본 가상 키·구분명)
GRID_TO_CATALOG = {"gtel1": "gtel", "gfax1": "gfax", "sname": "gbun_name"}


def _src() -> str:
    return PAGE.read_text(encoding="utf-8")


def _grid_columns(src: str) -> list[tuple[str, str]]:
    body = src[src.index("const columns: DataGridColumn"): src.index("const visibleColumns")]
    return re.findall(r'\{\s*key: "(\w+)",\s*label: "([^"]+)"', body)


def _default_hidden(src: str) -> set[str]:
    m = re.search(r"const CUSTOMER_DEFAULT_HIDDEN = \[(.*?)\] as const;", src, re.DOTALL)
    assert m, "CUSTOMER_DEFAULT_HIDDEN 상수"
    return set(re.findall(r'"(\w+)"', m.group(1)))


class GridSpec(TestCase):
    def test_columns_order_and_short_labels(self) -> None:
        self.assertEqual(_grid_columns(_src()), [(k, lbl) for k, lbl, _ in SPEC])

    def test_default_visible_is_parenthesized_set(self) -> None:
        hidden = _default_hidden(_src())
        self.assertEqual(hidden, {k for k, _, shown in SPEC if not shown})
        visible = [k for k, _, _ in SPEC if k not in hidden]
        self.assertEqual(
            visible,
            ["gcode", "gpost", "guper", "gjomo", "grat2", "grat3", "grat4", "grat5",
             "grat7", "grat6", "gqut1", "yesno"],
        )

    def test_grid_prefs_key_v2_with_default_hidden(self) -> None:
        src = _src()
        # 구 저장분(hidden 집합)이 새 기본을 덮지 않도록 저장 키 버전업(DEC-151 선례).
        self.assertIn('useGridPrefs(user?.server_id, "master.customer.v2", {', src)
        self.assertIn("defaultHidden: CUSTOMER_DEFAULT_HIDDEN", src)


class ExportAllFields(TestCase):
    def test_every_grid_column_is_in_excel_with_same_label(self) -> None:
        catalog = {c["key"]: c["label"] for c in mx.customer_field_catalog()}
        for key, label in _grid_columns(_src()):
            ck = GRID_TO_CATALOG.get(key, key)
            self.assertIn(ck, catalog, f"{key} 엑셀 누락")
            self.assertEqual(catalog[ck], label, "엑셀 헤더 = 화면 라벨(DEC-234)")

    def test_catalog_order_follows_screen_then_extras(self) -> None:
        keys = [c["key"] for c in mx.customer_field_catalog()]
        screen = [GRID_TO_CATALOG.get(k, k) for k, _, _ in SPEC]
        self.assertEqual(keys[: len(screen)], screen)
        self.assertEqual(keys[len(screen):], ["ocode", "gadd1", "gadd2", "gnum1"])

    def test_export_ignores_screen_visibility(self) -> None:
        src = _src()
        body = src[src.index("async function exportXlsx"): src.index("function resetFilters")]
        self.assertNotIn("visibleColumns", body, "화면 표시 컬럼으로 엑셀 필드를 줄이지 않는다")
        self.assertNotIn("gridPrefs", body)
        # 필드 선택 기본값 = 카탈로그 전체.
        self.assertIn("setSelectedFields(new Set(res.fields.map((f) => f.key)))", src)

    def test_grat7_selected_for_export(self) -> None:
        sql = customer_detail_select_sql({"grat7"}, {"grat7": "Grat7"}, alias="g")
        self.assertIn("COALESCE(g.Grat7,0) AS grat7", sql)
        self.assertIn("0 AS grat7", customer_detail_select_sql(set(), {}, alias="g"))


class ImportCompat(TestCase):
    def _wb(self, headers: list[str], row: list) -> bytes:
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        ws.append(row)
        buf = BytesIO()
        wb.save(buf)
        return buf.getvalue()

    def _parse(self, data: bytes) -> dict:
        return mx.parse_master_xlsx(
            data,
            pk=mx.CUSTOMER_IMPORT_PK,
            pk_aliases=mx.CUSTOMER_IMPORT_PK_ALIASES,
            field_map=mx.CUSTOMER_IMPORT_MAP,
            numeric_keys=mx.CUSTOMER_NUMERIC_KEYS,
        )

    def test_new_template_round_trip(self) -> None:
        rows = [{"gcode": "A0001", "gname": "가", "jubun": "서울", "gtel1": "02", "gtel2": "737-6111",
                 "grat7": 5, "gadd1": "종로", "gadd2": "1층"}]
        data = mx.build_list_workbook(sheet_title="거래처", columns=mx.CUSTOMER_FULL_COLUMNS, rows=rows)
        parsed = self._parse(data)
        self.assertTrue(parsed["header_ok"], parsed["warnings"])
        payload = parsed["rows"][0]["payload"]
        self.assertEqual(parsed["rows"][0]["gcode"], "A0001")
        self.assertEqual(payload["jubun"], "서울")
        self.assertEqual(payload["gtel"], "02-737-6111")
        self.assertEqual((payload["gadd1"], payload["gadd2"]), ("종로", "1층"))
        # 엑셀 전용(읽기전용) 컬럼은 역반영하지 않는다.
        self.assertNotIn("grat7", payload)
        self.assertNotIn("gjuso", payload)

    def test_previous_template_headers_still_import(self) -> None:
        headers = ["거래처코드", "거래처명", "거래처구분", "거래처지역", "전화번호", "팩스번호",
                   "이메일", "핸드폰번호", "출고정지", "계산서구분"]
        data = self._wb(headers, ["A0002", "나", "일반서점", "부산", "051-123-4567", "",
                                  "a@b.c", "010-1-2", 1, "월말"])
        parsed = self._parse(data)
        self.assertTrue(parsed["header_ok"], parsed["warnings"])
        self.assertEqual(parsed["rows"][0]["gcode"], "A0002")
        p = parsed["rows"][0]["payload"]
        self.assertEqual(p["gbun_name"], "일반서점")
        self.assertEqual(p["jubun"], "부산")
        self.assertEqual(p["gtel"], "051-123-4567")
        self.assertEqual(p["email"], "a@b.c")
        self.assertEqual(p["gphon"], "010-1-2")
        self.assertEqual(p["grat9"], 1)
        self.assertEqual(p["pubun"], "월말")

    def test_missing_pk_reports_current_label(self) -> None:
        parsed = self._parse(self._wb(["거래처명"], ["가"]))
        self.assertFalse(parsed["header_ok"])
        self.assertIn("'코드'", parsed["warnings"][0])


if __name__ == "__main__":
    main()
