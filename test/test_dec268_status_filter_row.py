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
        # 예외: 거래처거래원장 — 2026-09 UI 통일의 대표(레퍼런스) 화면. 기간·거래처·조회를
        # 제목 줄 오른쪽 부착형 필드로 배치한 기준 레이아웃이라 필터를 아래로 내리지 않는다.
        # 예외 2: 기간별재고원장 — DEC-310(2026-09-24 사용자 「다른 화면과 통일」)으로 거래처거래원장과 같은 한 줄 배치.
        # 예외 3: 원장변경(조정 원장 공용 화면) — DEC-314(2026-09-24 「검색 입력 라인 공간 효율」) 같은 한 줄 배치.
        # 예외 4: 원장관리 세부 화면 전부 — DEC-315(2026-09-24 「원장관리 세부 화면들은 모두 동일한 레이아웃, 한 줄 정렬」).
        allowed = {
            "app/(app)/ledger/customer/page.tsx",
            "app/(app)/inventory/status/page.tsx",
            "components/ledger/adjustment-ledger-screen.tsx",
            "app/(app)/ledger/receivable/page.tsx",
            "app/(app)/inventory/ledger/page.tsx",
            "app/(app)/inventory/value/page.tsx",
        }
        opted_out = sorted(
            str(p.relative_to(FRONT))
            for p in FRONT.rglob("*.tsx")
            if "filtersBelow={false}" in p.read_text(encoding="utf-8")
        )
        # 예외 5: 통계관리 하위 화면 전부 — DEC-320(2026-09-24 「통계관리 하위 화면 검색 레이아웃을 거래처거래원장처럼 통일」).
        stats_prefixes = ("app/(app)/stats/", "app/(app)/reports/")
        self.assertEqual(
            [p for p in opted_out if p not in allowed and not p.startswith(stats_prefixes)], [], opted_out
        )

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
        # 2026-09 — 도서구분(Sobo24.Panel102) 라디오그룹은 운영 화면에서 숨기고 항상 전체 조회
        # (화면 주석 참조). 나머지 Enter 스톱 순서는 그대로 유지돼야 한다.
        for lid in (
            "Sobo24.Edit104", "Sobo24.Edit106", "Sobo24.Edit109",
            "Sobo24.Edit101", "Sobo24.Edit102", "Sobo24.dxButton1",
        ):
            self.assertIn(lid, block, lid)
        self.assertNotIn("Sobo24.Panel102", block, "숨긴 필터는 Enter 스톱에서도 빠진다")
        screen = _read("components/transactions/transaction-status-screen.tsx")
        self.assertIn('const eStoreKind: OutboundStatusStoreKind = "ALL";', screen)


if __name__ == "__main__":
    main()
