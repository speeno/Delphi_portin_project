"""
C3 입고 리포트 (Sobo54·Sobo57) — Phase 2 보강 검증.

대상 화면 (dashboard/data/phase2-screen-cards.json):
  - Sobo54  /inbound/reports/daily   (일별 입고내역서)
  - Sobo57  /inbound/reports/period  (기간별 입고내역서)

계약: migration/contracts/inbound_receipt.yaml
   GET /api/v1/inbound/reports/daily   (gdate + limit/offset)
   GET /api/v1/inbound/reports/period  (dateFrom/dateTo + limit/offset)

목표
----
1) **422 회귀 가드** — 필수 query 누락 시 422.
2) **500 회귀 가드** — service 호출 실패 시 라우터가 500 + IN_TX_FAILED.
3) **페이징 계약** — limit/offset 패스-스루 + 응답 ``page`` 메타 + 동기 롤
   ``page.total = max(publisher_total, vendor_total)``.
4) **합계 분리** — 그리드는 페이지 행만, ``totals`` 는 전역 합 (페이지 변경 무관).

전략
----
실제 DB 없이 ``inbound_service.daily_report`` / ``period_report`` 를 monkeypatch
하여 라우터 검증·페이저 contract 만 본다. mysql3 호환 SQL 자체는
``test_list_count_grouped_mysql3.py`` 등 별도 통합 스모크에서 다룬다.

사용자 규칙: test 폴더에 저장 / 신규 헬퍼 금지 / SOLID(SRP) 유지.
"""

from __future__ import annotations

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
from app.services import inbound_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


def _publisher_row(gdate: str, hcode: str, gcode: str, bcode: str, *, qty: int) -> dict:
    return {
        "gdate": gdate, "hcode": hcode, "hname": f"P-{hcode}",
        "gcode": gcode, "gname": f"V-{gcode}",
        "idnum": "120000000001", "pubun": "신간",
        "bcode": bcode, "bname": f"B-{bcode}",
        "gsqut": qty, "gdang": 10000,
    }


def _vendor_row(gcode: str, bcode: str, *, qty: int, amount: int, gdate: str | None = None) -> dict:
    base = {
        "gcode": gcode, "gname": f"V-{gcode}",
        "idnum": "120000000001", "pubun": "신간",
        "bcode": bcode, "bname": f"B-{bcode}",
        "gsqut": qty, "gdang": 10000, "grat1": 0.7, "gssum": amount,
    }
    if gdate is not None:
        base = {"gdate": gdate, **base}
    return base


# ---------------------------------------------------------------
# AC-IN-RPT-1 / Sobo54 — gdate 누락 시 422 (회귀 러너 422 재현 가드)
# ---------------------------------------------------------------

class DailyReportContractTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_missing_gdate_returns_422(self) -> None:
        res = self.client.get("/api/v1/inbound/reports/daily?serverId=remote_1")
        self.assertEqual(res.status_code, 422, res.text)

    def test_paging_passthrough_and_synced_roll(self) -> None:
        captured: dict = {}

        async def fake_daily(*, server_id: str, gdate: str, limit: int, offset: int) -> dict:
            captured.update({
                "server_id": server_id, "gdate": gdate,
                "limit": limit, "offset": offset,
            })
            # 새 페이저 contract: page.total 은 ceiling = offset + visible (+1 if has_more)
            # has_more 가 진실의 원천 (count_grouped 미사용 — DEC-033(g) 대용량 변형).
            return {
                "by_publisher": [_publisher_row("2026.04.20", "H0001", "G0001", "B001", qty=5)],
                "by_vendor": [
                    _vendor_row("G0001", "B001", qty=5, amount=35000),
                    _vendor_row("G0002", "B002", qty=3, amount=21000),
                ],
                "totals": {"qty": 80, "amount": 560000},  # 전역 합 (offset==0 1회 산출)
                "page": {"limit": 1, "offset": 0, "total": 3, "has_more": True},
            }

        with patch.object(inbound_service, "daily_report", side_effect=fake_daily):
            res = self.client.get(
                "/api/v1/inbound/reports/daily"
                "?serverId=remote_1&gdate=2026-04-20&limit=1&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["limit"], 1)
        self.assertEqual(captured["offset"], 0)
        body = res.json()
        self.assertEqual(body["page"]["limit"], 1)
        self.assertTrue(body["page"]["has_more"])
        # totals 는 전역 (페이지 행 합이 아님 — offset==0 응답에서만 산출)
        self.assertEqual(body["totals"], {"qty": 80, "amount": 560000})

    def test_service_failure_yields_500_in_tx_failed(self) -> None:
        async def explode(**_: object) -> dict:
            raise RuntimeError("synthetic mysql3 syntax error")

        with patch.object(inbound_service, "daily_report", side_effect=explode):
            res = self.client.get(
                "/api/v1/inbound/reports/daily"
                "?serverId=remote_1&gdate=2026-04-20"
            )
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json()["detail"]["code"], "IN_TX_FAILED")


# ---------------------------------------------------------------
# AC-IN-RPT-2 / Sobo57 — dateFrom/dateTo 누락 422 + 500 가드 + 페이징
# ---------------------------------------------------------------

class PeriodReportContractTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_missing_date_range_returns_422(self) -> None:
        res = self.client.get("/api/v1/inbound/reports/period?serverId=remote_1")
        self.assertEqual(res.status_code, 422, res.text)

    def test_paging_passthrough_with_global_totals(self) -> None:
        captured: dict = {}

        async def fake_period(
            *, server_id: str, date_from: str, date_to: str, limit: int, offset: int
        ) -> dict:
            captured.update({
                "server_id": server_id, "date_from": date_from, "date_to": date_to,
                "limit": limit, "offset": offset,
            })
            return {
                "by_publisher": [
                    _publisher_row("2026.04.18", "H0001", "G0001", "B001", qty=5),
                    _publisher_row("2026.04.20", "H0001", "G0001", "B001", qty=5),
                ],
                "by_vendor": [
                    _vendor_row("G0001", "B001", qty=10, amount=70000, gdate="2026.04.18"),
                ],
                "totals": {"qty": 120, "amount": 840000},
                "page": {"limit": 50, "offset": 50, "total": 200, "has_more": True},
            }

        with patch.object(inbound_service, "period_report", side_effect=fake_period):
            res = self.client.get(
                "/api/v1/inbound/reports/period"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
                "&limit=50&offset=50"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["date_from"], "2026-04-01")
        self.assertEqual(captured["date_to"], "2026-04-30")
        self.assertEqual((captured["limit"], captured["offset"]), (50, 50))
        body = res.json()
        # by_vendor 행에는 ``gdate`` 컬럼이 포함된다 (period 전용)
        self.assertIn("gdate", body["by_vendor"][0])
        # 페이지 합과 전역 합은 분리 — totals 는 그리드 SUM 과 무관
        self.assertEqual(body["totals"]["qty"], 120)
        self.assertEqual(body["page"]["total"], 200)
        self.assertTrue(body["page"]["has_more"])

    def test_service_failure_yields_500_in_tx_failed(self) -> None:
        async def explode(**_: object) -> dict:
            raise RuntimeError("synthetic period failure")

        with patch.object(inbound_service, "period_report", side_effect=explode):
            res = self.client.get(
                "/api/v1/inbound/reports/period"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json()["detail"]["code"], "IN_TX_FAILED")


# ---------------------------------------------------------------
# AC-IN-RPT-3 — 서비스 단의 페이징 경계 (limit/offset 클램프 + LIMIT+1 has_more)
# DB 없이 execute_query 만 모킹하여 코드 경로 자체를 검증.
# 새 정책: count_grouped 미사용 (30s+ 타임아웃 회귀 방지 — DEC-033(g) 대용량 변형).
# 페이저 진실의 원천은 has_more 이며 page.total 은 진척도 ceiling.
# (mysql3 SQL 텍스트 자체의 호환성은 sql_mysql3 통합 테스트 책임)
# ---------------------------------------------------------------

class ReportServicePagingTest(TestCase):
    def _patch_db(
        self,
        *,
        pub_rows: list,
        ven_rows: list,
        grand_qty: int,
        grand_amount: int,
    ):
        """LIMIT+1 패턴: ``pub_rows`` / ``ven_rows`` 는 이미 limit+1 행까지
        포함된 raw 결과를 가정한다. 서비스가 직접 슬라이싱하며 has_more 판정.
        """
        async def fake_execute_query(server_id, sql, params=()):
            sql_lower = sql.lower()
            # GRAND_TOTALS: SUM 만 + GROUP BY 없음
            if "sum(gsqut)" in sql_lower and "group by" not in sql_lower:
                return [{"qty": grand_qty, "amount": grand_amount}]
            # publisher / vendor 분기 — SELECT 컬럼 차이로 구분
            if "as hname" in sql_lower:
                return pub_rows
            return ven_rows

        return patch.object(
            inbound_service, "execute_query", side_effect=fake_execute_query
        )

    @staticmethod
    def _run(coro):
        import asyncio
        return asyncio.run(coro)

    def test_daily_clamps_and_has_more_via_limit_plus_one(self) -> None:
        # limit=500 으로 클램프된 후 LIMIT+1=501 행을 모킹 → has_more True 확인.
        # 한쪽만 has_more 여도 두 그리드 동기 롤로 has_more 가 True 가 되어야 한다.
        pub_rows = [
            _publisher_row("2026.04.20", "H0001", "G0001", f"B{i:03d}", qty=1)
            for i in range(501)
        ]
        ven_rows = [
            _vendor_row("G0001", f"B{i:03d}", qty=1, amount=1000)
            for i in range(2)  # 작음 — has_more=False
        ]
        with self._patch_db(
            pub_rows=pub_rows, ven_rows=ven_rows,
            grand_qty=99, grand_amount=999000,
        ):
            result = self._run(
                inbound_service.daily_report(
                    server_id="remote_1",
                    gdate="2026-04-20",
                    limit=10_000,  # 상한(500) 클램프 검증
                    offset=-5,     # 음수 → 0 클램프
                )
            )

        self.assertEqual(result["page"]["limit"], 500)
        self.assertEqual(result["page"]["offset"], 0)
        # 슬라이싱: pub 501 → 500, ven 2 → 2. 동기 롤 has_more = True (pub 측)
        self.assertEqual(len(result["by_publisher"]), 500)
        self.assertEqual(len(result["by_vendor"]), 2)
        self.assertTrue(result["page"]["has_more"])
        # ceiling total = offset(0) + max(500, 2) + 1 = 501
        self.assertEqual(result["page"]["total"], 501)
        # offset==0 → grand_totals 채워짐
        self.assertEqual(result["totals"], {"qty": 99, "amount": 999000})

    def test_daily_no_more_when_within_limit(self) -> None:
        pub_rows = [
            _publisher_row("2026.04.20", "H0001", "G0001", f"B{i:03d}", qty=1)
            for i in range(3)
        ]
        ven_rows = [
            _vendor_row("G0001", f"B{i:03d}", qty=1, amount=1000)
            for i in range(2)
        ]
        with self._patch_db(
            pub_rows=pub_rows, ven_rows=ven_rows,
            grand_qty=5, grand_amount=5000,
        ):
            result = self._run(
                inbound_service.daily_report(
                    server_id="remote_1", gdate="2026-04-20",
                    limit=100, offset=0,
                )
            )
        # 두 그리드 모두 limit+1 미만 → has_more False
        self.assertFalse(result["page"]["has_more"])
        # ceiling total = 0 + max(3,2) = 3 (no +1)
        self.assertEqual(result["page"]["total"], 3)

    def test_period_offset_skips_grand_totals(self) -> None:
        """offset>0 응답은 grand_totals 미산출(0/0) — 30s 절감 핵심."""
        pub_rows = [
            _publisher_row("2026.04.18", "H0001", "G0001", "B001", qty=5),
        ]
        ven_rows: list = []  # 한 그리드 소진
        with self._patch_db(
            pub_rows=pub_rows, ven_rows=ven_rows,
            grand_qty=50, grand_amount=350000,
        ):
            result = self._run(
                inbound_service.period_report(
                    server_id="remote_1",
                    date_from="2026-04-01", date_to="2026-04-30",
                    limit=10, offset=10,
                )
            )

        self.assertFalse(result["page"]["has_more"])
        # ceiling total = offset(10) + max(1,0) = 11
        self.assertEqual(result["page"]["total"], 11)
        # offset>0 이면 totals 는 0 (프론트가 첫 페이지 응답을 캐시해 표시)
        self.assertEqual(result["totals"], {"qty": 0, "amount": 0})
        # 한 그리드가 비어도 200 OK + 빈 배열 (DEC-033 빈집합 정합)
        self.assertEqual(result["by_vendor"], [])
        self.assertEqual(len(result["by_publisher"]), 1)


if __name__ == "__main__":
    main()
