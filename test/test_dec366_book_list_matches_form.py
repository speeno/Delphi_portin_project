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

EXTRAS_MARKER = "// ── 이하 입력 화면에 없는 선택 컬럼"


def form_labels() -> list[str]:
    """입력 화면에 **보이는** 칸의 라벨(화면 순서). 숨김 칸(`data-hidden-fields`) 앞까지만 읽는다."""
    src = FORM.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = src.split("export function BookDetailForm(", 1)[1].split("<div hidden data-hidden-fields=", 1)[0]
    # 도서종류는 별도 컴포넌트(BookKindField) — 라벨이 정의부에 있어 자리 표식으로 바꾼다.
    body = body.replace("<BookKindField", '<BookKindField label="도서종류"')
    out = []
    for m in re.finditer(r'(?<![-\w])label="([^"]+)"|<Label>([^<]+)</Label>', body):
        out.append(m.group(1) or m.group(2))
    return out


def list_columns() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(입력 칸 구간, 뒤쪽 선택 컬럼 구간) — 각 (컬럼 id, 라벨)."""
    src = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = src.split("const columns: DataGridColumn<BookListItem>[] = [", 1)[1].split('id: "nl-lookup"', 1)[0]
    head, tail = body.split(EXTRAS_MARKER, 1)

    def cols(chunk: str) -> list[tuple[str, str]]:
        found = []
        for m in re.finditer(r'key: "(\w+)",\s*(?:id: "(\w+)",\s*)?(?:sortKey: "\w+",\s*)?label: "([^"]+)"', chunk):
            found.append((m.group(2) or m.group(1), m.group(3)))
        return found

    return cols(head), cols(tail)


def default_hidden() -> set[str]:
    src = PAGE.read_text(encoding="utf-8")
    return set(re.findall(r'"(\w+)"', src.split("const BOOK_DEFAULT_HIDDEN = [", 1)[1].split("] as const", 1)[0]))


class ListMatchesFormTest(TestCase):
    def test_form_has_the_36_input_cells(self) -> None:
        self.assertEqual(form_labels(), [
            "도서분류", "도서종류", "도서코드", "인지유무", "인세종류", "인세비율(%)",
            "도서명", "저자명", "ISBN", "정가", "자료제공",
            "서가위치", "판형", "쪽수", "판수", "덩이", "그램", "발행일", "등록일",
            "재고", "출고정지", "상태", "정지사유", "기타",
            "위탁", "현매", "매절", "납품", "특별", "한도", "기타(비율)",
            "비고",
            "전자책", "전자책 ISBN", "전자책 정가", "전자책 비고",
        ])

    def test_list_columns_equal_form_labels_in_order(self) -> None:
        head, _tail = list_columns()
        self.assertEqual([lbl for _id, lbl in head], form_labels(),
                         "도서관리 컬럼(이름 · 순서) = 신규도서 입력 칸")

    def test_each_list_column_reads_the_field_the_form_writes(self) -> None:
        """이름만 같고 다른 값을 보여 주면 안 된다 — 특히 도서종류(BookKind ≠ 묶음 Gbjil)."""
        head, _tail = list_columns()
        key_of = {lbl: cid for cid, lbl in head}
        expect = {
            "도서분류": "sname", "도서종류": "book_kind", "도서코드": "gcode", "인지유무": "stamp",
            "인세종류": "royalty_type", "인세비율(%)": "royalty_rate", "도서명": "gname", "저자명": "gjeja",
            "ISBN": "gisbn", "정가": "gdang", "자료제공": "supply", "서가위치": "gpost", "판형": "name1",
            "쪽수": "gpage", "판수": "gpan1", "덩이": "gqut1", "그램": "gqut2", "발행일": "date1", "등록일": "date2",
            "재고": "gsqut", "출고정지": "grat9", "상태": "status", "정지사유": "name2", "기타": "etc_memo",
            "위탁": "grat1", "현매": "grat2", "매절": "grat3", "납품": "grat4", "특별": "grat5", "한도": "grat7",
            "기타(비율)": "grat6", "비고": "gbigo", "전자책": "bigo3", "전자책 ISBN": "eisbn",
            "전자책 정가": "eprice", "전자책 비고": "ebook_memo",
        }
        self.assertEqual(key_of, expect)
        # 입력 화면의 값 키와도 맞는지(폼이 실제로 그 키를 고친다).
        form = FORM.read_text(encoding="utf-8")
        for key in ("book_kind", "royalty_type", "royalty_rate", "eisbn", "eprice", "ebook_memo", "name1", "name2"):
            self.assertRegex(form, r'onChange\("' + key + r'"', key)

    def test_extra_columns_kept_at_the_end_and_hidden(self) -> None:
        """입력 화면에 없는 기존 컬럼은 지우지 않는다(사용자 결정) — 맨 뒤 · 기본 숨김."""
        _head, tail = list_columns()
        self.assertEqual([cid for cid, _ in tail], [
            "gbjil", "price", "odang", "stock_amount", "scode", "jego1", "jego2", "jego3", "jego4",
            "ocode", "pubun", "gnumb", "gdabi", "bigo1", "bigo2",
        ])
        self.assertEqual(dict(tail)["gbjil"], "도서종류(묶음)", "입력 화면의 도서종류와 이름이 겹치지 않게")
        self.assertTrue({cid for cid, _ in tail} <= default_hidden())

    def test_default_visible_is_the_16_of_dec336(self) -> None:
        head, _tail = list_columns()
        hidden = default_hidden()
        self.assertEqual([lbl for cid, lbl in head if cid not in hidden], [
            "도서분류", "도서코드", "도서명", "저자명", "ISBN", "정가", "자료제공", "서가위치",
            "발행일", "재고", "상태", "정지사유", "기타", "위탁", "비고", "전자책",
        ])

    def test_hidden_list_has_no_stale_keys(self) -> None:
        head, tail = list_columns()
        self.assertTrue(default_hidden() <= {cid for cid, _ in head + tail}, "없는 컬럼 id 가 숨김 목록에 남았다")

    def test_prefs_key_bumped(self) -> None:
        """저장해 둔 컬럼 순서가 새 순서를 덮지 않게 키를 올린다."""
        self.assertIn('useGridPrefs(user?.server_id, "master.book.v4"', PAGE.read_text(encoding="utf-8"))


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
