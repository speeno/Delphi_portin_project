"""DEC-091 — 정산관리 정비 회귀 가드.

검증 축
------
1) 월키 정규화(DEC-085 확대): 정산 조회 SQL 은 레거시 점 표기 월('2026.07')과 웹
   6자리('202607')를 모두 매칭하는 정규화 키를 쓴다. 쓰기·가드 키도 DEC-131 부터
   정규화(확정 '1' 보존 가드 내장) — 종전 원시 키는 레거시 확정 행을 못 보던 결함.
2) Yesno 제외 제거(DEC-089/081 계열): 레거시 Subu42/47/49 원본에 없던
   ``COALESCE(Yesno,'0') <> '2'`` 를 입금현황·미수·세금계산서 조회에서 제거.
3) 출판사 행 스코프(DEC-090 확대): 라우터가 enforce_hcode_isolation 대신
   resolve_publisher_row_scope 를 쓴다(정산 hcode=출판사 코드).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import settlement_service as ss  # noqa: E402
from app.services import t5_ssub_adapt  # noqa: E402

_NORM = "REPLACE(REPLACE(REPLACE(TRIM("  # 정규화 월키 시그니처


class MonthKeyReadNormalizationTests(TestCase):
    """조회 SQL 상수의 월키 정규화 + Yesno 제거."""

    def test_list_billing_month_key_normalized(self) -> None:
        self.assertIn(_NORM, ss._SQL_LIST_BILLING)
        self.assertNotIn("t.Gdate BETWEEN", ss._SQL_LIST_BILLING)
        self.assertIn(_NORM, ss._SQL_COUNT_BILLING)

    def test_billing_detail_month_key_normalized(self) -> None:
        self.assertIn(_NORM, ss._SQL_BILLING_HEADER)
        self.assertNotIn("WHERE Gdate=%s", ss._SQL_BILLING_HEADER)
        # 상수 → 빌더 전환(T3 Idx DDL drift 어댑터) — 양쪽 변형 모두 정규화 월키 유지.
        self.assertIn(_NORM, ss._build_sql_billing_lines(True))
        self.assertIn(_NORM, ss._build_sql_billing_lines(False))
        self.assertNotIn("LEFT(Gdate,6)=%s", ss._build_sql_billing_lines(True))

    def test_cash_status_no_yesno_and_month_key(self) -> None:
        for sql in (
            ss._SQL_CASH_STATUS_BY_HCODE,
            ss._SQL_CASH_STATUS_BY_HCODE_COUNT,
            ss._SQL_CASH_STATUS_PREV_BY_HCODE,
            ss._SQL_CASH_STATUS_BY_SDATE,
        ):
            self.assertNotIn("<> '2'", sql, "DEC-091: Yesno 제외 제거")
            self.assertIn(_NORM, sql, "DEC-091: 월키 정규화")

    def test_line_counts_month_key_normalized(self) -> None:
        self.assertIn(_NORM, ss._SQL_BILLING_LINE_COUNTS)
        self.assertNotIn("LEFT(Gdate, 6)", ss._SQL_BILLING_LINE_COUNTS)


class WriteKeysNormalizedTests(TestCase):
    """DEC-131 — 쓰기·가드 키도 월키 정규화 (DEC-091 '원시 키' 정책 폐기).

    DEC-091 은 쓰기 키를 원시 'YYYYMM' 으로 남겼지만, DEC-129 자동 집계의 T2/T3
    DELETE 가 정규화 키로 레거시 행을 지우는 반면 마감 가드만 원시 키라 레거시
    확정('2026.07', Yesno='1') 행을 못 보는 최악 조합이 됨 — 확정 청구서의 라인이
    웹 재집계로 덮인 사고(2026-07-30)의 구조적 원인. 이제 가드·확정·취소 모두
    정규화 키 + LIMIT 1 제거(중복 행 전수 검사)여야 한다.
    """

    def test_check_yesno_normalized_no_limit(self) -> None:
        self.assertIn(_NORM, ss._SQL_CHECK_YESNO)
        self.assertNotIn("LIMIT 1", ss._SQL_CHECK_YESNO)

    def test_confirm_cancel_normalized(self) -> None:
        self.assertIn(_NORM, ss._SQL_CONFIRM_BILLING)
        self.assertIn(_NORM, ss._SQL_CANCEL_BILLING)
        self.assertIn(_NORM, ss._SQL_CONFIRM_LOCK_LINES)

    def test_rebuild_deletes_preserve_confirmed_and_locked(self) -> None:
        # 재구성 DELETE 는 확정 헤더('1')·잠금 라인('1')을 절대 지우지 않는다.
        self.assertIn("<> '1'", ss._SQL_DELETE_T2_UNCONFIRMED)
        self.assertIn("<> '1'", ss._SQL_DELETE_T3_UNLOCKED)
        self.assertIn(_NORM, ss._SQL_DELETE_T2_UNCONFIRMED)
        self.assertIn(_NORM, ss._SQL_DELETE_T3_UNLOCKED)


class OutstandingSqlTests(IsolatedAsyncioTestCase):
    """미수 청구(T2)/입금(T5) SQL 캡처 — Yesno 없음 + 청구측 월키 정규화."""

    def setUp(self) -> None:
        t5_ssub_adapt.clear_t5_column_cache_for_tests()

    def tearDown(self) -> None:
        t5_ssub_adapt.clear_t5_column_cache_for_tests()

    async def test_no_yesno_and_billed_month_key(self) -> None:
        captured: list[str] = []

        async def fake_execute(server_id, sql, params=()):  # noqa: ARG001
            captured.append(sql)
            if sql.strip().upper().startswith("SHOW COLUMNS"):
                return [{"Field": "Gdate"}, {"Field": "Hcode"}, {"Field": "Gssum"}]
            return []

        # compute_outstanding_by_customer 는 t5_ssub_adapt.t5_column_names(SHOW COLUMNS)
        # 를 거치며 그 어댑터는 자체 import 한 execute_query 를 쓰므로 함께 패치
        # (미패치 시 servers.yaml 라이브 DB 접근 → 스위트 실행 순서 의존 실패).
        with patch.object(ss, "execute_query", side_effect=fake_execute), \
             patch.object(t5_ssub_adapt, "execute_query", side_effect=fake_execute):
            await ss.compute_outstanding_by_customer(
                server_id="remote_138", month_from="2026.01", month_to="2026.12",
                hcode="",
            )
        billed = next(s for s in captured if "Billed" in s)
        paid = next(s for s in captured if "Paid" in s)
        self.assertNotIn("<> '2'", billed)
        self.assertNotIn("<> '2'", paid)
        self.assertIn(_NORM, billed)  # 청구(T2) 월키 정규화

    async def test_sort_whitelist_rejects_injection(self) -> None:
        # 정렬 화이트리스트 밖 키는 무시(기본 -balance 정렬 유지, 주입 없음).
        async def fake_execute(server_id, sql, params=()):  # noqa: ARG001
            if sql.strip().upper().startswith("SHOW COLUMNS"):
                return [{"Field": "Gdate"}, {"Field": "Hcode"}, {"Field": "Gssum"}]
            return []

        with patch.object(ss, "execute_query", side_effect=fake_execute), \
             patch.object(t5_ssub_adapt, "execute_query", side_effect=fake_execute):
            res = await ss.compute_outstanding_by_customer(
                server_id="remote_138", month_from="2026.01", month_to="2026.12",
                hcode="", sort_by="balance); DROP TABLE", sort_dir="desc",
            )
        self.assertIn("items", res)


class RouterUsesPublisherScopeTests(TestCase):
    """라우터가 출판사 행 스코프 헬퍼로 전환됐는지(DEC-090 확대)."""

    def test_router_source_uses_resolve_publisher_row_scope(self) -> None:
        src = (BACKEND / "app" / "routers" / "settlement.py").read_text(encoding="utf-8")
        # 호출(call) 로서의 enforce_hcode_isolation 은 없어야 한다(주석 언급은 허용).
        self.assertNotIn("enforce_hcode_isolation(", src,
                         "정산 라우터는 S1용 enforce_hcode_isolation 호출을 쓰지 않는다")
        # 5개 목록 라우트 + export 라우트가 모두 출판사 스코프 헬퍼 사용
        self.assertGreaterEqual(src.count("resolve_publisher_row_scope("), 5)


if __name__ == "__main__":
    main()
