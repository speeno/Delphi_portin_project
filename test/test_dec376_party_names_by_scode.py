"""DEC-376 — 전표 상대처명은 Scode 가 가리키는 마스터에서 찾는다 (X 거래처 · Y 입고처 · Z 기타거래처).

보고(교문사, 2026-10-05 캡처)
----------------------------
"2. 도서별판매 : 입고처명 다시 확인 요청 — 입고처 '뉴코아문고'가 없습니다. 그런데 자료에는 뉴코아로 반영되어있습니다."
(도서 84500 의 입고 512부 행이 「[X]#뉴코아문고*」로 표시 — 그 코드의 **거래처명**.)

근본 원인
---------
같은 코드가 거래처(G1_Ggeo) · 입고처(G2_Ggwo) · 기타거래처(G5_Ggeo)에 따로 있다. 도서별판매 하단(거래처별 내역 ·
내용 전체 보기)이 ① 행을 Gcode 만으로 묶고 ② 이름을 G1_Ggeo 에서만 찾았다. 2026-08-22 입고현황에서 고친 것과 같은 실수.

재발 방지
---------
- 공용 리졸버 ``party_names.fetch_party_names`` 하나로 통일(Scode → 마스터).
- 여러 Scode 가 섞이는 목록은 행 키에 Scode 를 넣는다.
- **G1_Ggeo 이름 직접 조회는 허용 목록의 함수에서만** — 새 화면이 같은 실수를 하면 이 테스트가 막는다.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import party_names as pn
from app.services import reports_service as rs

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "도서물류관리프로그램" / "backend" / "app" / "services"


class Resolver(IsolatedAsyncioTestCase):
    async def test_each_scode_uses_its_own_master(self) -> None:
        g1 = AsyncMock(return_value={("5019", "00100"): "뉴코아문고"})
        g5 = AsyncMock(return_value={("", "00100"): "기타처"})
        vendor = AsyncMock(return_value={"00100": "교과서인쇄소"})
        with patch.object(pn, "fetch_g1_customer_gnames", g1), \
             patch.object(pn, "fetch_g5_etc_gnames", g5), \
             patch("app.services.inbound_service._fetch_vendor_names", vendor):
            names = await pn.fetch_party_names(
                "remote_153",
                [("X", "5019", "00100"), ("Y", "5019", "00100"), ("Z", "5019", "00100"), ("y", "5019", "00100"), ("Q", "5019", "00100")],
            )
        self.assertEqual(names[("X", "5019", "00100")], "뉴코아문고")
        self.assertEqual(names[("Y", "5019", "00100")], "교과서인쇄소")  # 입고처 — 거래처명이 아니다
        self.assertEqual(names[("Z", "5019", "00100")], "기타처")
        self.assertEqual(names[("Q", "5019", "00100")], "")  # 모르는 Scode 는 이름을 지어내지 않는다
        vendor.assert_awaited_once()
        self.assertEqual(vendor.await_args.kwargs.get("scope_hcode"), "5019")


class BookSalesDetailKeepsPartiesApart(IsolatedAsyncioTestCase):
    ROWS = [
        # 같은 코드 00100 — 입고처(Y) 입고 512, 거래처(X) 출고 5
        {"Bcode": "84500", "Gcode": "00100", "Scode": "Y", "Gubun": "입고", "Pubun": "정품", "Gsqut": 512, "Gssum": 0},
        {"Bcode": "84500", "Gcode": "00100", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "Gsqut": 5, "Gssum": 5000},
        {"Bcode": "84500", "Gcode": "00200", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "Gsqut": 400, "Gssum": 400000},
    ]
    NAMES = {
        ("Y", "5019", "00100"): "교과서인쇄소",
        ("X", "5019", "00100"): "[X]#뉴코아문고*",
        ("X", "5019", "00200"): "$교과서판매(택배)",
    }

    async def _names(self, server_id: str, keys: Any) -> dict[tuple[str, str, str], str]:
        return {(pn.norm_scode(s), str(h or ""), str(g or "")): self.NAMES.get((pn.norm_scode(s), str(h or ""), str(g or "")), "") for s, h, g in keys}

    async def test_day_detail(self) -> None:
        with patch.object(rs, "execute_query", AsyncMock(return_value=list(self.ROWS))), \
             patch.object(rs, "fetch_party_names", AsyncMock(side_effect=self._names)), \
             patch.object(rs, "fetch_book_meta", AsyncMock(return_value={})):
            res = await rs.get_book_sales_day_detail(
                server_id="remote_153", hcode="5019", bcode="84500",
                date_from="2026-01-01", date_to="2026-10-02",
            )
        rows = {(r["scode"], r["gcode"]): r for r in res["rows"]}
        self.assertEqual(len(rows), 3)  # 같은 코드라도 입고처 · 거래처는 따로
        self.assertEqual(rows[("Y", "00100")]["gname"], "교과서인쇄소")
        self.assertEqual((rows[("Y", "00100")]["giqut"], rows[("Y", "00100")]["goqut"]), (512, 0))
        self.assertEqual(rows[("X", "00100")]["gname"], "[X]#뉴코아문고*")
        self.assertEqual((rows[("X", "00100")]["giqut"], rows[("X", "00100")]["goqut"]), (0, 5))

    async def test_customers_all(self) -> None:
        with patch.object(rs, "execute_query", AsyncMock(return_value=list(self.ROWS))), \
             patch.object(rs, "fetch_party_names", AsyncMock(side_effect=self._names)), \
             patch.object(rs, "fetch_book_meta", AsyncMock(return_value={})):
            res = await rs.get_book_sales_customers_all(
                server_id="remote_153", hcode="5019", date_from="2026-01-01", date_to="2026-10-02",
                bcodes=[], all_books=True,
            )
        rows = {(r["scode"], r["gcode"]): r for r in res["rows"]}
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[("Y", "00100")]["gname"], "교과서인쇄소")
        self.assertEqual(res["totals"]["giqut"], 512)
        self.assertEqual(res["totals"]["goqut"], 405)


# G1_Ggeo(거래처 마스터)에서 **이름(Gname)** 을 직접 읽는 서비스 파일 — 사유가 확인된 것만.
# 여기에 없는 파일이 G1_Ggeo 이름을 직접 조회하면 실패한다 → ``party_names.fetch_party_names`` 를 쓰거나,
# Scode='X'(거래처) 전용 화면임을 확인하고 사유와 함께 추가한다.
G1_NAME_LOOKUP_ALLOWLIST: dict[str, str] = {
    "g1_geo_lookup.py": "거래처 마스터 조회 헬퍼 본체",
    "party_names.py": "공용 리졸버의 거래처(X) 분기",
    "reports_service.py": "거래처별판매 — 한 번에 한 Scode(_PARTY_MASTER_BY_SCODE), 도서 축 상세는 fetch_party_names",
    "outbound_service.py": "출고 전표 — Scode='X' 고정",
    "transactions_service.py": "거래명세서 Scode='X' 고정 · 현황 3뷰는 _party_name_resolver(축별 마스터)",
    "verification_service.py": "출고 검증 — Gubun='출고' · Scode='X'",
    "production_service.py": "제작(S2_Ssub) — Scode 없음, 레거시 Subu26/27 이 G1 조회",
    "returns_service.py": "반품 전표 헤더(X). 원장 · 기간 상세의 JOIN 결과는 apply_party_names 로 Scode 별 보정",
    "customer_txn_ledger_service.py": "거래처거래원장 — S1/Sg_Gsum Scode='X' (H1 수금 Scode 무필터는 DEC-376 남은 것)",
    "customer_ledger_service.py": "통합 거래처원장 — DEC-376 남은 것(Scode 무필터 합산, 레거시 확인 후 수정)",
    "courier_service.py": "택배 — S.Scode='X' INNER JOIN",
    "sales_matrix_service.py": "년/월 매트릭스 — partner X→G1 / Y→G2 축 일치",
    "settlement_service.py": "정산 — 시내/지방 구분용(이름 미사용)",
    "adjustment_ledger_service.py": "원장변경 — Sg_Gsum Scode='X'",
    "masters_service.py": "거래처 마스터 CRUD",
    "masters_excel.py": "거래처 마스터 엑셀",
    "g1_ggeo_adapt.py": "거래처 마스터 컬럼 어댑터",
    "pricing_service.py": "공급율 조회(거래처 X / 입고처 Y 를 테이블로 구분)",
    "sales_statement_create_service.py": "거래명세서 입력 — 거래처(X) 공급율",
    "h2_branch_lookup.py": "거래처 지점 — 거래처 마스터 속성",
    "inventory_service.py": "재고 — 거래처명 미조회(주석 · 문서 언급)",
    "customer_code_prefix_service.py": "거래처 코드 채번",
    "cash_slip_service.py": "입출금전표 — Scode 로 마스터를 고른다",
    "e_invoice_service.py": "전자계산서(DEC-395) — 매출은 거래처별판매 Scode='X' 고정, 계산서 정보는 거래처 마스터 속성",
}


class NoNewDirectCustomerNameLookups(TestCase):
    def test_direct_g1_name_lookups_are_allowlisted(self) -> None:
        offenders: list[str] = []
        for path in sorted(SERVICES.glob("*.py")):
            src = path.read_text(encoding="utf-8")
            hit = False
            # SQL 문맥(FROM/JOIN G1_Ggeo)만 본다 — 주석의 단순 언급은 제외.
            for m in re.finditer(r"(?:FROM|JOIN)\s+G1_Ggeo", src):
                window = src[max(0, m.start() - 300) : m.end() + 300]
                if re.search(r"gname", window, re.I):
                    hit = True
                    break
            if "fetch_g1_customer_gnames(" in src:
                hit = True
            if hit and path.name not in G1_NAME_LOOKUP_ALLOWLIST:
                offenders.append(path.name)
        self.assertEqual(
            offenders, [],
            "G1_Ggeo(거래처) 이름을 직접 조회하는 서비스가 새로 생겼다 — 여러 Scode 가 섞이면 입고처 · 기타거래처 행에 "
            "거래처명이 뜬다. party_names.fetch_party_names 를 쓰거나, 거래처(Scode='X') 전용임을 확인하고 허용 목록에 사유와 함께 추가.",
        )

    def test_mixed_scode_screens_use_shared_resolver(self) -> None:
        reports = (SERVICES / "reports_service.py").read_text(encoding="utf-8")
        self.assertEqual(reports.count("await _attach_party_names(server_id, norm_hcode, out,"), 2)
        self.assertIn("by_cust[(sc, gc)]", reports)
        self.assertIn("by_pair[(bc, sc, gc)]", reports)
        self.assertIn('_PARTY_MASTER_BY_SCODE = {"X": "G1_Ggeo", "Y": "G2_Ggwo", "Z": "G5_Ggeo"}', reports)
        book_ledger = (SERVICES / "book_ledger_service.py").read_text(encoding="utf-8")
        self.assertEqual(book_ledger.count("await fetch_party_names("), 2)
        self.assertNotIn("FROM G1_Ggeo", book_ledger)
        returns = (SERVICES / "returns_service.py").read_text(encoding="utf-8")
        self.assertEqual(returns.count("await _apply_party_names_soft(server_id, detail_items)"), 2)
        inbound = (SERVICES / "inbound_service.py").read_text(encoding="utf-8")
        self.assertNotIn("SQL_VENDOR_BY_GCODE", inbound)


class ApplyNames(IsolatedAsyncioTestCase):
    async def test_non_customer_rows_never_keep_customer_name(self) -> None:
        rows = [
            {"scode": "Y", "hcode": "5019", "gcode": "00100", "gname": "[X]#뉴코아문고*"},  # JOIN 이 붙인 거래처명
            {"scode": "X", "hcode": "5019", "gcode": "00100", "gname": "[X]#뉴코아문고*"},
            {"scode": "Z", "hcode": "5019", "gcode": "05210", "gname": ""},
        ]

        async def fake(server_id: str, keys: Any) -> dict[tuple[str, str, str], str]:
            return {("Y", "5019", "00100"): "", ("X", "5019", "00100"): "", ("Z", "5019", "05210"): "애플2"}

        with patch.object(pn, "fetch_party_names", AsyncMock(side_effect=fake)):
            await pn.apply_party_names("remote_153", rows)
        self.assertEqual(rows[0]["gname"], "")  # 입고처 마스터에 없으면 비운다 — 거래처명을 남기지 않는다
        self.assertEqual(rows[1]["gname"], "[X]#뉴코아문고*")  # 거래처 행은 기존 이름 유지
        self.assertEqual(rows[2]["gname"], "애플2")


if __name__ == "__main__":
    main()
