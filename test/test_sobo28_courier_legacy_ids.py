"""
DEC-028 — Sobo28 택배관리(shipping/courier) data-legacy-id 회귀 가드.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT
    / "도서물류관리프로그램"
    / "frontend"
    / "src"
    / "app"
    / "(app)"
    / "shipping"
    / "courier"
    / "page.tsx"
)


def _legacy_ids_from_mapping_md() -> list[str]:
    """analysis/layout_mappings/Sobo28.md §8 블록에서 공백 구분 id 목록 추출."""
    md = ROOT / "analysis" / "layout_mappings" / "Sobo28.md"
    text = md.read_text(encoding="utf-8")
    if "```" not in text:
        return []
    block = text.split("## 8. 회귀 검사용 legacy_id 목록")[-1]
    if "```" not in block:
        return []
    chunk = block.split("```", 2)[1]
    return [x for x in re.split(r"\s+", chunk.strip()) if x]


class TestSobo28CourierLegacyIds(unittest.TestCase):
    def test_page_contains_mapping_legacy_ids(self) -> None:
        required = _legacy_ids_from_mapping_md()
        self.assertTrue(required, "layout_mappings/Sobo28.md §8 이 비었습니다.")
        src = PAGE.read_text(encoding="utf-8")
        missing = [lid for lid in required if lid not in src]
        self.assertEqual(missing, [], f"shipping/courier/page.tsx에 누락: {missing}")


if __name__ == "__main__":
    unittest.main()
