"""DEC-294 — 입고처관리 목록 필드 구성 + 엑셀 전 필드(기본 전체 선택) + 신규 입고처 위치 (2026-09-22).

사용자 요청: 거래처현황(DEC-292)과 같은 필드표 — 괄호(푸른색) 항목 = 기본 표시, 나머지 = 컬럼 설정.
엑셀은 모든 필드(기본 전체 선택). 신규입고처 버튼은 검색 입력 앞.
입고처는 E-mail·담당자2 칸이 G2_Ggwo 에 없어 확장 테이블(G2_Ggwo_Ext email2/manager2)에서 병합한다.

DEC-412: 프론트 재설계(M-DEC-7) 운영 반영 — 목록 = 피그마(1:425) 15칸(피그마 라벨) 전부 표시.
DEC-294 의 나머지 16칸(정지·우편번호·한도액·공급률·한도·신간수량·계산서·발행유무·담당자2·비고2·정지사유)과
헤더 클릭 정렬은 의도적 제거(M-DEC-7, 서버 정렬은 gcode 오름차순 고정). 엑셀은 그대로 전 필드 · 약식 헤더
(업로드 서식 호환) — 화면 라벨이 바뀐 피그마 칸은 SCREEN_TO_EXCEL 로 대응을 고정한다.
신규 버튼은 제목 옆 「신규 등록」(검색 띠 앞).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PAGE = FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "page.tsx"
CUST_PAGE = FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx"

from app.services import inbound_vendor_ext_service as ext  # noqa: E402
from app.services import masters_excel as mx  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

# (key, 화면 라벨) — 피그마 1:425
SPEC: list[tuple[str, str]] = [
    ("jubun", "지역"), ("gcode", "입고처 코드"), ("gname", "입고처명"),
    ("gnumb", "사업자번호"), ("gposa", "대표자"), ("gtel1", "전화번호"),
    ("gfax1", "팩스"), ("gphon", "핸드폰 번호"), ("email2", "이메일"),
    ("gbun_name", "입고처 구분"), ("guper", "업태"), ("gjomo", "종목"),
    ("gpper", "담당자"), ("gjuso", "주소"), ("gbigo", "비고"),
]
# DEC-294 칸 중 목록에서 의도적 제거(M-DEC-7) — 엑셀(전 필드)에는 남는다.
REMOVED_FROM_LIST = ("grat9", "gpost", "gssum", "grat1", "grat2", "grat3", "grat4", "grat5",
                     "grat7", "grat6", "gqut1", "name2", "yesno", "manager2", "name1", "email")
# 피그마 라벨 ↔ 엑셀 헤더(masters_excel.INBOUND_VENDOR_FULL_COLUMNS — 업로드 서식이라 바꾸지 않는다).
SCREEN_TO_EXCEL = {
    "입고처 코드": "코드", "사업자번호": "사업자등록번호", "전화번호": "전화", "핸드폰 번호": "핸드폰",
    "이메일": "E-mail", "입고처 구분": "구분", "담당자": "담당자1", "비고": "비고1",
}
GRID_TO_CATALOG = {"gtel1": "gtel", "gfax1": "gfax"}


def _src(p: Path = PAGE) -> str:
    return p.read_text(encoding="utf-8")


def _grid_columns(src: str) -> list[tuple[str, str]]:
    body = src[src.index("const columns: DataGridColumn"): src.index("const visibleColumns")]
    return re.findall(r'\{\s*key: "(\w+)",\s*label: "([^"]+)"', body)


class GridSpec(TestCase):
    def test_columns_order_and_short_labels(self) -> None:
        self.assertEqual(_grid_columns(_src()), SPEC)

    def test_default_visible_is_parenthesized_set(self) -> None:
        # 피그마 15칸 전부 기본 표시(숨김 기본값 없음). 제거된 DEC-294 칸은 컬럼 정의에도 없다.
        self.assertIn('useGridPrefs(user?.server_id, "master.inbound_vendor.v3", {', _src())
        self.assertIn("defaultHidden: [],", _src())
        self.assertNotIn("INBOUND_VENDOR_DEFAULT_HIDDEN", _src())
        keys = {k for k, _ in _grid_columns(_src())}
        for k in REMOVED_FROM_LIST:
            self.assertNotIn(k, keys, f"{k}: DEC-412 의도적 제거(M-DEC-7)")

    def test_no_header_sort(self) -> None:
        # DEC-412: 헤더 클릭 정렬 의도적 제거(M-DEC-7) — 목록·엑셀 모두 gcode 오름차순 고정.
        src = _src()
        self.assertNotIn("sortable: true", src)
        self.assertNotIn("onSortChange", src)
        self.assertEqual(src.count('sortBy: "gcode",'), 2, "목록 + 엑셀")

    def test_new_button_before_search(self) -> None:
        # 피그마 헤더: 제목 · 「신규 등록」(Button101) → 검색 기준 · 검색어 · 조회. 지역 입력칸 없음(DEC-335).
        chrome = (FRONT / "components" / "master" / "inbound-vendor-master-chrome.tsx").read_text(encoding="utf-8")
        btn = chrome.index('data-legacy-id="Sobo12.Button101"')
        self.assertLess(chrome.index("입고처 관리</h1>"), btn)
        self.assertLess(btn, chrome.index("<MasterSearchQueryField"), "검색 입력 앞")
        self.assertIn('router.push("/master/inbound-vendor/new")', chrome)
        self.assertIn("<InboundVendorMasterListHeader", _src())
        self.assertNotIn('id="f-jubun"', _src())


class ExportAllFields(TestCase):
    def test_every_grid_column_in_excel_with_same_label(self) -> None:
        catalog = {c["key"]: c["label"] for c in mx.inbound_vendor_field_catalog()}
        for key, label in _grid_columns(_src()):
            ck = GRID_TO_CATALOG.get(key, key)
            self.assertIn(ck, catalog, f"{key} 엑셀 누락")
            self.assertEqual(catalog[ck], SCREEN_TO_EXCEL.get(label, label), f"{key}: 엑셀 헤더 ↔ 화면 라벨 대응")

    def test_picker_resets_to_all_fields_on_open(self) -> None:
        # 「엑셀 저장 시 기본적으로 모든 필드 선택」 — 열 때마다 카탈로그 전체로 재설정(공용 ExportFieldPicker).
        picker = (FRONT / "components" / "master" / "export-field-picker.tsx").read_text(encoding="utf-8")
        self.assertIn("if (!open) selectAll();", picker)
        for p in (PAGE, CUST_PAGE):
            src = _src(p)
            self.assertIn("<ExportFieldPicker", src, p.name)
            body = src[src.index("async function exportXlsx"):]
            body = body[: body.index("\n  }\n")]
            self.assertNotIn("visibleColumns", body, "화면 표시 컬럼으로 줄이지 않는다")

    def test_ext_keys_are_export_only(self) -> None:
        for k in ("email2", "manager2", "gjuso"):
            self.assertNotIn(k, mx.INBOUND_VENDOR_IMPORT_MAP.values())
        self.assertEqual(mx.INBOUND_VENDOR_IMPORT_MAP["입고처구분"], "gbun_name", "구 양식 헤더 수용")


class ExtMerge(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ext._ensured.add("remote_x")
        self.addCleanup(ext._ensured.discard, "remote_x")

    async def test_bulk_get_binds_hcode_and_chunks(self) -> None:
        lookup = AsyncMock(return_value=[{"gcode": "I1", "email2": "a@b.c", "manager2": "김담당"}])
        with patch.object(ext, "in_clause_lookup", lookup):
            got = await ext.get_ext_many(server_id="remote_x", gcodes=["I1", "I2", "I1", ""], scope_hcode="5019",
                                         keys=("email2", "manager2"))
        self.assertEqual(got, {"I1": {"email2": "a@b.c", "manager2": "김담당"}})
        kw = lookup.await_args.kwargs
        self.assertEqual(kw["prefix_params"], ("5019",), "hcode 격리")
        self.assertEqual(kw["keys"], ["I1", "I2"], "중복·빈값 제거")
        self.assertIn("WHERE Hcode=%s AND Gcode IN ({placeholders})", kw["sql_template"])

    async def test_bulk_get_failure_is_empty(self) -> None:
        with patch.object(ext, "in_clause_lookup", AsyncMock(side_effect=RuntimeError("db down"))):
            self.assertEqual(await ext.get_ext_many(server_id="remote_x", gcodes=["I1"], scope_hcode="5019"), {})

    async def test_list_merges_email2_manager2(self) -> None:
        rows = [{"gcode": "I1", "gname": "가"}, {"gcode": "I2", "gname": "나"}]

        async def fake_exec(server_id, sql, params=()):
            if "COUNT(*)" in sql:
                return [{"row_count": 2}]
            return rows

        bulk = AsyncMock(return_value={"I1": {"email2": "a@b.c", "manager2": "김담당"}})
        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(ms, "g2_ggwo_column_meta", AsyncMock(return_value=(set(), {}))), \
                patch.object(ms, "_g2_gbun_code_name_map", AsyncMock(return_value={})), \
                patch.object(ms.inbound_vendor_ext_service, "get_ext_many", bulk):
            res = await ms.list_inbound_vendors(server_id="remote_x", scope_hcode="5019")
        by = {it["gcode"]: it for it in res["items"]}
        self.assertEqual((by["I1"]["email2"], by["I1"]["manager2"]), ("a@b.c", "김담당"))
        self.assertEqual((by["I2"]["email2"], by["I2"]["manager2"]), ("", ""))
        self.assertEqual(bulk.await_args.kwargs["scope_hcode"], "5019")


if __name__ == "__main__":
    main()
