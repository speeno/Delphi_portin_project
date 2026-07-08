"""tax-invoice ``Chek3``/``Sdate``/``Yesno`` 동적 SELECT 회귀 가드 (DEC-058 Wave B).

배경 — 변형사 DB 호환
-------------------
``remote_152`` 등 일부 변형사 DB 의 ``T2_Ssub`` 에는 ``Chek3``, ``Sdate``,
``Yesno`` 컬럼이 없다. 고정 SQL ``COALESCE(t.Chek3,'0')`` 사용 시
``OperationalError 1054 (Unknown column)`` → HTTP 500 으로 정산 화면이
완전히 막혔다.

해결 — ``_t2_columns`` 어댑터 + ``_build_sql_list_tax`` 동적 SELECT.
컬럼 존재 시 기존 표현식, 부재 시 정적 리터럴(``'0' AS Chek3``).

본 테스트는 ``t5_ssub_adapt`` 의 회귀 가드 패턴(서버별 컬럼 존재/부재 분기)
을 ``T2_Ssub`` 에 동일 적용 — 사용자 룰의 일반화 정신.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.services.tax_invoice_service import (  # noqa: E402
    _build_sql_count_tax,
    _build_sql_list_tax,
    _build_sql_print_row,
    clear_t2_column_cache_for_tests,
)


class TaxInvoiceChek3OptionalTest(TestCase):
    """``T2_Ssub`` 의 선택 컬럼 부재 시에도 SQL 이 정상 빌드되는지 검증."""

    def setUp(self) -> None:
        clear_t2_column_cache_for_tests()

    def test_full_columns_uses_coalesce(self) -> None:
        """모든 선택 컬럼 존재 → 기존 ``COALESCE(...)`` SELECT 표현식 유지."""
        cols = {"hcode", "sum26", "sum27", "sum28", "chek3", "sdate", "yesno", "gdate"}
        sql = _build_sql_list_tax(cols)
        self.assertIn("COALESCE(t.Chek3,'0') AS Chek3", sql)
        self.assertIn("COALESCE(t.Sdate,'') AS Sdate", sql)
        self.assertIn("COALESCE(t.Yesno,'0') AS Yesno", sql)
        # DEC-091 — 레거시 Subu49 는 WHERE 에 Yesno 절이 없다. 웹이 추가했던 마감
        # 제외(<> '2')가 실데이터를 전부 제외하던 회귀 → 조회 SQL 에서 제거.
        self.assertNotIn("<> '2'", sql, "DEC-091: Yesno 마감 제외 제거(레거시 무 Yesno)")
        # 월키 정규화(레거시 점 표기 '2026.07' 매칭) — 원시 t.Gdate=%s 금지.
        self.assertNotIn("t.Gdate = %s", sql)
        self.assertIn("REPLACE(REPLACE(REPLACE(TRIM(t.Gdate)", sql)

    def test_chek3_missing_uses_literal(self) -> None:
        """``Chek3`` 부재 → ``'0' AS Chek3`` 정적 리터럴, 1054 회피."""
        cols = {"hcode", "sum26", "sum27", "sum28", "sdate", "yesno", "gdate"}
        sql = _build_sql_list_tax(cols)
        self.assertNotIn("COALESCE(t.Chek3", sql)
        self.assertIn("'0' AS Chek3", sql)
        # alias 순서 보존 (응답 모델 호환)
        self.assertLess(sql.index("Chek3"), sql.index("Sdate"))

    def test_sdate_missing_uses_literal(self) -> None:
        cols = {"hcode", "sum26", "sum27", "sum28", "chek3", "yesno", "gdate"}
        sql = _build_sql_list_tax(cols)
        self.assertNotIn("COALESCE(t.Sdate", sql)
        self.assertIn("'' AS Sdate", sql)

    def test_yesno_missing_drops_where_filter(self) -> None:
        """``Yesno`` 부재 → SELECT 는 리터럴, WHERE 절의 마감 제외 조건도 제거."""
        cols = {"hcode", "sum26", "sum27", "sum28", "chek3", "sdate", "gdate"}
        sql = _build_sql_list_tax(cols)
        self.assertIn("'0' AS Yesno", sql)
        self.assertNotIn("Yesno", sql.split("ORDER BY")[0].split("AS Yesno")[1] if "AS Yesno" in sql else sql)
        # COUNT 쿼리도 동일 — Yesno 컬럼 부재 시 COALESCE(Yesno,...) 미등장
        sql_cnt = _build_sql_count_tax(cols)
        self.assertNotIn("COALESCE(Yesno", sql_cnt)

    def test_count_sql_no_yesno_filter_and_month_key(self) -> None:
        """DEC-091 — COUNT 도 Yesno 절 없음 + 월키 정규화."""
        cols = {"hcode", "sum27", "yesno", "gdate"}
        sql_cnt = _build_sql_count_tax(cols)
        self.assertNotIn("<> '2'", sql_cnt)
        self.assertNotIn("Gdate = %s", sql_cnt)
        self.assertIn("REPLACE(REPLACE(REPLACE(TRIM(Gdate)", sql_cnt)

    def test_all_optional_missing_no_unknown_column(self) -> None:
        """3개 선택 컬럼 모두 부재 — 1054 유발 컬럼 참조가 SQL 안에 없어야."""
        cols = {"hcode", "sum26", "sum27", "sum28", "gdate"}
        sql = _build_sql_list_tax(cols)
        for missing in ("t.Chek3", "t.Sdate", "t.Yesno"):
            self.assertNotIn(
                missing, sql,
                f"{missing} 가 SQL 에 잔존 — 1054 (Unknown column) 회귀 위험",
            )

    def test_print_row_sql_matches_list_adapter(self) -> None:
        """인쇄 1행 SELECT 도 목록과 동일하게 선택 컬럼 부재 시 리터럴만 사용."""
        cols_full = {
            "hcode", "sum26", "sum27", "sum28", "chek3", "sdate", "yesno", "gdate",
        }
        sql_f = _build_sql_print_row(cols_full)
        self.assertIn("COALESCE(t.Chek3,'0') AS Chek3", sql_f)
        # DEC-091 — 인쇄 1행도 월키 정규화(원시 t.Gdate=%s 금지).
        self.assertNotIn("WHERE t.Gdate=%s", sql_f)
        self.assertIn("REPLACE(REPLACE(REPLACE(TRIM(t.Gdate)", sql_f)
        self.assertIn("AND t.Hcode=%s", sql_f)

        cols_min = {"hcode", "sum26", "sum27", "sum28", "gdate"}
        sql_m = _build_sql_print_row(cols_min)
        self.assertIn("'0' AS Chek3", sql_m)
        self.assertNotIn("t.Chek3", sql_m)
        self.assertNotIn("t.Sdate", sql_m)
        self.assertNotIn("t.Yesno", sql_m)


if __name__ == "__main__":
    main()
