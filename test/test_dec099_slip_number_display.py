"""DEC-099 — 전표번호 표기 정본(Idnum) 통일 + 거래현황 정렬 패스스루 회귀.

고객 리포트(2026-07-16): 거래현황(list/상세/요약)·출고접수관리의 "전표" 번호가
화면마다 다름 — 원인은 Jubun(거래처별 차수)과 Idnum(일자별 전표번호) 혼용.
정본(DEC-064) = Idnum 5자리 zero-pad. 본 테스트는 백엔드 계약을 고정한다:

  1. outbound_service.list_orders — 슬립 그룹에 MAX(Idnum+0) 대표값을 SELECT 하고
     order_key.idnum 으로 반환한다(프론트 formatIdnumDisplay 입력).
  2. outbound_service.get_order_detail — 라인 Idnum 대표값(MAX)을 order_key.idnum 으로.
  3. /api/v1/transactions/status 파사드 — sortBy/sortDir 를
     list_sales_statements(sort_by/sort_dir)로 전달(거래현황 컬럼 정렬).
"""
from __future__ import annotations

from typing import Any
from unittest import TestCase
from unittest.mock import AsyncMock, patch

from unittest import IsolatedAsyncioTestCase


def _slip_row(**over: Any) -> dict[str, Any]:
    row = {
        "Gdate": "2026.07.01",
        "Hcode": "H001",
        "Jubun": "11",
        "stmt_gcode": "GCUST01",
        "line_count": 2,
        "qty": 3,
        "amount": 30000,
        "yesno_max": "1",
        "idnum": 7,
    }
    row.update(over)
    return row


def _line_row(**over: Any) -> dict[str, Any]:
    row = {
        "Gdate": "2026.07.01",
        "Hcode": "H001",
        "Jubun": "11",
        "Gcode": "GCUST01",
        "Bcode": "B0001",
        "Pubun": "위탁",
        "Gsqut": 1,
        "Gssum": 10000,
        "Yesno": "1",
        "Gdang": 10000,
        "Grat1": 60,
        "Gbigo": "",
        "Idnum": 7,
    }
    row.update(over)
    return row


class OutboundListIdnumTests(IsolatedAsyncioTestCase):
    async def test_list_orders_selects_and_returns_idnum(self) -> None:
        from app.services import outbound_service as svc

        with patch.object(svc, "execute_query", new=AsyncMock(return_value=[_slip_row()])) as ex, \
             patch.object(svc, "fetch_g1_customer_gnames", new=AsyncMock(return_value={("H001", "GCUST01"): "거래처A"})), \
             patch.object(svc, "count_grouped", new=AsyncMock(return_value=1)):
            items, total = await svc.list_orders(
                server_id="srv", date_from="2026-07-01", date_to="2026-07-31"
            )
        sql = ex.await_args_list[0].args[1]
        self.assertIn("MAX(Idnum+0) AS idnum", sql)
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["order_key"]["idnum"], 7)
        # 키 필드(jubun)는 불변 — idnum 은 표시 전용 부가 필드.
        self.assertEqual(items[0]["order_key"]["jubun"], "11")

    async def test_get_order_detail_returns_line_idnum_max(self) -> None:
        from app.services import outbound_service as svc

        lines = [_line_row(Idnum=7), _line_row(Bcode="B0002", Idnum=7)]
        with patch.object(svc, "execute_query", new=AsyncMock(return_value=lines)), \
             patch.object(svc, "s1_column_names", new=AsyncMock(return_value={
                 "gdate", "hcode", "jubun", "gcode", "bcode", "pubun", "gsqut",
                 "gssum", "yesno", "gdang", "grat1", "gbigo", "idnum",
             })), \
             patch.object(svc, "_fetch_product_names", new=AsyncMock(return_value={})), \
             patch.object(svc, "fetch_g1_customer_gnames", new=AsyncMock(return_value={})):
            detail = await svc.get_order_detail(
                server_id="srv", gdate="2026-07-01", hcode="H001", jubun="11"
            )
        assert detail is not None
        self.assertEqual(detail["order_key"]["idnum"], 7)
        self.assertEqual(detail["order_key"]["jubun"], "11")


class TransactionsStatusSortPassthroughTests(TestCase):
    """거래현황 파사드가 sortBy/sortDir 를 서비스로 전달하는지(컬럼 정렬)."""

    def setUp(self) -> None:
        from fastapi.testclient import TestClient
        from app.main import app
        from app.routers.auth import get_current_user

        def _override_auth() -> dict:
            return {"user_id": "u1", "server_id": "srv"}

        self._prev_override = app.dependency_overrides.get(get_current_user)
        app.dependency_overrides[get_current_user] = _override_auth
        self.app = app
        self.client = TestClient(app)

    def tearDown(self) -> None:
        from app.routers.auth import get_current_user

        if self._prev_override is not None:
            self.app.dependency_overrides[get_current_user] = self._prev_override
        else:
            self.app.dependency_overrides.pop(get_current_user, None)

    @patch("app.routers.transactions.transactions_service.list_sales_statements", new_callable=AsyncMock)
    def test_status_list_passes_sort_params(self, list_mock: AsyncMock) -> None:
        list_mock.return_value = ([], 0)
        res = self.client.get(
            "/api/v1/transactions/status",
            params={
                "serverId": "srv",
                "view": "list",
                "dateFrom": "2026-07-01",
                "dateTo": "2026-07-31",
                "sortBy": "idnum",
                "sortDir": "desc",
            },
        )
        self.assertEqual(res.status_code, 200, res.text)
        kwargs = list_mock.await_args.kwargs
        self.assertEqual(kwargs["sort_by"], "idnum")
        self.assertEqual(kwargs["sort_dir"], "desc")
