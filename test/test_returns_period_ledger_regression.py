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
    """v1.2.0 (PLAN-LDG-INV-DETAIL-2026-04-23 / DEC-033 e/g) 회귀 가드.

    변경 (2026-04-23)
    -----------------
    이전(v1.1.0) 가드는 ``count_grouped`` 호출을 강제했다(derived table SQL 우회).
    v1.2.0 페이저 표준은 ``LIMIT+1`` + ``_slice_with_has_more`` 으로 전환되어
    ``count_grouped`` 자체를 호출하지 않는다(R1 — 6컬럼 GROUP BY + JOIN 다중
    환경에서 mysql3 30s+ 타임아웃 회귀 차단). 본 테스트의 핵심 의도(``derived
    table SQL 직접 발행 0건``)는 v1.2.0 에서도 그대로 유효 — count_grouped 사용
    강제만 해제하고, derived SQL 0건 검증과 LIMIT+1 페이저 사용을 가드한다.
    """

    async def test_ledger_query_no_derived_table_and_uses_limit_plus_one(self) -> None:
        from app.services import returns_service

        ex_calls: list[tuple[str, str, tuple]] = []

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            ex_calls.append((server_id, sql, params))
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                return [{
                    "Bcode": "B001", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                    "Hcode": "H001",
                    "total_qty": 5, "total_amount": 5000,
                }]
            if "COUNT(DISTINCT" in sql:
                return [{"book_count": 1, "line_count": 5, "total_qty": 5, "total_amount": 5000}]
            return []

        # v1.2.0: count_grouped 는 호출되어선 안 됨(R1 — LIMIT+1 표준). 호출 시 즉시 실패.
        async def forbidden_count_grouped(*_a: Any, **_kw: Any) -> int:
            raise AssertionError(
                "count_grouped 가 호출됨 — v1.2.0 표준은 LIMIT+1 (R1 회귀)"
            )

        # _fetch_*_names 는 in_clause_lookup 청크 룩업이라 빈 dict 로 충분.
        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch("app.services.returns_service.count_grouped", new=forbidden_count_grouped),
            patch(
                "app.services.returns_service.build_d_select_clause",
                new=AsyncMock(return_value=" 1=1 "),
            ),
            patch(
                "app.services.returns_service._fetch_product_names",
                new=AsyncMock(return_value={"B001": "도서A"}),
            ),
            patch(
                "app.services.returns_service._fetch_publisher_names",
                new=AsyncMock(return_value={"H001": "출판사A"}),
            ),
        ):
            res = await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=10,
                offset=0,
            )

        # ceiling pagination — visible=1 + has_more=False ⇒ total=1.
        self.assertEqual(res["page"]["total"], 1)
        self.assertIn("has_more", res["page"], "v1.2.0 응답에 has_more 키 필요")
        self.assertFalse(res["page"]["has_more"])
        # execute_query 어디에서도 derived 패턴 발행 0건(DEC-033 (d) 가드 유지).
        for _sid, sql, _p in ex_calls:
            self.assertNotIn(
                "SELECT COUNT(*) AS total FROM (",
                sql,
                "ledger_query 가 직접 derived count SQL 발행 — DEC-033 (d) 위반",
            )
        # LIMIT+1 검증 — 메인 페이지 SQL 의 LIMIT 바인드 셋에 limit+1=11 포함.
        # mysql3 바인딩 순서는 (offset, limit) 라 마지막 두 값이 (0, 11) 또는 (11, 0).
        # 표준 MySQL 은 (11, 0). 어느 쪽이든 마지막 2개 셋에 11 이 들어 있어야 R3 PASS.
        master_calls = [c for c in ex_calls if "GROUP BY s.Bcode" in c[1]]
        self.assertEqual(len(master_calls), 1, "메인 페이지 SQL 발행 1회 기대")
        params = master_calls[0][2]
        last_two = {params[-2], params[-1]}
        self.assertIn(
            11, last_two,
            "LIMIT 바인딩 셋에 limit+1(=11) 미포함 — R3 회귀(LIMIT+1 페이저 미적용)",
        )
        self.assertIn(0, last_two, "OFFSET 바인딩 누락")

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


# ---------------------------------------------------------------
# E. v1.2.0 신규 가드 (PLAN-LDG-INV-DETAIL-2026-04-23 / DEC-033 e/g)
# ---------------------------------------------------------------

class LedgerMasterNoJoinSqlTests(TestCase):
    """R2: SQL_LEDGER_MASTER_NOJOIN 이 메인 SQL 에서 JOIN 0개 임을 검증.

    배경: mysql3 호환 서버에서 6컬럼 GROUP BY + 다중 LEFT JOIN 조합은
    Sobo54/57 v1.2.0~v1.2.1 에서 30s+ 타임아웃 회귀를 일으켰다. 본 화면도
    같은 표준(Sobo54/57 v1.2.2)을 일반화 적용 — 도서명/출판사명은 페이지
    행 단위 ``in_clause_lookup`` 청크 룩업으로 분리한다.
    """

    def test_no_join_keyword_in_main_sql(self) -> None:
        from app.services import returns_service

        sql = returns_service.SQL_LEDGER_MASTER_NOJOIN
        self.assertNotIn(" JOIN ", sql.upper(),
                         "메인 SQL 에 JOIN 키워드 — R2 회귀(JOIN 0개 표준)")
        self.assertNotIn("LEFT JOIN", sql.upper())
        # GROUP BY 에 Hcode 포함 — JOIN 제거 후 단일 Hcode 필터 동등성 보존.
        self.assertIn("s.Hcode", sql)
        # 회귀 가드 호환: 기존 정적 매처 토큰 보존 (test_master_row_includes_scode_for_react_key 등).
        self.assertIn("GROUP BY s.Bcode", sql)
        self.assertIn("ORDER BY s.Bcode", sql)
        self.assertIn("LIMIT %s OFFSET %s", sql)


class LedgerSummaryFirstPageOnlyTests(IsolatedAsyncioTestCase):
    """R4: ``summary`` 는 ``offset==0`` 일 때만 백엔드가 산출.

    후속 페이지에서는 0 placeholder 를 반환하여 KPI SQL 추가 호출을 피한다
    (프론트의 ``totalsCache`` 가 첫 페이지 응답을 보존). KPI SQL 이 후속 페이지에서
    실행되면 페이지마다 비싼 COUNT(DISTINCT) 가 반복되어 회귀.
    """

    async def _run_with_offset(self, offset: int) -> tuple[dict[str, Any], list[str]]:
        from app.services import returns_service

        seen_sqls: list[str] = []

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            seen_sqls.append(sql)
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                return []
            if "COUNT(DISTINCT" in sql:
                return [{"book_count": 9, "line_count": 9, "total_qty": 9, "total_amount": 9000}]
            return []

        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch("app.services.returns_service.count_grouped",
                  new=AsyncMock(side_effect=AssertionError("R1 회귀 — count_grouped 호출"))),
            patch("app.services.returns_service.build_d_select_clause",
                  new=AsyncMock(return_value=" 1=1 ")),
            patch("app.services.returns_service._fetch_product_names",
                  new=AsyncMock(return_value={})),
            patch("app.services.returns_service._fetch_publisher_names",
                  new=AsyncMock(return_value={})),
        ):
            res = await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=10,
                offset=offset,
            )
        return res, seen_sqls

    async def test_summary_populated_when_offset_zero(self) -> None:
        res, sqls = await self._run_with_offset(0)
        self.assertIn("summary", res)
        self.assertEqual(res["summary"]["book_count"], 9,
                         "offset=0 응답에 summary 미산출 — R4 회귀")
        # KPI SQL 이 첫 페이지에서는 발행되어야 함.
        self.assertTrue(
            any("COUNT(DISTINCT" in s for s in sqls),
            "offset=0 인데 KPI SQL 미발행 — summary 산출 누락",
        )
        # kpi 키 deprecation 호환 윈도우 — summary 와 동일 값.
        self.assertEqual(res["kpi"], res["summary"])

    async def test_summary_zero_when_offset_nonzero(self) -> None:
        res, sqls = await self._run_with_offset(20)
        self.assertEqual(res["summary"]["book_count"], 0)
        self.assertEqual(res["summary"]["line_count"], 0)
        self.assertEqual(res["summary"]["total_qty"], 0)
        self.assertEqual(res["summary"]["total_amount"], 0)
        # KPI SQL 은 후속 페이지에서 발행되면 안 됨 — 회귀 시 페이지당 비싼 COUNT 반복.
        self.assertFalse(
            any("COUNT(DISTINCT" in s for s in sqls),
            "offset>0 에서 KPI SQL 발행 — R4 회귀(후속 페이지 KPI 비용 누설)",
        )


class LedgerLookupChunkedTests(IsolatedAsyncioTestCase):
    """R5: 도서명/출판사명은 ``_fetch_*`` 청크 룩업으로 호출되며,
    호출 인자는 페이지 행에서 추출한 distinct 코드 셋 (소트된 list).
    """

    async def test_fetch_lookups_called_with_page_distinct_codes(self) -> None:
        from app.services import returns_service

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                return [
                    {"Bcode": "B002", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                     "Hcode": "H001", "total_qty": 1, "total_amount": 100},
                    {"Bcode": "B001", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                     "Hcode": "H002", "total_qty": 2, "total_amount": 200},
                    # B001 중복 — distinct 처리 검증.
                    {"Bcode": "B001", "Scode": "Y", "Gubun": "재생", "Pubun": "낱권",
                     "Hcode": "H001", "total_qty": 3, "total_amount": 300},
                ]
            if "COUNT(DISTINCT" in sql:
                return [{"book_count": 2, "line_count": 6, "total_qty": 6, "total_amount": 600}]
            return []

        product_mock = AsyncMock(return_value={"B001": "도서1", "B002": "도서2"})
        publisher_mock = AsyncMock(return_value={"H001": "출판사1", "H002": "출판사2"})

        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch("app.services.returns_service.count_grouped",
                  new=AsyncMock(side_effect=AssertionError("R1 회귀"))),
            patch("app.services.returns_service.build_d_select_clause",
                  new=AsyncMock(return_value=" 1=1 ")),
            patch("app.services.returns_service._fetch_product_names", new=product_mock),
            patch("app.services.returns_service._fetch_publisher_names", new=publisher_mock),
        ):
            res = await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                limit=10,
                offset=0,
            )

        # 1) 청크 룩업이 호출되었는가?
        self.assertEqual(product_mock.await_count, 1, "_fetch_product_names 미호출 — R2 회귀")
        self.assertEqual(publisher_mock.await_count, 1, "_fetch_publisher_names 미호출 — R2 회귀")
        # 2) 인자가 distinct + sorted bcode/hcode 셋인가?
        bcodes = list(product_mock.await_args.args[1])
        hcodes = list(publisher_mock.await_args.args[1])
        self.assertEqual(bcodes, ["B001", "B002"])
        self.assertEqual(hcodes, ["H001", "H002"])
        # 3) 응답 row 의 book_name/gname 이 룩업 결과로 채워지는가?
        names = {(r["bcode"], r["gname"]) for r in res["master"]}
        self.assertIn(("B001", "출판사2"), names)  # 첫 B001 row → H002
        self.assertIn(("B002", "출판사1"), names)  # B002 row → H001

    async def test_fetch_publisher_uses_filter_hcode_when_provided(self) -> None:
        """단일 Hcode 필터 시(레거시 Subu34_4.pas:396) 룩업 인자도 그 1개만."""
        from app.services import returns_service

        async def fake_execute(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql:
                return [
                    {"Bcode": "B001", "Scode": "X", "Gubun": "반품", "Pubun": "구간",
                     "Hcode": "H001", "total_qty": 1, "total_amount": 100},
                ]
            if "COUNT(DISTINCT" in sql:
                return [{"book_count": 1, "line_count": 1, "total_qty": 1, "total_amount": 100}]
            return []

        publisher_mock = AsyncMock(return_value={"H_FILTER": "필터출판사"})

        with (
            patch("app.services.returns_service.execute_query", new=fake_execute),
            patch("app.services.returns_service.count_grouped",
                  new=AsyncMock(side_effect=AssertionError("R1"))),
            patch("app.services.returns_service.build_d_select_clause",
                  new=AsyncMock(return_value=" 1=1 ")),
            patch("app.services.returns_service._fetch_product_names",
                  new=AsyncMock(return_value={})),
            patch("app.services.returns_service._fetch_publisher_names",
                  new=publisher_mock),
        ):
            await returns_service.ledger_query(
                server_id="remote_155",
                date_from="2026-03-01",
                date_to="2026-04-01",
                hcode="H_FILTER",
                limit=10,
                offset=0,
            )

        hcodes = list(publisher_mock.await_args.args[1])
        self.assertEqual(hcodes, ["H_FILTER"],
                         "단일 Hcode 필터 시 룩업 인자도 동일해야 함(불필요 코드 누출 방지)")


class LedgerRouterErrorMessageTests(IsolatedAsyncioTestCase):
    """R6: 라우터 500 응답에 예외 클래스명 포함 — 회귀 진단 시간 단축."""

    async def test_router_500_includes_exception_class_name(self) -> None:
        from fastapi import HTTPException
        from app.routers import returns as returns_router

        # _user_context 가 request.headers 를 읽으므로 빈 dict 헤더 mock 필요.
        class _StubReq:
            headers: dict[str, str] = {}
        stub_req = _StubReq()

        async def boom(**_kw: Any) -> Any:
            raise RuntimeError("simulated mysql3 1064")

        with patch.object(returns_router.returns_service, "ledger_query", side_effect=boom):
            with self.assertRaises(HTTPException) as cm:
                await returns_router.get_returns_ledger(
                    request=stub_req,  # type: ignore[arg-type]
                    server_id="remote_155",
                    date_from="2026-03-01",
                    date_to="2026-04-01",
                    hcode=None,
                    bcode=None,
                    detail_for_bcode=None,
                    gubun=None,
                    limit=100,
                    offset=0,
                    _user=object(),
                )
        exc = cm.exception
        self.assertEqual(exc.status_code, 500)
        self.assertIn("RuntimeError", str(exc.detail),
                      "500 detail 에 예외 클래스명 누락 — R6 회귀(진단 가독성)")
        self.assertIn("simulated mysql3 1064", str(exc.detail))


class LedgerFormRegistryPermissionTests(TestCase):
    """R7: form-registry.ts Sobo34_4 권한 키가 inventory.read (조회 전용)."""

    def test_form_registry_uses_inventory_read(self) -> None:
        registry_path = (
            ROOT
            / "도서물류관리프로그램"
            / "frontend"
            / "src"
            / "lib"
            / "form-registry.ts"
        )
        text = registry_path.read_text(encoding="utf-8")
        # Sobo34_4 블록 추출 (다음 객체 시작 전까지).
        idx = text.find('id: "Sobo34_4"')
        self.assertGreater(idx, 0, "form-registry 에 Sobo34_4 항목 없음")
        block = text[idx: idx + 1200]
        self.assertIn('requiredPermission: "inventory.read"', block,
                      "Sobo34_4 권한 키가 inventory.read 가 아님 — R7 회귀(쓰기 권한 강제)")
        self.assertIn('phase: "phase1"', block,
                      "Sobo34_4 phase1 승격 미반영 — T8 회귀")


if __name__ == "__main__":  # pragma: no cover
    main()
