"""기간별 반품 내역서(Sobo58) + 기간별 재고원장(Sobo34_4) 회귀 가드.

증상
----
- ``GET /api/v1/returns/period-report`` 응답의 마스터 ``hname``
  (출판사명/거래처명) 이 항상 빈 문자열 — 사용자 보고:
  "기간별 반품 내역서 화면에 거래처명이 출력되지 않는다".
- ``GET /api/v1/returns/ledger`` 가 mysql3 호환 서버(예: ``remote_155``)
  에서 SQL 1064 → HTTP 500 — 사용자 보고: "기간별 재고원장 화면은 500 오류".

근본 원인
----------
1) ``SQL_PERIOD_MASTER`` 의 ``LEFT JOIN G1_Ggeo g ON g.Gcode=s.Hcode AND g.Hcode=''``
   이 잘못. G1_Ggeo 는 (Hcode, Gcode) 복합키 거래처 마스터 — Hcode 가 빈
   문자열인 row 가 거의 없어 매칭이 항상 NULL 이 되어 ``hname=''`` 회귀.
   레거시 ``Subu58.pas:376`` 은 ``Base10.G7_Ggeo.Locate('Gcode', Hcode)``
   로 출판사명을 G7_Ggeo (단일키 출판사 마스터) 에서 찾는다.
   동일 화면 ``SQL_LEDGER_MASTER`` (Sobo34_4) 도 ``LEFT JOIN G7_Ggeo``
   패턴이며, ``list_returns`` (Sobo23) 의 in_clause_lookup 도 G7_Ggeo
   ``WHERE Gcode IN (…)`` 으로 출판사명을 lookup 한다 — 단일 진실 원천.

2) ``SQL_LEDGER_MASTER_COUNT`` 가 ``SELECT COUNT(*) FROM (subquery) t``
   파생 테이블 패턴이라 mysql3_protocol 서버에서 1064 → HTTP 500 발생.
   DEC-033 (d) HOTFIX(2026-04-21) 가 이미 4 화면(C2/C3/C4/C6) 에 일반화
   적용한 ``sql_mysql3.count_grouped`` 헬퍼를 ``ledger_query`` 에서도
   사용해야 한다 (SOLID-O — 신규 패턴 0).

본 회귀 가드
-------------
A. ``SQL_PERIOD_MASTER`` 가 G7_Ggeo 를 사용하고, 직전 결함 패턴
   ``g.Hcode=''`` 가 정의 본문에 없음을 캡처.
B. ``SQL_PERIOD_MASTER`` 가 ``LEFT JOIN G7_Ggeo g ON g.Gcode=s.Hcode``
   1:1 패턴(Subu58.pas:376) 임을 명시 검증.
C. ``ledger_query`` 호출 시 ``count_grouped`` 가 1회 이상 호출되고,
   직접 ``execute_query`` 로 ``"SELECT COUNT(*) FROM ("`` 발행이 0 임을 검증.
D. ``period_report_query`` 가 ``hname`` 을 비어있지 않은 문자열로 채워
   응답에 포함시킴을 mock 결과로 검증.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


# ---------------------------------------------------------------
# A/B. SQL_PERIOD_MASTER — 정적 SQL 가드
# ---------------------------------------------------------------

class PeriodMasterSqlPublisherJoinTests(TestCase):
    def test_uses_g7_ggeo_not_g1_with_empty_hcode(self) -> None:
        from app.services import returns_service

        sql = returns_service.SQL_PERIOD_MASTER
        self.assertIn(
            "LEFT JOIN G7_Ggeo g ON g.Gcode=s.Hcode",
            sql,
            "Subu58.pas:376 의 출판사명 lookup 패턴(G7_Ggeo) 과 일치해야 함",
        )
        # 직전 결함 패턴이 다시 들어오는 회귀 차단.
        self.assertNotIn(
            "g.Hcode=''",
            sql,
            "g.Hcode='' 매칭은 항상 NULL → hname='' 회귀(기간별 반품 거래처명 누락)",
        )
        self.assertNotIn(
            "G1_Ggeo g ON g.Gcode=s.Hcode",
            sql,
            "G1_Ggeo (복합키 거래처 마스터) 는 Hcode lookup 용 아님 — G7_Ggeo 사용",
        )


# ---------------------------------------------------------------
# C. ledger_query — derived table 직접 발행 0 + count_grouped 사용
# ---------------------------------------------------------------

class LedgerMasterRowKeyShapeTests(IsolatedAsyncioTestCase):
    """frontend React key 합성용 ``scode`` 가 master 응답에 포함되어야 한다.

    원인
    ----
    레거시 ``Subu34_4.pas:404,406`` 의 ``Group By Bcode, Scode, Gubun, Pubun``
    4컬럼 분할을 보존하므로 동일 ``bcode`` 가 다중 row 로 등장한다.
    frontend 의 React ``key`` 합성 (``${bcode}|${scode}|${gubun}|${pubun}``)
    이 unique 하려면 응답에 ``scode`` 가 반드시 들어 있어야 한다 — 누락 시
    "Encountered two children with the same key" 콘솔 오류 회귀.
    """

    async def test_master_row_includes_scode_for_react_key(self) -> None:
        from app.services import returns_service

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                # 동일 Bcode + 다른 Scode/Gubun/Pubun → 분할 row.
                return [
                    {
                        "Bcode": "CP-018S", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                        "total_qty": 3, "total_amount": 3000,
                        "book_name": "도서A", "gname": "거래처A",
                    },
                    {
                        "Bcode": "CP-018S", "Scode": "Y", "Gubun": "재생", "Pubun": "낱권",
                        "total_qty": 2, "total_amount": 2000,
                        "book_name": "도서A", "gname": "거래처A",
                    },
                ]
            if "DISTINCT" in sql or "publisher_count" in sql:
                return [{"book_count": 1, "line_count": 5, "total_qty": 5, "total_amount": 5000}]
            return []

        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch(
                "app.services.returns_service.count_grouped",
                new=AsyncMock(return_value=2),
            ),
            patch(
                "app.services.returns_service.build_d_select_clause",
                new=AsyncMock(return_value=" 1=1 "),
            ),
        ):
            res = await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=10,
                offset=0,
            )

        self.assertEqual(len(res["master"]), 2)
        for row in res["master"]:
            self.assertIn("scode", row, "master row 에 scode 키가 없음 — React key 회귀")
        # frontend 합성 키가 실제로 unique 한지 직접 시뮬레이션.
        composed = {
            f"{r['bcode']}|{r['scode']}|{r['gubun']}|{r['pubun']}"
            for r in res["master"]
        }
        self.assertEqual(
            len(composed),
            len(res["master"]),
            "(bcode|scode|gubun|pubun) 합성 키가 중복 — React 'two children with same key' 회귀",
        )


class LedgerQueryUsesCountGroupedTests(IsolatedAsyncioTestCase):
    async def test_ledger_query_calls_count_grouped_no_derived_table(self) -> None:
        from app.services import returns_service

        ex_calls: list[tuple[str, str, tuple]] = []

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            ex_calls.append((server_id, sql, params))
            # master 페이지 1행 + KPI 1행 + (detail 미요청) — 형식만 맞추면 충분.
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                return [{
                    "Bcode": "B001", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                    "total_qty": 5, "total_amount": 5000, "book_name": "도서A", "gname": "거래처A",
                }]
            if "DISTINCT s.Bcode" in sql or "COUNT(DISTINCT" in sql:
                return [{"book_count": 1, "line_count": 5, "total_qty": 5, "total_amount": 5000}]
            return []

        cg_calls: list[dict[str, Any]] = []

        async def fake_count_grouped(server_id: str, **kw: Any) -> int:
            cg_calls.append({"server_id": server_id, **kw})
            return 1

        # KPI 분기 SQL 도 fake_execute 로 흡수되도록 build_d_select_clause 는 더미.
        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch("app.services.returns_service.count_grouped", new=fake_count_grouped),
            patch(
                "app.services.returns_service.build_d_select_clause",
                new=AsyncMock(return_value=" 1=1 "),
            ),
        ):
            res = await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=10,
                offset=0,
            )

        self.assertEqual(res["page"]["total"], 1)
        self.assertGreaterEqual(len(cg_calls), 1, "count_grouped 미호출 — derived 표면 회귀")
        # execute_query 어디에서도 derived 패턴이 발행되면 안 됨.
        for _sid, sql, _p in ex_calls:
            self.assertNotIn(
                "SELECT COUNT(*) AS total FROM (",
                sql,
                "ledger_query 가 직접 derived count SQL 발행 — DEC-033 (d) 위반",
            )

    def test_ledger_master_count_constants_are_clauses_not_full_sql(self) -> None:
        """SQL_LEDGER_MASTER_COUNT_WHERE / GROUP_BY 가 헬퍼 입력용 절(節) 형태 유지."""
        from app.services import returns_service

        where = returns_service.SQL_LEDGER_MASTER_COUNT_WHERE
        group_by = returns_service.SQL_LEDGER_MASTER_GROUP_BY
        # WHERE 키워드/SELECT 키워드 미포함 — count_grouped 입력 규약 준수.
        self.assertNotIn("SELECT", where.upper())
        self.assertNotIn(" WHERE ", where.upper())
        self.assertIn("{gubun_list}", where, "gubun IN 절 placeholder 유지 필요")
        self.assertIn("s.Bcode", group_by)


# ---------------------------------------------------------------
# D. period_report_query — hname 채워짐 (end-to-end mock)
# ---------------------------------------------------------------

class PeriodReportHnameFilledTests(IsolatedAsyncioTestCase):
    async def test_master_hname_is_populated_from_g7_ggeo(self) -> None:
        from app.services import returns_service

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "ORDER BY s.Hcode" in sql:
                # master — G7_Ggeo join 으로 hname 채워진 row.
                return [{
                    "Hcode": "H001", "hname": "출판사가나다",
                    "line_count": 3, "total_qty": 9, "total_amount": 9000,
                }]
            if "COUNT(DISTINCT s.Hcode)" in sql and "AS total" in sql:
                return [{"total": 1}]
            if "publisher_count" in sql:
                return [{"publisher_count": 1, "line_count": 3, "total_qty": 9, "total_amount": 9000}]
            return []

        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch(
                "app.services.returns_service.build_d_select_clause",
                new=AsyncMock(return_value=" 1=1 "),
            ),
        ):
            res = await returns_service.period_report_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=50,
                offset=0,
            )

        self.assertEqual(len(res["master"]), 1)
        self.assertEqual(res["master"][0]["hcode"], "H001")
        self.assertEqual(
            res["master"][0]["hname"],
            "출판사가나다",
            "G7_Ggeo lookup 결과가 hname 으로 전달되지 않음 — 거래처명 누락 회귀",
        )


if __name__ == "__main__":  # pragma: no cover
    main()
