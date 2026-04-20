"""
C11 모바일/태블릿 UAT Phase 1 — 반응형 + 스캐너 충돌 + 데스크톱 회귀 가드 정적 회귀 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/mobile_uat.yaml v1.0.0 (디바이스 5 × 시나리오 4 매트릭스 + AC 5종)
- analysis/screen_cards/C11_Mobile_UAT.md (DoD 4종 + 결정 게이트)
- analysis/handlers/extension_dependencies.md (C11 진입 게이트 — C2/C8 회귀)
- legacy-analysis/decisions.md DEC-044 (외부 시스템 연동 제외 + 신규 SQL 0건 정책)
- frontend/src/components/shared/scan-input.tsx (터치 영역 + 모바일 친화 input attrs)
- frontend/src/lib/scanner.ts (DEC-004 USB-HID — 가상 키보드 충돌 방지 정합)

검증 케이스 (~20건 — 5 디바이스 × 4 시나리오 매트릭스 + 정합)
------------------------------------------------------------
정적 가드 매트릭스 (T5 무관 — 항상 실행)
- TC-C11-S-01  mobile_uat.yaml v1.0 frozen + AC-MOB-1~5 + constraints.external_integrations=excluded
- TC-C11-S-02  device_matrix 5 등록 (ipad_pro_15/17, galaxy_tab_s8/s9, pixel_8) + viewport 명시
- TC-C11-S-03  scenario_matrix 4 등록 (C2/C3/C4/C8) + 각 page_path 의 실제 파일 존재
- TC-C11-S-04  breakpoint_isolation_policy BPI-1~4 등록 + enforcement.static_check 명령 명시
- TC-C11-S-05  scanner_conflict_cases SC-1~3 등록 (모바일 가상 키보드 충돌 방지)
- TC-C11-S-06  decisions DEC-MOB-1, DEC-MOB-2 등록 + open_questions OQ-MOB-1
- TC-C11-S-07  ScanInput 의 input min-h-[44px] (Apple HIG 터치 영역 ≥ 44pt) 반영
- TC-C11-S-08  ScanInput 의 mobile attrs (autoCapitalize/autoCorrect/inputMode) 반영
- TC-C11-S-09  ScanInput 의 BPI-3 정합 (sm: prefix 로 desktop 잠금 — sm:py-1.5/sm:text-sm)
- TC-C11-S-10  scanner.ts 의 wedge interval/idle reset 임계 (DEC-004) 변경 0건 — Phase 1 22 케이스 정합

회귀 매트릭스 (5 디바이스 × 4 시나리오 = 20 cell — 모두 정합 검증)
- TC-C11-M-01..20  device × scenario 셀 검증 (각 디바이스가 4 시나리오 page_path 모두 매트릭스에 노출)

의존성 게이트 (extension_dependencies.md)
- TC-C11-D-01  extension_dependencies.md 에 C11 → C2/C4/C8/C10 선행 자산표 등록
- TC-C11-D-02  extension_dependencies.md 진입 게이트 §4 의 C11 행 (C2/C4/C8 desktop 동작 PASS, lib/scanner.ts Phase 1 회귀 22 PASS) 명시

설계 정합 (사용자 룰)
---------------------
- C8 Phase 1 패턴(test_c8_scan_phase1.py) 동일 — 정적 grep 위주 + 신규 헬퍼 금지.
- DEC-044 정합: 외부 시스템 연동 제외, 신규 SQL 0건 (모바일 UAT 는 UI/CSS 위주).
- 디바이스 emulation/Playwright 의존 추가 금지 (Phase 1 — 정적 회귀).
- T5 미착수 시점에도 모든 정적 케이스 실행 가능 (S/M/D 모두 backend import 무관).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
CONTRACT = ROOT / "migration" / "contracts" / "mobile_uat.yaml"
SCREEN_CARD = ROOT / "analysis" / "screen_cards" / "C11_Mobile_UAT.md"
DEPS_DOC = ROOT / "analysis" / "handlers" / "extension_dependencies.md"
DECISIONS_DOC = ROOT / "legacy-analysis" / "decisions.md"
SCAN_INPUT = FRONTEND_SRC / "components" / "shared" / "scan-input.tsx"
SCANNER_LIB = FRONTEND_SRC / "lib" / "scanner.ts"

DEVICES = ["ipad_pro_15", "ipad_pro_17", "galaxy_tab_s8", "galaxy_tab_s9", "pixel_8"]
SCENARIO_PAGES = {
    "C2_outbound_orders": FRONTEND_SRC / "app" / "(app)" / "outbound" / "orders" / "page.tsx",
    "C3_inbound_receipts": FRONTEND_SRC / "app" / "(app)" / "inbound" / "receipts" / "page.tsx",
    "C4_returns_receipts": FRONTEND_SRC / "app" / "(app)" / "returns" / "receipts" / "page.tsx",
    "C8_scan_match": FRONTEND_SRC / "components" / "shared" / "scan-input.tsx",
}


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ──────────────────────────────────────────────
# S — 정적 가드 매트릭스 (10 케이스)
# ──────────────────────────────────────────────
class StaticGuardTests(TestCase):
    """T5/T6 무관 — 컨트랙트·문서·CSS·컴포넌트 정합."""

    @classmethod
    def setUpClass(cls) -> None:
        assert CONTRACT.exists(), f"missing contract: {CONTRACT}"
        assert SCREEN_CARD.exists(), f"missing screen card: {SCREEN_CARD}"
        assert DEPS_DOC.exists(), f"missing dependency doc: {DEPS_DOC}"
        assert DECISIONS_DOC.exists(), f"missing decisions doc: {DECISIONS_DOC}"
        assert SCAN_INPUT.exists(), f"missing scan-input: {SCAN_INPUT}"
        assert SCANNER_LIB.exists(), f"missing scanner.ts: {SCANNER_LIB}"
        cls.contract = _read(CONTRACT)
        cls.scan_input = _read(SCAN_INPUT)
        cls.scanner_lib = _read(SCANNER_LIB)
        cls.deps_doc = _read(DEPS_DOC)

    def test_S_01_contract_v1_frozen_constraints(self) -> None:
        """TC-C11-S-01 — contract v1.0 동결 + AC-MOB-1~5 + constraints 정합."""
        c = self.contract
        self.assertIn("version: 1.0.0", c)
        self.assertIn("status: frozen", c)
        self.assertIn("scenario_id: C11", c)
        for ac in ("AC-MOB-1", "AC-MOB-2", "AC-MOB-3", "AC-MOB-4", "AC-MOB-5"):
            self.assertIn(ac, c, f"missing AC: {ac}")
        self.assertIn("external_integrations: excluded", c)
        self.assertIn("new_sql_count: 0", c)
        self.assertIn("DEC-044", c)

    def test_S_02_device_matrix_5_with_viewport(self) -> None:
        """TC-C11-S-02 — 디바이스 매트릭스 5종 + viewport 명시."""
        c = self.contract
        for d in DEVICES:
            self.assertIn(f"id: {d}", c, f"missing device id: {d}")
        viewport_count = len(re.findall(r"viewport:\s*\{", c))
        self.assertEqual(
            viewport_count, 5,
            f"expected 5 viewport entries (one per device), got {viewport_count}",
        )

    def test_S_03_scenario_matrix_4_with_pages(self) -> None:
        """TC-C11-S-03 — 시나리오 4종 매트릭스 + 각 page_path 파일 존재."""
        c = self.contract
        for sid in SCENARIO_PAGES.keys():
            self.assertIn(f"id: {sid}", c, f"missing scenario id in contract: {sid}")
        for sid, p in SCENARIO_PAGES.items():
            self.assertTrue(
                p.exists(),
                f"scenario {sid} page file missing: {p.relative_to(ROOT)}",
            )

    def test_S_04_breakpoint_isolation_policy(self) -> None:
        """TC-C11-S-04 — BPI-1~4 등록 + enforcement.static_check 명령 명시."""
        c = self.contract
        self.assertIn("breakpoint_isolation_policy:", c)
        for bpi in ("BPI-1", "BPI-2", "BPI-3", "BPI-4"):
            self.assertIn(bpi, c, f"missing breakpoint isolation rule: {bpi}")
        self.assertIn("enforcement:", c)
        self.assertIn("static_check:", c)
        self.assertIn("snapshot_test:", c)

    def test_S_05_scanner_conflict_cases(self) -> None:
        """TC-C11-S-05 — 스캐너-가상키보드 충돌 케이스 SC-1~3 등록."""
        c = self.contract
        self.assertIn("scanner_conflict_cases:", c)
        for sc in ("SC-1", "SC-2", "SC-3"):
            self.assertIn(sc, c, f"missing scanner conflict case: {sc}")

    def test_S_06_decisions_and_open_questions(self) -> None:
        """TC-C11-S-06 — DEC-MOB-1/2 + OQ-MOB-1 등록."""
        c = self.contract
        self.assertIn("DEC-MOB-1", c)
        self.assertIn("DEC-MOB-2", c)
        self.assertIn("OQ-MOB-1", c)
        # DEC-044 (외부 시스템 연동 제외) 도 카탈로그에 있어야 함
        self.assertIn("DEC-044", _read(DECISIONS_DOC))

    def test_S_07_scan_input_min_touch_target(self) -> None:
        """TC-C11-S-07 — ScanInput 의 input min-h-[44px] (Apple HIG ≥ 44pt) 반영."""
        s = self.scan_input
        self.assertIn("min-h-[44px]", s, "ScanInput must declare 44pt min touch target")
        self.assertIn('data-mobile-touch-target="44"', s)

    def test_S_08_scan_input_mobile_attrs(self) -> None:
        """TC-C11-S-08 — ScanInput 의 모바일 친화 input 속성 (auto* / inputMode)."""
        s = self.scan_input
        self.assertIn('autoCapitalize="off"', s)
        self.assertIn('autoCorrect="off"', s)
        self.assertIn('inputMode="text"', s)
        self.assertIn('autoComplete="off"', s)

    def test_S_09_scan_input_bpi3_desktop_lock(self) -> None:
        """TC-C11-S-09 — ScanInput 가 sm: prefix 로 desktop 잠금 (BPI-3 정합)."""
        s = self.scan_input
        # mobile-first 기본값 + sm:* 로 desktop 복원
        for token in ("sm:py-1.5", "sm:text-sm", "sm:min-h-0"):
            self.assertIn(token, s, f"ScanInput must use sm: prefix to lock desktop ({token})")

    def test_S_10_scanner_lib_dec004_thresholds_unchanged(self) -> None:
        """TC-C11-S-10 — scanner.ts 의 wedge interval/idle reset 임계 (DEC-004) 변경 0건."""
        s = self.scanner_lib
        self.assertIn("wedgeIntervalMs = 30", s, "DEC-004 wedge threshold must remain 30ms")
        self.assertIn("resetIdleMs = 50", s, "DEC-004 idle reset must remain 50ms")
        self.assertIn("minLength = 4", s)


# ──────────────────────────────────────────────
# M — 회귀 매트릭스 (20 cell — 5 디바이스 × 4 시나리오)
# ──────────────────────────────────────────────
class MatrixTests(TestCase):
    """5 device × 4 scenario = 20 셀 — 각 셀이 contract + page 정합 충족."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = _read(CONTRACT)


def _make_matrix_test(device: str, sid: str, page: Path):
    def t(self) -> None:
        c = self.contract
        self.assertIn(f"id: {device}", c, f"device missing in contract: {device}")
        self.assertIn(f"id: {sid}", c, f"scenario missing in contract: {sid}")
        self.assertTrue(page.exists(), f"page missing for {device} × {sid}: {page}")
    t.__doc__ = f"TC-C11-M — {device} × {sid} 매트릭스 셀 정합."
    return t


_idx = 1
for _device in DEVICES:
    for _sid, _page in SCENARIO_PAGES.items():
        setattr(
            MatrixTests,
            f"test_M_{_idx:02d}_{_device}__{_sid}",
            _make_matrix_test(_device, _sid, _page),
        )
        _idx += 1


# ──────────────────────────────────────────────
# D — 의존성 게이트 (extension_dependencies.md)
# ──────────────────────────────────────────────
class DependencyGateTests(TestCase):
    """확장 라인 의존성 그래프 정합 — C11 행 등록 + 진입 게이트 명시."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.deps_doc = _read(DEPS_DOC)

    def test_D_01_c11_preceding_assets_table(self) -> None:
        """TC-C11-D-01 — extension_dependencies.md §2 에 C11 → C2/C8/C10 선행 자산 등록."""
        d = self.deps_doc
        # §2 표는 마크다운 row 형태로 등록 — 각 표 셀에 C11 라벨 + 자산 키워드 grep
        # 최소 3 행 (C2/C8/C10) 등록 필요
        c11_rows = [line for line in d.splitlines() if "**C11**" in line]
        self.assertGreaterEqual(
            len(c11_rows), 3,
            f"extension_dependencies.md §2 must list ≥3 C11 rows (got {len(c11_rows)})",
        )
        joined = "\n".join(c11_rows)
        for asset in ("C2", "scanner", "PermissionGuard"):
            self.assertIn(asset, joined, f"C11 preceding asset row missing keyword: {asset}")

    def test_D_02_c11_entry_gate(self) -> None:
        """TC-C11-D-02 — extension_dependencies.md §4 진입 게이트 의 C11 행 명시."""
        d = self.deps_doc
        # 문서 내에 등록된 모든 C11 표 row 중, desktop + scanner 키워드를 포함한 진입 게이트 row 가 1건 이상 존재해야 함.
        rows = re.findall(r"\|\s*C11\s*\|[^\n]*", d)
        self.assertTrue(rows, "extension_dependencies.md must contain at least one C11 row")
        gate_rows = [r for r in rows if "desktop" in r and "scanner" in r]
        self.assertGreaterEqual(
            len(gate_rows), 1,
            f"C11 entry gate row (desktop + scanner) missing. C11 rows: {rows}",
        )


# ──────────────────────────────────────────────
# DESK — 데스크톱 회귀 가드 (BPI-1~4 정합 + 핵심 셀렉터/임계값 baseline)
# ──────────────────────────────────────────────
class DesktopRegressionGuardTests(TestCase):
    """C11 반응형 변경이 desktop 4 시나리오에 회귀를 유발하지 않는지 정합 검증.

    가드 원칙 (계획서 v0.2 §1 보강):
    - 모바일 신규 클래스는 default(미디어 쿼리 외) 셀렉터 변경 금지 (BPI-2).
    - sm: prefix 로만 desktop 잠금 (BPI-3) — md:/lg: 분기 추가 시 회귀 위험.
    - useScanner 인터페이스/임계값 변경 0건 — C8 Phase 1 22 회귀 그대로.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.scan_input = _read(SCAN_INPUT)
        cls.scanner_lib = _read(SCANNER_LIB)
        cls.pages = {sid: _read(p) for sid, p in SCENARIO_PAGES.items()}

    def test_DESK_01_scan_input_default_class_present(self) -> None:
        """TC-C11-DESK-01 — ScanInput 의 default(mobile-first) 클래스가 모두 등록되어 있고 desktop sm: 로 모두 잠김."""
        s = self.scan_input
        # default mobile 클래스
        for token in ("min-h-[44px]", "py-2", "text-base"):
            self.assertIn(token, s, f"missing mobile-first default class: {token}")
        # sm: prefix 로 desktop 복원 (1:1)
        for desktop_lock in ("sm:min-h-0", "sm:py-1.5", "sm:text-sm"):
            self.assertIn(desktop_lock, s, f"missing desktop lock: {desktop_lock}")

    def test_DESK_02_scan_input_no_md_or_lg_branching(self) -> None:
        """TC-C11-DESK-02 — ScanInput 가 sm: 외 추가 breakpoint 분기를 도입하지 않음 (단일 진입점)."""
        s = self.scan_input
        md_lg = re.findall(r"\b(?:md|lg|xl|2xl):[A-Za-z0-9_\-\[\]:/.\.]+", s)
        self.assertEqual(
            md_lg, [],
            f"ScanInput must not introduce md:/lg:/xl: breakpoint branches (BPI-3 violation): {md_lg}",
        )

    def test_DESK_03_scanner_lib_interface_unchanged(self) -> None:
        """TC-C11-DESK-03 — useScanner public 시그니처 변경 0건 (C8 22 회귀 정합)."""
        s = self.scanner_lib
        # 핵심 옵션 키 존재 확인 (interface UseScannerOptions)
        for key in (
            "onScan:",
            "captureGlobal?:",
            "targetRef?:",
            "wedgeIntervalMs?:",
            "resetIdleMs?:",
            "enabled?:",
            "minLength?:",
        ):
            self.assertIn(key, s, f"useScanner option missing/changed: {key}")
        self.assertIn("export function useScanner", s)

    # baseline: C11 진입 시점(2026-04-20) 의 4 핵심 페이지 fixed/sticky 사용 카운트.
    # 기존 패턴(예: 데이터그리드 헤더 sticky)은 desktop 의도된 동작이므로 baseline 으로 인정한다.
    # 신규 추가 시 ① baseline 갱신 + 카탈로그 PR 체크리스트 통과를 강제 (회귀 차단 게이트).
    BASELINE_FIXED_STICKY_COUNT = {
        "C2_outbound_orders": {"fixed": 0, "sticky": 0},
        "C3_inbound_receipts": {"fixed": 0, "sticky": 0},
        "C4_returns_receipts": {"fixed": 0, "sticky": 1},  # 데이터그리드 헤더 sticky top-0 (desktop 정합)
        "C8_scan_match": {"fixed": 0, "sticky": 0},
    }

    def test_DESK_04_no_new_fixed_or_sticky_introduced(self) -> None:
        """TC-C11-DESK-04 — 4 핵심 페이지의 fixed/sticky 카운트가 baseline 을 초과하지 않음.

        보강 원칙: 신규 fixed/sticky 도입은 desktop 회귀 위험 → baseline 갱신 PR + 카탈로그 갱신 강제.
        baseline 카운트는 C11 진입 시점 (확장 라인 v0.2 frozen) 기준.
        """
        for sid, src in self.pages.items():
            cls_attrs = re.findall(r'className="([^"]*)"', src)
            for keyword in ("fixed", "sticky"):
                actual = sum(1 for c in cls_attrs if re.search(rf"\b{keyword}\b", c))
                baseline = self.BASELINE_FIXED_STICKY_COUNT[sid][keyword]
                self.assertLessEqual(
                    actual, baseline,
                    f"{sid}: '{keyword}' className count {actual} exceeds baseline {baseline}. "
                    f"신규 도입은 BASELINE_FIXED_STICKY_COUNT 갱신 + sm:* 잠금 + 카탈로그 PR 필요.",
                )

    def test_DESK_05_no_global_css_default_selector_drift(self) -> None:
        """TC-C11-DESK-05 — globals.css 의 default selector 가 mobile UAT 작업 중 변경되지 않음.

        baseline: globals.css 는 `:root` / `.dark` / `@layer base` / `@theme inline` / `@import` 만 가짐.
        신규 default selector (e.g. body, .scan-input) 가 추가되면 desktop 회귀 위험 → 차단.
        """
        css_path = FRONTEND_SRC / "app" / "globals.css"
        css = _read(css_path)
        # 기존 허용 셀렉터 외 default(@media 외) 셀렉터가 추가되었는지 검사
        # 매우 단순한 휴리스틱: top-level rule 목록을 추출 후 화이트리스트와 비교
        # 화이트리스트 (baseline)
        allowed = {":root", ".dark"}
        # 허용 at-rule prefix
        # (@media/@layer/@theme/@import/@custom-variant 는 무관)
        # 현재 default selector 는 :root, .dark 두 개만 — 변경 시 fail
        m = re.findall(r"^([.\w][^\{\n@/]*?)\s*\{", css, re.MULTILINE)
        unique = sorted({sel.strip() for sel in m if sel.strip()})
        unexpected = [s for s in unique if s not in allowed]
        self.assertEqual(
            unexpected, [],
            f"globals.css introduced default selector(s) outside baseline (BPI-2 violation): {unexpected}",
        )


if __name__ == "__main__":
    main(verbosity=2)
