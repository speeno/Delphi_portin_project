"""C6 제작명세서(Subu26)·C7 제작현황(Subu27)·C8 원천징수(Subu28) — phase1 회귀.

검증 전략
--------
- 백엔드: 각 엔드포인트가 해당 서비스를 호출하고 hcode 필수·필터 전달·응답 형태가
  올바른지 monkeypatch 로 검증한다(라이브 DB 불필요).
- 프론트: 각 페이지의 핵심 ``data-legacy-id`` 부착(회귀 가드, layout_mappings 기준).

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
from app.services import production_service, withholding_service  # noqa: E402


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

Q = "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"


def _prod_payload() -> dict:
    return {
        "items": [{
            "gdate": "2026.04.18", "gubun": "제작", "gcode": "G001", "gname": "인쇄소",
            "bcode": "B001", "bname": "도서A", "jubun": "", "gsqut": 100, "gdang": 1000,
            "gssum": 100000, "gbigo": "",
        }],
        "totals": {"qty": 100, "amount": 100000},
        "page": {"limit": 10, "offset": 0, "total": 1, "has_more": False},
    }


def _wh_payload() -> dict:
    return {
        "items": [{
            "gdate": "2026.04.18", "gcode": "00007", "gname": "홍길동", "bcode": "",
            "gssum": 1000000, "grat1": 3, "gisum": 30000, "gosum": 3000, "gbsum": 967000,
        }],
        "totals": {"gssum": 1000000, "gisum": 30000, "gosum": 3000, "gbsum": 967000},
        "page": {"limit": 10, "offset": 0, "total": 1, "has_more": False},
    }


class ProductionWithholdingBackendTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_production_statement_passes_ycode_and_filters(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return _prod_payload()

        with patch.object(production_service, "list_production_statement", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/production/statement" + Q + "&gubun=제작&bcode=B001"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["totals"]["amount"], 100000)
        kw = captured[0]
        self.assertEqual(kw.get("ycode"), "5019")
        self.assertEqual(kw.get("gubun"), "제작")
        self.assertEqual(kw.get("bcode"), "B001")

    def test_production_status_passes_bcode_range(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return _prod_payload()

        with patch.object(production_service, "list_production_status", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/production/status" + Q + "&bcodeFrom=B001&bcodeTo=B999"
            )
        self.assertEqual(res.status_code, 200, res.text)
        kw = captured[0]
        self.assertEqual(kw.get("ycode"), "5019")
        self.assertEqual(kw.get("bcode_from"), "B001")
        self.assertEqual(kw.get("bcode_to"), "B999")

    def test_withholding_passes_hcode_and_gcode_range(self) -> None:
        captured: list[dict] = []

        async def fake(**kwargs):
            captured.append(kwargs)
            return _wh_payload()

        with patch.object(withholding_service, "list_withholding", side_effect=fake):
            res = self.client.get(
                "/api/v1/transactions/withholding" + Q + "&gcodeFrom=00001&gcodeTo=00099"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["totals"]["gbsum"], 967000)
        self.assertEqual(body["items"][0]["gname"], "홍길동")
        kw = captured[0]
        self.assertEqual(kw.get("hcode"), "5019")
        self.assertEqual(kw.get("gcode_from"), "00001")
        self.assertEqual(kw.get("gcode_to"), "00099")


class ProductionWithholdingWidgetTraceability(TestCase):
    def _src(self, *parts: str) -> str:
        return (FRONT / "app" / "(app)" / "transactions" / Path(*parts) / "page.tsx").read_text(encoding="utf-8")

    def test_c6_statement_legacy_ids(self) -> None:
        src = self._src("production", "statement")
        for lid in ("Sobo26_production_stmt.Root", "Sobo26.Edit101", "Sobo26.Edit103",
                    "Sobo26.Edit104", "Sobo26.Button101", "Sobo26.DBGrid101"):
            self.assertIn(lid, src, lid)
        self.assertIn("transactionsApi.productionStatement", src)

    def test_c7_status_legacy_ids(self) -> None:
        src = self._src("production", "status")
        for lid in ("Sobo27_production_status.Root", "Sobo27.Edit101", "Sobo27.Edit106",
                    "Sobo27.Edit107", "Sobo27.Button101", "Sobo27.DBGrid101"):
            self.assertIn(lid, src, lid)
        self.assertIn("transactionsApi.productionStatus", src)

    def test_c8_withholding_legacy_ids(self) -> None:
        src = self._src("withholding")
        for lid in ("Sobo28_withholding.Root", "Sobo28.Edit101", "Sobo28.Edit103",
                    "Sobo28.Edit105", "Sobo28.Button101", "Sobo28.DBGrid101"):
            self.assertIn(lid, src, lid)
        self.assertIn("transactionsApi.withholding", src)


if __name__ == "__main__":
    main()
