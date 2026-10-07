"""DEC-392 — 출고 명세서 삭제 잠금을 레거시 Subu21 규칙(G7_Ggeo.Chek3 = xChek)으로.

교문사 2026-10-07 22:44 「출고명세 선택 후 삭제가 작동하지 않는다」 — 완료(Yesno '1') 전표 2건이 422(완료 잠금). 레거시 출판 빌드는
``xChek``(G7_Ggeo.Chek3) ≠ 'ok' 이면 Yesno 와 무관하게 삭제를 허용한다(교문사 = 'Jeago'). 웹의 일괄 완료 잠금은 그보다 엄격했다(DEC-364 참고).

가드: Chek3 ≠ 'ok' → 완료 전표도 삭제 · 'ok' → 잠금 · 설정 조회 실패/행 없음 → 잠금(fail-closed) · 반품/폐기 첫 행 기본 수량 -1.
"""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, patch

from app.services import transactions_service as tx


def _exec(yesno: str, chek3):
    async def fake(server_id, sql, params=()):
        if "FROM G7_Ggeo" in sql:
            if chek3 == "ERR":
                raise RuntimeError("Unknown column 'Chek3'")
            return [] if chek3 is None else [{"chek3": chek3}]
        return [{"y": yesno}, {"y": yesno}]
    return fake


class DeleteLockFollowsTenantChek3(unittest.IsolatedAsyncioTestCase):
    async def _delete(self, yesno: str, chek3, confirm: bool = True):
        tr = AsyncMock(return_value=None)
        with patch.object(tx, "execute_query", AsyncMock(side_effect=_exec(yesno, chek3))), \
                patch.object(tx, "execute_in_transaction", tr):
            res = await tx.delete_sales_statement(
                server_id="remote_153", gdate="2026.10.07", hcode="5019", jubun="25", gjisa="", confirm_completed=confirm,
            )
        return res, tr

    async def test_completed_deletable_when_chek3_not_ok(self) -> None:
        res, tr = await self._delete("1", "Jeago")
        self.assertEqual(res["deleted"], 2)
        self.assertEqual(tr.await_count, 1)

    async def test_completed_requires_confirmation(self) -> None:
        """「이미 완료된 전표를 삭제하시겠습니까?」확인 없이 온 요청은 삭제하지 않는다(사용자 2026-10-07)."""
        with self.assertRaises(ValueError) as cm:
            await self._delete("1", "Jeago", confirm=False)
        self.assertEqual(str(cm.exception), "STATEMENT_COMPLETED_CONFIRM")
        res, _ = await self._delete("0", "Jeago", confirm=False)  # 미완료 전표는 확인 없이
        self.assertEqual(res["deleted"], 2)

    async def test_completed_locked_when_chek3_ok(self) -> None:
        with self.assertRaises(ValueError) as cm:
            await self._delete("1", "ok")
        self.assertEqual(str(cm.exception), "STATEMENT_LOCKED")

    async def test_fail_closed_without_setting(self) -> None:
        for chek3 in (None, "ERR"):
            with self.assertRaises(ValueError):
                await self._delete("2", chek3)

    async def test_pending_deletes_without_lookup(self) -> None:
        res, tr = await self._delete("0", "ok")
        self.assertEqual(res["deleted"], 2)


class ConfirmWiring(unittest.TestCase):
    def test_route_and_screens(self) -> None:
        from pathlib import Path
        root = Path(__file__).resolve().parents[1] / "도서물류관리프로그램"
        router = (root / "backend" / "app" / "routers" / "transactions.py").read_text(encoding="utf-8")
        self.assertIn('alias="confirmCompleted"', router)
        self.assertIn('"code": "INQ_TX_COMPLETED_CONFIRM"', router)
        fe = root / "frontend" / "src"
        rd = lambda rel: (fe / rel).read_text(encoding="utf-8").replace("\r\n", "\n")  # noqa: E731
        self.assertIn('confirmCompleted: opts.confirmCompleted ? "1" : undefined', rd("lib/inquiry-api.ts"))
        st = rd("components/transactions/transaction-status-screen.tsx")
        self.assertIn("이미 완료된 전표를 삭제하시겠습니까?", st)
        self.assertIn('confirmCompleted: s.status === "done",', st)
        lp = rd("app/(app)/transactions/sales-statement/page.tsx")
        self.assertIn("이미 완료된 전표를 삭제하시겠습니까?", lp)
        self.assertIn("deleteSalesStatement(ok, sid, { confirmCompleted: done })", lp)


if __name__ == "__main__":
    unittest.main()
