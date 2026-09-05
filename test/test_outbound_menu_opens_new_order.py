"""「출고 접수」 메뉴 진입점 = 신규 주문 화면 — 2026-08-22 운영 요청.

요청 원문
--------
"출고 접수 메뉴를 누르면 기존에는 출고 접수 목록 화면이 뜨고 신규 주문 버튼을 누르면
신규 출고 명세서를 작성하도록 되어 있는데. 이를 출고 접수를 누르면 바로 신규주문 화면이
뜨도록 수정해주세요."

왜 `route` 를 바꾸지 않았나 (이 테스트의 핵심)
--------------------------------------------
`getFormByRoute` 는 **접두 매칭**이다(`path === routePath || path.startsWith(routePath + "/")`,
가장 긴 매치 우선). `route` 를 `/outbound/orders/new` 로 바꾸면
  - `/outbound/orders` (목록) → 매칭 폼 없음
  - `/outbound/orders/{key}` (상세) → 매칭 폼 없음
이 되어 **목록·상세가 권한 caps 매핑에서 빠진다.**
그래서 `route` 는 대표 경로로 두고, 메뉴 링크만 `menuRoute` 로 덮어쓴다.

총판(물류) 회귀
--------------
`/outbound/orders` 는 총판이면 현황판(DistributorOutboundBoard), 그 외는 목록을 렌더한다.
메뉴가 `/outbound/orders/new` 를 직접 열게 되면서 총판도 이 경로로 들어오므로,
신규 화면에도 같은 분기를 둬 총판 화면이 진입 경로와 무관하게 동일하도록 한다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = SRC / "lib" / "form-registry.ts"
SIDEBAR = SRC / "components" / "app-shell" / "sidebar.tsx"
NEW_PAGE = SRC / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
LIST_PAGE = SRC / "app" / "(app)" / "outbound" / "orders" / "page.tsx"


def _sobo27_block(src: str) -> str:
    i = src.index('id: "Sobo27",')
    return src[i : src.index("},", i)]


class MenuRouteRegistryTests(TestCase):
    def setUp(self) -> None:
        self.src = REGISTRY.read_text(encoding="utf-8")

    def test_menu_route_field_declared(self) -> None:
        self.assertIn("menuRoute?: string;", self.src)

    def test_sobo27_menu_opens_new_order(self) -> None:
        block = _sobo27_block(self.src)
        self.assertIn('menuRoute: "/outbound/orders/new"', block)

    def test_sobo27_route_still_the_list_path(self) -> None:
        """route 는 대표 경로로 유지 — 목록·상세 caps 접두 매칭의 기준."""
        block = _sobo27_block(self.src)
        self.assertIn('route: "/outbound/orders"', block)
        self.assertNotIn('route: "/outbound/orders/new"', block)

    def test_prefix_matching_still_covers_list_and_detail(self) -> None:
        """getFormByRoute 의 접두 매칭 규칙 미러 — route 로 세 경로가 모두 해석된다."""
        route = "/outbound/orders"
        for path in ("/outbound/orders", "/outbound/orders/new", "/outbound/orders/A|B|C|1"):
            self.assertTrue(
                path == route or path.startswith(f"{route}/"),
                f"{path} 가 {route} 로 매칭되지 않는다",
            )
        # 반대로 route 를 /new 로 바꿨다면 목록·상세가 빠진다(이 테스트의 이유).
        bad = "/outbound/orders/new"
        self.assertFalse("/outbound/orders" == bad or "/outbound/orders".startswith(f"{bad}/"))

    def test_get_form_by_route_is_prefix_based(self) -> None:
        """전제 검증 — 구현이 접두 매칭이 아니게 되면 위 논리가 깨진다."""
        fn = self.src[self.src.index("export function getFormByRoute") :][:900]
        self.assertIn("startsWith(`${routePath}/`)", fn)


class InboundMenuRouteTests(TestCase):
    """입고 접수도 출고 접수와 동일하게 메뉴 → 신규 입력 화면 (2026-08-22 2차 요청)."""

    def setUp(self) -> None:
        self.src = REGISTRY.read_text(encoding="utf-8")

    def test_sobo22_menu_opens_new_receipt(self) -> None:
        i = self.src.index('id: "Sobo22",')
        block = self.src[i : self.src.index("},", i)]
        self.assertIn('menuRoute: "/inbound/receipts/new"', block)
        # route 는 대표 경로 유지 — 목록·상세 caps 접두 매칭 기준(DEC-180 함정).
        self.assertIn('route: "/inbound/receipts"', block)
        self.assertNotIn('route: "/inbound/receipts/new"', block)

    def test_new_receipt_page_keeps_back_link(self) -> None:
        page = (
            SRC / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
        ).read_text(encoding="utf-8")
        # DEC-239 — 「목록」 은 공용 골격(SlipEntryLayout listHref)이 그린다.
        self.assertIn('listHref="/inbound/receipts"', page)


class SidebarUsesMenuRouteTests(TestCase):
    def setUp(self) -> None:
        self.src = SIDEBAR.read_text(encoding="utf-8")

    def test_open_and_active_share_the_same_resolver(self) -> None:
        """열 때와 활성 표시가 같은 라우트를 써야 메뉴 하이라이트가 죽지 않는다."""
        self.assertIn("function openRouteOf(form: FormMeta)", self.src)
        self.assertIn("form.menuRoute || form.route", self.src)
        # DEC-199 플라이아웃 이후 «현재 화면» 판정(isFormFocused)도 같은 리졸버를 쓴다 — 3곳.
        self.assertEqual(
            3,
            len(re.findall(r"openRouteOf\(form\)", self.src)),
            "openRouteOf 는 handleFormClick·isFormActive·isFormFocused 세 곳에서 쓰여야 한다",
        )


class DistributorBranchPreservedTests(TestCase):
    """총판은 진입 경로와 무관하게 현황판 — 목록/신규 두 페이지 모두 분기."""

    def test_list_page_branches(self) -> None:
        src = LIST_PAGE.read_text(encoding="utf-8")
        self.assertIn("isDistributorViewer(user)", src)
        self.assertIn("<DistributorOutboundBoard />", src)

    def test_new_page_branches(self) -> None:
        src = NEW_PAGE.read_text(encoding="utf-8")
        self.assertIn("isDistributorViewer(user)", src)
        self.assertIn("<DistributorOutboundBoard />", src)

    def test_new_page_keeps_back_link_to_list(self) -> None:
        """목록은 신규 화면의 「목록」 버튼으로 계속 도달 가능해야 한다."""
        src = NEW_PAGE.read_text(encoding="utf-8")
        self.assertIn('listHref="/outbound/orders"', src)  # DEC-239 — 골격의 「목록」


if __name__ == "__main__":
    main()
