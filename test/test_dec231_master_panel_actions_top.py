"""DEC-231 — 구분/지점 관리 패널의 액션 버튼이 편집 카드 상단 헤더에 있어야 한다 (2026-08-27 사용자 지적)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "master"
PANELS = ("author-category-panel.tsx", "book-category-panel.tsx", "inbound-vendor-category-panel.tsx",
          "customer-branch-panel.tsx", "customer-category-panel.tsx", "etc-customer-category-panel.tsx", "simple-master-page.tsx")


class PanelActionsOnTop(TestCase):
    def test_header_row_precedes_fields(self) -> None:
        for name in PANELS:
            src = (MASTER / name).read_text(encoding="utf-8")
            hdr = src.index('{selected ? "선택 항목 수정" : "신규 등록"}')
            card = src.rindex('space-y-3 rounded-2xl border border-border bg-card p-4 shadow-sm"', 0, hdr)
            self.assertLess(card, hdr, name)
            # 헤더 뒤에 오는 첫 필드 라벨은 헤더보다 뒤
            first_label = src.index("<Label", hdr)
            self.assertLess(hdr, first_label, name)
            self.assertEqual(src.count('{selected ? "선택 항목 수정" : "신규 등록"}'), 1, name)
            self.assertNotIn('variant="secondary"', src[hdr: hdr + 2500], f"{name}: 저장은 검정(기본) 버튼")
            self.assertIn("border-destructive/40 text-destructive", src, f"{name}: 삭제 outline-destructive")


if __name__ == "__main__":
    main()
