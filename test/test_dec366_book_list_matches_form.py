"""DEC-366 — 도서관리 목록 컬럼 = 신규도서 등록 화면의 입력 칸 (같은 이름 · 같은 순서).

요청(2026-10-01 교문사, 캡처 2장 — 신규 도서 등록 화면 / 도서관리 컬럼 설정):
「신규도서 클릭하면 입력하는 컬럼과 도서관리 컬럼과 동일하게 요청」.

종전 차이: 이름(구분↔도서분류, 코드↔도서코드), 순서, 목록에 없는 입력 칸(인세종류 · 인세비율 · 전자책 ISBN/정가/비고),
그리고 목록 「도서종류」가 입력 화면의 도서종류(G4_Book_Ext.BookKind)가 아니라 옛 묶음(Gbjil)을 보여 주던 것.

사용자 결정(2026-10-01 질문 응답):
- 입력 화면에 없는 기존 목록 컬럼은 지우지 않고 **맨 뒤 선택 컬럼**으로 유지.
- 기본 표시는 DEC-336 의 16종 유지(순서만 입력 화면 순서).

이 가드는 두 소스(`book-detail-form.tsx` ↔ `master/book/page.tsx`)를 직접 대조한다 — 입력 화면에 칸을 넣고 빼면
목록도 같이 고쳐야 통과한다. 사용자 규칙: test 폴더에 저장.

DEC-412: 프론트 재설계(M-DEC-10·14·21) 운영 반영 — 입력 칸은 피그마 도서 폼(보이는 34칸)으로, 목록 컬럼은 그 34칸과
**같은 이름 · 같은 값 키**로 바뀌었다. 순서는 피그마 목록(도서명이 코드 뒤 · 재고 4칸은 맨 뒤 기본 숨김). M-DEC-21 이 입력 화면에
없는 선택 컬럼(도서종류(묶음) · 재고금액 · 도서타입 등)은 「DEC-412: 프론트 재설계 M-DEC-21 — 의도적 제거」 —
«맨 뒤 선택 컬럼» 가드는 «재고 4칸만 숨김» 으로 바꿨다.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

FORM = FRONT / "components" / "master" / "book-detail-form.tsx"
PAGE = FRONT / "app" / "(app)" / "master" / "book" / "page.tsx"

HIDDEN_MARKER = '<div hidden data-hidden-fields="figma-book">'

# 라벨 → (목록 컬럼 키, 폼이 쓰는 값 키). 도서 분류는 폼이 분류 이름(gbun_name)을 고르고 목록은 sname(서버가 분류명으로 채움, DEC-365).
EXPECT = {
    "도서명": ("gname", "gname"),
    "본사 정품": ("jego1", "jego1"), "본사 비품": ("jego2", "jego2"),
    "창고 정품": ("jego3", "jego3"), "창고 비품": ("jego4", "jego4"),
    "도서 분류": ("sname", "gbun_name"), "도서 코드": ("gcode", "gcode"), "저자명": ("gjeja", "gjeja"),
    "ISBN": ("gisbn", "gisbn"), "판형": ("name1", "name1"), "페이지수": ("gpage", "gpage"),
    "발행일": ("date1", "date1"), "등록일": ("date2", "date2"), "원가": ("price", "price"),
    "매입가": ("odang", "odang"), "정가": ("gdang", "gdang"), "전자책": ("bigo3", "bigo3"),
    "인세 종류": ("royalty_type", "royalty_type"), "인세율(%)": ("royalty_rate", "royalty_rate"),
    "인지 유무": ("stamp", "stamp"),
    "위탁": ("grat1", "grat1"), "현매": ("grat2", "grat2"), "매절": ("grat3", "grat3"), "납품": ("grat4", "grat4"),
    "특별": ("grat5", "grat5"), "한도": ("grat7", "grat7"), "기타": ("grat6", "grat6"), "신간수량": ("gqut1", "gqut1"),
    "등록번호": ("gnumb", "gnumb"), "서가 위치": ("gpost", "gpost"), "단위/묶음": ("gdabi", "gdabi"),
    "상태": ("grat9", "grat9"), "비고1": ("gbigo", "gbigo"), "비고2": ("etc_memo", "etc_memo"),
}


def _form_visible() -> str:
    src = FORM.read_text(encoding="utf-8").replace("\r\n", "\n")
    return src.split("export function BookDetailForm(", 1)[1].split(HIDDEN_MARKER, 1)[0]


def form_labels() -> list[str]:
    """입력 화면에 **보이는** 칸의 라벨(화면 순서). 조회/편집 삼항으로 두 번 나오는 칸은 한 번만."""
    out: list[str] = []
    for m in re.finditer(r'(?<![-\w])label="([^"]+)"|<Label>([^<]+)</Label>', _form_visible()):
        lbl = m.group(1) or m.group(2)
        if lbl not in out:
            out.append(lbl)
    return out


def list_columns() -> list[tuple[str, str]]:
    """목록 컬럼 (컬럼 id, 라벨)."""
    src = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = src.split("const columns: DataGridColumn<BookListItem>[] = [", 1)[1].split("\n  ];", 1)[0]
    found = []
    for m in re.finditer(r'key: "(\w+)",\s*(?:id: "(\w+)",\s*)?(?:sortKey: "\w+",\s*)?label: "([^"]+)"', body):
        found.append((m.group(2) or m.group(1), m.group(3)))
    return found


def default_hidden() -> set[str]:
    src = PAGE.read_text(encoding="utf-8")
    return set(re.findall(r'"(\w+)"', src.split("const BOOK_DEFAULT_HIDDEN = [", 1)[1].split("] as const", 1)[0]))


class ListMatchesFormTest(TestCase):
    def test_form_has_the_34_visible_cells(self) -> None:
        self.assertEqual(form_labels(), list(EXPECT))

    def test_list_columns_equal_form_labels(self) -> None:
        cols = list_columns()
        labels = [lbl for _id, lbl in cols]
        self.assertEqual(len(labels), len(set(labels)), "같은 이름 컬럼 중복")
        self.assertEqual(sorted(labels), sorted(form_labels()), "도서관리 컬럼(이름) = 도서 입력 칸")
        self.assertEqual(labels, [
            "도서 분류", "도서 코드", "도서명", "저자명", "ISBN", "판형", "페이지수", "발행일", "등록일",
            "원가", "매입가", "정가", "전자책", "인세 종류", "인세율(%)", "인지 유무",
            "위탁", "현매", "매절", "납품", "특별", "한도", "기타", "신간수량",
            "등록번호", "서가 위치", "단위/묶음", "상태", "비고1", "비고2",
            "본사 정품", "본사 비품", "창고 정품", "창고 비품",
        ], "피그마 도서 목록 순서")

    def test_each_list_column_reads_the_field_the_form_writes(self) -> None:
        """이름만 같고 다른 값을 보여 주면 안 된다(DEC-365 판형/정지사유 뒤바뀜 같은 사고)."""
        key_of = {lbl: cid for cid, lbl in list_columns()}
        self.assertEqual(key_of, {lbl: lk for lbl, (lk, _fk) in EXPECT.items()})
        visible = _form_visible()
        for lbl, (_lk, fk) in EXPECT.items():
            m = re.search(r'(?<![-\w])label="' + re.escape(lbl) + r'"|<Label>' + re.escape(lbl) + r'</Label>', visible)
            self.assertIsNotNone(m, lbl)
            chunk = visible[m.start():visible.index("/>", m.end())]
            self.assertTrue(f'onChange("{fk}"' in chunk or f"data.{fk}" in chunk, f"{lbl} 칸이 {fk} 를 읽고 쓰지 않는다")
        # 목록 「도서 분류」 = 서버가 채운 분류명(sname), 없으면 상세의 gbun_name.
        self.assertIn("cellText(row.sname || row.gbun_name)", PAGE.read_text(encoding="utf-8"))
        # 상태(출고/중지)의 편집 칸은 라벨 없는 드롭다운 — grat9 를 쓴다.
        self.assertIn('onChange={(next) => onChange("grat9", next === "1" ? CHECKED : "")}', visible)

    def test_stock_columns_at_the_end_and_hidden(self) -> None:
        """재고 4칸(읽기 전용)은 맨 뒤 · 기본 숨김. 그 밖의 컬럼은 모두 기본 표시."""
        cols = list_columns()
        self.assertEqual([cid for cid, _ in cols[-4:]], ["jego1", "jego2", "jego3", "jego4"])
        self.assertEqual(default_hidden(), {"jego1", "jego2", "jego3", "jego4"})

    def test_hidden_list_has_no_stale_keys(self) -> None:
        self.assertTrue(default_hidden() <= {cid for cid, _ in list_columns()}, "없는 컬럼 id 가 숨김 목록에 남았다")

    def test_prefs_key_bumped(self) -> None:
        """저장해 둔 컬럼 순서가 새 순서를 덮지 않게 키를 올린다(재설계 v7)."""
        self.assertIn('useGridPrefs(user?.server_id, "master.book.v7"', PAGE.read_text(encoding="utf-8"))


class EbookAttachTest(TestCase):
    """목록 행에 전자책 ISBN · 정가를 붙인다 — JOIN 없이(DEC-068), 회사 스코프로."""

    def setUp(self) -> None:
        import app.services.book_ebook_service as svc
        self.svc = svc

    def _run(self, items, rows=None, *, ensure=True, boom=False, hcode="5019"):
        seen: dict = {}

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            if boom:
                raise RuntimeError("db down")
            seen.update(sql=sql_template, keys=list(keys), prefix=tuple(prefix_params))
            return rows or []

        with patch.object(self.svc, "ensure_table", AsyncMock(return_value=ensure)), \
             patch.object(self.svc, "in_clause_lookup", fake_lookup):
            asyncio.run(self.svc.attach_ebook("remote_153", hcode, items))
        return seen

    def test_merges_by_code(self) -> None:
        items = [{"gcode": "3411"}, {"gcode": "90968"}]
        seen = self._run(items, [{"Gcode": "3411", "Eisbn": "9788936399999", "Eprice": 21000}])
        self.assertEqual(items[0]["eisbn"], "9788936399999")
        self.assertEqual(items[0]["eprice"], 21000)
        self.assertEqual((items[1]["eisbn"], items[1]["eprice"]), ("", 0))
        self.assertEqual(seen["keys"], ["3411", "90968"])

    def test_scoped_by_company_and_no_join(self) -> None:
        seen = self._run([{"gcode": "3411"}])
        self.assertIn("WHERE Hcode = %s AND Gcode IN ({placeholders})", seen["sql"])
        self.assertEqual(seen["prefix"], ("5019",))
        self.assertNotIn("JOIN", seen["sql"].upper())

    def test_failure_keeps_the_list(self) -> None:
        items = [{"gcode": "3411"}]
        self._run(items, boom=True)
        self.assertEqual((items[0]["eisbn"], items[0]["eprice"]), ("", 0))
        items = [{"gcode": "3411"}]
        self._run(items, ensure=False)
        self.assertEqual((items[0]["eisbn"], items[0]["eprice"]), ("", 0))

    def test_empty_page_does_not_query(self) -> None:
        self.assertEqual(self._run([]), {})

    def test_list_service_and_model_carry_the_fields(self) -> None:
        svc_src = (BACKEND / "app" / "services" / "masters_service.py").read_text(encoding="utf-8")
        self.assertIn("await book_ebook_service.attach_ebook(server_id, scope_hcode, items)", svc_src)
        from app.models.master import BookListItem
        item = BookListItem(gcode="1", gname="x", eisbn="978", eprice=1000)
        self.assertEqual((item.eisbn, item.eprice), ("978", 1000))
        self.assertEqual(BookListItem(gcode="1", gname="x").eprice, 0)


if __name__ == "__main__":
    main()
