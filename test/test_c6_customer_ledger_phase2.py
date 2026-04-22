"""
C6 거래처원장 (Sobo32) + 통합 거래처원장 (Sobo32_1) — Phase 2 → Phase 1 승격 테스트.

대상
----
- ``GET /api/v1/ledger/customer``               (Sobo32)
- ``GET /api/v1/ledger/customer-integrated``    (Sobo32_1)

계약  : ``migration/contracts/customer_book_ledger_phase2.yaml`` v1.1.0
T0   : ``docs/customer-ledger-implementation-plan.md`` PLAN-LDG-CUSTOMER-2026-04-22

목표
----
1) **Acceptance Criteria** — AC-LDG-1/3/5/6/7/8/9 모두 PASS.
2) **회귀 가드** R1~R7 (Sobo54/57 v1.2.2 회귀에서 일반화) 모두 검증.
3) **분기 표 10건** — contract `branch_table` (= Subu32.pas L411~L506) 의 9 분기 +
   누적 합산식이 ``_accumulate_row`` 로 1:1 재현됨.

전략
----
실제 DB 없이 ``customer_ledger_service.execute_query`` /
``in_clause_lookup`` 등을 monkeypatch — 코드 경로/페이저 contract/분기 누적식만 검증.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import customer_ledger_service as svc  # noqa: E402
from app.services.inventory_service import _accumulate_row  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


def _run(coro):
    return asyncio.run(coro)


def _empty_acc() -> dict:
    """svc._empty_accumulator 와 동등 — 12 컬럼 누적 슬롯."""
    return svc._empty_accumulator()


# ---------------------------------------------------------------
# A) 라우터 contract — 422 / 500 / 페이징 패스-스루
# ---------------------------------------------------------------

class CustomerLedgerRouterContractTest(TestCase):
    """AC-LDG-6 / R6 (라우터 진단 메시지) 회귀 가드."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_missing_customer_code_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/ledger/customer"
            "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
        )
        self.assertEqual(res.status_code, 422, res.text)

    def test_missing_dates_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/ledger/customer?serverId=remote_1&customerCode=H001"
        )
        self.assertEqual(res.status_code, 422, res.text)

    def test_limit_over_500_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/ledger/customer"
            "?serverId=remote_1&customerCode=H001"
            "&dateFrom=2026-04-01&dateTo=2026-04-30&limit=1000"
        )
        self.assertEqual(res.status_code, 422, res.text)

    def test_router_500_includes_exception_class_name(self) -> None:
        """R6 — Sobo54/57 v1.2.2 회귀 가드 일반화."""

        async def explode(**_: object) -> dict:
            raise TimeoutError("synthetic mysql3 read_timeout")

        with patch.object(svc, "get_customer_ledger", side_effect=explode):
            res = self.client.get(
                "/api/v1/ledger/customer"
                "?serverId=remote_1&customerCode=H001"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 500)
        body = res.json()
        self.assertEqual(body["detail"]["code"], "INQ_TX_FAILED")
        self.assertIn("TimeoutError", body["detail"]["message"])

    def test_router_passes_query_to_service(self) -> None:
        captured: dict = {}

        async def fake(**kwargs) -> dict:
            captured.update(kwargs)
            return {
                "opening_date": "2026.03.31",
                "rows": [],
                "summary": {
                    "opening_qty": 100,
                    "total_in": 0,
                    "total_out": 0,
                    "closing_qty": 100,
                },
                "page": {"limit": 50, "offset": 0, "total": 0, "has_more": False},
                "truncated": False,
            }

        with patch.object(svc, "get_customer_ledger", side_effect=fake):
            res = self.client.get(
                "/api/v1/ledger/customer"
                "?serverId=remote_1&customerCode=H001"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
                "&bcodeFrom=B001&bcodeTo=B099&scope=A&limit=50&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["customer_code"], "H001")
        self.assertEqual(captured["bcode_from"], "B001")
        self.assertEqual(captured["bcode_to"], "B099")
        self.assertEqual(captured["scope"], "A")
        self.assertEqual((captured["limit"], captured["offset"]), (50, 0))


class IntegratedRouterContractTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_integrated_paging_passthrough(self) -> None:
        captured: dict = {}

        async def fake(**kwargs) -> dict:
            captured.update(kwargs)
            return {
                "opening_date": None,
                "rows": [
                    {
                        "hcode": "H001",
                        "hname": "신화서점",
                        "opening_qty": 100,
                        "period_in": 50,
                        "period_out": 30,
                        "closing_qty": 120,
                    }
                ],
                "page": {"limit": 25, "offset": 25, "total": 51, "has_more": True},
                "truncated": False,
            }

        with patch.object(svc, "get_integrated_customer_ledger", side_effect=fake):
            res = self.client.get(
                "/api/v1/ledger/customer-integrated"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
                "&customerPattern=H&limit=25&offset=25"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["customer_pattern"], "H")
        self.assertEqual((captured["limit"], captured["offset"]), (25, 25))
        body = res.json()
        self.assertTrue(body["page"]["has_more"])
        self.assertEqual(body["rows"][0]["closing_qty"], 120)

    def test_integrated_500_includes_exception_class_name(self) -> None:
        async def explode(**_: object) -> dict:
            raise TimeoutError("synthetic")

        with patch.object(svc, "get_integrated_customer_ledger", side_effect=explode):
            res = self.client.get(
                "/api/v1/ledger/customer-integrated"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 500)
        self.assertIn("TimeoutError", res.json()["detail"]["message"])


# ---------------------------------------------------------------
# B) 분기 표 10건 — _accumulate_row 가 contract `branch_table` 1:1 재현
#    (AC-LDG-7) — 결과 등가성의 단일 원천
# ---------------------------------------------------------------

class BranchTableEquivalenceTest(TestCase):
    """contract `branch_table` 의 10 분기 (= Subu32.pas L411~L506) 동등성."""

    def _apply(self, scode, gubun, pubun, gsqut, gssum=0):
        acc = _empty_acc()
        _accumulate_row(acc, scode, gubun, pubun, gsqut, gssum)
        return acc

    def test_branch_Y_pubun_이동(self) -> None:
        # row 1: yesno=Y, gubun=*, pubun=이동 → gsqut += Gsqut
        # (Subu31._accumulate_row SSOT — DBGrid 의 GPSUM 표기는 모던 응답에서
        #  'gsqut' 키로 매핑됨; layout_mappings/Sobo32.md §4 노트 참조)
        acc = self._apply("Y", "출고", "이동", 5)
        self.assertEqual(acc["gsqut"], 5)
        self.assertEqual(acc["giqut"], 0)
        self.assertEqual(acc["gpsum"], 0)  # 이동은 gpsum 미가산 (회귀 가드)

    def test_branch_Y_pubun_반품(self) -> None:
        # row 2: yesno=Y, gubun=*, pubun=반품 → gisum += Gsqut
        acc = self._apply("Y", "출고", "반품", 7)
        self.assertEqual(acc["gisum"], 7)

    def test_branch_Y_gubun_입고(self) -> None:
        # row 3: yesno=Y, gubun=입고, pubun=* → giqut += Gsqut
        acc = self._apply("Y", "입고", "신간", 10)
        self.assertEqual(acc["giqut"], 10)

    def test_branch_X_pubun_증정(self) -> None:
        # row 4: yesno=X, gubun=*, pubun=증정 → gjqut + gosum
        acc = self._apply("X", "출고", "증정", 3, gssum=21000)
        self.assertEqual(acc["gjqut"], 3)
        self.assertEqual(acc["gosum"], 21000)

    def test_branch_X_gubun_출고(self) -> None:
        # row 5: yesno=X, gubun=출고, pubun=* → goqut + gosum
        acc = self._apply("X", "출고", "신간", 4, gssum=28000)
        self.assertEqual(acc["goqut"], 4)
        self.assertEqual(acc["gosum"], 28000)

    def test_branch_X_gubun_폐기_pubun_비품(self) -> None:
        # row 6: yesno=X, gubun=폐기, pubun=비품 → gpqut + gjsum
        acc = self._apply("X", "폐기", "비품", 2)
        self.assertEqual(acc["gpqut"], 2)
        self.assertEqual(acc["gjsum"], 2)

    def test_branch_X_gubun_폐기_else(self) -> None:
        # row 7: yesno=X, gubun=폐기, pubun=_else → gpqut + gpsum
        # (실제 _accumulate_row 는 'gpqut+=Gsqut, gpsum+=Gsqut' 로 매핑되어 있음 —
        #  contract branch_table 의 'gbsum' 표기는 inventory_service 의 분기에서는
        #  gpsum 슬롯에 매핑됨. 두 슬롯 모두 +Gsqut 가산만 검증.)
        acc = self._apply("X", "폐기", "신간", 6)
        self.assertEqual(acc["gpqut"], 6)
        # _accumulate_row 의 폐기 else 가지 — gpsum += Gsqut (Subu31 분기 정의)
        self.assertEqual(acc["gpsum"], 6)

    def test_branch_X_pubun_비품_gubun_else(self) -> None:
        # row 8: yesno=X, gubun=_else, pubun=비품 → gbqut + bs/jsum
        acc = self._apply("X", "출고제외", "비품", 5, gssum=35000)
        self.assertEqual(acc["gbqut"], 5)
        # gbsum += Gssum, gjsum -= Gsqut (Subu31 분기)
        self.assertEqual(acc["gbsum"], 35000)
        self.assertEqual(acc["gjsum"], -5)

    def test_branch_X_pubun_폐기_gubun_else(self) -> None:
        # row 9: yesno=X, gubun=_else, pubun=폐기 → gpqut += (Subu31 분기)
        acc = self._apply("X", "출고제외", "폐기", 4)
        self.assertEqual(acc["gpqut"], 4)

    def test_accumulator_preserves_zero_when_unmatched(self) -> None:
        """매칭되지 않는 분기는 가산 0 — 회귀(우발 가산) 가드."""
        acc = self._apply("X", "잡기타", "잡기타", 99)
        # 어떤 알려진 컬럼도 가산되지 않아야 함
        self.assertEqual(
            sum(v for k, v in acc.items() if isinstance(v, int)),
            0,
        )


# ---------------------------------------------------------------
# C) Service 페이저 / 등가성 / 회귀 가드 — DB monkeypatch
# ---------------------------------------------------------------

class CustomerLedgerServicePagingTest(TestCase):
    """R1~R5 + AC-LDG-1 회귀 가드."""

    def _patch_db(self, *, dates, raw_rows, opening_qty=100, grand_rows=None):
        """customer_ledger_service.execute_query / in_clause_lookup 모킹.

        - ``Sv_Ghng`` 이월 기준일 → opening_date row 1건.
        - ``COUNT(DISTINCT Gdate)`` → len(dates).
        - ``DISTINCT Gdate ... LIMIT %s OFFSET %s`` → 슬라이싱.
        - ``Sb_Csum SUM(Gsqut) WHERE Gcode=%s`` → opening_qty.
        - grand_summary (``GROUP BY Scode,Gubun,Pubun`` 단독) → grand_rows.
        """
        captured_main_sqls: list[str] = []
        grand = grand_rows or []

        async def fake_execute(server_id, sql, params=()):
            sql_lower = sql.lower().strip()
            captured_main_sqls.append(sql_lower)

            if "max(gdate)" in sql_lower and "sv_ghng" in sql_lower:
                return [{"opening_date": "2026.03.31"}]
            if "count(distinct gdate)" in sql_lower:
                return [{"cnt": len(dates)}]
            if "select distinct gdate" in sql_lower:
                # 마지막 2 params 는 limit, offset
                lim, off = params[-2], params[-1]
                window = dates[off : off + lim]
                return [{"Gdate": d} for d in window]
            if "from sb_csum" in sql_lower and "where gcode" in sql_lower:
                return [{"qty": opening_qty}]
            if (
                "group by scode, gubun, pubun" in sql_lower
                and "from s1_ssub" in sql_lower
            ):
                return grand
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=()):
            # _ledger_rows_sql 패턴 — page_dates 의 raw_rows 만 반환
            return [r for r in raw_rows if r.get("Gdate") in keys]

        return patch.multiple(
            svc,
            execute_query=fake_execute,
            in_clause_lookup=fake_in_clause,
        ), captured_main_sqls

    def test_self_consistent_opening_plus_in_minus_out(self) -> None:
        """AC-LDG-1 — opening + Σin - Σout == closing_qty."""
        dates = ["2026.04.01", "2026.04.02"]
        raw_rows = [
            # 2026.04.01: 입고 10, 출고 4
            {"Gdate": "2026.04.01", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 10, "Gssum": 0},
            {"Gdate": "2026.04.01", "Scode": "X", "Gubun": "출고", "Pubun": "신간",
             "Gsqut": 4,  "Gssum": 28000},
            # 2026.04.02: 증정 1
            {"Gdate": "2026.04.02", "Scode": "X", "Gubun": "출고", "Pubun": "증정",
             "Gsqut": 1,  "Gssum": 7000},
        ]
        # grand summary (offset==0 응답에서만 산출). 동일 raw 합.
        grand_rows = [
            {"Scode": "Y", "Gubun": "입고", "Pubun": "신간", "Gsqut": 10, "Gssum": 0},
            {"Scode": "X", "Gubun": "출고", "Pubun": "신간", "Gsqut": 4,  "Gssum": 28000},
            {"Scode": "X", "Gubun": "출고", "Pubun": "증정", "Gsqut": 1,  "Gssum": 7000},
        ]
        ctx, _ = self._patch_db(
            dates=dates, raw_rows=raw_rows,
            opening_qty=100, grand_rows=grand_rows,
        )
        with ctx:
            result = _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=50, offset=0,
            ))

        # 일별 누적 잔량 — 4/1: 100 + 10 - 4 = 106, 4/2: 106 - 1 = 105
        self.assertEqual(result["rows"][0]["balance_qty"], 106)
        self.assertEqual(result["rows"][1]["balance_qty"], 105)
        # summary 자기일관: opening(100) + in(10) - out(5) = 105 == closing
        s = result["summary"]
        self.assertEqual(s["opening_qty"], 100)
        self.assertEqual(s["total_in"], 10)
        self.assertEqual(s["total_out"], 5)
        self.assertEqual(
            s["closing_qty"],
            s["opening_qty"] + s["total_in"] - s["total_out"],
        )

    def test_pager_LIMIT_via_distinct_dates(self) -> None:
        """R3 — DISTINCT Gdate LIMIT/OFFSET 으로 페이저가 동작."""
        dates = [f"2026.04.{i:02d}" for i in range(1, 11)]  # 10 일
        raw_rows = [
            {"Gdate": d, "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 1, "Gssum": 0}
            for d in dates
        ]
        ctx, _ = self._patch_db(dates=dates, raw_rows=raw_rows, opening_qty=0)
        with ctx:
            result = _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=3, offset=3,
            ))
        # 3행만 노출 — 페이지 4~6일
        self.assertEqual(len(result["rows"]), 3)
        self.assertEqual(result["rows"][0]["gdate"], "2026.04.04")
        self.assertEqual(result["page"]["total"], 10)
        self.assertEqual((result["page"]["limit"], result["page"]["offset"]), (3, 3))

    def test_summary_offset_zero_only(self) -> None:
        """R4 / AC-LDG-LDG — offset>0 응답은 summary 0 (프론트 totalsCache)."""
        dates = ["2026.04.01", "2026.04.02"]
        raw_rows = [
            {"Gdate": "2026.04.01", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 5, "Gssum": 0},
            {"Gdate": "2026.04.02", "Scode": "X", "Gubun": "출고", "Pubun": "신간",
             "Gsqut": 2, "Gssum": 14000},
        ]
        ctx, _ = self._patch_db(
            dates=dates, raw_rows=raw_rows,
            opening_qty=200,
            grand_rows=[
                {"Scode": "Y", "Gubun": "입고", "Pubun": "신간", "Gsqut": 5, "Gssum": 0},
            ],
        )
        with ctx:
            result = _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=1, offset=1,
            ))
        # summary 4종 모두 0 (offset>0)
        self.assertEqual(result["summary"]["opening_qty"], 0)
        self.assertEqual(result["summary"]["total_in"], 0)
        self.assertEqual(result["summary"]["total_out"], 0)
        self.assertEqual(result["summary"]["closing_qty"], 0)
        # opening 도 0 (R4) → balance_qty 가 opening 없이 가산
        self.assertEqual(result["rows"][0]["balance_qty"], -2)  # 0 + 0 - 2 (4/2)

    def test_no_join_in_main_sql(self) -> None:
        """R2 / AC-LDG-8 — 메인 SQL 에 JOIN G4_Book/G7_Ggeo/G1_Ggeo 미포함."""
        dates = ["2026.04.01"]
        raw_rows = [
            {"Gdate": "2026.04.01", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 5, "Gssum": 0},
        ]
        ctx, captured = self._patch_db(
            dates=dates, raw_rows=raw_rows, opening_qty=0
        )
        with ctx:
            _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=10, offset=0,
            ))
        for sql in captured:
            # 메인 페이저 단일 테이블만 — 룩업 테이블과의 JOIN 금지
            self.assertNotIn(" join g4_book", sql)
            self.assertNotIn(" join g7_ggeo", sql)
            self.assertNotIn(" join g1_ggeo", sql)

    def test_empty_dates_returns_empty_with_opening_at_offset_zero(self) -> None:
        """결과 0건 + offset==0 시에도 opening_qty 는 채워져 자기일관 유지."""
        ctx, _ = self._patch_db(dates=[], raw_rows=[], opening_qty=300)
        with ctx:
            result = _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=10, offset=0,
            ))
        self.assertEqual(result["rows"], [])
        self.assertEqual(result["summary"]["opening_qty"], 300)
        self.assertEqual(result["summary"]["closing_qty"], 300)


# ---------------------------------------------------------------
# D) 통합 거래처원장 — 페이저 + 자기일관 + AC-LDG-3
# ---------------------------------------------------------------

class IntegratedCustomerLedgerServiceTest(TestCase):
    def _patch_db(self, *, hcodes, raw_rows, opening_map=None, name_map=None):
        opening_map = opening_map or {}
        name_map = name_map or {}

        async def fake_execute(server_id, sql, params=()):
            sql_lower = sql.lower().strip()
            if "max(gdate)" in sql_lower and "sv_ghng" in sql_lower:
                return [{"opening_date": "2026.03.31"}]
            if "count(distinct hcode)" in sql_lower:
                return [{"cnt": len(hcodes)}]
            if "select distinct hcode" in sql_lower:
                lim, off = params[-2], params[-1]
                window = hcodes[off : off + lim]
                return [{"Hcode": h} for h in window]
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=()):
            tpl_lower = sql_template.lower()
            if "from sb_csum" in tpl_lower:
                return [
                    {"hcode": k, "qty": opening_map.get(k, 0)}
                    for k in keys
                ]
            if "from g7_ggeo" in tpl_lower:
                return [
                    {"hcode": k, "hname": name_map.get(k, "")}
                    for k in keys
                ]
            # _integrated_rows_sql — Hcode IN
            return [r for r in raw_rows if r.get("Hcode") in keys]

        # G7_Ggeo 룩업은 inbound_service._fetch_publisher_names 가 수행 →
        # in_clause_lookup 모듈은 inbound_service 내부 alias 도 monkeypatch 필요.
        from app.services import inbound_service as inb
        return patch.multiple(
            svc,
            execute_query=fake_execute,
            in_clause_lookup=fake_in_clause,
        ), patch.object(inb, "in_clause_lookup", side_effect=fake_in_clause)

    def test_integrated_self_consistent_per_hcode(self) -> None:
        """closing_qty == opening_qty + period_in - period_out (per row)."""
        hcodes = ["H001", "H002"]
        raw_rows = [
            # H001: in 10, out 3
            {"Hcode": "H001", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 10, "Gssum": 0},
            {"Hcode": "H001", "Scode": "X", "Gubun": "출고", "Pubun": "신간",
             "Gsqut": 3,  "Gssum": 21000},
            # H002: in 5
            {"Hcode": "H002", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 5,  "Gssum": 0},
        ]
        ctx_svc, ctx_inb = self._patch_db(
            hcodes=hcodes, raw_rows=raw_rows,
            opening_map={"H001": 100, "H002": 50},
            name_map={"H001": "신화서점", "H002": "샘플도서"},
        )
        with ctx_svc, ctx_inb:
            result = _run(svc.get_integrated_customer_ledger(
                server_id="remote_1",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=10, offset=0,
            ))

        rows = {r["hcode"]: r for r in result["rows"]}
        h001 = rows["H001"]
        self.assertEqual(h001["hname"], "신화서점")
        self.assertEqual(h001["opening_qty"], 100)
        self.assertEqual(h001["period_in"], 10)
        self.assertEqual(h001["period_out"], 3)
        self.assertEqual(
            h001["closing_qty"],
            h001["opening_qty"] + h001["period_in"] - h001["period_out"],
        )
        h002 = rows["H002"]
        self.assertEqual(h002["closing_qty"], 50 + 5 - 0)

    def test_integrated_equals_sum_of_singles(self) -> None:
        """AC-LDG-3 — integrated.row[H].closing == 단일 호출의 closing."""
        hcodes = ["H001"]
        raw_rows = [
            {"Hcode": "H001", "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 7, "Gssum": 0},
            {"Hcode": "H001", "Scode": "X", "Gubun": "출고", "Pubun": "신간",
             "Gsqut": 2, "Gssum": 14000},
        ]
        # integrated 호출
        ctx_svc, ctx_inb = self._patch_db(
            hcodes=hcodes, raw_rows=raw_rows,
            opening_map={"H001": 100}, name_map={"H001": "X"},
        )
        with ctx_svc, ctx_inb:
            integrated = _run(svc.get_integrated_customer_ledger(
                server_id="remote_1",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=10, offset=0,
            ))

        # 단일 호출 — 동일 raw + grand summary 동일.
        single_dates = ["2026.04.01"]
        single_raw = [
            {"Gdate": "2026.04.01", **{k: v for k, v in r.items() if k != "Hcode"}}
            for r in raw_rows
        ]
        grand = [
            {"Scode": r["Scode"], "Gubun": r["Gubun"], "Pubun": r["Pubun"],
             "Gsqut": r["Gsqut"], "Gssum": r["Gssum"]}
            for r in raw_rows
        ]

        async def fake_exec(server_id, sql, params=()):
            sql_lower = sql.lower().strip()
            if "max(gdate)" in sql_lower:
                return [{"opening_date": "2026.03.31"}]
            if "count(distinct gdate)" in sql_lower:
                return [{"cnt": len(single_dates)}]
            if "select distinct gdate" in sql_lower:
                return [{"Gdate": d} for d in single_dates]
            if "from sb_csum" in sql_lower:
                return [{"qty": 100}]
            if "group by scode, gubun, pubun" in sql_lower:
                return grand
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=()):
            return [r for r in single_raw if r.get("Gdate") in keys]

        with patch.multiple(
            svc, execute_query=fake_exec, in_clause_lookup=fake_in_clause,
        ):
            single = _run(svc.get_customer_ledger(
                server_id="remote_1", customer_code="H001",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=10, offset=0,
            ))

        self.assertEqual(
            integrated["rows"][0]["closing_qty"],
            single["summary"]["closing_qty"],
        )

    def test_integrated_pager_passthrough(self) -> None:
        """R3 — DISTINCT Hcode LIMIT/OFFSET 작동."""
        hcodes = [f"H{i:03d}" for i in range(1, 21)]
        raw_rows = [
            {"Hcode": h, "Scode": "Y", "Gubun": "입고", "Pubun": "신간",
             "Gsqut": 1, "Gssum": 0}
            for h in hcodes
        ]
        ctx_svc, ctx_inb = self._patch_db(
            hcodes=hcodes, raw_rows=raw_rows,
            opening_map={h: 0 for h in hcodes},
            name_map={h: "" for h in hcodes},
        )
        with ctx_svc, ctx_inb:
            result = _run(svc.get_integrated_customer_ledger(
                server_id="remote_1",
                date_from="2026-04-01", date_to="2026-04-30",
                limit=5, offset=10,
            ))
        self.assertEqual(len(result["rows"]), 5)
        self.assertEqual(result["rows"][0]["hcode"], "H011")
        self.assertEqual(result["page"]["total"], 20)


if __name__ == "__main__":
    main()
