"""
DEC-024 — 표준 paging 헬퍼 단위 검증.

목적
----
``app/core/pagination.py`` 의 ``clamp_limit`` / ``clamp_offset`` /
``build_page`` / ``with_page`` / ``PageMeta`` 가 시나리오 무관하게
일관된 계약을 지키는지 회귀 가드한다.

부수 검증
- `with_page(legacy_flat=True)` 는 C2/C6 1차 BC 평면 필드를 함께 반환.
- `has_more` 는 (offset+returned < total) OR (returned >= limit && total==0)
  두 신호 OR — total 이 부정확한 경로(예: mysql3 의 가벼운 list)에서도 다음 페이지
  존재 가능성을 보수적으로 표시.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.pagination import (  # noqa: E402
    DEFAULT_CEIL,
    DEFAULT_LIMIT,
    PageMeta,
    build_page,
    clamp_limit,
    clamp_offset,
    with_page,
)


class ClampLimitTests(TestCase):
    def test_none_returns_default(self) -> None:
        self.assertEqual(clamp_limit(None), DEFAULT_LIMIT)

    def test_zero_returns_default(self) -> None:
        self.assertEqual(clamp_limit(0), DEFAULT_LIMIT)

    def test_negative_returns_default(self) -> None:
        self.assertEqual(clamp_limit(-3), DEFAULT_LIMIT)

    def test_above_ceil_clamps(self) -> None:
        self.assertEqual(clamp_limit(10_000), DEFAULT_CEIL)

    def test_custom_ceil(self) -> None:
        self.assertEqual(clamp_limit(5_000, ceil=2000), 2000)

    def test_custom_default(self) -> None:
        self.assertEqual(clamp_limit(None, default=20), 20)

    def test_invalid_string(self) -> None:
        self.assertEqual(clamp_limit("abc"), DEFAULT_LIMIT)  # type: ignore[arg-type]


class ClampOffsetTests(TestCase):
    def test_none_returns_zero(self) -> None:
        self.assertEqual(clamp_offset(None), 0)

    def test_negative_returns_zero(self) -> None:
        self.assertEqual(clamp_offset(-50), 0)

    def test_positive_passthrough(self) -> None:
        self.assertEqual(clamp_offset(120), 120)

    def test_invalid_string(self) -> None:
        self.assertEqual(clamp_offset("xx"), 0)  # type: ignore[arg-type]


class BuildPageTests(TestCase):
    def test_basic_no_more(self) -> None:
        p = build_page(limit=100, offset=0, total=37, returned=37)
        self.assertEqual(
            p, {"limit": 100, "offset": 0, "total": 37, "has_more": False}
        )

    def test_more_via_total(self) -> None:
        p = build_page(limit=100, offset=0, total=250, returned=100)
        self.assertTrue(p["has_more"])

    def test_more_via_total_zero_signal(self) -> None:
        # mysql3 경로 — total 부정확/0 인데 page 가 가득 찼으면 보수적으로 has_more=True.
        p = build_page(limit=50, offset=0, total=0, returned=50)
        self.assertTrue(p["has_more"])

    def test_last_page(self) -> None:
        p = build_page(limit=100, offset=200, total=250, returned=50)
        self.assertFalse(p["has_more"])
        self.assertEqual(p["offset"], 200)


class WithPageTests(TestCase):
    def test_default_only_page_object(self) -> None:
        out = with_page(items=[1, 2], limit=100, offset=0, total=2)
        self.assertIn("items", out)
        self.assertIn("page", out)
        self.assertNotIn("total", out)
        self.assertNotIn("limit", out)
        self.assertNotIn("offset", out)

    def test_legacy_flat_emits_bc_fields(self) -> None:
        out = with_page(
            items=["a", "b", "c"], limit=100, offset=0, total=3, legacy_flat=True
        )
        self.assertEqual(out["total"], 3)
        self.assertEqual(out["limit"], 100)
        self.assertEqual(out["offset"], 0)
        self.assertEqual(out["page"]["total"], 3)


class PageMetaModelTests(TestCase):
    def test_round_trip(self) -> None:
        m = PageMeta(limit=100, offset=50, total=275, has_more=True)
        d = m.model_dump()
        self.assertEqual(d["limit"], 100)
        self.assertEqual(d["offset"], 50)
        self.assertEqual(d["total"], 275)
        self.assertTrue(d["has_more"])


if __name__ == "__main__":
    main()
