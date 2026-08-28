"""DEC-234 — 전화/팩스 한 칸 통합, 엑셀 합본 export/import, 헤더=화면 라벨, 신규 거래처 CTA (2026-08-28)."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import masters_excel as mx  # noqa: E402


class SplitJoin(TestCase):
    def test_split_rules(self) -> None:
        self.assertEqual(mx.split_phone("02-737-6111"), ("02", "737-6111"))
        self.assertEqual(mx.split_phone("031 123 4567"), ("031", "123 4567"))
        self.assertEqual(mx.split_phone("010-1234-5678"), ("010", "1234-5678"))
        self.assertEqual(mx.split_phone("0505-123-4567"), ("0505", "123-4567"))
        self.assertEqual(mx.split_phone("1588-1234"), ("", "1588-1234"))
        self.assertEqual(mx.split_phone(""), ("", ""))
        self.assertEqual(mx.join_phone("02", "737-6111"), "02-737-6111")
        self.assertEqual(mx.join_phone("", "1588-1234"), "1588-1234")

    def test_frontend_rule_identical(self) -> None:
        ts = (FRONT / "lib" / "phone-format.ts").read_text(encoding="utf-8")
        py_re = re.search(r'_PHONE_AREA_RE = re\.compile\(r"(.+?)"\)', mx.__file__ and Path(mx.__file__).read_text(encoding="utf-8")).group(1)
        ts_re = re.search(r"const AREA_RE = /(.+?)/;", ts).group(1)
        self.assertEqual(py_re.replace("\\\\", "\\"), ts_re)

    def test_import_expands_virtual_keys_and_accepts_legacy_headers(self) -> None:
        row = mx.expand_phone_fields({"gname": "가", "gtel": "02-737-6111", "gfax": ""})
        self.assertEqual((row["gtel1"], row["gtel2"], row["gfax1"], row["gfax2"]), ("02", "737-6111", "", ""))
        self.assertNotIn("gtel", row)
        self.assertEqual(mx.CUSTOMER_IMPORT_MAP["전화번호"], "gtel")
        self.assertEqual(mx.CUSTOMER_IMPORT_MAP["전화번호1"], "gtel1")
        self.assertEqual(mx.CUSTOMER_IMPORT_MAP["사업자번호"], "gnumb")
        self.assertNotIn("gjuso", mx.CUSTOMER_IMPORT_MAP.values(), "합본 주소는 읽기전용")
        self.assertEqual(mx.INBOUND_VENDOR_IMPORT_MAP["팩스번호"], "gfax")

    def test_catalog_headers_match_grid_labels(self) -> None:
        grid = (FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx").read_text(encoding="utf-8")
        labels = dict(re.findall(r'key: "(\w+)",\s*\n\s*label: "([^"]+)"', grid))
        catalog = {c["key"]: c["label"] for c in mx.customer_field_catalog()}
        # 그리드 키 → 카탈로그 키 대응(합본 가상 키)
        alias = {"gtel1": "gtel", "gfax1": "gfax", "sname": "gbun_name"}
        mismatch = []
        for k, lbl in labels.items():
            ck = alias.get(k, k)
            if ck in catalog and catalog[ck] != lbl:
                mismatch.append((k, lbl, catalog[ck]))
        self.assertEqual(mismatch, [], "엑셀 헤더는 거래처현황 화면 라벨과 동일해야 한다")


class FormsAndCta(TestCase):
    def test_forms_use_single_phone_field(self) -> None:
        for name in ("customer-detail-form.tsx", "inbound-vendor-detail-form.tsx", "etc-customer-detail-form.tsx", "author-detail-form.tsx"):
            src = (FRONT / "components" / "master" / name).read_text(encoding="utf-8")
            self.assertNotIn("PairField", src, name)
            self.assertEqual(src.count("<PhoneField"), 2, name)
            self.assertIn('legacyId1="', src, name)

    def test_new_customer_cta_is_brand_primary(self) -> None:
        src = (FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx").read_text(encoding="utf-8")
        i = src.index('data-legacy-id="Sobo11.Button101"')
        tag = src[src.rindex("<Button", 0, i): i]
        self.assertIn('variant="brand-primary"', tag)
        self.assertNotIn('variant="secondary"', tag)


if __name__ == "__main__":
    main()
