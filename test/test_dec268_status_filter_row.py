"""DEC-268 — 조회 필터는 «제목·경로 줄 다음 줄, 왼쪽 정렬» (2026-09-08 → 09 전 화면 확대).

- 2026-09-08 「출고 현황 화면의 검색 관련 여러 필터 입력 그룹을 아래부분으로 이동하면 좋겠다」
- 2026-09-09 「재고현황, 청구서 관리 화면등 여러 화면에서 조회용 필터 값 입력 컴포넌트와 검색
  버튼이 모두 오른쪽 정렬 → 왼쪽 정렬로, 화면이름 및 경로 라인 다음 라인으로. 기타 유사 케이스도
  같은 규칙」 → `PageHeader.filtersBelow` **기본값 true**(전 화면 규칙).

액션(엑셀·신규 등록 등)은 종전대로 **제목 줄 우측 끝**(DEC-228/263)이고, 액션만 있고 필터가 없는
화면은 두 번째 줄을 만들지 않는다. 필터는 **여전히 띠(PageHeader children) 안**이라 인라인 라벨
CSS(DEC-200 `.page-header` 스코프)와 Enter 이동 스코프(FILTER_STOP_IDS)는 그대로다.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class FiltersBelowTitle(TestCase):
    def test_page_header_puts_filters_below_by_default(self) -> None:
        src = _read("components/shared/page-header.tsx")
        self.assertIn("filtersBelow?: boolean", src)
        self.assertIn("filtersBelow = true", src)  # 전 화면 기본 규칙(2026-09-09)
        self.assertIn('filtersBelow ? "justify-start pt-1 md:col-span-2" : "justify-end"', src)

    def test_actions_stay_on_the_title_row(self) -> None:
        """엑셀·신규 등록 등 액션은 제목 줄 우측 끝(DEC-228/263) — 필터만 아래로 내려간다."""
        src = _read("components/shared/page-header.tsx")
        self.assertIn('data-slot="page-header-actions"', src)
        self.assertIn("{actions && filtersBelow ? (", src)
        # 필터가 없고 액션만 있는 화면은 두 번째 줄을 만들지 않는다
        self.assertIn("filtersBelow ? Boolean(children) : Boolean(children) || Boolean(actions)", src)

    def test_screens_do_not_opt_out(self) -> None:
        """전 화면 규칙이므로 `filtersBelow={false}` 로 되돌린 화면이 없어야 한다(예외는 여기에 명시)."""
        opted_out = [
            str(p)
            for p in sorted(FRONT.rglob("*.tsx"))
            if "filtersBelow={false}" in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(opted_out, [], opted_out)

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
