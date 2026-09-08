"""DEC-268 — 현황 화면 검색 필터를 띠 «아래 줄 전폭»으로 (2026-09-08 사용자).

「출고 현황 화면의 검색 관련 여러 필터 입력 그룹을 아래부분으로 이동하면 좋겠다.」
거래처·도서코드·전표·시작일·종료일·도서구분·거래구분 7묶음이 제목 오른쪽에 몰려 좁고 멀었다.

`PageHeader` 에 `filtersBelow` 를 두고 현황 공용 화면(TransactionStatusScreen — 출고/입고/반품/
폐기/신간발행)이 그것을 쓴다. 필터는 **여전히 띠(PageHeader children) 안**이라 인라인 라벨 CSS
(DEC-200 `.page-header` 스코프)와 Enter 이동 스코프(FILTER_STOP_IDS)는 그대로다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class FiltersBelowTitle(TestCase):
    def test_page_header_supports_below_row(self) -> None:
        src = _read("components/shared/page-header.tsx")
        self.assertIn("filtersBelow?: boolean", src)
        self.assertIn("filtersBelow = false", src)  # 다른 화면은 종전대로 제목 오른쪽
        self.assertIn('filtersBelow ? "justify-start pt-1 md:col-span-2" : "justify-end"', src)
        self.assertIn('filtersBelow && "ml-auto"', src)  # 액션(엑셀·신규 등)은 그 줄 우측 끝

    def test_status_screen_opts_in(self) -> None:
        src = _read("components/transactions/transaction-status-screen.tsx")
        i = src.index("<PageHeader")
        head = src[i : src.index(">", src.index("filtersBelow", i))]
        self.assertIn("filtersBelow", head)

    def test_filters_stay_inside_the_band(self) -> None:
        """필터는 띠 밖으로 나가지 않는다 — .page-header 인라인 라벨 CSS·Enter 스코프 유지."""
        src = _read("components/transactions/transaction-status-screen.tsx")
        band = src[src.index("<PageHeader") : src.index("</PageHeader>")]
        self.assertIn('data-legacy-id="Sobo24.SearchPanel"', band)
        self.assertIn("data-enter-scope", band)
        self.assertIn('data-legacy-id="Sobo24.dxButton1"', band)  # 조회 버튼도 같은 스코프

    def test_enter_stop_order_unchanged(self) -> None:
        src = _read("components/transactions/transaction-status-screen.tsx")
        block = src[src.index("const FILTER_STOP_IDS") : src.index("];", src.index("const FILTER_STOP_IDS"))]
        for lid in (
            "Sobo24.Edit104", "Sobo24.Edit106", "Sobo24.Edit109",
            "Sobo24.Edit101", "Sobo24.Edit102", "Sobo24.Panel102", "Sobo24.dxButton1",
        ):
            self.assertIn(lid, block, lid)


if __name__ == "__main__":
    main()
