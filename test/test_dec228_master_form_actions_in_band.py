"""DEC-228 — 마스터 상세/신규 화면의 등록·저장·삭제가 제목 띠 actions 에 있어야 한다 (2026-08-27 사용자 지적)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
FAMILIES = (
    ("customer", "customer-detail-form.tsx", "CustomerFormActions", "Sobo11"),
    ("inbound-vendor", "inbound-vendor-detail-form.tsx", "InboundVendorFormActions", "Sobo12"),
    ("etc-customer", "etc-customer-detail-form.tsx", "EtcCustomerFormActions", "Sobo15"),
)


class FormsHaveNoBottomBar(TestCase):
    def test_actions_component_exported_and_bottom_bar_gone(self) -> None:
        for _, form, comp, pid in FAMILIES:
            src = (FRONT / "components" / "master" / form).read_text(encoding="utf-8")
            self.assertIn(f"export function {comp}(", src, form)
            body = src[: src.index(f"export function {comp}(")]
            for n in ("101", "102", "103"):
                self.assertNotIn(f'data-legacy-id="{pid}.Button{n}"', body, f"{form}: 폼 본문에 버튼 잔존")
                self.assertIn(f'data-legacy-id="{pid}.Button{n}"', src, f"{form}: 레거시 id 유지")
            self.assertNotIn("  onSave: () => void;\n", body, "폼 Props 에서 액션 콜백 제거")


class PagesRenderActionsInBand(TestCase):
    def test_band_actions(self) -> None:
        for family, _, comp, _ in FAMILIES:
            for sub, expect in (("[gcode]", "onSave={save} onDelete={handleDelete}"), ("new", "createMode onCreate={handleCreate}")):
                src = (FRONT / "app" / "(app)" / "master" / family / sub / "page.tsx").read_text(encoding="utf-8")
                band = src[src.index("<PageHeader"): src.index("\n      />", src.index("<PageHeader")) + 8]
                self.assertIn(f"actions={{<{comp} caps={{caps}} canWrite={{canWrite}}", band, f"{family}/{sub}")
                self.assertIn(expect, band, f"{family}/{sub}")


if __name__ == "__main__":
    main()
