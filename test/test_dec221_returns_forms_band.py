"""DEC-221 — 폐기·반품 접수 신규 입력의 헤더 입력이 제목 띠 안에 있어야 한다 (2026-08-27 사용자 지적)."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"


class ReturnsFormsHeaderInBand(TestCase):
    def _band(self, rel: str) -> str:
        # DEC-240 — 반품·폐기 신규는 공용 골격(SlipEntryLayout)이 띠를 그린다. 헤더 폼 슬롯을 띠로 본다.
        src = (FRONT / rel).read_text(encoding="utf-8")
        i = src.index("headerForm={")
        return src[i: src.index("linesTitle=", i)]

    def test_scrap_new(self) -> None:
        band = self._band("returns/scrap/new/page.tsx")
        self.assertIn('headerFormLegacyId="Sobo23_scrap.Panel201"', (FRONT / "returns/scrap/new/page.tsx").read_text(encoding="utf-8"))
        for lid in ("Sobo23_scrap.Edit202", "Sobo23_scrap.Edit203", "Sobo23_scrap.Edit204", "Sobo23_scrap.Edit_Gcode", "Sobo23_scrap.Edit206"):
            self.assertIn(lid, band, lid)
        self.assertNotIn("text-gray-600", band)

    def test_returns_new(self) -> None:
        band = self._band("returns/receipts/new/page.tsx")
        self.assertIn('headerFormLegacyId="Sobo23.Panel201"', (FRONT / "returns/receipts/new/page.tsx").read_text(encoding="utf-8"))
        for lid in ("Sobo23.Edit202", "Sobo23.Edit203", "Sobo23.Edit204", "Sobo23.Edit206"):
            self.assertIn(lid, band, lid)

    def test_no_header_card_below_band(self) -> None:
        for rel in ("returns/scrap/new/page.tsx", "returns/receipts/new/page.tsx"):
            src = (FRONT / rel).read_text(encoding="utf-8")
            after = src[src.index("linesTitle="):]
            self.assertNotIn('variant="memo"\n        className="grid', after, rel)
            self.assertNotIn('<SurfacePanel variant="memo" className="grid', after, rel)


if __name__ == "__main__":
    main()
