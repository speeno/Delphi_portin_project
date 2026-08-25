"""C2 입고현황(거래관리 Menu205 / Sobo25_2) — 공용 3뷰 축 회귀.

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/inbound-status?view=list|detail|summary`` 가
  **출고현황과 같은 facade**(`_status_axis_facade`)를 입고처 축으로 타는지 monkeypatch 로
  검증한다. 축 계약 3가지를 못 박는다.
    1. 고정 조건 = ``Scode='Y'`` + ``Gcode<>''`` (레거시 Sobo25_2.Button101Click L396-420).
    2. 거래구분은 ``IN ('입고','반품')`` — 「입고처 반품」을 하드필터로 지우지 않는다.
       (반품현황은 거래처축 ``Scode='X'`` 라 그 행을 잡지 않아, 지우면 조회 불가.)
    3. 표시명 원천 = 입고처 **G2_Ggwo**(``name_source='vendor'``), 하단 집계 주 거래구분
       = '입고'. G1_Ggeo 를 쓰면 같은 Gcode 가 거래처명으로 뒤바뀐다(2026-08-22 리포트).
- 프론트: 페이지가 공용 컴포넌트의 입고 축 래퍼인지(레이아웃 갈림 방지).

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

ROUTE = "/api/v1/transactions/inbound-status"
COMMON_QUERY = "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


def _slip_row() -> dict:
    return {
        "order_key": {"gdate": "2026.04.18", "hcode": "5019", "jubun": "1",
                      "gjisa": "", "gcode": "00062"},
        "gdate": "2026.04.18", "jubun": "1", "idnum": 3, "gcode": "00062",
        "customer_name": "중원아트(랩핑)", "item_count": 2, "qty": 30,
        "amount": 300_000, "gbigo": "", "status": "received",
    }


def _line_row() -> dict:
    return {
        "order_key": {"gdate": "2026.04.18", "hcode": "5019", "jubun": "1", "gcode": "00062"},
        "gdate": "2026.04.18", "idnum": 3, "pubun": "", "gcode": "00062",
        "customer_name": "중원아트(랩핑)", "bcode": "B1", "bname": "도서A", "gisbn": "",
        "gsqut": 30, "gdang": 10_000, "grat1": 0, "gssum": 300_000,
        "gbigo": "", "status": "received",
    }


def _rollup_row() -> dict:
    return {
        "gcode": "00062", "customer_name": "중원아트(랩핑)",
        "out_qty": 30, "out_amount": 300_000, "gift_qty": 0,
        "return_qty": 0, "return_amount": 0, "sales_qty": 30, "sales_amount": 300_000,
    }


class InboundStatusAxisTests(TestCase):
    """입고현황이 출고현황과 같은 3뷰 facade 를 입고처 축으로 탄다."""

    def setUp(self) -> None:
        # 다른 테스트 파일이 공유 app 의 dependency_overrides 를 pop/clear 해도
        # (전체 스위트 실행 순서 의존) 인증 우회가 유지되도록 매 테스트마다 재설치.
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def _get(self, view: str, captured: list[dict], *, extra: str = ""):
        async def fake_slips(**kwargs):
            captured.append(kwargs)
            return [_slip_row()], 1

        async def fake_lines(**kwargs):
            captured.append(kwargs)
            return [_line_row()], 1, {"qty": 30, "amount": 300_000}

        async def fake_rollup(**kwargs):
            captured.append(kwargs)
            return [_rollup_row()]

        with patch.object(transactions_service, "list_outbound_status_slips", side_effect=fake_slips), \
             patch.object(transactions_service, "list_outbound_status_lines", side_effect=fake_lines), \
             patch.object(transactions_service, "outbound_status_customer_rollup", side_effect=fake_rollup):
            return self.client.get(f"{ROUTE}{COMMON_QUERY}&view={view}{extra}")

    def test_summary_and_detail_use_slip_service(self) -> None:
        for view in ("summary", "detail"):
            with self.subTest(view=view):
                captured: list[dict] = []
                res = self._get(view, captured)
                self.assertEqual(res.status_code, 200, res.text)
                self.assertEqual(len(res.json()["items"]), 1)
                self.assertEqual(len(captured), 1)

    def test_list_view_returns_lines_rollup_totals(self) -> None:
        captured: list[dict] = []
        res = self._get("list", captured)
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["lines"]), 1)
        self.assertEqual(len(body["rollup"]), 1)
        self.assertEqual(body["totals"], {"qty": 30, "amount": 300_000})
        # 라인 + 집계 두 서비스 호출.
        self.assertEqual(len(captured), 2)

    def test_axis_is_vendor_scode_with_nonempty_gcode(self) -> None:
        """고정 조건 = Scode='Y' + Gcode<>'' (레거시 Sobo25_2 L396-420)."""
        for view in ("detail", "list"):
            with self.subTest(view=view):
                captured: list[dict] = []
                self._get(view, captured)
                for call in captured:
                    self.assertEqual(call["scode_clause"], "Scode = 'Y' AND Gcode <> ''")

    def test_axis_is_inbound_gubun_only(self) -> None:
        """거래구분은 **입고만** — 라인·전표·집계 전부 동일 축.

        사용자 결정 2026-08-25 "입고 현황에 입고반품 모두 포함하지 말고 입고만
        대상으로". 출고/반품/폐기 현황이 각각 한 구분을 맡는 모던 분할과 같다.
        (레거시 Sobo25_2 는 거래구분이 선택 콤보라 무입력 시 「입고처 반품」도
        함께 나왔다 — 의도된 차이, DEC-194.)
        """
        for view in ("detail", "list"):
            with self.subTest(view=view):
                captured: list[dict] = []
                self._get(view, captured)
                for call in captured:
                    self.assertEqual(call["gubun_clause"], "Gubun = '입고'")

    def test_names_come_from_vendor_master(self) -> None:
        """표시명 = 입고처 G2_Ggwo. G1_Ggeo 를 쓰면 거래처명이 입고처명 자리에 뜬다."""
        for view in ("summary", "detail", "list"):
            with self.subTest(view=view):
                captured: list[dict] = []
                self._get(view, captured)
                for call in captured:
                    self.assertEqual(call["name_source"], "vendor")

    def test_rollup_primary_gubun_is_inbound(self) -> None:
        """하단 집계 out_* 버킷이 '입고' — 기본 '출고' 면 입고수량이 통째로 0."""
        captured: list[dict] = []
        self._get("list", captured)
        rollup_call = [c for c in captured if "primary_gubun" in c]
        self.assertEqual(len(rollup_call), 1)
        self.assertEqual(rollup_call[0]["primary_gubun"], "입고")

    def test_store_kind_reaches_service(self) -> None:
        """본사/창고 토글(Ocode) — 레거시 Edit107 동등, 종전 구현에는 없던 필터."""
        captured: list[dict] = []
        self._get("detail", captured, extra="&storeKind=B")
        self.assertEqual(captured[0]["store_kind"], "B")

    def test_invalid_view_returns_422(self) -> None:
        res = self.client.get(f"{ROUTE}{COMMON_QUERY}&view=bogus")
        self.assertEqual(res.status_code, 422, res.text)

    def test_invalid_store_kind_returns_422(self) -> None:
        res = self.client.get(f"{ROUTE}{COMMON_QUERY}&view=list&storeKind=Z")
        self.assertEqual(res.status_code, 422, res.text)


class InboundStatusScreenTests(TestCase):
    """화면이 공용 컴포넌트의 한 축인지 — 레이아웃이 갈릴 여지를 없앤다."""

    PAGE = FRONT / "app" / "(app)" / "transactions" / "inbound-status" / "page.tsx"
    SCREEN = FRONT / "components" / "transactions" / "transaction-status-screen.tsx"

    def test_page_is_thin_axis_wrapper(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn("TransactionStatusScreen", src)
        self.assertIn("INBOUND_STATUS_AXIS", src)
        # 자체 그리드/필터를 다시 만들지 않는다(600여 줄 별도 구현으로 되돌아가는 것 차단).
        self.assertNotIn("DataGrid", src)
        self.assertNotIn("MasterLookupField", src)

    def test_axis_declares_vendor_party(self) -> None:
        src = self.SCREEN.read_text(encoding="utf-8")
        head = src.split("export const RETURNS_STATUS_AXIS")[0]
        axis = head.split("export const INBOUND_STATUS_AXIS")[1]
        # 입고축은 Gcode 가 입고처 — 룩업 종류·라벨이 거래처축과 달라야 한다.
        self.assertIn('partyLabel: "입고처"', axis)
        self.assertIn('partyLookupKind: "inboundVendor"', axis)
        self.assertIn('rollupPrimaryLabel: "입고"', axis)

    def test_shared_screen_has_no_hardcoded_party_labels(self) -> None:
        """표/집계 헤더가 「거래처」 리터럴이면 입고현황에서 잘못된 라벨이 뜬다."""
        src = self.SCREEN.read_text(encoding="utf-8")
        body = src.split("export function TransactionStatusScreen")[1]
        for literal in ('label: "거래처명"', 'label: "거래처"', ">거래처명<", "출고수량"):
            self.assertNotIn(literal, body, literal)

    def test_session_snapshot_key_is_per_axis(self) -> None:
        """축별 스냅샷 분리 — 하나로 두면 4개 현황이 서로의 기간·거래처 필터를 덮어쓴다."""
        src = self.SCREEN.read_text(encoding="utf-8")
        self.assertIn("`transactions.status${axis.route", src)


if __name__ == "__main__":
    main()
