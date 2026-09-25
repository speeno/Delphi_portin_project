"""
DEC-336 — 도서관리: 검색 줄 통일 + 컬럼 재구성 + 확장 필드(상태·자료제공·기타·인지유무) + 엑셀 전 필드(사용자 2026-09-25).

사용자 결정(질문 응답): 상태 = 새 칸 + 기존 기록으로 초기값 / 자료제공 = 자유 입력 / 기타 = 새 메모칸 / 도서종류 = 기존 묶음(Gbjil).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services import book_ext_service as bx  # noqa: E402


class StatusDerivation(TestCase):
    def test_from_legacy_records(self):
        self.assertEqual(bx.derive_status(name2="절판->개정판 나옴"), "절판")
        self.assertEqual(bx.derive_status(name2="재고 없음"), "일시품절")
        self.assertEqual(bx.derive_status(jubun="품절"), "품절")
        self.assertEqual(bx.derive_status(bigo2="1"), "절판")
        self.assertEqual(bx.derive_status(name2="구판", jubun="신간"), "정상")

    def test_saved_status_wins(self):
        item = {"status": "품절", "name2": "절판"}
        bx.apply_status_default(item)
        self.assertEqual(item["status"], "품절")


class ExtStore(IsolatedAsyncioTestCase):
    def setUp(self):
        bx.clear_ensured_for_tests()
        self.addCleanup(bx.clear_ensured_for_tests)

    async def test_partial_upsert_and_attach(self):
        store: dict[tuple[str, str], dict] = {}

        async def fake_exec(server_id, sql, params=()):
            if sql.startswith("CREATE"):
                return []
            if sql.startswith("SELECT"):
                r = store.get((params[0], params[1]))
                return [r] if r else []
            if sql.startswith("REPLACE"):
                h, g, st, su, em, sp = params
                store[(h, g)] = {"Gcode": g, "Status": st, "Supply": su, "EtcMemo": em, "Stamp": sp}
                return []
            if sql.startswith("DELETE"):
                store.pop((params[0], params[1]), None)
                return []
            raise AssertionError(sql)

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            self.assertIn("Hcode = %s", sql_template)
            return [r for (h, g), r in store.items() if h == prefix_params[0] and g in keys]

        old = (bx.execute_query, bx.in_clause_lookup)
        bx.execute_query, bx.in_clause_lookup = fake_exec, fake_lookup
        try:
            await bx.upsert_ext(server_id="s", gcode="B1", scope_hcode="5019", values={"supply": "PPT"})
            await bx.upsert_ext(server_id="s", gcode="B1", scope_hcode="5019", values={"status": "품절", "stamp": "true"})
            got = await bx.get_ext(server_id="s", gcode="B1", scope_hcode="5019")
            self.assertEqual(got, {"status": "품절", "supply": "PPT", "etc_memo": "", "stamp": "1"})  # 부분 갱신 보존
            items = [{"gcode": "B1", "name2": "절판"}, {"gcode": "B2", "name2": "재고없음"}]
            await bx.attach_ext("s", "5019", items)
            self.assertEqual((items[0]["status"], items[0]["supply"]), ("품절", "PPT"))
            self.assertEqual((items[1]["status"], items[1]["supply"]), ("일시품절", ""))  # 추정값, DB 무기록
            self.assertNotIn(("5019", "B2"), store)
            with self.assertRaises(ValueError):
                await bx.upsert_ext(server_id="s", gcode="B1", scope_hcode="5019", values={"status": "단종"})
        finally:
            bx.execute_query, bx.in_clause_lookup = old


class ExcelAndModels(TestCase):
    def test_excel_all_fields(self):
        from app.services import masters_excel as mx

        headers = [h for h, _ in mx.BOOK_COLUMNS]
        for h in ("전자책", "상태", "자료제공", "기타메모", "인지유무", "도서종류", "기타(비율)"):
            self.assertIn(h, headers)
        self.assertNotIn("묶음", headers)
        self.assertEqual(mx.BOOK_IMPORT_MAP["도서종류"], "gbjil")
        self.assertEqual(mx.BOOK_IMPORT_MAP["기타"], "grat6")          # 종전 파일 하위호환
        self.assertEqual(mx.BOOK_IMPORT_MAP["기타(비율)"], "grat6")
        self.assertNotIn("기타메모", mx.BOOK_IMPORT_MAP)               # 확장 필드는 가져오기 대상 아님

    def test_models_carry_ext(self):
        from app.models.master import BookDetail, BookListItem, BookUpdateRequest

        for m in (BookListItem, BookDetail, BookUpdateRequest):
            for k in ("status", "supply", "etc_memo", "stamp"):
                self.assertIn(k, m.model_fields, f"{m.__name__}.{k}")
        self.assertIn("bigo3", BookListItem.model_fields)


class Screens(TestCase):
    def test_list_columns_and_search(self):
        src = (FE / "app" / "(app)" / "master" / "book" / "page.tsx").read_text(encoding="utf-8")
        body = src.split("const columns: DataGridColumn<BookListItem>[] = [")[1].split("// ── 이하 선택 컬럼")[0]
        labels = re.findall(r'label: "([^"]+)"', body)
        self.assertEqual(labels, ["구분", "코드", "전자책", "도서명", "저자명", "ISBN", "정가", "재고", "서가위치",
                                  "위탁", "발행일", "상태", "정지사유", "자료제공", "기타", "비고"])
        self.assertIn('useGridPrefs(user?.server_id, "master.book.v3"', src)
        self.assertIn('<AttachedFilterField\n                  label="검색"', src.replace("\r\n", "\n"))
        self.assertIn('placeholder="코드, 도서명, ISBN"', src)

    def test_detail_form_fields(self):
        src = (FE / "components" / "master" / "book-detail-form.tsx").read_text(encoding="utf-8")
        for token in ('label="도서종류"', "<Label>상태</Label>", 'label="자료제공"', 'label="기타"',
                      'label="인지유무"', 'label="기타(비율)"', 'const BOOK_STATUS_OPTIONS = ["정상", "일시품절", "품절", "절판"]'):
            self.assertIn(token, src)
        self.assertNotIn('label="묶음"', src)


if __name__ == "__main__":
    main(verbosity=2)
