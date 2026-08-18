"""일괄 출고요청 라우터(PATCH /api/v1/outbound/orders/batch/request) 회귀.

레거시 동등: 신규 생성(신청)만 하고 출고요청을 안 한 대기('') 전표를
거래명세서(Sobo21)/출고현황(Sobo24) 화면에서 선택 일괄 접수('0') 전이.
가드: keys 순서 보존 / 항목 단위 부분 실패(not_found·error) / 빈 keys 422 /
단건 라우트(/orders/{key}/request)에 "batch" 가 삼켜지지 않는 등록 순서.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import outbound_service  # noqa: E402

_SID = "remote_1"


def _auth() -> dict:
    return {"user_id": "hong01", "server_id": _SID}


class BatchRequestRouterTests(TestCase):
    def setUp(self) -> None:
        self._prev = app.dependency_overrides.get(get_current_user)
        app.dependency_overrides[get_current_user] = _auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev is not None:
            app.dependency_overrides[get_current_user] = self._prev
        else:
            app.dependency_overrides.pop(get_current_user, None)

    def test_batch_mixed_results_preserve_key_order(self) -> None:
        async def fake_request(**kwargs):  # noqa: ANN001
            jubun = kwargs["jubun"]
            if jubun == "2":
                return None  # not_found
            if jubun == "3":
                raise RuntimeError("db down")  # error
            return {
                "order_key": {"gdate": kwargs["gdate"], "hcode": kwargs["hcode"],
                              "gcode": kwargs["gcode"], "jubun": jubun},
                "status": "received", "updated_at": "t",
            }

        with patch.object(outbound_service, "request_dispatch", side_effect=fake_request):
            r = self.client.patch(
                f"/api/v1/outbound/orders/batch/request?serverId={_SID}",
                json={"keys": [
                    "2026.07.03|H1|G01|1",
                    "2026.07.03|H1|G01|2",
                    "2026.07.03|H1|G01|3",
                ]},
            )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual([it["status"] for it in body["results"]],
                         ["received", "not_found", "error"])  # keys 순서 보존
        self.assertEqual(body["transitioned"], 1)
        self.assertEqual(body["not_found"], 1)
        self.assertEqual(body["errors"], 1)

    def test_batch_empty_list_422(self) -> None:
        r = self.client.patch(
            f"/api/v1/outbound/orders/batch/request?serverId={_SID}",
            json={"keys": []},
        )
        self.assertEqual(r.status_code, 422, r.text)

    def test_batch_blank_keys_422(self) -> None:
        r = self.client.patch(
            f"/api/v1/outbound/orders/batch/request?serverId={_SID}",
            json={"keys": ["  "]},
        )
        self.assertEqual(r.status_code, 422, r.text)
        self.assertEqual(r.json()["detail"]["code"], "OUT_KEYS_EMPTY")

    def test_batch_path_not_swallowed_by_single_route(self) -> None:
        """단건 라우트가 'batch' 를 order_key 로 파싱하면 422/404 — 200 이면 배치 매칭."""
        async def fake_request(**kwargs):  # noqa: ANN001, ARG001
            return {"order_key": {"gdate": "g", "hcode": "h", "gcode": "c", "jubun": "1"},
                    "status": "received", "updated_at": "t"}

        with patch.object(outbound_service, "request_dispatch", side_effect=fake_request):
            r = self.client.patch(
                f"/api/v1/outbound/orders/batch/request?serverId={_SID}",
                json={"keys": ["2026.07.03|H1|G01|1"]},
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("results", r.json())


class PagesStaticGuards(TestCase):
    """두 화면의 일괄 출고요청 UI 정적 가드."""

    def test_sales_statement_page_has_bulk_request(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
               / "transactions" / "sales-statement" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("Sobo21.BulkRequestDispatch", src)
        self.assertIn("requestDispatchBatch", src)
        self.assertIn('it.status === "pending"', src)  # 대기 전표만 대상

    def test_outbound_status_page_has_bulk_request(self) -> None:
        # DEC-114(2026-07-21): 종전 '대기 N건 출고요청'(`Sobo24.BulkRequestDispatch`)은
        # 배치 '바로출력 (N건)'(`Sobo24.BatchImmediateDispatch`)에 흡수 — 대기분은 여전히
        # requestDispatchBatch(→접수) 로 보내고 완료전 전체를 긴급 출력 큐에 적재한다.
        src = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
               / "transactions" / "outbound-status" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("Sobo24.BatchImmediateDispatch", src)
        self.assertIn("requestDispatchBatch", src)
        self.assertIn('s.status === "pending"', src)  # 대기분만 출고요청(접수) 전이
