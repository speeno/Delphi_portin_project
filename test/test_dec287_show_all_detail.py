"""DEC-287 — 「내용 전체 보기」 = 상단 목록 전 건의 하단 상세 + 같은 행 재클릭 선택 유지.

사용자 리포트(2026-09-12, 거래처거래원장 스크린샷 2장):
1. 상단 목록의 항목을 한 번 더 누르거나 더블클릭하면 선택이 풀려 목록이 전체 목록으로 돌아간다.
2. 「내용 전체 보기」는 상단 표를 페이징 없이 펼치는 기능이 아니라, 켜면 **상단에 조회된 모든 건**의
   세부 도서 정보가 하단 목록에 함께 조회되는 기능이다 (DEC-203 14:31 정의를 대체).

여기서는 ① 두 원장의 「전체 상세」 서비스(전표별/일자별 상세를 이어 붙인 것 = 앵커 규칙),
② 라우트·프로브 등록, ③ 화면 배선(전체 보기 = 하단 전체 상세 / 재클릭 선택 유지)을 고정한다.
"""

import re
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from app.services import book_ledger_service as book_svc
from app.services import customer_txn_ledger_service as cust_svc

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class CustomerSlipDetailAll(unittest.IsolatedAsyncioTestCase):
    """전표별 상세를 차례로 눌러 본 결과와 동일 — 전표마다 직전 미수에서 running 을 이어받는다."""

    async def _run(self):
        s1_daily = [
            {"Gdate": "2026.02.20", "Gubun": "출고", "Pubun": "", "Jubun": "11", "Gjisa": "",
             "Bcode": "B1", "Gbigo": "", "qty": 100, "amt": 1000},
            {"Gdate": "2026.02.20", "Gubun": "출고", "Pubun": "", "Jubun": "11", "Gjisa": "",
             "Bcode": "B2", "Gbigo": "", "qty": 12, "amt": 500},
            {"Gdate": "2026.03.26", "Gubun": "반품", "Pubun": "반품", "Jubun": "12", "Gjisa": "",
             "Bcode": "B1", "Gbigo": "", "qty": -34, "amt": -300},
        ]
        s1_lines = [
            {"Gdate": "2026.02.20", "Gubun": "출고", "Pubun": "", "Bcode": "B1", "Gbigo": "",
             "Gjisa": "", "Jubun": "11", "grat1": 80, "qty": 100, "amt": 1000},
            {"Gdate": "2026.02.20", "Gubun": "출고", "Pubun": "", "Bcode": "B2", "Gbigo": "",
             "Gjisa": "", "Jubun": "11", "grat1": 85, "qty": 12, "amt": 500},
            {"Gdate": "2026.03.26", "Gubun": "반품", "Pubun": "반품", "Bcode": "B1", "Gbigo": "",
             "Gjisa": "", "Jubun": "12", "grat1": 80, "qty": -34, "amt": -300},
        ]
        h1_rows = [
            {"Gdate": "2026.03.16", "Gubun": "입금", "Pubun": "현금", "Ocode": "",
             "Oname": "대학서적", "Gbigo": "", "amt": 700},
        ]

        async def fake_query(server_id, sql, params=None):
            if "FROM S1_Ssub" in sql and "Grat1" in sql:
                return s1_lines           # 전체 상세용 라인 조회
            if "FROM S1_Ssub" in sql:
                return s1_daily           # 상단 전표 목록용
            if "FROM H1_Ssub" in sql and "Oname" in sql:
                return h1_rows
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            return [{"Gcode": "B1", "Gname": "테스트도서", "gdang": 10000}]

        with patch.object(cust_svc, "execute_query", AsyncMock(side_effect=fake_query)), \
             patch.object(cust_svc, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)), \
             patch.object(cust_svc, "attach_book_meta", AsyncMock(side_effect=lambda *a, **k: a[2])), \
             patch.object(cust_svc, "_opening_receivable", AsyncMock(return_value=2000)):
            return await cust_svc.customer_ledger_slip_detail_all(
                server_id="remote_153", hcode="5019", gcode="1015",
                date_from="2026-01-01", date_to="2026-09-12",
            )

    async def test_running_anchors_per_slip(self):
        res = await self._run()
        self.assertEqual(res["opening"], 2000)
        self.assertEqual([r["balance"] for r in res["items"]], [3000, 3500, 2500])
        # 수금(H1 700)은 도서 라인이 없다 → 반품 전표는 2800(수금 반영 미수)에서 이어받는다.
        self.assertEqual(res["items"][-1]["balance"], 2800 - 300)
        self.assertEqual(res["closing"], 2500)          # 기간 말 미수 = 상단 합계 미수
        self.assertEqual(res["slips"], 2)               # 수금 전표 제외

    async def test_rows_mirror_single_slip_detail(self):
        res = await self._run()
        first = res["items"][0]
        self.assertEqual(first["gname"], "테스트도서")   # G4 이름 미조회 코드는 코드 그대로
        self.assertEqual(res["items"][1]["gname"], "B2")
        self.assertEqual((first["price"], first["grat1"], first["qty"]), (10000, 80, 100))
        self.assertEqual((first["out_amt"], first["rtn_amt"]), (1000, 0))
        rtn = res["items"][-1]
        self.assertEqual((rtn["out_amt"], rtn["rtn_amt"]), (0, -300))

    async def test_no_giant_in_clause(self):
        """기간 전체라 도서코드가 많다 — 마스터 lookup 은 청크(in_clause_lookup) 경로."""
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "services"
               / "customer_txn_ledger_service.py").read_text(encoding="utf-8")
        body = src.split("async def customer_ledger_slip_detail_all")[1].split("\nasync def ")[0]
        self.assertIn("in_clause_lookup(", body)
        self.assertNotIn('",".join(["%s"]', body)


class BookDayDetailAll(unittest.IsolatedAsyncioTestCase):
    """일자별 상세를 차례로 눌러 본 결과와 동일 — 일자마다 전일재고에서 running 을 이어받는다."""

    async def _run(self):
        agg = [
            {"Gdate": "2026.01.05", "Scode": "X", "Gubun": "출고", "Pubun": "", "qty": 10},
            {"Gdate": "2026.01.06", "Scode": "Y", "Gubun": "입고", "Pubun": "", "qty": 20},
            {"Gdate": "2026.01.07", "Scode": "X", "Gubun": "출고", "Pubun": "", "qty": 5},
        ]
        lines = [
            {"Gdate": "2026.01.05", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gcode": "G1",
             "Gjisa": "", "Gbigo": "", "grat1": 80, "qty": 10, "amt": 1000},
            {"Gdate": "2026.01.06", "Scode": "Y", "Gubun": "입고", "Pubun": "", "Gcode": "G2",
             "Gjisa": "", "Gbigo": "", "grat1": 70, "qty": 20, "amt": 2000},
            {"Gdate": "2026.01.07", "Scode": "X", "Gubun": "출고", "Pubun": "", "Gcode": "G1",
             "Gjisa": "", "Gbigo": "", "grat1": 80, "qty": 5, "amt": 500},
        ]

        async def fake_query(server_id, sql, params=None):
            if "FROM Sg_Csum" in sql:
                return [{"Gdate": "2026.01.06", "qty": 5}]   # 라인 없는 「변경」 +5
            if "FROM S1_Ssub" in sql and "SUM(" in sql:
                return agg
            if "FROM S1_Ssub" in sql:
                return lines
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            return [{"Gcode": "G1", "Gname": "가나문고"}]

        with patch.object(book_svc, "execute_query", AsyncMock(side_effect=fake_query)), \
             patch.object(book_svc, "in_clause_lookup", AsyncMock(side_effect=fake_in_clause)), \
             patch.object(book_svc, "fetch_book_meta", AsyncMock(return_value={})), \
             patch.object(book_svc, "_fetch_stock_asof", AsyncMock(return_value={"3226": 100})):
            return await book_svc.book_ledger_day_detail_all(
                server_id="remote_153", hcode="5019", bcode="3226",
                date_from="2026-01-01", date_to="2026-01-31",
            )

    async def test_running_reanchors_each_day(self):
        res = await self._run()
        self.assertEqual(res["opening"], 100)
        # 1.05 100−10=90 · 1.06 90+20=110(변경 +5 는 라인이 없어 일자 잔량 115) ·
        # 1.07 은 **상단 잔량 115** 에서 다시 앵커 → 110 (라인 running 누적이 아니다)
        self.assertEqual([r["balance"] for r in res["items"]], [90, 110, 110])
        self.assertEqual(res["closing"], 110)    # 기간 말 현재고 = 상단 합계
        self.assertEqual(res["days"], 3)

    async def test_row_shape_matches_day_detail(self):
        res = await self._run()
        self.assertEqual(res["items"][0]["gname"], "가나문고")
        self.assertEqual(res["items"][0]["out_qty"], 10)
        self.assertTrue(res["items"][1]["gname"].startswith("입고("))
        self.assertEqual(res["items"][1]["in_qty"], 20)


class RoutesAndProbe(unittest.TestCase):
    def setUp(self) -> None:
        self.router = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers"
                       / "inventory.py").read_text(encoding="utf-8")

    def test_routes_registered_with_hcode_isolation(self):
        for path, fn in (
            ("/book-ledger/day-detail-all", "book_ledger_day_detail_all"),
            ("/customer-ledger/slip-detail-all", "customer_ledger_slip_detail_all"),
        ):
            self.assertIn(f'@router.get("{path}")', self.router)
            block = self.router.split(f'@router.get("{path}")')[1].split("@router.get(")[0]
            self.assertIn("enforce_hcode_isolation(hcode, current)", block, path)
            self.assertIn(f"{fn}(", block)
            self.assertIn('alias="dateFrom"', block)

    def test_probe_matrix_registered(self):
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("inventory.book_ledger_day_detail_all", probe)
        self.assertIn("inventory.customer_ledger_slip_detail_all", probe)


class LedgerScreensShowAll(unittest.TestCase):
    """두 원장 화면 — 「내용 전체 보기」 = 하단 전체 상세(상단 표를 펼치는 기능이 아니다)."""

    # (화면, 선택 상태 변수, 전체 상세 엔드포인트, 체크 시 하단 표 제목, 체크박스 라벨)
    # 거래처원장 라벨/제목은 사용자 지정(2026-09-12): 「일자별 출고 상세」 → 「일자별 출고 도서 상세 내역」.
    CASES = (
        ("app/(app)/ledger/customer/page.tsx", "selKey", "customer-ledger/slip-detail-all",
         "일자별 출고 도서 상세 내역", "일자별 출고 상세"),
        ("app/(app)/inventory/ledger/page.tsx", "selDate", "book-ledger/day-detail-all",
         "전체 일자 상세 조회", "내용 전체 보기"),
    )

    def test_show_all_loads_full_detail(self):
        for rel, sel, endpoint, title, label in self.CASES:
            src = _read(rel)
            self.assertIn(label, src)
            self.assertIn('data-legacy-id="ShowAll"', src)
            self.assertIn(endpoint, src, rel)
            self.assertIn("setAllDetail", src, rel)
            self.assertIn(title, src, rel)
            # 하단은 전체 보기면 선택 없이도 표시 / 분할도 유지된다
            self.assertIn(f"disabled={{!showAll && {sel} === null}}", src, rel)
            self.assertIn(f"!showAll && {sel} === null ? (", src, rel)

    def test_show_all_no_longer_expands_top_grid(self):
        """종전 정의(unbounded 로 상단 표 펼치기)는 제거 — 상단은 분할 칸을 채운다."""
        for rel, *_ in self.CASES:
            src = _read(rel)
            self.assertNotIn("unbounded={showAll}", src, rel)
            self.assertNotIn("fillHeight={!showAll}", src, rel)


class ReselectKeepsSelection(unittest.TestCase):
    """마스터-디테일 화면: 같은 행 재클릭/더블클릭이 선택을 풀면 안 된다(하단이 초기화됨)."""

    SCREENS = (
        "app/(app)/ledger/customer/page.tsx",
        "app/(app)/inventory/ledger/page.tsx",
        "app/(app)/ledger/customer-integrated/page.tsx",
        "app/(app)/ledger/book-summary/page.tsx",
        "app/(app)/transactions/inbound-statement/page.tsx",
        "app/(app)/reports/customer-sales/page.tsx",
        "components/transactions/transaction-status-screen.tsx",
    )
    # `if (key === selectedKey) { setSelectedKey(null); ... }` 형태의 «접기» 분기
    COLLAPSE = re.compile(
        r"if\s*\([^)]*===[^)]*\)\s*\{\s*\n\s*set(?:Sel|selected)\w*\(null\)", re.IGNORECASE
    )

    def test_no_collapse_branch_left(self):
        for rel in self.SCREENS:
            src = _read(rel)
            self.assertIsNone(self.COLLAPSE.search(src), f"{rel}: 같은 행 재클릭 시 선택 해제 분기 잔존")

    def test_same_key_returns_immediately(self):
        for rel in self.SCREENS:
            src = _read(rel)
            self.assertRegex(src, r"if \([^)]+===[^)]+\) return;", rel)


if __name__ == "__main__":
    unittest.main()
