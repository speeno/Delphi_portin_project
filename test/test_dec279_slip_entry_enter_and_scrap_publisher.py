"""DEC-279 — 전표 입력 화면 Enter 이어달리기 + 폐기 접수 출판사 칸 (2026-09-12).

교문사 보고(폐기 접수): ① 출판사코드가 반품과 같은 현상(자사만 검색됨) ② 「비고」에서 Enter 가 안 된다.
- ① 출판 계정은 Hcode 가 로그인 스코프로 정해져 있다(DEC-275 entry-profile). 칸을 띄우지 않는다.
- ② 헤더 폼 **마지막 칸**에서 Enter 는 다음 칸이 없어 아무 일도 하지 않았다. 레거시 Enter=다음 흐름대로
  라인 편집기 첫 칸으로 이어 간다(입고·출고·반품·폐기 접수 공용 `SlipEntryLayout`).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

_HUB = Path(__file__).resolve().parents[1]
_FE = _HUB / "도서물류관리프로그램" / "frontend" / "src"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class EnterHandoffTests(TestCase):
    def setUp(self) -> None:
        self.layout = _read(_FE / "components" / "transactions" / "slip-entry-layout.tsx")
        self.focus = _read(_FE / "lib" / "focus-advance.ts")

    def test_focus_helper_exposes_first_field_handoff(self) -> None:
        self.assertIn("export function focusFirstIn", self.focus)
        self.assertIn("FOCUSABLE_SELECTOR", self.focus)

    def test_layout_hands_off_to_line_editor(self) -> None:
        """헤더 안에서 이동했으면 그대로, 못 갔으면 라인 첫 칸."""
        self.assertIn("focusFirstIn(linesRef.current)", self.layout)
        self.assertIn("document.activeElement === before", self.layout)
        self.assertIn("<div ref={linesRef}>{lines}</div>", self.layout)

    def test_layout_still_respects_optouts(self) -> None:
        """기존 Enter 규약(헤더 Enter 끄기·자체 처리)은 그대로."""
        self.assertIn("if (!headerEnterAdvance || e.defaultPrevented) return;", self.layout)


class ScrapPublisherFieldTests(TestCase):
    def setUp(self) -> None:
        self.page = _read(_FE / "app" / "(app)" / "returns" / "scrap" / "new" / "page.tsx")

    def test_publisher_field_only_for_select_profile(self) -> None:
        self.assertIn('{publisherMode === "select" && (', self.page)
        self.assertIn("returnsApi\n      .entryProfile()", self.page.replace("\r\n", "\n"))

    def test_company_code_falls_back_to_login_scope(self) -> None:
        self.assertIn('const company = publisherMode === "select" ? hcode.trim() : loginHcode;', self.page)
        self.assertIn("returnHeader: { gdate, hcode: company", self.page)

    def test_scrap_legacy_axis_untouched(self) -> None:
        """폐기 식별 3요소(Gubun/Scode/Ocode)·음수 수량은 이번 변경 범위 밖 — 서버 규칙 그대로."""
        svc = _read(_HUB / "도서물류관리프로그램" / "backend" / "app" / "services" / "returns_service.py")
        self.assertIn("'폐기'", svc)
        self.assertIn("-abs(qty)", svc)


if __name__ == "__main__":
    main()
