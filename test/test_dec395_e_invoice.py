"""DEC-395 — [정산관리] 전자계산서: 메뉴 명칭·순서 · 조회월 거래처별 매출금액(출고−반품) + 계산서 정보 · 엑셀.

요청(2026-10-09): 「세금계산서 발행」 → 명칭 「전자계산서」, 순서 = 입출금전표거래처 – 계산서 발행 – 미수현황,
그외 청구서관리 · 청구금액(년월) · 청구서인쇄(미리보기) 불필요. 컬럼 순서 = 코드 · 사업자등록번호 · 거래처명 ·
대표자 · 주소 · 업태 · 종목 · 이메일1 · 이메일2 · 매출금액(출고금액-반품금액, 콤마). 해당 자료 엑셀 다운로드.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.routers.auth import get_current_user
from app.services import e_invoice_service

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
REGISTRY = FRONT / "lib" / "form-registry.ts"
PAGE = FRONT / "app" / "(app)" / "settlement" / "e-invoice" / "page.tsx"


def _sales(rows):
    return AsyncMock(return_value={"rows": rows, "total": len(rows), "truncated": False, "totals": {}})


class MonthRangeTests(TestCase):
    def test_formats(self) -> None:
        self.assertEqual(e_invoice_service.month_range("202609"), ("2026-09-01", "2026-09-30"))
        self.assertEqual(e_invoice_service.month_range("2024-02"), ("2024-02-01", "2024-02-29"))

    def test_invalid(self) -> None:
        for bad in ("", "2026", "202613", "2026-9"):
            with self.assertRaises(e_invoice_service.EInvoiceValidationError):
                e_invoice_service.month_range(bad)


class ListTargetsTests(IsolatedAsyncioTestCase):
    async def test_sales_is_out_minus_return_and_zero_rows_dropped(self) -> None:
        rows = [
            {"hcode": "5019", "gcode": "00004", "gname": "영풍", "gosum": 100_000, "gbsum": -30_000},
            {"hcode": "5019", "gcode": "00001", "gname": "교보", "gosum": 500_000, "gbsum": 0},
            {"hcode": "5019", "gcode": "00007", "gname": "수금만", "gosum": 0, "gbsum": 0},
            {"hcode": "5019", "gcode": "00009", "gname": "상쇄", "gosum": 20_000, "gbsum": -20_000},
            {"hcode": "5019", "gcode": "00012", "gname": "반품초과", "gosum": 0, "gbsum": -5_000},
        ]
        masters = {
            "00001": {"gname": "(주)교보문고", "gnumb": "102-81-11670", "gposa": "허정도", "gadd1": "서울 종로구",
                      "gadd2": "종로1가 1", "guper": "도소매", "gjomo": "도서", "email": "kb@x.kr"},
        }
        with patch.object(e_invoice_service.reports_service, "get_customer_sales", _sales(rows)) as gs, \
             patch.object(e_invoice_service, "_master_map", AsyncMock(return_value=masters)), \
             patch.object(e_invoice_service.customer_ext_service, "get_ext_many",
                          AsyncMock(return_value={"00001": {"email2": "tax@kb.kr"}})):
            res = await e_invoice_service.list_targets(server_id="remote_153", hcode="5019", month="202609")

        kw = gs.await_args.kwargs
        self.assertEqual((kw["date_from"], kw["date_to"], kw["scope"], kw["hcode"]), ("2026-09-01", "2026-09-30", "X", "5019"))
        self.assertEqual([i["gcode"] for i in res["items"]], ["00001", "00004", "00012"])  # 코드 순 · 0 제외
        self.assertEqual([i["sales"] for i in res["items"]], [500_000, 70_000, -5_000])
        self.assertEqual(res["totals"], {"sales": 565_000})
        kb = res["items"][0]
        self.assertEqual(
            {k: kb[k] for k in ("gnumb", "gname", "gposa", "gjuso", "guper", "gjomo", "email1", "email2")},
            {"gnumb": "102-81-11670", "gname": "(주)교보문고", "gposa": "허정도", "gjuso": "서울 종로구 종로1가 1",
             "guper": "도소매", "gjomo": "도서", "email1": "kb@x.kr", "email2": "tax@kb.kr"},
        )
        self.assertEqual(res["items"][1]["gname"], "영풍")  # 마스터에 없으면 매출 집계의 이름

    async def test_pages_through_customer_sales(self) -> None:
        page1 = {"rows": [{"hcode": "5019", "gcode": "00001", "gosum": 1, "gbsum": 0}], "total": 2, "truncated": False}
        page2 = {"rows": [{"hcode": "5019", "gcode": "00002", "gosum": 2, "gbsum": 0}], "total": 2, "truncated": False}
        with patch.object(e_invoice_service.reports_service, "get_customer_sales", AsyncMock(side_effect=[page1, page2])), \
             patch.object(e_invoice_service, "_master_map", AsyncMock(return_value={})), \
             patch.object(e_invoice_service.customer_ext_service, "get_ext_many", AsyncMock(return_value={})):
            res = await e_invoice_service.list_targets(server_id="remote_153", hcode="5019", month="202609")
        self.assertEqual([i["gcode"] for i in res["items"]], ["00001", "00002"])

    async def test_master_lookup_is_hcode_scoped_and_drift_safe(self) -> None:
        """G1_Ggeo 는 공유 테이블 — Hcode 바인딩 필수. 테넌트에 없는 컬럼은 '' 리터럴(DEC-033)."""
        lookup = AsyncMock(return_value=[])
        with patch.object(e_invoice_service, "g1_geo_column_meta",
                          AsyncMock(return_value=({"gnumb", "email"}, {"gnumb": "Gnumb", "email": "Email"}))), \
             patch.object(e_invoice_service, "in_clause_lookup", lookup):
            await e_invoice_service._master_map("remote_153", "5019", ["00001"])
        sql = lookup.await_args.kwargs["sql_template"]
        self.assertIn("WHERE Hcode=%s AND Gcode IN", sql)
        self.assertEqual(lookup.await_args.kwargs["prefix_params"], ("5019",))
        self.assertIn("IFNULL(Gnumb,'') AS gnumb", sql)
        self.assertIn("'' AS gposa", sql)
        self.assertNotIn("COALESCE", sql)


class RouterTests(TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = lambda: {"user_id": "hong01", "server_id": "remote_1", "hcode": "5019"}
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.pop(get_current_user, None)

    def test_scope_hcode_injected(self) -> None:
        fake = AsyncMock(return_value={"items": [], "totals": {"sales": 0}, "total": 0, "truncated": False})
        with patch.object(e_invoice_service, "list_targets", fake):
            res = self.client.get("/api/v1/settlement/e-invoice?serverId=remote_1&month=202609")
        self.assertEqual(res.status_code, 200, res.text[:200])
        self.assertEqual(fake.await_args.kwargs["hcode"], "5019")

    def test_other_tenant_hcode_ignored(self) -> None:
        """격리 계정(출판사)은 요청 hcode 를 무시하고 본인 코드 — 정산 라우터 공통 출판사 행 스코프(DEC-090/091)."""
        fake = AsyncMock(return_value={"items": [], "totals": {"sales": 0}, "total": 0, "truncated": False})
        with patch.object(e_invoice_service, "list_targets", fake):
            res = self.client.get("/api/v1/settlement/e-invoice?serverId=remote_1&month=202609&hcode=4201")
        self.assertEqual(res.status_code, 200, res.text[:200])
        self.assertEqual(fake.await_args.kwargs["hcode"], "5019")

    def test_bad_month_422(self) -> None:
        res = self.client.get("/api/v1/settlement/e-invoice?serverId=remote_1&month=2026")
        self.assertEqual(res.status_code, 422)


def _settlement_entries() -> list[tuple[str, str, bool]]:
    src = REGISTRY.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = src.split("export const FORM_REGISTRY: FormMeta[] = [", 1)[1]
    out = []
    for blk in re.split(r"\n  \{\n", body):
        head = blk.split("\n  },")[0]
        if 'menuGroup: "settlement"' not in head:
            continue
        fid = re.search(r'id:\s*"([^"]+)"', head).group(1)
        caption = re.search(r'caption:\s*"([^"]+)"', head).group(1)
        menu_id = (re.search(r'menuId:\s*"([^"]+)"', head) or [None, ""])[1]
        shown = "hiddenFromMenu: true" not in head and "HIDDEN" not in menu_id
        out.append((fid, caption, shown))
    return out


class MenuTests(TestCase):
    def test_visible_order(self) -> None:
        shown = [c for _, c, s in _settlement_entries() if s]
        self.assertEqual(shown, ["입출금전표 거래처", "전자계산서", "미수현황"])

    def test_unneeded_menus_hidden_but_routes_kept(self) -> None:
        entries = {fid: s for fid, _, s in _settlement_entries()}
        for fid in ("Sobo45_billing", "Sobo47_billing", "Sobo46_billing", "Sobo49_tax"):
            self.assertIn(fid, entries, f"{fid} 항목(라우트)은 남아 있어야 한다")
            self.assertFalse(entries[fid], f"{fid} 는 정산관리 메뉴에서 감춤")

    def test_page_columns_in_requested_order(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        block = src.split("const COLUMNS", 1)[1].split("];", 1)[0]
        labels = re.findall(r'label:\s*"([^"]+)"', block)
        self.assertEqual(labels, ["코드", "사업자등록번호", "거래처명", "대표자", "주소", "업태", "종목", "이메일1", "이메일2", "매출금액"])
        self.assertIn('numFmt: SALES_FMT', src)
        self.assertIn('const SALES_FMT = "#,##0"', src)


if __name__ == "__main__":
    unittest.main()
