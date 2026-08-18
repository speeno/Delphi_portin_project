"""DEC-169 — 도서명 목록 정가/ISBN 공통 컬럼 (GROUP 1: 보고서/통계/재고) 회귀 가드.

``book_meta_lookup.attach_book_meta`` 를 목록 SQL 과 분리해(JOIN 금지) 결과 행에
``gisbn``(+``gdang`` 폴백) 을 부착하는지 — 서비스 3종을 DB 무의존(mock)으로 확인.

- reports_service.get_customer_sales_detail  (거래처판매 하단 도서별 상세, bcode 키)
- customer_txn_ledger_service.customer_ledger_slip_detail (거래처원장 전표 상세 — price 보존)
- stats_service.get_book_turnover (get_book_sales 재사용 → 회전율 항목에 gdang/gisbn 전파)
- 라우터 엑셀 컬럼 카탈로그(도서별판매/년말집계/회전율)에 ISBN·정가가 도서명 바로 뒤에 있는지
"""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, patch

from app.services import book_meta_lookup as bml
from app.services import customer_txn_ledger_service as txn
from app.services import reports_service as rs
from app.services import stats_service as ss

_G4 = {
    "B1": {"bcode": "B1", "gname": "도서일", "gdang": 15000, "gisbn": "9788900000011"},
    "B2": {"bcode": "B2", "gname": "도서이", "gdang": 0, "gisbn": "9788900000028"},
}


async def _fake_meta_lookup(server_id, *, sql_template, keys, prefix_params=(), **_):
    return [dict(_G4[k]) for k in keys if k in _G4]


async def _fake_col_meta(server_id):
    return {"gcode", "gname", "gdang", "gisbn"}, {
        "gcode": "Gcode", "gname": "Gname", "gdang": "Gdang", "gisbn": "Gisbn"
    }


def _meta_patches():
    return (
        patch.object(bml, "in_clause_lookup", _fake_meta_lookup),
        patch.object(bml, "g4_book_column_meta", _fake_col_meta),
    )


class CustomerSalesDetailMetaTest(unittest.IsolatedAsyncioTestCase):
    async def test_detail_rows_carry_gisbn_and_gdang(self):
        s1_rows = [
            {"Bcode": "B1", "Gubun": "출고", "Pubun": "", "Gsqut": 3, "Gssum": 30000},
            {"Bcode": "B2", "Gubun": "반품", "Pubun": "", "Gsqut": -1, "Gssum": -5000},
        ]

        async def fake_exec(server_id, sql, params=None):
            return s1_rows

        async def fake_names(server_id, *, sql_template, keys, **_):
            return [{"bcode": k, "gname": _G4[k]["gname"]} for k in keys if k in _G4]

        p1, p2 = _meta_patches()
        with patch.object(rs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(rs, "in_clause_lookup", fake_names), p1, p2:
            res = await rs.get_customer_sales_detail(
                server_id="remote_1", hcode="5019",
                date_from="2026-01-01", date_to="2026-01-31", gcode="1015",
            )

        rows = {r["bcode"]: r for r in res["rows"]}
        self.assertEqual(rows["B1"]["gisbn"], "9788900000011")
        self.assertEqual(rows["B1"]["gdang"], 15000)
        self.assertEqual(rows["B2"]["gisbn"], "9788900000028")
        self.assertEqual(rows["B2"]["gdang"], 0)
        # 기존 필드(도서명·합계) 회귀 없음
        self.assertEqual(rows["B1"]["bname"], "도서일")
        self.assertEqual(res["totals"]["goqut"], 3)


class CustomerLedgerSlipDetailMetaTest(unittest.IsolatedAsyncioTestCase):
    async def test_slip_detail_items_carry_gisbn_and_keep_price(self):
        s1_rows = [
            {"Gdate": "2026.02.20", "Gubun": "출고", "Pubun": "", "Bcode": "B1",
             "Gbigo": "", "Gjisa": "", "Jubun": "11", "grat1": 80, "qty": 2, "amt": 24000},
        ]

        async def fake_query(server_id, sql, params=None):
            if "FROM S1_Ssub" in sql:
                return s1_rows
            if "FROM G4_Book" in sql:
                # 전표 상세의 기존 정가 lookup — 마스터 정가(12000)가 그대로 price 로 남아야 한다.
                return [{"Gcode": "B1", "Gname": "도서일", "gdang": 12000}]
            return []

        p1, p2 = _meta_patches()
        with patch.object(txn, "execute_query", AsyncMock(side_effect=fake_query)), p1, p2:
            res = await txn.customer_ledger_slip_detail(
                server_id="remote_1", hcode="5019", gcode="1015", gdate="2026-02-20",
                jubun="11", gjisa="", kind=1, opening=1000,
            )

        self.assertEqual(len(res["items"]), 1)
        it = res["items"][0]
        self.assertEqual(it["gisbn"], "9788900000011")
        self.assertEqual(it["price"], 12000)  # price_key=None → 기존 단가 보존
        self.assertEqual(it["bcode"], "B1")
        self.assertEqual(it["balance"], 1000 + 24000)


class BookTurnoverMetaPropagationTest(unittest.IsolatedAsyncioTestCase):
    async def test_turnover_items_carry_gdang_gisbn_from_book_sales(self):
        async def fake_book_sales(**kwargs):
            return {
                "rows": [{"gcode": "B1", "gname": "도서일", "gdang": 15000,
                          "gisbn": "9788900000011", "giqut": 10, "goqut": 5,
                          "gbqut": 0, "gjqut": 0, "gpqut": 0, "gdate": "2026.01.05"}],
                "total": 1,
            }

        with patch.object(ss.reports_service, "get_book_sales", side_effect=fake_book_sales):
            res = await ss.get_book_turnover(
                server_id="remote_1", hcode="5019",
                date_from="2026-01-01", date_to="2026-01-31",
            )
        item = res["items"][0]
        self.assertEqual(item["gisbn"], "9788900000011")
        self.assertEqual(item["gdang"], 15000)
        self.assertEqual(item["turnover_ratio"], 0.5)


class ExportColumnCatalogTest(unittest.TestCase):
    def _assert_after_name(self, columns, name_key="gname"):
        keys = [k for _, k in columns]
        i = keys.index(name_key)
        self.assertEqual(keys[i + 1], "gisbn", keys)
        self.assertEqual(keys[i + 2], "gdang", keys)
        labels = dict((k, lb) for lb, k in columns)
        self.assertEqual(labels["gisbn"], "ISBN")
        self.assertEqual(labels["gdang"], "정가")

    def test_reports_and_stats_export_columns(self):
        from app.routers.reports import _BOOK_SALES_EXPORT_COLUMNS, _YEAR_END_EXPORT_COLUMNS
        from app.routers.stats import _BOOK_TURNOVER_EXPORT_COLUMNS

        self._assert_after_name(_BOOK_SALES_EXPORT_COLUMNS)
        self._assert_after_name(_YEAR_END_EXPORT_COLUMNS)
        self._assert_after_name(_BOOK_TURNOVER_EXPORT_COLUMNS)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
