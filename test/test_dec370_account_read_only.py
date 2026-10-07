"""DEC-370 — 조회 전용 계정(교문사 등 위러브 창고 출판사 본계정).

사용자 결정(2026-10-03)
----------------------
- 「교문사 계정은 계정 전용 정보를 제외하고 모든 정보 읽기 전용」
- 「교문사와 같은 권한의 계정은 모두 동일하게」 → T3 · warehouse_publisher · chul_09 · publisher_main.
- 자동출력 완료(접수→완료)만 예외 — 교문사 PC 의 역할.
- 부서 계정(경리부 등)과 위러브 관리자(hcode 0000)는 대상 아님.

가드
----
- 계약(허브 정본) == 번들 사본.
- 서버 미들웨어가 대상 계정의 쓰기를 403(ACCOUNT_READ_ONLY)으로 거절, 예외 경로는 통과.
- 비대상 계정은 미들웨어가 막지 않는다.
- 프론트: 화면 caps canWrite=false · 헤더 「조회 전용」 표시.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app
from app.services import account_write_policy as awp

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "migration" / "contracts" / "account_write_policy.yaml"
BUNDLE = ROOT / "도서물류관리프로그램" / "backend" / "data" / "contracts" / "account_write_policy.yaml"
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"

GYOMUNSA = {
    "sub": "교문사", "sid": "remote_153", "hcode": "5019", "role": "operator",
    "account_type": "T3", "build_role": "warehouse_publisher", "account_family": "chul_09",
    "login_profile": "publisher_main", "rdb": "chul_09_db",
}
GYEONGRI = {**GYOMUNSA, "sub": "경리부", "login_profile": "department_accounting"}
WELOVE_ADMIN = {**GYOMUNSA, "sub": "위러브", "hcode": "0000"}
OTHER_FAMILY = {**GYOMUNSA, "account_family": "book_07", "rdb": "book_07_db"}
# DEC-388 — 운영 교문사 본계정 로그인(소유성 ambiguous · DSN-DEC-12): account_family · tenant_id · active_build_id 가 빈다.
AMBIGUOUS_OWNERSHIP = {**GYOMUNSA, "account_family": None, "tenant_id": None, "active_build_id": None}


def _hdr(claims: dict) -> dict:
    return {"Authorization": "Bearer " + create_access_token(dict(claims))}


class PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        awp.reload_for_tests()

    def test_bundle_copy_matches_hub(self) -> None:
        self.assertEqual(HUB.read_text(encoding="utf-8"), BUNDLE.read_text(encoding="utf-8"))

    def test_targets(self) -> None:
        self.assertTrue(awp.is_read_only_account(GYOMUNSA))
        self.assertFalse(awp.is_read_only_account(GYEONGRI))
        self.assertFalse(awp.is_read_only_account(WELOVE_ADMIN))
        self.assertFalse(awp.is_read_only_account(OTHER_FAMILY))
        self.assertFalse(awp.is_read_only_account({}))
        self.assertTrue(awp.is_read_only_account(AMBIGUOUS_OWNERSHIP))  # DEC-388 — 운영 실제 케이스
        self.assertTrue(awp.is_read_only_account({**GYOMUNSA, "rdb": None, "resolved_db": "chul_09_db"}))  # 컨텍스트 키

    def test_allowed_writes(self) -> None:
        for method, path in [
            ("PATCH", "/api/v1/me/profile"),
            ("POST", "/api/v1/me/password"),
            ("PUT", "/api/v1/grid-prefs/outbound.status"),
            ("POST", "/api/v1/auth/refresh"),
            ("POST", "/api/v1/export/table-xlsx"),
            ("PATCH", "/api/v1/transactions/sales-statement/2026.10.02|5019|1||6|출고|00001/complete"),
            ("GET", "/api/v1/masters/book"),
        ]:
            self.assertFalse(awp.blocks(GYOMUNSA, method, path), (method, path))

    def test_blocked_writes(self) -> None:
        for method, path in [
            ("POST", "/api/v1/outbound/orders"),
            ("PATCH", "/api/v1/outbound/orders/batch/request"),
            ("POST", "/api/v1/transactions/sales-statement/urgent-print"),
            ("DELETE", "/api/v1/transactions/sales-statement/k"),
            ("PATCH", "/api/v1/masters/book/1234"),
            ("POST", "/api/v1/me/tenant-print/seal"),
            ("POST", "/api/v1/ledger/adjustments"),
        ]:
            self.assertTrue(awp.blocks(GYOMUNSA, method, path), (method, path))
            self.assertFalse(awp.blocks(GYEONGRI, method, path), (method, path))


class MiddlewareTests(unittest.TestCase):
    def setUp(self) -> None:
        awp.reload_for_tests()
        self.client = TestClient(app)

    def test_readonly_account_write_is_403(self) -> None:
        r = self.client.post("/api/v1/outbound/orders", json={}, headers=_hdr(GYOMUNSA))
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json()["detail"]["code"], "ACCOUNT_READ_ONLY")

    def test_other_account_not_blocked_by_middleware(self) -> None:
        r = self.client.post("/api/v1/outbound/orders", json={}, headers=_hdr(GYEONGRI))
        self.assertNotEqual(
            (r.json().get("detail") or {}).get("code") if isinstance(r.json().get("detail"), dict) else None,
            "ACCOUNT_READ_ONLY",
        )

    def test_no_token_passes_to_route_auth(self) -> None:
        # 상태 코드는 라우트 인증 몫(다른 테스트가 인증 의존성을 덮어쓰면 422 도 나온다) —
        # 여기서는 미들웨어가 조회 전용으로 막지 않았는지만 본다.
        r = self.client.post("/api/v1/outbound/orders", json={})
        detail = r.json().get("detail")
        self.assertFalse(isinstance(detail, dict) and detail.get("code") == "ACCOUNT_READ_ONLY")


class FrontendWiringTests(unittest.TestCase):
    def test_caps_force_no_write(self) -> None:
        src = (FE / "lib" / "screen-caps.ts").read_text(encoding="utf-8")
        self.assertIn("readOnly?: boolean;", src)
        self.assertIn(
            "return resolver.readOnly && !resolver.isSuperUser ? { ...caps, canWrite: false } : caps;", src
        )
        perms = (FE / "lib" / "use-permissions.ts").read_text(encoding="utf-8")
        self.assertIn("readOnly: u?.account_read_only === true,", perms)

    def test_header_badge(self) -> None:
        src = (FE / "components" / "app-shell" / "header.tsx").read_text(encoding="utf-8")
        self.assertIn("user?.account_read_only", src)
        self.assertIn("조회 전용", src)


if __name__ == "__main__":
    unittest.main()
