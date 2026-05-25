"""`enforce_hcode_isolation` 회귀 가드 — Hcode 전면 적용 Phase 2.

검증 시나리오 (ACC-DATA-03 / DEC-033 f / M4 tamper)
---------------------------------------------------
1. T2_PUB·공유 DB 계정 + 빈 hcode → JWT scope 가 자동 주입.
2. T2_PUB 계정이 본인 hcode 와 다른 값을 명시 → 403 ``HCODE_FORBIDDEN``.
3. T2_PUB 계정이 본인 hcode 와 동일한 값을 명시 → 통과.
4. T2_DIST·super 계정은 임의 hcode 명시 가능.
5. 점검(`inspect_subject_hcode`) 모드는 명시값을 그대로 통과.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi import HTTPException  # noqa: E402

from app.core.deps import enforce_hcode_isolation  # noqa: E402


def _ctx_t2_pub(hcode: str = "9001") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["master.read"],
        "account_type": "T2_PUB",
        "account_family": "",
    }


def _ctx_t2_dist(hcode: str = "1001") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["master.read"],
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


def _ctx_t3_chul09(hcode: str = "9001") -> dict:
    return {
        "role": "operator",
        "hcode": hcode,
        "permissions": ["master.read"],
        "account_type": "T3",
        "account_family": "chul_09",
    }


class EnforceHcodeIsolationTests(TestCase):
    # ── coalesce 의미 보존 ──
    def test_t2_pub_empty_query_injects_jwt_scope(self) -> None:
        self.assertEqual(enforce_hcode_isolation(None, _ctx_t2_pub("9001")), "9001")
        self.assertEqual(enforce_hcode_isolation("", _ctx_t2_pub("9001")), "9001")
        self.assertEqual(enforce_hcode_isolation("0000", _ctx_t2_pub("9001")), "9001")

    def test_t3_chul09_empty_query_injects_jwt_scope(self) -> None:
        self.assertEqual(
            enforce_hcode_isolation("", _ctx_t3_chul09("KMS01")), "KMS01"
        )

    def test_t2_dist_empty_query_returns_none(self) -> None:
        # 총판은 빈 hcode = 전체 (DEC-033 f).
        self.assertIsNone(enforce_hcode_isolation(None, _ctx_t2_dist("1001")))

    def test_super_empty_query_returns_none(self) -> None:
        self.assertIsNone(enforce_hcode_isolation(None, _ctx_super()))

    # ── tamper 가드 ──
    def test_t2_pub_other_hcode_raises_403(self) -> None:
        ctx = _ctx_t2_pub("9001")
        with self.assertRaises(HTTPException) as cm:
            enforce_hcode_isolation("OTHER", ctx)
        exc = cm.exception
        self.assertEqual(exc.status_code, 403)
        self.assertIsInstance(exc.detail, dict)
        self.assertEqual(exc.detail.get("code"), "HCODE_FORBIDDEN")

    def test_t2_pub_own_hcode_passes(self) -> None:
        self.assertEqual(
            enforce_hcode_isolation("9001", _ctx_t2_pub("9001")), "9001"
        )

    def test_t2_dist_arbitrary_hcode_passes(self) -> None:
        # 총판은 다른 거래처 hcode 명시 허용.
        self.assertEqual(
            enforce_hcode_isolation("9001", _ctx_t2_dist("1001")), "9001"
        )

    def test_super_arbitrary_hcode_passes(self) -> None:
        self.assertEqual(
            enforce_hcode_isolation("ANY", _ctx_super()), "ANY"
        )

    # ── 점검 모드 ──
    def test_inspect_subject_overrides_jwt(self) -> None:
        ctx = _ctx_t2_pub("9001")
        ctx["inspect_subject_hcode"] = "INSPECT01"
        # 빈 입력 → inspect 값으로 fallback.
        self.assertEqual(enforce_hcode_isolation("", ctx), "INSPECT01")

    def test_inspect_explicit_match_passes(self) -> None:
        ctx = _ctx_t2_pub("9001")
        ctx["inspect_subject_hcode"] = "INSPECT01"
        # 명시 hcode 가 inspect scope 와 일치 — 통과.
        self.assertEqual(
            enforce_hcode_isolation("INSPECT01", ctx), "INSPECT01"
        )

    def test_inspect_explicit_mismatch_raises(self) -> None:
        ctx = _ctx_t2_pub("9001")
        ctx["inspect_subject_hcode"] = "INSPECT01"
        # 명시 hcode 가 inspect scope 와 다르면 — 점검도 격리.
        with self.assertRaises(HTTPException):
            enforce_hcode_isolation("OTHER", ctx)


if __name__ == "__main__":
    main()
