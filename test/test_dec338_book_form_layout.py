"""
DEC-338 — 신규도서등록(Sobo14 상세 폼) 줄 배치·숨김 칸·도서종류 목록·인세 필드(사용자 2026-09-28 캡처 2장).

- 줄 배치: 1 도서분류·도서종류·도서코드·인지유무·인세종류·인세비율 / 2 도서명·저자명·ISBN·정가·자료제공 /
  3 서가위치·판형·쪽수·판수·덩이·그램·발행일·등록일 / 4 재고·상태·정지사유·기타 / 5 비율 / 6 비고 / 8 전자책 ISBN·정가·비고.
- 삭제 요청 칸은 값 보존을 위해 숨김(hidden 블록) — 저장 시 원값 그대로 왕복, 레거시 위젯 id 유지.
- 도서종류 값은 Jubun(varchar(6)) 대신 G4_Book_Ext.BookKind 에 저장.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FORM = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "master" / "book-detail-form.tsx"
sys.path.insert(0, str(BACKEND))

from app.services import book_ext_service as bx  # noqa: E402

HIDDEN_LABELS = ("도서코드2", "비율구분", "등록번호", "도서종류(묶음)", "원가", "매입가",
                 "본사재고 정품", "본사재고 비품", "창고재고 정품", "창고재고 비품", "도서처리",
                 "단위", "세액유무", "재고절판")  # 뒤 3개 DEC-341


def _split(src: str) -> tuple[str, str]:
    body = src.split("export function BookDetailForm")[1].split("const SELECT_CLASS")[0]
    visible, hidden = body.split('<div hidden data-hidden-fields="DEC-338">')
    return visible, hidden.split("</div>")[0]


class FormLayout(TestCase):
    def setUp(self):
        self.src = FORM.read_text(encoding="utf-8")
        self.visible, self.hidden = _split(self.src)

    def test_visible_order(self):
        labels = re.findall(r'label="([^"]+)"|<Label>([^<]+)</Label>|<BookKindField', self.visible)
        flat = [a or b or "도서종류" for a, b in labels]
        expected = ["도서분류", "도서종류", "도서코드", "인지유무", "인세종류", "인세비율(%)",
                    "도서명", "저자명", "ISBN", "정가", "자료제공",
                    "서가위치", "판형", "쪽수", "판수", "덩이", "그램", "발행일", "등록일",
                    "재고", "출고정지", "상태", "정지사유", "기타",
                    "위탁", "현매", "매절", "납품", "특별", "한도", "기타(비율)",
                    "비고",
                    "전자책", "전자책 ISBN", "전자책 정가", "전자책 비고"]
        self.assertEqual(flat, expected)

    def test_deleted_fields_hidden_not_removed(self):
        for label in HIDDEN_LABELS:
            self.assertIn(f'label="{label}"', self.hidden, label)
            self.assertNotIn(f'label="{label}"', self.visible, label)
        self.assertIn("<BookTypeField", self.hidden)  # 도서타입
        for lid in ("Sobo14.Edit102", "Sobo14.Edit104", "Sobo14.Edit107", "Sobo14.Edit111", "Sobo14.Edit120",
                    "Sobo14.Edit130", "Sobo14.Edit131", "Sobo14.Edit133", "Sobo14.Edit301", "Sobo14.Edit304",
                    "Sobo14.Edit108", "Sobo14.CheckBox1", "Sobo14.CheckBox3"):
            self.assertIn(lid, self.src, lid)

    def test_row3_shelf_wide_dates_compact(self):
        """DEC-339 — 3열: 서가위치 2fr·짧은 칸 5.75rem 하한·날짜 13rem 고정 + 달력 버튼 아이콘 폭(data-compact-dates)."""
        row = self.visible.split('label="서가위치"')[0].rsplit("<div", 1)[1]
        self.assertIn("xl:grid-cols-[minmax(0,2fr)_repeat(5,minmax(5.75rem,1fr))_repeat(2,13rem)]", row)
        self.assertIn('data-compact-dates=""', row)
        css = (FORM.parents[2] / "app" / "globals.css").read_text(encoding="utf-8")
        rule = css.split("[data-form-grid][data-compact-dates]", 1)[1].split("}", 1)[0]
        self.assertIn("> [data-date-field] > button", rule)
        self.assertIn("width: 2rem !important", rule)
        # 공통 규칙(입력·버튼 100% !important)과 같은 @layer utilities 안이어야 특이도로 이긴다.
        self.assertGreater(css.index("[data-form-grid][data-compact-dates]"), css.index("@layer utilities"))

    def test_row2_ends_align_with_row1_and_stop_next_to_stock(self):
        """DEC-340 — 1열 6칸=2열 12칸의 2칸씩: 도서명 4(도서종류 끝)·저자명 2(도서코드 끝)·ISBN 2(인지유무 끝).
        ISBN 은 라벨 최소폭 해제+13px, NL 조회는 알약 suffix 가 아니라 상세 머리글. 출고정지는 재고 오른쪽."""
        row2 = self.visible.split("{/* 2열")[1].split("{/* 3열")[0]
        spans = re.findall(r'(?:label="([^"]+)"|<Label>([^<]+)</Label>)', row2)
        self.assertEqual([a or b for a, b in spans], ["도서명", "저자명", "ISBN", "정가", "자료제공"])
        self.assertIn('label="도서명"', row2.split("xl:col-span-4")[0])
        self.assertNotIn("xl:col-span-3", row2)
        self.assertIn("xl:col-span-2 [&_[data-slot=label]]:!min-w-0", row2)
        self.assertNotIn("isbnAction", self.src)
        self.assertNotIn("data-field-suffix", row2)
        page = (FORM.parents[2] / "app" / "(app)" / "master" / "book" / "[gcode]" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn('data-legacy-id="Sobo14.NL.LookupIsbn"', page.split("actions={", 1)[1].split("BookFormActions")[0])
        row4 = self.visible.split("{/* 4열")[1].split("</div>\n      </div>")[0]
        order = re.findall(r'label="([^"]+)"|<Label>([^<]+)</Label>', row4)
        self.assertEqual([a or b for a, b in order][:3], ["재고", "출고정지", "상태"])

    def test_book_kind_options(self):
        self.assertIn('"저서", "번역서-CP", "번역서-SP", "원서1팀", "원서2팀", "교과서", "단행본", "기타", "영상·기타", "파프리카·한승"', self.src)
        self.assertIn(">직접입력</option>", self.src)
        self.assertIn('onChange={(v) => onChange("book_kind", v)}', self.src)


class ExtColumns(IsolatedAsyncioTestCase):
    def setUp(self):
        bx.clear_ensured_for_tests()
        self.addCleanup(bx.clear_ensured_for_tests)

    async def _run(self, show_cols, alter_fails=False):
        calls: list[str] = []
        store: dict = {}

        async def fake_exec(server_id, sql, params=()):
            calls.append(sql)
            if sql.startswith("CREATE"):
                return []
            if sql.startswith("SHOW COLUMNS"):
                return [{"Field": c} for c in show_cols]
            if sql.startswith("ALTER"):
                if alter_fails:
                    raise RuntimeError("no ALTER privilege")
                return []
            if sql.startswith("SELECT"):
                return [store["row"]] if "row" in store else []
            if sql.startswith("REPLACE"):
                cols = sql.split("(", 1)[1].split(")", 1)[0].split(", ")
                store["row"] = dict(zip(cols, params))
                return []
            raise AssertionError(sql)

        old = bx.execute_query
        bx.execute_query = fake_exec
        try:
            await bx.upsert_ext(server_id="s", gcode="B1", scope_hcode="5019",
                                values={"book_kind": "번역서-CP", "royalty_type": "정률", "royalty_rate": "10",
                                        "ebook_memo": "메모", "supply": "PPT"})
            got = await bx.get_ext(server_id="s", gcode="B1", scope_hcode="5019")
        finally:
            bx.execute_query = old
        return calls, got

    async def test_old_table_gets_columns(self):
        calls, got = await self._run(["Hcode", "Gcode", "Status", "Supply", "EtcMemo", "Stamp"])
        self.assertEqual(sum(c.startswith("ALTER TABLE G4_Book_Ext ADD") for c in calls), 4)
        self.assertEqual((got["book_kind"], got["royalty_rate"], got["ebook_memo"], got["supply"]),
                         ("번역서-CP", "10", "메모", "PPT"))

    async def test_alter_failure_keeps_base_fields(self):
        _calls, got = await self._run(["Hcode", "Gcode", "Status", "Supply", "EtcMemo", "Stamp"], alter_fails=True)
        self.assertEqual(got["supply"], "PPT")      # 기존 칸은 계속 저장
        self.assertEqual(got["book_kind"], "")      # 새 칸은 조용히 생략(500 없음)

    def test_models(self):
        from app.models.master import BookDetail, BookUpdateRequest

        for m in (BookDetail, BookUpdateRequest):
            for k in ("book_kind", "royalty_type", "royalty_rate", "ebook_memo"):
                self.assertIn(k, m.model_fields, f"{m.__name__}.{k}")


if __name__ == "__main__":
    main(verbosity=2)
