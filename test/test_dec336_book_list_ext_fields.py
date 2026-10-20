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
            self.assertEqual(got, {"status": "품절", "supply": "PPT", "etc_memo": "", "stamp": "1",  # 부분 갱신 보존
                                   "royalty_type": "", "royalty_rate": "", "ebook_memo": "", "book_kind": ""})  # DEC-338 칸
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
        """DEC-412: 프론트 재설계(M-DEC-10·14·21) 운영 반영 — 목록 기본 컬럼은 피그마 도서 목록(등록 폼에 보이는 칸),
        재고 4칸만 기본 숨김. 등록 폼에 없는 칸(자료제공 · 품절 상태 · 정지사유 · 재고 합계 등) 컬럼과 발행일 기간 필터는
        「DEC-412: 프론트 재설계 M-DEC-10·21 — 의도적 제거」.
        확장 필드 중 인지 유무 · 인세 · 비고2(기타 메모)는 목록에 남는다. 검색 줄 = 피그마 검색 띠(발행일 기간 필터 없음)."""
        src = (FE / "app" / "(app)" / "master" / "book" / "page.tsx").read_text(encoding="utf-8")
        body = src.split("const columns: DataGridColumn<BookListItem>[] = [")[1].split("\n  ];")[0]
        hidden = set(re.findall(r'"(\w+)"', src.split("const BOOK_DEFAULT_HIDDEN = [")[1].split("] as const")[0]))
        cols = re.findall(r'key: "(\w+)",\s*label: "([^"]+)"', body)
        shown = [lbl for key, lbl in cols if key not in hidden]
        self.assertEqual(shown, ["도서 분류", "도서 코드", "도서명", "저자명", "ISBN", "판형", "페이지수", "발행일", "등록일",
                                 "원가", "매입가", "정가", "전자책", "인세 종류", "인세율(%)", "인지 유무",
                                 "위탁", "현매", "매절", "납품", "특별", "한도", "기타", "신간수량",
                                 "등록번호", "서가 위치", "단위/묶음", "상태", "비고1", "비고2"])
        self.assertEqual(hidden, {"jego1", "jego2", "jego3", "jego4"})
        keys = dict(cols)
        for k in ("bigo3", "stamp", "etc_memo", "royalty_type", "royalty_rate"):
            self.assertIn(k, keys, k)
        self.assertIn('useGridPrefs(user?.server_id, "master.book.v7"', src)
        self.assertIn("<BookMasterListHeader", src)
        chrome = (FE / "components" / "master" / "book-master-chrome.tsx").read_text(encoding="utf-8")
        self.assertIn('{ id: "isbn", label: "ISBN", placeholder: "ISBN을 입력하세요" }', chrome)

    def test_detail_form_fields(self):
        """DEC-412: 프론트 재설계(M-DEC-12·14) 운영 반영 — 보이는 칸: 인지 유무(유/무) · 인세 · 비율 「기타」(grat6) ·
        비고2(= 기타 메모 etc_memo). 피그마에 없는 확장 칸(도서종류 · 자료제공 · 품절 상태)은 숨김 블록에서 값 왕복."""
        src = (FE / "components" / "master" / "book-detail-form.tsx").read_text(encoding="utf-8")
        visible, hidden = src.split("export function BookDetailForm(")[1].split('<div hidden data-hidden-fields="figma-book">')
        hidden = hidden.split("<ReadOnlyBanner")[0]
        for token in ('label="인지 유무"', 'legacyId="Sobo14.Ext.Stamp"', 'label="인세 종류"', '<Label>비고2</Label>',
                      'data-legacy-id="Sobo14.Ext.EtcMemo"', 'onChange={(v) => onChange("grat6", v)}'):
            self.assertIn(token, visible, token)
        for token in ("<BookKindField", 'label="자료제공"', "<Label>품절 상태</Label>", 'data-legacy-id="Sobo14.Ext.Status"'):
            self.assertIn(token, hidden, token)
        self.assertIn('const BOOK_STATUS_OPTIONS = ["정상", "일시품절", "품절", "절판"]', src)
        self.assertNotIn('label="묶음"', src)

if __name__ == "__main__":
    main(verbosity=2)
