"""C10 내역조회(저자) (거래관리 / Subu26_1 publisher MySQL) — phase1 회귀.

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/author-history`` 가 ``author_history_service``
  를 호출하고, hcode 필수·필터 전달·응답 형태가 올바른지 monkeypatch 로 검증한다.
- 프론트: Sobo_author_history.md §1 의 핵심 ``data-legacy-id`` 부착(회귀 가드).

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
from app.services import author_history_service  # noqa: E402


def _override_auth() -> dict:
    # T2_PUB scope — hcode 자동 주입 대상 (enforce_hcode_isolation).
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

COMMON_QUERY = "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"


def _payload() -> dict:
    return {
        "items": [
            {
                "gdate": "2026.04.18", "idnum": "00007", "gcode": "G001",
                "bcode": "B001", "bname": "도서A", "author": "홍길동",
                "pubun": "", "gubun": "출고", "jubun": "1",
                "gsqut": 10, "gssum": 100000, "gdang": 10000, "grat1": 70, "yesno": "1",
            }
        ],
        "totals": {"qty": 10, "amount": 100_000},
        "page": {"limit": 10, "offset": 0, "total": 1, "has_more": False},
    }


class AuthorHistoryServiceTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_lists_with_injected_hcode_and_filters(self) -> None:
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            return _payload()

        with patch.object(author_history_service, "list_author_history", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/transactions/author-history"
                + COMMON_QUERY
                + "&gubun=출고&gcode=G001&bcode=B001"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["totals"]["amount"], 100_000)
        self.assertEqual(body["items"][0]["author"], "홍길동")
        kw = captured[0]
        # T2_PUB scope 의 hcode(5019) 가 자동 주입돼야 한다.
        self.assertEqual(kw.get("hcode"), "5019")
        self.assertEqual(kw.get("gubun"), "출고")
        self.assertEqual(kw.get("gcode"), "G001")
        self.assertEqual(kw.get("bcode"), "B001")

    def test_service_failure_returns_500(self) -> None:
        async def boom(**kwargs):
            raise RuntimeError("db down")

        with patch.object(author_history_service, "list_author_history", side_effect=boom):
            res = self.client.get("/api/v1/transactions/author-history" + COMMON_QUERY)
        self.assertEqual(res.status_code, 500, res.text)


class AuthorHistoryWidgetTraceability(TestCase):
    def test_core_legacy_ids_present(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "author-history" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        for legacy_id in (
            "Sobo_author_history.Root",
            "Sobo26_1.Edit101",   # 시작일
            "Sobo26_1.Edit102",   # 종료일
            "Sobo26_1.Edit103",   # 전표구분
            "Sobo26_1.Edit105",   # 거래처
            "Sobo26_1.Edit108",   # 도서코드
            "Sobo26_1.Button101", # 조회
            "Sobo26_1.DBGrid101", # 내역 그리드
        ):
            self.assertIn(legacy_id, src, legacy_id)

    def test_uses_author_history_api(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "author-history" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        self.assertIn("transactionsApi.authorHistory", src)


if __name__ == "__main__":
    main()
