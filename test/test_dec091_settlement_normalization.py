"""DEC-091 — 정산관리 정비 회귀 가드.

검증 축
------
1) 월키 정규화(DEC-085 확대): 정산 조회 SQL 은 레거시 점 표기 월('2026.07')과 웹
   6자리('202607')를 모두 매칭하는 정규화 키를 쓴다. 단, 쓰기 키(마감/확정/취소)는
   원시 'YYYYMM' 그대로(레거시 행 오매칭 방지).
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


class WriteKeysStayRawTests(TestCase):
    """DEC-085 주의 — 쓰기 키는 원시 'YYYYMM' 그대로(정규화 금지)."""

    def test_check_yesno_raw(self) -> None:
        self.assertIn("WHERE Gdate=%s AND Hcode=%s", ss._SQL_CHECK_YESNO)
        self.assertNotIn(_NORM, ss._SQL_CHECK_YESNO)

    def test_confirm_cancel_raw(self) -> None:
        self.assertIn("WHERE Gdate=%s AND Hcode=%s", ss._SQL_CONFIRM_BILLING)
        self.assertIn("WHERE Gdate=%s AND Hcode=%s", ss._SQL_CANCEL_BILLING)
        self.assertNotIn(_NORM, ss._SQL_CONFIRM_BILLING)
        self.assertNotIn(_NORM, ss._SQL_CANCEL_BILLING)


class OutstandingSqlTests(IsolatedAsyncioTestCase):
    """미수 청구(T2)/입금(T5) SQL 캡처 — Yesno 없음 + 청구측 월키 정규화."""

    async def test_no_yesno_and_billed_month_key(self) -> None:
        captured: list[str] = []

        async def fake_execute(server_id, sql, params=()):  # noqa: ARG001
            captured.append(sql)
            if sql.strip().upper().startswith("SHOW COLUMNS"):
                return [{"Field": "Gdate"}, {"Field": "Hcode"}, {"Field": "Gssum"}]
            return []

        with patch.object(ss, "execute_query", side_effect=fake_execute):
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

        with patch.object(ss, "execute_query", side_effect=fake_execute):
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
