"""출고현황(Subu24 거래현황) 서비스 — 가벼운 단위 회귀.

목적
----
신규 출고현황 서비스 3종의 **SQL 빌드 + 상태 매핑**을 실 DB 없이 검증한다.
DB 경계는 ``execute_query`` / ``count_grouped`` / ``in_clause_lookup`` /
``fetch_g1_customer_gnames`` / ``s1_column_names`` / ``g4_column_names`` 를
monkeypatch 로 막아 캡처한 SQL 과 변환된 dict 만 본다(라우터/계약 검증은
``test_outbound_status_subu24.py`` 가 담당 — 본 파일은 서비스 내부 SQL 빌드 보강).

대상
----
- ``list_outbound_status_slips``  : 전표 GROUP BY master 목록 + count_grouped total.
- ``list_outbound_status_lines``  : 원시 라인 + 도서명 + 합계(totals), DDL drift 컬럼 흡수.
- ``outbound_status_customer_rollup`` : 거래처별 IF()-조건합 + 거래처명 매핑.

검증 축
-------
1. SQL 골격(FROM S1_Ssub / GROUP BY / ORDER BY / Gubun 범위 / Scode='X' /
   storeKind→Ocode / hcode 격리 / LIMIT) 과 mysql3 호환(파생테이블/CASE/COALESCE 부재).
2. 상태 매핑 = ``_line_status_from_yesno_max`` ('1'·'2'→done, '0'→received, 그외→pending).
3. 바인딩 파라미터 순서(Gdate 정규화 → 필터 → LIMIT/OFFSET) 와 합계/total 전파.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import transactions_service as tx  # noqa: E402

DATE_FROM = "2026-04-01"
DATE_TO = "2026-04-30"
# _normalize_gdate('YYYY-MM-DD') → 'YYYY.MM.DD' (S1_Ssub.Gdate 포맷)
G_FROM = "2026.04.01"
G_TO = "2026.04.30"


def _no_mysql3_no_case_no_derived(test, sql: str) -> None:
    """mysql3 호환 가드 — 파생테이블/CASE/COALESCE 미사용(DEC-033)."""
    test.assertNotIn("FROM (", sql)
    test.assertNotIn("CASE", sql)
    test.assertNotIn("COALESCE", sql)


class SlipsSqlTests(IsolatedAsyncioTestCase):
    """list_outbound_status_slips — 전표 GROUP BY + 상태/거래처명 매핑."""

    async def test_slips_sql_build_status_mapping_and_total(self) -> None:
        captured: list[tuple] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append((server_id, sql, params))
            # yesno_max 별 상태 매핑 커버: '2'→done, '0'→received, ''→pending
            return [
                {"gdate": "2026.04.18", "hcode": "H0001", "jubun": "11",
                 "gcode": "00001", "item_count": 3, "qty": 30, "amount": 300000,
                 "gbigo": "메모", "yesno_max": "2"},
                {"gdate": "2026.04.17", "hcode": "H0001", "jubun": "12",
                 "gcode": "00002", "item_count": 1, "qty": 5, "amount": 50000,
                 "gbigo": "", "yesno_max": "0"},
                {"gdate": "2026.04.16", "hcode": "H0001", "jubun": "13",
                 "gcode": "00003", "item_count": 2, "qty": 8, "amount": 80000,
                 "gbigo": "", "yesno_max": ""},
            ]

        cg = AsyncMock(return_value=42)
        gnames = AsyncMock(return_value={("H0001", "00001"): "교보문고"})

        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "count_grouped", cg), \
                patch("app.services.s1_ssub_adapt.s1_column_names",
                      AsyncMock(return_value={"idnum"})), \
                patch.object(tx, "fetch_g1_customer_gnames", gnames):
            items, total = await tx.list_outbound_status_slips(
                server_id="remote_1", date_from=DATE_FROM, date_to=DATE_TO,
                hcode="H0001", store_kind="A", limit=10, offset=5,
            )

        # --- total 전파 = count_grouped 결과 ---
        self.assertEqual(total, 42)
        self.assertEqual(len(items), 3)

        # --- SQL 골격 ---
        _, sql, params = captured[0]
        self.assertIn("FROM S1_Ssub", sql)
        self.assertIn("GROUP BY Gdate, Hcode, IFNULL(Jubun,''), Gcode", sql)
        self.assertIn("ORDER BY Gdate DESC", sql)
        self.assertIn("Gubun = '출고'", sql)
        self.assertIn("Scode = 'X'", sql)
        self.assertIn("Ocode = %s", sql)   # storeKind A → 본사
        self.assertIn("Hcode = %s", sql)   # 멀티테넌트 격리
        self.assertIn("LIMIT %s OFFSET %s", sql)
        _no_mysql3_no_case_no_derived(self, sql)

        # --- 바인딩 순서: Gdate 정규화 → Ocode → Hcode → (limit, offset) ---
        self.assertEqual(params[0], G_FROM)
        self.assertEqual(params[1], G_TO)
        self.assertIn("A", params)        # Ocode 값(본사)
        self.assertIn("H0001", params)    # 격리 hcode
        self.assertEqual(tuple(params[-2:]), (10, 5))  # remote_1 비-mysql3 → (limit, offset)

        # --- 상태 매핑 ---
        self.assertEqual([it["status"] for it in items], ["done", "received", "pending"])

        # --- 거래처명 매핑(G1_Ggeo 배치) ---
        self.assertEqual(items[0]["customer_name"], "교보문고")
        self.assertEqual(items[0]["order_key"],
                         {"gdate": "2026.04.18", "hcode": "H0001", "jubun": "11", "gcode": "00001"})

        # --- count_grouped 가 동일 테이블/그룹으로 호출(파생테이블 우회) ---
        cg.assert_awaited_once()
        ckw = cg.await_args.kwargs
        self.assertEqual(ckw["table"], "S1_Ssub")
        self.assertEqual(ckw["group_by"], "Gdate, Hcode, IFNULL(Jubun,''), Gcode")
        self.assertIn("Gubun = '출고'", ckw["where_sql"])

    async def test_slips_store_kind_all_omits_ocode(self) -> None:
        captured: list[str] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            return []

        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "count_grouped", AsyncMock(return_value=0)), \
                patch("app.services.s1_ssub_adapt.s1_column_names",
                      AsyncMock(return_value={"idnum"})), \
                patch.object(tx, "fetch_g1_customer_gnames", AsyncMock(return_value={})):
            items, total = await tx.list_outbound_status_slips(
                server_id="remote_1", date_from=DATE_FROM, date_to=DATE_TO,
                store_kind="ALL",
            )
        self.assertEqual((items, total), ([], 0))
        self.assertNotIn("Ocode", captured[0])     # ALL → 본사/창고 합산(Ocode 미부착)
        self.assertNotIn("Hcode = %s", captured[0])  # hcode 미지정(슈퍼) → 격리 절 없음


class LinesSqlTests(IsolatedAsyncioTestCase):
    """list_outbound_status_lines — 원시 라인 + 도서명(in_clause_lookup) + totals."""

    async def test_lines_sql_status_mapping_bname_and_totals(self) -> None:
        calls: list[tuple] = []

        async def fake_exec(server_id, sql, params=()):
            calls.append((sql, params))
            if "COUNT(*) AS cnt" in sql:  # 합계 쿼리
                return [{"cnt": 2, "qty": 13, "amount": 700000, "hcode": "H0001"}]
            return [  # 라인 쿼리 — yesno '2'→done, '0'→received
                {"gdate": "2026.04.18", "hcode": "H0001", "jubun": "11",
                 "gcode": "00001", "bcode": "B1", "pubun": "위탁", "gsqut": 10,
                 "gdang": 10000, "grat1": 70.0, "gssum": 700000, "gbigo": "",
                 "yesno": "2"},
                {"gdate": "2026.04.19", "hcode": "H0001", "jubun": "",
                 "gcode": "00001", "bcode": "B1", "pubun": "증정", "gsqut": 3,
                 "gdang": 0, "grat1": 0, "gssum": 0, "gbigo": "x", "yesno": "0"},
            ]

        # 도서명 경로: _fetch_outbound_book_names → _fetch_product_names →
        # _fetch_book_line_meta(g4_column_names + in_clause_lookup) 를 모킹.
        book_rows = AsyncMock(return_value=[{"bcode": "B1", "gname": "도서A", "shelf": ""}])
        s1cols = AsyncMock(return_value={"gdang", "grat1", "pubun"})
        g4cols = AsyncMock(return_value={"gcode", "gname"})
        # 거래처명 lookup(G1_Ggeo) — 목록 JOIN 금지 원칙의 런타임 채움 (2026-07-03 추가).
        cust_names = AsyncMock(return_value={("H0001", "00001"): "북센"})

        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "in_clause_lookup", book_rows), \
                patch.object(tx, "fetch_g1_customer_gnames", cust_names), \
                patch("app.services.s1_ssub_adapt.s1_column_names", s1cols), \
                patch("app.services.g4_book_adapt.g4_column_names", g4cols):
            lines, total, totals = await tx.list_outbound_status_lines(
                server_id="remote_1", date_from=DATE_FROM, date_to=DATE_TO,
                hcode="H0001", store_kind="B", limit=10, offset=0,
            )

        # --- 라인 쿼리 SQL ---
        line_sql = next(s for s, _ in calls if "COUNT(*) AS cnt" not in s)
        self.assertIn("FROM S1_Ssub", line_sql)
        self.assertIn("ORDER BY Gdate, IFNULL(Jubun,'')", line_sql)
        self.assertIn("Gubun = '출고'", line_sql)
        self.assertIn("Scode = 'X'", line_sql)
        self.assertIn("Ocode = %s", line_sql)   # storeKind B → 창고
        self.assertIn("LIMIT %s OFFSET %s", line_sql)
        # 테넌트 컬럼 존재 → 실 컬럼 셀렉트
        self.assertIn("IFNULL(Gdang,0) AS gdang", line_sql)
        self.assertIn("IFNULL(Grat1,0) AS grat1", line_sql)
        self.assertIn("IFNULL(Pubun,'') AS pubun", line_sql)
        _no_mysql3_no_case_no_derived(self, line_sql)

        # --- 합계 쿼리(단일 집계, LIMIT 없음, 파생테이블 없음) ---
        agg_sql = next(s for s, _ in calls if "COUNT(*) AS cnt" in s)
        self.assertIn("IFNULL(SUM(Gsqut),0) AS qty", agg_sql)
        self.assertIn("IFNULL(SUM(Gssum),0) AS amount", agg_sql)
        self.assertIn("MAX(Hcode) AS hcode", agg_sql)
        self.assertNotIn("LIMIT", agg_sql)
        self.assertNotIn("FROM (", agg_sql)

        # --- 결과 전파 ---
        self.assertEqual(total, 2)
        self.assertEqual(totals, {"qty": 13, "amount": 700000})
        self.assertEqual(len(lines), 2)

        # --- 상태 매핑 + 도서명 + 수치 타입 ---
        self.assertEqual([ln["status"] for ln in lines], ["done", "received"])
        self.assertEqual(lines[0]["bname"], "도서A")
        self.assertEqual(lines[0]["gdang"], 10000)
        self.assertIsInstance(lines[0]["grat1"], float)
        self.assertEqual(lines[0]["grat1"], 70.0)

    async def test_lines_ddl_drift_columns_absent_use_literals(self) -> None:
        """테넌트 컬럼(Gdang/Grat1/Pubun) 부재 → 리터럴 셀렉트(서비스층 if 없음)."""
        captured: list[str] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            if "COUNT(*) AS cnt" in sql:
                return [{"cnt": 0, "qty": 0, "amount": 0, "hcode": "H0001"}]
            return []

        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "in_clause_lookup", AsyncMock(return_value=[])), \
                patch("app.services.s1_ssub_adapt.s1_column_names",
                      AsyncMock(return_value=set())), \
                patch("app.services.g4_book_adapt.g4_column_names",
                      AsyncMock(return_value=set())):
            lines, total, totals = await tx.list_outbound_status_lines(
                server_id="remote_1", date_from=DATE_FROM, date_to=DATE_TO,
                hcode="H0001",
            )
        line_sql = next(s for s in captured if "COUNT(*) AS cnt" not in s)
        self.assertIn("0 AS gdang", line_sql)
        self.assertIn("0 AS grat1", line_sql)
        self.assertIn("'' AS pubun", line_sql)
        self.assertEqual((lines, total, totals), ([], 0, {"qty": 0, "amount": 0}))


class RollupSqlTests(IsolatedAsyncioTestCase):
    """outbound_status_customer_rollup — IF()-조건합 행 → dict + 거래처명."""

    async def test_rollup_row_transform_scope_and_customer_name(self) -> None:
        captured: list[str] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            return [{
                "gcode": "00001", "hcode": "H0001",
                "out_qty": 10, "out_amount": 700000, "gift_qty": 0,
                "return_qty": -2, "return_amount": -140000,
                "sales_qty": 8, "sales_amount": 560000,
            }]

        gnames = AsyncMock(return_value={("H0001", "00001"): "교보문고"})

        with patch.object(tx, "execute_query", side_effect=fake_exec), \
                patch.object(tx, "fetch_g1_customer_gnames", gnames):
            rows = await tx.outbound_status_customer_rollup(
                server_id="remote_1", date_from=DATE_FROM, date_to=DATE_TO,
                hcode="H0001", store_kind="B",
            )

        # --- 반품 포함 범위 + GROUP BY + 격리 정합 ---
        sql = captured[0]
        self.assertIn("Gubun IN ('출고','반품')", sql)
        self.assertIn("GROUP BY Gcode", sql)
        self.assertIn("MAX(Hcode) AS hcode", sql)
        self.assertIn("Ocode = %s", sql)  # storeKind B → 창고
        _no_mysql3_no_case_no_derived(self, sql)

        # --- 행 변환(부호 컨벤션: 반품 음수합) + 거래처명 ---
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(
            set(r.keys()),
            {"gcode", "customer_name", "out_qty", "out_amount", "gift_qty",
             "return_qty", "return_amount", "sales_qty", "sales_amount"},
        )
        self.assertEqual(r["customer_name"], "교보문고")
        self.assertEqual(r["return_qty"], -2)
        self.assertEqual(r["return_amount"], -140000)
        self.assertEqual(r["sales_qty"], 8)
        self.assertEqual(r["sales_amount"], 560000)


if __name__ == "__main__":
    main()
