"""DEC-337 — 「택배관리」 대메뉴 제거(사용자 2026-09-25). 그룹의 유일 화면을 hiddenFromMenu 로 감춰 빈 그룹 미렌더.

라우트(/shipping/courier)·레지스트리·권한은 보존(직접 링크는 열림, DEC-309/331 취지).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class DeliveryMenuHidden(TestCase):
    def test_only_delivery_form_hidden(self):
        reg = (FE / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        entries = re.findall(r'\{\s*id: "[^"]+",.*?\n  \},', reg, re.S)
        delivery = [e for e in entries if 'menuGroup: "delivery"' in e]
        self.assertEqual(len(delivery), 1)
        self.assertIn('id: "Sobo28_delivery"', delivery[0])
        self.assertIn("hiddenFromMenu: true", delivery[0])
        self.assertIn('route: "/shipping/courier"', delivery[0])

    def test_sidebar_skips_empty_group(self):
        sb = (FE / "components" / "app-shell" / "sidebar.tsx").read_text(encoding="utf-8")
        self.assertIn("if (form.hiddenFromMenu) return false;", sb)
        self.assertIn("if (forms.length === 0) return null;", sb)


if __name__ == "__main__":
    main(verbosity=2)
