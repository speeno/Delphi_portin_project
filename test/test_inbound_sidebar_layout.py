"""입고관리 사이드바 IA 정합 — static 회귀 가드."""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONT / "lib" / "form-registry.ts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class InboundSidebarLayoutTest(TestCase):
    def setUp(self) -> None:
        self.src = _read(REGISTRY)

    def _layout_form_ids(self) -> list[str]:
        block = re.search(
            r"export const INBOUND_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];",
            self.src,
        )
        self.assertIsNotNone(block, "INBOUND_SIDEBAR_LAYOUT 상수가 필요합니다.")
        return re.findall(r'formId:\s*"([^"]+)"', block.group("body"))

    def test_inbound_group_exists(self) -> None:
        self.assertRegex(self.src, r'\{ id: "inbound", label: "입고관리"')
        self.assertRegex(self.src, r'inbound:\s*"ACC-MENU-NAV-09"')

    def test_layout_order(self) -> None:
        # 입고현황은 출고현황(Sobo67_status)과 동일하게 단일 메뉴 항목(Sobo25_status_list).
        # 상세/요약은 페이지 내부 탭(view=detail|summary 딥링크)이라 사이드바에 미노출.
        ids = self._layout_form_ids()
        self.assertEqual(
            ids,
            [
                "Sobo22",
                "Sobo22_inbound_statement",
                "Sobo25_status_list",
                "Sobo54",
                "Sobo57",
                "Sobo22_import",
            ],
        )
        # 단일 레벨 보증 — 입고현황 children 서브그룹이 없어야 한다.
        self.assertNotIn("Sobo25_status_detail", ids)
        self.assertNotIn("Sobo25_status_summary", ids)

    def test_sidebar_layouts_map_registers_inbound(self) -> None:
        block = re.search(
            r"export const SIDEBAR_LAYOUTS:[\s\S]*?=\s*\{(?P<body>[\s\S]*?)\};",
            self.src,
        )
        self.assertIsNotNone(block, "SIDEBAR_LAYOUTS 맵이 필요합니다.")
        self.assertIn("inbound: INBOUND_SIDEBAR_LAYOUT", block.group("body"))

    def test_all_layout_forms_registered_in_inbound_group(self) -> None:
        for fid in self._layout_form_ids():
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"'
                    + re.escape(fid)
                    + r'"[\s\S]{0,500}?menuGroup:\s*"inbound"',
                    self.src,
                )
                self.assertIsNotNone(m, f"{fid} 가 inbound 그룹으로 등록돼 있어야 합니다.")


if __name__ == "__main__":
    from unittest import main

    main()
