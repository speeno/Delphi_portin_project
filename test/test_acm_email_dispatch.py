"""ACM-DEC-09 — 메일 발송 서비스(email_dispatch_service) 회귀 가드.

- provider 선택(console/smtp/unknown), smtp 설정 누락 시 예외 없이 결과 반환
- smtp 경로가 aiosmtplib.send 를 STARTTLS·자격으로 호출하고 메시지 헤더가 올바른지
- 로그·결과에 비밀번호 원문이 없고 수신 주소는 마스킹되는지 (secrets-policy G3)
- 기동 경고(startup_warnings)
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import email_dispatch_service as svc  # noqa: E402

_SMTP_ENV = {
    "BLS_EMAIL_PROVIDER": "smtp",
    "BLS_SMTP_HOST": "smtp-relay.example.test",
    "BLS_SMTP_PORT": "587",
    "BLS_SMTP_USER": "login@smtp.example.test",
    "BLS_SMTP_PASSWORD": "TEST-SECRET-KEY-DO-NOT-LOG",
    "BLS_EMAIL_FROM": "no-reply@example.test",
    "BLS_EMAIL_FROM_NAME": "북이오웍스",
    "BLS_EMAIL_REPLY_TO": "",
    "BLS_EMAIL_DEBUG_ECHO": "0",
}
_CLEAR = {k: "" for k in _SMTP_ENV}


class MaskAndValidateTests(unittest.TestCase):
    def test_mask_email(self):
        self.assertEqual(svc.mask_email("hong@company.co.kr"), "h***@company.co.kr")
        self.assertEqual(svc.mask_email("not-an-email"), "***")
        self.assertEqual(svc.mask_email(""), "***")

    def test_is_valid_email(self):
        self.assertTrue(svc.is_valid_email("a@b.co"))
        self.assertFalse(svc.is_valid_email("a@b"))
        self.assertFalse(svc.is_valid_email("a b@c.com"))
        self.assertFalse(svc.is_valid_email("x" * 130 + "@c.com"))


class ConsoleProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_console_ok_and_masks_recipient_in_log(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "console"}):
            with self.assertLogs("app.services.email_dispatch_service", level="INFO") as cm:
                r = await svc.send_email(to="hong@company.co.kr", subject="테스트", html="<p>hi</p>")
        self.assertTrue(r.ok)
        self.assertEqual(r.provider, "console")
        self.assertEqual(r.to_masked, "h***@company.co.kr")
        joined = "\n".join(cm.output)
        self.assertIn("h***@company.co.kr", joined)
        self.assertNotIn("hong@company.co.kr", joined)

    async def test_invalid_recipient_and_empty_subject(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "console"}):
            r1 = await svc.send_email(to="bad", subject="x", html="")
            r2 = await svc.send_email(to="a@b.co", subject="  ", html="")
        self.assertFalse(r1.ok); self.assertEqual(r1.error, "invalid_recipient")
        self.assertFalse(r2.ok); self.assertEqual(r2.error, "empty_subject")


class SmtpProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_missing_config_returns_result_without_raising(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "smtp", "BLS_SMTP_HOST": "h"}):
            r = await svc.send_email(to="a@b.co", subject="s", html="<b>x</b>")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "smtp_not_configured")

    async def test_unknown_provider(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "carrier-pigeon"}):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "unknown_provider")

    async def test_smtp_calls_aiosmtplib_send_with_starttls_and_credentials(self):
        import aiosmtplib

        sent = AsyncMock(return_value=({}, "OK"))
        with patch.dict(os.environ, _SMTP_ENV), patch.object(aiosmtplib, "send", sent):
            with self.assertLogs("app.services.email_dispatch_service", level="INFO") as cm:
                r = await svc.send_email(
                    to="hong@company.co.kr", subject="[북이오웍스] 인증코드", html="<p>123456</p>", text="123456"
                )
        self.assertTrue(r.ok, r)
        self.assertEqual(r.provider, "smtp")
        self.assertTrue(r.message_id)
        sent.assert_awaited_once()
        msg = sent.await_args.args[0]
        kw = sent.await_args.kwargs
        self.assertEqual(kw["hostname"], "smtp-relay.example.test")
        self.assertEqual(kw["port"], 587)
        self.assertEqual(kw["username"], "login@smtp.example.test")
        self.assertEqual(kw["password"], "TEST-SECRET-KEY-DO-NOT-LOG")
        self.assertTrue(kw["start_tls"])
        import ssl
        self.assertIsInstance(kw["tls_context"], ssl.SSLContext)
        self.assertEqual(msg["To"], "hong@company.co.kr")
        self.assertIn("no-reply@example.test", msg["From"])
        self.assertEqual(msg["Subject"], "[북이오웍스] 인증코드")
        # multipart/alternative: text + html
        parts = [p.get_content_type() for p in msg.iter_parts()]
        self.assertEqual(parts, ["text/plain", "text/html"])
        joined = "\n".join(cm.output)
        self.assertNotIn("TEST-SECRET-KEY-DO-NOT-LOG", joined)
        self.assertNotIn("hong@company.co.kr", joined)

    async def test_smtp_failure_is_returned_not_raised_and_secret_not_logged(self):
        import aiosmtplib

        boom = AsyncMock(side_effect=aiosmtplib.SMTPException("relay refused"))
        with patch.dict(os.environ, _SMTP_ENV), patch.object(aiosmtplib, "send", boom):
            with self.assertLogs("app.services.email_dispatch_service", level="WARNING") as cm:
                r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "SMTPException")
        self.assertNotIn("TEST-SECRET-KEY-DO-NOT-LOG", "\n".join(cm.output))


class StartupWarningTests(unittest.TestCase):
    def test_warn_when_smtp_missing_fields(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "smtp"}):
            w = svc.startup_warnings()
        self.assertTrue(any("설정 누락" in x for x in w))

    def test_warn_console_on_render_and_debug_echo(self):
        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "console", "RENDER": "true"}):
            self.assertTrue(any("console" in x for x in svc.startup_warnings()))
        with patch.dict(os.environ, {**_SMTP_ENV, "BLS_EMAIL_DEBUG_ECHO": "1"}):
            self.assertTrue(any("DEBUG_ECHO" in x for x in svc.startup_warnings()))

    def test_no_warnings_when_smtp_configured(self):
        with patch.dict(os.environ, {**_SMTP_ENV, "RENDER": ""}):
            self.assertEqual(svc.startup_warnings(), [])


if __name__ == "__main__":
    unittest.main()
