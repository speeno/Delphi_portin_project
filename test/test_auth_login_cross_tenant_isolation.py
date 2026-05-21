"""DSN-DEC-12 — 공유 DB 환경에서 타사 데이터 노출 차단 회귀 가드.

배경
----
WeLove 통합 운영에서 ``chul_09_db`` 는 위러브1·2·3·교문사 4 테넌트가 공유한다.
``server_id`` 만으로 narrow 안 되는 조합(예: 서버3 = 위러브3 + 교문사) 에서
이전에는 ``lookup_by_account_family`` / ``lookup_by_hcode_hint`` 가 “첫 매치” 를
반환해 사용자에게 다른 회사 컨텍스트가 부여될 수 있었다.

본 테스트는 다음 정책을 회귀 가드한다.

1. 공유 DB 좌표(server_id, db_name) 가 단일화 불가능하면
   ``ownership_status="ambiguous"`` 가 audit 로그에 기록된다.
2. ambiguous 시 ``tenant_id``/``account_family``/``active_build_id`` 가 ``None``/빈
   값으로 떨어져 다운스트림이 fail-closed 로 동작한다.
3. ``hcode_in`` / ``hcode_pattern`` / ``hcode_prefix`` 격리 키가 시드에 추가되면
   같은 좌표여도 unique 결정이 가능해진다.
4. 단일 테넌트 DB(공유 아님) 에서는 ownership_status="unique" 가 되어
   ``ownership_violation`` 이 false 인지 확인.
5. (서버 좌표) 만으로 narrow 되는 케이스(book_07_db: 서버1=북앤북 / 서버4=유앤북) 는
   server_id 기반 격리가 그대로 동작.

본 가드의 분류 코드는 [docs/welove-cross-tenant-exposure-runbook.md] §2 와 1:1.
"""

from __future__ import annotations

import importlib
import json
import logging
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import tenants_directory_service  # noqa: E402


# ────────────────────────────────────────────────────────────────────
# 1) Pure-unit — resolve_unique_tenant 공유 DB / hcode 격리 검증
# ────────────────────────────────────────────────────────────────────

_SHARED_DB_TENANTS = [
    {
        "tenant_id": "tid-위러브3",
        "tenant_label_kor": "서버3(위러브3)",
        "account_family": "chul_09",
        "primary_server": "서버3",
        "db_name_logical": "chul_09_db",
        "active_build_id": "BLD-CHUL-09-W3",
        "build_role": "distributor",
        "default_account_type": "T2_DIST",
        "is_active": True,
    },
    {
        "tenant_id": "tid-교문사",
        "tenant_label_kor": "교문사",
        "account_family": "chul_09",
        "primary_server": "서버3",
        "db_name_logical": "chul_09_db",
        "active_build_id": "BLD-CHUL-09-KYM",
        "build_role": "distributor",
        "default_account_type": "T2_DIST",
        "is_active": True,
    },
]

_BOOKB_TENANTS = [
    {
        "tenant_id": "tid-book07-bookbook",
        "tenant_label_kor": "북앤북",
        "account_family": "book_07_b",
        "primary_server": "서버1",
        "db_name_logical": "book_07_db",
        "default_account_type": "T3",
        "is_active": True,
    },
    {
        "tenant_id": "tid-book07-uandbook",
        "tenant_label_kor": "유앤북",
        "account_family": "book_07_u",
        "primary_server": "서버4",
        "db_name_logical": "book_07_db",
        "default_account_type": "T3",
        "is_active": True,
    },
]


class ResolveUniqueTenantTests(TestCase):
    """``tenants_directory_service.resolve_unique_tenant`` 동작 단위 테스트."""

    def _patched_loader(self, tenants):
        return patch.object(
            tenants_directory_service, "_load_tenants", lambda: tenants
        )

    def test_chul09_server3_no_isolation_returns_ambiguous(self):
        """서버3 + chul_09_db 좌표 + 격리 키 부재 → ambiguous."""
        with self._patched_loader(_SHARED_DB_TENANTS):
            status, owner, candidates = tenants_directory_service.resolve_unique_tenant(
                "remote_153", "chul_09_db", hcode="9001"
            )
            self.assertEqual(status, "ambiguous")
            self.assertIsNone(owner)
            self.assertEqual(len(candidates), 2)
            self.assertSetEqual(
                {c["tenant_id"] for c in candidates},
                {"tid-위러브3", "tid-교문사"},
            )

    def test_chul09_with_tenant_id_hint_unique(self):
        """tenant_id 힌트가 있으면 ambiguous 가 unique 로 단일화."""
        with self._patched_loader(_SHARED_DB_TENANTS):
            status, owner, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_153",
                "chul_09_db",
                tenant_id_hint="tid-위러브3",
            )
            self.assertEqual(status, "unique")
            self.assertEqual(owner["tenant_id"], "tid-위러브3")

    def test_chul09_with_hcode_pattern_isolation_unique(self):
        """시드에 hcode_pattern 이 있으면 같은 (server, db) 도 unique."""
        tenants = [
            dict(_SHARED_DB_TENANTS[0], hcode_pattern=r"^9\d+$"),
            dict(_SHARED_DB_TENANTS[1], hcode_pattern=r"^[A-Za-z].*$"),
        ]
        with self._patched_loader(tenants):
            status, owner, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_153", "chul_09_db", hcode="9001"
            )
            self.assertEqual(status, "unique")
            self.assertEqual(owner["tenant_id"], "tid-위러브3")

    def test_chul09_with_hcode_in_list_isolation_unique(self):
        """``hcode_in`` 리스트(가장 강한 격리 키) 매치 검증."""
        tenants = [
            dict(_SHARED_DB_TENANTS[0], hcode_in=["9001", "9002"]),
            dict(_SHARED_DB_TENANTS[1], hcode_in=["KMS01", "KMS02"]),
        ]
        with self._patched_loader(tenants):
            status, owner, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_153", "chul_09_db", hcode="KMS01"
            )
            self.assertEqual(status, "unique")
            self.assertEqual(owner["tenant_id"], "tid-교문사")

    def test_chul09_with_hcode_prefix_isolation_unique(self):
        """``hcode_prefix`` startswith 격리."""
        tenants = [
            dict(_SHARED_DB_TENANTS[0], hcode_prefix="W3-"),
            dict(_SHARED_DB_TENANTS[1], hcode_prefix="KYM-"),
        ]
        with self._patched_loader(tenants):
            status, owner, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_153", "chul_09_db", hcode="W3-001"
            )
            self.assertEqual(status, "unique")
            self.assertEqual(owner["tenant_id"], "tid-위러브3")

    def test_book07_server_id_already_narrows_to_unique(self):
        """book_07_db 는 서버1/서버4 분리 → server_id 만으로 unique."""
        with self._patched_loader(_BOOKB_TENANTS):
            status1, owner1, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_154", "book_07_db"
            )
            status4, owner4, _ = tenants_directory_service.resolve_unique_tenant(
                "remote_138", "book_07_db"
            )
            self.assertEqual(status1, "unique")
            self.assertEqual(owner1["tenant_id"], "tid-book07-bookbook")
            self.assertEqual(status4, "unique")
            self.assertEqual(owner4["tenant_id"], "tid-book07-uandbook")

    def test_no_candidates_returns_none(self):
        """좌표 매칭 0건 → 'none' (인덱스 miss / 시드 누락 케이스)."""
        with self._patched_loader(_SHARED_DB_TENANTS):
            status, owner, candidates = tenants_directory_service.resolve_unique_tenant(
                "remote_999", "nonexistent_db"
            )
            self.assertEqual(status, "none")
            self.assertIsNone(owner)
            self.assertEqual(candidates, [])

    def test_is_shared_db_detects_multi_tenant_coordinate(self):
        with self._patched_loader(_SHARED_DB_TENANTS):
            self.assertTrue(tenants_directory_service.is_shared_db("remote_153", "chul_09_db"))
        with self._patched_loader(_BOOKB_TENANTS):
            self.assertFalse(tenants_directory_service.is_shared_db("remote_154", "book_07_db"))


# ────────────────────────────────────────────────────────────────────
# 2) End-to-end — POST /auth/login 응답 + audit 로그
# ────────────────────────────────────────────────────────────────────


def _route(remote_id: str, db_name: str, *, candidate_via: str = "index_single") -> dict:
    return {
        "remote_id": remote_id,
        "db_name": db_name,
        "tenant_id": "",
        "account_family": db_name.removesuffix("_db"),
        "primary_server_label": "",
        "build_role": "",
        "default_account_type": "",
        "tenant_label_kor": "",
        "via": "index",
        "index_status": "single",
        "candidate_via": candidate_via,
        "confidence": "high",
        "priority": 0,
    }


def _user(
    user_id: str,
    *,
    server_id: str,
    db_name: str,
    hcode: str = "9001",
    ownership_status: str = "none",
    ownership_candidate_count: int = 0,
    tenant_id: str | None = None,
    account_family: str | None = None,
    active_build_id: str | None = None,
) -> dict:
    return {
        "user_id": user_id,
        "user_name": "테스트",
        "display_name": "테스트",
        "server_id": server_id,
        "server_label": server_id,
        "hcode": hcode,
        "auth_flags": f"{hcode}:테스트",
        "role": "",
        "permissions": [],
        "resolved_db": db_name,
        "tenant_id": tenant_id,
        "account_family": account_family,
        "active_build_id": active_build_id,
        "ownership_status": ownership_status,
        "ownership_candidate_count": ownership_candidate_count,
    }


class _CapturingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def parsed(self) -> list[dict]:
        out: list[dict] = []
        for r in self.records:
            msg = r.getMessage()
            i = msg.find("{")
            if i < 0:
                continue
            try:
                out.append(json.loads(msg[i:]))
            except Exception:
                continue
        return out


class CrossTenantAuditTests(TestCase):
    """라우터 e2e — ownership_violation 신호가 audit 로그까지 도달하는지 확인."""

    def setUp(self) -> None:
        # FastAPI 앱은 import 시점에 환경변수를 굳히므로 매 테스트마다 새로 import.
        import os

        os.environ["BLS_AUTH_SERVER_ID"] = "remote_138"
        from fastapi.testclient import TestClient
        from app.main import app

        self.client = TestClient(app)
        self.handler = _CapturingHandler()
        self.audit_logger = logging.getLogger("audit.auth")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_shared_db_ambiguous_audit_marks_violation(
        self, mock_auth: AsyncMock, mock_cands, mock_single
    ) -> None:
        """ownership_status='ambiguous' 가 audit 로그에 ownership_violation=true 로 기록."""
        route = _route("remote_153", "chul_09_db")
        mock_single.return_value = route
        mock_cands.return_value = [route]
        mock_auth.return_value = _user(
            "shared-user",
            server_id="remote_153",
            db_name="chul_09_db",
            ownership_status="ambiguous",
            ownership_candidate_count=2,
            tenant_id=None,  # fail-closed
            account_family=None,
            active_build_id=None,
        )

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "shared-user", "password": "pw"},
        )
        self.assertEqual(res.status_code, 200, res.text)

        recs = self.handler.parsed()
        self.assertTrue(recs, "audit log captured nothing")
        latest = recs[-1]
        self.assertTrue(latest.get("ownership_violation"), latest)
        self.assertEqual(latest.get("ownership_status"), "ambiguous")
        self.assertEqual(latest.get("ownership_candidate_count"), 2)

        # 응답 본문도 fail-closed: tenant_id/account_family/active_build_id 비어있어야.
        body = res.json()
        user = body["user"]
        self.assertIn(user.get("tenant_id"), (None, ""))
        self.assertIn(user.get("account_family"), (None, ""))
        self.assertIn(user.get("active_build_id"), (None, ""))
        # DSN-DEC-12 — 프론트가 보조 입력 UI 강제 노출에 사용할 신호.
        self.assertEqual(user.get("ownership_status"), "ambiguous")
        self.assertEqual(user.get("ownership_candidate_count"), 2)

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_unique_owner_does_not_set_violation(
        self, mock_auth: AsyncMock, mock_cands, mock_single
    ) -> None:
        """ownership_status='unique' → ownership_violation=False (정상)."""
        route = _route("remote_154", "book_07_db")
        mock_single.return_value = route
        mock_cands.return_value = [route]
        mock_auth.return_value = _user(
            "unique-user",
            server_id="remote_154",
            db_name="book_07_db",
            ownership_status="unique",
            ownership_candidate_count=1,
            tenant_id="tid-book07-bookbook",
            account_family="book_07_b",
            active_build_id="BLD-X",
        )

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "unique-user", "password": "pw"},
        )
        self.assertEqual(res.status_code, 200, res.text)

        latest = self.handler.parsed()[-1]
        self.assertFalse(latest.get("ownership_violation"), latest)
        self.assertEqual(latest.get("ownership_status"), "unique")

        body = res.json()
        user = body["user"]
        self.assertEqual(user.get("tenant_id"), "tid-book07-bookbook")
        self.assertEqual(user.get("account_family"), "book_07_b")
        self.assertEqual(user.get("active_build_id"), "BLD-X")
        self.assertEqual(user.get("ownership_status"), "unique")

    @patch("app.services.login_id_index_service.add_entry", lambda **_kw: None)
    @patch("app.services.tenants_directory_service.resolve_login_route")
    @patch("app.services.tenants_directory_service.resolve_login_route_candidates")
    @patch("app.routers.auth.authenticate_user", new_callable=AsyncMock)
    def test_invalid_credentials_audit_includes_ownership_zero(
        self, mock_auth: AsyncMock, mock_cands, mock_single
    ) -> None:
        """비밀번호 실패 → 401 + audit ownership_status='none' (가드 미적용)."""
        route = _route("remote_153", "chul_09_db")
        mock_single.return_value = route
        mock_cands.return_value = [route]
        mock_auth.return_value = None

        res = self.client.post(
            "/api/v1/auth/login",
            json={"userId": "bad", "password": "wrong"},
        )
        self.assertEqual(res.status_code, 401, res.text)

        latest = self.handler.parsed()[-1]
        self.assertEqual(latest.get("result"), "failure")
        self.assertEqual(latest.get("ownership_status"), "none")
        self.assertFalse(latest.get("ownership_violation"))


if __name__ == "__main__":
    main()
