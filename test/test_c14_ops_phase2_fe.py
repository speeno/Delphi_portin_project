"""
C14 운영 모니터링 Phase 2 (T6) — 프론트 정적 회귀.

검증 범위
---------
- 도서물류관리프로그램/frontend/src/lib/ops-api.ts
- 도서물류관리프로그램/frontend/src/components/ops/global-alert-banner.tsx
- 도서물류관리프로그램/frontend/src/app/(app)/admin/{ops,audit}/page.tsx
- 도서물류관리프로그램/frontend/src/app/(app)/layout.tsx (GlobalAlertBanner 마운트)
- 도서물류관리프로그램/frontend/src/lib/form-registry.ts (WebAdmOps/WebAdmAudit 등록)
- 도서물류관리프로그램/frontend/src/i18n/messages/c14.ko.json
- 도서물류관리프로그램/frontend/next.config.ts (/metrics rewrite)
- migration/contracts/ops_monitoring.yaml (phase2_frontend 섹션 — 게이트 #6 SLA)
- dashboard/data/porting-screens.json (C14.tasks.T6 = completed)

설계 정합
---------
- C13 Phase 2 FE 회귀 패턴 — 정적 grep 위주, 백엔드 import 0.
- 외부 SaaS 호출 ❌ — DEC-044. opsApi 는 동일 출처 fetch 만.
- ETag (If-Match) 적용 — DEC-042. dismissAlert 가 If-Match 헤더 필수.
- 글로벌 폴링은 60s 저빈도 + document.hidden 시 일시정지.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE_SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
NEXT_CONFIG = ROOT / "도서물류관리프로그램" / "frontend" / "next.config.ts"
CONTRACT = ROOT / "migration" / "contracts" / "ops_monitoring.yaml"
DASHBOARD = ROOT / "dashboard" / "data" / "porting-screens.json"

OPS_API = FE_SRC / "lib" / "ops-api.ts"
FORM_REGISTRY = FE_SRC / "lib" / "form-registry.ts"
KO_JSON = FE_SRC / "i18n" / "messages" / "c14.ko.json"
GLOBAL_BANNER = FE_SRC / "components" / "ops" / "global-alert-banner.tsx"
LAYOUT = FE_SRC / "app" / "(app)" / "layout.tsx"
OPS_PAGE = FE_SRC / "app" / "(app)" / "admin" / "ops" / "page.tsx"
AUDIT_PAGE = FE_SRC / "app" / "(app)" / "admin" / "audit" / "page.tsx"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# S — 정적 인프라 회귀
# ============================================================================
class StaticInfraC14Phase2(TestCase):

    def test_S_01_ops_api_exports_required_methods(self):
        src = _read(OPS_API)
        for token in (
            "export const opsApi",
            "healthFull",
            "metricsText",
            "listAudit",
            "listAlerts",
            "pushAlert",
            "dismissAlert",
        ):
            self.assertIn(token, src, f"ops-api.ts missing: {token}")
        # 백엔드 엔드포인트 경로 정합
        for path in (
            "/api/v1/health/full",
            "/metrics",
            "/api/v1/admin/audit",
            "/api/v1/admin/alerts",
        ):
            self.assertIn(path, src, f"ops-api.ts missing path: {path}")

    def test_S_02_dismiss_alert_uses_if_match(self):
        """DEC-042 — dismissAlert 는 반드시 If-Match 헤더 부착."""
        src = _read(OPS_API)
        self.assertRegex(
            src,
            r'"If-Match"\s*:\s*ifMatch',
            "dismissAlert must send If-Match header (DEC-042 concurrency)",
        )

    def test_S_03_no_external_saas_in_ops_api(self):
        """DEC-044 — 외부 SaaS 호출 ❌ (datadog/newrelic/slack/pagerduty 등)."""
        src = _read(OPS_API).lower()
        for forbidden in ("datadog", "newrelic", "sentry", "slack", "pagerduty", "teams.microsoft"):
            self.assertNotIn(
                forbidden, src,
                f"ops-api.ts must not call external SaaS '{forbidden}' (DEC-044)",
            )

    def test_S_04_global_alert_banner_polling_policy(self):
        """폴링 60s + document.hidden 일시정지 + admin.audit.read 권한 가드."""
        src = _read(GLOBAL_BANNER)
        self.assertIn("POLL_INTERVAL_MS = 60_000", src)
        self.assertIn("document.hidden", src)
        self.assertIn('"admin.audit.read"', src)
        self.assertIn("hasPermission", src)
        # info 는 글로벌 미노출
        self.assertIn('a.severity !== "info"', src)
        # ETag 정합 — dismiss 시 If-Match (etag) 사용
        self.assertRegex(
            src,
            r"opsApi\.dismissAlert\(\s*alertId\s*,\s*etag\s*\)",
            "GlobalAlertBanner must call opsApi.dismissAlert(alertId, etag) (DEC-042)",
        )

    def test_S_05_layout_mounts_global_alert_banner(self):
        src = _read(LAYOUT)
        self.assertIn("GlobalAlertBanner", src)
        self.assertIn(
            'from "@/components/ops/global-alert-banner"',
            src,
            "layout must import GlobalAlertBanner from canonical path",
        )

    def test_S_06_form_registry_routes_phase2(self):
        src = _read(FORM_REGISTRY)
        for route in ("/admin/ops", "/admin/audit"):
            self.assertIn(route, src, f"form-registry must register {route}")
        # 두 항목이 모두 phase2 마킹
        ops_block = re.search(
            r'\{\s*id:\s*"WebAdmOps".*?\}', src, re.DOTALL,
        )
        audit_block = re.search(
            r'\{\s*id:\s*"WebAdmAudit".*?\}', src, re.DOTALL,
        )
        self.assertIsNotNone(ops_block, "WebAdmOps registry entry missing")
        self.assertIsNotNone(audit_block, "WebAdmAudit registry entry missing")
        self.assertIn('phase: "phase2"', ops_block.group(0))
        self.assertIn('phase: "phase2"', audit_block.group(0))

    def test_S_07_ko_json_keys(self):
        with KO_JSON.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for key in (
            "ops.title",
            "ops.health.title",
            "ops.metrics.title",
            "ops.alerts.title",
            "ops.alerts.stale",          # DEC-042 메시지
            "ops.alerts.precondition",   # 428 메시지
            "ops.error.forbidden",
            "audit.title",
            "audit.column.ts",
            "audit.column.channel",
            "audit.column.msg",
            "audit.error.forbidden",
        ):
            self.assertIn(key, data, f"c14.ko.json missing: {key}")

    def test_S_08_metrics_proxy_rewrite_present(self):
        """Prometheus exposition 은 root mount — next.config 가 동일 출처 프록시 제공."""
        src = _read(NEXT_CONFIG)
        self.assertIn('source: "/metrics"', src)
        self.assertIn('destination: `${apiProxyTarget}/metrics`', src)


# ============================================================================
# M — 페이지 매트릭스 회귀
# ============================================================================
class StaticPageMatrixC14(TestCase):

    def test_M_01_ops_page_structure(self):
        src = _read(OPS_PAGE)
        self.assertIn('PermissionGuard', src)
        self.assertIn('"admin.health.read"', src)
        self.assertIn('opsApi.healthFull', src)
        self.assertIn('opsApi.metricsText', src)
        self.assertIn('opsApi.listAlerts', src)
        self.assertIn('opsApi.dismissAlert', src)
        # 표준 에러 매핑은 StatsErrorBanner 재사용 (DEC-041 정합)
        self.assertIn('StatsErrorBanner', src)
        # data-legacy-id (Sobo 매핑은 없으나 WebAdmOps prefix 정합)
        self.assertIn('data-legacy-id={`${LEGACY_ID}.Page`}', src)
        self.assertIn('LEGACY_ID = "WebAdmOps"', src)
        # 409 (STALE_VERSION) / 428 (PRECONDITION_REQUIRED) 분기
        self.assertIn('e.status === 409', src)
        self.assertIn('e.status === 428', src)

    def test_M_02_audit_page_structure(self):
        src = _read(AUDIT_PAGE)
        self.assertIn('PermissionGuard', src)
        self.assertIn('"admin.audit.read"', src)
        self.assertIn('opsApi.listAudit', src)
        self.assertIn('StatsErrorBanner', src)
        self.assertIn('LEGACY_ID = "WebAdmAudit"', src)
        # 채널 필터 + limit
        self.assertIn('CHANNELS', src)
        self.assertIn('audit.auth', src)
        self.assertIn('audit.outbound', src)

    def test_M_03_pages_use_data_legacy_id(self):
        for path, prefix in ((OPS_PAGE, "WebAdmOps"), (AUDIT_PAGE, "WebAdmAudit")):
            src = _read(path)
            self.assertGreaterEqual(
                src.count("data-legacy-id"), 3,
                f"{path.name} must have multiple data-legacy-id markers",
            )
            self.assertIn(prefix, src)


# ============================================================================
# G — 거버넌스/계약 동기화
# ============================================================================
class GovernanceSyncC14(TestCase):

    def test_G_01_dashboard_t6_completed(self):
        with DASHBOARD.open(encoding="utf-8") as fh:
            data = json.load(fh)
        screens = data.get("screens") or data.get("scenarios") or []
        if isinstance(screens, dict):
            screens = list(screens.values())
        c14 = next(
            (s for s in screens if "C14" in (s.get("id", "") + s.get("title", ""))),
            None,
        )
        self.assertIsNotNone(c14, "C14 entry missing in porting-screens.json")
        t6 = ((c14.get("tasks") or {}).get("T6") or {})
        self.assertEqual(
            t6.get("status"), "completed",
            f"C14.tasks.T6 must be completed (got {t6})",
        )

    def test_G_02_contract_phase2_frontend_section(self):
        c = _read(CONTRACT)
        for token in (
            "phase2_frontend:",
            "polling_interval_ms: 60000",
            "polling_pause_when_hidden: true",
            "/admin/ops",
            "/admin/audit",
            "global_alert_banner:",
            "sla_alignment:",
            "external_calls: 0",   # DEC-044
            "ETag/If-Match",       # DEC-042
        ):
            self.assertIn(token, c, f"ops_monitoring.yaml missing phase2 token: {token}")


if __name__ == "__main__":
    main(verbosity=2)
