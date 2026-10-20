"""
DEC-338 — 신규도서등록(Sobo14 상세 폼) 줄 배치·숨김 칸·도서종류 목록·인세 필드(사용자 2026-09-28 캡처 2장).

- 줄 배치: 1 도서분류·도서종류·도서코드·인지유무·인세종류·인세비율 / 2 도서명·저자명·ISBN·정가·자료제공 /
  3 서가위치·판형·쪽수·판수·덩이·그램·발행일·등록일 / 4 재고·상태·정지사유·기타 / 5 비율 / 6 비고 / 8 전자책 ISBN·정가·비고.
- 삭제 요청 칸은 값 보존을 위해 숨김(hidden 블록) — 저장 시 원값 그대로 왕복, 레거시 위젯 id 유지.
- 도서종류 값은 Jubun(varchar(6)) 대신 G4_Book_Ext.BookKind 에 저장.

DEC-412: 프론트 재설계(M-DEC-10·12·14, 피그마 33:10317/10531/10752) 운영 반영 — 줄 배치는 피그마로 바뀌었다:
  머리 줄 도서명 + 재고 4칸(읽기 전용) / 4열 격자 도서 분류·도서 코드·저자명·ISBN·판형·페이지수·발행일·등록일·원가·매입가·정가·전자책·
  인세 종류·인세율(%)·인지 유무 / 거래 조건 줄(위탁~기타·신간수량) / 등록번호·서가 위치·단위/묶음·상태 / 비고1·비고2.
  피그마에 없는 칸은 숨김 블록(`data-hidden-fields="figma-book"`)에서 값 왕복 — DEC-338 의 «지우지 않고 숨김» 원칙은 그대로.
  DEC-339(3열 폭)·DEC-340(2열 끝맞춤 · NL 조회 머리글)은 「DEC-412: 프론트 재설계 M-DEC-10·12 — 의도적 제거」(가드 삭제).
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

# 피그마에 없는 칸 — 숨김 블록에서 값을 그대로 왕복한다(레거시 위젯 id 유지).
HIDDEN_LABELS = ("자료제공", "판수", "그램", "재고", "정지사유", "전자책 ISBN", "전자책 정가", "전자책 비고",
                 "세액유무", "재고절판", "도서처리", "도서코드2", "비율구분", "도서종류(묶음)")
# 숨김 칸의 값 키 — 상세 저장(PATCH) · 신규 등록 payload 가 모두 실어 보내야 원값이 유지된다.
HIDDEN_KEYS = ("book_kind", "supply", "gpan1", "gqut2", "status", "name2", "eisbn", "eprice", "ebook_memo",
               "bigo1", "bigo2", "jubun", "scode", "ocode", "pubun", "gbjil")
PAGES = FORM.parents[2] / "app" / "(app)" / "master" / "book"


def _split(src: str) -> tuple[str, str]:
    body = src.split("export function BookDetailForm")[1].split("function ratioShown(")[0]
    visible, hidden = body.split('<div hidden data-hidden-fields="figma-book">')
    return visible, hidden.split("<ReadOnlyBanner")[0]


def _labels(chunk: str) -> list[str]:
    """화면 순서 라벨 — 조회/편집 삼항으로 같은 칸이 두 번 나오면 한 번만."""
    out: list[str] = []
    for a, b in re.findall(r'(?<![-\w])label="([^"]+)"|<Label>([^<]+)</Label>', chunk):
        lbl = a or b
        if lbl not in out:
            out.append(lbl)
    return out


class FormLayout(TestCase):
    def setUp(self):
        self.src = FORM.read_text(encoding="utf-8")
        self.visible, self.hidden = _split(self.src)

    def test_visible_order(self):
        self.assertEqual(_labels(self.visible), [
            "도서명", "본사 정품", "본사 비품", "창고 정품", "창고 비품",
            "도서 분류", "도서 코드", "저자명", "ISBN", "판형", "페이지수", "발행일", "등록일",
            "원가", "매입가", "정가", "전자책", "인세 종류", "인세율(%)", "인지 유무",
            "위탁", "현매", "매절", "납품", "특별", "한도", "기타", "신간수량",
            "등록번호", "서가 위치", "단위/묶음", "상태",
            "비고1", "비고2",
        ])

    def test_deleted_fields_hidden_not_removed(self):
        for label in HIDDEN_LABELS:
            self.assertIn(f'label="{label}"', self.hidden, label)
            self.assertNotIn(f'label="{label}"', self.visible, label)
        self.assertIn("<BookTypeField", self.hidden)  # 도서타입
        self.assertIn("<BookKindField", self.hidden)  # 도서종류(G4_Book_Ext.BookKind)
        self.assertIn("<Label>품절 상태</Label>", self.hidden)  # 상태 4종(G4_Book_Ext.Status)
        # 도서타입(Edit107) · 도서종류(Ext.BookKind) 위젯 id 는 각 하위 컴포넌트 정의부에 있다.
        for lid in ("Sobo14.Edit107", "Sobo14.Ext.BookKind"):
            self.assertIn(lid, self.src, lid)
        for lid in ("Sobo14.Edit102", "Sobo14.Edit104", "Sobo14.Edit111", "Sobo14.Edit112",
                    "Sobo14.Edit125", "Sobo14.Edit127", "Sobo14.Edit129", "Sobo14.Edit133",
                    "Sobo14.CheckBox1", "Sobo14.CheckBox3", "Sobo14.Ext.Status", "Sobo14.Ext.Supply"):
            self.assertIn(lid, self.hidden, lid)
        for lid in ("Sobo14.Edit120", "Sobo14.Edit130", "Sobo14.Edit131", "Sobo14.Edit301", "Sobo14.Edit304",
                    "Sobo14.Edit108"):
            self.assertIn(lid, self.visible, lid)

    def test_hidden_values_round_trip_on_save(self):
        """숨긴 칸도 저장 payload 에 실린다 — 빠지면 상세 저장 때 원값이 지워지거나 신규 등록에서 사라진다."""
        detail = (PAGES / "[gcode]" / "page.tsx").read_text(encoding="utf-8")
        body = detail.split("const body: BookUpdatePayload = {", 1)[1].split("};", 1)[0]
        create = (PAGES / "new" / "page.tsx").read_text(encoding="utf-8")
        create_body = create.split("await masterApi.bookCreate({", 1)[1].split("});", 1)[0]
        for key in HIDDEN_KEYS:
            self.assertRegex(body, rf"\b{key}:", f"상세 저장 {key}")
            self.assertRegex(create_body, rf"\b{key}:", f"신규 등록 {key}")

    def test_title_row_has_read_only_stock(self):
        """머리 줄 = 도서명 + 재고 4칸(본사/창고 정품·비품). 재고는 시스템 산정이라 입력칸이 아니다."""
        head = self.visible.split('<div className="my-5 border-t border-form-divider" />', 1)[0]
        self.assertIn('legacyId="Sobo14.Edit105"', head)
        for lid in ("Sobo14.Edit301", "Sobo14.Edit302", "Sobo14.Edit303", "Sobo14.Edit304"):
            self.assertIn(f'legacyId="{lid}"', head)
        stock = self.src.split("function StockBox(", 1)[1].split("\n}\n", 1)[0]
        self.assertNotIn("<Input", stock)

    def test_trade_terms_row(self):
        """거래 조건 줄 — 비율 7칸 + 신간수량(Gqut1). 레거시 위젯 id 순서 그대로."""
        row = self.visible.split('data-legacy-id="Sobo14.PanelTrade"', 1)[1].split("</section>", 1)[0]
        self.assertEqual(re.findall(r'label="([^"]+)"', row), ["위탁", "현매", "매절", "납품", "특별", "한도", "기타", "신간수량"])
        self.assertEqual(re.findall(r'legacyId="(Sobo14\.Edit\d+)"', row), [
            "Sobo14.Edit113", "Sobo14.Edit114", "Sobo14.Edit115", "Sobo14.Edit116", "Sobo14.Edit117",
            "Sobo14.Edit132", "Sobo14.Edit118", "Sobo14.Edit126",
        ])
        for key in ("grat1", "grat2", "grat3", "grat4", "grat5", "grat7", "grat6", "gqut1"):
            self.assertIn(f'onChange("{key}", v)', row, key)

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
