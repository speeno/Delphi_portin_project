"""DEC-RBAC-04 / account-menu-fxx-rbac Phase D — Fxx caps JWT merge 회귀.

검증 범위
---------
1. ``app.core.fxx_caps`` 단일 정본의 셀(O/R/X) 의미가 ``derive_fkey_caps`` 와
   완전히 동일 — debug probe / 백엔드 / 프론트가 같은 결정 트리를 공유한다.
2. ``build_fxx_caps_from_matrix`` 가 audit JSON 정본
   (``analysis/audit/account-menu-fxx-5019.json``) 의 교문사·경리부 Fxx 를
   read/write/print 셀로 정확히 변환.
3. ``_make_token_pair`` 가 JWT 페이로드에 ``fxx_caps`` 클레임을 싣고,
   ``get_current_user`` 가 ctx 로 그대로 복원한다.
4. ``require_fxx_write("F11")`` Depends 팩토리가 슈퍼/O/R/X 시나리오에서
   각각 통과/통과/403/403 을 정확히 산출.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

import pytest
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
AUDIT = ROOT / "analysis" / "audit" / "account-menu-fxx-5019.json"
sys.path.insert(0, str(BACKEND))


class FxxCapsCellSemantics(TestCase):
    def test_o_r_x_to_caps(self) -> None:
        from app.core.fxx_caps import derive_fkey_caps

        self.assertEqual(
            derive_fkey_caps("O"),
            {"read": True, "write": True, "print": True},
        )
        self.assertEqual(
            derive_fkey_caps("R"),
            {"read": True, "write": False, "print": True},
        )
        self.assertEqual(
            derive_fkey_caps("X"),
            {"read": False, "write": False, "print": False},
        )
        # 빈/누락/소문자도 안전 정규화 (probe 의 derive_fkey_caps 와 동일).
        self.assertEqual(
            derive_fkey_caps(""),
            {"read": False, "write": False, "print": False},
        )
        self.assertEqual(
            derive_fkey_caps("o"),
            {"read": True, "write": True, "print": True},
        )

    def test_probe_thin_alias_matches_backend(self) -> None:
        """probe `derive_fkey_caps` 가 백엔드 단일 정본을 그대로 위임한다 (DIP)."""
        from app.core.fxx_caps import derive_fkey_caps as backend_derive

        sys.path.insert(0, str(ROOT / "debug"))
        from probe_account_fxx_caps import derive_fkey_caps as probe_derive

        for cell in ("O", "R", "X", "", "o", "r"):
            self.assertEqual(probe_derive(cell), backend_derive(cell))


class FxxCapsMatrixVsAudit(TestCase):
    """audit JSON 정본의 교문사/경리부 Fxx 가 정확히 caps 매트릭스로 매핑된다."""

    @classmethod
    def setUpClass(cls) -> None:
        doc = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.accounts = doc.get("accounts") or {}

    def _row_for(self, gcode: str) -> dict[str, str]:
        entry = self.accounts.get(gcode)
        if not isinstance(entry, dict):
            raise AssertionError(f"{gcode} not found in audit JSON")
        return entry.get("fxx") or {}

    def test_kyomunsa_master_writes_o(self) -> None:
        """교문사: F11(거래처)=O / F14(도서)=O / F17(출판사)=O — 마스터 쓰기 허용."""
        from app.core.fxx_caps import build_fxx_caps_from_matrix

        fxx = self._row_for("교문사")
        caps = build_fxx_caps_from_matrix(fxx)
        for ok_fkey in ("F11", "F14", "F17"):
            self.assertEqual(
                caps.get(ok_fkey, {}).get("write"),
                True,
                f"교문사 {ok_fkey} write 가 True 여야 audit JSON 과 일치",
            )

    def test_kyomunsa_read_only_masters_block_writes(self) -> None:
        """교문사: F12/F13/F15=R 마스터 — write=False (R 셀)."""
        from app.core.fxx_caps import build_fxx_caps_from_matrix

        fxx = self._row_for("교문사")
        caps = build_fxx_caps_from_matrix(fxx)
        for r_fkey in ("F12", "F13", "F15"):
            self.assertEqual(caps.get(r_fkey, {}).get("read"), True)
            self.assertEqual(
                caps.get(r_fkey, {}).get("write"),
                False,
                f"교문사 {r_fkey}=R 의 write 는 False 여야 한다 (canWrite 회귀 차단).",
            )

    def test_kyomunsa_f26_x_blocks(self) -> None:
        """교문사: F26=X — bulk master.write 차단."""
        from app.core.fxx_caps import build_fxx_caps_from_matrix

        fxx = self._row_for("교문사")
        caps = build_fxx_caps_from_matrix(fxx)
        cell = caps.get("F26") or {}
        self.assertEqual(cell.get("read"), False)
        self.assertEqual(cell.get("write"), False)

    def test_accounting_dept_no_master_caps(self) -> None:
        """경리부: F11~F15 셀 자체가 없으므로 caps 매트릭스에도 없거나 모두 False."""
        from app.core.fxx_caps import build_fxx_caps_from_matrix

        fxx = self._row_for("경리부")
        caps = build_fxx_caps_from_matrix(fxx)
        for fkey in ("F11", "F12", "F13", "F14", "F15"):
            cell = caps.get(fkey)
            if cell is None:
                continue
            self.assertEqual(cell.get("read"), False, f"{fkey} read should be False")
            self.assertEqual(cell.get("write"), False, f"{fkey} write should be False")
        # 통계/회계는 O 부여(레거시 동등 — F51~55 부서 셸)
        for fkey in ("F51", "F52", "F53", "F54", "F55"):
            self.assertEqual(caps.get(fkey, {}).get("write"), True, f"{fkey}=O 가 audit 정본")


class JwtTokenIncludesFxxCaps(TestCase):
    """``_make_token_pair`` + ``get_current_user`` 가 ``fxx_caps`` 를 왕복한다."""

    def test_token_pair_serializes_fxx_caps(self) -> None:
        from app.routers.auth import _make_token_pair

        user = {
            "user_id": "kyomunsa",
            "server_id": "remote_153",
            "hcode": "5019",
            "role": "",
            "permissions": ["master.customer.read", "master.book.read"],
            "license_keys": ["F11", "F12", "F14"],
            "fxx_caps": {
                "F11": {"read": True, "write": True, "print": True},
                "F12": {"read": True, "write": False, "print": True},
            },
            "primary_data_server_set": True,
            "account_type": "T2_PUB",
        }
        token = _make_token_pair(user)
        self.assertEqual(token.user.fxx_caps["F11"]["write"], True)
        self.assertEqual(token.user.fxx_caps["F12"]["write"], False)


class JwtCurrentUserPayloadContainsFxxCaps(IsolatedAsyncioTestCase):
    async def test_get_current_user_restores_fxx_caps(self) -> None:
        import os
        os.environ.setdefault("BLS_JWT_SECRET", "test-secret-fxx-caps")
        from app.core.security import create_access_token
        from app.routers.auth import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials

        token = create_access_token(
            {
                "sub": "kyomunsa",
                "sid": "remote_153",
                "hcode": "5019",
                "role": "",
                "permissions": ["master.customer.read"],
                "license_keys": ["F11"],
                "fxx_caps": {
                    "F11": {"read": True, "write": True, "print": True},
                    "F12": {"read": True, "write": False, "print": True},
                },
            }
        )
        cred = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        ctx = await get_current_user(cred)
        self.assertEqual(
            ctx["fxx_caps"]["F11"], {"read": True, "write": True, "print": True}
        )
        self.assertEqual(ctx["fxx_caps"]["F12"]["write"], False)


class RequireFxxWriteDependency(IsolatedAsyncioTestCase):
    async def test_super_user_passes_without_caps(self) -> None:
        from app.core.deps import require_fxx_write

        dep = require_fxx_write("F11")
        ctx = {
            "permissions": ["*"],
            "role": "admin",
            "fxx_caps": {},
        }
        # 슈퍼유저 우회 — fxx_caps 가 비어 있어도 통과.
        result = await dep.__wrapped__(ctx) if hasattr(dep, "__wrapped__") else None
        # FastAPI Depends 콜러블은 wrapped 가 아니라 바로 호출 가능 — 직접 호출.
        result = await dep(ctx)
        self.assertEqual(result, ctx)

    async def test_o_cell_allows_write(self) -> None:
        from app.core.deps import require_fxx_write

        dep = require_fxx_write("F11")
        ctx = {
            "permissions": ["master.customer.read"],
            "role": "",
            "fxx_caps": {"F11": {"read": True, "write": True, "print": True}},
        }
        result = await dep(ctx)
        self.assertEqual(result, ctx)

    async def test_r_cell_denies_write(self) -> None:
        from app.core.deps import require_fxx_write

        dep = require_fxx_write("F12")
        ctx = {
            "permissions": ["master.book.read"],
            "role": "",
            "fxx_caps": {"F12": {"read": True, "write": False, "print": True}},
        }
        with pytest.raises(HTTPException) as exc:
            await dep(ctx)
        self.assertEqual(exc.value.status_code, 403)
        self.assertEqual(exc.value.detail.get("code"), "PERMISSION_DENIED")
        self.assertEqual(exc.value.detail.get("detail", {}).get("required_fxx"), "F12")
        self.assertEqual(exc.value.detail.get("detail", {}).get("action"), "write")

    async def test_missing_cell_denies_write(self) -> None:
        from app.core.deps import require_fxx_write

        dep = require_fxx_write("F11")
        ctx = {
            "permissions": ["report.read"],
            "role": "",
            "fxx_caps": {},  # 경리부 시나리오 — F11 셀 없음
        }
        with pytest.raises(HTTPException) as exc:
            await dep(ctx)
        self.assertEqual(exc.value.status_code, 403)


if __name__ == "__main__":
    main(verbosity=2)
