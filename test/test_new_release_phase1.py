"""신간발행(Menu209) — 입고현황과 같은 3뷰 공용 축 회귀 (2026-08-25 재작성).

사용자 요청: "신간발행 화면을 입고현황(목록, 상세 …) 화면과 동일한 폼으로 수정해줘".

검증 전략
--------
- 백엔드: ``GET /api/v1/transactions/new-release?view=list|detail|summary`` 가 입고현황과
  **같은 facade**(`_status_axis_facade`)를 타되 거래구분 절만 「입고 + Pubun='신간'」인지
  monkeypatch 로 검증한다. 고정 조건(Scode='Y'+Gcode<>'')·표시명 원천(G2_Ggwo)·집계 주
  거래구분('입고')은 입고현황과 동일해야 한다.
- 프론트: 페이지가 공용 컴포넌트의 얇은 축 래퍼인지 / 입고축(kind=inbound)이 상세 라인·편집
  팝업을 **입고 API·입고 팝업**으로 타고 출고 전용 조작을 숨기는지 정적 검사.

종전 정본(기타명세서 `list_other_statements(pubun='신간')` facade + Sobo29 위젯 ID)은
폐기됐다. 축 결정 근거는 `transactions_service._GUBUN_IN_NEW_RELEASE` 주석.

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

ROUTE = "/api/v1/transactions/new-release"
COMMON_QUERY = "?serverId=remote_1&dateFrom=2026-08-01&dateTo=2026-08-25&limit=10&offset=0"


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


class NewReleaseAxisTests(TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def _get(self, view: str, captured: list[dict]):
        async def fake_slips(**kwargs):
            captured.append(kwargs)
            return [], 0

        async def fake_lines(**kwargs):
            captured.append(kwargs)
            return [], 0, {"qty": 0, "amount": 0}

        async def fake_rollup(**kwargs):
            captured.append(kwargs)
            return []

        with patch.object(transactions_service, "list_outbound_status_slips", side_effect=fake_slips), \
             patch.object(transactions_service, "list_outbound_status_lines", side_effect=fake_lines), \
             patch.object(transactions_service, "outbound_status_customer_rollup", side_effect=fake_rollup):
            res = self.client.get(f"{ROUTE}{COMMON_QUERY}&view={view}")
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(captured)
        return res

    def test_three_views_share_status_facade(self) -> None:
        for view, n_calls in (("summary", 1), ("detail", 1), ("list", 2)):
            with self.subTest(view=view):
                captured: list[dict] = []
                self._get(view, captured)
                self.assertEqual(len(captured), n_calls)

    def test_axis_is_inbound_new_release_only(self) -> None:
        """거래구분 절 = 입고 + Pubun='신간' — 라인·전표·집계 전부 동일 축."""
        for view in ("detail", "list"):
            with self.subTest(view=view):
                captured: list[dict] = []
                self._get(view, captured)
                for call in captured:
                    self.assertEqual(call["gubun_clause"], "Gubun = '입고' AND Pubun = '신간'")

    def test_fixed_scope_same_as_inbound_status(self) -> None:
        """고정 조건·표시명 원천·집계 주 거래구분은 입고현황과 같다."""
        captured: list[dict] = []
        self._get("list", captured)
        for call in captured:
            self.assertEqual(call["scode_clause"], "Scode = 'Y' AND Gcode <> ''")
            self.assertEqual(call["name_source"], "vendor")
        rollup = [c for c in captured if "primary_gubun" in c]
        self.assertEqual(len(rollup), 1)
        self.assertEqual(rollup[0]["primary_gubun"], "입고")

    def test_where_sql_has_no_yesno_filter(self) -> None:
        where_sql, _ = transactions_service._build_outbound_status_where(
            date_from="2026-08-01", date_to="2026-08-25",
            gubun_clause=transactions_service._GUBUN_IN_NEW_RELEASE,
            scode_clause=transactions_service._INBOUND_STATUS_FIXED,
            hcode="5019",
        )
        self.assertIn("Pubun = '신간'", where_sql)
        self.assertIn("Gubun = '입고'", where_sql)
        self.assertIn("Scode = 'Y'", where_sql)
        self.assertNotIn("Yesno", where_sql)

    def test_invalid_view_returns_422(self) -> None:
        res = self.client.get(f"{ROUTE}{COMMON_QUERY}&view=bogus")
        self.assertEqual(res.status_code, 422, res.text)


class NewReleaseScreenTests(TestCase):
    PAGE = FRONT / "app" / "(app)" / "transactions" / "new-release" / "page.tsx"
    SCREEN = FRONT / "components" / "transactions" / "transaction-status-screen.tsx"

    def test_page_is_thin_axis_wrapper(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        self.assertIn("TransactionStatusScreen", src)
        self.assertIn("NEW_RELEASE_AXIS", src)
        self.assertNotIn("DataGrid", src)
        self.assertNotIn("transactionsApi.newReleases", src)

    def _axis_block(self, name: str) -> str:
        src = self.SCREEN.read_text(encoding="utf-8")
        start = src.index(f"export const {name}")
        end = src.index("};", start)
        return src[start:end]

    def test_new_release_axis_is_inbound_kind(self) -> None:
        axis = self._axis_block("NEW_RELEASE_AXIS")
        self.assertIn('kind: "inbound"', axis)
        self.assertIn('partyLookupKind: "inboundVendor"', axis)
        self.assertIn('partyLabel: "입고처"', axis)
        self.assertIn('route: "/transactions/new-release"', axis)
        self.assertIn("transactionsApi.newRelease", axis)

    def test_inbound_status_axis_is_inbound_kind_too(self) -> None:
        """입고현황도 같은 도메인 — 종전엔 kind 가 없어 출고 상세/팝업을 타고 있었다."""
        self.assertIn('kind: "inbound"', self._axis_block("INBOUND_STATUS_AXIS"))

    def test_inbound_kind_uses_inbound_detail_and_dialog(self) -> None:
        """입고축 상세 라인 = inboundApi.detail, 편집 팝업 = ReceiptDetailDialog.

        출고 팝업(OrderDetailDialog)은 PUT /outbound/orders 로 저장한다 — 입고 전표에 쓰면
        잘못된 쓰기다. 상세 라인도 출고 API 는 입고 키에 대해 라인을 보장하지 않는다.
        """
        src = self.SCREEN.read_text(encoding="utf-8")
        self.assertIn("inboundApi.detail(key, sid)", src)
        self.assertIn("<ReceiptDetailDialog", src)
        self.assertIn("<OrderDetailDialog", src)
        self.assertIn("{isOutbound ? (", src)
        # 입고 라인(bname)을 출고 라인 모양(product_name)으로 맞춰 같은 표에 그린다.
        self.assertIn("product_name: ln.bname", src)

    def test_outbound_only_actions_gated(self) -> None:
        """바로출고·바로재출고·거래명세서 출력은 출고축에서만 렌더."""
        src = self.SCREEN.read_text(encoding="utf-8")
        body = src.split("export function TransactionStatusScreen")[1]
        self.assertIn('const isOutbound = (axis.kind ?? "outbound") === "outbound"', body)
        # 배치 툴바(출력/바로출고/재출고) 래핑
        self.assertIn('{isOutbound && (\n                <div className="ml-auto flex items-center gap-2">', body)
        # 단건 바로출고
        self.assertIn("{isOutbound &&\n                    selectedSlip &&", body)
        # 단건 출력
        idx = body.index('data-legacy-id="Sobo24.PrintSelected"')
        self.assertIn("{isOutbound && (", body[idx - 400:idx])


if __name__ == "__main__":
    main()
