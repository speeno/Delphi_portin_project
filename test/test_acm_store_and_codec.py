"""ACM-DEC-01/05 — 저장소 DDL(MySQL 3.23 호환·전용 DB 한정) + 비밀번호 코덱."""

from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import account_secret_codec as codec  # noqa: E402
from app.services import web_accounts_db as store  # noqa: E402


class DdlTests(unittest.TestCase):
    def test_ddl_is_mysql3_safe_and_qualified_to_dedicated_db(self):
        with patch.dict(os.environ, {"BLS_ACCOUNT_STORE_DB": "", "BLS_ACCOUNT_STORE_SERVER_ID": ""}):
            self.assertEqual(store.store_db(), "")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BLS_ACCOUNT_STORE_DB", None)
            stmts = store.ddl_statements()
        self.assertEqual(stmts[0], "CREATE DATABASE IF NOT EXISTS `bukio_web_db`")
        self.assertEqual(len(stmts), 4)
        joined = "\n".join(stmts)
        for banned in ("SELECT", "ON DUPLICATE", "JSON", "CASE WHEN", "AUTO_INCREMENT"):
            self.assertNotIn(banned, joined.upper())
        self.assertIn("`bukio_web_db`.`Web_Accounts`", joined)
        self.assertIn("PRIMARY KEY (ServerId, DbName, Hcode, Gcode)", joined)
        self.assertIn("UNIQUE ux_web_accounts_email (Email)", joined)

    def test_queries_are_qualified_and_parameterized(self):
        calls: list[tuple[str, tuple]] = []

        async def fake(server_id, sql, params=None):
            calls.append((sql, tuple(params or ())))
            return []

        store.clear_ensured_for_tests()
        with patch.dict(os.environ, {"BLS_ACCOUNT_STORE_DB": "bukio_web_db", "BLS_ACCOUNT_STORE_SERVER_ID": "remote_138"}), \
             patch("app.services.web_accounts_db.execute_query", side_effect=fake):
            import asyncio
            asyncio.run(store.get_account_by_email("A@B.co"))
            asyncio.run(store.find_link("remote_138", "db", "h", "g"))
        # ensure(4 DDL) + 2 SELECT
        selects = [c for c in calls if c[0].startswith("SELECT")]
        self.assertEqual(len(selects), 2)
        self.assertIn("`bukio_web_db`.`Web_Accounts`", selects[0][0]); self.assertEqual(selects[0][1], ("a@b.co",))
        for sql, _ in selects:
            self.assertNotRegex(sql, re.compile(r"'[^']*@"))  # 값 인라인 금지

    def test_lock_helpers(self):
        self.assertFalse(store.is_locked(None))
        self.assertTrue(store.is_locked({"Status": "disabled"}))
        self.assertTrue(store.is_locked({"Status": "active", "LockedUntil": store.ts_after(minutes=5)}))
        self.assertFalse(store.is_locked({"Status": "active", "LockedUntil": "2000-01-01 00:00:00"}))


class CodecTests(unittest.TestCase):
    def test_policy(self):
        self.assertEqual(codec.validate_password_policy("short1"), "ACCT_WEAK_PASSWORD")
        self.assertEqual(codec.validate_password_policy("onlyletters"), "ACCT_WEAK_PASSWORD")
        self.assertEqual(codec.validate_password_policy("12345678"), "ACCT_WEAK_PASSWORD")
        self.assertIsNone(codec.validate_password_policy("abc12345"))
        self.assertEqual(codec.validate_password_policy("a1" * 40), "ACCT_WEAK_PASSWORD")

    def test_hash_verify(self):
        h = codec.hash_password("abc12345")
        self.assertTrue(h.startswith("$2")); self.assertTrue(codec.verify_password("abc12345", h))
        self.assertFalse(codec.verify_password("abc12346", h)); self.assertFalse(codec.verify_password("", h))

    def test_plain_and_aesgcm_modes(self):
        with patch.dict(os.environ, {"BLS_ACCOUNT_PW_STORE": "plain"}):
            self.assertEqual(codec.encode_secret("abc12345"), "abc12345")
            self.assertEqual(codec.decode_secret("abc12345"), "abc12345")
        with patch.dict(os.environ, {"BLS_ACCOUNT_PW_STORE": "aesgcm", "BLS_ACCOUNT_PW_KEY": "test-key-not-secret"}):
            enc = codec.encode_secret("abc12345")
            self.assertTrue(enc.startswith("gcm:")); self.assertNotIn("abc12345", enc)
            self.assertEqual(codec.decode_secret(enc), "abc12345")
            self.assertTrue(codec.is_encrypted(enc))


if __name__ == "__main__":
    unittest.main()
