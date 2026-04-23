"""
DEC-025 — 마스터 5 종 q 검색 회귀 가드 (master_data.yaml v1.2.0 정정).

목적
----
DEC-024 직후 추가된 마스터 list 5 종 (customer/book/publisher/book-code/
discount) 에서 한글/영문/공백 q 의 LIKE 패턴 생성과 ``execute_query``
호출 인자가 안정적으로 일관되는지 service 레벨에서 검증.

이력 (2026-04-23, v1.2.0): 구 「Sobo45 = 물류비」 매핑 추정 오류 정정으로
``logistics-cost`` 케이스 제거 (구 6 마스터 18 케이스 → 5 마스터 15 케이스).
배경은 master_data.yaml v1.2.0 changelog + DEC-019 보강 참조.

또한 ``app.core.db._escape_mysql3_value`` 의 정수 quote 버그 회귀 가드를
포함한다 — MySQL 3.x ``LIMIT 'N' OFFSET 'M'`` 에서 quoted string 거부 이슈
(DEC-025 root fix).

DB 미연결 — ``masters_service.execute_query`` 만 patch 하여 SQL/params 캡처.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core import db as core_db  # noqa: E402
from app.services import masters_service  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# 헬퍼 — 5개 list 함수 각각의 호출 시그니처 (v1.2.0 정정 — logistics-cost 제거)
# ─────────────────────────────────────────────────────────────────────────────

LIST_FUNCS = [
    ("customer", masters_service.list_customer_master),
    ("book", masters_service.list_books),
    ("publisher", masters_service.list_publishers),
    ("book-code", masters_service.list_book_codes),
    ("discount", masters_service.list_discounts),
]

Q_CASES = [
    ("empty", ""),
    ("ascii", "A0001"),
    ("korean", "도서"),
]


class _Capture:
    """execute_query 의 (sql, params) 호출을 순서대로 모아두는 stub."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        # COUNT 쿼리는 row_count 1행, SELECT 는 빈 row 리스트
        sql_upper = sql.upper()
        if "COUNT(*)" in sql_upper:
            return [{"row_count": 0}]
        return []


# ─────────────────────────────────────────────────────────────────────────────
# 15 케이스 매트릭스 (5 마스터 × 3 q; 구 6 마스터 18 케이스 → v1.2.0 정정)
# ─────────────────────────────────────────────────────────────────────────────


class MastersQSearchMatrix(TestCase):
    def _run_case(self, fn, q: str | None) -> _Capture:
        cap = _Capture()
        with patch.object(masters_service, "execute_query", new=cap):
            asyncio.run(fn(server_id="remote_1", q=q, limit=50, offset=0))
        return cap

    # --- 빈 q: WHERE 절 없어야 한다 ---
    def test_empty_q_no_like(self) -> None:
        for label, fn in LIST_FUNCS:
            with self.subTest(entity=label):
                cap = self._run_case(fn, "")
                self.assertEqual(len(cap.calls), 2, f"{label}: select+count 두 호출")
                select_sql, select_params = cap.calls[0]
                count_sql, count_params = cap.calls[1]
                self.assertNotIn("LIKE", select_sql.upper())
                self.assertNotIn("LIKE", count_sql.upper())
                # LIMIT/OFFSET 만 들어가므로 params 는 정확히 (limit, offset)
                self.assertEqual(select_params, (50, 0))
                self.assertEqual(count_params, ())

    # --- ASCII q: LIKE 포함 + 패턴 정확 일치 ---
    def test_ascii_q_likify(self) -> None:
        for label, fn in LIST_FUNCS:
            with self.subTest(entity=label):
                cap = self._run_case(fn, "A0001")
                select_sql, select_params = cap.calls[0]
                self.assertIn("LIKE", select_sql.upper())
                # 패턴이 양끝 % 부착 + literal 그대로
                self.assertIn("%A0001%", select_params)
                # 마지막 두 인자는 LIMIT/OFFSET
                self.assertEqual(select_params[-2:], (50, 0))

    # --- 한글 q: 패턴 그대로 전달 (인코딩은 db 계층 책임) ---
    def test_korean_q_likify(self) -> None:
        for label, fn in LIST_FUNCS:
            with self.subTest(entity=label):
                cap = self._run_case(fn, "도서")
                select_sql, select_params = cap.calls[0]
                self.assertIn("LIKE", select_sql.upper())
                self.assertIn("%도서%", select_params)


# ─────────────────────────────────────────────────────────────────────────────
# _likify 단위 — 와일드카드 escape / 공백 정규화
# ─────────────────────────────────────────────────────────────────────────────


class LikifyHelper(TestCase):
    def test_none_and_blank_returns_none(self) -> None:
        self.assertIsNone(masters_service._likify(None))
        self.assertIsNone(masters_service._likify(""))
        self.assertIsNone(masters_service._likify("   "))

    def test_escape_wildcards(self) -> None:
        # 사용자가 입력한 % / _ / \ 는 literal 로 매치되어야 한다.
        self.assertEqual(masters_service._likify("50%"), "%50\\%%")
        self.assertEqual(masters_service._likify("a_b"), "%a\\_b%")
        self.assertEqual(masters_service._likify("c\\d"), "%c\\\\d%")

    def test_korean_passthrough(self) -> None:
        self.assertEqual(masters_service._likify("도서"), "%도서%")


# ─────────────────────────────────────────────────────────────────────────────
# db._escape_mysql3_value — 정수 unquoted 회귀 가드 (DEC-025 root fix)
# ─────────────────────────────────────────────────────────────────────────────


class Mysql3EscapeIntUnquoted(TestCase):
    def test_int_is_unquoted(self) -> None:
        # MySQL 3.x LIMIT/OFFSET 은 quoted string 을 받지 않는다.
        self.assertEqual(core_db._escape_mysql3_value(0), "0")
        self.assertEqual(core_db._escape_mysql3_value(50), "50")
        self.assertEqual(core_db._escape_mysql3_value(-1), "-1")

    def test_bool_is_zero_or_one(self) -> None:
        self.assertEqual(core_db._escape_mysql3_value(True), "1")
        self.assertEqual(core_db._escape_mysql3_value(False), "0")

    def test_string_is_quoted(self) -> None:
        self.assertEqual(core_db._escape_mysql3_value("abc"), "'abc'")
        # single quote escape
        self.assertEqual(core_db._escape_mysql3_value("a'b"), "'a\\'b'")

    def test_none_is_null_literal(self) -> None:
        self.assertEqual(core_db._escape_mysql3_value(None), "NULL")

    def test_build_sql_limit_offset_unquoted(self) -> None:
        # 회귀 핵심: ``LIMIT %s OFFSET %s`` + (50, 0) → quote 없이 인라인
        sql = "SELECT 1 FROM t WHERE x LIKE %s LIMIT %s OFFSET %s"
        out = core_db._build_mysql3_sql(sql, ("%도서%", 50, 0))
        self.assertIn("LIKE '%도서%'", out)
        self.assertIn("LIMIT 50 OFFSET 0", out)
        self.assertNotIn("LIMIT '50'", out)
        self.assertNotIn("OFFSET '0'", out)


# ─────────────────────────────────────────────────────────────────────────────
# DEC-026 — PK 가드 회귀 (NULL/빈 PK row 노출 차단)
# ─────────────────────────────────────────────────────────────────────────────


class MasterPkGuard(TestCase):
    """``_build_master_where`` + 5 list 가 PK NULL/빈 row 를 자동 제외하는지 (v1.2.0)."""

    def test_pk_guard_in_all_list_sql_empty_q(self) -> None:
        for label, fn in LIST_FUNCS:
            with self.subTest(entity=label):
                cap = _Capture()
                with patch.object(masters_service, "execute_query", new=cap):
                    asyncio.run(fn(server_id="remote_1", q="", limit=50, offset=0))
                self.assertEqual(len(cap.calls), 2)
                for sql, _params in cap.calls:
                    self.assertIn("Gcode IS NOT NULL", sql, f"{label}: PK NULL guard")
                    self.assertIn("Gcode <> ''", sql, f"{label}: PK empty guard")

    def test_pk_guard_in_all_list_sql_with_q(self) -> None:
        for label, fn in LIST_FUNCS:
            with self.subTest(entity=label):
                cap = _Capture()
                with patch.object(masters_service, "execute_query", new=cap):
                    asyncio.run(fn(server_id="remote_1", q="A0001", limit=50, offset=0))
                for sql, _params in cap.calls:
                    self.assertIn("Gcode IS NOT NULL", sql, f"{label}: PK guard with q")
                    self.assertIn("Gcode <> ''", sql, f"{label}: PK empty guard with q")
                # 첫 호출(SELECT)은 PK guard + LIKE 결합 → AND 연산자 존재
                select_sql, _ = cap.calls[0]
                self.assertIn("AND", select_sql)
                self.assertIn("LIKE", select_sql.upper())

    def test_build_master_where_no_pattern(self) -> None:
        clause, params = masters_service._build_master_where(None)
        self.assertEqual(clause, " WHERE Gcode IS NOT NULL AND Gcode <> ''")
        self.assertEqual(params, [])

    def test_build_master_where_with_pattern_default_cols(self) -> None:
        clause, params = masters_service._build_master_where("%abc%")
        self.assertEqual(
            clause,
            " WHERE Gcode IS NOT NULL AND Gcode <> '' AND (Gcode LIKE %s OR Gname LIKE %s)",
        )
        self.assertEqual(params, ["%abc%", "%abc%"])

    def test_build_master_where_with_pattern_custom_cols(self) -> None:
        clause, params = masters_service._build_master_where(
            "%isbn%", search_cols=("Gcode", "Gname", "COALESCE(Gisbn,'')")
        )
        self.assertIn("COALESCE(Gisbn,'') LIKE %s", clause)
        self.assertEqual(len(params), 3)


# ─────────────────────────────────────────────────────────────────────────────
# v1.2.0 정정 회귀 가드 — 「Sobo45 = 물류비」 매핑 부재 단언
# ─────────────────────────────────────────────────────────────────────────────


class LogisticsCostMappingRemovedTests(TestCase):
    """master_data.yaml v1.2.0 정정 회귀 가드.

    근본 원인 : v1.0.0 (2026-04-18) 가 G5_Ggeo.Gposa 컬럼만 보고 「Sobo45 = 물류비」
    로 추정. 실제 레거시 Subu45.dfm Caption='청구서관리' (Sobo45_billing 으로 별도
    정상 등록). 본 가드는 동일 추정 오류가 다음 사이클에서 재유입되지 않도록 5축
    (서비스 함수 / 모델 / 라우트 / 프론트 페이지 / 계약 catalog) 부재를 단언.
    사용자 룰 — 일반화 해결 (특정 케이스가 아닌 5축 모두 보호).
    """

    def test_service_function_removed(self) -> None:
        self.assertFalse(
            hasattr(masters_service, "list_logistics_costs"),
            "masters_service.list_logistics_costs 가 재유입되었다 — v1.2.0 정정 회귀.",
        )

    def test_model_class_removed(self) -> None:
        from app.models import master as master_models

        self.assertFalse(
            hasattr(master_models, "LogisticsCostListResponse"),
            "models.master.LogisticsCostListResponse 가 재유입되었다 — v1.2.0 정정 회귀.",
        )
        self.assertFalse(
            hasattr(master_models, "LogisticsCostListItem"),
            "models.master.LogisticsCostListItem 가 재유입되었다 — v1.2.0 정정 회귀.",
        )

    def test_router_path_removed(self) -> None:
        from app.routers import masters as masters_router

        for route in masters_router.router.routes:
            path = getattr(route, "path", "")
            self.assertNotIn(
                "logistics-cost",
                path,
                f"GET {path} 가 재유입되었다 — v1.2.0 정정 회귀.",
            )

    def test_frontend_page_removed(self) -> None:
        page_path = (
            ROOT
            / "도서물류관리프로그램"
            / "frontend"
            / "src"
            / "app"
            / "(app)"
            / "master"
            / "logistics-cost"
            / "page.tsx"
        )
        self.assertFalse(
            page_path.exists(),
            f"{page_path} 가 재생성되었다 — v1.2.0 정정 회귀.",
        )

    def test_contract_catalog_no_logistics_cost(self) -> None:
        contract_path = ROOT / "migration" / "contracts" / "master_data.yaml"
        body = contract_path.read_text(encoding="utf-8")
        # endpoint 정의가 다시 들어왔는지 검사 — 주석/changelog 의 단순 언급은 통과해야 하므로
        # endpoint 블록 내 path 라인만 ``path: /api/v1/masters/logistics-cost`` 로 검출.
        self.assertNotIn(
            "path: /api/v1/masters/logistics-cost",
            body,
            "master_data.yaml 에 SQL-MAS-10 endpoint 가 재유입되었다 — v1.2.0 정정 회귀.",
        )
        self.assertNotIn(
            "schema_ref: backend/app/models/master.py#LogisticsCostListResponse",
            body,
            "master_data.yaml 에 LogisticsCostListResponse 참조가 재유입되었다 — v1.2.0 정정 회귀.",
        )


if __name__ == "__main__":
    main()
