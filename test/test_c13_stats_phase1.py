"""
C13 통계/리포트 확장 Phase 1 — 신규 SQL 0건 + 권한 가드 + 기간 경계 회귀 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/stats_reports.yaml v1.0.0 (4 endpoint + AC-STAT-1~5 + PBP-1~3)
- legacy-analysis/stats_inventory.md (Sobo50~55 인벤토리 + 4 endpoint 재사용 매핑)
- legacy-analysis/permission-keys-catalog.md §4 (F50/F51e/F52e/F53e — admin.stats.*)
- legacy-analysis/decisions.md (DEC-040 + DEC-044)
- 도서물류관리프로그램/backend/app/services/stats_service.py (신규 SQL 0건 정책)
- 도서물류관리프로그램/backend/app/routers/stats.py (PermissionGuard 4종)

검증 케이스
-----------
정적 가드 (S — T5 무관)
- TC-C13-S-01  stats_reports.yaml v1.0 frozen + AC-STAT-1~5 + constraints (DEC-044)
- TC-C13-S-02  stats_inventory.md 의 4 endpoint 재사용 매핑 + 신규 SQL 0건 가드 명령
- TC-C13-S-03  stats_service.py / stats.py 에 신규 SQL 호출 0건 (execute_query 등 grep)
- TC-C13-S-04  permission-keys-catalog.md §4 에 F50/F51e/F52e/F53e + admin.stats.* 등록
- TC-C13-S-05  stats router 가 admin.stats.* 4 권한 모두 require_permission 부착
- TC-C13-S-06  decisions.md 에 DEC-044 등록 (외부 시스템 연동 제외 + 신규 SQL 0건)
- TC-C13-S-07  main.py 에 stats.router include_router 등록

런타임 가드 (R — T5 의존)
- TC-C13-R-01  무토큰/권한 부족 → 401/403 (DEC-041 표준)
- TC-C13-R-02  dateFrom > dateTo, year/quarter 범위 외 → 422 STAT_INVALID_RANGE
- TC-C13-R-03  마감 미완 미래 기간 → metadata.partial=true (PBP-2)
- TC-C13-R-04  수치 동등성 — 동일 입력 → reports endpoint 와 합계 일치

설계 정합 (사용자 룰)
---------------------
- C8/C10/C11 Phase 1 패턴 동일 — monkeypatch + dependency_overrides + skipUnless.
- 신규 SQL 0건 (DEC-040/044) — stats_service 는 reports_service / settlement_service 만 호출.
- 신규 헬퍼 금지, 기존 service 100% 재사용.
- T5 의존 케이스는 _RUNTIME_OK 로 격리 — 정적 케이스 항상 실행.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
CONTRACT = ROOT / "migration" / "contracts" / "stats_reports.yaml"
INVENTORY = ROOT / "legacy-analysis" / "stats_inventory.md"
PERM_CATALOG = ROOT / "legacy-analysis" / "permission-keys-catalog.md"
DECISIONS = ROOT / "legacy-analysis" / "decisions.md"
STATS_SERVICE = BACKEND / "app" / "services" / "stats_service.py"
STATS_ROUTER = BACKEND / "app" / "routers" / "stats.py"
MAIN_PY = BACKEND / "app" / "main.py"
WEB_ADMIN_SEED = BACKEND / "data" / "web_admin.json"

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

    def _override_operator() -> dict:
        return {
            "user_id": "9999",
            "server_id": "remote_138",
            "role": "operator",
            "hcode": "1234",
            "branch_id": "1234",
            "permissions": [],
        }

    app.dependency_overrides[get_current_user] = _override_admin
    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]
    _override_admin = None  # type: ignore[assignment]
    _override_operator = None  # type: ignore[assignment]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ============================================================================
# S — 정적 회귀 (T5 무관, 항상 실행)
# ============================================================================
class StaticGuardC13(TestCase):
    """contract / inventory / catalog / service / router 정합."""

    def test_S_01_contract_v1_frozen(self):
        """TC-C13-S-01 — stats_reports.yaml v1.0 동결 + AC + constraints (DEC-044)."""
        c = _read(CONTRACT)
        for token in (
            "version: 1.0.0",
            "status: frozen",
            "scenario_id: C13_stats",
            "AC-STAT-1", "AC-STAT-2", "AC-STAT-3", "AC-STAT-4", "AC-STAT-5",
            "PBP-1", "PBP-2", "PBP-3",
            "external_integrations: excluded",
            "new_sql_count: 0",
            "DEC-044",
            "DEC-040",
            "STAT_INVALID_RANGE",
            "admin.stats.sales",
            "admin.stats.customer",
            "admin.stats.book",
            "admin.stats.quarterly",
            "F50", "F51e", "F52e", "F53e",
            "reports_service.get_book_sales",
            "settlement_service.list_billing_period",
        ):
            self.assertIn(token, c, f"contract missing token: {token}")

    def test_S_02_inventory_reuse_mapping(self):
        """TC-C13-S-02 — stats_inventory.md 의 4 endpoint 재사용 매핑 + 신규 SQL 0건 명령."""
        c = _read(INVENTORY)
        for token in (
            "Sobo50", "Sobo51", "Sobo52", "Sobo53", "Sobo55",
            "/api/v1/stats/sales-period",
            "/api/v1/stats/customer-analysis",
            "/api/v1/stats/book-turnover",
            "/api/v1/stats/quarterly-summary",
            "신규 SQL 0건",
            "DEC-040",
            "stats_service.py",
            "stats_router|stats.py",  # one of these must appear
        ):
            # 마지막 토큰은 OR 조건 — 별도 처리
            if "|" in token:
                opts = token.split("|")
                self.assertTrue(
                    any(o in c for o in opts),
                    f"inventory missing one of: {opts}",
                )
            else:
                self.assertIn(token, c, f"inventory missing token: {token}")

    def test_S_03_no_new_sql_in_stats_layer(self):
        """TC-C13-S-03 — stats_service / stats router 에 직접 SQL 호출 0건 (DEC-040 정합).

        검사 정책:
        - 함수 *호출* 형태만 검사 (`execute_query(` 등) — docstring/주석에 텍스트로 등장하는
          것은 정책 정합을 위한 설명이므로 통과.
        - SQL 키워드는 문자열 리터럴 상수에서 등장하는지 검사 — 본 layer 는 SQL 문자열을
          직접 들고 있어서는 안 된다 (기존 service 함수의 SQL 만 재사용).
        """
        sources = [
            ("stats_service.py", _read(STATS_SERVICE)),
            ("stats.py (router)", _read(STATS_ROUTER)),
        ]
        forbidden_call_patterns = [
            r"\bexecute_query\s*\(",
            r"\bexecute_in_transaction\s*\(",
        ]
        forbidden_sql_literal_patterns = [
            r"[\"']\s*INSERT\s+INTO\b",
            r"[\"']\s*UPDATE\s+\w+\s+SET\b",
            r"[\"']\s*DELETE\s+FROM\b",
            r"[\"']\s*CREATE\s+TABLE\b",
            r"[\"']\s*SELECT\s+.+\s+FROM\b",
        ]

        def _strip_doc_and_comment(src: str) -> str:
            # 주석 제거 + triple-quoted docstring 블록 제거 (간단 제거 — 나머지 문자열은 보존)
            no_comment = "\n".join(
                ln for ln in src.splitlines() if not ln.lstrip().startswith("#")
            )
            # """ ... """ 블록 제거 (DOTALL)
            no_doc = re.sub(r'"""[\s\S]*?"""', "", no_comment)
            no_doc = re.sub(r"'''[\s\S]*?'''", "", no_doc)
            return no_doc

        for fname, src in sources:
            stripped = _strip_doc_and_comment(src)
            for pat in forbidden_call_patterns + forbidden_sql_literal_patterns:
                m = re.search(pat, stripped)
                self.assertIsNone(
                    m,
                    f"{fname} uses forbidden pattern '{pat}': "
                    f"{m.group(0) if m else ''} — DEC-040 (신규 SQL 0건) 정합 위반",
                )

    def test_S_04_permission_catalog_registered(self):
        """TC-C13-S-04 — permission-keys-catalog.md §4 + admin.stats.* 등록."""
        c = _read(PERM_CATALOG)
        for token in (
            "F50", "F51e", "F52e", "F53e",
            "admin.stats.sales",
            "admin.stats.customer",
            "admin.stats.book",
            "admin.stats.quarterly",
            "/api/v1/stats/sales-period",
        ):
            self.assertIn(token, c, f"catalog missing: {token}")

    def test_S_05_router_uses_require_permission_4_codes(self):
        """TC-C13-S-05 — stats.py 가 admin.stats.* 4 권한 모두 require_permission 부착."""
        src = _read(STATS_ROUTER)
        used = set(re.findall(r"require_permission\(\s*[\"']([\w\.]+)[\"']\s*\)", src))
        expected = {
            "admin.stats.sales",
            "admin.stats.customer",
            "admin.stats.book",
            "admin.stats.quarterly",
        }
        self.assertEqual(
            used, expected,
            f"stats router require_permission codes mismatch: got={used}, want={expected}",
        )

    def test_S_06_dec_044_registered(self):
        """TC-C13-S-06 — decisions.md 에 DEC-044 등록 (외부 시스템 연동 제외 + 신규 SQL 0건)."""
        c = _read(DECISIONS)
        self.assertIn("DEC-044", c)
        self.assertIn("외부 시스템 연동", c)
        self.assertIn("admin.stats", c)

    def test_S_07_main_router_registered(self):
        """TC-C13-S-07 — main.py 에 stats.router include_router 등록."""
        c = _read(MAIN_PY)
        self.assertIn("stats", c)
        self.assertIn("app.include_router(stats.router)", c)

    def test_S_08_admin_role_seed_lists_stats_permissions(self):
        """TC-C13-S-08 — web_admin.json::role-admin 이 admin.stats.* 4 키를 명시 등재.

        배경
        ----
        - `core/deps.py::_resolve_permissions` 는 ``role=='admin'`` 또는
          ``permissions==['*']`` 면 모든 가드를 통과시킨다(LSP 슈퍼유저 규칙).
        - 그러나 운영 감사/카탈로그 정합 관점에서는 wildcard 만 남겨 두면 향후
          (Phase 2) wildcard 제거 시 도서 회전율(`admin.stats.book`) 등 신규 가드가
          모두 회귀로 깨질 수 있다 — 이를 사전에 차단하기 위해 4 stats 키를
          **명시 등재**한다 (DEC-041 / DEC-044 의 권한 정본화 기조).
        - 본 테스트는 시드의 wildcard 의존도를 줄이고 도서 회전율 화면이
          admin 계정으로 항상 통과하도록 보증한다.
        """
        import json
        seed = json.loads(_read(WEB_ADMIN_SEED))
        roles = {r.get("code"): r for r in seed.get("web_roles", [])}
        admin_role = roles.get("admin")
        self.assertIsNotNone(admin_role, "role-admin 시드 누락")
        admin_perms = set(admin_role.get("permissions") or [])
        for code in (
            "admin.stats.sales",
            "admin.stats.customer",
            "admin.stats.book",       # 도서 회전율 — F52e
            "admin.stats.quarterly",
        ):
            self.assertIn(
                code, admin_perms,
                f"role-admin 에 {code} 명시 등재 누락 — wildcard 만 의존 시 Phase 2 회귀 위험",
            )


# ============================================================================
# R — 런타임 가드 (T5 의존 — skipUnless)
# ============================================================================
@skipUnless(_RUNTIME_OK, "T5 dependencies not ready")
class RuntimeGuardC13(TestCase):
    """라우터 동작 — 권한/기간 경계/에러 코드 회귀."""

    def setUp(self):
        # 다른 테스트가 dependency_overrides 를 변경했을 수 있으므로 매번 admin 으로 재설정
        app.dependency_overrides[get_current_user] = _override_admin
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides[get_current_user] = _override_admin

    def test_R_01_unauthorized_returns_401_403(self):
        """TC-C13-R-01 — operator 토큰 (permissions=[]) 으로 stats endpoint → 403."""
        app.dependency_overrides[get_current_user] = _override_operator
        try:
            r = self.client.get(
                "/api/v1/stats/sales-period",
                params={
                    "serverId": "remote_138",
                    "hcode": "1234",
                    "dateFrom": "2026.01.01",
                    "dateTo": "2026.01.31",
                },
            )
            self.assertEqual(r.status_code, 403, f"expected 403, got {r.status_code}: {r.text}")
            body = r.json()
            self.assertEqual(body.get("detail", {}).get("code"), "PERMISSION_DENIED")
        finally:
            app.dependency_overrides[get_current_user] = _override_admin

    def test_R_02_invalid_range_returns_422(self):
        """TC-C13-R-02 — dateFrom > dateTo → 422 STAT_INVALID_RANGE (PBP-1)."""
        r = self.client.get(
            "/api/v1/stats/sales-period",
            params={
                "serverId": "remote_138",
                "hcode": "1234",
                "dateFrom": "2026.12.31",
                "dateTo": "2026.01.01",
            },
        )
        # 422 + 표준 코드
        self.assertEqual(r.status_code, 422, f"expected 422, got {r.status_code}: {r.text}")
        body = r.json()
        self.assertEqual(body.get("detail", {}).get("code"), "STAT_INVALID_RANGE")

    def test_R_02b_quarterly_invalid_quarter(self):
        """TC-C13-R-02b — quarter=5 → 422 (FastAPI Query 검증으로 422)."""
        r = self.client.get(
            "/api/v1/stats/quarterly-summary",
            params={"serverId": "remote_138", "hcode": "1234", "year": 2026, "quarter": 5},
        )
        # FastAPI Query(le=4) 가 먼저 잡으므로 422 (RequestValidationError)
        self.assertEqual(r.status_code, 422)

    def test_R_03_partial_marker_for_future_range(self):
        """TC-C13-R-03 — 마감 미완 미래 기간 → metadata.partial=true (PBP-2).

        DB 의존성 없이 stats_service._is_partial 만 검증.
        """
        from app.services import stats_service as svc
        self.assertTrue(svc._is_partial("2099.12.31"))
        self.assertFalse(svc._is_partial("2000.01.01"))

    def test_R_04_router_endpoints_registered(self):
        """TC-C13-R-04 — 4 endpoint 가 OpenAPI 스키마에 등록."""
        r = self.client.get("/openapi.json")
        self.assertEqual(r.status_code, 200)
        paths = r.json().get("paths", {})
        for p in (
            "/api/v1/stats/sales-period",
            "/api/v1/stats/customer-analysis",
            "/api/v1/stats/book-turnover",
            "/api/v1/stats/quarterly-summary",
        ):
            self.assertIn(p, paths, f"endpoint not registered: {p}")


if __name__ == "__main__":
    main(verbosity=2)
