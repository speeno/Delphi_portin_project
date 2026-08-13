"""DEC-152 — 출고검증 메뉴 총판(물류) 전용 노출 회귀 가드.

2026-08-13 사용자: 출고검증(1)/(2)/(개별) 메뉴는 총판(물류) 계정에만 표시.
게이팅은 확립된 `distributorOnly` 패턴(Sobo39 출고내역서 선례) — 사이드바
isVisibleForm 이 `form.distributorOnly && !isDistributorViewer(user)` 면 숨김.
isDistributorViewer = account_type T2_DIST | build_role distributor | 슈퍼유저.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONTEND / "lib" / "form-registry.ts"


def _entry_block(src: str, form_id: str) -> str:
    m = re.search(rf'\{{\n(?:[^{{}}]|\{{[^{{}}]*\}})*?id: "{form_id}",.*?\n  \}},', src, re.S)
    assert m, form_id
    return m.group(0)


class VerificationDistributorOnlyGuard(TestCase):
    def test_all_verification_entries_distributor_only(self) -> None:
        src = REGISTRY.read_text(encoding="utf-8")
        for fid in (
            "Sobo59_1",
            "Sobo59_2",
            "Sobo59_3",
            "Sobo59_verification_shipment_alias",
        ):
            block = _entry_block(src, fid)
            self.assertIn("distributorOnly: true", block, f"{fid} 총판 전용 게이팅")

    def test_sidebar_enforces_distributor_only(self) -> None:
        src = (FRONTEND / "components" / "app-shell" / "sidebar.tsx").read_text(
            encoding="utf-8"
        )
        self.assertIn("form.distributorOnly && !isDistributor", src)

    def test_precedent_screen_unchanged(self) -> None:
        # ※ id "Sobo39" 는 할인율 화면과 중복 사용 중 — 캡션으로 출고내역서 블록 특정.
        src = REGISTRY.read_text(encoding="utf-8")
        i = src.index('caption: "출고내역서"')
        block = src[i : i + 400]
        self.assertIn("distributorOnly: true", block, "선례(출고내역서) 게이팅 유지")


if __name__ == "__main__":
    main()
