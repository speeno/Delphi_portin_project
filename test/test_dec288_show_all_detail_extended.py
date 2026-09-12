"""DEC-288 — 「내용 전체 보기」 재정의를 입고명세서·도서별 판매로 확장 (2026-09-12).

사용자: "입고명세서, 도서별 판매의 전체보기도 유사하게 변경가능한지 확인후 필요하면 변경,
아니면 해당 버튼을 제거" → 두 화면 모두 **가능**해서 DEC-287(원장 2화면)과 같은 의미로 바꿨다:
체크하면 **상단 목록(그 페이지)에 보이는 모든 건**의 세부 내역이 하단에 함께 조회된다.

- 입고명세서: `list_receipt_lines_all` = 목록 페이지의 전표들 × 그 라인 (전표 상세를 이어 붙인 것).
- 도서별 판매: `get_book_sales_customers_all` = 목록 페이지의 도서들 × 거래처별 내역
  (도서 상세를 이어 붙인 것 — 분기표·0행 제외 규칙 공유).
"""

import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from app.services import inbound_service as inb
from app.services import reports_service as rs

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class InboundLinesAll(unittest.IsolatedAsyncioTestCase):
    async def _run(self, **kw):
        items = [
            {
                "receipt_key": {"gdate": "2026.09.01", "hcode": "5019", "gcode": "V1", "jubun": "1"},
                "publisher_name": "교문사", "vendor_name": "입고처1",
                "idnum": 7, "lines": 2, "qty": 30, "amount": 3000, "status": "done",
            },
            {
                "receipt_key": {"gdate": "2026.09.02", "hcode": "5019", "gcode": "V2", "jubun": "1"},
                "publisher_name": "교문사", "vendor_name": "입고처2",
                "idnum": 8, "lines": 1, "qty": 5, "amount": 500, "status": "pending",
            },
        ]
        line_rows = [
            {"Gdate": "2026.09.01", "Hcode": "5019", "Gcode": "V1", "Jubun": "1", "Bcode": "B1",
             "Pubun": "", "Gsqut": 20, "Gdang": 100, "Grat1": 80, "Gssum": 2000, "Gbigo": "", "Yesno": "1"},
            {"Gdate": "2026.09.01", "Hcode": "5019", "Gcode": "V1", "Jubun": "1", "Bcode": "B2",
             "Pubun": "", "Gsqut": 10, "Gdang": 100, "Grat1": 80, "Gssum": 1000, "Gbigo": "", "Yesno": "1"},
            {"Gdate": "2026.09.02", "Hcode": "5019", "Gcode": "V2", "Jubun": "1", "Bcode": "B1",
             "Pubun": "", "Gsqut": 5, "Gdang": 100, "Grat1": 80, "Gssum": 500, "Gbigo": "", "Yesno": "0"},
            # 다른 페이지/취소 전표 — 키가 목록에 없으므로 결과에서 빠져야 한다
            {"Gdate": "2026.09.02", "Hcode": "5019", "Gcode": "V9", "Jubun": "3", "Bcode": "B3",
             "Pubun": "", "Gsqut": 99, "Gdang": 100, "Grat1": 80, "Gssum": 9900, "Gbigo": "", "Yesno": "2"},
        ]

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            self.assertIn("{placeholders}", sql_template)
            return line_rows

        with patch.object(inb, "list_receipts", AsyncMock(return_value=(items, len(items)))), \
             patch.object(inb, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)), \
             patch.object(inb, "_fetch_product_names", AsyncMock(return_value={"B1": "도서1"})), \
             patch.object(inb, "_attach_isbn", AsyncMock(return_value=None)), \
             patch.object(inb, "mysql3_protocol", lambda s: False):
            return await inb.list_receipt_lines_all(
                server_id="remote_153", date_from="2026-09-01", date_to="2026-09-12",
                hcode="5019", limit=20, offset=0, **kw,
            )

    async def test_lines_are_scoped_to_listed_receipts(self):
        res = await self._run()
        self.assertEqual(res["receipts"], 2)
        self.assertEqual([l["bcode"] for l in res["lines"]], ["B1", "B2", "B1"])
        self.assertNotIn("B3", [l["bcode"] for l in res["lines"]])  # 목록에 없는 전표 라인 제외

    async def test_rows_carry_slip_identity_and_names(self):
        res = await self._run()
        first = res["lines"][0]
        self.assertEqual(first["idnum"], 7)
        self.assertEqual(first["gdate"], "2026.09.01")
        self.assertEqual(first["vendor_name"], "입고처1")
        self.assertEqual(first["bname"], "도서1")
        self.assertEqual((first["gsqut"], first["gssum"]), (20, 2000))
        self.assertEqual(res["lines"][-1]["vendor_name"], "입고처2")

    async def test_single_line_query_not_per_receipt(self):
        """전표마다 상세를 치지 않는다 — 일자 청크 lookup 1경로."""
        with patch.object(inb, "get_receipt_detail", AsyncMock()) as detail:
            await self._run()
            detail.assert_not_called()


class BookSalesCustomersAll(unittest.IsolatedAsyncioTestCase):
    async def _run(self):
        rows = [
            {"Bcode": "B1", "Gcode": "C1", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 10, "Gssum": 1000},
            {"Bcode": "B1", "Gcode": "C2", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 5, "Gssum": 500},
            {"Bcode": "B2", "Gcode": "C1", "Scode": "X", "Gubun": "반품", "Pubun": "반품",
             "Gsqut": -2, "Gssum": -200},
            # 전 측정치 0 → 결과에서 제외되어야 한다
            {"Bcode": "B2", "Gcode": "C9", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gsqut": 0, "Gssum": 0},
        ]

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            if "G1_Ggeo" in sql_template:
                return [{"gcode": "C1", "gname": "거래처1"}]
            self.assertIn("GROUP BY Bcode, Gcode", sql_template)
            return rows

        with patch.object(rs, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)), \
             patch.object(rs, "fetch_book_meta", AsyncMock(return_value={"B1": {"gname": "도서1"}})):
            return await rs.get_book_sales_customers_all(
                server_id="remote_153", hcode="5019",
                date_from="2026-08-01", date_to="2026-09-12",
                bcodes=["B1", "B2"],
            )

    async def test_rows_per_book_and_customer(self):
        res = await self._run()
        self.assertEqual(res["books"], 2)
        self.assertEqual(
            [(r["bcode"], r["gcode"]) for r in res["rows"]],
            [("B1", "C1"), ("B1", "C2"), ("B2", "C1")],  # 상단 목록 순서 → 거래처 코드 순
        )
        self.assertEqual(res["rows"][0]["goqut"], 10)
        self.assertEqual(res["rows"][0]["gosum"], 1000)
        self.assertEqual(res["rows"][2]["gbqut"], -2)

    async def test_names_attached(self):
        res = await self._run()
        self.assertEqual(res["rows"][0]["bname"], "도서1")
        self.assertEqual(res["rows"][0]["gname"], "거래처1")
        self.assertEqual(res["rows"][1]["gname"], "")   # 미조회 거래처는 빈 이름(코드 표시는 화면)

    async def test_empty_bcodes_short_circuits(self):
        res = await rs.get_book_sales_customers_all(
            server_id="remote_153", hcode="5019",
            date_from="2026-08-01", date_to="2026-09-12", bcodes=[],
        )
        self.assertEqual(res, {"rows": [], "books": 0})


class RoutesAndProbe(unittest.TestCase):
    def test_routes_registered_with_hcode_isolation(self):
        for rel, path, fn in (
            ("routers/inbound.py", "/receipts/lines-all", "list_receipt_lines_all"),
            ("routers/reports.py", "/book-sales/customers-all", "get_book_sales_customers_all"),
        ):
            src = (BACK / rel).read_text(encoding="utf-8")
            self.assertIn(f'@router.get("{path}")', src)
            block = src.split(f'@router.get("{path}")')[1].split("@router.get(")[0]
            self.assertIn("enforce_hcode_isolation(hcode, current)", block, path)
            self.assertIn(f"{fn}(", block)

    def test_lines_all_declared_before_dynamic_receipt_route(self):
        """FastAPI 라우트 순서 — `/receipts/{receipt_key}` 보다 먼저여야 static 경로가 잡힌다."""
        src = (BACK / "routers" / "inbound.py").read_text(encoding="utf-8")
        self.assertLess(
            src.index('@router.get("/receipts/lines-all")'),
            src.index('@router.get("/receipts/{receipt_key}"'),
        )

    def test_probe_matrix_registered(self):
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("inbound.receipt_lines_all", probe)
        self.assertIn("reports.book_sales_customers_all", probe)


class ScreensShowAll(unittest.TestCase):
    """두 화면 — 「내용 전체 보기」가 상단 펼치기가 아니라 하단 전 건 상세."""

    CASES = (
        ("app/(app)/transactions/inbound-statement/page.tsx", "linesAll", "전체 전표 라인"),
        ("app/(app)/reports/book-sales/page.tsx", "bookSalesCustomersAll", "도서별 거래처 상세 내역"),
    )

    def test_show_all_loads_full_detail(self):
        for rel, api_fn, title in self.CASES:
            src = _read(rel)
            self.assertIn("내용 전체 보기", src, rel)
            self.assertIn(api_fn, src, rel)
            self.assertIn(title, src, rel)

    def test_show_all_no_longer_expands_top_grid(self):
        for rel, *_ in self.CASES:
            src = _read(rel)
            self.assertNotIn("unbounded={showAll}", src, rel)
            self.assertNotIn("fillHeight={!showAll}", src, rel)

    def test_split_stays_on_when_show_all(self):
        self.assertIn(
            "disabled={!showAll && !selectedKey}",
            _read("app/(app)/transactions/inbound-statement/page.tsx"),
        )
        self.assertIn("disabled={!showAll && !detail}", _read("app/(app)/reports/book-sales/page.tsx"))

    def test_identity_columns_prepended_in_all_mode(self):
        """여러 전표/도서가 한 표에 섞이므로 식별 컬럼이 앞에 붙는다."""
        inbound = _read("app/(app)/transactions/inbound-statement/page.tsx")
        self.assertIn("ALL_LINE_KEY_COLUMNS", inbound)
        self.assertIn("showAll ? [...ALL_LINE_KEY_COLUMNS, ...cols] : cols", inbound)
        sales = _read("app/(app)/reports/book-sales/page.tsx")
        self.assertIn("ALL_BOOK_KEY_COLUMNS", sales)
        self.assertIn("showAll ? [...ALL_BOOK_KEY_COLUMNS, ...cols] : cols", sales)


class AllMasterDetailScreensCovered(unittest.TestCase):
    """사용자 규칙(2026-09-12): 「내용 전체 보기」는 **상단 목록 + 하단 세부 목록** 화면의 공통 기능.

    마스터-디테일 화면을 하나라도 빠뜨리면 실패한다 — 새 2단 화면을 만들 때도 같이 붙이라는 가드.
    """

    # (화면, 전체 보기 데이터 경로 토큰) — 토큰은 그 화면이 «전 건»을 가져오는 방식.
    SCREENS = (
        ("app/(app)/ledger/customer/page.tsx", "customer-ledger/slip-detail-all"),
        ("app/(app)/inventory/ledger/page.tsx", "book-ledger/day-detail-all"),
        ("app/(app)/ledger/customer-integrated/page.tsx", "customer-ledger/daily-all"),
        ("app/(app)/ledger/book-summary/page.tsx", "book-summary/months-all"),
        ("app/(app)/ledger/receivable/page.tsx", "showAll || selGubun === null"),
        ("app/(app)/inventory/value/page.tsx", "showAll\n        ? (data?.by_book ?? [])"),
        ("app/(app)/transactions/inbound-statement/page.tsx", "inboundApi.linesAll"),
        ("app/(app)/reports/book-sales/page.tsx", "bookSalesCustomersAll"),
        ("app/(app)/reports/customer-sales/page.tsx", "customerSalesBooksAll"),
        ("app/(app)/returns/ledger/page.tsx", "detailAll"),
        ("app/(app)/returns/period-report/page.tsx", "detailAll"),
        ("components/transactions/transaction-status-screen.tsx", "axis.api.linesAll"),
    )

    def test_every_master_detail_screen_has_show_all(self):
        for rel, token in self.SCREENS:
            src = _read(rel)
            self.assertIn("내용 전체 보기", src, f"{rel}: 「내용 전체 보기」 체크박스 없음")
            self.assertIn("showAll", src, rel)
            self.assertIn(token, src, f"{rel}: 전 건 조회 경로({token}) 없음")

    def test_no_split_screen_left_without_show_all(self):
        """SplitListPanes 를 쓰는 2단 화면 중 체크박스가 없는 화면 목록을 고정(신규 화면 알림)."""
        app = FRONT / "app"
        left = []
        for path in sorted(app.glob("**/page.tsx")) + sorted((FRONT / "components").glob("**/*.tsx")):
            src = path.read_text(encoding="utf-8")
            if "SplitListPanes" not in src or "내용 전체 보기" in src:
                continue
            left.append(str(path.relative_to(FRONT)))
        self.assertEqual(
            sorted(left),
            sorted([
                # 두 표가 서로 독립(마스터-디테일 아님) — 하단이 이미 전 건이라 대상이 아니다.
                "app/(app)/inbound/reports/daily/page.tsx",
                "app/(app)/inbound/reports/period/page.tsx",
                # 총판/출판 비율 프로필 2축 편집 화면(목록-상세 아님).
                "app/(app)/master/special/page.tsx",
                # 공용 컴포넌트(분할 자체) — 화면이 아니다.
                "components/shared/split-list-panes.tsx",
            ]),
            f"2단 화면인데 「내용 전체 보기」가 없다(또는 예외 목록 갱신 필요): {sorted(left)}",
        )


if __name__ == "__main__":
    unittest.main()
