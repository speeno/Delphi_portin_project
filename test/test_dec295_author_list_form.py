"""DEC-295 — 저자관리 목록 필드 구성 + 엑셀 전 필드 + 저자도서명·비고2 신설 + 등록 폼 4열 배치 (2026-09-22).

사용자 요청: 필드표(코드, 저자구분, 저자명, 소속대학, 학과, 저자도서명(기록칸 여유), (은행), (계좌번호), (주민번호),
(사업자등록번호), (원천징수), 이메일, 전화번호, (우편번호), 자택주소, 연구소주소, 담당자1, 담당자2, 비고1, 비고2, 등록일자)
— 괄호 = 기본 표시, 나머지 선택. 엑셀은 모든 필드가 기본. 신규 저자 버튼은 검색 앞. 저자등록 화면 배치 효율화.

DEC-412: 프론트 재설계(M-DEC-9 · M-DEC-27) 운영 반영 — 목록 컬럼·라벨·순서는 피그마 시안(「컬럼 = 신규 등록 폼 항목」,
전 컬럼 기본 표시, 저장 키 v5)을 따른다. 의도적 제거(M-DEC-9): 필드표 인세 항목(은행·원천징수·사업자등록번호·
담당자2)·저자도서명·우편번호 컬럼, 헤더 클릭 정렬(서버 정렬은 코드 오름차순 고정). 폼에서는 숨은 칸(data-hidden-fields)으로
값만 유지한다. 엑셀(백엔드 카탈로그)은 종전 필드표 전 필드·이름 그대로라, 화면 라벨과 같은지 대신 「목록의 모든 컬럼이
엑셀 카탈로그에 있다」를 본다.
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

# DEC-412 — 피그마 시안 컬럼(폼 칸 순서). 소속대학·학과 = 직장명(gname)·소속/직책(gjice) 칸(DEC-335).
SPEC: list[tuple[str, str]] = [
    ("gbun_name", "저자 구분"), ("gcode", "저자 코드"), ("gposa", "저자명"), ("date1", "등록일자"),
    ("gname", "직장명"), ("gjice", "소속/직책"), ("gscho", "출신학교"), ("gnum1", "주민번호"),
    ("gnum2", "계좌번호"), ("gtel2", "휴대전화"), ("gfax1", "팩스번호"), ("email", "이메일"),
    ("gadd1", "집 주소"), ("manager1", "담당"), ("oadd1", "직장 주소"), ("gbigo", "비고1"), ("bigo2", "비고2"),
]
# 화면 컬럼 → 엑셀 카탈로그 키(합본 전화·팩스·주소).
GRID_TO_CATALOG = {"gtel2": "gtel", "gfax1": "gfax", "gadd1": "home_addr", "oadd1": "lab_addr"}


def _grid_columns(src: str) -> list[tuple[str, str]]:
    body = src[src.index("const columns: DataGridColumn"): src.index("const visibleColumns")]
    return re.findall(r'\{\s*key: "(\w+)",\s*label: "([^"]+)"', body)


class ListSpec(TestCase):
    def test_columns_and_default_visible(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        self.assertEqual(_grid_columns(src), SPEC)
        # 피그마 — 전 컬럼 기본 표시(숨김은 컬럼 설정에서 사용자가 고른다).
        self.assertIn('useGridPrefs(user?.server_id, "master.author.v5", {\n    defaultHidden: [],', src)
        # 의도적 제거(M-DEC-9) — 헤더 클릭 정렬. 목록·엑셀 모두 코드 오름차순.
        self.assertEqual(src.count('sortBy: "gcode",\n'), 2, "목록 · 엑셀")

    def test_new_button_before_search_and_picker(self) -> None:
        # DEC-412 — 신규 등록 버튼은 피그마 머리(AuthorMasterListHeader) 제목 옆, 검색칸보다 앞.
        chrome = (FRONT / "components" / "master" / "author-master-chrome.tsx").read_text(encoding="utf-8")
        head = chrome[chrome.index("export function AuthorMasterListHeader"):]
        btn = head.index('data-legacy-id="Sobo13.Button101"')
        self.assertLess(btn, head.index("<MasterSearchQueryField"), "검색 입력 앞")
        src = PAGE.read_text(encoding="utf-8")
        self.assertIn("<AuthorMasterListHeader", src)
        self.assertIn("loadFields={authorApi.exportFields}", src)

    def test_every_grid_column_in_excel_with_same_label(self) -> None:
        # DEC-412 — 라벨은 피그마(화면) · 필드표(엑셀)로 갈렸다. 목록에 보이는 값은 모두 엑셀로 내려받을 수 있어야 한다.
        catalog = {c["key"] for c in mx.author_field_catalog()}
        for key, _label in _grid_columns(PAGE.read_text(encoding="utf-8")):
            self.assertIn(GRID_TO_CATALOG.get(key, key), catalog, f"{key} 엑셀 카탈로그에 있음")

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
        # DEC-412 — 피그마 시트: 4열 FORM_GRID, 주소는 3칸(lg:col-span-3) + 담당/비고1.
        self.assertIn("<div className={FORM_GRID} data-form-grid=\"\">", src)
        self.assertEqual(src.count("<AddressGroup"), 2, "자택·연구소 주소 한 줄")
        self.assertNotIn("lg:col-span-2", src, "종전 불균등 칸 제거")
        self.assertIn('onChange("bigo2", e.target.value)', src)
        # 의도적 제거(M-DEC-9) — 저자도서명·은행·원천징수·사업자등록번호·담당자2 는 숨은 칸에서 값만 유지.
        hidden = src[src.index('<div hidden data-hidden-fields="figma-author">'):]
        hidden = hidden[: hidden.index("</div>")]
        for frag in ('onChange("books", v)', 'onChange("bank_name", v)', 'onChange("withhold", v)',
                     'onChange("gnumb", v)', 'onChange("manager2", v)', 'legacyId="Sobo13.Edit107"'):
            self.assertIn(frag, hidden, frag)
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
