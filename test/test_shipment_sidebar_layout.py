"""출고관리(물류 셸·Menu200/ACC-MENU-NAV-09) 사이드바 IA 정합 — static 회귀 가드.

물류 셸 「출고관리」 하위를 SHIPMENT_SIDEBAR_LAYOUT + form-registry 별칭으로
보존하는지 검증한다. 거래관리(transactions·NAV-02)와 공유하는 화면은 단일 route/API 를
쓰되 `*_shipment_alias` 얇은 별칭으로만 재노출한다 (DEC-049 패턴).
(런타임 없이 form-registry.ts 소스만 파싱 — test_master_sidebar_layout.py 와 동일 정책.)
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONT / "lib" / "form-registry.ts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ShipmentSidebarLayoutTest(TestCase):
    def setUp(self) -> None:
        self.src = _read(REGISTRY)

    def _layout_form_ids(self) -> list[str]:
        block = re.search(
            r"export const SHIPMENT_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];",
            self.src,
        )
        self.assertIsNotNone(block, "SHIPMENT_SIDEBAR_LAYOUT 상수가 필요합니다.")
        return re.findall(r'formId:\s*"([^"]+)"', block.group("body"))

    def test_layout_order(self) -> None:
        ids = self._layout_form_ids()
        self.assertEqual(
            ids,
            [
                # 자체 물류 화면
                "Sobo27",
                # 총판(물류) 전용 출고내역서 — DEC-124(2026-07-24): 출고관리 하위에 배치,
                # 노출은 distributorOnly 로만 게이팅(menuId:null 매트릭스 우회).
                "Sobo39",
                "Sobo67_status",
                # 거래관리(NAV-02) 공유 화면 별칭
                "Sobo21_shipment_alias",
                "Sobo59_verification_shipment_alias",
                "Sobo29_new_release_shipment_alias",
            ],
        )

    def test_sidebar_layouts_map_registers_shipment(self) -> None:
        block = re.search(
            r"export const SIDEBAR_LAYOUTS:[\s\S]*?=\s*\{(?P<body>[\s\S]*?)\};",
            self.src,
        )
        self.assertIsNotNone(block, "SIDEBAR_LAYOUTS 맵이 필요합니다.")
        self.assertIn("shipment: SHIPMENT_SIDEBAR_LAYOUT", block.group("body"))

    def test_all_layout_forms_in_shipment_group(self) -> None:
        for fid in self._layout_form_ids():
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'"[\s\S]{0,400}?menuGroup:\s*"shipment"',
                    self.src,
                )
                self.assertIsNotNone(
                    m, f"{fid} 가 shipment 그룹으로 등록돼 있어야 합니다."
                )

    def test_aliases_share_canonical_routes(self) -> None:
        # 별칭은 transactions 정본과 동일 route 를 가리킨다 (단일 API 공유).
        for fid, route in (
            ("Sobo21_shipment_alias", "/transactions/sales-statement"),
            ("Sobo59_verification_shipment_alias", "/transactions/verification?v=1"),
            ("Sobo29_new_release_shipment_alias", "/transactions/new-release"),
        ):
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'"[\s\S]{0,200}?route:\s*"' + re.escape(route) + r'"',
                    self.src,
                )
                self.assertIsNotNone(m, f"{fid} → route {route} 별칭이 필요합니다.")

    def test_aliases_gated_to_nav09(self) -> None:
        # 별칭은 물류 NAV-09 로 게이트 — publisher(NAV-02) 사용자에게 동시 노출되지 않도록.
        for fid in (
            "Sobo21_shipment_alias",
            "Sobo59_verification_shipment_alias",
            "Sobo29_new_release_shipment_alias",
        ):
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'"[\s\S]{0,200}?menuId:\s*"ACC-MENU-NAV-09"',
                    self.src,
                )
                self.assertIsNotNone(m, f"{fid} 는 menuId ACC-MENU-NAV-09 로 게이트해야 합니다.")


if __name__ == "__main__":
    from unittest import main

    main()
