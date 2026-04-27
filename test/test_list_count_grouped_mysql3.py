"""list LIST 화면 4종(C2/C3/C4/C6) — mysql3 derived-table 우회 회귀.

원인
----
2026-04-21 이전, 출고접수(C2 list_orders) / 입고접수(C3 list_receipts) /
거래명세서(C6 list_sales_statements) / 반품(C4 list_returns_paged) 의 ``count_sql``
은 ``SELECT COUNT(*) FROM (subquery) t`` 파생 테이블 패턴이었다. MySQL 3.23
호환 서버(``servers.yaml`` ``mysql3_protocol: true``)는 derived table 미지원
→ 1064 SQL syntax error → HTTP 500 발생. 출고현황(Sobo67) 만 별도 분기로
살아남아 사용자 체감 “출고현황만 정상” 으로 보였다.

수정
----
``app.core.sql_mysql3.count_grouped`` 공통 헬퍼 도입 — modern 은 derived,
mysql3 는 단일 GROUP BY 결과 ``len(rows)``. 4개 list 함수 모두 동일 헬퍼 사용.

본 테스트
---------
- mysql3_protocol True 일 때 ``count_grouped`` 가 derived 가 아닌 단일 GROUP BY
  SQL 만 발행함을 캡처한 SQL 텍스트로 직접 검증.
- 4개 서비스 list 함수가 ``count_grouped`` 를 호출함을 spy 로 검증
  (실제 SQL 실행은 mock — DB 의존 0).
- 거래명세서 hcode 옵셔널 정책 — 빈 hcode 일 때 ``Hcode = %s`` 절이
  WHERE/COUNT 양쪽에서 빠지는지 검증.

테스트 격리
-----------
``app.services.*`` 모듈은 모듈 단위로 import 되어 있으므로, ``count_grouped``
임포트 위치를 그 모듈에서 patch 해야 한다 (이미 from-import 된 alias 패치).
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
# 1) sql_mysql3.count_grouped — 단위 테스트
# ---------------------------------------------------------------

class CountGroupedMysql3PathTests(IsolatedAsyncioTestCase):
    @patch("app.core.sql_mysql3.mysql3_protocol", return_value=True)
    async def test_mysql3_no_derived_table_uses_len(self, _m: Any) -> None:
        from app.core import sql_mysql3 as mod

        captured: dict[str, Any] = {}

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured["sql"] = sql
            captured["params"] = params
            return [{"Gdate": "2026.04.01", "Hcode": f"H{i:03d}", "_ym": "1"} for i in range(7)]

        with patch("app.core.db.execute_query", new=fake_exec):
            total = await mod.count_grouped(
                "srv_x",
                table="S1_Ssub",
                where_sql="Gdate >= %s AND Gdate <= %s",
                group_by="Gdate, Hcode",
                having="HAVING MAX(Yesno) <> '2'",
                params=("2026.01.01", "2026.04.30"),
            )
        self.assertEqual(total, 7)
        self.assertNotIn("FROM (", captured["sql"], "mysql3 경로는 derived table 금지")
        self.assertIn("GROUP BY Gdate, Hcode", captured["sql"])
        self.assertIn("HAVING MAX(Yesno) <> '2'", captured["sql"])

    @patch("app.core.sql_mysql3.mysql3_protocol", return_value=False)
    async def test_modern_uses_derived_count(self, _m: Any) -> None:
        from app.core import sql_mysql3 as mod

        captured: dict[str, Any] = {}

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured["sql"] = sql
            return [{"total": 42}]

        with patch("app.core.db.execute_query", new=fake_exec):
            total = await mod.count_grouped(
                "srv_modern",
                table="S1_Ssub",
                where_sql="1=1",
                group_by="Gdate, Hcode, Jubun",
            )
        self.assertEqual(total, 42)
        self.assertIn("SELECT COUNT(*) AS total FROM (", captured["sql"])
        self.assertIn("GROUP BY Gdate, Hcode, Jubun", captured["sql"])


# ---------------------------------------------------------------
# 2) 4개 list 서비스 함수가 count_grouped 헬퍼를 호출하는지 검증
# ---------------------------------------------------------------

def _row_outbound() -> dict[str, Any]:
    return {
        "Gdate": "2026.04.01",
        "Hcode": "H001",
        "Jubun": "J1",
        "stmt_gcode": "GCUST01",
        "line_count": 1,
        "qty": 1,
        "amount": 1000,
        "yesno_max": "1",
    }


def _row_inbound() -> dict[str, Any]:
    return {
        "Gdate": "2026.04.01",
        "Hcode": "H001",
        "Gcode": "V001",
        "Jubun": "J1",
        "line_count": 1,
        "qty": 1,
        "amount": 1000,
        "yesno_max": "1",
    }


def _row_sales() -> dict[str, Any]:
    return {
        "Gdate": "2026.04.01",
        "Hcode": "H001",
        "Jubun": "J1",
        "Gjisa": "",
        "stmt_gcode": "GCUST01",
        "row_count": 1,
        "qty": 1,
        "amount": 1000,
        "yesno_max": "1",
    }


def _row_returns() -> dict[str, Any]:
    return {
        "Gdate": "2026.04.01",
        "Hcode": "H001",
        "Jubun": "J1",
        "line_count": 1,
        "qty": 1,
        "amount": 1000,
        "yesno_max": "1",
    }


class ListUsesCountGroupedTests(IsolatedAsyncioTestCase):
    """4개 list 함수가 derived 우회 헬퍼를 사용하는지 호출 캡처."""

    async def _verify(
        self,
        module_path: str,
        call_kwargs: dict[str, Any],
        rows: list[dict[str, Any]],
        names_attr: str,
        names_value: dict[str, str],
        list_fn_name: str,
        expected_group_by: str,
        names_attr2: str | None = None,
        names_value2: dict[str, str] | None = None,
    ) -> None:
        with patch(f"{module_path}.execute_query", new=AsyncMock(return_value=rows)) as exec_mock, \
             patch(f"{module_path}.{names_attr}", new=AsyncMock(return_value=names_value)), \
             patch(f"{module_path}.count_grouped", new=AsyncMock(return_value=999)) as cg_mock:
            if names_attr2:
                with patch(f"{module_path}.{names_attr2}", new=AsyncMock(return_value=names_value2 or {})):
                    await self._invoke(module_path, list_fn_name, call_kwargs)
            else:
                await self._invoke(module_path, list_fn_name, call_kwargs)

            cg_mock.assert_awaited_once()
            kwargs = cg_mock.await_args.kwargs
            self.assertEqual(kwargs["group_by"], expected_group_by)
            self.assertEqual(kwargs["table"], "S1_Ssub")
            # data SELECT 는 1번만 — derived count 분기 제거 확인.
            self.assertEqual(exec_mock.await_count, 1)

    async def _invoke(self, module_path: str, fn_name: str, kwargs: dict[str, Any]) -> Any:
        import importlib

        mod = importlib.import_module(module_path)
        return await getattr(mod, fn_name)(**kwargs)

    async def test_outbound_list_orders(self) -> None:
        await self._verify(
            module_path="app.services.outbound_service",
            call_kwargs={
                "server_id": "srv",
                "date_from": "2026-04-01",
                "date_to": "2026-04-30",
            },
            rows=[_row_outbound()],
            names_attr="fetch_g1_customer_gnames",
            names_value={("H001", "GCUST01"): "거래처A"},
            list_fn_name="list_orders",
            expected_group_by="Gdate, Hcode, COALESCE(Jubun,'')",
        )

    async def test_inbound_list_receipts(self) -> None:
        await self._verify(
            module_path="app.services.inbound_service",
            call_kwargs={
                "server_id": "srv",
                "date_from": "2026-04-01",
                "date_to": "2026-04-30",
            },
            rows=[_row_inbound()],
            names_attr="_fetch_publisher_names",
            names_value={"H001": "출판사A"},
            names_attr2="_fetch_vendor_names",
            names_value2={"V001": "벤더A"},
            list_fn_name="list_receipts",
            expected_group_by="Gdate, Hcode, COALESCE(Gcode,''), COALESCE(Jubun,'')",
        )

    async def test_transactions_list_sales_statements_no_hcode(self) -> None:
        """hcode 빈 값일 때 전체 거래처 대상 — 2026-04-21 정책 회귀."""
        await self._verify(
            module_path="app.services.transactions_service",
            call_kwargs={
                "server_id": "srv",
                "hcode": None,
                "date_from": "2026-04-01",
                "date_to": "2026-04-30",
            },
            rows=[_row_sales()],
            names_attr="fetch_g1_customer_gnames",
            names_value={("H001", "GCUST01"): "거래처A", ("", "GCUST01"): "거래처A"},
            list_fn_name="list_sales_statements",
            expected_group_by="Gdate, Hcode, COALESCE(Jubun,''), COALESCE(Gjisa,'')",
        )

    async def test_returns_list(self) -> None:
        # returns_service.list_returns: data SELECT 1회 + publisher lookup 1회.
        # publisher lookup 은 ``in_clause_lookup`` 헬퍼 경유 — 헬퍼 자체를 stub.
        from app.services import returns_service as rs

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            return [_row_returns()]

        with patch("app.services.returns_service.execute_query", new=fake_exec), \
             patch("app.services.returns_service.in_clause_lookup",
                   new=AsyncMock(return_value=[{"hcode": "H001", "hname": "출판사A"}])), \
             patch("app.services.returns_service.count_grouped", new=AsyncMock(return_value=99)) as cg_mock:
            await rs.list_returns(
                server_id="srv",
                date_from="2026-04-01",
                date_to="2026-04-30",
                limit=10,
                offset=0,
            )
            cg_mock.assert_awaited_once()
            self.assertEqual(cg_mock.await_args.kwargs["group_by"], "Gdate, Hcode, Jubun")
            self.assertEqual(cg_mock.await_args.kwargs["table"], "S1_Ssub")


# ---------------------------------------------------------------
# 3) 거래명세서 hcode 옵셔널 — WHERE 절에 Hcode 가 빠지는지
# ---------------------------------------------------------------

class TransactionsSalesStatementHcodeOptionalTests(IsolatedAsyncioTestCase):
    async def test_no_hcode_means_all_customers(self) -> None:
        from app.services import transactions_service as ts

        captured_sql: list[str] = []
        captured_params: list[tuple] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            captured_params.append(params)
            return [_row_sales()]

        with patch("app.services.transactions_service.execute_query", new=fake_exec), \
             patch(
                 "app.services.transactions_service.fetch_g1_customer_gnames",
                 new=AsyncMock(return_value={}),
             ), \
             patch("app.services.transactions_service.count_grouped", new=AsyncMock(return_value=1)) as cg_mock:
            items, total = await ts.list_sales_statements(
                server_id="srv",
                hcode=None,
                date_from="2026-04-01",
                date_to="2026-04-30",
            )

        self.assertEqual(total, 1)
        # data 쿼리에 Hcode = %s 절이 없어야 함.
        joined = "\n".join(captured_sql)
        self.assertNotIn("Hcode = %s", joined)
        self.assertIn("Ocode = 'B'", joined)
        # count_grouped 도 동일 where_sql 사용 (Hcode 없음).
        cg_kwargs = cg_mock.await_args.kwargs
        self.assertNotIn("Hcode = %s", cg_kwargs["where_sql"])

    async def test_with_hcode_keeps_filter(self) -> None:
        from app.services import transactions_service as ts

        captured_sql: list[str] = []
        captured_params: list[tuple] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured_sql.append(sql)
            captured_params.append(params)
            return [_row_sales()]

        with patch("app.services.transactions_service.execute_query", new=fake_exec), \
             patch(
                 "app.services.transactions_service.fetch_g1_customer_gnames",
                 new=AsyncMock(return_value={}),
             ), \
             patch("app.services.transactions_service.count_grouped", new=AsyncMock(return_value=1)) as cg_mock:
            await ts.list_sales_statements(
                server_id="srv",
                hcode="H001",
                date_from="2026-04-01",
                date_to="2026-04-30",
            )

        joined = "\n".join(captured_sql)
        self.assertIn("Hcode = %s", joined)
        cg_kwargs = cg_mock.await_args.kwargs
        self.assertIn("Hcode = %s", cg_kwargs["where_sql"])
        self.assertIn("H001", cg_kwargs["params"])


# ---------------------------------------------------------------
# 4) HTTP 라우터 회귀 — 거래명세서 hcode 미지정 200, 출고/입고 list 200
# ---------------------------------------------------------------

class HttpRouterRegressionTests(TestCase):
    """라우터 단위에서 hcode 옵셔널 + count_grouped 통합 동작 확인."""

    def setUp(self) -> None:
        from fastapi.testclient import TestClient
        from app.main import app
        from app.routers.auth import get_current_user

        def _override_auth() -> dict:
            return {"user_id": "u1", "server_id": "srv"}

        # 이전에 등록된 override 가 있다면 보존했다가 tearDown 에서 복원 — 다른 테스트
        # 파일이 모듈 레벨로 등록한 override 를 의도치 않게 지우지 않도록 한다
        # (사용자 룰 §재귀 오류 방지: 이전 케이스 고려).
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

    @patch("app.services.transactions_service.count_grouped", new_callable=AsyncMock)
    @patch("app.services.transactions_service.fetch_g1_customer_gnames", new_callable=AsyncMock)
    @patch("app.services.transactions_service.execute_query", new_callable=AsyncMock)
    def test_sales_statement_without_hcode_returns_200(
        self,
        mock_exec: AsyncMock,
        mock_names: AsyncMock,
        mock_cg: AsyncMock,
    ) -> None:
        mock_exec.return_value = []
        mock_names.return_value = {}
        mock_cg.return_value = 0
        r = self.client.get(
            "/api/v1/transactions/sales-statement",
            params={
                "serverId": "srv",
                "dateFrom": "2026-04-01",
                "dateTo": "2026-04-30",
                "limit": 50,
                "offset": 0,
            },
        )
        self.assertEqual(r.status_code, 200, r.text)

    @patch("app.services.outbound_service.count_grouped", new_callable=AsyncMock)
    @patch("app.services.outbound_service.fetch_g1_customer_gnames", new_callable=AsyncMock)
    @patch("app.services.outbound_service.execute_query", new_callable=AsyncMock)
    def test_outbound_orders_list_returns_200(
        self,
        mock_exec: AsyncMock,
        mock_names: AsyncMock,
        mock_cg: AsyncMock,
    ) -> None:
        mock_exec.return_value = []
        mock_names.return_value = {}
        mock_cg.return_value = 0
        r = self.client.get(
            "/api/v1/outbound/orders",
            params={
                "serverId": "srv",
                "dateFrom": "2026-04-01",
                "dateTo": "2026-04-30",
                "limit": 50,
                "offset": 0,
            },
        )
        self.assertEqual(r.status_code, 200, r.text)

    @patch("app.services.inbound_service._fetch_vendor_names", new_callable=AsyncMock)
    @patch("app.services.inbound_service._fetch_publisher_names", new_callable=AsyncMock)
    @patch("app.services.inbound_service.count_grouped", new_callable=AsyncMock)
    @patch("app.services.inbound_service.execute_query", new_callable=AsyncMock)
    def test_inbound_receipts_list_returns_200(
        self,
        mock_exec: AsyncMock,
        mock_cg: AsyncMock,
        mock_pub: AsyncMock,
        mock_ven: AsyncMock,
    ) -> None:
        mock_exec.return_value = []
        mock_cg.return_value = 0
        mock_pub.return_value = {}
        mock_ven.return_value = {}
        r = self.client.get(
            "/api/v1/inbound/receipts",
            params={
                "serverId": "srv",
                "dateFrom": "2026-04-01",
                "dateTo": "2026-04-30",
                "limit": 50,
                "offset": 0,
            },
        )
        self.assertEqual(r.status_code, 200, r.text)


if __name__ == "__main__":
    main()
