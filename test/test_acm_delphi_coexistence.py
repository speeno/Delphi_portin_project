"""ACM-INV-1/3/4/7 — 레거시 델파이 병행 불변식 정적·동적 가드.

- 계정 전환·이메일 로그인 경로 모듈에 ``Id_Logn`` 쓰기 SQL 이 0건인지(정적).
- ``load_user_by_identity`` 가 정확한 Gcode 로만 찾고(만료 관례 ``_이름_`` 는 다른 행), 행이 없으면 None.
- ``authenticate_email_account`` 는 Id_Logn 을 쓰지 않는다(execute_query 호출 SQL 감시).
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT / "test"))

_ACCOUNT_PATH_MODULES = [
    "app/services/account_switch_service.py",
    "app/services/web_accounts_db.py",
    "app/services/auth_login_core.py",
    "app/services/account_secret_codec.py",
    "app/services/email_dispatch_service.py",
    "app/routers/public_account_switch.py",
]
_WRITE_RE = re.compile(r"(INSERT\s+INTO|UPDATE|DELETE\s+FROM|REPLACE\s+INTO|ALTER\s+TABLE|DROP\s+TABLE)\s+[`\"']?(\w+\.)?[`\"']?Id_Logn", re.IGNORECASE)


class StaticNoIdLognWriteTests(unittest.TestCase):
    def test_no_id_logn_write_in_account_paths(self):
        for rel in _ACCOUNT_PATH_MODULES:
            src = (BACKEND / rel).read_text(encoding="utf-8")
            self.assertIsNone(_WRITE_RE.search(src), f"{rel}: Id_Logn 쓰기 SQL 금지 (ACM-INV-1)")

    def test_identity_loader_region_has_no_write(self):
        src = (BACKEND / "app/services/auth_service.py").read_text(encoding="utf-8")
        start = src.index("async def load_user_by_identity(")
        region = src[start:]
        self.assertIsNone(_WRITE_RE.search(region))
        self.assertNotIn("set_password", region)


class IdentityLoaderTests(unittest.IsolatedAsyncioTestCase):
    async def test_exact_gcode_only_and_expired_lock_convention_blocks_web(self):
        from app.services import auth_service

        rows_by_gcode = {
            "_hong_": [{"user_id": "_hong_", "password": "x", "user_name": "한빛", "display_name": "홍", "hcode": "x1060", "auth_flags": "x1060:홍"}],
        }

        async def fake_query(server_id, sql, params):  # noqa: ARG001
            return list(rows_by_gcode.get(params[0], []))

        with patch("app.services.auth_service.get_server_profile", return_value={"id": "remote_138", "label": "138", "database": "book_kb_db"}), \
             patch("app.services.auth_service.execute_query", side_effect=fake_query):
            # 링크는 'hong' 을 가리키지만 델파이가 '_hong_' 로 잠갔다 → 정확 일치 실패 → None (fail-closed)
            self.assertIsNone(await auth_service.load_user_by_identity("remote_138", "hong", db_name="book_kb_db", hcode="x1060"))

    async def test_hcode_mismatch_row_is_ignored(self):
        from app.services import auth_service

        async def fake_query(server_id, sql, params):  # noqa: ARG001
            return [{"user_id": "hong", "password": "x", "user_name": "다른회사", "display_name": "홍", "hcode": "z9999", "auth_flags": "z9999:홍"}]

        with patch("app.services.auth_service.get_server_profile", return_value={"id": "remote_138", "label": "138", "database": "book_kb_db"}), \
             patch("app.services.auth_service.execute_query", side_effect=fake_query):
            self.assertIsNone(await auth_service.load_user_by_identity("remote_138", "hong", db_name="book_kb_db", hcode="x1060"))

    async def test_matching_row_builds_user_without_password_check(self):
        from app.services import auth_service

        async def fake_query(server_id, sql, params):  # noqa: ARG001
            self.assertIn("book_kb_db", sql)  # DSN-DEC-08 cross-DB 한정
            return [{"user_id": "hong", "password": "secret", "user_name": "한빛", "display_name": "홍", "hcode": "x1060", "auth_flags": "x1060:홍"}]

        with patch("app.services.auth_service.get_server_profile", return_value={"id": "remote_138", "label": "138", "database": "book_kb_db"}), \
             patch("app.services.auth_service.execute_query", side_effect=fake_query), \
             patch("app.services.auth_service._fetch_user_fxx_matrix", AsyncMock(return_value={"F11": "O"})), \
             patch("app.services.auth_service._resolve_role_and_permissions_async", AsyncMock(return_value=("operator", ["outbound.read"]))), \
             patch("app.services.auth_service._resolve_account_type", return_value={"account_type": "T3", "tenant_id": "tid-kb"}):
            u = await auth_service.load_user_by_identity("remote_138", "hong", db_name="book_kb_db", hcode="x1060")
        self.assertIsNotNone(u)
        self.assertEqual(u["user_id"], "hong"); self.assertEqual(u["hcode"], "x1060"); self.assertEqual(u["resolved_db"], "book_kb_db")
        self.assertTrue(u["fxx_caps"]["F11"]["write"])
        self.assertNotIn("password", u)


class DynamicNoWriteTests(unittest.IsolatedAsyncioTestCase):
    async def test_email_login_path_issues_no_write_sql(self):
        from _acm_fake_store import FakeStore, patch_store
        from app.services import account_secret_codec as codec
        from app.services import account_switch_service as acs

        store = FakeStore()
        seen: list[str] = []

        async def spy_query(server_id, sql, params=None):  # noqa: ARG001
            seen.append(sql)
            return [{"user_id": "hong", "password": "x", "user_name": "한빛", "display_name": "홍", "hcode": "x1060", "auth_flags": "x1060:홍"}]

        with patch_store(store):
            a = await store.create_account(email="h@x.co", pw_hash=codec.hash_password("abc12345"), pw_secret="abc12345")
            await store.add_link(account_id=a["AccountId"], server_id="remote_138", db_name="book_kb_db", hcode="x1060", gcode="hong")
            with patch("app.services.auth_service.get_server_profile", return_value={"id": "remote_138", "label": "138", "database": "book_kb_db"}), \
                 patch("app.services.auth_service.execute_query", side_effect=spy_query), \
                 patch("app.services.auth_service._fetch_user_fxx_matrix", AsyncMock(return_value={})), \
                 patch("app.services.auth_service._resolve_role_and_permissions_async", AsyncMock(return_value=("operator", []))), \
                 patch("app.services.auth_service._resolve_account_type", return_value={"account_type": "T3"}):
                res = await acs.authenticate_email_account(email="h@x.co", password="abc12345")
        self.assertTrue(res.ok, res.reason)
        self.assertTrue(seen)
        for sql in seen:
            self.assertIsNone(_WRITE_RE.search(sql), sql)
            self.assertTrue(sql.lstrip().upper().startswith("SELECT"), sql)


if __name__ == "__main__":
    unittest.main()
