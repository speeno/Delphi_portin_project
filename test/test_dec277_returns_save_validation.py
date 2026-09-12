"""DEC-277 — 반품 접수 저장 사전 검증·오류 문구 가드 (2026-09-12).

교문사 보고: 「저장 실패: 422」. 원인은 수량 0 라인(`ReturnLineInput.gsqut ge=1`)이며,
FastAPI 422 의 detail 은 «배열»이라 화면의 `detail.message` 폴백이 상태코드만 보여 줬다.
폐기 접수에 이미 있던 사전 검증을 반품 접수에도 두고, 두 화면 모두 공용 `formatApiError`
(422 배열 → 「필드 — 사유」)를 쓰게 한다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
_APP = _HUB / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
sys.path.insert(0, str(_BACKEND))


def _read(rel: Path) -> str:
    return rel.read_text(encoding="utf-8")


class ReturnsSaveValidationTests(TestCase):
    def setUp(self) -> None:
        self.receipt = _read(_APP / "returns" / "receipts" / "new" / "page.tsx")
        self.scrap = _read(_APP / "returns" / "scrap" / "new" / "page.tsx")

    def test_quantity_zero_blocked_before_request(self) -> None:
        """수량 0 = 서버 422. 두 화면 모두 저장 전에 한국어로 막는다."""
        for src, name in ((self.receipt, "반품접수"), (self.scrap, "폐기접수")):
            self.assertIn("Number(l.gsqut)", src, f"{name}: 수량 0 사전 검증 없음")
            self.assertIn("수량이 0인 라인이 있습니다", src, f"{name}: 안내 문구 없음")

    def test_save_error_uses_shared_formatter(self) -> None:
        """422 detail 은 배열 — detail.message 폴백이면 「저장 실패: 422」 만 보인다."""
        for src, name in ((self.receipt, "반품접수"), (self.scrap, "폐기접수")):
            self.assertIn("formatApiError(e)", src, f"{name}: 공용 포맷터 미사용")
            self.assertNotIn("?.message ?? e.status", src, f"{name}: 옛 폴백 잔존")

    def test_backend_still_requires_positive_quantity(self) -> None:
        """사전 검증은 편의일 뿐 — 서버 계약(gsqut ≥ 1)은 그대로여야 한다(fail-closed)."""
        from app.models.returns import ReturnLineInput

        f = ReturnLineInput.model_fields["gsqut"]
        metas = [getattr(m, "ge", None) for m in getattr(f, "metadata", [])]
        self.assertIn(1, metas, "gsqut ge=1 계약이 사라졌다")


if __name__ == "__main__":
    main()
