"""출고현황(거래관리 / Subu24 거래현황, 출고 관점) — 백엔드 회귀.

검증 전략
--------
- 라우터: ``GET /api/v1/transactions/outbound-status?view=summary|detail|list`` 가
  view 별로 올바른 transactions_service 함수를 호출하고, 응답 키(JSON 계약)가
  계약과 1:1 인지 monkeypatch 로 검증한다. storeKind/view 검증(422)도 확인.
- 서비스: 공통 WHERE 빌더(storeKind→Ocode, hcode 격리, Gubun 범위)와 rollup SQL
  의 IF()-조건합 산식(Subu24.pas L657-688)을 SQL 캡처로 검증한다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import transactions_service as tx  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth

COMMON = "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"


def _slip_item() -> dict:
    return {
        "order_key": {"gdate": "2026.04.18", "hcode": "H0001", "jubun": "11", "gcode": "00001"},
        "gdate": "2026.04.18",
        "jubun": "11",
        "gcode": "00001",
        "customer_name": "교보문고",
        "item_count": 3,
        "qty": 30,
        "amount": 300_000,
        "gbigo": "메모",
        "status": "done",
    }


def _line_item() -> dict:
    return {
        "order_key": {"gdate": "2026.04.18", "hcode": "H0001", "jubun": "11", "gcode": "00001"},
        "gdate": "2026.04.18",
        "pubun": "위탁",
        "gcode": "00001",
        "bcode": "B1",
        "bname": "도서A",
        "gsqut": 10,
        "gdang": 10_000,
        "grat1": 70.0,
        "gssum": 700_000,
        "gbigo": "",
        "status": "done",
    }


def _rollup_item() -> dict:
    return {
        "gcode": "00001",
        "customer_name": "교보문고",
        "out_qty": 10,
        "out_amount": 700_000,
        "gift_qty": 0,
        "return_qty": -2,
        "return_amount": -140_000,
        "sales_qty": 8,
        "sales_amount": 560_000,
    }


class OutboundStatusRouterTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_summary_view_calls_slips_and_shape(self) -> None:
        captured: list[dict] = []

        async def fake_slips(**kwargs):
            captured.append(kwargs)
            return [_slip_item()], 1

        with patch.object(tx, "list_outbound_status_slips", side_effect=fake_slips):
            res = self.client.get(
                "/api/v1/transactions/outbound-status" + COMMON + "&view=summary"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(set(body.keys()), {"items", "page"})
        it = body["items"][0]
        self.assertEqual(
            set(it.keys()),
            {
                "order_key", "gdate", "jubun", "idnum", "gcode", "customer_name",
                "item_count", "qty", "amount", "gbigo", "status",
            },
        )
        self.assertEqual(set(it["order_key"].keys()), {"gdate", "hcode", "jubun", "gcode"})
        self.assertEqual(captured[0]["date_from"], "2026-04-01")
        self.assertEqual(captured[0]["store_kind"], "ALL")

    def test_detail_view_uses_same_slips_shape(self) -> None:
        async def fake_slips(**kwargs):
            return [_slip_item()], 1

        with patch.object(tx, "list_outbound_status_slips", side_effect=fake_slips):
            res = self.client.get(
                "/api/v1/transactions/outbound-status" + COMMON + "&view=detail&storeKind=A"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(res.json()["items"]), 1)

    def test_list_view_returns_lines_rollup_totals(self) -> None:
        async def fake_lines(**kwargs):
            return [_line_item()], 1, {"qty": 10, "amount": 700_000}

        async def fake_rollup(**kwargs):
            return [_rollup_item()]

        with patch.object(tx, "list_outbound_status_lines", side_effect=fake_lines), \
                patch.object(tx, "outbound_status_customer_rollup", side_effect=fake_rollup):
            res = self.client.get(
                "/api/v1/transactions/outbound-status" + COMMON + "&view=list&storeKind=B"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(set(body.keys()), {"lines", "rollup", "totals", "page"})
        self.assertEqual(
            set(body["lines"][0].keys()),
            {
                "order_key", "gdate", "idnum", "pubun", "gcode", "bcode", "bname",
                "gsqut", "gdang", "grat1", "gssum", "gbigo", "status",
            },
        )
        self.assertEqual(
            set(body["rollup"][0].keys()),
            {
                "gcode", "customer_name", "out_qty", "out_amount", "gift_qty",
                "return_qty", "return_amount", "sales_qty", "sales_amount",
            },
        )
        self.assertEqual(body["totals"], {"qty": 10, "amount": 700_000})
        self.assertEqual(set(body["page"].keys()), {"limit", "offset", "total", "has_more"})

    def test_invalid_view_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/transactions/outbound-status" + COMMON + "&view=bogus"
        )
        self.assertEqual(res.status_code, 422, res.text)

    def test_invalid_store_kind_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/transactions/outbound-status" + COMMON + "&view=list&storeKind=C"
        )
        self.assertEqual(res.status_code, 422, res.text)


class OutboundStatusWhereBuilderTests(TestCase):
    def test_store_kind_a_adds_ocode_a(self) -> None:
        where, params = tx._build_outbound_status_where(
            date_from="2026-04-01", date_to="2026-04-30",
            gubun_clause=tx._GUBUN_OUT, hcode="H0001", store_kind="A",
        )
        self.assertIn("Gubun = '출고'", where)
        self.assertIn("Scode = 'X'", where)
        self.assertIn("Ocode = %s", where)
        self.assertIn("Hcode = %s", where)
        self.assertIn("A", params)          # Ocode 값
        self.assertIn("H0001", params)      # hcode 격리

    def test_store_kind_all_omits_ocode(self) -> None:
        where, params = tx._build_outbound_status_where(
            date_from="2026-04-01", date_to="2026-04-30",
            gubun_clause=tx._GUBUN_OUT, store_kind="ALL",
        )
        self.assertNotIn("Ocode", where)
        self.assertNotIn("Hcode = %s", where)  # hcode 미지정(슈퍼) → 필터 없음

    def test_rollup_uses_out_return_scope(self) -> None:
        where, _ = tx._build_outbound_status_where(
            date_from="2026-04-01", date_to="2026-04-30",
            gubun_clause=tx._GUBUN_OUT_RETURN, store_kind="B",
        )
        self.assertIn("Gubun IN ('출고','반품')", where)
        self.assertIn("Ocode = %s", where)


class OutboundStatusRollupSqlTests(IsolatedAsyncioTestCase):
    async def test_rollup_sql_formulas_and_scope(self) -> None:
        captured: list[str] = []

        async def fake_exec(server_id, sql, params=()):
            captured.append(sql)
            return []

        with patch.object(tx, "execute_query", side_effect=fake_exec):
            rows = await tx.outbound_status_customer_rollup(
                server_id="remote_1", date_from="2026-04-01", date_to="2026-04-30",
                hcode="H0001", store_kind="B",
            )
        self.assertEqual(rows, [])
        sql = captured[0]
        # Gubun 범위 = 출고+반품, GROUP BY Gcode, MAX(Hcode) 정합.
        self.assertIn("Gubun IN ('출고','반품')", sql)
        self.assertIn("GROUP BY Gcode", sql)
        self.assertIn("MAX(Hcode) AS hcode", sql)
        # 산식(Subu24.pas L657-688) — 증정 제외 출고수량 / 증정 분기 / 반품 음수합.
        self.assertIn("SUM(IF(Gubun='출고' AND Pubun<>'증정', IFNULL(Gsqut,0), 0)) AS out_qty", sql)
        self.assertIn("SUM(IF(Gubun<>'반품' AND Pubun='증정', IFNULL(Gsqut,0), 0)) AS gift_qty", sql)
        self.assertIn("SUM(IF(Gubun='반품', IFNULL(Gsqut,0), 0)) AS return_qty", sql)
        self.assertIn("SUM(IF(Gubun='반품', IFNULL(Gssum,0), 0)) AS return_amount", sql)
        # mysql3 호환: 파생테이블/CASE/COALESCE 미사용.
        self.assertNotIn("CASE", sql)
        self.assertNotIn("COALESCE", sql)
        self.assertNotIn("FROM (", sql)


if __name__ == "__main__":
    main()
