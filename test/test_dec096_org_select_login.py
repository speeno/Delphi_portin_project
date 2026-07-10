"""DEC-096 — 로그인 조직(테넌트) 선택 챌린지 회귀 가드.

배경: 동일 아이디+비밀번호가 복수 테넌트 DB 에 등재된 계정 672건(실측) —
first-match 오라우팅 대신, 인덱스 유래 후보(index_single/index_ambiguous)가
복수 검증되면 409 ORG_SELECT_REQUIRED + 선택지(비밀번호 검증 성공 후보만)를
반환하고, tenantId/dbName 재제출로 단일화한다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

_CANDS = [
    {"remote_id": "remote_138", "db_name": "book_11_db", "tenant_id": "tid-11",
     "account_family": "book_11", "candidate_via": "index_ambiguous"},
    {"remote_id": "remote_138", "db_name": "book_kb_db", "tenant_id": "tid-kb",
     "account_family": "book_kb", "candidate_via": "index_ambiguous"},
    # 스윕 후보 — 챌린지 우주에서 제외되어야 한다.
    {"remote_id": "remote_155", "db_name": "chul_01_db", "tenant_id": "",
     "account_family": "chul_01", "candidate_via": "directory_sweep"},
]


def _user_for(db: str) -> dict:
    return {
        "user_id": "어깨동무", "user_name": "어깨동무",
        "server_id": "remote_138", "hcode": "x1060",
        "role": "operator", "permissions": [],
        "resolved_db": db,
    }


async def _fake_auth_all_match(server_id, user_id, password, db_name=None, **kw):  # noqa: ARG001
    """모든 후보 DB 에서 비밀번호 검증 성공(동일 ID+PW 복제 계정 시나리오).

    async 함수 patch 는 AsyncMock 이 되므로 side_effect 도 async 로 제공해야
    반환 dict 가 그대로 결과가 된다(코루틴 이중 포장 방지).
    """
    return _user_for(db_name or "")


async def _fake_auth_only_kb(server_id, user_id, password, db_name=None, **kw):  # noqa: ARG001
    return _user_for(db_name) if db_name == "book_kb_db" else None


class OrgSelectChallengeTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def _post(self, body: dict):
        return self.client.post("/api/v1/auth/login", json=body)

    def test_multi_verified_returns_409_choices(self) -> None:
        with patch("app.routers.auth.authenticate_user", side_effect=_fake_auth_all_match), \
             patch("app.services.tenants_directory_service.resolve_login_route_candidates",
                   return_value=list(_CANDS)):
            r = self._post({"userId": "어깨동무", "password": "pw"})
        self.assertEqual(r.status_code, 409, r.text)
        detail = r.json()["detail"]
        self.assertEqual(detail["code"], "ORG_SELECT_REQUIRED")
        choices = detail["choices"]
        # 인덱스 후보 2개만 — directory_sweep 후보는 선택지에서 제외.
        self.assertEqual(len(choices), 2)
        dbs = {c["dbName"] for c in choices}
        self.assertEqual(dbs, {"book_11_db", "book_kb_db"})
        self.assertTrue(all(c.get("label") for c in choices), "표시 라벨 필수")
        # 토큰 미발급.
        self.assertNotIn("access_token", r.json())

    def test_retry_with_tenant_id_narrows_to_single(self) -> None:
        with patch("app.routers.auth.authenticate_user", side_effect=_fake_auth_all_match), \
             patch("app.services.tenants_directory_service.resolve_login_route_candidates",
                   return_value=list(_CANDS)):
            r = self._post({"userId": "어깨동무", "password": "pw", "tenantId": "tid-kb"})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("access_token", r.json())

    def test_retry_with_db_name_narrows_to_single(self) -> None:
        with patch("app.routers.auth.authenticate_user", side_effect=_fake_auth_all_match), \
             patch("app.services.tenants_directory_service.resolve_login_route_candidates",
                   return_value=list(_CANDS)):
            r = self._post({"userId": "어깨동무", "password": "pw", "dbName": "book_11_db"})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("access_token", r.json())

    def test_single_verified_passes_through(self) -> None:
        """비밀번호가 한 DB 에서만 맞으면(정상 다중 등재) 챌린지 없이 로그인."""
        with patch("app.routers.auth.authenticate_user", side_effect=_fake_auth_only_kb), \
             patch("app.services.tenants_directory_service.resolve_login_route_candidates",
                   return_value=list(_CANDS)):
            r = self._post({"userId": "어깨동무", "password": "pw"})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("access_token", r.json())

    def test_single_index_candidate_no_challenge(self) -> None:
        with patch("app.routers.auth.authenticate_user", side_effect=_fake_auth_all_match), \
             patch("app.services.tenants_directory_service.resolve_login_route_candidates",
                   return_value=[_CANDS[0], _CANDS[2]]):  # 인덱스 1 + 스윕 1
            r = self._post({"userId": "어깨동무", "password": "pw"})
        self.assertEqual(r.status_code, 200, r.text)


if __name__ == "__main__":
    main()
