from __future__ import annotations

from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MasterLookupDialogStaticTest(TestCase):
    def test_lookup_config_has_required_kinds(self) -> None:
        src = _read(FRONT / "lib" / "master-lookup-config.ts")
        for kind in ('customer', 'book', 'inboundVendor'):
            self.assertIn(f'{kind}: {{', src)
        self.assertIn("MASTER_LOOKUP_CONFIGS", src)
        self.assertIn("rowKey: (row, index)", src)
        self.assertIn(":${index}`", src)

    def test_dialog_contains_core_elements(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-lookup-dialog.tsx")
        for kw in ("DataGrid<MasterLookupRow>", "Input", "Button", 'event.key === "Escape"', "onSelect"):
            self.assertIn(kw, src)
        self.assertIn("CommonLookupDialog.SearchInput", src)
        self.assertIn("CommonLookupDialog.SelectButton", src)

    def test_dialog_has_mobile_responsive_classes(self) -> None:
        src = _read(FRONT / "components" / "master" / "master-lookup-dialog.tsx")
        for cls in ("fixed inset-x-2 top-8 bottom-2", "sm:w-[min(960px,96vw)]", "sm:max-h-[88vh]", "overflow-auto"):
            self.assertIn(cls, src)

    def test_representative_pages_use_lookup_button(self) -> None:
        customer = _read(FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx")
        book = _read(FRONT / "app" / "(app)" / "master" / "book" / "page.tsx")
        inbound = _read(FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "page.tsx")

        self.assertIn("MasterLookupButton", customer)
        self.assertIn('lookupKind="customer"', customer)

        self.assertIn("MasterLookupButton", book)
        self.assertIn('lookupKind="book"', book)

        self.assertIn("MasterLookupButton", inbound)
        self.assertIn('lookupKind="inboundVendor"', inbound)
