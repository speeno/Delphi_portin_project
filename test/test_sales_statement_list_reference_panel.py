"""거래명세서 목록 — 참조·메모 패널·customer-preview 회귀."""

from __future__ import annotations

from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys_path_added = False


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SalesStatementListPanelsStaticTest(TestCase):
    def test_list_page_has_bottom_panels(self) -> None:
        src = _read(FRONT / "app" / "(app)" / "transactions" / "sales-statement" / "page.tsx")
        self.assertIn("SalesStatementReferencePanel", src)
        self.assertIn("SalesStatementMemoPanel", src)
        self.assertIn("loadCustomerPreview", src)
        self.assertIn("selectStatementRow", src)
        self.assertIn("Sobo21.Link.Detail", src)
        self.assertIn("refError", src)
        self.assertIn("memoPreview", src)

    def test_shared_panel_components_exist(self) -> None:
        ref = _read(FRONT / "components" / "transactions" / "sales-statement-reference-panel.tsx")
        self.assertIn("Sobo21.Label104", ref)
        self.assertIn("Sobo21.Edit203", ref)
        self.assertIn("memoPreview", ref)
        self.assertIn("RichMemoEditor", ref)
        self.assertIn("Sobo21.Panel203.S1Preview", ref)
        self.assertIn("Sobo21.Panel007.Error", ref)
        self.assertIn(
            "Sobo21.Button801",
            _read(FRONT / "components" / "transactions" / "sales-statement-memo-panel.tsx"),
        )

    def test_reference_panel_is_collapsible(self) -> None:
        """거래처 참조 = 접었다 펼 수 있는 패널 (사용자 요청 2026-09-22).

        - 제목 줄이 토글 버튼(aria-expanded/aria-controls)이고, 접힘 상태는 화면별
          localStorage 키(`bls.ref-panel.<storageKey>`)로 기억한다(기본 펼침).
        - 접어도 재고·거래처명 요약은 제목 줄에 남는다(참조 값을 완전히 잃지 않게).
        """
        ref = _read(FRONT / "components" / "transactions" / "sales-statement-reference-panel.tsx")
        self.assertIn("aria-expanded={open}", ref)
        self.assertIn("aria-controls={bodyId}", ref)
        self.assertIn("`bls.ref-panel.${storageKey}`", ref)
        self.assertIn("storageKey = \"reference\"", ref)
        # 접힘 시 본문 미렌더 + 요약 유지
        self.assertIn("{open ? (", ref)
        self.assertIn("{!open && custName ?", ref)
        head = ref[ref.index("거래처 참조") - 1200 : ref.index('id={bodyId}')]
        self.assertIn('data-legacy-id="Sobo21.Label104"', head, "재고는 제목 줄(접어도 보임)")
        # 화면마다 따로 기억 — 4개 사용처가 각자 키를 넘긴다.
        for rel, key in (
            ("app/(app)/inbound/receipts/new/page.tsx", "inbound.receipts.new"),
            ("app/(app)/outbound/orders/new/page.tsx", "outbound.orders.new"),
            ("app/(app)/transactions/sales-statement/page.tsx", "sales-statement.list"),
            ("app/(app)/transactions/sales-statement/[orderKey]/page.tsx", "sales-statement.detail"),
        ):
            with self.subTest(screen=rel):
                self.assertIn(f'storageKey="{key}"', _read(FRONT / rel))

    def test_reference_panel_layout_is_compact(self) -> None:
        """레이아웃 최적화 — 한 줄 입력은 촘촘한 다열 그리드, 메모는 전폭(2026-09-22).

        실측(CSS 하네스): 1512px 폭에서 8개 단일 입력이 3열 3줄로 들어가고 메모는 전폭.
        종전에는 sm:col-span-2 가 붙은 필드들이 한 줄씩 차지해 빈 칸이 크게 남았다.
        """
        ref = _read(FRONT / "components" / "transactions" / "sales-statement-reference-panel.tsx")
        self.assertIn("sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4", ref)
        self.assertNotIn('className="space-y-1 sm:col-span-2"', ref, "단일 입력은 열 병합 없이 채운다")
        # 메모/미리보기는 전폭 + 라벨 결합형 예외(표식은 조상에 — CSS 는 자손만 제외한다).
        self.assertEqual(ref.count('className="col-span-full" data-attached-field-exempt'), 2)

    def test_router_customer_preview_before_detail(self) -> None:
        router = _read(BACKEND / "app" / "routers" / "transactions.py")
        prev = router.find("/sales-statement/customer-preview")
        detail = router.find('"/sales-statement/{order_key}"')
        self.assertGreater(prev, 0)
        self.assertGreater(detail, 0)
        self.assertLess(prev, detail)
        fn = router[prev : prev + 800]
        self.assertIn("jubun", fn)
        self.assertIn("bcode", fn)

    def test_inquiry_api_memo_preview(self) -> None:
        src = _read(FRONT / "lib" / "inquiry-api.ts")
        self.assertIn("memo_preview", src)
        self.assertIn("jubun:", src)


class SalesStatementStockQtyTest(IsolatedAsyncioTestCase):
    async def test_compute_stock_delegates_prinjing(self) -> None:
        import sys

        global sys_path_added
        if not sys_path_added:
            sys.path.insert(0, str(BACKEND))
            sys_path_added = True

        from unittest.mock import patch

        from app.services import transactions_service

        async def fake_prinjing(_server_id, *, ocode, bcode, hcode):
            self.assertEqual(ocode, "B")
            self.assertEqual(bcode, "BK99")
            self.assertEqual(hcode, "5019")
            return 694

        with patch(
            "app.services.prinjing_service.compute_warehouse_stock_qty",
            new=fake_prinjing,
        ):
            qty = await transactions_service.compute_sales_statement_stock_qty(
                "remote_138",
                bcode="BK99",
                hcode="5019",
                ocode="B",
            )

        self.assertEqual(qty, 694)

    async def test_customer_preview_uses_g1_fallback_hcodes(self) -> None:
        import sys

        if str(BACKEND) not in sys.path:
            sys.path.insert(0, str(BACKEND))

        from unittest.mock import AsyncMock, patch

        from app.services import transactions_service

        captured: dict[str, tuple[str, ...]] = {}

        async def fake_preview(**kwargs):
            captured["g1_fallback_hcodes"] = kwargs.get("g1_fallback_hcodes") or ()
            captured["hcode"] = kwargs.get("hcode") or ""
            return {
                "gcode": "00004",
                "customer_profile": {"gname": "영풍"},
                "stock_qty": None,
                "memo_preview": {},
            }

        with patch.object(
            transactions_service,
            "get_sales_statement_customer_preview",
            new=AsyncMock(side_effect=fake_preview),
        ):
            from app.core.hcode_isolation import resolve_scope_hcode
            from app.core.deps import enforce_hcode_isolation

            ctx = {
                "user_id": "u1",
                "server_id": "remote_153",
                "role": "operator",
                "hcode": "5019",
                "permissions": ["transactions.read"],
                "account_type": "T2_PUB",
            }
            scope = resolve_scope_hcode(ctx)
            self.assertEqual(scope, "5019")
            raw = ""
            publisher = "" if not raw else enforce_hcode_isolation(raw, ctx) or ""
            g1_fb = (scope,) if scope and not raw else ()
            await transactions_service.get_sales_statement_customer_preview(
                server_id="remote_153",
                gcode="00004",
                date_from="2026-05-14",
                date_to="2026-05-14",
                hcode=publisher,
                g1_fallback_hcodes=g1_fb,
            )

        self.assertEqual(captured["hcode"], "")
        self.assertEqual(captured["g1_fallback_hcodes"], ("5019",))

    async def test_list_sales_statements_gcode_in_filter(self) -> None:
        import sys

        if str(BACKEND) not in sys.path:
            sys.path.insert(0, str(BACKEND))

        from app.services import transactions_service
        import app.services.h2_branch_lookup as h2bl

        captured: list[tuple[str, tuple]] = []

        async def fake_query(_server_id, sql, params=None):
            captured.append((sql, tuple(params or ())))
            if "COUNT" in sql or "row_count" in sql.lower():
                return [{"row_count": 0}]
            return []

        async def noop_assert(**_kwargs):
            return None

        old_q = transactions_service.execute_query
        old_cg = transactions_service.count_grouped
        transactions_service.execute_query = fake_query

        async def fake_count(*_a, **_k):
            return 0

        transactions_service.count_grouped = fake_count
        old_assert = h2bl.assert_sales_statement_search_allowed
        h2bl.assert_sales_statement_search_allowed = noop_assert

        # 어댑터(SHOW COLUMNS 캐시) 는 자체 import 한 execute_query 를 쓰므로 함께 fake 로
        # 대체 — 미대체 시 servers.yaml 라이브 DB 로 나가 스위트 실행 순서(이벤트 루프)
        # 에 따라 실패하던 순서 의존을 제거한다.
        import app.services.s1_ssub_adapt as s1a
        import app.services.h2_gbun_adapt as h2a

        async def fake_adapter_query(_server_id, sql, params=None):
            up = sql.strip().upper()
            if up.startswith("SHOW COLUMNS FROM S1_SSUB"):
                return [{"Field": f} for f in (
                    "Gdate", "Hcode", "Jubun", "Gjisa", "Gcode", "Bcode", "Gubun",
                    "Scode", "Ocode", "Yesno", "Gsqut", "Gssum", "Gbigo", "Idnum",
                )]
            if up.startswith("SHOW COLUMNS FROM H2_GBUN"):
                return [{"Field": f} for f in (
                    "id", "Scode", "Gcode", "Hcode", "Gname", "oname", "gdate",
                    "gnum1", "jubun", "gbigo",
                )]
            return []

        old_s1_q = s1a.execute_query
        old_h2_q = h2a.execute_query
        s1a.execute_query = fake_adapter_query
        h2a.execute_query = fake_adapter_query
        s1a.clear_s1_column_cache_for_tests()
        h2a.clear_h2_column_cache_for_tests()
        try:
            await transactions_service.list_sales_statements(
                server_id="remote_138",
                date_from="2026-01-01",
                date_to="2026-01-31",
                gcode="00001",
                gjisa="2|부곡리(매장)",
                limit=10,
                offset=0,
            )
        finally:
            transactions_service.execute_query = old_q
            transactions_service.count_grouped = old_cg
            h2bl.assert_sales_statement_search_allowed = old_assert
            s1a.execute_query = old_s1_q
            h2a.execute_query = old_h2_q
            s1a.clear_s1_column_cache_for_tests()
            h2a.clear_h2_column_cache_for_tests()

        list_sql = next(
            (s for s, _ in captured if "FROM S1_Ssub" in s and "GROUP BY" in s),
            "",
        )
        self.assertIn("Gcode IN", list_sql)
        self.assertIn("COALESCE(Gjisa,'') IN", list_sql)
