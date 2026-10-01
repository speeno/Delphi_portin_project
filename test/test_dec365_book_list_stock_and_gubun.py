"""DEC-365 — 도서관리 목록·상세: 재고는 계산해서, 「구분」은 분류명으로 채운다.

배경(2026-10-01 교문사 「도서관리 현황표 재고가 모두 0」): 출판 빌드 테넌트의 ``G4_Book`` 에는
``Gsqut``/``Jego1~4`` 컬럼이 없어 존재-컬럼 SELECT 가 리터럴 0 을 돌려줬다(실재고 2·1·441·28 이 전부 0).
목록 「구분」(sname)도 JOIN 금지(DEC-068)로 늘 빈 값 — 3,466종 중 3,428종에 분류가 있는데 빈칸.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import inventory_service, masters_service, reports_service  # noqa: E402


def _items() -> list[dict]:
    return [
        {"gcode": "00009", "gubun": "10001", "sname": "", "gsqut": 0.0, "jego1": 0.0, "jego2": 0.0, "jego3": 0.0, "jego4": 0.0},
        {"gcode": "3095", "gubun": "10002", "sname": "", "gsqut": 0.0, "jego1": 0.0, "jego2": 0.0, "jego3": 0.0, "jego4": 0.0},
    ]


class ComputedBookStock(unittest.IsolatedAsyncioTestCase):
    async def test_fills_stock_when_columns_absent(self) -> None:
        calls: list[tuple[str, str | None]] = []

        async def good(server_id, *, hcode, asof, axis_like, bcodes):  # noqa: ANN001
            calls.append(("good", axis_like))
            self.assertEqual(hcode, "5019")
            self.assertEqual(bcodes, ["00009", "3095"])
            return {None: {"00009": 2, "3095": 441}, "%A%": {"00009": 78, "3095": 441}, "%B%": {"00009": -76}}[axis_like]

        async def ret(server_id, *, hcode, asof, bcodes, axis_like=None):  # noqa: ANN001
            calls.append(("return", axis_like))
            return {"3095": 3} if axis_like == "%A%" else {}

        items = _items()
        with patch.object(reports_service, "_fetch_stock_asof", side_effect=good), \
                patch.object(inventory_service, "_fetch_return_stock_asof", side_effect=ret):
            await masters_service._attach_computed_book_stock("srv", "5019", items, {"gcode", "gname"})
        self.assertEqual([it["gsqut"] for it in items], [2.0, 441.0])   # 재고 = 정품 전체
        self.assertEqual([it["jego1"] for it in items], [78.0, 441.0])  # 본사재고(A)
        self.assertEqual([it["jego3"] for it in items], [-76.0, 0.0])   # 창고정품(B)
        self.assertEqual([it["jego2"] for it in items], [0.0, 3.0])     # 본사비품(반품재고 A)
        self.assertEqual(sorted(calls, key=str), sorted(
            [("good", None), ("good", "%A%"), ("good", "%B%"), ("return", "%A%"), ("return", "%B%")], key=str))

    async def test_keeps_stored_values_when_columns_exist(self) -> None:
        """재고 컬럼이 있는 테넌트는 저장값을 덮지 않는다(DEC-033 — 컬럼 유무로 데이터 분기)."""
        items = [{"gcode": "B1", "gsqut": 7.0, "jego1": 5.0, "jego2": 0.0, "jego3": 2.0, "jego4": 0.0}]
        mock = AsyncMock()
        with patch.object(reports_service, "_fetch_stock_asof", mock), \
                patch.object(inventory_service, "_fetch_return_stock_asof", mock):
            await masters_service._attach_computed_book_stock(
                "srv", "H1", items, {"gcode", "gsqut", "jego1", "jego2", "jego3", "jego4"})
        mock.assert_not_awaited()
        self.assertEqual(items[0]["gsqut"], 7.0)

    async def test_no_scope_no_compute(self) -> None:
        """회사 스코프가 없으면 여러 회사 수량이 섞이므로 계산하지 않는다."""
        mock = AsyncMock()
        items = _items()
        with patch.object(reports_service, "_fetch_stock_asof", mock):
            await masters_service._attach_computed_book_stock("srv", None, items, {"gcode"})
        mock.assert_not_awaited()

    async def test_failure_keeps_list_alive(self) -> None:
        items = _items()
        with patch.object(reports_service, "_fetch_stock_asof", AsyncMock(side_effect=RuntimeError("db"))), \
                patch.object(inventory_service, "_fetch_return_stock_asof", AsyncMock(return_value={})):
            await masters_service._attach_computed_book_stock("srv", "5019", items, {"gcode"})
        self.assertEqual(items[0]["gsqut"], 0.0)

    def test_asof_is_korean_today(self) -> None:
        from datetime import datetime, timedelta, timezone

        kst = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y.%m.%d")
        self.assertEqual(masters_service._book_stock_asof_today(), kst)


class BookGubunNames(unittest.IsolatedAsyncioTestCase):
    async def test_fills_sname_from_gbun_table_scoped_by_hcode(self) -> None:
        items = _items() + [{"gcode": "X", "gubun": "", "sname": ""}, {"gcode": "Y", "gubun": "10001", "sname": "기존값"}]
        exec_mock = AsyncMock(return_value=[
            {"gcode": "10001", "gname": "가정학"}, {"gcode": "10002", "gname": "식품영양학"},
        ])
        with patch.object(masters_service, "g4_gbun_column_meta",
                          AsyncMock(return_value=({"gcode", "gname", "hcode"}, {"gcode": "Gcode", "gname": "Gname"}))), \
                patch.object(masters_service, "execute_query", exec_mock):
            await masters_service._attach_book_gubun_names("srv", "5019", items)
        self.assertEqual([it["sname"] for it in items], ["가정학", "식품영양학", "", "기존값"])
        sql, params = exec_mock.await_args.args[1], exec_mock.await_args.args[2]
        self.assertIn("G4_Gbun", sql)
        self.assertIn("Hcode=%s", sql)  # 다른 회사 분류명이 섞이지 않게
        self.assertEqual(tuple(params), ("5019",))


class Wiring(unittest.TestCase):
    def test_list_and_detail_call_both(self) -> None:
        src = (BACKEND / "app/services/masters_service.py").read_text(encoding="utf-8")
        lst = src[src.index("async def list_books("):src.index("_BOOK_STOCK_COMPUTED")]
        self.assertIn("await _attach_book_gubun_names(server_id, scope_hcode, items)", lst)
        self.assertIn("await _attach_computed_book_stock(server_id, scope_hcode, items, book_cols)", lst)
        det = src[src.index("async def get_book("):src.index("async def create_book(")]
        self.assertIn("await _attach_computed_book_stock(server_id, scope_hcode, [out], book_cols)", det)


class BookFormatAndStopReasonLabels(unittest.TestCase):
    """판형 = Name1 · 정지사유 = Name2.

    레거시 Subu14(출판 빌드): Edit123(Panel123 「판 형」)=Name1, Edit129(CheckBox2 「정지사유->」)=Name2.
    교문사 실데이터: Name1 = 'B5, 188*257mm'·'규격외 변형'… / Name2 = '절판'·'구판'·'재고없음'….
    종전 웹은 두 라벨이 서로 바뀌어, 「판형」에 입력하면 정지사유 컬럼에 저장됐다.
    """

    FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"

    def test_list_columns(self) -> None:
        src = (self.FE / "app/(app)/master/book/page.tsx").read_text(encoding="utf-8")
        self.assertIn('{ key: "name2", label: "정지사유"', src)
        self.assertIn('{ key: "name1", label: "판형"', src)
        hidden = src[src.index("const BOOK_DEFAULT_HIDDEN"):src.index("];", src.index("const BOOK_DEFAULT_HIDDEN"))]
        self.assertIn('"name1"', hidden)      # 판형 = 기본 숨김(종전과 같은 화면 구성)
        self.assertNotIn('"name2"', hidden)   # 정지사유 = 기본 표시

    def test_detail_form(self) -> None:
        src = (self.FE / "components/master/book-detail-form.tsx").read_text(encoding="utf-8")
        self.assertIn('label="판형" value={data.name1} onChange={(v) => onChange("name1", v)} legacyId="Sobo14.Edit123"', src)
        self.assertIn('label="정지사유" value={data.name2} onChange={(v) => onChange("name2", v)} legacyId="Sobo14.Edit129"', src)

    def test_excel_export_import(self) -> None:
        from app.services import masters_excel

        self.assertEqual(masters_excel.BOOK_IMPORT_MAP["판형"], "name1")
        self.assertEqual(masters_excel.BOOK_IMPORT_MAP["정지사유"], "name2")
        src = (BACKEND / "app/services/masters_excel.py").read_text(encoding="utf-8")
        self.assertIn('("판형", "name1")', src)
        self.assertIn('("정지사유", "name2")', src)

    def test_blank_legacy_date_mask_is_hidden(self) -> None:
        src = (self.FE / "app/(app)/master/book/page.tsx").read_text(encoding="utf-8")
        self.assertIn('label: "발행일"', src)
        self.assertEqual(src.count("format: fmtDate"), 2)  # 발행일 · 등록일


if __name__ == "__main__":
    unittest.main()
