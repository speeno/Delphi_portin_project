"""DEC-295 — 저자관리 목록 필드 구성 + 엑셀 전 필드 + 저자도서명·비고2 신설 + 등록 폼 4열 배치 (2026-09-22).

사용자 요청: 필드표(코드, 저자구분, 저자명, 소속대학, 학과, 저자도서명(기록칸 여유), (은행), (계좌번호), (주민번호),
(사업자등록번호), (원천징수), 이메일, 전화번호, (우편번호), 자택주소, 연구소주소, 담당자1, 담당자2, 비고1, 비고2, 등록일자)
— 괄호 = 기본 표시, 나머지 선택. 엑셀은 모든 필드가 기본. 신규 저자 버튼은 검색 앞. 저자등록 화면 배치 효율화.
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
PAGE = FRONT / "app" / "(app)" / "master" / "author" / "page.tsx"
FORM = FRONT / "components" / "master" / "author-detail-form.tsx"

from app.services import author_ext_service as ax  # noqa: E402
from app.services import masters_excel as mx  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

SPEC: list[tuple[str, str, bool]] = [
    ("gcode", "코드", False), ("gbun_name", "저자구분", False), ("gposa", "저자명", False),
    # DEC-335 — 소속대학·학과 = 레거시 직장명(gname)·직책(gjice) 칸.
    ("gname", "소속대학", False), ("gjice", "학과", False), ("books", "저자도서명", False),
    ("bank_name", "은행", True), ("gnum2", "계좌번호", True), ("gnum1", "주민번호", True),
    ("gnumb", "사업자등록번호", True), ("withhold", "원천징수", True), ("email", "이메일", False),
    ("gtel1", "전화번호", False), ("gpost", "우편번호", True), ("gadd1", "자택주소", False),
    ("oadd1", "연구소주소", False), ("manager1", "담당자1", False), ("manager2", "담당자2", False),
    ("gbigo", "비고1", False), ("bigo2", "비고2", False), ("date1", "등록일자", False),
    # 종전 목록 컬럼(필드표 밖) — 기본 숨김 유지
    ("gfax1", "연락처2", False), ("gscho", "출신학교", False),
]
GRID_TO_CATALOG = {"gtel1": "gtel", "gfax1": "gfax", "gadd1": "home_addr", "oadd1": "lab_addr"}


def _grid_columns(src: str) -> list[tuple[str, str]]:
    body = src[src.index("const columns: DataGridColumn"): src.index("const visibleColumns")]
    return re.findall(r'\{\s*key: "(\w+)",\s*label: "([^"]+)"', body)


class ListSpec(TestCase):
    def test_columns_and_default_visible(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        self.assertEqual(_grid_columns(src), [(k, lbl) for k, lbl, _ in SPEC])
        m = re.search(r"const AUTHOR_DEFAULT_HIDDEN = \[(.*?)\] as const;", src, re.DOTALL)
        self.assertEqual(set(re.findall(r'"(\w+)"', m.group(1))), {k for k, _, shown in SPEC if not shown})
        self.assertIn('useGridPrefs(user?.server_id, "master.author.v2", {', src)

    def test_new_button_before_search_and_picker(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        band_start = src.index("              >\n", src.index("actions={"))
        btn = src.index('data-legacy-id="Sobo13.Button101"')
        self.assertLess(band_start, btn, "필터 띠 안")
        self.assertLess(btn, src.index('<Label htmlFor="q">'), "검색 입력 앞")
        self.assertIn("loadFields={authorApi.exportFields}", src)

    def test_every_grid_column_in_excel_with_same_label(self) -> None:
        catalog = {c["key"]: c["label"] for c in mx.author_field_catalog()}
        for key, label in _grid_columns(PAGE.read_text(encoding="utf-8")):
            ck = GRID_TO_CATALOG.get(key, key)
            self.assertEqual(catalog.get(ck), label, f"{key} 엑셀 헤더 = 화면 라벨")

    def test_excel_subset_keeps_pk_and_import_covers_legacy_columns(self) -> None:
        self.assertEqual([h for h, _ in mx.select_author_columns(["books", "gposa"])], ["코드", "저자명", "저자도서명"])
        self.assertEqual(len(mx.select_author_columns(None)), 28)  # DEC-335 — 웹 학과(dept) 제외
        for h in ("저자명", "저자구분", "직장명", "등록일자", "직책"):  # 종전 5헤더 유지(DEC-335 가져오기 별칭)
            self.assertIn(h, mx.AUTHOR_IMPORT_MAP)
        self.assertEqual(mx.AUTHOR_IMPORT_MAP["전화번호"], "gtel")
        for k in ("books", "bigo2", "dept", "home_addr"):
            self.assertNotIn(k, mx.AUTHOR_IMPORT_MAP.values(), f"{k} 엑셀 전용")


class ExtTable(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ax.clear_ensured_for_tests()
        self.addCleanup(ax.clear_ensured_for_tests)

    async def test_existing_table_gets_new_columns(self) -> None:
        calls: list[str] = []

        async def fake(server_id, sql, params=()):
            calls.append(sql)
            if sql.startswith("SHOW COLUMNS"):
                return [{"Field": c} for c in ("Hcode", "Gcode", "Dept", "Manager1", "Manager2", "Withhold", "BankName", "Email")]
            return []

        with patch.object(ax, "execute_query", fake):
            self.assertTrue(await ax.ensure_table("remote_x"))
        alters = [c for c in calls if c.startswith("ALTER TABLE")]
        self.assertEqual(alters, ["ALTER TABLE G3_Gjeo_Ext ADD COLUMN Books TEXT",
                                  "ALTER TABLE G3_Gjeo_Ext ADD COLUMN Bigo2 VARCHAR(200) NOT NULL DEFAULT ''"])
        self.assertIn(("books", "Books"), ax._fields_for("remote_x"))

    async def test_alter_failure_keeps_base_fields_working(self) -> None:
        async def fake(server_id, sql, params=()):
            if sql.startswith("SHOW COLUMNS"):
                return [{"Field": "Hcode"}]
            if sql.startswith("ALTER"):
                raise RuntimeError("ALTER command denied")
            return []

        with patch.object(ax, "execute_query", fake):
            self.assertTrue(await ax.ensure_table("remote_x"))
        keys = [k for k, _ in ax._fields_for("remote_x")]
        self.assertNotIn("books", keys)
        self.assertIn("bank_name", keys)

    async def test_bulk_get_binds_hcode(self) -> None:
        ax._ensured.add("remote_x")
        ax._available["remote_x"] = ax._FIELDS
        lookup = AsyncMock(return_value=[{"gcode": "A1", "books": "식품학개론", "bank_name": "국민"}])
        with patch.object(ax, "in_clause_lookup", lookup):
            got = await ax.get_ext_many(server_id="remote_x", gcodes=["A1", "A1", "A2"], scope_hcode="5019")
        self.assertEqual(got["A1"]["books"], "식품학개론")
        self.assertEqual(got["A1"]["bigo2"], "", "빠진 키는 빈값")
        kw = lookup.await_args.kwargs
        self.assertEqual(kw["prefix_params"], ("5019",))
        self.assertEqual(kw["keys"], ["A1", "A2"])

    async def test_list_merges_ext_fields(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            return [{"gcode": "A1", "gposa": "홍길동", "gnum2": "123-45"}]

        bulk = AsyncMock(return_value={"A1": {**ax.EMPTY_EXT, "books": "식품학개론", "withhold": "3.3%"}})
        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(ms, "g3_gjeo_column_meta", AsyncMock(return_value=({"gcode", "gposa", "gnum2"}, {"gcode": "Gcode", "gposa": "Gposa", "gnum2": "Gnum2"}))), \
                patch.object(ms, "g3_gbun_column_meta", AsyncMock(return_value=(set(), {}))), \
                patch.object(ms.author_ext_service, "get_ext_many", bulk):
            res = await ms.list_authors(server_id="remote_x", scope_hcode="5019")
        it = res["items"][0]
        self.assertEqual((it["gnum2"], it["books"], it["withhold"]), ("123-45", "식품학개론", "3.3%"))
        self.assertEqual(bulk.await_args.kwargs["scope_hcode"], "5019")


class FormLayout(TestCase):
    def test_form_uses_shared_grid_and_new_fields(self) -> None:
        src = FORM.read_text(encoding="utf-8")
        self.assertIn('from "@/components/master/form-grid";', src)
        self.assertIn("className={`${FORM_GRID} ", src)
        self.assertEqual(src.count("<AddressGroup"), 2, "자택·연구소 주소 한 줄")
        self.assertNotIn("lg:col-span-2", src, "종전 불균등 칸 제거")
        self.assertIn('onChange("books", e.target.value)', src)
        self.assertIn('className="col-span-full space-y-1"', src, "저자도서명 전폭 기록칸")
        self.assertIn('onChange("bigo2", v)', src)
        for lid in ("Sobo13.Edit101", "Sobo13.Edit102", "Sobo13.Edit103", "Sobo13.Edit104", "Sobo13.Edit105",
                    "Sobo13.Edit106", "Sobo13.Edit107", "Sobo13.Edit108", "Sobo13.Edit109", "Sobo13.Edit110",
                    "Sobo13.Edit111", "Sobo13.Edit113", "Sobo13.Edit115", "Sobo13.Edit116", "Sobo13.Edit117",
                    "Sobo13.Edit118", "Sobo13.Edit119", "Sobo13.Edit120", "Sobo13.Edit121"):
            self.assertIn(lid, src, f"{lid} 레거시 위젯 보존")

    def test_pages_send_new_fields(self) -> None:
        for sub in ("new", "[gcode]"):
            src = (PAGE.parent / sub / "page.tsx").read_text(encoding="utf-8")
            self.assertIn("books: data.books", src, sub)
            self.assertIn("bigo2: data.bigo2", src, sub)


if __name__ == "__main__":
    main()
