from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONT / "lib" / "form-registry.ts"
SIDEBAR = FRONT / "components" / "app-shell" / "sidebar.tsx"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MasterSidebarLayoutTest(TestCase):
    def test_master_layout_order(self) -> None:
        src = _read(REGISTRY)
        block = re.search(
            r"export const MASTER_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];",
            src,
        )
        self.assertIsNotNone(block, "MASTER_SIDEBAR_LAYOUT 상수가 필요합니다.")
        body = block.group("body")
        form_ids = re.findall(r'formId:\s*"([^"]+)"', body)
        self.assertEqual(
            form_ids,
            [
                "Sobo11",
                "Sobo12",
                "Sobo13",
                "Sobo14",
                "Sobo16_special",
            ],
        )
        # 할인율(Sobo39)은 운영 요청(2026-08-13, DEC-155)으로 사이드바에서 숨김 —
        # route(/master/discount)·API·구현은 유지(배본처관리 숨김 선례와 동일 방식).
        self.assertNotIn("Sobo39", form_ids)
        # 배본처관리(Sobo16_baebon)는 운영 요청으로 사이드바에서 감춤 (2026-05).
        self.assertNotIn("Sobo16_baebon", form_ids)
        # 기타거래처(Sobo15)는 거래처관리(Sobo11)와 중복(평행 G5_Ggeo 마스터)이라
        # 운영 요청으로 사이드바에서 감춤 (2026-06-20). 레지스트리/페이지는 보존.
        self.assertNotIn("Sobo15", form_ids)
        self.assertIn('kind: "separator"', body)
        self.assertIn('label: "비율관리"', body)

    def test_hidden_unused_forms(self) -> None:
        src = _read(REGISTRY)
        for menu_id in (
            "ACC-MENU-HIDDEN-MASTER-PUBLISHER",
            "ACC-MENU-HIDDEN-MASTER-BOOK-CODE",
            "ACC-MENU-HIDDEN-MASTER-BAEBON",
        ):
            self.assertIn(menu_id, src)
        self.assertNotIn('menuId: "ACC-MENU-HIDDEN-MASTER-DISCOUNT"', src)

    def test_baebon_entry_exists(self) -> None:
        # 배본처관리는 사이드바·허브에서 감추지만 레지스트리 항목·route·API 는 유지한다.
        # menuId 만 HIDDEN 으로 분리되어 show-first 정책에서 visible=false 처리된다.
        src = _read(REGISTRY)
        self.assertIn('id: "Sobo16_baebon"', src)
        self.assertIn('route: "/master/baebon"', src)
        self.assertIn('menuId: "ACC-MENU-HIDDEN-MASTER-BAEBON"', src)
        self.assertNotIn('menuId: "ACC-MENU-MASTERS-07"', src)

    def test_sidebar_uses_layout_and_group(self) -> None:
        # 사이드바는 master 전용 분기 대신 그룹별 SIDEBAR_LAYOUTS 맵으로 일반화됨
        # (master + transactions 공통 렌더). 레이아웃·서브그룹·구분선 처리는 유지.
        src = _read(SIDEBAR)
        self.assertIn("SIDEBAR_LAYOUTS", src)
        self.assertIn("SIDEBAR_LAYOUTS[group.id]", src)
        self.assertIn("entry.children", src)
        self.assertIn("entry.label", src)
        self.assertIn('entry.kind === "separator"', src)

