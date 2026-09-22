"""DEC-298 — 신규 출고 주문 거래처 참조 「전일미수 불러오기」 + 거래처명 제외 (2026-09-22).

원문: "신규출고주문 화면에 거래처 참조 : (거래처관리 자료) 거래처명 제외하고, 「전일미수」 기능이 기존
화면에서 누락되어 해당 기능을 추가해줘" (레거시 거래명세서-(본사) 캡처: CheckBox1 전일미수불러오기 +
Edit208 전일미수 1,838,520).

레거시 정본 — Subu21.Button301Click: ``if CheckBox1.Checked then Tong40.SetTring01('X', Edit101(거래일자), '',
Edit104(거래처코드), '')`` → ``Edit208 := GsumX``. SetTring01 = ``_Sv_Chng_`` 경로(스냅샷 Gdate < 거래일자 +
S1/H1/Sg_Gsum 창 합산) — 원장 전일미수 ``_opening_receivable``(DEC-165, 앵커 1015 대사)과 같은 식이라 재사용.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import customer_txn_ledger_service as svc  # noqa: E402

FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _user() -> dict:
    return {"user_id": "kyomun", "server_id": "remote_153", "hcode": "5019", "role": "user"}


class OpeningReceivableServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_delegates_to_ledger_opening_with_dotted_date(self) -> None:
        with patch.object(svc, "_opening_receivable", AsyncMock(return_value=1838520)) as m:
            res = await svc.opening_receivable(
                server_id="remote_153", hcode="5019", gcode="1015", date="2026-09-22",
            )
        self.assertEqual(res, {"gcode": "1015", "date": "2026.09.22", "prev_receivable": 1838520})
        m.assert_awaited_once_with("remote_153", hcode="5019", gcode="1015", date_from="2026.09.22")

    async def test_validation(self) -> None:
        with self.assertRaises(ValueError):
            await svc.opening_receivable(server_id="r", hcode=None, gcode=" ", date="2026-09-22")
        with self.assertRaises(ValueError):
            await svc.opening_receivable(server_id="r", hcode=None, gcode="1015", date="2026-9")

    async def test_composition_matches_tong40(self) -> None:
        """스냅샷(Gssum−Gsusu) + S1 Σ Gssum − H1 입금 + H1 출금 + Sg_Gsum — 거래일자 **미만** 창."""

        seen: list[tuple[str, tuple]] = []

        async def fake_query(server_id, sql, params=None):
            seen.append((sql, tuple(params or ())))
            if "MAX(Gdate)" in sql:
                return [{"d": "2026.08.31"}]
            if "FROM Sv_Chng" in sql:
                return [{"s": 5000, "u": 1000}]
            if "FROM S1_Ssub" in sql:
                return [{"s": 700}]
            if "FROM H1_Ssub" in sql:
                return [{"inp": 300, "outp": 20}]
            if "FROM Sg_Gsum" in sql:
                return [{"b": -50}]
            return []

        with patch.object(svc, "execute_query", AsyncMock(side_effect=fake_query)):
            res = await svc.opening_receivable(
                server_id="remote_153", hcode="5019", gcode="1015", date="2026-09-22",
            )
        self.assertEqual(res["prev_receivable"], 5000 - 1000 + 700 - 300 + 20 - 50)
        snap_sql, snap_par = seen[0]
        self.assertIn("Gdate < %s", snap_sql)
        self.assertEqual(snap_par, ("2026.09.22", "5019"))
        for sql, par in seen[1:]:
            self.assertIn("Hcode=%s", sql)  # 격리 hcode 가 전 소스에 바인딩
            self.assertIn("5019", par)


class OpeningReceivableRouteTest(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _user
        self.client = TestClient(app)

    def test_route_scopes_hcode_and_returns_amount(self) -> None:
        with patch.object(svc, "opening_receivable", AsyncMock(return_value={
            "gcode": "1015", "date": "2026.09.22", "prev_receivable": 1838520,
        })) as m:
            res = self.client.get(
                "/api/v1/inventory/customer-ledger/opening?serverId=remote_153&gcode=1015&date=2026-09-22"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["prev_receivable"], 1838520)
        self.assertEqual(m.await_args.kwargs["hcode"], "5019")  # 무입력 → JWT scope 자동 주입

    def test_route_rejects_other_tenant_hcode(self) -> None:
        with patch.object(svc, "opening_receivable", AsyncMock()) as m:
            res = self.client.get(
                "/api/v1/inventory/customer-ledger/opening?serverId=remote_153&gcode=1015&date=2026-09-22&hcode=9999"
            )
        self.assertEqual(res.status_code, 403)
        m.assert_not_awaited()

    def test_route_bad_date_is_422(self) -> None:
        res = self.client.get(
            "/api/v1/inventory/customer-ledger/opening?serverId=remote_153&gcode=1015&date=bad"
        )
        self.assertEqual(res.status_code, 422)


class OutboundNewPanelWiring(unittest.TestCase):
    def setUp(self) -> None:
        self.page = (FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx").read_text(encoding="utf-8")
        self.panel = (FE / "components" / "transactions" / "sales-statement-reference-panel.tsx").read_text(encoding="utf-8")

    def test_customer_name_excluded_here_only(self) -> None:
        self.assertIn("showCustomerName={false}", self.page)
        self.assertIn("showCustomerName = true,", self.panel)

    def test_prev_receivable_checkbox_and_field(self) -> None:
        self.assertIn('data-legacy-id="Sobo21.CheckBox1"', self.panel)
        self.assertIn('data-legacy-id="Sobo21.Edit208"', self.panel)
        self.assertIn("prevReceivable={{", self.page)
        # 체크했을 때만 조회(레거시 기본 해제), 거래일자·확정 거래처 기준.
        self.assertIn("if (!serverId || !customerCode || !prevRecvOn || !gdate)", self.page)
        self.assertIn(".customerOpeningReceivable({ serverId, gcode: customerCode, date: gdate })", self.page)

    def test_probe_matrix_registers_route(self) -> None:
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("/api/v1/inventory/customer-ledger/opening?", probe)


if __name__ == "__main__":
    unittest.main()
