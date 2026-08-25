"""DEC-206 — 거래 명세서 상세 팝업: 거래일자 수정 + 팝업 드래그 이동 (2026-08-25 15:39 사용자 요청).

원문: "날짜도 수정 가능하게 요청합니다." / "팝업창을 원하는 위치로 이동하게 될까요?"

- 백엔드: `PUT /api/v1/outbound/orders/{key}` 에 `newGdate` — 현재 일자와 다르면 라인 diff 보다 먼저
  이 전표(거래처·지점 스코프)의 Gdate 를 옮기고 이후 diff 는 새 일자 키로(DEC-078 과 같은 정밀 스코프,
  전표번호 Idnum 유지). 응답 order_key.gdate = 새 일자.
- 프론트: 상세 팝업 일자 = DateFieldYMD, 「라인 저장」 시 함께 저장 → 일자 바뀌면 목록 새로고침 후 닫힘.
  팝업 헤더 드래그(`useDraggablePanel`) — 상세/입고 상세/검색 팝업 공통.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import outbound_service as svc  # noqa: E402

CURRENT = [
    {"Gdate": "2026.08.25", "Hcode": "5019", "Jubun": "3", "Gcode": "00047", "Bcode": "208", "Pubun": "위탁",
     "Gsqut": 1, "Gssum": 0, "Yesno": "", "Gjisa": "", "Gubun": "출고", "Ocode": "A", "Scode": "X", "Idnum": 72},
]


class UpdateOrderDateMoveTests(IsolatedAsyncioTestCase):
    def _run(self, new_gdate):
        calls: list = []

        async def fake_query(server_id, sql, params=()):
            calls.append(("Q", sql, params))
            return list(CURRENT)

        async def fake_tx(server_id, statements):
            calls.append(("TX", statements))

        async def fake_cols(server_id):
            return {"gdate", "hcode", "jubun", "gjisa", "gcode", "bcode", "gubun", "ocode", "scode", "yesno", "pubun", "gsqut", "gssum", "idnum"}

        return calls, patch.object(svc, "execute_query", fake_query), patch.object(svc, "execute_in_transaction", fake_tx), patch.object(svc, "s1_column_names", fake_cols)

    async def test_move_runs_first_and_scoped_then_diff_uses_new_date(self) -> None:
        calls, p1, p2, p3 = self._run("2026-08-27")
        with p1, p2, p3:
            res = await svc.update_order(
                server_id="remote_153", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 2, "gssum": 0}],
                new_gdate="2026-08-27",
            )
        self.assertEqual(res["order_key"]["gdate"], "2026.08.27")
        txs = [c for c in calls if c[0] == "TX"]
        self.assertEqual(len(txs), 1)
        stmts = txs[0][1]
        self.assertIn("UPDATE S1_Ssub SET Gdate=%s", stmts[0][0], "이동이 첫 문장")
        self.assertIn("Hcode=%s", stmts[0][0])
        self.assertIn("Gcode", stmts[0][0], "거래처 스코프")
        self.assertEqual(stmts[0][1][0], "2026.08.27")
        self.assertEqual(stmts[0][1][1], "2026.08.25", "WHERE 는 옛 일자")
        # 수량 1→2 UPDATE 는 새 일자 키로
        upd = [s for s in stmts[1:] if s[0].startswith("UPDATE")]
        self.assertTrue(upd)
        self.assertIn("2026.08.27", upd[0][1])
        self.assertNotIn("2026.08.25", upd[0][1])

    async def test_same_date_does_not_move(self) -> None:
        calls, p1, p2, p3 = self._run("2026.08.25")
        with p1, p2, p3:
            res = await svc.update_order(
                server_id="remote_153", gdate="2026.08.25", hcode="5019", jubun="3", gcode="00047",
                desired_lines=[{"gcode": "00047", "bcode": "208", "pubun": "위탁", "gsqut": 1, "gssum": 0}],
                new_gdate="2026-08-25",
            )
        self.assertEqual(res["order_key"]["gdate"], "2026.08.25")
        self.assertEqual([c for c in calls if c[0] == "TX"], [], "변경 없음 → 트랜잭션 없음")


class ContractGuard(TestCase):
    def test_request_model_and_router_pass_new_gdate(self) -> None:
        from app.models.outbound import OrderUpdateRequest

        req = OrderUpdateRequest.model_validate({"orderLines": [], "newGdate": "2026-08-27"})
        self.assertEqual(req.new_gdate, "2026-08-27")
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers" / "outbound.py").read_text(encoding="utf-8")
        self.assertIn('**({"new_gdate": payload.new_gdate} if payload.new_gdate else {})', src)


class FrontendWiring(TestCase):
    def test_detail_dialog_edits_date_and_moves(self) -> None:
        src = (FRONT / "components" / "outbound" / "order-detail-dialog.tsx").read_text(encoding="utf-8")
        self.assertIn('legacyId="Sobo24.Detail.Gdate"', src)
        self.assertIn("{ newGdate: dateChanged ? draftGdate : undefined }", src)
        self.assertIn("(저장 시 이동)", src)
        # 일자가 바뀌면 낡은 키의 팝업은 닫고 목록 새로고침
        self.assertIn("if (dateChanged) {\n        // 키(일자)가 바뀌어 이 팝업의 orderKey 는 낡았다", src)
        api = (FRONT / "lib" / "outbound-api.ts").read_text(encoding="utf-8")
        self.assertIn("opts?: { newGdate?: string }", api)

    def test_dialogs_are_draggable_by_header(self) -> None:
        hook = (FRONT / "components" / "shared" / "use-draggable-panel.ts").read_text(encoding="utf-8")
        self.assertIn("export function useDraggablePanel", hook)
        self.assertIn("setPointerCapture", hook)
        self.assertIn("transform: `translate(", hook)
        for rel in (
            "components/outbound/order-detail-dialog.tsx",
            "components/inbound/receipt-detail-dialog.tsx",
            "components/master/master-lookup-dialog.tsx",
        ):
            src = (FRONT / rel).read_text(encoding="utf-8")
            self.assertIn("useDraggablePanel(open)", src, rel)
            self.assertIn("style={drag.panelStyle}", src, rel)
            self.assertIn("{...drag.handleProps}", src, rel)


if __name__ == "__main__":
    main()
