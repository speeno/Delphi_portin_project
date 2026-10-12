"""DEC-398 · DEC-399 — 거래명세서 거래처코드 · 거래처명-지점 · 배송 칸 (2026-10-12).

DEC-398 「출력 시 거래처코드가 거래처별로 나와야 하는데 5019 로 모두 동일하게 출력된다」:
  삼련 명세서 「거래처코드」가 ``customer.hcode``(S1_Ssub.Hcode)였다. 교문사(chul_09)는 Hcode 가 출판사(5019),
  거래처는 S1_Ssub.Gcode(예: 교보문고 00001) — 레거시 실물은 00001. 거래처명을 찾은 쪽 코드를 찍는다.
DEC-399 「출고현황 - 거래명세서: 거래처명 옆 지점명 · 출고 완료 이후 도서 옆 출고 여부」:
  목록 · 상세 팝업 거래처명 = 「거래처명-지점」(인쇄 DEC-393 과 같은 규칙), 상세 라인 끝 「배송」(완료 · 접수 · 취소).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from app.services import transactions_service as tx
from app.services.g1_geo_lookup import g1_code_for_slip, g1_gname_for_slip

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _fe(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


class CustomerCode(unittest.TestCase):
    def test_publisher_hcode_tenant_prints_customer_gcode(self) -> None:
        pair = {("5019", "00001"): "(주)교보문고"}
        self.assertEqual(g1_gname_for_slip("5019", "00001", pair), "(주)교보문고")
        self.assertEqual(g1_code_for_slip("5019", "00001", pair), "00001")

    def test_hcode_is_customer_data_keeps_hcode(self) -> None:
        pair = {("A123", "A123"): "어느서점"}  # (Hcode, Hcode) 로만 이름을 찾는 자료 — Gcode 는 거래처가 아니다
        self.assertEqual(g1_code_for_slip("A123", "B999", pair), "A123")

    def test_no_name_or_no_gcode(self) -> None:
        self.assertEqual(g1_code_for_slip("5019", "00002", {}), "00002")
        self.assertEqual(g1_code_for_slip("5019", "", {}), "5019")

    def test_triplicate_prints_code_not_publisher(self) -> None:
        detail = {
            "order_key": {"gdate": "2026.10.08", "hcode": "5019", "jubun": "1", "gjisa": ""},
            "customer": {"hcode": "5019", "gname": "(주)교보문고", "gcode": "00001", "code": "00001"},
            "lines": [{"gcode": "00001", "bcode": "B1", "product_name": "도서", "shelf": "A1", "pubun": "",
                       "gsqut": 1, "gdang": 1000, "grat1": 85, "gssum": 850, "gbigo": ""}],
        }
        html = tx.render_sales_statement_html(detail, layout="legacy_triplicate", server_id="remote_1", user_id="u")
        codes = re.findall(r"data-legacy-id='Sobo21.Triplicate.Hcode'><span class='cval'>([^<]*)<", html)
        self.assertTrue(codes)
        self.assertEqual(set(codes), {"00001"})
        # 구 detail(code 없음)은 종전대로 hcode
        old = {**detail, "customer": {"hcode": "H1", "gname": "x"}}
        html_old = tx.render_sales_statement_html(old, layout="legacy_triplicate", server_id="remote_1", user_id="u")
        self.assertIn("<span class='cval'>H1</span>", html_old)

    def test_detail_exposes_customer_code(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "services" / "transactions_service.py").read_text(encoding="utf-8")
        self.assertIn('"code": g1_code_for_slip(hcode, stmt_gcode, pair_map),', src)
        # 삼련 · A4 렌더러 모두 code 우선
        self.assertEqual(src.count('hcode = str(cust.get("code") or cust.get("hcode") or key.get("hcode") or "")'), 2)


class BranchAndShip(unittest.TestCase):
    def test_branch_label_matches_print_rule(self) -> None:
        src = _fe("lib/customer-branch-label.ts")
        self.assertIn("export function customerWithBranch(", src)
        self.assertIn('return base ? `${base}-${branch}` : branch;', src)
        self.assertIn("if (!branch || base.endsWith(branch)) return base;", src)

    def test_status_list_and_dialog_use_branch_label(self) -> None:
        screen = _fe("components/transactions/transaction-status-screen.tsx")
        self.assertIn("customerWithBranch(r.customer_name || r.gcode || \"\", r.order_key?.gjisa)", screen)
        self.assertEqual(screen.count('format: (_v, r) => partyName(r) || "—",'), 3)
        dialog = _fe("components/outbound/order-detail-dialog.tsx")
        self.assertIn("customerWithBranch(\n                      detail.customer.gname || detail.customer.gcode,", dialog)

    def test_ship_column(self) -> None:
        dialog = _fe("components/outbound/order-detail-dialog.tsx")
        self.assertIn("shipStatus={allowDispatch}", dialog)
        self.assertIn("yesno: l.yesno,", dialog)
        grid = _fe("components/outbound/order-line-grid.tsx")
        self.assertIn('label: shipStatus ? "배송" : "상태"', grid)
        self.assertIn('shipStatus && !axis.columnOrder.includes("yesno") ? [...axis.columnOrder, "yesno"]', grid)
        labels = _fe("lib/column-labels.ts")
        body = labels.split("export function formatShipYesno", 1)[1].split("\n}\n", 1)[0]
        for code, text in (('"1"', '"완료"'), ('"0"', '"접수"'), ('"2"', '"취소"')):
            self.assertRegex(body, rf"case {code}:\s*return {text};")


if __name__ == "__main__":
    unittest.main()
