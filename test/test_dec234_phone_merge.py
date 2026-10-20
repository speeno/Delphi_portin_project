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
        labels = dict(re.findall(r'\{\s*key: "(\w+)",\s*label: "([^"]+)"', grid))
        catalog = {c["key"]: c["label"] for c in mx.customer_field_catalog()}
        # 그리드 키 → 카탈로그 키 대응(합본 가상 키)
        alias = {"gtel1": "gtel", "gfax1": "gfax", "sname": "gbun_name"}
        mismatch = set()
        for k, lbl in labels.items():
            ck = alias.get(k, k)
            if ck in catalog and catalog[ck] != lbl:
                mismatch.add((k, lbl, catalog[ck]))
        # 전화 합본(gtel)은 화면 · 엑셀 같은 「전화」.
        self.assertEqual((labels["gtel1"], catalog["gtel"]), ("전화", "전화"))
        # DEC-412: 프론트 재설계(M-DEC-15) 운영 반영 — 화면 라벨이 폼 라벨로 바뀌고 엑셀(백엔드 카탈로그)은
        # 아직 DEC-292 약식 라벨이다. 아래 차이만 허용(백엔드 카탈로그 라벨 변경 시 줄인다) — 새 차이는 실패.
        # 목록은 test_dec292_customer_list_fields.LABEL_DIFF_PENDING 과 같다.
        pending = {
            ("grat9", "상태", "정지"), ("gcode", "거래처코드", "코드"), ("jubun", "거래처 지역", "지역"),
            ("gnumb", "사업자번호", "사업자등록번호"), ("gpper", "담당자", "담당자1"), ("gphon", "휴대전화", "핸드폰"),
            ("gfax1", "팩스번호", "팩스"), ("gjuso", "주소1", "주소"), ("email", "이메일1", "E-mail"),
            ("yesno", "계산서", "발행유무"), ("name2", "담당", "담당자2"),
        }
        self.assertLessEqual(mismatch, pending, "엑셀 헤더 ≠ 거래처 관리 화면 라벨 — 허용 목록 밖")


class FormsAndCta(TestCase):
    def test_forms_use_single_phone_field(self) -> None:
        # DEC-412: 프론트 재설계 M-DEC-27 — 의도적 제거: 저자관리 전화번호 칸 → 「담당」.
        # 저자 폼의 PhoneField 개수는 저자 화면 소관(팩스는 반드시 한 칸 PhoneField) — 1~2 개를 허용한다.
        for name in ("customer-detail-form.tsx", "inbound-vendor-detail-form.tsx", "etc-customer-detail-form.tsx", "author-detail-form.tsx"):
            src = (FRONT / "components" / "master" / name).read_text(encoding="utf-8")
            self.assertNotIn("PairField", src, name)
            n = src.count("<PhoneField")
            if name == "author-detail-form.tsx":
                self.assertIn(n, (1, 2), name)
                self.assertRegex(src, r'<PhoneField\s+label="팩스번호"', name)
            else:
                self.assertEqual(n, 2, name)
            self.assertIn('legacyId1="', src, name)

    def test_new_customer_cta_is_brand_primary(self) -> None:
        # DEC-412: 프론트 재설계(M-DEC-1) 운영 반영 — 「신규 등록」(Sobo11.Button101)은 목록 · 상세 · 신규 공용
        # 헤더(CustomerMasterListHeader)의 제목 옆 외곽선 버튼(Figma). 라임 채움 CTA 는 의도적 제거 — 검색 입력보다 앞.
        header = (FRONT / "components" / "master" / "customer-master-list-header.tsx").read_text(encoding="utf-8")
        i = header.index('data-legacy-id="Sobo11.Button101"')
        tag = header[header.rindex("<Button", 0, i): i]
        self.assertIn("router.push(\"/master/customer/new\")", tag)
        self.assertIn("disabled={!canWrite}", tag)
        self.assertNotIn('variant="secondary"', tag)
        self.assertLess(i, header.index("<MasterSearchQueryField"), "검색 입력창 앞")
        page = (FRONT / "app" / "(app)" / "master" / "customer" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("<CustomerMasterListHeader", page)
        self.assertNotIn("hideNewButton", page, "목록에서는 신규 등록 버튼을 보인다")
        self.assertLessEqual(page.count('variant="brand-primary"') + header.count('variant="brand-primary"'), 1,
                             "화면당 라임 CTA 최대 1개")

if __name__ == "__main__":
    main()
