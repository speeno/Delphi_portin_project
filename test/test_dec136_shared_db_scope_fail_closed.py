"""DEC-136 — 공유 DB 좌표 정산 스코프 fail-closed 회귀 가드.

배경(2026-08-09 교문사-경리부 리포트): 정산관리 하위 화면 값이 "본인들 자료가
아니다" — remote_153 의 chul_09_db 는 **위러브3 + 교문사가 hcode 로만 구분해 공유**
(welove-login-tenant-audit B3/B4). 종전 `resolve_g7_ggeo_list_scope` 는 T2_PUB /
T3+chul_09 만 격리하고 나머지(T1/T2_DIST/미분류)는 전체 합산(fail-open) — 공유 DB
에서 타사 정산 노출. 레거시 출판 빌드는 모든 공유 테이블 쿼리에 자사 Hcode(Hnnnn)
를 강제하므로 격리가 정본.

규칙(DEC-136):
- 공유 좌표(remote_153×chul_09)는 계정 유형 불문(슈퍼 제외) 본인 hcode 강제.
- 미분류(account_type·family 모두 없음) 계정도 격리.
- 격리 필요 + hcode 신뢰 불가(빈/'0000') → SCOPE_DENIED_HCODE(0건) — 전체 노출 금지.
- 단일 테넌트 좌표의 운영(T1/T2_DIST)·T3(비 chul_09)·슈퍼는 종전 그대로(DEC-085/090).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.core.hcode_isolation import (  # noqa: E402
    SCOPE_DENIED_HCODE,
    resolve_g7_ggeo_list_scope,
    resolve_publisher_row_scope,
)


def _ctx(**kw) -> dict:
    base = {"user_id": "u1", "role": "operator", "permissions": []}
    base.update(kw)
    return base


class SharedDbCoordTests(TestCase):
    """remote_153×chul_09 — 계정 유형 불문 격리."""

    def test_kyomunsa_like_account_forced_to_own_hcode(self) -> None:
        # 교문사류: 공유 좌표 + (분류가 무엇이든) → 본인 hcode. 요청 필터도 무시.
        for acct in ("", "T1", "T2_DIST", "T3", "T2_PUB"):
            ctx = _ctx(server_id="remote_153", account_family="chul_09",
                       account_type=acct, hcode="1234")
            self.assertEqual(resolve_g7_ggeo_list_scope(ctx), "1234", acct)
            self.assertEqual(resolve_publisher_row_scope("9999", ctx), "1234", acct)

    def test_shared_coord_without_hcode_denied(self) -> None:
        # hcode 빈값 → fail-closed(0건). ('0000' 은 _is_super_ctx 레거시 규약상
        # 슈퍼로 간주되어 이 함수에 도달 전 전체 허용 — DEC-136 잔여 리스크로 기록,
        # 공유 서버에 0000 비밀번호 로그인 실재 여부는 운영 점검 항목.)
        ctx = _ctx(server_id="remote_153", account_family="chul_09",
                   account_type="T1", hcode="")
        self.assertEqual(resolve_g7_ggeo_list_scope(ctx), SCOPE_DENIED_HCODE)

    def test_super_still_broad_on_shared_coord(self) -> None:
        ctx = _ctx(server_id="remote_153", account_family="chul_09",
                   account_type="T1", hcode="1234", role="admin")
        self.assertIsNone(resolve_g7_ggeo_list_scope(ctx))


class UnclassifiedFailClosedTests(TestCase):
    """미분류(account_type·family 모두 없음) — fail-closed."""

    def test_unclassified_with_hcode_forced_to_own(self) -> None:
        ctx = _ctx(server_id="remote_1", hcode="5019")
        self.assertEqual(resolve_g7_ggeo_list_scope(ctx), "5019")

    def test_unclassified_without_hcode_denied_not_broad(self) -> None:
        ctx = _ctx(server_id="remote_1")
        self.assertEqual(resolve_g7_ggeo_list_scope(ctx), SCOPE_DENIED_HCODE)

    def test_sentinel_yields_zero_rows_semantics(self) -> None:
        # sentinel 은 실존 hcode 와 절대 충돌하지 않는 형태여야 한다.
        self.assertTrue(SCOPE_DENIED_HCODE.startswith("__"))
        self.assertNotEqual(SCOPE_DENIED_HCODE, "0000")


class PreservedBehaviorTests(TestCase):
    """DEC-085/090 종전 동작 보존 — 단일 테넌트 좌표."""

    def test_t1_single_tenant_coord_broad(self) -> None:
        # 위러브1(remote_154×chul_09 단독) 류 — 운영 전체 합산 유지.
        ctx = _ctx(server_id="remote_154", account_family="chul_09",
                   account_type="T1", hcode="5019")
        self.assertIsNone(resolve_g7_ggeo_list_scope(ctx))
        self.assertIsNone(resolve_publisher_row_scope(None, ctx))

    def test_t2_dist_passthrough_filter(self) -> None:
        ctx = _ctx(server_id="remote_138", account_family="book_kb",
                   account_type="T2_DIST", hcode="5019")
        self.assertEqual(resolve_publisher_row_scope("P001", ctx), "P001")

    def test_t2_pub_forced_anywhere(self) -> None:
        ctx = _ctx(server_id="remote_138", account_family="book_kb",
                   account_type="T2_PUB", hcode="P777")
        self.assertEqual(resolve_publisher_row_scope("P001", ctx), "P777")

    def test_t3_chul09_family_isolated_regardless_of_server(self) -> None:
        ctx = _ctx(server_id="remote_154", account_family="chul_09",
                   account_type="T3", hcode="7777")
        self.assertEqual(resolve_g7_ggeo_list_scope(ctx), "7777")


if __name__ == "__main__":
    main()
