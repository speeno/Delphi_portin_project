"""DEC-094 — 청구서 인쇄(미리보기, Sobo46) 복구 회귀 가드.

근본 원인 3종 (레거시 Subu46.pas L648-655/L781-787 대조):
1) 정적 헤더 SELECT 가 Sum38/Sum39 포함 — 레거시 원문은 Sum01~37+Sum40~48(38/39
   건너뜀 = 컬럼 부재) → 1054 → 전 서버 500.
2) `WHERE Gdate=%s` 원시 비교 — 레거시 T2.Gdate 점 표기('2026.07') → 404.
3) 라인 `LEFT(Gdate,6)` — 점 표기 전체일자에서 '2026.0' → 라인 0건.

수정: _t2_columns(SHOW COLUMNS 캐시, DEC-058) 동적 SELECT + _t2_month_key 정규화.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import settlement_print_service as ps  # noqa: E402
from app.services import tax_invoice_service as tx  # noqa: E402

_NORM = "REPLACE(REPLACE(REPLACE(TRIM(Gdate)"

# 레거시 운영 T2 형태 — Sum38/39/Sdate/Chek3 부재.
_LEGACY_COLS = {
    *(f"sum{n:02d}" for n in (*range(1, 38), *range(40, 49), *range(51, 60), *range(61, 70))),
    "gdate", "hcode", "gsusu", "vdate", "bigo1", "bigo2", "yesno",
}


class HeaderSqlBuilderTests(TestCase):
    def test_absent_sum38_39_become_literals(self) -> None:
        sql = ps._build_sql_print_header(set(_LEGACY_COLS))
        select_part = sql.split("FROM")[0]
        self.assertIn("0 AS Sum38", select_part, "부재 컬럼은 리터럴 alias")
        self.assertIn("0 AS Sum39", select_part)
        self.assertIn("IFNULL(Sum26,0) AS Sum26", select_part, "존재 컬럼은 IFNULL")
        self.assertIn("'' AS Sdate", select_part)
        self.assertIn("'' AS Chek3", select_part)

    def test_where_uses_normalized_month_key(self) -> None:
        sql = ps._build_sql_print_header(set(_LEGACY_COLS))
        self.assertIn(_NORM, sql)
        self.assertNotIn("WHERE Gdate=%s", sql, "원시 Gdate 비교 금지(점 표기 404)")

    def test_lines_sql_normalized(self) -> None:
        self.assertIn(_NORM, ps._SQL_PRINT_LINES)
        self.assertNotIn("LEFT(Gdate,6)", ps._SQL_PRINT_LINES)


class GetPrintDataTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        tx.clear_t2_column_cache_for_tests()

    def tearDown(self) -> None:
        tx.clear_t2_column_cache_for_tests()

    async def test_legacy_shape_returns_full_schema(self) -> None:
        """레거시 형태(점 표기·Sum38/39 부재)에서 200 + 67개 sum 키 전부 직렬화."""
        async def fake(server_id, sql, params=()):  # noqa: ARG001
            up = sql.strip().upper()
            if up.startswith("SHOW COLUMNS"):
                return [{"Field": c.capitalize() if not c.startswith("sum") else f"Sum{c[3:]}"}
                        for c in _LEGACY_COLS]
            if "FROM T2_SSUB" in up:
                return [{"Sum26": 100, "Sum27": 10, "Sum28": 110, "Sum38": 0, "Sum39": 0,
                         "Gsusu": 50, "Vdate": "", "Bigo1": "", "Bigo2": "",
                         "Sdate": "", "Chek3": "", "Yesno": "1"}]
            if "FROM G7_GGEO" in up:
                return [{"Hname": "가출판", "Bname": "", "Gadd1": "", "Gadd2": "", "Gtel1": ""}]
            if "FROM T3_SSUB" in up:
                return [{"Idx": 1, "Gdate": "2026.07.15", "Gqut1": 1, "Gqut2": 0, "Gqut3": 0,
                         "Gqut4": 0, "Gqut5": 1, "Gqut6": 0, "Gqut7": 0, "Name1": "서울",
                         "Name2": "", "Gname": "가서점", "Gcode": "C01", "Gsqut": 1,
                         "Gssum": 3000, "Yesno": "0"}]
            return []

        # _t2_columns 는 tax 모듈 전역 execute_query 를 쓰므로 양쪽 모두 패치(밀폐형).
        with patch.object(ps, "execute_query", side_effect=fake), \
             patch.object(tx, "execute_query", side_effect=fake):
            data = await ps.get_print_data(
                server_id="remote_138", gdate="2026.07", hcode="P001",
            )
        # 방어적 정규화: 'YYYY.MM' 입력 → 'YYYYMM' 키.
        self.assertEqual(data["billing_key"]["gdate"], "202607")
        # 67개 sum 키 스키마 보존(부재 컬럼 → 0).
        self.assertEqual(data["summary"]["sum38"], 0)
        self.assertEqual(data["summary"]["sum28"], 110)
        self.assertEqual(len(data["lines"]), 1)
        self.assertEqual(data["status"]["yesno"], "1")

    async def test_not_found_raises_404_error(self) -> None:
        async def fake(server_id, sql, params=()):  # noqa: ARG001
            if sql.strip().upper().startswith("SHOW COLUMNS"):
                return [{"Field": "Gdate"}, {"Field": "Hcode"}, {"Field": "Sum26"}]
            return []

        with patch.object(ps, "execute_query", side_effect=fake), \
             patch.object(tx, "execute_query", side_effect=fake):
            with self.assertRaises(ps.PrintDataNotFoundError):
                await ps.get_print_data(
                    server_id="remote_138", gdate="202607", hcode="NOPE",
                )


if __name__ == "__main__":
    main()
