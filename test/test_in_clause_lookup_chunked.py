"""IN(...) lookup 청크 분할 — POC `_SOBO67_GNAME_CODES_CHUNK` 정책 회귀.

원인
----
9 개 lookup 함수(_fetch_publisher_names, _fetch_customer_names,
_fetch_product_names, _fetch_vendor_names, inventory/reports book lookup 등)
가 단일 ``WHERE Gcode IN (?,?,...)`` 으로 수백~수천 코드를 묶었다.
`servers.yaml.mysql3_protocol: true` 서버는 raw socket 으로 SQL 을 그대로
받기 때문에 거대 IN 절이 SQL 파싱 stall / read_timeout 을 유발한다 (POC
seak80-sample 이 검증·청크 분할로 해결한 회귀).

수정
----
``app.core.sql_mysql3.in_clause_lookup`` 공통 헬퍼 도입 — placeholders 자리표시
SQL + keys 청크 분할 + dedupe + prefix_params. 9 개 호출처 모두 동일 헬퍼 사용
(SOLID-D / DRY / DEC-053 §회귀 가드 일반화).

본 테스트
---------
- 헬퍼 단위: chunk 경계, dedupe, 빈 keys, 잘못된 template 검증.
- 통합 spy: 9 개 lookup 함수가 모두 ``in_clause_lookup`` 을 거치는지.
- mysql3_protocol 분기와 무관 — 헬퍼는 동일하게 청크 분할 (mysql3 가 우선
  타깃이지만 modern MySQL 에도 stall 회피 효과).

테스트 격리
-----------
- 각 모듈은 ``from app.core.sql_mysql3 import in_clause_lookup`` 으로 alias 를
  잡고 있으므로 ``app.services.<mod>.in_clause_lookup`` 위치를 patch.
- ``app.core.db.execute_query`` 만 monkey patch — 실 DB 의존 0.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


# ---------------------------------------------------------------
# 1) in_clause_lookup 단위 테스트 — 청크 / dedupe / template 검증
# ---------------------------------------------------------------

class InClauseLookupUnitTests(IsolatedAsyncioTestCase):
    async def test_empty_keys_no_query(self) -> None:
        from app.core import sql_mysql3 as mod

        called = {"n": 0}

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            called["n"] += 1
            return []

        with patch("app.core.db.execute_query", new=fake_exec):
            rows = await mod.in_clause_lookup(
                "srv", sql_template="SELECT 1 FROM T WHERE x IN ({placeholders})", keys=[]
            )
        self.assertEqual(rows, [])
        self.assertEqual(called["n"], 0, "빈 keys 면 SQL 호출 0회")

    async def test_dedupe_and_strip(self) -> None:
        from app.core import sql_mysql3 as mod

        captured: list[tuple[str, tuple[Any, ...]]] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append((sql, tuple(params)))
            return [{"k": p} for p in params]

        with patch("app.core.db.execute_query", new=fake_exec):
            rows = await mod.in_clause_lookup(
                "srv",
                sql_template="SELECT k FROM T WHERE k IN ({placeholders})",
                keys=["A", " B ", "A", "", None, "C", "B"],
            )
        self.assertEqual(len(captured), 1, "한 번에 묶이는 크기")
        sql, params = captured[0]
        self.assertEqual(params, ("A", "B", "C"), "공백 strip + 중복 제거 + 순서 보존")
        self.assertEqual(sql.count("%s"), 3)
        self.assertEqual([r["k"] for r in rows], ["A", "B", "C"])

    async def test_chunk_split_by_size(self) -> None:
        from app.core import sql_mysql3 as mod

        captured: list[int] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append(len(params))
            return [{"x": p} for p in params]

        keys = [f"K{i:04d}" for i in range(450)]
        with patch("app.core.db.execute_query", new=fake_exec):
            rows = await mod.in_clause_lookup(
                "srv",
                sql_template="SELECT x FROM T WHERE x IN ({placeholders})",
                keys=keys,
                chunk_size=200,
            )
        self.assertEqual(captured, [200, 200, 50], "청크 크기에 따라 분할")
        self.assertEqual(len(rows), 450, "결과 단순 concat")

    async def test_prefix_params_prepended_each_chunk(self) -> None:
        from app.core import sql_mysql3 as mod

        captured: list[tuple] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append(tuple(params))
            return []

        keys = [f"B{i:03d}" for i in range(5)]
        with patch("app.core.db.execute_query", new=fake_exec):
            await mod.in_clause_lookup(
                "srv",
                sql_template="SELECT 1 FROM T WHERE Hcode=%s AND Gcode IN ({placeholders})",
                keys=keys,
                prefix_params=("H001",),
                chunk_size=2,
            )
        # 5 개 → 2/2/1 청크. 각 호출 첫 인자는 prefix("H001").
        self.assertEqual(len(captured), 3)
        for params in captured:
            self.assertEqual(params[0], "H001")

    async def test_default_chunk_uses_module_default(self) -> None:
        from app.core import sql_mysql3 as mod

        captured: list[int] = []

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            captured.append(len(params))
            return []

        keys = [f"K{i:04d}" for i in range(mod.DEFAULT_IN_CHUNK + 5)]
        with patch("app.core.db.execute_query", new=fake_exec):
            await mod.in_clause_lookup(
                "srv",
                sql_template="SELECT 1 FROM T WHERE x IN ({placeholders})",
                keys=keys,
            )
        self.assertEqual(captured, [mod.DEFAULT_IN_CHUNK, 5])

    async def test_missing_placeholder_raises(self) -> None:
        from app.core import sql_mysql3 as mod

        with self.assertRaises(ValueError):
            await mod.in_clause_lookup(
                "srv",
                sql_template="SELECT 1 FROM T WHERE x = %s",  # 자리표시자 없음
                keys=["A"],
            )


# ---------------------------------------------------------------
# 2) 9 개 lookup 함수가 in_clause_lookup 을 사용하는지 통합 spy
# ---------------------------------------------------------------

class LookupCallersUseHelperTests(IsolatedAsyncioTestCase):
    async def _spy_module(
        self,
        module_path: str,
        callable_name: str,
        *call_args: Any,
        **call_kwargs: Any,
    ) -> AsyncMock:
        import importlib

        mod = importlib.import_module(module_path)
        spy = AsyncMock(return_value=[])
        with patch.object(mod, "in_clause_lookup", new=spy):
            fn = getattr(mod, callable_name)
            await fn(*call_args, **call_kwargs)
        spy.assert_awaited()
        return spy

    async def test_transactions_customer_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.transactions_service",
            "_fetch_customer_names",
            "srv",
            ["H001", "H002"],
        )

    async def test_transactions_product_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.transactions_service",
            "_fetch_product_names",
            "srv",
            "H001",
            ["B001", "B002"],
        )

    async def test_inbound_publisher_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.inbound_service",
            "_fetch_publisher_names",
            "srv",
            ["H001", "H002"],
        )

    async def test_inbound_vendor_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.inbound_service",
            "_fetch_vendor_names",
            "srv",
            ["V001", "V002"],
        )

    async def test_inbound_product_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.inbound_service",
            "_fetch_product_names",
            "srv",
            ["B001", "B002"],
        )

    async def test_outbound_customer_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.outbound_service",
            "_fetch_customer_names",
            "srv",
            ["H001", "H002"],
        )

    async def test_outbound_product_names_uses_helper(self) -> None:
        await self._spy_module(
            "app.services.outbound_service",
            "_fetch_product_names",
            "srv",
            ["B001", "B002"],
        )

    async def test_inventory_book_lookup_uses_helper(self) -> None:
        # DEC-033 (h) — get_inventory_ledger 는 in_clause_lookup 을 두 번 호출한다:
        #   (a) raw 행 fetch — S1_Ssub WHERE Gdate IN (...)
        #   (b) 도서명 lookup — G4_Book WHERE Hcode=? AND Gcode IN (...)
        # 본 테스트는 (b) book lookup 호출의 prefix_params 가 (hcode,) 인지 검증한다.
        from app.services import inventory_service as inv

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            if "Sv_Ghng" in sql:
                return [{"opening_date": "2026.03.31"}]
            if "COUNT(DISTINCT Gdate)" in sql:
                return [{"cnt": 1}]
            if sql.lstrip().startswith("SELECT DISTINCT Gdate"):
                return [{"Gdate": "2026.04.01"}]
            return []

        # raw 행 fetch (a) 시뮬레이터 — book lookup (b) spy 와 분리.
        async def fake_in_lookup(
            server_id: str,
            *,
            sql_template: str,
            keys: Any,
            prefix_params: tuple = (),
            chunk_size: int | None = None,
        ) -> list[dict[str, Any]]:
            if "G4_Book" in sql_template:
                return []
            return [
                {
                    "Gdate": "2026.04.01",
                    "Bcode": "B001",
                    "Scode": "X",
                    "Gubun": "출고",
                    "Pubun": "",
                    "Gbigo": "",
                    "Gsqut": 1,
                    "Gssum": 1000,
                }
            ]

        spy = AsyncMock(side_effect=fake_in_lookup)
        with patch("app.services.inventory_service.execute_query", new=fake_exec), \
             patch("app.services.inventory_service.in_clause_lookup", new=spy):
            await inv.get_inventory_ledger(
                server_id="srv",
                hcode="H001",
                bcode="B001",
                bcode_to=None,
                date_from="2026-04-01",
                date_to="2026-04-30",
            )
        # 두 번 호출됐는지 확인 — (a) raw rows, (b) book names.
        self.assertGreaterEqual(spy.await_count, 2)
        # 마지막 호출 (도서명 lookup) 의 prefix_params 가 (hcode,) 인지 확인.
        last_kwargs = spy.await_args_list[-1].kwargs
        self.assertEqual(last_kwargs.get("prefix_params"), ("H001",))
        self.assertIn("G4_Book", last_kwargs.get("sql_template", ""))

    async def test_reports_book_sales_uses_helper(self) -> None:
        from app.services import reports_service as rs

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            if "S1_Ssub" in sql and "Sg_Csum" not in sql:
                return [
                    {
                        "Bcode": "B001",
                        "Scode": "X",
                        "Gubun": "출고",
                        "Pubun": "",
                        "Gsqut": 1,
                        "Gssum": 100,
                    }
                ]
            return []

        spy = AsyncMock(return_value=[])
        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=spy):
            await rs.get_book_sales(
                server_id="srv",
                hcode="H001",
                date_from="2026-04-01",
                date_to="2026-04-30",
            )
        spy.assert_awaited()

    async def test_reports_customer_sales_uses_helper(self) -> None:
        from app.services import reports_service as rs

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            return [
                {
                    "Hcode": "H001",
                    "Gcode": "G001",
                    "Scode": "X",
                    "Gubun": "출고",
                    "Pubun": "",
                    "Gjisa": "01",
                    "Gsqut": 1,
                    "Gssum": 100,
                }
            ]

        spy = AsyncMock(return_value=[])
        with patch("app.services.reports_service.execute_query", new=fake_exec), \
             patch("app.services.reports_service.in_clause_lookup", new=spy):
            await rs.get_customer_sales(
                server_id="srv",
                hcode="H001",
                date_from="2026-04-01",
                date_to="2026-04-30",
            )
        spy.assert_awaited()

    async def test_returns_list_uses_helper_for_publisher(self) -> None:
        from app.services import returns_service as rs

        async def fake_exec(server_id: str, sql: str, params: tuple) -> list[dict[str, Any]]:
            # 데이터 SELECT (G7_Ggeo lookup 은 helper 가 가로챔)
            return [
                {
                    "Gdate": "2026.04.01",
                    "Hcode": "H001",
                    "Jubun": "001",
                    "yesno_max": "1",
                    "row_count": 1,
                    "qty_sum": 10,
                    "amt_sum": 1000,
                }
            ]

        spy = AsyncMock(return_value=[])
        with patch("app.services.returns_service.execute_query", new=fake_exec), \
             patch("app.services.returns_service.count_grouped", new=AsyncMock(return_value=1)), \
             patch("app.services.returns_service.in_clause_lookup", new=spy):
            await rs.list_returns(
                server_id="srv",
                date_from="2026-04-01",
                date_to="2026-04-30",
                limit=10,
                offset=0,
            )
        spy.assert_awaited()


if __name__ == "__main__":  # pragma: no cover
    main()
