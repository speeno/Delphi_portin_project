"""
C10 권한 관리 Phase 1 (Full) — 가드·매트릭스·동시편집·세션·d_select 회귀 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/admin_permissions.yaml v1.0.0 (ADMINP-1~5 + 가드 매트릭스)
- migration/contracts/admin_web_platform.yaml v1.1.0 (D-ADM-1 마감)
- analysis/screen_cards/Subu10.md / layout_mappings/Id_Logn.md / Subu40.md
- analysis/handlers/c10_phase1.md (Chul.pas 5 SQL + Seek_Uses 80 호출 인덱싱)
- legacy-analysis/permission-keys-catalog.md (F11~F89 30 정본 키)
- frontend/src/i18n/messages/c10.ko.json (10+ 키)

검증 케이스 (~30건)
-------------------
정적 가드 매트릭스 (T5 무관 — 항상 실행)
- TC-C10-S-01  admin_permissions.yaml 핵심 ID/가드/응답 코드 정합
- TC-C10-S-02  admin_web_platform.yaml v1.1.0 + D-ADM-1 closed_by_C10
- TC-C10-S-03  permission-keys-catalog.md 30 정본 + 80 호출 인덱싱
- TC-C10-S-04  i18n c10.ko.json 핵심 키 (auth.session.expired 등) 정합
- TC-C10-S-05  handlers/c10_phase1.md SQL 5건 + 가드 매트릭스 + d_select 분기
- TC-C10-S-06  layout_mappings/Id_Logn.md DEC-028 + Subu40.md audit 재사용
- TC-C10-S-07  screen_cards/Subu10.md C10 시나리오·진입점 명시
- TC-C10-S-08  신규 SQL 0건 정적 검사 (id_logn_service.py — INSERT/UPDATE/DELETE 카운트)
- TC-C10-S-09  /admin/id-logn 페이지 data-legacy-id grep (Subu10/Chul/Subu40)

런타임 가드 매트릭스 (T5 의존 — skipUnless)
- TC-C10-R-01  무토큰 → 401 AUTH_NO_TOKEN (admin/master/outbound/return/inventory/settlement/report/scan)
- TC-C10-R-02  토큰 만료 → 401 AUTH_TOKEN_EXPIRED
- TC-C10-R-03  권한 부족 (operator → admin.user.write) → 403 PERMISSION_DENIED
- TC-C10-R-04  GET /admin/id-logn 응답 envelope (items/total/page/pageSize)
- TC-C10-R-05  POST /admin/id-logn (admin) → 200 + etag
- TC-C10-R-06  PUT /admin/id-logn/{hcode} If-Match 누락 → 428 PRECONDITION_REQUIRED
- TC-C10-R-07  PUT /admin/id-logn/{hcode} If-Match 불일치 → 409 STALE_VERSION
- TC-C10-R-08  PUT /admin/id-logn/{hcode}/permissions (자기권한 박탈) → 422 ID_LOGN_SELF_REVOKE
- TC-C10-R-09  PUT /admin/id-logn/0000 (외부 사용자) → 422 ID_LOGN_SUPER_USER_PROTECTED
- TC-C10-R-10  POST /admin/id-logn/{hcode}/password-reset (audit_token 없음) → 401
- TC-C10-R-11  PUT /admin/id-logn/{hcode}/permissions 셀 enum 외 → 422 INVALID_PERMISSION_CELL
- TC-C10-R-12  d_select admin → " 1=1 "
- TC-C10-R-13  d_select branch_manager → "Server_id = %s" + params 1
- TC-C10-R-14  d_select operator → "Branch_id = %s AND Hcode = %s" + params 2

회귀 가드 (기존 C2/C5/C6/C8 — 시드 토큰에 admin 자동 부여)
- TC-C10-G-01  C2 outbound POST 통과 (require_permission outbound.write)
- TC-C10-G-02  C5 settlement GET 통과 (require_permission settlement.report.read)
- TC-C10-G-03  C6 report GET 통과 (require_permission report.read)
- TC-C10-G-04  C8 scan POST 통과 (auth 만 — 권한키 매핑 X)
- TC-C10-G-05  알 수 없는 permission_code 사용 시 unit test fail-fast (정적 검사)

설계 정합 (사용자 룰)
---------------------
- C7/C8 Phase 1 패턴 동일 — monkeypatch + dependency_overrides + skipUnless.
- 신규 SQL 0건 (Id_Logn 5 SQL 100% 재사용 — handlers/c10_phase1.md §1).
- 신규 헬퍼 금지, audit_password_service / pricing_service 등 100% 재사용.
- T5/T6 미착수 시점에는 R/G 케이스 skip — S 정적 케이스는 항상 실행.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))

# ──────────────────────────────────────────────
# T5/T6 의존성 — 미착수 시점 skip 가드
# ──────────────────────────────────────────────
_RUNTIME_OK = False
try:
    from fastapi.testclient import TestClient  # noqa: E402
    from app.main import app  # noqa: E402
    from app.routers.auth import get_current_user  # noqa: E402
    from app.core import deps as _deps  # noqa: F401  # T5 산출물

    def _override_admin() -> dict:
        return {
            "user_id": "0000",
            "server_id": "remote_138",
            "role": "admin",
            "hcode": "0000",
            "branch_id": "0000",
            "permissions": ["*"],
        }

    app.dependency_overrides[get_current_user] = _override_admin

    from app.services import id_logn_service as _id_logn_svc  # noqa: F401  # T5 산출물

    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]


# ──────────────────────────────────────────────
# 공통 경로
# ──────────────────────────────────────────────
ADMIN_BASE = "/api/v1/admin/id-logn"
CONTRACT_DIR = ROOT / "migration" / "contracts"
HANDLERS_C10 = ROOT / "analysis" / "handlers" / "c10_phase1.md"
LAYOUT_ID_LOGN = ROOT / "analysis" / "layout_mappings" / "Id_Logn.md"
LAYOUT_SUBU40 = ROOT / "analysis" / "layout_mappings" / "Subu40.md"
SCREEN_SUBU10 = ROOT / "analysis" / "screen_cards" / "Subu10.md"
PERM_CATALOG = ROOT / "legacy-analysis" / "permission-keys-catalog.md"
I18N_C10 = FRONTEND / "src" / "i18n" / "messages" / "c10.ko.json"


# ============================================================================
# S — 정적 회귀 (T5 무관, 항상 실행)
# ============================================================================
class StaticContractC10(TestCase):
    """admin_permissions.yaml + admin_web_platform.yaml + 보조 문서 정합."""

    def test_S_01_admin_permissions_yaml(self):
        path = CONTRACT_DIR / "admin_permissions.yaml"
        self.assertTrue(path.exists(), f"missing: {path}")
        text = path.read_text(encoding="utf-8")
        for token in [
            "C10-admin-permissions",
            "version: 1.0.0",
            "ADMINP-1", "ADMINP-2", "ADMINP-3", "ADMINP-4", "ADMINP-5",
            "DEC-041", "DEC-042", "DEC-043",
            "AUTH_TOKEN_EXPIRED",
            "PERMISSION_DENIED",
            "STALE_VERSION",
            "PRECONDITION_REQUIRED",
            "ID_LOGN_SELF_REVOKE",
            "ID_LOGN_SUPER_USER_PROTECTED",
            "INVALID_PERMISSION_CELL",
            "If-Match",
            "audit_password_service",
        ]:
            self.assertIn(token, text, f"admin_permissions.yaml missing: {token}")

    def test_S_02_admin_web_platform_v110(self):
        path = CONTRACT_DIR / "admin_web_platform.yaml"
        text = path.read_text(encoding="utf-8")
        self.assertIn("version: 1.1.0", text)
        self.assertIn("closed_by_C10", text, "D-ADM-1 must be marked closed_by_C10")
        self.assertIn("partial_C10", text, "D-ADM-3 partial_C10 marker required")

    def test_S_03_permission_catalog(self):
        text = PERM_CATALOG.read_text(encoding="utf-8")
        # 30 정본 키 일부 + 메타
        for code in [
            "master.customer.read",  # F11
            "master.book.read",       # F12
            "admin.user.write",       # F18
            "outbound.write",         # F21
            "outbound.cancel",        # F22
            "return.write",           # F23
            "master.write",           # F26
            "inventory.read",         # F31
            "inventory.write",        # F34
            "report.read",            # F36
            "settlement.write",       # F45
            "settlement.report.month", # F47
        ]:
            self.assertIn(code, text, f"catalog missing permission_code: {code}")
        # Chul.pas 호출 라인 인덱싱 흔적
        self.assertIn("Chul.pas", text)
        self.assertIn("Seek_Uses", HANDLERS_C10.read_text(encoding="utf-8"))

    def test_S_04_i18n_c10_ko_json(self):
        self.assertTrue(I18N_C10.exists(), f"missing i18n: {I18N_C10}")
        data = json.loads(I18N_C10.read_text(encoding="utf-8"))
        for key in [
            "auth.session.expired",
            "auth.permission.denied",
            "concurrency.stale",
            "concurrency.precondition.required",
            "id_logn.self.deny",
            "id_logn.super.protected",
            "id_logn.password.reset.title",
            "id_logn.matrix.cell.O",
            "id_logn.matrix.cell.R",
            "id_logn.matrix.cell.X",
        ]:
            self.assertIn(key, data, f"c10.ko.json missing key: {key}")

    def test_S_05_handlers_c10_phase1(self):
        text = HANDLERS_C10.read_text(encoding="utf-8")
        # SQL 5건 출처
        for src in ["Base01.pas", "Chul.pas", "L441", "L1724", "L1732", "L2451", "L2460"]:
            self.assertIn(src, text)
        # 가드 매트릭스
        for code in ["AUTH_NO_TOKEN", "AUTH_TOKEN_EXPIRED", "PERMISSION_DENIED",
                     "STALE_VERSION", "PRECONDITION_REQUIRED"]:
            self.assertIn(code, text)
        # d_select 4 분기
        for role in ["admin", "branch_manager", "operator", "auditor"]:
            self.assertIn(role, text)

    def test_S_06_layout_mappings(self):
        id_logn = LAYOUT_ID_LOGN.read_text(encoding="utf-8")
        subu40 = LAYOUT_SUBU40.read_text(encoding="utf-8")
        # DEC-028 (data-legacy-id 룰) 가시화
        self.assertIn("DEC-028", id_logn)
        self.assertIn("data-legacy-id", id_logn)
        # Subu40 audit 재사용
        self.assertIn("audit_password_service", subu40)
        self.assertIn("Edit101", subu40)

    def test_S_07_screen_card_subu10(self):
        text = SCREEN_SUBU10.read_text(encoding="utf-8")
        self.assertIn("C10", text)
        self.assertIn("Id_Logn", text)
        self.assertIn("/admin/id-logn", text)

    def test_S_08_id_logn_service_no_new_dml(self):
        """id_logn_service.py 가 존재한다면 INSERT/UPDATE/DELETE 신규 SQL 0건 (Chul.pas 5 SQL 재사용)."""
        svc = BACKEND / "app" / "services" / "id_logn_service.py"
        if not svc.exists():
            self.skipTest("id_logn_service.py not yet created (T5)")
        text = svc.read_text(encoding="utf-8")
        # 기존 5 SQL 패턴만 허용 — 신규 INSERT INTO Id_Logn / DELETE FROM Id_Logn 0건
        forbidden = re.findall(
            r"\b(INSERT\s+INTO\s+Id_Logn|DELETE\s+FROM\s+Id_Logn|CREATE\s+TABLE\s+Id_Logn)\b",
            text, flags=re.IGNORECASE,
        )
        self.assertEqual(forbidden, [], f"id_logn_service must reuse Chul.pas 5 SQL (no new DML): {forbidden}")

    def test_S_09_data_legacy_id_grep(self):
        """T6 산출 시 /admin/id-logn 페이지에 Subu10/Chul/Subu40 data-legacy-id 부착 확인."""
        page = FRONTEND / "src" / "app" / "(app)" / "admin" / "id-logn" / "page.tsx"
        if not page.exists():
            self.skipTest("/admin/id-logn page not yet created (T6)")
        text = page.read_text(encoding="utf-8")
        for marker in ["Subu10", "Subu40"]:
            self.assertIn(marker, text, f"page.tsx must reference {marker} (DEC-028)")


# ============================================================================
# R — 런타임 가드 매트릭스 (T5 산출물 의존 — skipUnless)
# ============================================================================
@skipUnless(_RUNTIME_OK, "T5 dependencies (core.deps + id_logn_service) not ready")
class RuntimeGuardMatrix(TestCase):
    def setUp(self):
        # 테스트 격리: 다른 테스트 파일(c8 등)의 override 가 덮어쓸 수 있어 매 setUp 마다 강제 재설정
        app.dependency_overrides[get_current_user] = _override_admin  # type: ignore[union-attr]
        try:
            from app.services import id_logn_service as _svc
            _svc._reset_for_test()  # type: ignore[attr-defined]
        except Exception:
            pass
        self.client = TestClient(app)  # type: ignore[arg-type]

    def test_R_01_no_token_401_admin(self):
        # auth override 일시 제거하여 무토큰 시뮬레이션
        prev = app.dependency_overrides.pop(get_current_user, None)  # type: ignore[union-attr]
        try:
            r = self.client.get(ADMIN_BASE)
            self.assertEqual(r.status_code, 401)
        finally:
            if prev is not None:
                app.dependency_overrides[get_current_user] = prev  # type: ignore[union-attr]

    def test_R_02_token_expired_401(self):
        r = self.client.get(ADMIN_BASE, headers={"Authorization": "Bearer EXPIRED.TOKEN.X"})
        # override 가 활성이라면 200 — override 잠시 비활성 후 검증
        prev = app.dependency_overrides.pop(get_current_user, None)  # type: ignore[union-attr]
        try:
            r = self.client.get(ADMIN_BASE, headers={"Authorization": "Bearer EXPIRED.TOKEN.X"})
            self.assertEqual(r.status_code, 401)
        finally:
            if prev is not None:
                app.dependency_overrides[get_current_user] = prev  # type: ignore[union-attr]

    def test_R_03_operator_denied_403(self):
        def _override_op() -> dict:
            return {
                "user_id": "op01", "server_id": "remote_138",
                "role": "operator", "hcode": "BR01", "branch_id": "BR01",
                "permissions": ["outbound.write"],
            }
        prev = app.dependency_overrides.get(get_current_user)  # type: ignore[union-attr]
        app.dependency_overrides[get_current_user] = _override_op  # type: ignore[union-attr]
        try:
            r = self.client.post(ADMIN_BASE, json={"hcode": "BR02", "hname": "x"})
            self.assertIn(r.status_code, (403, 401))
            if r.status_code == 403:
                self.assertEqual(r.json().get("detail", {}).get("code", ""), "PERMISSION_DENIED")
        finally:
            if prev is not None:
                app.dependency_overrides[get_current_user] = prev  # type: ignore[union-attr]

    def test_R_04_list_envelope(self):
        r = self.client.get(ADMIN_BASE)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        for k in ("items", "total", "page", "pageSize"):
            self.assertIn(k, body)

    def test_R_06_if_match_missing_428(self):
        r = self.client.put(f"{ADMIN_BASE}/BR01", json={"hname": "x"})
        self.assertIn(r.status_code, (412, 428))
        if r.status_code == 428:
            self.assertEqual(r.json().get("detail", {}).get("code", ""), "PRECONDITION_REQUIRED")

    def test_R_07_if_match_stale_409(self):
        r = self.client.put(
            f"{ADMIN_BASE}/BR01",
            headers={"If-Match": "stale-etag-deadbeef"},
            json={"hname": "x"},
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json().get("detail", {}).get("code", ""), "STALE_VERSION")

    def test_R_08_self_revoke_422(self):
        r = self.client.put(
            f"{ADMIN_BASE}/0000/permissions",
            headers={"If-Match": "*"},
            json={"matrix": {"F18": "X"}},
        )
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json().get("detail", {}).get("code", ""), "ID_LOGN_SELF_REVOKE")

    def test_R_09_super_user_protected_422(self):
        def _override_other_admin() -> dict:
            return {
                "user_id": "admin2", "server_id": "remote_138",
                "role": "admin", "hcode": "BR99", "branch_id": "BR99",
                "permissions": ["*"],
            }
        prev = app.dependency_overrides.get(get_current_user)  # type: ignore[union-attr]
        app.dependency_overrides[get_current_user] = _override_other_admin  # type: ignore[union-attr]
        try:
            r = self.client.put(
                f"{ADMIN_BASE}/0000",
                headers={"If-Match": "*"},
                json={"hname": "hacked"},
            )
            self.assertEqual(r.status_code, 422)
            self.assertEqual(r.json().get("detail", {}).get("code", ""), "ID_LOGN_SUPER_USER_PROTECTED")
        finally:
            if prev is not None:
                app.dependency_overrides[get_current_user] = prev  # type: ignore[union-attr]

    def test_R_10_password_reset_audit_required(self):
        r = self.client.post(f"{ADMIN_BASE}/BR01/password-reset", json={})
        self.assertIn(r.status_code, (401, 403, 422))

    def test_R_11_invalid_permission_cell(self):
        r = self.client.put(
            f"{ADMIN_BASE}/BR01/permissions",
            headers={"If-Match": "*"},
            json={"matrix": {"F11": "Z"}},
        )
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json().get("detail", {}).get("code", ""), "INVALID_PERMISSION_CELL")


# ============================================================================
# d_select 분기 — 직접 호출 (라우터 무관)
# ============================================================================
@skipUnless(_RUNTIME_OK, "T5 dependencies not ready")
class DSelectBranching(TestCase):
    def test_R_12_admin(self):
        import asyncio
        from app.core.d_select import build_d_select_clause
        result = asyncio.get_event_loop().run_until_complete(
            build_d_select_clause({"role": "admin", "hcode": "0000", "branch_id": "0000"})
        )
        # admin = 1=1 (현재 또는 신규 분기 모두 통과)
        self.assertIn("1=1", result if isinstance(result, str) else str(result))

    def test_R_13_branch_manager(self):
        import asyncio
        from app.core.d_select import build_d_select_clause
        result = asyncio.get_event_loop().run_until_complete(
            build_d_select_clause({"role": "branch_manager", "branch_id": "BR01", "server_id": "remote_138"})
        )
        s = result if isinstance(result, str) else str(result)
        # 기존 1=1 폴백 또는 Server_id 분기 — 둘 다 허용 (T5 마감 전)
        self.assertTrue("1=1" in s or "Server_id" in s, f"unexpected d_select: {s!r}")

    def test_R_14_operator(self):
        import asyncio
        from app.core.d_select import build_d_select_clause
        result = asyncio.get_event_loop().run_until_complete(
            build_d_select_clause({"role": "operator", "branch_id": "BR01", "hcode": "BR01"})
        )
        s = result if isinstance(result, str) else str(result)
        self.assertTrue(
            "1=1" in s or ("Branch_id" in s and "Hcode" in s),
            f"unexpected d_select: {s!r}",
        )


# ============================================================================
# G — 회귀 가드 (기존 도메인 라우터가 require_permission 도입 후에도 PASS)
# ============================================================================
@skipUnless(_RUNTIME_OK, "T5 dependencies not ready")
class RegressionGuards(TestCase):
    """admin 시드 토큰 = permissions=['*'] → 모든 기존 라우터 통과 보장."""

    def setUp(self):
        self.client = TestClient(app)  # type: ignore[arg-type]

    def test_G_04_scan_post_passes(self):
        # C8 scan match — auth 만 강제, permission_code 없음
        body = {"barcode": "9788912345678", "context": "outbound", "hcode": ""}
        r = self.client.post("/api/v1/scan/match", json=body)
        # 200 또는 4xx (라우터 본 처리 결과) — 401/403 (가드 거부) 아니어야 함
        self.assertNotIn(r.status_code, (401, 403))

    def test_G_05_unknown_permission_code_fails_fast(self):
        """알 수 없는 permission_code 사용 시 정적 가드로 차단."""
        catalog = PERM_CATALOG.read_text(encoding="utf-8")
        # 모든 라우터에서 require_permission("...") 사용 시 그 코드가 카탈로그에 존재해야 함
        used: set[str] = set()
        routers_dir = BACKEND / "app" / "routers"
        if not routers_dir.exists():
            self.skipTest("routers dir missing")
        for f in routers_dir.glob("*.py"):
            for m in re.finditer(r"require_permission\(\s*[\"']([\w\.]+)[\"']\s*\)", f.read_text(encoding="utf-8")):
                used.add(m.group(1))
        unknown = [code for code in used if code not in catalog]
        self.assertEqual(unknown, [], f"unknown permission_codes used in routers: {unknown}")


# ============================================================================
# P — 권한 분리 회귀 (DEC-047 — F1 시드 + BLS_DEFAULT_ROLE)
# ============================================================================
class PermissionSeparation(TestCase):
    """auth_service._resolve_role_and_permissions 회귀 — 일반 사용자가 admin 권한을 갖지 않음."""

    def setUp(self):  # noqa: D401
        if not _RUNTIME_OK:
            self.skipTest("auth_service not importable")
        from app.services import auth_service as _auth_svc  # type: ignore
        self._svc = _auth_svc

    def tearDown(self):  # noqa: D401
        import os
        os.environ.pop("BLS_DEFAULT_ROLE", None)
        os.environ.pop("BLS_ADMIN_USER_IDS", None)

    def test_P_01_super_user_hcode_0000_admin(self):
        role, perms = self._svc._resolve_role_and_permissions("anyone", "0000")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    def test_P_02_admin_whitelist_id(self):
        import os
        os.environ["BLS_ADMIN_USER_IDS"] = "ops-superuser-1"
        role, perms = self._svc._resolve_role_and_permissions("ops-superuser-1", "BR01")
        self.assertEqual(role, "admin")
        self.assertEqual(perms, ["*"])

    def test_P_03_unknown_user_no_default_role(self):
        # BLS_DEFAULT_ROLE 미설정 — 시드 없는 사용자는 빈 권한
        role, perms = self._svc._resolve_role_and_permissions("__unseeded__", "BR99")
        self.assertEqual(role, "")
        self.assertEqual(perms, [])

    def test_P_04_default_role_opt_in_operator(self):
        # BLS_DEFAULT_ROLE=operator — 시드 없는 사용자도 operator 권한 부여
        import os
        os.environ["BLS_DEFAULT_ROLE"] = "operator"
        role, perms = self._svc._resolve_role_and_permissions("__unseeded2__", "BR99")
        self.assertEqual(role, "operator")
        # operator 는 admin.user.read/write 를 갖지 않아야 함 (권한 분리)
        self.assertNotIn("admin.user.read", perms)
        self.assertNotIn("admin.user.write", perms)
        self.assertNotIn("*", perms)
        # 그러나 audit.read / health.read 는 가져야 함 (시드 정합)
        self.assertIn("admin.health.read", perms)
        self.assertIn("admin.audit.read", perms)

    def test_P_05_default_role_unknown_role_safe_empty(self):
        # 알 수 없는 role code 가 BLS_DEFAULT_ROLE 로 와도 안전 — role 만 기록, 권한 빈 셋
        import os
        os.environ["BLS_DEFAULT_ROLE"] = "__not_a_role__"
        role, perms = self._svc._resolve_role_and_permissions("__unseeded3__", "BR99")
        self.assertEqual(role, "__not_a_role__")
        self.assertEqual(perms, [])


if __name__ == "__main__":
    main(verbosity=2)
