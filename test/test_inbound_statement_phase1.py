"""C1 입고명세서(거래관리 Menu202 / Sobo22 publisher variant) — phase1 회귀.

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/inbound-statement`` 가 입고접수와 동일
  ``inbound_service.list_receipts`` 를 호출하는 얇은 facade 이고, 응답 형태가
  ``/api/v1/inbound/receipts`` 와 1:1 동일한지(신규 SQL 0) monkeypatch 로 검증한다.
- 프론트: 매핑노트 Sobo22.md §2·§3 의 핵심 ``data-legacy-id`` 가 페이지 DOM 에
  부착됐는지(dfm-layout-input.mdc 회귀 가드) 정적 검사한다.

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

COMMON_QUERY = (
    "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"
)


def _receipt_item() -> dict:
    return {
        "receipt_key": {"gdate": "2026.04.18", "hcode": "A0001", "gcode": "V001", "jubun": "120000000001"},
        "publisher_name": "교문사",
        "vendor_name": "한국출판협동",
        "lines": 3,
        "qty": 30,
        "amount": 300_000,
        "status": "active",
    }


class InboundStatementFacadeTests(TestCase):
    def setUp(self) -> None:
        # 다른 테스트 파일이 공유 app 의 dependency_overrides 를 pop/clear 해도
        # (전체 스위트 실행 순서 의존) 인증 우회가 유지되도록 매 테스트마다 재설치.
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_facade_equivalent_to_receipts(self) -> None:
        """입고명세서 facade 와 입고접수 목록이 동일 서비스를 호출하고
        동일 응답 형태를 반환하는지 검증 (신규 SQL 0)."""
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            items = [_receipt_item()]
            return items, len(items)

        with patch.object(inbound_service, "list_receipts", side_effect=fake_list):
            res_facade = self.client.get(
                "/api/v1/transactions/inbound-statement" + COMMON_QUERY
            )
            res_canonical = self.client.get(
                "/api/v1/inbound/receipts" + COMMON_QUERY
            )

        self.assertEqual(res_facade.status_code, 200, res_facade.text)
        self.assertEqual(res_canonical.status_code, 200, res_canonical.text)
        self.assertEqual(res_facade.json()["items"], res_canonical.json()["items"])
        self.assertEqual(res_facade.json()["total"], res_canonical.json()["total"])
        # 두 엔드포인트 모두 동일 서비스(list_receipts) 호출 — facade 가 새 SQL 을 만들지 않음.
        self.assertEqual(len(captured), 2)
        self.assertEqual(captured[0].get("date_from"), "2026-04-01")
        self.assertEqual(captured[0].get("date_to"), "2026-04-30")

    def test_facade_passes_filters(self) -> None:
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            return [], 0

        with patch.object(inbound_service, "list_receipts", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/transactions/inbound-statement"
                + COMMON_QUERY
                + "&hcode=A0001&gcode=V001&includeCancelled=true"
            )
        self.assertEqual(res.status_code, 200, res.text)
        kw = captured[0]
        self.assertEqual(kw.get("gcode"), "V001")
        self.assertTrue(kw.get("include_cancelled"))


class InboundStatementWidgetTraceability(TestCase):
    """Sobo22.md 매핑노트의 핵심 legacy id 가 입고명세서 페이지 DOM 에 부착됐는지."""

    def test_core_legacy_ids_present(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "inbound-statement" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        for legacy_id in (
            "Sobo22.Panel001",
            "Sobo22.Edit103",   # 출판사코드
            "Sobo22.Edit104",   # 입고처코드
            "Sobo22.Edit101",   # 거래일자(시작)
            "Sobo22.Button101", # 조회
            "Sobo22.DBGrid101",
            # DBGrid101 9개 컬럼 FieldName (Sobo22.md §3)
            "Sobo22.DBGrid101.PUBUN",
            "Sobo22.DBGrid101.BCODE",
            "Sobo22.DBGrid101.BNAME",
            "Sobo22.DBGrid101.GSQUT",
            "Sobo22.DBGrid101.GDANG",
            "Sobo22.DBGrid101.GRAT1",
            "Sobo22.DBGrid101.GSSUM",
            "Sobo22.DBGrid101.GBIGO",
            "Sobo22.DBGrid101.YESNO",
        ):
            self.assertIn(legacy_id, src, legacy_id)

    def test_reuses_inbound_statement_facade(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "inbound-statement" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        # 신규 SQL 없이 facade + 기존 detail 재사용 (DRY).
        self.assertIn("inboundApi.statement", src)
        self.assertIn("inboundApi.detail", src)


if __name__ == "__main__":
    main()
