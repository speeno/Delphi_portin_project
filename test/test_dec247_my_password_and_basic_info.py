"""내정보 — 기본 정보 수정 · 웹 비밀번호 변경 회귀 가드 (DEC-247).

핵심 불변식
- ACM-INV-1: 비밀번호 변경 경로가 `Id_Logn` 을 읽지도 쓰지도 않는다(델파이 병행 운영).
- 현재 비밀번호 확인 필수(세션 탈취 시 비밀번호 교체 차단).
- 이메일 계정 세션이 아니면 400 `ACCT_NOT_EMAIL_LOGIN` 으로 거절(레거시 ID 세션엔 웹 비번이 없다).
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.services import account_secret_codec as codec  # noqa: E402
from app.services import account_switch_service as acs  # noqa: E402


class ChangePasswordServiceTests(unittest.IsolatedAsyncioTestCase):
    def _account(self, pw: str = "oldpass1") -> dict:
        return {"AccountId": "acc1", "Email": "a@buk.io", "PwHash": codec.hash_password(pw), "Status": "active", "LockedUntil": ""}

    async def test_wrong_current_password_rejected(self) -> None:
        with patch.object(acs.store, "get_account_by_id", return_value=self._account()):
            with self.assertRaises(acs.SwitchError) as cm:
                await acs.change_password(account_id="acc1", current_password="nope", new_password="newpass1")
        self.assertEqual(cm.exception.code, "ACCT_CURRENT_PW_INVALID")

    async def test_policy_and_unchanged_rejected(self) -> None:
        with patch.object(acs.store, "get_account_by_id", return_value=self._account()):
            with self.assertRaises(acs.SwitchError):
                await acs.change_password(account_id="acc1", current_password="oldpass1", new_password="short")
            with self.assertRaises(acs.SwitchError) as cm:
                await acs.change_password(account_id="acc1", current_password="oldpass1", new_password="oldpass1")
        self.assertEqual(cm.exception.code, "ACCT_PW_UNCHANGED")

    async def test_success_updates_only_web_account(self) -> None:
        seen: list[tuple] = []

        async def fake_update(**kw):
            seen.append(("update", kw))

        with patch.object(acs.store, "get_account_by_id", return_value=self._account()), \
                patch.object(acs.store, "update_password", side_effect=fake_update):
            res = await acs.change_password(account_id="acc1", current_password="oldpass1", new_password="newpass1")
        self.assertIn("비밀번호를 변경했습니다", res["message"])
        self.assertEqual(len(seen), 1)
        kw = seen[0][1]
        self.assertEqual(kw["account_id"], "acc1")
        self.assertTrue(codec.verify_password("newpass1", kw["pw_hash"]))


class StaticGuards(unittest.TestCase):
    def test_no_id_logn_touch_in_change_password(self) -> None:
        src = (BACKEND / "app" / "services" / "account_switch_service.py").read_text(encoding="utf-8")
        i = src.index("async def change_password(")
        block = src[i : src.index("\nasync def ", i + 10)]
        # docstring 은 불변식을 **설명**하므로 제외하고, 실행 코드에 Id_Logn SQL 이 없는지 본다.
        body = re.sub(r'"""..*?"""', "", block, count=1, flags=re.S)
        self.assertIsNone(
            re.search(r"(SELECT|INSERT|UPDATE|DELETE|REPLACE)[^\n]*Id_Logn", body, re.I),
            "ACM-INV-1 — 웹 비밀번호 변경은 Id_Logn 을 읽지도 쓰지도 않는다",
        )
        self.assertIn("verify_password", body, "현재 비밀번호 확인 필수")

    def test_route_requires_email_account(self) -> None:
        src = (BACKEND / "app" / "routers" / "me.py").read_text(encoding="utf-8")
        self.assertIn('@router.post("/password")', src)
        self.assertIn("ACCT_NOT_EMAIL_LOGIN", src)
        self.assertIn("log_account_event", src, "비밀번호 변경은 감사 로그를 남긴다")

    def test_profile_page_has_basic_info_and_password_form(self) -> None:
        page = (FRONT / "app" / "(app)" / "settings" / "my-profile" / "page.tsx").read_text(encoding="utf-8")
        for lid in ("MyProfile.DisplayName", "MyProfile.ContactPhone", "MyProfile.CurrentPassword",
                    "MyProfile.NewPassword", "MyProfile.NewPasswordConfirm"):
            self.assertIn(lid, page, lid)
        self.assertIn("<PasswordRules", page, "비밀번호 조건 실시간 표시 재사용")
        self.assertIn("changeMyPassword", page)
        # 델파이 병행 안내 — 웹 비번 변경이 델파이에 영향 없음을 화면에서 알린다.
        self.assertIn("델파이 프로그램의 비밀번호는", page)


if __name__ == "__main__":
    unittest.main()
