"""거래명세서 인쇄 기능 회귀 — 테두리 토글 / 완료 전이 / 당일 접수 / 일괄 PDF.

DB 부작용 없이 서비스 경계(execute_query / execute_in_transaction / render_pdf /
list_sales_statements / get_sales_statement_detail) 를 monkeypatch 로 막아
SQL/HTML/라우터 계약만 검증한다. 사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import transactions_service as tx  # noqa: E402

_SID = "remote_1"


def _detail() -> dict:
    return {
        "order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": "00001", "gjisa": ""},
        "customer": {"hcode": "H1", "gname": "테스트거래처"},
        "lines": [
            {"gcode": "00001", "bcode": "B1", "product_name": "도서A", "shelf": "",
             "pubun": "위탁", "gsqut": 3, "gdang": 10000, "grat1": 70, "gssum": 21000, "gbigo": ""},
        ],
    }


class BordersToggleTests(TestCase):
    def test_borders_off_hides_chrome_keeps_data(self) -> None:
        off = tx.render_sales_statement_html(
            _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=False
        )
        on = tx.render_sales_statement_html(
            _detail(), layout="legacy_triplicate", server_id=_SID, user_id="u", borders=True
        )
        # 양식지(off): body.preprinted + chrome 숨김 CSS, 데이터는 유지.
        self.assertIn("class='preprinted'", off)
        self.assertIn("visibility: hidden", off)
        self.assertIn("도서A", off)
        self.assertIn("21,000", off)
        # 테두리(on): preprinted 아님, geometry 동일(같은 표 클래스).
        self.assertNotIn("class='preprinted'", on)
        self.assertIn("tri-lines", on)
        self.assertIn("tri-lines", off)  # geometry 보존

    def test_resolve_preprinted_default_off(self) -> None:
        # 명시 인자 우선.
        self.assertTrue(tx.resolve_sales_statement_preprinted(_SID, "u", False))
        self.assertFalse(tx.resolve_sales_statement_preprinted(_SID, "u", True))


class CombinedBatchHtmlTests(TestCase):
    def test_combined_two_statements_pagebreak(self) -> None:
        html = tx.render_sales_statements_combined_html(
            [_detail(), _detail()], layout="legacy_triplicate", server_id=_SID, user_id="u", borders=True
        )
        # 명세서 사이 강제 page-break + 단일 <style>.
        self.assertIn("stmt-wrap", html)
        self.assertIn("page-break-after: always", html)
        self.assertEqual(html.count("<style>"), 1)
        # 두 본문 모두 포함.
        self.assertGreaterEqual(html.count("거래명세서"), 2)

    def test_combined_single_falls_back_to_one(self) -> None:
        html = tx.render_sales_statements_combined_html(
            [_detail()], layout="legacy_triplicate", server_id=_SID, user_id="u"
        )
        self.assertNotIn("stmt-wrap", html)


class MarkCompletedServiceTests(IsolatedAsyncioTestCase):
    async def test_received_to_done_transition(self) -> None:
        calls: list[str] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            calls.append(sql)
            # 첫 SELECT = 접수('0'), 두번째 SELECT(after) = 완료('1').
            sel_count = sum(1 for s in calls if s.strip().upper().startswith("SELECT"))
            return [{"y": "0"}] if sel_count == 1 else [{"y": "1"}]

        tx_mock = AsyncMock()
        with patch.object(tx, "execute_query", side_effect=fake_eq), \
                patch.object(tx, "execute_in_transaction", tx_mock):
            res = await tx.mark_sales_statement_completed(
                server_id=_SID, gdate="2026-06-28", hcode="H1", jubun="00001", gjisa="",
            )
        self.assertIsNotNone(res)
        self.assertEqual(res["status"], "done")
        # UPDATE 가 Yesno='1' 로, 접수('0') 라인만 대상.
        upd_sql = tx_mock.await_args.args[1][0][0]
        self.assertIn("SET Yesno='1'", upd_sql)
        self.assertIn("IFNULL(Yesno,'')='0'", upd_sql)

    async def test_no_rows_returns_none(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            return []

        with patch.object(tx, "execute_query", side_effect=fake_eq), \
                patch.object(tx, "execute_in_transaction", AsyncMock()):
            res = await tx.mark_sales_statement_completed(
                server_id=_SID, gdate="2026-06-28", hcode="H1", jubun="00001", gjisa="",
            )
        self.assertIsNone(res)


class DeleteServiceTests(IsolatedAsyncioTestCase):
    async def test_delete_pending_removes_lines(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            return [{"y": "0"}, {"y": ""}]  # 접수/대기 — 삭제 가능

        del_mock = AsyncMock()
        with patch.object(tx, "execute_query", side_effect=fake_eq), \
                patch.object(tx, "execute_in_transaction", del_mock):
            res = await tx.delete_sales_statement(
                server_id=_SID, gdate="2026-06-28", hcode="H1", jubun="00001", gjisa="",
            )
        self.assertEqual(res["status"], "deleted")
        self.assertEqual(res["deleted"], 2)
        sql = del_mock.await_args.args[1][0][0]
        self.assertIn("DELETE FROM S1_Ssub", sql)

    async def test_delete_completed_locked(self) -> None:
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            return [{"y": "1"}]  # 완료 — 잠금

        del_mock = AsyncMock()
        with patch.object(tx, "execute_query", side_effect=fake_eq), \
                patch.object(tx, "execute_in_transaction", del_mock):
            with self.assertRaises(ValueError) as cm:
                await tx.delete_sales_statement(
                    server_id=_SID, gdate="2026-06-28", hcode="H1", jubun="00001", gjisa="",
                )
        self.assertEqual(str(cm.exception), "STATEMENT_LOCKED")
        del_mock.assert_not_awaited()  # 삭제 미실행

    async def test_delete_no_rows_returns_none(self) -> None:
        with patch.object(tx, "execute_query", side_effect=AsyncMock(return_value=[])), \
                patch.object(tx, "execute_in_transaction", AsyncMock()):
            res = await tx.delete_sales_statement(
                server_id=_SID, gdate="2026-06-28", hcode="H1", jubun="9", gjisa="",
            )
        self.assertIsNone(res)


def _auth() -> dict:
    return {"user_id": "u", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": []}


class RouterTests(TestCase):
    def setUp(self) -> None:
        self._p1 = app.dependency_overrides.get(get_current_user)
        self._p2 = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _auth
        app.dependency_overrides[get_user_context] = _auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in ((get_current_user, self._p1), (get_user_context, self._p2)):
            if prev is not None:
                app.dependency_overrides[dep] = prev
            else:
                app.dependency_overrides.pop(dep, None)

    def test_received_today_filters_received(self) -> None:
        async def fake_list(**kwargs):  # noqa: ARG001
            items = [
                {"order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": "1", "gjisa": "", "idnum": 1, "gubun": "출고", "gcode": "00001"}, "status": "received", "customer_name": "가"},
                {"order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": "2", "gjisa": "", "idnum": 2, "gubun": "출고", "gcode": "00002"}, "status": "done", "customer_name": "나"},
            ]
            return items, len(items)

        with patch.object(tx, "list_sales_statements", side_effect=fake_list):
            r = self.client.get(
                f"/api/v1/transactions/sales-statement/received-today?serverId={_SID}&today=2026-06-28"
            )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["items"][0]["status"], "received")

    def test_complete_endpoint_200(self) -> None:
        async def fake_complete(**kwargs):  # noqa: ARG001
            return {"order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": "1", "gjisa": ""},
                    "status": "done", "updated_at": "t"}

        with patch.object(tx, "mark_sales_statement_completed", side_effect=fake_complete):
            r = self.client.patch(
                f"/api/v1/transactions/sales-statement/2026.06.28%7CH1%7C1%7C/complete?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["status"], "done")

    def test_complete_endpoint_404_when_missing(self) -> None:
        with patch.object(tx, "mark_sales_statement_completed", AsyncMock(return_value=None)):
            r = self.client.patch(
                f"/api/v1/transactions/sales-statement/2026.06.28%7CH1%7C9%7C/complete?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 404, r.text)

    def test_batch_pdf_combines_and_returns_pdf(self) -> None:
        from app.services import print_service

        async def fake_detail(**kwargs):  # noqa: ARG001
            return _detail()

        captured: dict = {}

        def fake_combined(details, **kwargs):  # noqa: ANN001
            captured["n"] = len(details)
            captured["layout"] = kwargs.get("layout")
            return "<html><body>combined</body></html>"

        with patch.object(tx, "get_sales_statement_detail", side_effect=fake_detail), \
                patch.object(tx, "render_sales_statements_combined_html", side_effect=fake_combined), \
                patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 fake"):
            r = self.client.get(
                f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}"
                "&keys=2026.06.28%7CH1%7C1%7C,2026.06.28%7CH1%7C2%7C&layout=legacy_triplicate&borders=on"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.headers["content-type"], "application/pdf")
        self.assertEqual(captured["n"], 2)
        self.assertEqual(captured["layout"], "legacy_triplicate")

    def test_batch_pdf_empty_keys_422(self) -> None:
        r = self.client.get(f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}&keys=")
        self.assertEqual(r.status_code, 422, r.text)

    def test_delete_endpoint_200(self) -> None:
        async def fake_del(**kwargs):  # noqa: ARG001
            return {"order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": "1", "gjisa": ""},
                    "deleted": 2, "status": "deleted"}

        with patch.object(tx, "delete_sales_statement", side_effect=fake_del):
            r = self.client.delete(
                f"/api/v1/transactions/sales-statement/2026.06.28%7CH1%7C1%7C?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["deleted"], 2)

    def test_delete_endpoint_locked_422(self) -> None:
        async def fake_del(**kwargs):  # noqa: ARG001
            raise ValueError("STATEMENT_LOCKED")

        with patch.object(tx, "delete_sales_statement", side_effect=fake_del):
            r = self.client.delete(
                f"/api/v1/transactions/sales-statement/2026.06.28%7CH1%7C1%7C?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 422, r.text)
        self.assertEqual(r.json()["detail"]["code"], "INQ_TX_LOCKED")

    def test_delete_endpoint_404_when_missing(self) -> None:
        with patch.object(tx, "delete_sales_statement", AsyncMock(return_value=None)):
            r = self.client.delete(
                f"/api/v1/transactions/sales-statement/2026.06.28%7CH1%7C9%7C?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 404, r.text)


if __name__ == "__main__":
    main()
