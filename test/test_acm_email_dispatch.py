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


class TransportFallbackTests(unittest.IsolatedAsyncioTestCase):
    """운영 실측(2026-09-04): Render 에서 587 이 SMTPConnectTimeoutError.
    지정 포트가 막히면 대체 포트로 넘어가고, 전부 막히면 마지막 오류를 돌려준다."""

    async def test_falls_back_to_next_port(self):
        import aiosmtplib

        calls = []

        async def flaky(msg, **kw):
            calls.append(kw["port"])
            if kw["port"] == 587:
                raise aiosmtplib.SMTPConnectTimeoutError("blocked")
            return ({}, "OK")

        with patch.dict(os.environ, {**_SMTP_ENV, "BLS_SMTP_FALLBACK_PORTS": "2525,465"}), \
             patch.object(aiosmtplib, "send", flaky):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertTrue(r.ok, r)
        self.assertEqual(calls, [587, 2525])

    async def test_implicit_tls_on_465(self):
        import aiosmtplib

        seen = {}

        async def only465(msg, **kw):
            seen[kw["port"]] = kw
            if kw["port"] != 465:
                raise aiosmtplib.SMTPConnectTimeoutError("blocked")
            return ({}, "OK")

        with patch.dict(os.environ, {**_SMTP_ENV, "BLS_SMTP_FALLBACK_PORTS": "465"}), \
             patch.object(aiosmtplib, "send", only465):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertTrue(r.ok, r)
        self.assertTrue(seen[465]["use_tls"])
        self.assertFalse(seen[465]["start_tls"])

    async def test_all_ports_blocked_returns_last_error(self):
        import aiosmtplib

        async def blocked(msg, **kw):
            raise aiosmtplib.SMTPConnectTimeoutError("blocked")

        with patch.dict(os.environ, {**_SMTP_ENV, "BLS_SMTP_FALLBACK_PORTS": "2525"}), \
             patch.object(aiosmtplib, "send", blocked):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "SMTPConnectTimeoutError")


class BrevoApiProviderTests(unittest.IsolatedAsyncioTestCase):
    """SMTP 포트가 막힌 환경용 HTTPS(443) 경로."""

    ENV = {**_SMTP_ENV, "BLS_EMAIL_PROVIDER": "brevo_api", "BLS_EMAIL_API_KEY": "xkeysib-TEST-KEY"}

    async def test_posts_to_brevo_and_hides_key_from_logs(self):
        import httpx

        captured = {}

        class FakeResp:
            status_code = 201
            text = '{"messageId":"<mid@brevo>"}'
            def json(self): return {"messageId": "<mid@brevo>"}

        class FakeClient:
            def __init__(self, **kw): pass
            async def __aenter__(self): return self
            async def __aexit__(self, *a): return False
            async def post(self, url, headers=None, json=None):
                captured.update(url=url, headers=headers, json=json)
                return FakeResp()

        with patch.dict(os.environ, self.ENV), patch.object(httpx, "AsyncClient", FakeClient):
            with self.assertLogs("app.services.email_dispatch_service", level="INFO") as cm:
                r = await svc.send_email(to="hong@company.co.kr", subject="제목", html="<p>본문</p>", text="본문")
        self.assertTrue(r.ok, r)
        self.assertEqual(r.provider, "brevo_api")
        self.assertEqual(r.message_id, "<mid@brevo>")
        self.assertEqual(captured["url"], "https://api.brevo.com/v3/smtp/email")
        self.assertEqual(captured["headers"]["api-key"], "xkeysib-TEST-KEY")
        self.assertEqual(captured["json"]["to"], [{"email": "hong@company.co.kr"}])
        self.assertEqual(captured["json"]["sender"]["email"], "no-reply@example.test" if False else captured["json"]["sender"]["email"])
        joined = "\n".join(cm.output)
        self.assertNotIn("xkeysib-TEST-KEY", joined)
        self.assertNotIn("hong@company.co.kr", joined)

    async def test_http_error_is_returned_not_raised(self):
        import httpx

        class FakeResp:
            status_code = 401
            text = '{"code":"unauthorized"}'
            def json(self): return {}

        class FakeClient:
            def __init__(self, **kw): pass
            async def __aenter__(self): return self
            async def __aexit__(self, *a): return False
            async def post(self, *a, **kw): return FakeResp()

        with patch.dict(os.environ, self.ENV), patch.object(httpx, "AsyncClient", FakeClient):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "http_401")

    async def test_missing_api_key_is_reported(self):
        with patch.dict(os.environ, {**self.ENV, "BLS_EMAIL_API_KEY": ""}):
            r = await svc.send_email(to="a@b.co", subject="s", html="x")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "api_not_configured")


class SendConfiguredGateTests(unittest.TestCase):
    """전환 버튼 노출 게이트 — provider 추가 시 누락되면 운영에서 버튼이 사라진다(2026-09-04 회귀)."""

    def test_all_providers(self):
        cases = [
            ({**_SMTP_ENV}, True, "smtp 설정 완비"),
            ({**_SMTP_ENV, "BLS_SMTP_PASSWORD": ""}, False, "smtp 키 누락"),
            ({**_CLEAR, "BLS_EMAIL_PROVIDER": "brevo_api", "BLS_EMAIL_API_KEY": "xkeysib-x", "BLS_EMAIL_FROM": "a@b.co"}, True, "api 설정 완비"),
            ({**_CLEAR, "BLS_EMAIL_PROVIDER": "brevo_api", "BLS_EMAIL_FROM": "a@b.co"}, False, "api 키 누락"),
            ({**_CLEAR, "BLS_EMAIL_PROVIDER": "console", "BLS_EMAIL_DEBUG_ECHO": "1"}, True, "console+에코"),
            ({**_CLEAR, "BLS_EMAIL_PROVIDER": "console"}, False, "console 실발송 없음"),
        ]
        for env, expected, why in cases:
            with self.subTest(why=why), patch.dict(os.environ, env):
                self.assertEqual(svc.is_send_configured(), expected, why)

    def test_login_policy_uses_the_same_judgement(self):
        from app.routers import auth as auth_router

        with patch.dict(os.environ, {**_CLEAR, "BLS_EMAIL_PROVIDER": "brevo_api",
                                     "BLS_EMAIL_API_KEY": "xkeysib-x", "BLS_EMAIL_FROM": "a@b.co"}):
            self.assertTrue(auth_router._email_switch_available())


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
