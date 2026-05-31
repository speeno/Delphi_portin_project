"""C3~C5 출고검증 (거래관리 / Subu59_1/2/3) — phase1 회귀.

검증 전략
--------
- 백엔드: GET /verification 가 list_verification 을 mode 분기로 호출,
  PATCH /verification 가 confirm/cancel 서비스를 호출하고 잘못된 action 은 422.
- 프론트: verification 페이지의 핵심 data-legacy-id 부착(Sobo59_2.md 기준).

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
from app.services import verification_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "kyomun", "server_id": "remote_1", "hcode": "5019"}


# 모듈 단위 override 설정/복원 — 다른 테스트 모듈로 전역 오염 방지(테스트 격리).
_PREV_OVERRIDE = None


def setUpModule() -> None:
    global _PREV_OVERRIDE
    _PREV_OVERRIDE = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = _override_auth


def tearDownModule() -> None:
    if _PREV_OVERRIDE is None:
        app.dependency_overrides.pop(get_current_user, None)
    else:
        app.dependency_overrides[get_current_user] = _PREV_OVERRIDE


class VerificationBackendTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_book_mode_default(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return {"items": [], "page": {"limit": 10, "offset": 0, "total": 0, "has_more": False}}

        with patch.object(verification_service, "list_verification", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/verification?serverId=remote_1&v=2"
                "&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured[0].get("mode"), "book")

    def test_list_summary_mode_for_v1(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return {"items": [], "page": {"limit": 10, "offset": 0, "total": 0, "has_more": False}}

        with patch.object(verification_service, "list_verification", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/verification?serverId=remote_1&v=1"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured[0].get("mode"), "summary")

    def test_confirm_calls_service(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return {"action": "confirm", "affected": 1}

        body = {
            "serverId": "remote_1",
            "action": "confirm",
            "items": [{"hcode": "5019", "gdate": "2026.04.18", "gcode": "G001", "bcode": "B001", "gsqut": 10}],
        }
        with patch.object(verification_service, "confirm_verification", side_effect=fake):
            res = self.client.patch("/api/v1/transactions/verification", json=body)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["affected"], 1)
        self.assertEqual(captured[0]["items"][0]["bcode"], "B001")

    def test_cancel_calls_service(self) -> None:
        async def fake(**kwargs):
            return {"action": "cancel", "affected": 2}

        body = {
            "serverId": "remote_1",
            "action": "cancel",
            "items": [
                {"hcode": "5019", "gdate": "2026.04.18", "gcode": "G001", "bcode": "B001"},
                {"hcode": "5019", "gdate": "2026.04.18", "gcode": "G002", "bcode": "B002"},
            ],
        }
        with patch.object(verification_service, "cancel_verification", side_effect=fake):
            res = self.client.patch("/api/v1/transactions/verification", json=body)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "cancel")

    def test_invalid_action_returns_422(self) -> None:
        body = {"serverId": "remote_1", "action": "delete", "items": []}
        res = self.client.patch("/api/v1/transactions/verification", json=body)
        self.assertEqual(res.status_code, 422, res.text)


class VerificationWidgetTraceability(TestCase):
    def test_core_legacy_ids_present(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "verification" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        for lid in (
            "Sobo59_verification.Root",
            "Sobo59_2.Edit101",
            "Sobo59_2.Edit102",
            "Sobo59_2.RadioButton1",
            "Sobo59_2.RadioButton2",
            "Sobo59_2.Button101",
            "Sobo59_2.Button102",
            "Sobo59_2.Button103",
            "Sobo59_2.DBGrid101",
        ):
            self.assertIn(lid, src, lid)

    def test_uses_verification_api(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "verification" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        self.assertIn("transactionsApi.verificationList", src)
        self.assertIn("transactionsApi.verificationWrite", src)


if __name__ == "__main__":
    main()
