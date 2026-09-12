"""거래처별판매(Sobo62) — 상단 거래처 행 **재선택은 선택 유지** (교문사 리포트 2026-09-12).

종전 `selectCustomerRow` 는 같은 행을 다시 클릭하면 선택을 풀고 하단 「도서별 상세」를
«전체 거래처» 로 되돌렸다(DataGrid 가 클릭 1회에 onSelectedRowChange·onRowClick 을 모두
호출하고, ↑↓ 로 고른 행에서 Enter 도 onRowClick 이라 같은 증상). 요구: 같은 행 재클릭은
하단을 바꾸지 않는다 — 다른 행 선택만 전환, 전체 복귀는 「조회」 재실행(load 가 초기화).

정적 가드: 페이지 소스의 selectCustomerRow 본문에 해제(setSelectedKey(null)/
loadDetail(undefined)) 분기가 없고, 같은 키는 조기 반환해야 한다. 「조회」의 전체 복귀
경로(load 내 선택 초기화)는 그대로 남아 있어야 한다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "reports" / "customer-sales" / "page.tsx"


def _fn_body(src: str, name: str) -> str:
    m = re.search(rf"function {name}\([^)]*\)\s*\{{", src)
    assert m, f"{name} 정의를 찾지 못함"
    depth, i = 0, m.end() - 1
    while i < len(src):
        ch = src[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return src[m.end() : i]
        i += 1
    raise AssertionError(f"{name} 본문 끝을 찾지 못함")


class CustomerSalesReselectKeepsDetail(TestCase):
    def setUp(self) -> None:
        self.src = PAGE.read_text("utf-8")

    def test_same_row_reselect_is_noop(self) -> None:
        body = _fn_body(self.src, "selectCustomerRow")
        self.assertIn("if (key === selectedKey) return;", body, "같은 키는 조기 반환(선택 유지)")
        self.assertNotIn("setSelectedKey(null)", body, "재선택으로 선택을 풀면 안 됨")
        self.assertNotIn("setSelectedRow(null)", body)
        self.assertNotIn("loadDetail(undefined", body, "재선택이 전체 거래처 상세로 되돌리면 안 됨")

    def test_query_still_resets_to_all_customers(self) -> None:
        # 「조회」 재실행 = 전체 거래처 복귀 경로(DEC-197) — 재선택 무시 도입 후에도 유지.
        body = _fn_body(self.src, "load")
        self.assertIn("setSelectedKey(null)", body)
        self.assertIn("loadDetail(undefined", body)


if __name__ == "__main__":
    main()
