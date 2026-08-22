"""거래관리(2번째 대메뉴) 사이드바 IA 정합 — static 회귀 가드.

레거시 「거래관리」(Menu200 / ACC-MENU-NAV-02) 스크린샷 구조를
TRANSACTIONS_SIDEBAR_LAYOUT + form-registry 항목으로 1:1 보존하는지 검증한다.
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


class TransactionsSidebarLayoutTest(TestCase):
    def setUp(self) -> None:
        self.src = _read(REGISTRY)

    def _layout_form_ids(self) -> list[str]:
        block = re.search(
            r"export const TRANSACTIONS_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];",
            self.src,
        )
        self.assertIsNotNone(block, "TRANSACTIONS_SIDEBAR_LAYOUT 상수가 필요합니다.")
        return re.findall(r'formId:\s*"([^"]+)"', block.group("body"))

    def test_group_label_is_transaction_management(self) -> None:
        # 그룹 라벨이 「거래현황」이 아니라 레거시와 동일한 「거래관리」여야 한다.
        self.assertRegex(
            self.src,
            r'\{ id: "transactions", label: "거래관리"',
        )

    def test_layout_order_matches_screenshot(self) -> None:
        ids = self._layout_form_ids()
        self.assertEqual(
            ids,
            [
                # 명세서 3종
                "Sobo21",
                "Sobo29_other",
                # 거래현황 4뷰
                "Sobo21_status_list",
                "Sobo21_status_detail",
                "Sobo21_status_summary",
                "Sobo21_status_memo",
                # 출고검증 3종
                "Sobo59_1",
                "Sobo59_2",
                "Sobo59_3",
                # 제작·원천·저자
                "Sobo26_production_stmt",
                "Sobo27_production_status",
                "Sobo28_withholding",
                "Sobo_author_history",
                # 신간발행
                "Sobo29_new_release",
            ],
        )

    def test_layout_subgroups_present(self) -> None:
        block = re.search(
            r"export const TRANSACTIONS_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];",
            self.src,
        )
        body = block.group("body")
        # 2026-08-22 표기 통일(입고 접수/현황·출고 접수/현황과 동일 규칙): 거래현황 → 거래 현황.
        self.assertIn('label: "거래 현황"', body)
        self.assertNotIn('label: "입고현황"', body)
        self.assertGreaterEqual(body.count('kind: "separator"'), 3)

    def test_all_layout_forms_registered_in_transactions_group(self) -> None:
        ids = self._layout_form_ids()
        for fid in ids:
            with self.subTest(form_id=fid):
                # 해당 id 등록 블록 + menuGroup transactions 가 같은 객체 안에 있는지
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'"[\s\S]{0,400}?menuGroup:\s*"transactions"',
                    self.src,
                )
                self.assertIsNotNone(
                    m, f"{fid} 가 transactions 그룹으로 등록돼 있어야 합니다."
                )

    def test_sales_statement_moved_out_of_shipment(self) -> None:
        # Sobo21(거래명세서)는 transactions 그룹 1건만 — shipment 그룹 중복 노출 금지.
        m = re.search(
            r'id:\s*"Sobo21"[\s\S]{0,300}?menuGroup:\s*"(?P<grp>\w+)"',
            self.src,
        )
        self.assertIsNotNone(m)
        self.assertEqual(m.group("grp"), "transactions")

    def test_sidebar_layouts_map_registers_transactions(self) -> None:
        block = re.search(
            r"export const SIDEBAR_LAYOUTS:[\s\S]*?=\s*\{(?P<body>[\s\S]*?)\};",
            self.src,
        )
        self.assertIsNotNone(block, "SIDEBAR_LAYOUTS 맵이 필요합니다.")
        body = block.group("body")
        self.assertIn("master: MASTER_SIDEBAR_LAYOUT", body)
        self.assertIn("transactions: TRANSACTIONS_SIDEBAR_LAYOUT", body)

    def test_id_conflict_aliases_keep_legacy_folder(self) -> None:
        # 셸 충돌 id 는 논리 id + 원본 Subu 폴더 유지 (dfm-layout-input.mdc).
        for fid, folder in (
            ("Sobo26_production_stmt", "Subu26"),
            ("Sobo27_production_status", "Subu27"),
            ("Sobo28_withholding", "Subu28"),
            ("Sobo29_new_release", "Subu29"),
        ):
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'"[\s\S]{0,120}?folder:\s*"' + re.escape(folder) + r'"',
                    self.src,
                )
                self.assertIsNotNone(m, f"{fid} → folder {folder} 매핑이 필요합니다.")


if __name__ == "__main__":
    from unittest import main

    main()
