"""ACM / DEC-235 — 계정 전환 3단계 · 이메일 로그인 · 링크 규칙 · 코드 정책 · 비밀 무노출 회귀 가드.

실 DB 없이: 로그인 코어(``auth_login_core.resolve_and_authenticate``)·identity 로더
(``auth_service.load_user_by_identity``)·메일 발송(``email_dispatch_service.send_email``)을 patch 하고,
저장소는 ``_acm_fake_store.FakeStore`` 로 대체한다.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
sys.path.insert(0, str(ROOT / "test"))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.services import account_switch_service as acs  # noqa: E402
from app.services import auth_login_core  # noqa: E402
from app.services import account_secret_codec as codec  # noqa: E402
from _acm_fake_store import FakeStore, patch_store  # noqa: E402

_ENV = {
    "BLS_EMAIL_PROVIDER": "console",
    "BLS_EMAIL_DEBUG_ECHO": "1",
    "BLS_LEGACY_ID_LOGIN": "on",
    "BLS_ACCOUNT_PW_STORE": "plain",
    "BLS_PUBLIC_BASE_URL": "https://web.example.test",
}


def _legacy_user(gcode="hong", hcode="x1060", db="book_kb_db", sid="remote_138"):
    return {
        "user_id": gcode, "user_name": "한빛출판", "display_name": "홍길동", "gname": "홍길동",
        "server_id": sid, "server_label": "서버 138", "hcode": hcode, "role": "operator", "permissions": ["outbound.read"],
        "account_type": "T3", "tenant_id": "tid-kb", "account_family": "book_kb", "active_build_id": "BLD-PUB-KBT",
        "build_role": "publisher", "dist_hcode": None, "license_keys": ["F11"], "login_profile": "std",
        "menu_shell_hint": "", "fxx_caps": {"F11": {"read": True, "write": True, "print": True}},
        "resolved_db": db, "ownership_status": "unique", "ownership_candidate_count": 1,
    }


def _outcome_ok(user=None, sid="remote_138", db="book_kb_db"):
    o = auth_login_core.LoginOutcome()
    o.user = user or _legacy_user(sid=sid, db=db)
    o.hit_candidate = {"remote_id": sid, "db_name": db, "tenant_id": "tid-kb", "account_family": "book_kb", "candidate_via": "index_single"}
    o.target_server, o.target_db, o.resolved_via = sid, db, "index_single"
    o.candidates = [o.hit_candidate]; o.attempts = [(sid, db)]
    return o


def _outcome_fail():
    o = auth_login_core.LoginOutcome(); o.fail_reason = "invalid_credentials"; o.primary_sid = "remote_138"; return o


class _Base(unittest.TestCase):
    def setUp(self) -> None:
        # 다른 테스트가 남긴 get_current_user 등 dependency override 격리 (전체 스위트 순서 의존 방지).
        self._saved_overrides = dict(app.dependency_overrides)
        app.dependency_overrides.clear()
        self.client = TestClient(app)
        self.store = FakeStore()
        self._stack = patch_store(self.store)
        self._stack.__enter__()
        self._env = patch.dict(os.environ, _ENV); self._env.__enter__()
        self._label = patch.object(auth_login_core, "org_label", lambda cand, hcode="": "한빛출판"); self._label.__enter__()

    def tearDown(self) -> None:
        self._label.__exit__(None, None, None)
        self._env.__exit__(None, None, None)
        self._stack.__exit__(None, None, None)
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self._saved_overrides)

    # ── helpers ──
    def verify(self, **body):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok())):
            return self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "pw", **body})

    def send(self, ticket, email="Hong@Company.co.kr"):
        return self.client.post("/api/v1/public/account-switch/send-code", json={"switchTicket": ticket, "email": email})

    def complete(self, ticket, code, email="hong@company.co.kr", password="abc12345"):
        body = {"switchTicket": ticket, "email": email, "code": code}
        if password is not None:
            body["newPassword"] = password
        return self.client.post("/api/v1/public/account-switch/complete", json=body)

    def switch_full(self, email="hong@company.co.kr", password="abc12345", user=None):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok(user=user))):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "pw"})
        self.assertEqual(r.status_code, 200, r.text)
        ticket = r.json()["switchTicket"]
        s = self.send(ticket, email); self.assertEqual(s.status_code, 200, s.text)
        c = self.complete(ticket, s.json()["debugCode"], email=email, password=password)
        self.assertEqual(c.status_code, 200, c.text)
        return c.json()

    def email_login(self, email, password, **hints):
        with patch("app.services.auth_service.load_user_by_identity", AsyncMock(return_value=_legacy_user())):
            return self.client.post("/api/v1/auth/login", json={"userId": email, "password": password, **hints})


class SwitchFlowTests(_Base):
    def test_verify_legacy_issues_ticket_without_touching_password(self):
        r = self.verify()
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertIn("switchTicket", body)
        self.assertEqual(body["legacy"]["userId"], "hong")
        self.assertEqual(body["legacy"]["label"], "한빛출판")
        self.assertNotIn("pw", r.text)
        t = acs.decode_switch_ticket(body["switchTicket"])
        self.assertEqual(t["type"], "switch"); self.assertEqual(t["gcode"], "hong"); self.assertEqual(t["rdb"], "book_kb_db")
        self.assertNotIn("password", t)

    def test_verify_legacy_invalid_is_same_401_message_as_login(self):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_fail())):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "bad"})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.json()["detail"]["message"], "아이디 또는 비밀번호가 올바르지 않습니다.")

    def test_verify_legacy_passes_org_select_challenge_through(self):
        o = _outcome_ok(); o.org_choices = [{"serverId": "remote_138", "dbName": "a_db", "tenantId": "t1", "hcode": "h", "label": "A"},
                                            {"serverId": "remote_138", "dbName": "b_db", "tenantId": "t2", "hcode": "h", "label": "B"}]
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=o)):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "pw"})
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["detail"]["code"], "ORG_SELECT_REQUIRED")
        self.assertEqual(len(r.json()["detail"]["choices"]), 2)

    def test_full_switch_creates_account_hash_and_plain_and_link(self):
        out = self.switch_full()
        self.assertEqual(out["mode"], "new"); self.assertEqual(out["linkedCount"], 1)
        self.assertIn("델파이", out["message"])
        self.assertNotIn("accountId", out)
        acct = next(iter(self.store.accounts.values()))
        self.assertEqual(acct["Email"], "hong@company.co.kr")
        self.assertTrue(codec.verify_password("abc12345", acct["PwHash"]))
        self.assertEqual(acct["PwPlain"], "abc12345")  # ACM-DEC-05 요구안(plain 모드)
        link = next(iter(self.store.links.values()))
        self.assertEqual((link["ServerId"], link["DbName"], link["Hcode"], link["Gcode"]), ("remote_138", "book_kb_db", "x1060", "hong"))
        self.assertEqual(link["Label"], "한빛출판")

    def test_send_code_normalizes_email_and_stores_hash_only(self):
        r = self.verify(); ticket = r.json()["switchTicket"]
        s = self.send(ticket, "  Hong@Company.co.kr ")
        self.assertEqual(s.status_code, 200, s.text)
        code = s.json()["debugCode"]
        row = self.store.codes[-1]
        self.assertEqual(row["Email"], "hong@company.co.kr")
        self.assertNotEqual(row["CodeHash"], code); self.assertNotIn(code, row["CodeHash"])
        self.assertEqual(row["TicketId"], acs.decode_switch_ticket(ticket)["jti"])

    def test_code_wrong_five_times_locks(self):
        ticket = self.verify().json()["switchTicket"]
        s = self.send(ticket); self.assertEqual(s.status_code, 200)
        codes = []
        for i in range(5):
            c = self.complete(ticket, "000000" if s.json()["debugCode"] != "000000" else "111111")
            codes.append(c.status_code)
        self.assertEqual(codes[:4], [400] * 4)
        self.assertEqual(codes[4], 423)
        # 정답이라도 소진된 코드는 무효
        c = self.complete(ticket, s.json()["debugCode"]); self.assertEqual(c.status_code, 400)

    def test_resend_cooldown_and_hourly_limit(self):
        ticket = self.verify().json()["switchTicket"]
        self.assertEqual(self.send(ticket).status_code, 200)
        r = self.send(ticket); self.assertEqual(r.status_code, 429)
        self.assertEqual(r.json()["detail"]["code"], "ACCT_CODE_RATE_LIMITED")
        self.store.backdate_latest_sent(61)
        self.assertEqual(self.send(ticket).status_code, 200)

    def test_expired_ticket_is_410(self):
        with patch.object(acs, "TICKET_TTL_MIN", -1):
            ticket = self.verify().json()["switchTicket"]
        r = self.send(ticket); self.assertEqual(r.status_code, 410)
        self.assertEqual(r.json()["detail"]["code"], "ACCT_TICKET_EXPIRED")

    def test_code_bound_to_ticket_jti(self):
        t1 = self.verify().json()["switchTicket"]
        s = self.send(t1); code = s.json()["debugCode"]
        t2 = self.verify().json()["switchTicket"]  # 다른 티켓(같은 identity)
        c = self.complete(t2, code); self.assertEqual(c.status_code, 400)

    def test_weak_password_rejected(self):
        ticket = self.verify().json()["switchTicket"]
        code = self.send(ticket).json()["debugCode"]
        c = self.complete(ticket, code, password="short1")
        self.assertEqual(c.status_code, 422); self.assertEqual(c.json()["detail"]["code"], "ACCT_WEAK_PASSWORD")

    def test_already_switched_identity_is_409_with_masked_email(self):
        self.switch_full()
        r = self.verify()
        self.assertEqual(r.status_code, 409)
        d = r.json()["detail"]
        self.assertEqual(d["code"], "ACCT_ALREADY_SWITCHED")
        self.assertEqual(d["emailMasked"], "h***@company.co.kr")
        self.assertNotIn("hong@company", r.text)

    def test_email_unavailable_when_smtp_send_fails(self):
        ticket = self.verify().json()["switchTicket"]
        from app.services import email_dispatch_service as ed
        with patch.dict(os.environ, {"BLS_EMAIL_PROVIDER": "smtp", "BLS_SMTP_HOST": "h", "BLS_SMTP_USER": "u", "BLS_SMTP_PASSWORD": "p", "BLS_EMAIL_FROM": "n@x.co"}), \
             patch.object(ed, "send_email", AsyncMock(return_value=ed.SendResult(ok=False, provider="smtp", error="SMTPException"))):
            r = self.send(ticket)
        self.assertEqual(r.status_code, 503); self.assertEqual(r.json()["detail"]["code"], "ACCT_EMAIL_UNAVAILABLE")
        self.assertNotIn("debugCode", r.text)


class LookupTests(_Base):
    def lookup(self, **body):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok())):
            return self.client.post("/api/v1/public/account-switch/lookup", json={"userId": "hong", "password": "pw", **body})

    def test_lookup_before_switch_issues_ticket(self):
        r = self.lookup()
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertFalse(body["found"]); self.assertIn("switchTicket", body)
        self.assertEqual(body["legacy"]["userId"], "hong"); self.assertNotIn("account", body)
        self.assertEqual(acs.decode_switch_ticket(body["switchTicket"])["gcode"], "hong")

    def test_lookup_after_switch_shows_email_account(self):
        self.switch_full()
        r = self.lookup()
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertTrue(body["found"]); self.assertNotIn("switchTicket", body)
        self.assertEqual(body["account"]["email"], "hong@company.co.kr")
        self.assertEqual(body["account"]["linkedCount"], 1); self.assertFalse(body["account"]["stale"])

    def test_lookup_invalid_and_org_select(self):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_fail())):
            r = self.client.post("/api/v1/public/account-switch/lookup", json={"userId": "hong", "password": "bad"})
        self.assertEqual(r.status_code, 401)
        o = _outcome_ok(); o.org_choices = [{"serverId": "s", "dbName": "a", "tenantId": "t1", "hcode": "h", "label": "A"},
                                            {"serverId": "s", "dbName": "b", "tenantId": "t2", "hcode": "h", "label": "B"}]
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=o)):
            r = self.client.post("/api/v1/public/account-switch/lookup", json={"userId": "hong", "password": "pw"})
        self.assertEqual(r.status_code, 409); self.assertEqual(r.json()["detail"]["code"], "ORG_SELECT_REQUIRED")


class SweepBudgetTests(_Base):
    """운영 실측 89초(회사 미선택 스윕) → 예산 초과 시 401 대신 409 회사 선택 안내."""

    def test_budget_exhausted_returns_org_hint_required(self):
        o = _outcome_fail()
        o.sweep_budget_exhausted = True
        o.skipped_candidates = 27
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=o)):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "pw"})
            r2 = self.client.post("/api/v1/public/account-switch/lookup", json={"userId": "hong", "password": "pw"})
        for res in (r, r2):
            self.assertEqual(res.status_code, 409, res.text)
            self.assertEqual(res.json()["detail"]["code"], "ACCT_ORG_HINT_REQUIRED")
            self.assertEqual(res.json()["detail"]["skipped"], 27)

    def test_plain_invalid_still_401(self):
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_fail())):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong", "password": "pw"})
        self.assertEqual(r.status_code, 401)


class LinkRuleTests(_Base):
    def test_second_company_links_to_existing_email_without_password(self):
        self.switch_full()
        user2 = _legacy_user(gcode="hong2", hcode="y2020", db="chul_09_db")
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok(user=user2, db="chul_09_db"))):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong2", "password": "pw"})
        ticket = r.json()["switchTicket"]
        s = self.send(ticket); self.assertEqual(s.json()["mode"], "link")
        c = self.complete(ticket, s.json()["debugCode"], password=None)
        self.assertEqual(c.status_code, 200, c.text)
        self.assertEqual(c.json()["mode"], "link"); self.assertEqual(c.json()["linkedCount"], 2)
        self.assertEqual(len(self.store.accounts), 1)

    def test_relink_replaces_stale_link_in_same_scope(self):
        self.switch_full()
        # 델파이에서 Gcode 가 hong → hong_new 로 바뀐 상황: 같은 (서버, DB, hcode)
        user_new = _legacy_user(gcode="hong_new")
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok(user=user_new))):
            r = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong_new", "password": "pw"})
        ticket = r.json()["switchTicket"]
        s = self.send(ticket); self.assertEqual(s.json()["mode"], "relink")
        c = self.complete(ticket, s.json()["debugCode"], password=None)
        self.assertEqual(c.status_code, 200, c.text); self.assertEqual(c.json()["mode"], "relink")
        gcodes = sorted(k[3] for k in self.store.links)
        self.assertEqual(gcodes, ["hong_new"])  # 옛 링크 제거, 계정·이메일 유지
        self.assertEqual(len(self.store.accounts), 1)


class EmailLoginTests(_Base):
    def test_email_login_issues_same_claims_as_legacy(self):
        self.switch_full()
        r = self.email_login("hong@company.co.kr", "abc12345")
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        from app.core.security import decode_token
        claims = decode_token(body["access_token"])
        self.assertEqual(claims["sub"], "hong"); self.assertEqual(claims["sid"], "remote_138")
        self.assertEqual(claims["rdb"], "book_kb_db"); self.assertEqual(claims["hcode"], "x1060")
        self.assertEqual(claims["lvia"], "email"); self.assertTrue(claims["acct"])
        self.assertEqual(claims["fxx_caps"]["F11"]["write"], True)
        self.assertEqual(body["user"]["login_via"], "email"); self.assertEqual(body["user"]["user_id"], "hong")
        # /me 도 동일 identity
        me = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
        self.assertEqual(me.status_code, 200); self.assertEqual(me.json()["user_id"], "hong"); self.assertEqual(me.json()["login_via"], "email")

    def test_email_login_wrong_password_same_401_and_locks_after_five(self):
        self.switch_full()
        for _ in range(4):
            r = self.email_login("hong@company.co.kr", "nope12345")
            self.assertEqual(r.status_code, 401); self.assertEqual(r.json()["detail"], "아이디 또는 비밀번호가 올바르지 않습니다.")
        r = self.email_login("hong@company.co.kr", "nope12345"); self.assertEqual(r.status_code, 423)
        r = self.email_login("hong@company.co.kr", "abc12345"); self.assertEqual(r.status_code, 423)

    def test_unknown_email_is_same_401(self):
        r = self.email_login("nobody@company.co.kr", "abc12345")
        self.assertEqual(r.status_code, 401); self.assertEqual(r.json()["detail"], "아이디 또는 비밀번호가 올바르지 않습니다.")

    def test_stale_link_fails_closed(self):
        """ACM-INV-4 — Id_Logn 행이 사라졌으면(삭제·_이름_ 잠금·Gcode 변경) 401 ACCT_LINK_STALE, 다른 행에 붙지 않음."""
        self.switch_full()
        with patch("app.services.auth_service.load_user_by_identity", AsyncMock(return_value=None)) as loader:
            r = self.client.post("/api/v1/auth/login", json={"userId": "hong@company.co.kr", "password": "abc12345"})
        self.assertEqual(r.status_code, 401); self.assertEqual(r.json()["detail"]["code"], "ACCT_LINK_STALE")
        loader.assert_awaited_once()
        self.assertEqual(loader.await_args.args[:2], ("remote_138", "hong"))
        self.assertEqual(loader.await_args.kwargs["hcode"], "x1060")
        link = next(iter(self.store.links.values())); self.assertTrue(link["StaleAt"])

    def test_identity_reloaded_on_every_login(self):
        """ACM-INV-3 — 권한은 매 로그인마다 Id_Logn 에서 재도출된다(캐시 없음)."""
        self.switch_full()
        with patch("app.services.auth_service.load_user_by_identity", AsyncMock(return_value=_legacy_user())) as loader:
            for _ in range(3):
                self.client.post("/api/v1/auth/login", json={"userId": "hong@company.co.kr", "password": "abc12345"})
        self.assertEqual(loader.await_count, 3)

    def test_multiple_links_require_org_select_then_hint_resolves(self):
        self.switch_full()
        user2 = _legacy_user(gcode="hong2", hcode="y2020", db="chul_09_db")
        with patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok(user=user2, db="chul_09_db"))):
            t = self.client.post("/api/v1/public/account-switch/verify-legacy", json={"userId": "hong2", "password": "pw"}).json()["switchTicket"]
        code = self.send(t).json()["debugCode"]; self.complete(t, code, password=None)
        r = self.email_login("hong@company.co.kr", "abc12345")
        self.assertEqual(r.status_code, 409); d = r.json()["detail"]
        self.assertEqual(d["code"], "ORG_SELECT_REQUIRED"); self.assertEqual(len(d["choices"]), 2)
        r2 = self.email_login("hong@company.co.kr", "abc12345", dbName="chul_09_db")
        self.assertEqual(r2.status_code, 200, r2.text)

    def test_store_unavailable_is_503(self):
        self.store.fail = True
        r = self.client.post("/api/v1/auth/login", json={"userId": "hong@company.co.kr", "password": "x"})
        self.assertEqual(r.status_code, 503); self.assertEqual(r.json()["detail"]["code"], "ACCT_STORE_UNAVAILABLE")


class ResetFlowTests(_Base):
    def test_reset_changes_password_and_unknown_email_is_404(self):
        self.switch_full()
        r = self.client.post("/api/v1/public/account-reset/send-code", json={"email": "hong@company.co.kr"})
        self.assertEqual(r.status_code, 200); code = r.json()["debugCode"]
        r2 = self.client.post("/api/v1/public/account-reset/complete", json={"email": "hong@company.co.kr", "code": code, "newPassword": "newpass99"})
        self.assertEqual(r2.status_code, 200, r2.text)
        self.assertEqual(self.email_login("hong@company.co.kr", "newpass99").status_code, 200)
        self.assertEqual(self.email_login("hong@company.co.kr", "abc12345").status_code, 401)
        # 없는 이메일 — 즉시 404 안내(사용자 결정 2026-09-03), 코드 저장·발송 없음
        n = len(self.store.codes)
        r3 = self.client.post("/api/v1/public/account-reset/send-code", json={"email": "ghost@company.co.kr"})
        self.assertEqual(r3.status_code, 404); self.assertEqual(r3.json()["detail"]["code"], "ACCT_EMAIL_NOT_REGISTERED")
        self.assertNotIn("debugCode", r3.text)
        self.assertEqual(len(self.store.codes), n)


class LegacyLoginPolicyTests(_Base):
    def test_legacy_id_login_blocked_when_flag_off(self):
        with patch.dict(os.environ, {"BLS_LEGACY_ID_LOGIN": "off"}), \
             patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok())) as core:
            r = self.client.post("/api/v1/auth/login", json={"userId": "hong", "password": "pw"})
            pol = self.client.get("/api/v1/auth/login-policy").json()
        self.assertEqual(r.status_code, 403); self.assertEqual(r.json()["detail"]["code"], "ACCT_SWITCH_REQUIRED")
        core.assert_not_awaited()
        self.assertFalse(pol["legacyIdLogin"]); self.assertTrue(pol["emailLogin"])

    def test_legacy_id_login_allowed_by_default_and_policy_reports_switch_available(self):
        with patch.dict(os.environ, {"BLS_LEGACY_ID_LOGIN": ""}), \
             patch.object(auth_login_core, "resolve_and_authenticate", AsyncMock(return_value=_outcome_ok())):
            r = self.client.post("/api/v1/auth/login", json={"userId": "hong", "password": "pw"})
            pol = self.client.get("/api/v1/auth/login-policy").json()
        self.assertEqual(r.status_code, 200, r.text)
        self.assertTrue(pol["legacyIdLogin"]); self.assertTrue(pol["switchAvailable"])  # console + DEBUG_ECHO
        with patch.dict(os.environ, {"BLS_EMAIL_DEBUG_ECHO": "0"}):
            self.assertFalse(self.client.get("/api/v1/auth/login-policy").json()["switchAvailable"])


class NoSecretLeakTests(_Base):
    def test_audit_and_app_logs_never_contain_code_password_or_raw_email(self):
        with self.assertLogs(level="INFO") as cm:
            out_ticket = self.verify().json()["switchTicket"]
            s = self.send(out_ticket); code = s.json()["debugCode"]
            self.complete(out_ticket, code)
            self.email_login("hong@company.co.kr", "abc12345")
        joined = "\n".join(cm.output)
        self.assertNotIn(code, joined)
        self.assertNotIn("abc12345", joined)
        self.assertNotIn(out_ticket, joined)
        self.assertNotIn("hong@company.co.kr", joined)
        self.assertIn("h***@company.co.kr", joined)
        self.assertIn("account_switch.complete", joined); self.assertIn("login.email", joined)


if __name__ == "__main__":
    unittest.main()
