"""ACC-DATA-03 보강 — 식별자/범위/패턴 tamper 가드 + scope 최후 방어선 단위 테스트.

검증 대상 (deps.py / hcode_isolation.py)
----------------------------------------
- enforce_hcode_identity : 단건 식별자(customerCode·courier hcode·scan hcode)
- enforce_hcode_range    : hcode 구간(courier hcodeFrom~hcodeTo)
- enforce_hcode_pattern  : LIKE 패턴(통합 원장 customerPattern)
- guard_scope_bound      : multi-tenant 테이블 scope 미바인딩 런타임 검출

정책
----
- 격리 계정(T2_PUB·T3 공유 DB): 빈 값 → JWT scope 자동 주입, 타사 값 → 403.
- 슈퍼만 광역 조회 허용. 그 외는 JWT scope 주입 + tamper 403.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi import HTTPException  # noqa: E402

from app.core.deps import (  # noqa: E402
    enforce_hcode_identity,
    enforce_hcode_pattern,
    enforce_hcode_range,
)
from app.core.hcode_isolation import guard_scope_bound  # noqa: E402
from app.core.hcode_scope_context import (  # noqa: E402
    clear_hcode_scope_context,
    set_hcode_scope_context,
)


def _ctx_t2_pub(hcode: str = "9001") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["ledger.read"],
        "account_type": "T2_PUB",
        "account_family": "",
    }


def _ctx_t2_dist(hcode: str = "1001") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["ledger.read"],
        "account_type": "T2_DIST",
        "account_family": "kbt",
    }


def _ctx_super() -> dict:
    return {
        "role": "admin",
        "hcode": "0000",
        "permissions": ["*"],
        "account_type": "T1",
        "account_family": "",
    }


def _ctx_t3_chul09(hcode: str = "KMS01") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["ledger.read"],
        "account_type": "T3",
        "account_family": "chul_09",
    }


class EnforceHcodeIdentityTests(TestCase):
    def test_t2_pub_empty_injects_scope(self) -> None:
        self.assertEqual(enforce_hcode_identity(None, _ctx_t2_pub("9001")), "9001")
        self.assertEqual(enforce_hcode_identity("", _ctx_t2_pub("9001")), "9001")

    def test_t2_pub_own_passes(self) -> None:
        self.assertEqual(enforce_hcode_identity("9001", _ctx_t2_pub("9001")), "9001")

    def test_t2_pub_other_raises_403(self) -> None:
        with self.assertRaises(HTTPException) as cm:
            enforce_hcode_identity("OTHER", _ctx_t2_pub("9001"), field="customerCode")
        self.assertEqual(cm.exception.status_code, 403)
        self.assertEqual(cm.exception.detail.get("code"), "HCODE_FORBIDDEN")
        self.assertEqual(cm.exception.detail.get("field"), "customerCode")

    def test_t3_chul09_other_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_identity("OTHER", _ctx_t3_chul09("KMS01"))

    def test_t2_dist_other_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_identity("9001", _ctx_t2_dist("1001"))

    def test_t2_dist_own_passes(self) -> None:
        self.assertEqual(enforce_hcode_identity("1001", _ctx_t2_dist("1001")), "1001")

    def test_super_arbitrary_passes(self) -> None:
        self.assertEqual(enforce_hcode_identity("ANY", _ctx_super()), "ANY")

    def test_t2_dist_empty_injects_scope(self) -> None:
        self.assertEqual(enforce_hcode_identity(None, _ctx_t2_dist("1001")), "1001")


class EnforceHcodeRangeTests(TestCase):
    def test_t2_pub_empty_forces_scope_pair(self) -> None:
        self.assertEqual(
            enforce_hcode_range(None, None, _ctx_t2_pub("9001")), ("9001", "9001")
        )

    def test_t2_pub_own_pair_passes(self) -> None:
        self.assertEqual(
            enforce_hcode_range("9001", "9001", _ctx_t2_pub("9001")), ("9001", "9001")
        )

    def test_t2_pub_other_range_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_range("0001", "ZZZZ", _ctx_t2_pub("9001"))

    def test_t2_dist_other_range_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_range("0001", "ZZZZ", _ctx_t2_dist("1001"))


class EnforceHcodePatternTests(TestCase):
    def test_t2_pub_empty_returns_scope(self) -> None:
        self.assertEqual(enforce_hcode_pattern("", _ctx_t2_pub("9001")), "9001")

    def test_t2_pub_own_pattern_returns_scope(self) -> None:
        self.assertEqual(enforce_hcode_pattern("9001", _ctx_t2_pub("9001")), "9001")

    def test_t2_pub_other_pattern_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_pattern("00", _ctx_t2_pub("9001"))

    def test_t2_dist_other_pattern_raises_403(self) -> None:
        with self.assertRaises(HTTPException):
            enforce_hcode_pattern("00", _ctx_t2_dist("1001"))

    def test_t2_dist_empty_pattern_returns_scope(self) -> None:
        self.assertEqual(enforce_hcode_pattern("", _ctx_t2_dist("1001")), "1001")


class GuardScopeBoundTests(TestCase):
    def tearDown(self) -> None:
        clear_hcode_scope_context()

    def test_no_request_ctx_is_noop(self) -> None:
        clear_hcode_scope_context()
        guard_scope_bound("", table="S1_Ssub")  # 예외 없음

    def test_not_required_is_noop(self) -> None:
        set_hcode_scope_context(row_filter_required=False)
        guard_scope_bound("", table="S1_Ssub")

    def test_required_with_scope_is_noop(self) -> None:
        set_hcode_scope_context(row_filter_required=True, scope_hcode="9001")
        guard_scope_bound("9001", table="S1_Ssub")

    def test_required_missing_scope_warns_by_default(self) -> None:
        # 기본(warn) 모드: 예외 없이 통과(로그만).
        set_hcode_scope_context(row_filter_required=True, scope_hcode="9001")
        guard_scope_bound("", table="S1_Ssub")

    def test_required_missing_scope_strict_raises(self) -> None:
        import os

        set_hcode_scope_context(row_filter_required=True, scope_hcode="9001")
        old = os.environ.get("BLS_HCODE_SCOPE_GUARD")
        os.environ["BLS_HCODE_SCOPE_GUARD"] = "strict"
        try:
            with self.assertRaises(RuntimeError):
                guard_scope_bound("", table="S1_Ssub")
        finally:
            if old is None:
                os.environ.pop("BLS_HCODE_SCOPE_GUARD", None)
            else:
                os.environ["BLS_HCODE_SCOPE_GUARD"] = old


if __name__ == "__main__":
    main()
