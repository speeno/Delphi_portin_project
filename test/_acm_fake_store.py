"""ACM 테스트용 인메모리 Web_Accounts 저장소 — ``web_accounts_db`` 의 공개 함수와 동일 시그니처.

실 DB 없이 전환 흐름·이메일 로그인을 검증한다. ``patch_store(module)`` 이 서비스 모듈이 참조하는
``store`` 이름의 함수들을 이 객체의 메서드로 바꿔 끼운다.
"""

from __future__ import annotations

from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import patch

from app.services import web_accounts_db as real

_TS = "%Y-%m-%d %H:%M:%S"


class FakeStore:
    def __init__(self) -> None:
        self.accounts: dict[str, dict[str, Any]] = {}
        self.links: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        self.codes: list[dict[str, Any]] = []
        self.ensure_calls = 0
        self.fail = False  # True 면 모든 호출이 예외 (저장소 장애 시나리오)

    # ── util passthrough ──
    normalize_email = staticmethod(real.normalize_email)
    identity_key = staticmethod(real.identity_key)
    parse_ts = staticmethod(real.parse_ts)
    now_ts = staticmethod(real.now_ts)
    ts_after = staticmethod(real.ts_after)
    is_locked = staticmethod(real.is_locked)
    AccountExists = real.AccountExists
    LinkExists = real.LinkExists

    def _guard(self) -> None:
        if self.fail:
            raise RuntimeError("store down")

    async def ensure_store(self) -> None:
        self._guard(); self.ensure_calls += 1

    # ── accounts ──
    async def get_account_by_email(self, email):
        self._guard()
        e = real.normalize_email(email)
        for a in self.accounts.values():
            if a["Email"] == e:
                return dict(a)
        return None

    async def get_account_by_id(self, account_id):
        self._guard(); a = self.accounts.get(account_id); return dict(a) if a else None

    async def create_account(self, *, email, pw_hash, pw_secret):
        self._guard()
        e = real.normalize_email(email)
        if any(a["Email"] == e for a in self.accounts.values()):
            raise real.AccountExists(e)
        aid = real.new_id(); ts = real.now_ts()
        self.accounts[aid] = {"AccountId": aid, "Email": e, "PwHash": pw_hash, "PwPlain": pw_secret, "Status": "active",
                              "EmailVerifiedAt": ts, "CreatedAt": ts, "LastLoginAt": "", "FailCount": 0, "LockedUntil": ""}
        return dict(self.accounts[aid])

    async def update_password(self, *, account_id, pw_hash, pw_secret):
        self._guard(); a = self.accounts[account_id]; a.update(PwHash=pw_hash, PwPlain=pw_secret, FailCount=0, LockedUntil="")

    async def record_login_success(self, account_id):
        self._guard(); a = self.accounts[account_id]; a.update(LastLoginAt=real.now_ts(), FailCount=0, LockedUntil="")

    async def record_login_failure(self, account, *, max_fail=5, lock_minutes=15):
        self._guard(); a = self.accounts[account["AccountId"]]
        fails = int(a["FailCount"]) + 1
        if fails >= max_fail:
            a.update(FailCount=0, LockedUntil=real.ts_after(minutes=lock_minutes)); return True
        a["FailCount"] = fails; return False

    # ── links ──
    async def list_links(self, account_id):
        self._guard(); return [dict(l) for l in self.links.values() if l["AccountId"] == account_id]

    async def find_link(self, server_id, db_name, hcode, gcode):
        self._guard(); l = self.links.get(real.identity_key(server_id, db_name, hcode, gcode)); return dict(l) if l else None

    async def find_links_by_scope(self, account_id, server_id, db_name, hcode):
        self._guard()
        return [dict(l) for k, l in self.links.items() if l["AccountId"] == account_id and k[:3] == (server_id, db_name, hcode)]

    async def add_link(self, *, account_id, server_id, db_name, hcode, gcode, gname="", hname="", tenant_id="", label=""):
        self._guard(); k = real.identity_key(server_id, db_name, hcode, gcode)
        if k in self.links:
            raise real.LinkExists(k)
        ts = real.now_ts()
        self.links[k] = {"AccountId": account_id, "ServerId": k[0], "DbName": k[1], "Hcode": k[2], "Gcode": k[3], "Gname": gname,
                         "Hname": hname, "TenantId": tenant_id, "Label": label, "LinkedAt": ts, "LastSeenAt": ts, "StaleAt": ""}
        return dict(self.links[k])

    async def delete_link(self, server_id, db_name, hcode, gcode):
        self._guard(); self.links.pop(real.identity_key(server_id, db_name, hcode, gcode), None)

    async def mark_link_seen(self, server_id, db_name, hcode, gcode):
        self._guard(); l = self.links.get(real.identity_key(server_id, db_name, hcode, gcode))
        if l: l.update(LastSeenAt=real.now_ts(), StaleAt="")

    async def mark_link_stale(self, server_id, db_name, hcode, gcode):
        self._guard(); l = self.links.get(real.identity_key(server_id, db_name, hcode, gcode))
        if l and not l["StaleAt"]: l["StaleAt"] = real.now_ts()

    async def count_links_for_account(self, account_id):
        self._guard(); return sum(1 for l in self.links.values() if l["AccountId"] == account_id)

    # ── codes ──
    async def create_code(self, *, email, purpose, code_hash, salt, ticket_id, expires_at, client_ip):
        self._guard(); cid = real.new_id()
        self.codes.append({"CodeId": cid, "Email": real.normalize_email(email), "Purpose": purpose, "CodeHash": code_hash, "Salt": salt,
                           "TicketId": ticket_id, "ExpiresAt": expires_at, "Attempts": 0, "UsedAt": "", "SentAt": real.now_ts(), "ClientIp": client_ip})
        return cid

    async def get_latest_code(self, email, purpose):
        self._guard(); e = real.normalize_email(email)
        rows = [c for c in self.codes if c["Email"] == e and c["Purpose"] == purpose and not c["UsedAt"]]
        return dict(rows[-1]) if rows else None

    async def count_codes_since(self, email, since_ts):
        self._guard(); e = real.normalize_email(email)
        return sum(1 for c in self.codes if c["Email"] == e and c["SentAt"] >= since_ts)

    async def count_codes_by_ip_since(self, client_ip, since_ts):
        self._guard(); return sum(1 for c in self.codes if c["ClientIp"] == client_ip and c["SentAt"] >= since_ts)

    async def increment_attempts(self, code_id):
        self._guard()
        for c in self.codes:
            if c["CodeId"] == code_id: c["Attempts"] += 1

    async def mark_code_used(self, code_id):
        self._guard()
        for c in self.codes:
            if c["CodeId"] == code_id: c["UsedAt"] = real.now_ts()

    async def invalidate_codes(self, email, purpose):
        self._guard(); e = real.normalize_email(email)
        for c in self.codes:
            if c["Email"] == e and c["Purpose"] == purpose and not c["UsedAt"]: c["UsedAt"] = real.now_ts()

    async def delete_expired_codes(self, email):
        self._guard()

    # ── 테스트 보조 ──
    def latest_code_plain(self) -> str | None:
        return getattr(self, "_last_code", None)

    def backdate_latest_sent(self, seconds: int) -> None:
        c = self.codes[-1]
        c["SentAt"] = (datetime.now(timezone.utc) - timedelta(seconds=seconds)).strftime(_TS)


def patch_store(store: FakeStore):
    """``account_switch_service.store`` 가 가리키는 모듈 함수들을 FakeStore 메서드로 교체하는 ExitStack."""
    stack = ExitStack()
    names = [n for n in dir(FakeStore) if not n.startswith("_") and n not in ("latest_code_plain", "backdate_latest_sent")]
    for n in names:
        if hasattr(real, n) and callable(getattr(real, n)) and n not in ("AccountExists", "LinkExists"):
            stack.enter_context(patch.object(real, n, getattr(store, n)))
    return stack
