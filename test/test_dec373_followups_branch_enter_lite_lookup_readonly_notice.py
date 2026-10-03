"""DEC-373 — 10/3 후속: 거래명세서 신규 지점 Enter 대기 · 도서 검색 팝업 가벼운 조회 · 조회 전용 안내 줄.

1. 거래명세서 신규(`sales-statement/new`) — 신규 출고(DEC-368)와 같은 증상: 지점 목록을 받는 중의 Enter 가 곧장
   그리드로 넘어가 지점을 못 고른다 → 로드가 끝날 때까지 기다렸다가 지점이 있으면 지점 선택칸에, 없으면 그리드로.
2. 도서 검색 팝업 · 자동완성이 쓰는 `/masters/book` 은 DEC-365(2026-10-01)부터 행마다 재고 5종을 계산한다
   (빈 검색 200행 = 운영 ~7초 — DEC-367 경합의 배경). 팝업은 코드 · 도서명 · 저자 · ISBN · 단가만 쓰므로 `lite=true` 로 생략.
3. 조회 전용 계정(DEC-370)은 저장 버튼이 그대로 보이는 화면이 많다 → 입력 가능한 업무 영역 화면 맨 위에 안내 한 줄.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import masters_service as ms

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class SalesStatementNewBranchEnterWaits(TestCase):
    def setUp(self) -> None:
        self.src = _read("app/(app)/transactions/sales-statement/new/page.tsx")

    def test_enter_while_loading_is_deferred(self) -> None:
        start = self.src.index("function onGjisaKeyDown(e: React.KeyboardEvent)")
        body = self.src[start : self.src.index("\n  }\n", start)]
        guard = body.index("if (gc && (branchLoading || branchesForHcodeRef.current !== gc))")
        self.assertIn("gjisaEnterPendingRef.current = true;", body)
        self.assertLess(guard, body.index("focusCell(0, firstEditCol);"))

    def test_after_load_focus_select_or_grid(self) -> None:
        self.assertIn("if (branchLoading || !gjisaEnterPendingRef.current) return;", self.src)
        self.assertIn("if (showGjisa && branchOptions.length > 0) gjisaRef.current?.focus();", self.src)
        self.assertIn("branchesForHcodeRef.current = gc; // 실패도", self.src)
        self.assertNotIn("지점 확인 중… (Enter로 통과)", self.src)


class BookLookupLite(IsolatedAsyncioTestCase):
    async def _run(self, lite: bool) -> dict[str, AsyncMock]:
        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            return [{"gcode": "B1", "gname": "도서", "gdang": 1000}]

        mocks = {
            "ext": AsyncMock(return_value=None),
            "ebook": AsyncMock(return_value=None),
            "gubun": AsyncMock(return_value=None),
            "stock": AsyncMock(return_value=None),
        }
        with patch.object(ms, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(ms, "g4_book_column_meta", AsyncMock(side_effect=RuntimeError("no meta"))), \
             patch.object(ms.book_ext_service, "attach_ext", mocks["ext"]), \
             patch.object(ms.book_ebook_service, "attach_ebook", mocks["ebook"]), \
             patch.object(ms, "_attach_book_gubun_names", mocks["gubun"]), \
             patch.object(ms, "_attach_computed_book_stock", mocks["stock"]):
            res = await ms.list_books(server_id="remote_153", scope_hcode="5019", limit=200, lite=lite)
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["gcode"], "B1")
        return mocks

    async def test_lite_skips_attachments(self) -> None:
        mocks = await self._run(True)
        for name, m in mocks.items():
            self.assertEqual(m.await_count, 0, name)

    async def test_full_list_keeps_attachments(self) -> None:
        mocks = await self._run(False)
        for name, m in mocks.items():
            self.assertEqual(m.await_count, 1, name)

    def test_route_and_lookup_wiring(self) -> None:
        router = (BACK / "routers" / "masters.py").read_text(encoding="utf-8")
        self.assertIn('lite: bool = Query(False, description="검색 팝업용', router)
        self.assertIn("lite=lite,", router)
        cfg = _read("lib/master-lookup-config.ts")
        book = cfg[cfg.index("  book: {") : cfg.index("  inboundVendor: {")]
        self.assertIn("lite: true,", book)
        # 도서관리 목록(재고 · 확장 필드 표시)은 종전대로 전체 조회.
        self.assertNotIn("lite", _read("app/(app)/master/book/page.tsx"))


class ReadOnlyNotice(TestCase):
    def test_notice_component_and_mount(self) -> None:
        src = _read("components/app-shell/read-only-account-notice.tsx")
        self.assertIn("user?.account_read_only !== true || superUser", src)
        self.assertIn('"/outbound"', src)
        self.assertIn('"/transactions/sales-statement/auto-print"', src)
        for read_area in ('"/reports"', '"/stats"', '"/inventory"'):
            self.assertNotIn(read_area, src)
        layout = _read("app/(app)/layout.tsx")
        self.assertIn("<ReadOnlyAccountNotice />", layout)


if __name__ == "__main__":
    main()
