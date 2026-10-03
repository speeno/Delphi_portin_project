"""DEC-368 — 신규 출고: 지점 목록 로딩 중 지사 Enter 는 통과하지 않고 로드를 기다린다.

보고(교문사, 2026-10-02)
-----------------------
"신규 출고 주문 : 거래처명 검색 - 지사 선택에서 엔터.. 하면 지사들이 나와야하는데
바로 위탁으로 넘어가서 지정이 안되는경우가 있습니다."

원인
----
거래처 확정 후 지점(H2_Gbun) 목록은 비동기로 받는다. 받는 동안 지사 칸은 일반 입력칸이고
그 Enter 는 곧장 첫 줄 「구분」(기본 위탁)으로 넘겼다 → 지사가 있는 거래처인데 목록이
늦게 오면 지사를 고르지 못했다("가끔" = 응답이 늦을 때).

가드
----
- 로딩 중(또는 현재 거래처 기준 확인 전) Enter 는 대기 표식만 남기고 멈춘다.
- 로드가 끝나면: 지사가 있으면 지사 목록을 연다(LocalComboField autoOpen),
  없으면(실패 포함) 그때 「구분」으로 간다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PAGE = SRC / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
COMBO = SRC / "components" / "shared" / "local-combo-field.tsx"


class OutboundGjisaEnterWaitsTests(TestCase):
    def setUp(self) -> None:
        self.page = PAGE.read_text(encoding="utf-8")

    def _enter_handler(self) -> str:
        start = self.page.index("function focusFirstPubun(e: ReactKeyboardEvent)")
        return self.page[start : self.page.index("\n  }", start)]

    def test_enter_while_loading_does_not_advance(self) -> None:
        body = self._enter_handler()
        guard = body.index("branchLoading || branchesForHcodeRef.current !== customerCode")
        self.assertIn("gjisaEnterPendingRef.current = true;", body)
        self.assertLess(guard, body.index("focusFirstPubunEl();"))

    def test_pending_enter_opens_list_or_advances_after_load(self) -> None:
        self.assertIn("if (branchLoading || !gjisaEnterPendingRef.current) return;", self.page)
        self.assertIn(
            "if (showGjisa && branchOptions.length > 0) setGjisaAutoOpen(true);", self.page
        )
        self.assertIn("autoOpen={gjisaAutoOpen}", self.page)
        self.assertIn("onAutoOpened={() => setGjisaAutoOpen(false)}", self.page)

    def test_load_failure_releases_pending_enter(self) -> None:
        catch = self.page.index(".customerBranchList(gc")
        tail = self.page[catch : catch + 1200]
        self.assertIn("branchesForHcodeRef.current = gc; // 실패도", tail)

    def test_placeholder_no_longer_says_pass_through(self) -> None:
        self.assertNotIn("지점 확인 중… (Enter로 통과)", self.page)

    def test_combo_supports_auto_open(self) -> None:
        src = COMBO.read_text(encoding="utf-8")
        self.assertIn("autoOpen?: boolean;", src)
        self.assertIn("if (!autoOpen || options.length === 0) return;", src)
        self.assertIn("onAutoOpened?.();", src)


if __name__ == "__main__":
    main()
