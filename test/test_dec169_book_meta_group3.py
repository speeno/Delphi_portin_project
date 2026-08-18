"""DEC-169 GROUP 3(반품) — 도서명 목록에 ISBN(gisbn)·정가(gdang) 공통 부착 회귀 가드.

- 반품재고 후보 목록(``list_inventory_candidates``): 행에 단가가 없으므로 마스터 정가(gdang)
  + ISBN(gisbn) 을 ``attach_book_meta`` 로 부착한다(목록 SQL JOIN 금지 — 후처리).
- 기간별재고원장 상세(``ledger_query`` detail): 단일 도서(detail_for_bcode) 라인에
  ``bcode`` 를 실어 정가·ISBN 을 부착한다.
- 기간별재고원장 마스터(``ledger_query`` master, 도서별 누계): 상세와 동일 hcode 로직으로
  ``gisbn`` + 마스터 정가(``gdang``) 를 부착한다(마스터 행엔 단가가 없음).
- 반품 상세 라인(``get_return_detail``): 전표 단가(Gdang) 는 보존하고 ISBN 만 채운다.
- 부착 실패는 목록을 500 으로 만들지 않고 ``gisbn=''`` 로 fail-soft.
- 바코드 스캔 매칭(``scan_match_service.match_barcode``): resolved 에 ``gisbn`` 을 실어
  입고/반품 스캔 draft 라인의 read-only ISBN 셀이 저장 전에도 채워지게 한다.
"""
from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, patch

from app.services import returns_service as svc
from app.services import scan_match_service as scan_svc


class InventoryCandidatesBookMetaTests(unittest.IsolatedAsyncioTestCase):
    async def test_candidates_rows_carry_gisbn_and_master_gdang(self) -> None:
        captured: list[tuple] = []

        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            if sql.strip().upper().startswith("SELECT COUNT("):
                return [{"total": 2}]
            return [
                {"id": 7, "Gdate": "2026.07.01", "Hcode": "5019", "Jubun": "0001",
                 "Bcode": "B0001", "gsqut": 3, "gbigo": ""},
                {"id": 8, "Gdate": "2026.07.02", "Hcode": "5019", "Jubun": "0002",
                 "Bcode": "B0002", "gsqut": 1, "gbigo": ""},
            ]

        async def fake_attach(server_id, hcode, rows, *, bcode_key="bcode",
                              price_key="gdang", isbn_key="gisbn", name_key=None,
                              overwrite_price=False):
            captured.append((server_id, hcode, bcode_key, price_key))
            meta = {"B0001": ("978-89-0001", 15000)}
            for r in rows:
                m = meta.get(r.get(bcode_key))
                r[isbn_key] = m[0] if m else ""
                if price_key and not r.get(price_key):
                    r[price_key] = m[1] if m else 0
            return rows

        with patch.object(svc, "execute_query", side_effect=fake_exec), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={"B0001": "책"})), \
             patch.object(svc, "attach_book_meta", side_effect=fake_attach):
            res = await svc.list_inventory_candidates(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019",
            )

        items = res["items"]
        self.assertEqual(len(items), 2)
        # ISBN 은 모든 행에 존재(미존재 코드는 빈 문자열), 정가는 마스터에서 보충.
        self.assertEqual(items[0]["gisbn"], "978-89-0001")
        self.assertEqual(items[0]["gdang"], 15000)
        self.assertEqual(items[1]["gisbn"], "")
        self.assertEqual(items[1]["gdang"], 0)
        # 로그인 스코프 hcode 로 한 번에 조회(테넌트 격리 유지), bcode 키·정가 키 표준.
        self.assertEqual(captured, [("remote_138", "5019", "bcode", "gdang")])
        # 기존 컬럼(도서명·수량·행 id) 은 그대로.
        self.assertEqual(items[0]["bname"], "책")
        self.assertEqual(items[0]["id"], 7)

    async def test_candidates_attach_failure_is_fail_soft(self) -> None:
        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            if sql.strip().upper().startswith("SELECT COUNT("):
                return [{"total": 1}]
            return [{"id": 1, "Gdate": "2026.07.01", "Hcode": "5019", "Jubun": "0001",
                     "Bcode": "B0001", "gsqut": 3, "gbigo": ""}]

        with patch.object(svc, "execute_query", side_effect=fake_exec), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={})), \
             patch.object(svc, "attach_book_meta", new=AsyncMock(side_effect=RuntimeError("db down"))):
            res = await svc.list_inventory_candidates(
                server_id="remote_138", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019",
            )
        self.assertEqual(res["items"][0]["gisbn"], "")
        self.assertEqual(res["items"][0]["gdang"], 0)
        self.assertEqual(res["items"][0]["gsqut"], 3)


class LedgerDetailBookMetaTests(unittest.IsolatedAsyncioTestCase):
    async def test_ledger_detail_rows_carry_bcode_gdang_gisbn(self) -> None:
        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            up = sql.strip().upper()
            if "COUNT(DISTINCT S.BCODE)" in up:
                return [{"book_count": 1, "line_count": 1, "total_qty": 1, "total_amount": 1}]
            if "AND S.BCODE=%S" in up:
                return [{"Gdate": "2026.07.01", "Gubun": "반품", "Gcode": "00405", "Hcode": "5019",
                         "gname": "거래처", "gsqut": 2, "gssum": 20000}]
            return [{"Bcode": "B0001", "Scode": "X", "Hcode": "5019", "Gubun": "반품",
                     "Pubun": "구간", "total_qty": 2, "total_amount": 20000}]

        async def fake_attach(server_id, hcode, rows, *, bcode_key="bcode",
                              price_key="gdang", isbn_key="gisbn", name_key=None,
                              overwrite_price=False):
            for r in rows:
                self.assertEqual(r[bcode_key], "B0001")
                r[isbn_key] = "978-89-0001"
                if price_key and not r.get(price_key):
                    r[price_key] = 12000
            return rows

        with patch.object(svc, "execute_query", side_effect=fake_exec), \
             patch.object(svc, "s1_column_names", new=AsyncMock(return_value={"gdate", "gubun", "gcode", "hcode", "bcode", "gsqut", "gssum"})), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={"B0001": "책"})), \
             patch.object(svc, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(svc, "build_d_select_clause", new=AsyncMock(return_value="1=1")), \
             patch.object(svc, "attach_book_meta", side_effect=fake_attach):
            res = await svc.ledger_query(
                server_id="remote_153", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019", detail_for_bcode="B0001", limit=50, offset=0,
            )
        d = res["detail"][0]
        self.assertEqual(d["bcode"], "B0001")
        self.assertEqual(d["gisbn"], "978-89-0001")
        self.assertEqual(d["gdang"], 12000)
        self.assertEqual(d["gssum"], 20000)   # 원본 컬럼 보존

    async def test_ledger_master_rows_carry_gisbn_and_master_gdang(self) -> None:
        """마스터(도서별 누계) 행에도 ISBN·정가가 붙는다 — 상세와 동일 hcode 스코프."""
        captured: list[tuple] = []

        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            up = sql.strip().upper()
            if "COUNT(DISTINCT S.BCODE)" in up:
                return [{"book_count": 2, "line_count": 3, "total_qty": 5, "total_amount": 50000}]
            return [
                {"Bcode": "B0001", "Scode": "X", "Hcode": "5019", "Gubun": "반품",
                 "Pubun": "구간", "total_qty": 2, "total_amount": 20000},
                {"Bcode": "B0002", "Scode": "X", "Hcode": "5019", "Gubun": "반품",
                 "Pubun": "신간", "total_qty": 3, "total_amount": 30000},
            ]

        async def fake_attach(server_id, hcode, rows, *, bcode_key="bcode",
                              price_key="gdang", isbn_key="gisbn", name_key=None,
                              overwrite_price=False):
            captured.append((server_id, hcode, bcode_key, price_key))
            meta = {"B0001": ("978-89-0001", 15000)}
            for r in rows:
                m = meta.get(r.get(bcode_key))
                r[isbn_key] = m[0] if m else ""
                if price_key and not r.get(price_key):
                    r[price_key] = m[1] if m else 0
            return rows

        with patch.object(svc, "execute_query", side_effect=fake_exec), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={"B0001": "책"})), \
             patch.object(svc, "_fetch_publisher_names", new=AsyncMock(return_value={"5019": "출판사"})), \
             patch.object(svc, "build_d_select_clause", new=AsyncMock(return_value="1=1")), \
             patch.object(svc, "attach_book_meta", side_effect=fake_attach):
            res = await svc.ledger_query(
                server_id="remote_153", date_from="2026-07-01", date_to="2026-07-31",
                hcode="5019", limit=50, offset=0,
            )

        master = res["master"]
        self.assertEqual(len(master), 2)
        # ISBN 은 모든 마스터 행에 존재(미존재 코드는 빈 문자열), 정가는 마스터에서 보충.
        self.assertEqual(master[0]["gisbn"], "978-89-0001")
        self.assertEqual(master[0]["gdang"], 15000)
        self.assertEqual(master[1]["gisbn"], "")
        self.assertEqual(master[1]["gdang"], 0)
        # 기존 마스터 필드 보존 + 부착용 임시 hcode 키는 응답에 노출하지 않는다.
        self.assertEqual(master[0]["book_name"], "책")
        self.assertEqual(master[0]["gname"], "출판사")
        self.assertEqual(master[0]["total_amount"], 20000)
        self.assertNotIn("hcode", master[0])
        # 상세 미요청(detail_for_bcode 없음) → 부착 호출은 마스터 1회, 로그인 스코프 hcode.
        self.assertEqual(captured, [("remote_153", "5019", "bcode", "gdang")])
        self.assertEqual(res["detail"], [])


class ReturnDetailBookMetaTests(unittest.IsolatedAsyncioTestCase):
    async def test_detail_lines_keep_slip_gdang_and_get_gisbn(self) -> None:
        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            up = sql.strip().upper()
            if "FROM S1_SSUB" in up:
                return [{"Bcode": "B0001", "Pubun": "구간", "Gsqut": 2, "Gdang": 9000,
                         "Grat1": 0.7, "Gssum": 12600, "Gbigo": "", "Yesno": "0"}]
            if "FROM G4_BOOK" in up:
                return [{"bcode": "B0001", "gname": "책"}]
            return []

        async def fake_attach(server_id, hcode, rows, *, bcode_key="bcode",
                              price_key="gdang", isbn_key="gisbn", name_key=None,
                              overwrite_price=False):
            self.assertEqual(hcode, "5019")
            for r in rows:
                r[isbn_key] = "978-89-0001"
                if price_key and not r.get(price_key):
                    r[price_key] = 15000
            return rows

        with patch.object(svc, "execute_query", side_effect=fake_exec), \
             patch.object(svc, "attach_book_meta", side_effect=fake_attach):
            res = await svc.get_return_detail(
                server_id="remote_138", return_key_str="G|2026.07.01|5019|0001",
            )
        ln = res["lines"][0]
        self.assertEqual(ln["gisbn"], "978-89-0001")
        self.assertEqual(ln["gdang"], 9000)   # 전표 단가 보존(마스터 정가로 덮지 않음)
        self.assertEqual(ln["bname"], "책")


class ScanMatchBookMetaTests(unittest.IsolatedAsyncioTestCase):
    async def test_scan_resolved_carries_gisbn(self) -> None:
        seen_sql: list[str] = []

        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            seen_sql.append(sql)
            return [{"Gcode": "001", "Gname": "샘플도서", "Gjeja": "저자", "Ocode": "B",
                     "Gdang": 15000, "Gisbn": " 9788972754381 "}]

        with patch.object(scan_svc, "execute_query", side_effect=fake_exec), \
             patch.object(scan_svc.pricing_service, "resolve_grats",
                          new=AsyncMock(return_value={"grats": None, "grats_source": "none"})):
            res = await scan_svc.match_barcode(
                barcode="9788972754381", hcode="1234", context="inbound", server_id="remote_138",
            )
        self.assertEqual(res["status"], "matched")
        self.assertEqual(res["resolved"]["gisbn"], "9788972754381")   # 트림된 마스터 Gisbn
        self.assertEqual(res["resolved"]["gdang"], 15000)
        # SELECT 목록에 Gisbn 포함(WHERE 는 이미 Gisbn 매칭 — 드리프트 표면 추가 0).
        self.assertIn("Gisbn", seen_sql[0].split("FROM")[0])
        self.assertIn("WHERE Gisbn=%s", seen_sql[0])

    async def test_scan_resolved_gisbn_falls_back_to_barcode(self) -> None:
        async def fake_exec(server_id, sql, params=()):  # noqa: ARG001
            return [{"Gcode": "001", "Gname": "샘플도서", "Gjeja": "", "Ocode": "B",
                     "Gdang": 0, "Gisbn": None}]

        with patch.object(scan_svc, "execute_query", side_effect=fake_exec), \
             patch.object(scan_svc.pricing_service, "resolve_grats",
                          new=AsyncMock(return_value={"grats": None, "grats_source": "none"})):
            res = await scan_svc.match_barcode(
                barcode="9788972754381", hcode="1234", context="return", server_id="remote_138",
            )
        self.assertEqual(res["resolved"]["gisbn"], "9788972754381")


if __name__ == "__main__":
    unittest.main()
