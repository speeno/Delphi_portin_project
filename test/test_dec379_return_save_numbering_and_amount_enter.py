"""DEC-379 — 반품 · 폐기 저장 500(전표 채번 호출 오류) + 금액 Enter 재계산 (교문사 2026-10-07).

1. 「반품 신규명세서 저장 안 됨」 — Render 로그: `POST /api/v1/returns 500 … _generate_jubun() takes 0 positional
   arguments but 1 was given`. 반품 · 폐기 · 반품 가져오기가 동기 · 무인자 함수를 `await f(server_id)` 로 불렀다.
   테스트는 이 함수를 AsyncMock 으로 바꿔 끼워 **실제 호출 형태를 한 번도 검사하지 않았다** → 여기서는 모킹하지 않고 진짜 경로를 탄다.
   수정: 출고와 같은 채번 — Jubun = (일자 · 회사 · 거래처) 다음 차수, Idnum = 일자별 전표번호(컬럼 있을 때).
2. 「금액을 지운 뒤 수량 · 공급율 · 정가를 Enter 로 넘겨도 금액이 안 바뀜」 — 값이 바뀔 때만 계산했다 → Enter 에도 재계산.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import outbound_service as obs
from app.services import returns_service as svc

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class SaveUsesRealNumbering(IsolatedAsyncioTestCase):
    async def _run(self, cols: set[str], creator: str) -> list[tuple[str, tuple]]:
        captured: list[tuple[str, tuple]] = []

        async def fake_query(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "MAX(Jubun+0)" in sql:
                return [{"mx": 3}]
            if "Idnum" in sql and "MAX" in sql:
                return [{"mx": 41}]
            return []

        async def fake_tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1] * len(ops)

        with patch.object(obs, "execute_query", AsyncMock(side_effect=fake_query)), \
             patch("app.services.slip_numbering.execute_query", AsyncMock(side_effect=fake_query)), \
             patch.object(svc, "s1_column_names", AsyncMock(return_value=cols)), \
             patch.object(svc, "_default_outbound_ocode", return_value="A"), \
             patch.object(svc, "execute_in_transaction", AsyncMock(side_effect=fake_tx)):
            if creator == "return":
                await svc.create_return(
                    server_id="remote_153",
                    header={"gdate": "2026-10-07", "hcode": "5019", "gcode": "00238"},
                    lines=[{"bcode": "3411", "pubun": "정품", "gsqut": 1, "gdang": 30000, "grat1": 85}],
                    memo=None,
                )
            else:
                with patch.object(svc, "resolve_scrap_customer", AsyncMock(return_value=("05210", "애플2"))):
                    await svc.create_scrap(
                        server_id="remote_153",
                        header={"gdate": "2026-10-07", "hcode": "5019"},
                        lines=[{"bcode": "3411", "pubun": "정품", "gsqut": 2, "gdang": 30000}],
                        memo=None,
                    )
        return captured

    async def test_return_save_numbers_like_outbound(self) -> None:
        ops = await self._run({"idnum"}, "return")
        sql, params = ops[0]
        self.assertIn("Idnum", sql)
        self.assertEqual(sql.count("%s"), len(params))
        self.assertEqual(params[2], "4")  # Jubun = 거래처 다음 차수
        self.assertEqual(params[-1], 42)  # Idnum = 일자별 다음 번호

    async def test_return_save_without_idnum_column(self) -> None:
        ops = await self._run(set(), "return")
        sql, params = ops[0]
        self.assertNotIn("Idnum", sql)
        self.assertEqual(sql.count("%s"), len(params))

    async def test_scrap_save(self) -> None:
        ops = await self._run({"idnum"}, "scrap")
        sql, params = ops[0]
        self.assertIn("'폐기'", sql)
        self.assertEqual(sql.count("%s"), len(params))
        self.assertEqual(params[2], "4")

    def test_no_await_on_sync_jubun(self) -> None:
        import re

        src = inspect.getsource(svc)
        self.assertIsNone(re.search(r"^\s*\w+\s*=\s*await _generate_jubun", src, re.M))
        self.assertFalse(inspect.iscoroutinefunction(obs._generate_jubun))  # noqa: SLF001


class AmountRecalcOnEnter(TestCase):
    def test_enter_recalculates(self) -> None:
        src = (FE / "components" / "outbound" / "order-line-grid.tsx").read_text(encoding="utf-8")
        self.assertIn("function recalcOnEnter(idx: number", src)
        self.assertEqual(src.count("onKeyDown={(e) => recalcOnEnter(idx, e)}"), 3)  # 공급율 · 수량 · 단가


if __name__ == "__main__":
    main()
