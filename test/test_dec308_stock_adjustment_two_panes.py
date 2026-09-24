"""DEC-308 — 재고변경 = 레거시 Subu52 정품·비품 두 창(좌우 분할) + 도서 확정 검색 + 도서명 편집 칸.

사용자 2026-09-24: 「화면 분할은 좌우로 하더라도 거의 기존 재고변경 레거시 기능과 동일하게」,
「도서명도 편집박스 내에 표시 (원본처럼 정품, 비품 재고변경 모두 할 수 있도록)」.

레거시 근거(WeLove_FTP/도서유통-출판/Subu52.pas):
  - Button101Click: Sg_Csum Scode='A'(정품) / Button201Click: Scode='C'(비품).
  - Edit104/204 Enter → Seek40 → Edit103/203 코드 확정 → ``Gcode = 코드`` 로 조회.
  - DBGrid201KeyPress: 비품 원장재고 = Tong40 ``Gbqut``(본사 반품재고).
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import adjustment_ledger_service as svc

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
SCREEN = FRONT / "components" / "ledger" / "adjustment-ledger-screen.tsx"
PAGE = FRONT / "app" / "(app)" / "ledger" / "adjust" / "book" / "page.tsx"


class ReturnAxisService(TestCase):
    def test_book_return_axis_is_scode_c_on_sg_csum(self) -> None:
        cfg = svc.axis_config("book_return")
        self.assertEqual((cfg["table"], cfg["scode"]), ("Sg_Csum", "C"))
        self.assertEqual(cfg["ledger_value"], "return_stock_asof")
        self.assertEqual(svc.axis_config("book")["scode"], "A", "정품 창은 그대로 A")

    def test_list_filters_exact_code_when_confirmed(self) -> None:
        seen: dict = {}

        async def fake_query(_sid, sql, params):
            seen["sql"], seen["params"] = sql, params
            return []

        with patch.object(svc, "execute_query", side_effect=fake_query):
            asyncio.run(svc.list_adjustments(
                server_id="s", axis="book_return", hcode="5019",
                date_from="2026-09-01", date_to="2026-09-24", gcode="2988",
            ))
        self.assertIn("Gcode = %s", seen["sql"])
        self.assertIn("Hcode = %s", seen["sql"])
        self.assertEqual(seen["params"], ("5019", "C", "2026.09.01", "2026.09.24", "2988"))

    def test_return_ledger_value_uses_return_stock_on_hq_axis(self) -> None:
        fake = AsyncMock(return_value={"2988": 7})
        with patch("app.services.inventory_service._fetch_return_stock_asof", fake):
            out = asyncio.run(svc.ledger_value(
                server_id="s", axis="book_return", hcode="5019", gcode="2988", asof="2026-09-24",
            ))
        self.assertEqual(out, {"supported": True, "gosum": 7})
        kwargs = fake.await_args.kwargs
        self.assertEqual(kwargs["axis_like"], "%A%", "레거시: 본사 축(Ocode/Scode A)")
        self.assertEqual(kwargs["asof"], "2026.09.24")


class TwoPaneScreen(TestCase):
    def setUp(self) -> None:
        self.src = SCREEN.read_text(encoding="utf-8")

    def test_page_renders_two_panes_left_right(self) -> None:
        page = PAGE.read_text(encoding="utf-8")
        self.assertIn("<StockAdjustmentScreen />", page)
        block = self.src.split("export function StockAdjustmentScreen()")[1]
        self.assertIn('orientation="horizontal"', block, "좌우 분할")
        self.assertIn("axis={BOOK_ADJUSTMENT_AXIS}", block)
        self.assertIn("axis={BOOK_RETURN_ADJUSTMENT_AXIS}", block)

    def test_lower_pane_uses_legacy_2xx_widget_ids(self) -> None:
        block = self.src.split("export const BOOK_RETURN_ADJUSTMENT_AXIS")[1].split("};")[0]
        for wid in ("Edit201", "Edit202", "Edit204", "Button201", "Panel004", "DBGrid201", "Panel003"):
            self.assertIn(f'"{wid}"', block)
        self.assertIn('kind: "book_return"', block)
        self.assertIn('paneTitle: "비품"', block)

    def test_book_name_is_an_edit_box_with_lookup(self) -> None:
        name_col = self.src.split('key: "gname",')[1].split('key: "gssum"')[0]
        self.assertIn("<MasterLookupField", name_col, "도서명도 편집 칸(검색 가능)")
        self.assertIn("GNAME.EDIT", name_col)
        self.assertIn("useInlineAutocomplete", name_col)
        self.assertIn("commitCode(row.uid, code, row.gdate)", name_col, "확정하면 원장재고까지 채운다")

    def test_confirmed_search_book_filters_by_code_and_seeds_row(self) -> None:
        self.assertIn("gcode: eCode || undefined", self.src)
        self.assertIn("pristine: true", self.src, "미리 채운 입력 줄은 건드리기 전엔 저장하지 않는다")
        self.assertIn("if (!o) return !r.pristine && !isBlankNew(r);", self.src)

    def test_grid_sorts_and_exports_excel(self) -> None:
        """2026-09-24 사용자 「목록표 정렬 기능 추가, 엑셀 저장 기능 추가」."""
        for key in ("gdate", "gcode", "gname", "gssum", "gosum", "gbsum", "gbigo"):
            col = self.src.split(f'key: "{key}",')[1][:40]
            self.assertIn("sortable: true", col, f"{key} 헤더 정렬")
        self.assertIn("sort={gridSort.sort}", self.src)
        self.assertIn("rows={displayRows}", self.src)
        # 새 행은 정렬과 무관하게 맨 아래 — 행 추가/입력 줄 포커스(«마지막 행»)가 깨지지 않게.
        self.assertIn("[...gridSort.sortedRows, ...newRows]", self.src)
        self.assertIn('"엑셀 저장"', self.src)
        self.assertIn("gridRowsToExport(cols, displayRows)", self.src, "화면 컬럼·정렬 그대로")
        self.assertIn('!== "row-actions"', self.src, "삭제 버튼 칸은 엑셀에서 뺀다")

    def test_unresolved_code_is_not_saved(self) -> None:
        self.assertIn("등록된 ${axis.codePlaceholder}가 아닙니다", self.src)


if __name__ == "__main__":
    main()
