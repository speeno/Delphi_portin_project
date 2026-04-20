"""
C14 운영 모니터링 Phase 1 — health/full + metrics + audit + alerts 회귀 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/ops_monitoring.yaml v1.0.0 (AC-OPS-1~5 + DM-1~3 + 라벨 카디널리티)
- legacy-analysis/permission-keys-catalog.md §4 (F90/F91/F92 — admin.{audit,metrics,health}.read)
- legacy-analysis/decisions.md (DEC-044)
- 도서물류관리프로그램/backend/app/services/ops_service.py (in-memory ring + Prometheus)
- 도서물류관리프로그램/backend/app/routers/ops.py (PermissionGuard 3종 + ETag)

검증 케이스
-----------
정적 가드 (S — T5 무관)
- TC-C14-S-01  ops_monitoring.yaml v1.0 frozen + AC-OPS-1~5 + degraded_mapping (DM-1~3)
- TC-C14-S-02  contract 의 라벨 카디널리티 정책 (allowed/forbidden) 명시
- TC-C14-S-03  permission-keys-catalog.md §4 + admin.{audit,metrics,health}.read 등록
- TC-C14-S-04  ops_service / ops router 신규 SQL 0건 (DEC-040 정합)
- TC-C14-S-05  ops router 가 admin.{audit,metrics,health}.read 3 권한 require_permission
- TC-C14-S-06  ops_service 가 prometheus_client 의 Counter/Gauge/Histogram 사용
- TC-C14-S-07  main.py 에 ops.router include_router 등록

런타임 가드 (R — T5 의존)
- TC-C14-R-01  /health/full → DM-1~3 정합 (deps 분리 + status enum)
- TC-C14-R-02  /metrics → Prometheus exposition (text 0.0.4) + http_requests_total 메트릭 노출
- TC-C14-R-03  /admin/alerts → ETag 헤더 + DEC-042 (If-Match 누락 → 428, 불일치 → 409)
- TC-C14-R-04  /admin/audit → admin.audit.read 가드 PASS + ring buffer 적재 정합
- TC-C14-R-05  /admin/audit → operator role 의 d_select 분기 (본인 hcode 만)
- TC-C14-R-06  운영 알림 라벨 카디널리티 — Counter labels 가 forbidden 키 미사용

설계 정합 (사용자 룰)
---------------------
- C13 Phase 1 패턴 — monkeypatch + dependency_overrides + skipUnless.
- 신규 SQL 0건 — ops_service 는 in-memory ring buffer 만.
- 외부 시스템 연동 ❌ — Prometheus exposition 만 (alerting 채널은 in-app 전용).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
CONTRACT = ROOT / "migration" / "contracts" / "ops_monitoring.yaml"
PERM_CATALOG = ROOT / "legacy-analysis" / "permission-keys-catalog.md"
DECISIONS = ROOT / "legacy-analysis" / "decisions.md"
OPS_SERVICE = BACKEND / "app" / "services" / "ops_service.py"
OPS_ROUTER = BACKEND / "app" / "routers" / "ops.py"
MAIN_PY = BACKEND / "app" / "main.py"

sys.path.insert(0, str(BACKEND))

# ──────────────────────────────────────────────
# T5 런타임 의존성 — 미준비 시 R 케이스 skip
# ──────────────────────────────────────────────
_RUNTIME_OK = False
try:
    from fastapi.testclient import TestClient  # noqa: E402
    from app.main import app  # noqa: E402
    from app.routers.auth import get_current_user  # noqa: E402

    def _override_admin() -> dict:
        return {
            "user_id": "0000",
            "server_id": "remote_138",
            "role": "admin",
            "hcode": "0000",
            "branch_id": "0000",
            "permissions": ["*"],
        }

    def _override_operator(hcode: str = "1234") -> dict:
        return {
            "user_id": "9999",
            "server_id": "remote_138",
            "role": "operator",
            "hcode": hcode,
            "branch_id": hcode,
            "permissions": [],
        }

    app.dependency_overrides[get_current_user] = _override_admin
    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# S — 정적 회귀
# ============================================================================
class StaticGuardC14(TestCase):

    def test_S_01_contract_v1_frozen(self):
        """TC-C14-S-01 — ops_monitoring.yaml v1.0 frozen + AC-OPS-1~5 + DM-1~3."""
        c = _read(CONTRACT)
        for token in (
            "version: 1.0.0",
            "status: frozen",
            "scenario_id: C14",
            "AC-OPS-1", "AC-OPS-2", "AC-OPS-3", "AC-OPS-4", "AC-OPS-5",
            "DM-1", "DM-2", "DM-3",
            "external_integrations: excluded",
            "external_apm:",
            "external_alerting:",
            "external_log_aggr:",
            "DEC-044",
            "/api/v1/health/full",
            "/metrics",
            "/api/v1/admin/audit",
            "/api/v1/admin/alerts",
            "admin.health.read",
            "admin.metrics.read",
            "admin.audit.read",
        ):
            self.assertIn(token, c, f"contract missing token: {token}")

    def test_S_02_label_cardinality_policy(self):
        """TC-C14-S-02 — 라벨 카디널리티 정책 (allowed/forbidden) 명시."""
        c = _read(CONTRACT)
        for token in (
            "label_cardinality_policy:",
            "max_unique_label_values_per_metric",
            "forbidden_label_keys:",
            "allowed_label_keys:",
            "user_id",        # forbidden 예시
            "request_id",
            "method",         # allowed 예시
            "endpoint_pattern",
            "status_class",
        ):
            self.assertIn(token, c, f"contract missing label policy token: {token}")

    def test_S_03_permission_catalog_registered(self):
        """TC-C14-S-03 — permission-keys-catalog.md §4 + F90/F91/F92 등록."""
        c = _read(PERM_CATALOG)
        for token in (
            "F90", "F91", "F92",
            "admin.audit.read",
            "admin.metrics.read",
            "admin.health.read",
        ):
            self.assertIn(token, c, f"catalog missing: {token}")

    def test_S_04_no_new_sql_in_ops_layer(self):
        """TC-C14-S-04 — ops_service / ops router 에 직접 SQL 호출 0건 (DEC-040)."""
        sources = [("ops_service.py", _read(OPS_SERVICE)), ("ops.py", _read(OPS_ROUTER))]
        forbidden_call = [r"\bexecute_query\s*\(", r"\bexecute_in_transaction\s*\("]
        forbidden_lit = [
            r"[\"']\s*INSERT\s+INTO\b",
            r"[\"']\s*UPDATE\s+\w+\s+SET\b",
            r"[\"']\s*DELETE\s+FROM\b",
            r"[\"']\s*CREATE\s+TABLE\b",
            r"[\"']\s*SELECT\s+.+\s+FROM\b",
        ]

        def strip_doc(src: str) -> str:
            no_c = "\n".join(ln for ln in src.splitlines() if not ln.lstrip().startswith("#"))
            no_d = re.sub(r'"""[\s\S]*?"""', "", no_c)
            return re.sub(r"'''[\s\S]*?'''", "", no_d)

        for fname, src in sources:
            stripped = strip_doc(src)
            for pat in forbidden_call + forbidden_lit:
                m = re.search(pat, stripped)
                self.assertIsNone(
                    m,
                    f"{fname} uses forbidden pattern '{pat}': {m.group(0) if m else ''}",
                )

    def test_S_05_router_uses_3_require_permissions(self):
        """TC-C14-S-05 — ops router 가 admin.{audit,metrics,health}.read 3 권한 부착."""
        src = _read(OPS_ROUTER)
        used = set(re.findall(r"require_permission\(\s*[\"']([\w\.]+)[\"']\s*\)", src))
        expected = {"admin.audit.read", "admin.metrics.read", "admin.health.read"}
        self.assertEqual(
            used, expected,
            f"ops router require_permission codes mismatch: got={used}, want={expected}",
        )

    def test_S_06_prometheus_metrics_defined(self):
        """TC-C14-S-06 — ops_service 가 Counter/Gauge/Histogram 정의 + 라벨 카디널리티 정합."""
        src = _read(OPS_SERVICE)
        for token in (
            "Counter(",
            "Histogram(",
            "Gauge(",
            "http_requests_total",
            "http_errors_total",
            "http_request_duration_seconds",
            "db_queries_total",
            "db_pool_size",
        ):
            self.assertIn(token, src, f"ops_service missing: {token}")
        # forbidden labels (user_id/request_id/hcode_full) 가 Counter labels= 에 등장하면 안 됨
        # 단순 grep — labels=[ ... ] 안 검사 (정밀)
        labels_blocks = re.findall(r"labels\s*=\s*\[(.*?)\]", src, re.DOTALL)
        joined = " ".join(labels_blocks)
        for forbidden in ("user_id", "request_id", "hcode_full"):
            self.assertNotIn(
                f'"{forbidden}"', joined,
                f"forbidden label key '{forbidden}' present in metric labels — cardinality violation",
            )

    def test_S_07_main_router_registered(self):
        """TC-C14-S-07 — main.py 에 ops.router include_router 등록."""
        c = _read(MAIN_PY)
        self.assertIn("ops", c)
        self.assertIn("app.include_router(ops.router)", c)


# ============================================================================
# R — 런타임 가드
# ============================================================================
@skipUnless(_RUNTIME_OK, "T5 dependencies not ready")
class RuntimeGuardC14(TestCase):

    def setUp(self):
        app.dependency_overrides[get_current_user] = _override_admin
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides[get_current_user] = _override_admin

    def test_R_01_health_full_dependency_split(self):
        """TC-C14-R-01 — /health/full 응답에 dependencies 별 status 분리."""
        r = self.client.get("/api/v1/health/full")
        self.assertIn(r.status_code, (200, 503))
        body = r.json()
        self.assertIn("status", body)
        self.assertIn(body["status"], ("ok", "degraded", "fail"))
        self.assertIn("dependencies", body)
        for k in ("db", "disk", "external"):
            self.assertIn(k, body["dependencies"])
        self.assertIn("uptime_seconds", body)

    def test_R_02_metrics_prometheus_format(self):
        """TC-C14-R-02 — /metrics → Prometheus exposition (text 0.0.4)."""
        # 메트릭 1건 emit (counter inc) 후 노출 확인
        from app.services import ops_service as _ops
        _ops.HTTP_REQUESTS_TOTAL.labels(
            method="GET", endpoint_pattern="/test", status_class="2xx"
        ).inc()
        r = self.client.get("/metrics")
        self.assertEqual(r.status_code, 200)
        ct = r.headers.get("content-type", "")
        self.assertIn("text/plain", ct)
        body = r.text
        # 메트릭 이름이 노출되어야 함 (HELP/TYPE 메타라인 포함)
        self.assertIn("# TYPE http_requests_total counter", body)
        self.assertIn("http_requests_total", body)

    def test_R_03_in_app_banner_etag(self):
        """TC-C14-R-03 — /admin/alerts → ETag + If-Match 누락 428 + 불일치 409."""
        # 알림 1건 생성
        r = self.client.post(
            "/api/v1/admin/alerts",
            params={"severity": "warn", "message": "test alert"},
        )
        self.assertEqual(r.status_code, 200)
        alert_id = r.json()["id"]

        # ETag 조회
        r = self.client.get("/api/v1/admin/alerts")
        self.assertEqual(r.status_code, 200)
        etag = r.headers.get("etag")
        self.assertIsNotNone(etag, "alerts response must include ETag header")
        self.assertTrue(etag.startswith('W/"alerts-'), f"unexpected etag: {etag}")

        # If-Match 누락 → 428
        r = self.client.delete(f"/api/v1/admin/alerts/{alert_id}")
        self.assertEqual(r.status_code, 428)
        body = r.json()
        self.assertEqual(body["detail"]["code"], "PRECONDITION_REQUIRED")

        # If-Match 불일치 → 409
        r = self.client.delete(
            f"/api/v1/admin/alerts/{alert_id}",
            headers={"If-Match": 'W/"alerts-9999999"'},
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["detail"]["code"], "STALE_VERSION")

        # If-Match 정합 → 200
        r = self.client.delete(
            f"/api/v1/admin/alerts/{alert_id}",
            headers={"If-Match": etag},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["dismissed"], alert_id)

    def test_R_04_audit_view_guard_and_ringbuffer(self):
        """TC-C14-R-04 — /admin/audit + emit 후 ring buffer 적재 정합."""
        # admin emit
        r = self.client.post(
            "/api/v1/admin/audit/test-emit",
            params={"channel": "audit.auth", "message": "smoke test admin"},
        )
        self.assertEqual(r.status_code, 200)
        # audit 조회
        r = self.client.get("/api/v1/admin/audit", params={"limit": 10})
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertIn("items", body)
        self.assertIn("total", body)
        self.assertGreaterEqual(body["total"], 1)
        # 최신 1건이 우리 메시지인지 확인
        msgs = [e.get("msg") for e in body["items"]]
        self.assertTrue(
            any("smoke test admin" in m for m in msgs),
            f"emitted message not found in ring buffer: {msgs}",
        )

    def test_R_05_audit_operator_dselect(self):
        """TC-C14-R-05 — operator role + 본인 hcode='5555' → 본인 hcode 매칭만 노출."""
        from app.services import ops_service as _ops
        # admin 으로 다양한 메시지 emit
        self.client.post(
            "/api/v1/admin/audit/test-emit",
            params={"channel": "audit.outbound", "message": "hcode 5555 outbound op A"},
        )
        self.client.post(
            "/api/v1/admin/audit/test-emit",
            params={"channel": "audit.outbound", "message": "hcode 9999 outbound op B"},
        )
        # operator hcode='5555' 로 dependency override 교체 후 audit 조회
        def _op() -> dict:
            return _override_operator("5555") | {"permissions": ["admin.audit.read"]}

        app.dependency_overrides[get_current_user] = _op
        try:
            r = self.client.get("/api/v1/admin/audit", params={"limit": 50})
            self.assertEqual(r.status_code, 200)
            items = r.json().get("items", [])
            for e in items:
                self.assertIn("5555", e.get("msg", ""), f"d_select leak (operator): {e}")
        finally:
            app.dependency_overrides[get_current_user] = _override_admin

    def test_R_06_metrics_no_forbidden_labels(self):
        """TC-C14-R-06 — /metrics 출력에 forbidden 라벨 키 (user_id/request_id) 미등장."""
        r = self.client.get("/metrics")
        self.assertEqual(r.status_code, 200)
        text = r.text
        for forbidden in ("user_id=", "request_id=", "hcode_full="):
            self.assertNotIn(
                forbidden, text,
                f"forbidden label '{forbidden}' present in /metrics output — cardinality violation",
            )


if __name__ == "__main__":
    main(verbosity=2)
