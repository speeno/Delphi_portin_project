"""C2 입고현황(거래관리 Menu205 / Sobo25 publisher) — phase1 회귀.

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/inbound-status?view=list|detail|summary`` 가
  입고접수와 동일 ``inbound_service.list_receipts`` / ``period_report`` 를 호출하는
  얇은 facade(신규 SQL 0)이고, view 분기·검증이 올바른지 monkeypatch 로 검증한다.
- 프론트: Sobo25_inbound_status.md §2 의 핵심 ``data-legacy-id`` 부착(회귀 가드).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import inbound_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth

COMMON_QUERY = "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"


def _receipt_item() -> dict:
    return {
        "receipt_key": {"gdate": "2026.04.18", "hcode": "A0001", "gcode": "V001", "jubun": "120000000001"},
        "publisher_name": "교문사",
        "vendor_name": "한국출판협동",
        "lines": 3,
        "qty": 30,
        "amount": 300_000,
        # 실제 list_receipts 어휘(_line_status_from_yesno_max → pending|received|done).
        # 2026-06-27 회귀: ReceiptListItem.status 가 active/cancelled 2-state Literal 이라
        # 'received' 입력에서 ValidationError(→500, 입고현황 목록/상세 조회 불가)였다.
        "status": "received",
    }


def _period_payload() -> dict:
    return {
        "by_publisher": [],
        "by_vendor": [
            {
                "gdate": "2026.04.18", "gcode": "V001", "gname": "한국출판협동",
                "idnum": "1", "pubun": "", "bcode": "B1", "bname": "도서A",
                "gsqut": 30, "gdang": 10000, "grat1": 0.7, "gssum": 300000,
            }
        ],
        "totals": {"qty": 30, "amount": 300_000},
        "page": {"limit": 10, "offset": 0, "total": 1, "has_more": False},
    }


class InboundStatusFacadeTests(TestCase):
    def setUp(self) -> None:
        # 다른 테스트 파일이 공유 app 의 dependency_overrides 를 pop/clear 해도
        # (전체 스위트 실행 순서 의존) 인증 우회가 유지되도록 매 테스트마다 재설치.
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_list_view_facade_equivalent_to_receipts(self) -> None:
        """view=list facade 와 입고접수 목록이 동일 서비스를 호출하고 동일 응답을 반환."""
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            items = [_receipt_item()]
            return items, len(items)

        with patch.object(inbound_service, "list_receipts", side_effect=fake_list):
            res_facade = self.client.get(
                "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=list"
            )
            res_canonical = self.client.get("/api/v1/inbound/receipts" + COMMON_QUERY)

        self.assertEqual(res_facade.status_code, 200, res_facade.text)
        self.assertEqual(res_canonical.status_code, 200, res_canonical.text)
        self.assertEqual(res_facade.json()["items"], res_canonical.json()["items"])
        self.assertEqual(len(captured), 2)

    def test_detail_view_uses_list_service(self) -> None:
        async def fake_list(**kwargs):
            return [_receipt_item()], 1

        with patch.object(inbound_service, "list_receipts", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=detail"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(res.json()["items"]), 1)

    def test_summary_view_uses_period_report(self) -> None:
        captured: list[dict] = []

        async def fake_period(**kwargs):
            captured.append(kwargs)
            return _period_payload()

        with patch.object(inbound_service, "period_report", side_effect=fake_period):
            res = self.client.get(
                "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=summary"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertIn("by_vendor", body)
        self.assertEqual(body["totals"]["qty"], 30)
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0].get("date_from"), "2026-04-01")

    def test_invalid_view_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=bogus"
        )
        self.assertEqual(res.status_code, 422, res.text)


class InboundStatusWidgetTraceability(TestCase):
    def test_core_legacy_ids_present(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "inbound-status" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        for legacy_id in (
            "Sobo25_status.Root",
            "Sobo25.Edit101",   # 시작일
            "Sobo25.Edit102",   # 종료일
            "Sobo25.Edit105",   # 입고처코드
            "Sobo25.Edit106",   # 출판사
            "Sobo25.Button101", # 조회
            "Sobo25.DBGrid101", # 상세 라인
            "Sobo25.DBGrid201", # 요약
            "Sobo25_status.tab.", # list/detail/summary 뷰 탭 (템플릿 리터럴)
        ):
            self.assertIn(legacy_id, src, legacy_id)

    def test_reuses_inbound_facade(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "inbound-status" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        self.assertIn("inboundApi.status", src)
        self.assertIn("inboundApi.statusSummary", src)
        self.assertIn("inboundApi.detail", src)


if __name__ == "__main__":
    main()
