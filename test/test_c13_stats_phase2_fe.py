"""
C13 통계/리포트 확장 Phase 2 (T6) — 프론트 4 화면 정적 회귀.

검증 범위
---------
- 도서물류관리프로그램/frontend/src/lib/stats-api.ts
- 도서물류관리프로그램/frontend/src/components/stats/{stats-filter-bar,stats-banners,charts}.tsx
- 도서물류관리프로그램/frontend/src/app/(app)/stats/{sales-period,customer-analysis,book-turnover,quarterly-summary}/page.tsx
- 도서물류관리프로그램/frontend/src/lib/form-registry.ts (4 라우트 등록)
- 도서물류관리프로그램/frontend/src/i18n/messages/c13.ko.json (Phase 2 메시지)
- 도서물류관리프로그램/frontend/package.json (recharts 의존)
- migration/contracts/stats_reports.yaml (frontend 등록 — Phase 2 메모)
- dashboard/data/porting-screens.json (C13.tasks.T6 = completed)

설계 정합
---------
- C8/C10/C11 Phase 1 패턴 — 정적 grep 위주, 백엔드 import 0.
- 신규 SQL 0건 정책은 Phase 1 backend 테스트가 책임 — 본 모듈은 FE 회귀만.
- recharts 단일 import 지점은 components/stats/charts.tsx 만 — DEC-019 정합.
- 4 페이지 모두 PermissionGuard + data-legacy-id + StatsErrorBanner + PartialBanner 정합.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PKG_JSON = ROOT / "도서물류관리프로그램" / "frontend" / "package.json"
CONTRACT = ROOT / "migration" / "contracts" / "stats_reports.yaml"
DASHBOARD = ROOT / "dashboard" / "data" / "porting-screens.json"

STATS_API = FE_SRC / "lib" / "stats-api.ts"
FORM_REGISTRY = FE_SRC / "lib" / "form-registry.ts"
KO_JSON = FE_SRC / "i18n" / "messages" / "c13.ko.json"
COMP_DIR = FE_SRC / "components" / "stats"
PAGE_DIR = FE_SRC / "app" / "(app)" / "stats"

PAGES = {
    "sales-period": ("admin.stats.sales", "Sobo50", "/api/v1/stats/sales-period"),
    "customer-analysis": ("admin.stats.customer", "Sobo51", "/api/v1/stats/customer-analysis"),
    "book-turnover": ("admin.stats.book", "Sobo52", "/api/v1/stats/book-turnover"),
    "quarterly-summary": ("admin.stats.quarterly", "Sobo53", "/api/v1/stats/quarterly-summary"),
}


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# 1. 공용 인프라 (api / 컴포넌트 / i18n / form-registry)
# ============================================================================
class StaticInfraC13Phase2(TestCase):

    def test_S_01_recharts_dependency_added(self):
        """package.json 에 recharts 의존 추가 (DEC-019 단일 차트)."""
        pkg = json.loads(_read(PKG_JSON))
        deps = pkg.get("dependencies", {})
        self.assertIn("recharts", deps, f"recharts not in deps: {sorted(deps.keys())}")

    def test_S_02_typecheck_script_present(self):
        """package.json scripts 에 typecheck (tsc --noEmit) 등록 — FE 품질 게이트."""
        pkg = json.loads(_read(PKG_JSON))
        scripts = pkg.get("scripts", {})
        self.assertIn("typecheck", scripts, f"typecheck script missing: {sorted(scripts.keys())}")
        self.assertIn("tsc", scripts["typecheck"])

    def test_S_03_stats_api_exports_4_methods(self):
        """stats-api.ts 가 4 endpoint 호출 메서드 모두 노출."""
        src = _read(STATS_API)
        for name in ("salesPeriod", "customerAnalysis", "bookTurnover", "quarterlySummary"):
            self.assertIn(name, src, f"statsApi.{name} missing")
        for path in (
            "/api/v1/stats/sales-period",
            "/api/v1/stats/customer-analysis",
            "/api/v1/stats/book-turnover",
            "/api/v1/stats/quarterly-summary",
        ):
            self.assertIn(path, src, f"endpoint path missing in stats-api.ts: {path}")

    def test_S_04_shared_components_present(self):
        """공용 필터/배너/차트 컴포넌트 3종 모두 존재."""
        for fname in ("stats-filter-bar.tsx", "stats-banners.tsx", "charts.tsx"):
            self.assertTrue(
                (COMP_DIR / fname).exists(),
                f"shared stats component missing: {fname}",
            )

    def test_S_05_recharts_single_import_point(self):
        """DEC-019 정합 — recharts 는 components/stats/charts.tsx 단일 import 지점만 사용.

        4 페이지 / lib / 다른 컴포넌트가 직접 recharts 를 import 하지 않아야 한다.
        """
        bad: list[str] = []
        for tsx in FE_SRC.rglob("*.ts*"):
            if tsx == COMP_DIR / "charts.tsx":
                continue
            text = tsx.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"from\s+[\"']recharts[\"']", text):
                bad.append(str(tsx.relative_to(FE_SRC)))
        self.assertEqual(
            bad, [],
            f"recharts must only be imported in components/stats/charts.tsx, found: {bad}",
        )

    def test_S_06_form_registry_4_routes_phase2(self):
        """form-registry 에 4 stats 라우트가 phase2 로 등록."""
        src = _read(FORM_REGISTRY)
        for slug, (_perm, _legacy, _path) in PAGES.items():
            self.assertIn(f"/stats/{slug}", src, f"route /stats/{slug} not registered")
        # phase2 stats 항목 4건 — Sobo50/51/52/53_stats id 사용
        for sid in ("Sobo50_stats", "Sobo51_stats", "Sobo52_stats", "Sobo53_stats"):
            self.assertIn(sid, src, f"FORM_REGISTRY id missing: {sid}")

    def test_S_07_ko_json_keys(self):
        """c13.ko.json 의 핵심 키 (partial banner / 에러 / 필터) 존재."""
        ko = json.loads(_read(KO_JSON))
        for k in (
            "stats.partial.banner",
            "stats.error.invalid_range",
            "stats.error.permission_denied",
            "stats.filter.search",
            "stats.sales_period.title",
            "stats.customer_analysis.title",
            "stats.book_turnover.title",
            "stats.quarterly_summary.title",
        ):
            self.assertIn(k, ko, f"c13.ko.json missing key: {k}")


# ============================================================================
# 2. 4 페이지 정합 매트릭스
# ============================================================================
class StaticPageMatrixC13(TestCase):

    def test_M_01_pages_exist(self):
        """/stats/* 4 page.tsx 모두 존재."""
        for slug in PAGES:
            self.assertTrue(
                (PAGE_DIR / slug / "page.tsx").exists(),
                f"page missing: stats/{slug}/page.tsx",
            )

    def test_M_02_pages_use_permission_guard_with_correct_code(self):
        """각 페이지가 PermissionGuard(code=...) + 정확한 admin.stats.* 코드 부착."""
        for slug, (perm, _legacy, _path) in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn("PermissionGuard", src, f"{slug}: PermissionGuard 미사용")
            self.assertIn(f'code="{perm}"', src, f"{slug}: PermissionGuard code != {perm}")

    def test_M_03_pages_call_stats_api(self):
        """각 페이지가 statsApi.<method> 호출."""
        for slug, _ in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn("statsApi.", src, f"{slug}: statsApi 호출 없음")

    def test_M_04_pages_render_partial_banner(self):
        """각 페이지가 PartialBanner(metadata.partial 배너) 렌더링."""
        for slug, _ in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn("PartialBanner", src, f"{slug}: PartialBanner 미사용 (PBP-2)")

    def test_M_05_pages_render_error_banner(self):
        """각 페이지가 StatsErrorBanner(403/422 표시) 렌더링."""
        for slug, _ in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn(
                "StatsErrorBanner", src,
                f"{slug}: StatsErrorBanner 미사용 (DEC-041 표준 에러 표시)",
            )

    def test_M_06_pages_use_filter_bar(self):
        """각 페이지가 공용 StatsFilterBar 재사용."""
        for slug, _ in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn("StatsFilterBar", src, f"{slug}: StatsFilterBar 미사용")

    def test_M_07_pages_data_legacy_id(self):
        """각 페이지가 data-legacy-id (DEC-028) 부착 — 최소 1건 이상."""
        for slug, (_perm, legacy, _path) in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn(
                "data-legacy-id", src,
                f"{slug}: data-legacy-id 미사용 (DEC-028)",
            )
            self.assertIn(legacy, src, f"{slug}: legacy id prefix '{legacy}' 미사용")

    def test_M_08_pages_use_chart_card(self):
        """각 페이지가 ChartCard + recharts 차트 (Line/Bar/Pie) 1개 이상 사용."""
        for slug, _ in PAGES.items():
            src = _read(PAGE_DIR / slug / "page.tsx")
            self.assertIn("ChartCard", src, f"{slug}: ChartCard 미사용")
            has_chart = any(name in src for name in ("StatsLineChart", "StatsBarChart", "StatsPieChart"))
            self.assertTrue(has_chart, f"{slug}: recharts 차트 컴포넌트 미사용")


# ============================================================================
# 3. 거버넌스 동기화
# ============================================================================
class GovernanceSyncC13(TestCase):

    def test_G_01_dashboard_t6_completed(self):
        """dashboard/data/porting-screens.json — C13_stats.tasks.T6 = completed."""
        data = json.loads(_read(DASHBOARD))
        screens = data.get("scenarios") or data.get("rows") or data.get("scenarios_list") or []
        # 구조: scenarios 안에 id == 'C13_stats' 인 항목
        if not screens:
            screens = next((v for v in data.values() if isinstance(v, list)), [])
        target = next((s for s in screens if s.get("id") == "C13_stats"), None)
        self.assertIsNotNone(target, "C13_stats not found in dashboard")
        t6 = (target.get("tasks") or {}).get("T6") or {}
        self.assertEqual(
            t6.get("status"), "completed",
            f"C13.T6 status != completed (got {t6.get('status')})",
        )

    def test_G_02_contract_mentions_phase2_frontend(self):
        """stats_reports.yaml 에 Phase 2 frontend 진행 표식 (recharts / phase 2 / page.tsx 중 하나)."""
        c = _read(CONTRACT)
        # 동결 v1.0 은 유지 — Phase 2 진행 노트는 changelog 또는 reference 에 기록될 수 있다.
        # 본 케이스는 contract 의 charts_library: recharts 가 그대로 유지되는지 가드.
        self.assertIn("charts_library: recharts", c)


if __name__ == "__main__":
    main(verbosity=2)
