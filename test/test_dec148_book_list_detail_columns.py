"""DEC-148 — 도서관리 목록 = 도서 세부내역 컬럼 전면 회귀 가드.

2026-08-13 영업팀: "기초관리-도서관리: 컬럼에 도서세부내역으로 보여지는 내용
추가 요청". list_books 가 g4_book_adapt 의 존재-컬럼 SELECT 를 재사용해 상세
필드 전면을 반환하고(테넌트 DDL drift 는 ''/0, JOIN 0 — DEC-068 행증식 금지),
화면 목록 컬럼·모델이 이를 1:1 노출한다. SHOW COLUMNS 실패 시 종전 기본
7컬럼 폴백(목록 500 금지).

라이브 대사(교문사 5019, 00004): 41키 — 서가위치 H13,25 · 도서구분 A ·
출고정지 '1' · 단가 13000 = 상세 화면과 일치.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import g4_book_adapt as adapt  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

_G4_COLS = [
    "Gcode", "Gname", "Gjeja", "Gisbn", "Gdang", "Gpost", "Date1", "Date2",
    "Sname", "Jubun", "Scode", "Ocode", "Pubun", "Gnumb", "Gdabi", "Gbjil",
    "Name1", "Name2", "Gbigo", "Bigo1", "Bigo2", "Grat9", "Gsqut",
    "Grat1", "Grat2", "Grat3", "Grat4", "Grat5", "Grat6", "Grat7",
    "Gpage", "Gpan1", "Gqut1", "Gqut2", "Price", "Odang",
    "Jego1", "Jego2", "Jego3", "Jego4",
]


class BookListDetailColumnsTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        adapt.clear_g4_column_cache_for_tests()
        self.addCleanup(adapt.clear_g4_column_cache_for_tests)

    async def test_list_returns_detail_fields(self) -> None:
        captured: list[str] = []

        async def fake_adapt_exec(server_id, sql, params=()):
            assert "SHOW COLUMNS" in sql
            return [{"Field": c} for c in _G4_COLS]

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            return [{
                "gcode": "00004", "gname": "[X]가정경제학*", "gpost": "H13, 25",
                "scode": "A", "name2": "절판", "gdang": 13000, "grat9": "1",
                "sname": "가정학", "jubun": "", "price": 0, "gsqut": 3,
            }]

        with patch.object(adapt, "execute_query", fake_adapt_exec), \
                patch.object(ms, "execute_query", fake_exec):
            res = await ms.list_books(server_id="remote_1", q="00004")

        item = res["items"][0]
        # 세부내역 필드가 목록 행에 실림 (누락 키는 ''/0 기본).
        self.assertEqual(item["gpost"], "H13, 25")
        self.assertEqual(item["scode"], "A")
        self.assertEqual(item["name2"], "절판")
        self.assertEqual(item["grat9"], "1")
        self.assertEqual(item["gsqut"], 3.0)
        for k in ("sname", "jubun", "ocode", "pubun", "gnumb", "gbigo",
                  "price", "odang", "jego1", "jego4", "grat7", "bigo1"):
            self.assertIn(k, item)
        # 내부/사이드테이블 필드 제외.
        for k in ("hcode", "yesno", "bigo3", "gbun_name"):
            self.assertNotIn(k, item)
        # JOIN 0 (DEC-068 목록 행증식 금지).
        select_sql = next(s for s in captured if "COUNT(*)" not in s)
        self.assertNotIn("JOIN", select_sql.upper())

    async def test_show_columns_failure_falls_back_to_base_seven(self) -> None:
        async def broken_adapt_exec(server_id, sql, params=()):
            raise RuntimeError("SHOW COLUMNS denied")

        async def fake_exec(server_id, sql, params=()):
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            return [{"gcode": "B1", "gname": "책", "gdang": 1000}]

        with patch.object(adapt, "execute_query", broken_adapt_exec), \
                patch.object(ms, "execute_query", fake_exec):
            res = await ms.list_books(server_id="remote_1")
        item = res["items"][0]
        self.assertEqual(item["gcode"], "B1", "폴백 시에도 목록 동작(500 금지)")
        self.assertEqual(item["gdang"], 1000)


class ScreenAndModelGuard(TestCase):
    def test_page_has_detail_columns_and_shelf_label_fix(self) -> None:
        src = (FRONTEND / "app" / "(app)" / "master" / "book"
               / "page.tsx").read_text(encoding="utf-8")
        for needle in (
            'label: "서가위치"',   # gpost 오라벨("출판사") 정정
            'label: "도서분류"',
            'label: "도서처리"',
            'label: "판형"',
            'label: "원가"',
            'label: "매입가"',
            'label: "위탁"',
            'label: "한도"',
            'label: "본사재고 정품"',
            'label: "세액유무"',
            'label: "출고정지"',
        ):
            self.assertIn(needle, src)
        self.assertNotIn('label: "출판사"', src)

    def test_backend_model_has_detail_fields(self) -> None:
        from app.models.master import BookListItem

        fields = BookListItem.model_fields
        for k in ("sname", "jubun", "scode", "ocode", "pubun", "gnumb",
                  "name1", "name2", "date2", "gbigo", "bigo1", "bigo2",
                  "grat9", "gsqut", "grat1", "grat7", "gpage", "price",
                  "odang", "jego1", "jego4"):
            self.assertIn(k, fields)


class ExcelCatalogGuard(TestCase):
    """DEC-148 확장 — 엑셀 저장 헤더 = 목록 화면 컬럼 1:1 (2026-08-13 후속 보고)."""

    def test_book_export_columns_cover_detail_fields(self) -> None:
        from app.services.masters_excel import BOOK_COLUMNS

        headers = [h for h, _ in BOOK_COLUMNS]
        keys = [k for _, k in BOOK_COLUMNS]
        self.assertEqual(headers[0], "도서코드", "PK 첫 컬럼(업로드 행 식별)")
        self.assertIn("서가위치", headers)
        self.assertNotIn("출판사", headers, "gpost 오라벨 정정 — export 는 신 헤더만")
        for h in ("도서분류", "도서처리", "판형", "원가", "매입가", "위탁", "한도",
                  "재고", "본사재고 정품", "창고재고 비품", "세액유무", "출고정지"):
            self.assertIn(h, headers)
        for k in ("sname", "jubun", "name2", "price", "odang", "grat1",
                  "grat7", "gsqut", "jego1", "jego4", "bigo1", "grat9"):
            self.assertIn(k, keys)

    def test_book_import_map_extended_with_legacy_alias(self) -> None:
        from app.services.masters_excel import BOOK_IMPORT_MAP, BOOK_NUMERIC_KEYS

        # 신/구 헤더 모두 gpost — 구 서식 재업로드 하위호환.
        self.assertEqual(BOOK_IMPORT_MAP["서가위치"], "gpost")
        self.assertEqual(BOOK_IMPORT_MAP["출판사"], "gpost")
        self.assertEqual(BOOK_IMPORT_MAP["판형"], "name2")
        self.assertEqual(BOOK_IMPORT_MAP["한도"], "grat7")
        self.assertEqual(BOOK_IMPORT_MAP["기타"], "grat6")
        # 읽기전용 재고는 역반영 금지.
        for ro in ("gsqut", "jego1", "jego2", "jego3", "jego4"):
            self.assertNotIn(ro, BOOK_IMPORT_MAP.values())
        # 수치 필드 파싱 — 비율/가격/물성. 플래그(grat9)는 텍스트 유지.
        for k in ("price", "odang", "gpage", "grat1", "grat7"):
            self.assertIn(k, BOOK_NUMERIC_KEYS)
        self.assertNotIn("grat9", BOOK_NUMERIC_KEYS)


if __name__ == "__main__":
    main()
