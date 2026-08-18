"""출력 결과 추적 회귀 — X-Printed-Keys 헤더 / Web_Print_Log / received-today days 창.

요구(2026-07-03): ① 출력이 실제 완료된 건만 접수→완료 전이(서버가 PDF 포함 전표를
헤더로 명시), ② 어떤 건이 출력되었는지 상세 이력 기록, ③ 일괄 출고요청(DEC-071)으로
접수된 과거 거래일자 전표도 자동출력이 포착(days 조회창). 여러 건 접수요청 후
일괄 출력도 단건과 동일하게 동작해야 한다(멀티키 헤더 검증).
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import print_log_db, transactions_service as tx  # noqa: E402

_SID = "remote_1"


def _auth() -> dict:
    return {"user_id": "u", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": []}


def _detail(jubun: str = "00001") -> dict:
    return {
        "order_key": {"gdate": "2026.06.28", "hcode": "H1", "jubun": jubun, "gjisa": ""},
        "customer": {"hcode": "H1", "gname": "테스트거래처", "gcode": "00044"},
        "lines": [{"gcode": "00044", "bcode": "B1", "gsqut": 3, "gssum": 21000}],
    }


def _decode_header(value: str) -> list[str]:
    return json.loads(base64.b64decode(value).decode("utf-8"))


class PrintedKeysHeaderTests(TestCase):
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

    def test_batch_pdf_header_lists_multi_keys_and_records_log(self) -> None:
        """여러 건 접수요청 후 일괄 출력 — 포함 전표 전부 헤더 명시 + 이력 기록."""
        from app.services import print_service

        log_mock = AsyncMock(return_value=3)

        async def fake_detail(**kwargs):  # noqa: ANN001
            return _detail(kwargs["jubun"])

        with patch.object(tx, "get_sales_statement_detail", side_effect=fake_detail), \
                patch.object(tx, "render_sales_statements_combined_html", return_value="<html/>"), \
                patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"), \
                patch.object(print_log_db, "record_printed", log_mock):
            r = self.client.get(
                f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}&source=auto"
                "&keys=2026.06.28%7CH1%7C00001%7C,2026.06.28%7CH1%7C00002%7C,2026.06.28%7CH1%7C00003%7C"
            )
        self.assertEqual(r.status_code, 200, r.text)
        keys = _decode_header(r.headers["X-Printed-Keys"])
        self.assertEqual(
            keys,
            ["2026.06.28|H1|00001|", "2026.06.28|H1|00002|", "2026.06.28|H1|00003|"],
        )
        log_mock.assert_awaited_once()
        self.assertEqual(log_mock.await_args.kwargs["kind"], "auto")  # source=auto
        entries = log_mock.await_args.kwargs["entries"]
        self.assertEqual([e["jubun"] for e in entries], ["00001", "00002", "00003"])
        self.assertEqual(entries[0]["customer_name"], "테스트거래처")
        self.assertEqual(entries[0]["amount"], 21000)

    def test_batch_pdf_header_excludes_missing_details(self) -> None:
        """자료 없는 키는 PDF 미포함 → 헤더에서도 제외(완료 전이 대상 아님)."""
        from app.services import print_service

        async def fake_detail(**kwargs):  # noqa: ANN001
            return _detail(kwargs["jubun"]) if kwargs["jubun"] != "00002" else None

        with patch.object(tx, "get_sales_statement_detail", side_effect=fake_detail), \
                patch.object(tx, "render_sales_statements_combined_html", return_value="<html/>"), \
                patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"), \
                patch.object(print_log_db, "record_printed", AsyncMock(return_value=2)):
            r = self.client.get(
                f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}"
                "&keys=2026.06.28%7CH1%7C00001%7C,2026.06.28%7CH1%7C00002%7C,2026.06.28%7CH1%7C00003%7C"
            )
        self.assertEqual(r.status_code, 200, r.text)
        keys = _decode_header(r.headers["X-Printed-Keys"])
        self.assertEqual([k.split("|")[2] for k in keys], ["00001", "00003"])

    def test_single_pdf_header_and_log_kind_single(self) -> None:
        from app.services import print_service

        log_mock = AsyncMock(return_value=1)
        with patch.object(tx, "get_sales_statement_detail", AsyncMock(return_value=_detail())), \
                patch.object(tx, "render_sales_statement_html", return_value="<html/>"), \
                patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"), \
                patch.object(print_log_db, "record_printed", log_mock):
            r = self.client.get(
                f"/api/v1/print/sales-statement/2026.06.28%7CH1%7C00001%7C.pdf?serverId={_SID}"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(_decode_header(r.headers["X-Printed-Keys"]), ["2026.06.28|H1|00001|"])
        self.assertEqual(log_mock.await_args.kwargs["kind"], "single")

    def test_print_log_endpoint_returns_items(self) -> None:
        rows = [{"seq": 2, "printed_at": "2026-07-03 22:00:00", "kind": "auto",
                 "user_id": "u", "gdate": "2026.07.03", "jubun": "00007", "gjisa": "",
                 "gcode": "00044", "customer_name": "북센", "line_count": 3, "amount": 48450}]
        with patch.object(print_log_db, "list_recent", AsyncMock(return_value=rows)):
            r = self.client.get(f"/api/v1/print/sales-statement/print-log?serverId={_SID}&limit=5")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["count"], 1)
        self.assertEqual(r.json()["items"][0]["jubun"], "00007")

    def test_received_today_days_window_widens_date_from(self) -> None:
        """일괄 출고요청된 과거 일자 전표 포착 — days=7 이면 date_from = 기준일-6."""
        captured: dict = {}

        async def fake_list(**kwargs):  # noqa: ANN001
            captured.update(kwargs)
            return [], 0

        with patch.object(tx, "list_sales_statements", side_effect=fake_list):
            r = self.client.get(
                f"/api/v1/transactions/sales-statement/received-today?serverId={_SID}"
                "&today=2026-07-03&days=7"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(captured["date_from"], "2026-06-27")
        self.assertEqual(captured["date_to"], "2026-07-03")

    def test_received_today_default_stays_single_day(self) -> None:
        captured: dict = {}

        async def fake_list(**kwargs):  # noqa: ANN001
            captured.update(kwargs)
            return [], 0

        with patch.object(tx, "list_sales_statements", side_effect=fake_list):
            r = self.client.get(
                f"/api/v1/transactions/sales-statement/received-today?serverId={_SID}&today=2026-07-03"
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(captured["date_from"], "2026-07-03")  # 기본 당일 유지


class PrintLogDbSqlTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        print_log_db.clear_ensured_for_tests()

    async def test_record_inserts_with_hcode(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            captured.append((sql, params))
            return []

        with patch.object(print_log_db, "execute_query", side_effect=fake_eq):
            n = await print_log_db.record_printed(
                server_id=_SID, user_id="u", kind="batch",
                entries=[{"hcode": "H1", "gdate": "2026.07.03", "jubun": "00007",
                          "gjisa": "", "gcode": "00044", "customer_name": "북센",
                          "line_count": 3, "amount": 48450}],
            )
        self.assertEqual(n, 1)
        ins = next(c for c in captured if c[0].startswith("INSERT INTO Web_Print_Log"))
        self.assertEqual(ins[1][0], "H1")  # Hcode 격리

    async def test_record_failure_is_graceful(self) -> None:
        async def boom(*a, **k):  # noqa: ANN001, ARG001
            raise RuntimeError("db down")

        with patch.object(print_log_db, "execute_query", side_effect=boom):
            n = await print_log_db.record_printed(
                server_id=_SID, user_id="u", kind="auto",
                entries=[{"hcode": "H1"}],
            )
        self.assertEqual(n, 0)  # 인쇄 비차단

    async def test_list_recent_filters_hcode(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            captured.append((sql, params))
            return []

        with patch.object(print_log_db, "execute_query", side_effect=fake_eq):
            out = await print_log_db.list_recent(server_id=_SID, hcode="H1", limit=10)
        self.assertEqual(out, [])
        sel = next(c for c in captured if c[0].strip().startswith("SELECT"))
        self.assertIn("WHERE Hcode=%s", sel[0])
        self.assertEqual(sel[1], ("H1",))


class MonitorStaticGuards(TestCase):
    """자동출력 모니터 — 다중 접수 연동/출력된 건만 완료 정적 가드."""

    def setUp(self) -> None:
        self.src = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
                    / "transactions" / "sales-statement" / "auto-print" / "page.tsx"
                    ).read_text(encoding="utf-8")

    def test_polls_with_days_window(self) -> None:
        self.assertIn("days: 7", self.src)  # 과거 일자 일괄 접수 전표 포착

    def test_completes_only_printed_keys(self) -> None:
        # DEC-158 — 일괄 1요청(`printed ?? fresh`)이 N건×~20s 렌더로 통째 실패하던 원인 →
        # 1건씩 순차 인쇄로 분할, 건별 실제 인쇄 키만 완료(`printed ?? [key]`) + 실패 키는
        # printedRef 롤백(다음 주기 재시도).
        self.assertIn("printed ?? [key]", self.src)
        self.assertIn("printedRef.current.delete(k)", self.src)
        self.assertNotIn("printed ?? fresh", self.src)
        self.assertIn('source: "auto"', self.src)

    def test_history_panel_present(self) -> None:
        self.assertIn("getSalesStatementPrintLog", self.src)
        self.assertIn("Sobo21.AutoPrintMonitor.PrintLog", self.src)
