"""C9 신간발행(거래관리 Menu209 / Sobo29) — phase1 회귀.

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/new-release`` 가 기타명세서와 동일
  ``transactions_service.list_other_statements`` 를 전표구분 ``Jubun='신간'`` 으로
  고정 호출하는 facade 인지(신규 SQL 0) monkeypatch 로 검증한다.
- 프론트: Sobo29.md 핵심 ``data-legacy-id`` 가 신간발행 페이지에 부착됐고,
  전표구분이 신간 고정인지 정적 검사한다.

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
from app.services import transactions_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


class NewReleaseFacadeTests(TestCase):
    def setUp(self) -> None:
        # 다른 테스트 파일이 공유 app 의 dependency_overrides 를 pop/clear 해도
        # (전체 스위트 실행 순서 의존) 인증 우회가 유지되도록 매 테스트마다 재설치.
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_facade_pins_pubun_singan(self) -> None:
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {
                "items": [{"gdate": "2026.04.01", "hcode": "H001", "bcode": "B001", "jubun": "신간"}],
                "page": {"limit": 25, "offset": 0, "total": 1, "has_more": False},
            }

        with patch.object(transactions_service, "list_other_statements", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/new-release?serverId=remote_1"
                "&dateFrom=2026-04-01&dateTo=2026-04-30&hcode=H001&limit=25"
            )
        self.assertEqual(res.status_code, 200, res.text)
        # 신간발행은 기타명세서 서비스를 재사용하되 전표구분을 신간으로 고정한다.
        # 전표구분 정본 컬럼은 Pubun (Subu29 Edit102). Jubun 은 전표번호라
        # 문자열 '신간' 이 들어가지 않는다 — 2026-08-24 라이브: Jubun 0건 / Pubun 81건.
        self.assertEqual(captured["pubun"], "신간")
        self.assertNotIn("jubun", captured)
        self.assertEqual(captured["hcode"], "H001")
        self.assertEqual(res.json()["page"]["total"], 1)

    def test_facade_ignores_client_pubun_override(self) -> None:
        # 쿼리로 다른 전표구분을 넘겨도 신간 고정 (신간 전용 IA).
        captured: dict = {}

        async def fake(**kwargs):
            captured.update(kwargs)
            return {"items": [], "page": {"limit": 100, "offset": 0, "total": 0, "has_more": False}}

        with patch.object(transactions_service, "list_other_statements", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/new-release?serverId=remote_1"
                "&dateFrom=2026-04-01&dateTo=2026-04-30&pubun=기타"
            )
        self.assertEqual(res.status_code, 200, res.text)
        # 전표구분 정본 컬럼은 Pubun (Subu29 Edit102). Jubun 은 전표번호라
        # 문자열 '신간' 이 들어가지 않는다 — 2026-08-24 라이브: Jubun 0건 / Pubun 81건.
        self.assertEqual(captured["pubun"], "신간")
        self.assertNotIn("jubun", captured)


class NewReleaseWidgetTraceability(TestCase):
    def test_core_legacy_ids_present(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "new-release" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        for legacy_id in (
            "Sobo29.Panel001",
            "Sobo29.Edit101",
            "Sobo29.Edit104",
            "Sobo29.Edit107",
            "Sobo29.Button101",
            "Sobo29.DBGrid101",
            "Sobo29.DBGrid101.GSQUT",
            "Sobo29.DBGrid101.GSSUM",
            "Sobo29.Button301",
        ):
            self.assertIn(legacy_id, src, legacy_id)

    def test_jubun_pinned_and_reuses_facade(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "new-release" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        self.assertIn('NEW_RELEASE_JUBUN = "신간"', src)
        self.assertIn("transactionsApi.newReleases", src)
        # 전표구분 입력은 읽기 전용(신간 고정) — 기타명세서와의 유일한 IA 차이.
        self.assertIn("readOnly", src)


if __name__ == "__main__":
    main()
