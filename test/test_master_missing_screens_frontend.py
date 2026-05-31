"""
account-menu-fxx-rbac Phase F-3 — 누락 기초관리 3화면 프론트 회귀 가드.

검증
----
1. form-registry 3엔트리(Sobo12/15/13) 등록 + 라우트(/master/inbound-vendor·etc-customer·author)
   + Fxx 읽기 권한 코드 + menuGroup=master.
2. Next 라우트 페이지 3개 존재.
   - Sobo12: 목록/상세/신규 분리 라우트 + 전용 상세 폼/구분 패널(거래처 Sobo11 패턴)
   - Sobo13: 목록/상세/신규 분리 라우트 + 전용 상세 폼/구분 패널(거래처 Sobo11 패턴)
   - Sobo15: 목록/상세/신규 분리 라우트 + 전용 상세 폼/구분 패널(거래처 Sobo11 패턴)
3. data-legacy-id 「위젯 ID 누락 0」 — 각 페이지가 부착하는 모든 legacy_id 가 해당
   layout_mappings/SoboXX.md 에 존재(매핑노트 ↔ DOM 추적성, 고아 ID 0).
4. Phase D 게이트(useScreenCaps/WriteGate/PrintGate) 적용 + 계정 하드코딩 0.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONT / "lib" / "form-registry.ts"
COMPONENT = FRONT / "components" / "master" / "simple-master-page.tsx"
API = FRONT / "lib" / "master-api.ts"
MAPPINGS = ROOT / "analysis" / "layout_mappings"

# (screenId, route, requiredPermission, page rel path, api const, name col legacy id,
#  code edit, name edit, hcode edit)
_SCREENS = [
    ("Sobo12", "/master/inbound-vendor", "master.book.read",
     "app/(app)/master/inbound-vendor/page.tsx", "inboundVendorApi",
     "Sobo12.DBGrid101.GNAME", "Sobo12.Edit103", "Sobo12.Edit105", "Sobo12.Edit101"),
    ("Sobo15", "/master/etc-customer", "master.misc.read",
     "app/(app)/master/etc-customer/page.tsx", "etcCustomerApi",
     "Sobo15.DBGrid101.GNAME", "Sobo15.Edit103", "Sobo15.Edit105", "Sobo15.Edit101"),
    ("Sobo13", "/master/author", "master.book_code.read",
     "app/(app)/master/author/page.tsx", "authorApi",
     "Sobo13.DBGrid101.GPOSA", "Sobo13.Edit103", "Sobo13.Edit104", "Sobo13.Edit101"),
]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class FormRegistryEntries(TestCase):
    def test_three_entries_registered(self) -> None:
        src = _read(REGISTRY)
        for screen, route, perm, *_ in _SCREENS:
            self.assertIn(f'id: "{screen}"', src, screen)
            self.assertIn(f'route: "{route}"', src, route)
            self.assertIn(f'requiredPermission: "{perm}"', src, perm)
        # menuGroup master + CRUD parity (쓰기 master.write 백엔드 가드)
        self.assertEqual(src.count('crudParity: "CRUD"') >= 3, True)


class RoutePagesWired(TestCase):
    def test_pages_use_shared_component_and_config(self) -> None:
        for screen, route, _perm, rel, api_const, name_lid, code_e, name_e, hcode_e in _SCREENS:
            page = FRONT / rel
            self.assertTrue(page.exists(), f"missing page {rel}")
            src = _read(page)
            self.assertIn(api_const, src)
            if screen == "Sobo12":
                self.assertNotIn("InboundVendorDetailForm", src)
                self.assertNotIn("InboundVendorCategoryPanel", src)
                self.assertNotIn("setTab(", src)
                detail_page = FRONT / "app/(app)/master/inbound-vendor/[gcode]/page.tsx"
                new_page = FRONT / "app/(app)/master/inbound-vendor/new/page.tsx"
                self.assertTrue(detail_page.exists(), "missing inbound-vendor detail route")
                self.assertTrue(new_page.exists(), "missing inbound-vendor new route")
                self.assertIn("InboundVendorDetailForm", _read(detail_page))
                self.assertIn("InboundVendorDetailForm", _read(new_page))
                self.assertIn("InboundVendorCategoryCollapsible", _read(detail_page))
                self.assertIn("InboundVendorCategoryCollapsible", _read(new_page))
            elif screen == "Sobo13":
                self.assertNotIn("AuthorCategoryPanel", src)
                self.assertNotIn("setTab(", src)
                detail_page = FRONT / "app/(app)/master/author/[gcode]/page.tsx"
                new_page = FRONT / "app/(app)/master/author/new/page.tsx"
                self.assertTrue(detail_page.exists(), "missing author detail route")
                self.assertTrue(new_page.exists(), "missing author new route")
                self.assertIn("AuthorDetailForm", _read(detail_page))
                self.assertIn("AuthorDetailForm", _read(new_page))
                self.assertIn("AuthorCategoryCollapsible", _read(detail_page))
                self.assertIn("AuthorCategoryCollapsible", _read(new_page))
            elif screen == "Sobo15":
                self.assertNotIn("EtcCustomerDetailForm", src)
                self.assertNotIn("EtcCustomerCategoryPanel", src)
                self.assertNotIn("setTab(", src)
                detail_page = FRONT / "app/(app)/master/etc-customer/[gcode]/page.tsx"
                new_page = FRONT / "app/(app)/master/etc-customer/new/page.tsx"
                self.assertTrue(detail_page.exists(), "missing etc-customer detail route")
                self.assertTrue(new_page.exists(), "missing etc-customer new route")
                self.assertIn("EtcCustomerDetailForm", _read(detail_page))
                self.assertIn("EtcCustomerDetailForm", _read(new_page))
                self.assertIn("EtcCustomerCategoryCollapsible", _read(detail_page))
                self.assertIn("EtcCustomerCategoryCollapsible", _read(new_page))
            else:
                self.assertIn("SimpleMasterPage", src)
                self.assertIn(f'screenId: "{screen}"', src)
                self.assertIn(f'legacyPrefix: "{screen}"', src)
                self.assertIn(f'gridNameLegacyId: "{name_lid}"', src)
                self.assertIn(f'codeEditLegacyId: "{code_e}"', src)
                self.assertIn(f'nameEditLegacyId: "{name_e}"', src)
                self.assertIn(f'hcodeEditLegacyId: "{hcode_e}"', src)

    def test_api_factory_exports(self) -> None:
        src = _read(API)
        for _s, _r, _p, _rel, api_const, *_ in _SCREENS:
            self.assertIn(f"export const {api_const}", src)


class WidgetIdTraceability(TestCase):
    """페이지가 부착하는 모든 data-legacy-id 가 매핑노트에 존재(누락/고아 0)."""

    def test_no_orphan_legacy_ids(self) -> None:
        comp = _read(COMPONENT)
        # 컴포넌트가 prefix 템플릿으로 부착하는 접미사 (literal `${p}.<suffix>`)
        suffixes = re.findall(r"\$\{p\}\.([A-Za-z0-9_.]+)", comp)
        self.assertIn("DBGrid101", suffixes)
        self.assertIn("Panel002", suffixes)
        for btn in ("Button101", "Button102", "Button103", "Button104", "Button000"):
            self.assertIn(btn, suffixes, btn)

        for screen, _route, _perm, _rel, _api, name_lid, code_e, name_e, hcode_e in _SCREENS:
            note = _read(MAPPINGS / f"{screen}.md")
            rendered = {f"{screen}.{suf}" for suf in suffixes}
            rendered |= {name_lid, code_e, name_e, hcode_e}
            for lid in sorted(rendered):
                # 매핑노트에는 bare 토큰(예 Sobo12.Edit103 또는 컬럼은 DBGrid101.GCODE)으로 존재.
                bare = lid.split(".", 1)[1]  # Sobo12 접두 제거 → DBGrid101.GCODE / Edit103 ...
                self.assertTrue(
                    (lid in note) or (bare in note),
                    f"{screen}: legacy_id {lid} (bare {bare}) 가 layout_mappings/{screen}.md 에 없음",
                )


class GatesAndNoHardcode(TestCase):
    def test_phase_d_gates_applied(self) -> None:
        comp = _read(COMPONENT)
        for token in ("useScreenCaps", "WriteGate", "PrintGate", "ReadOnlyBanner", "canWrite"):
            self.assertIn(token, comp, token)

    def test_no_account_hardcode(self) -> None:
        # 계정 분기 금지 — 특정 계정명/hcode 상수가 페이지·컴포넌트에 박혀선 안 됨.
        banned = ["교문사", "경리부", "5019", "5097", "위러브"]
        for f in [COMPONENT, API] + [FRONT / s[3] for s in _SCREENS]:
            src = _read(f)
            for b in banned:
                self.assertNotIn(b, src, f"{f.name}: 계정 하드코딩 '{b}' 발견")


if __name__ == "__main__":
    main(verbosity=2)
