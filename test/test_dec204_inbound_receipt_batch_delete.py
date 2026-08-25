"""DEC-204 — 입고현황 「선택 삭제」: 입고 명세서 통째 삭제 (2026-08-25 사용자 요청).

원문: "해당 명세서를 완전 삭제하라고 하는데 안 되는 것 같습니다. 명세서 '선택' 삭제도 추가 가능할까요?
입고 명세서 통째 선택 삭제 기능을 추가해주세요."

결정
----
- 새 라우트 ``DELETE /api/v1/inbound/receipts/{receipt_key}`` — 전표의 입고 라인(``Scode='Y'``) 전부 DELETE.
  스코프는 취소와 같은 ``_SQL_INBOUND_ROW_WHERE`` (헤더키 + Scode='Y') → 같은 키의 출고 전표는 무사.
- 상태(Yesno) 잠금 없음 — 레거시 입고 폼(Subu22)에 삭제 잠금이 없고 요청이 「완전 삭제」다
  (출고 거래명세서 삭제의 완료/확정 잠금 DEC 과 다름).
- 메모(S1_Memo, 헤더키만)는 같은 헤더키 라인이 0건일 때만 삭제(출고 전표와 메모 공유 가능).
- hcode 는 로그인 소유로 고정(enforce_hcode_identity), audit.inbound 'deleted'.
- 화면: 입고축(입고현황·신간발행)에만 「선택 삭제 (N건)」 destructive 버튼 + ConfirmDialog(danger),
  순차 삭제 후 결과 요약·목록 재조회. 출고축엔 렌더하지 않는다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import inbound_service as svc  # noqa: E402


class DeleteReceiptServiceTests(IsolatedAsyncioTestCase):
    def _patches(self, select_rows, left_count):
        calls: list[tuple[str, tuple]] = []

        async def fake_query(server_id, sql, params=()):
            calls.append(("Q", sql, params))
            if "SELECT IFNULL(Yesno" in sql:
                return select_rows
            if "COUNT(*)" in sql:
                return [{"c": left_count}]
            return []

        async def fake_tx(server_id, statements):
            calls.append(("TX", statements))
            return None

        return calls, patch.object(svc, "execute_query", fake_query), patch.object(svc, "execute_in_transaction", fake_tx)

    async def test_deletes_all_lines_scoped_to_inbound_and_memo_when_empty(self) -> None:
        calls, p1, p2 = self._patches([{"y": "0"}, {"y": "1"}], left_count=0)
        with p1, p2:
            res = await svc.delete_receipt(server_id="remote_153", gdate="2026-08-23", hcode="5019", gcode="A0001", jubun="00002")
        self.assertEqual(res["status"], "deleted")
        self.assertEqual(res["deleted"], 2, "라인 2건 — 상태 잠금 없음(Yesno '1' 포함 삭제)")
        self.assertTrue(res["memo_deleted"])
        txs = [c for c in calls if c[0] == "TX"]
        self.assertEqual(len(txs), 2)
        line_sql = txs[0][1][0][0]
        self.assertIn("DELETE FROM S1_Ssub", line_sql)
        self.assertIn("Scode='Y'", line_sql, "출고 전표 보호 — 입고 라인만")
        self.assertIn("Hcode=%s", line_sql, "hcode 격리")
        self.assertEqual(txs[0][1][0][1], ("2026.08.23", "5019", "A0001", "00002"))
        self.assertIn("DELETE FROM S1_Memo", txs[1][1][0][0])

    async def test_memo_kept_when_other_lines_remain(self) -> None:
        calls, p1, p2 = self._patches([{"y": ""}], left_count=3)
        with p1, p2:
            res = await svc.delete_receipt(server_id="remote_153", gdate="2026.08.23", hcode="5019", gcode="A0001", jubun="00002")
        self.assertFalse(res["memo_deleted"])
        self.assertEqual(len([c for c in calls if c[0] == "TX"]), 1, "같은 헤더키 출고 라인이 남으면 메모 유지")

    async def test_not_found_returns_none_without_delete(self) -> None:
        calls, p1, p2 = self._patches([], left_count=0)
        with p1, p2:
            res = await svc.delete_receipt(server_id="remote_153", gdate="2026.08.23", hcode="5019", gcode="A0001", jubun="00002")
        self.assertIsNone(res)
        self.assertEqual([c for c in calls if c[0] == "TX"], [])


class RouteAndAuditGuard(TestCase):
    def test_delete_route_registered(self) -> None:
        from app.routers import inbound as r

        methods = {
            m for x in r.router.routes if x.path.endswith("/receipts/{receipt_key}") for m in x.methods
        }
        self.assertIn("DELETE", methods)
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers" / "inbound.py").read_text(encoding="utf-8")
        i = src.index("async def delete_receipt(")
        body = src[i : i + 2200]
        self.assertIn('enforce_hcode_identity(hcode, current, field="hcode")', body)
        self.assertIn('action="deleted"', body)

    def test_audit_action_vocab(self) -> None:
        import typing

        from app.services import audit_service

        self.assertIn("deleted", typing.get_args(audit_service.InboundAction))


class ScreenWiring(TestCase):
    def setUp(self) -> None:
        self.src = (FRONT / "components" / "transactions" / "transaction-status-screen.tsx").read_text(encoding="utf-8")

    def test_button_only_on_inbound_axis(self) -> None:
        self.assertIn('data-legacy-id="Sobo24.BatchDelete"', self.src)
        self.assertIn("{!isOutbound && checkedKeys.size > 0 && (", self.src)
        self.assertIn('variant="destructive"', self.src)
        self.assertIn("선택 삭제 (${checkedKeys.size}건)", self.src)

    def test_confirm_dialog_is_danger_and_batch_deletes(self) -> None:
        self.assertIn('title="입고 명세서 삭제"', self.src)
        i = self.src.index("async function doBatchDelete()")
        fn = self.src[i : self.src.index("async function doBatchReprint()")]
        self.assertIn("inboundApi.delete(key, sid)", fn)
        self.assertIn("if (!sid || isOutbound) return;", fn, "출고축 차단")
        self.assertIn("void load(0);", fn, "삭제 후 목록 재조회")
        self.assertIn("setCheckedKeys(new Set())", fn)
        api = (FRONT / "lib" / "inbound-api.ts").read_text(encoding="utf-8")
        self.assertIn("api.delete<ReceiptDeleteResponse>(", api)


if __name__ == "__main__":
    main()
