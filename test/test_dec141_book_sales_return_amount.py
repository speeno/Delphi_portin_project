"""DEC-141 — 도서별판매 반품액(GBSUM)·매출부수/매출액·컬럼 순서 회귀 가드.

2026-08-11 영업팀 주석(라이브 새 화면 위): ① 증정수를 폐기수 앞으로,
② 출고액 뒤 반품액 추가, ③ 매출부수(출고수+반품수), ④ 매출액(출고액+반품액).
반품액 정본 = 레거시 Subu61 L402~404 (Gbqut += T01 **and Gbsum += T02**) —
종전 분기표는 반품 수량만 누적하고 금액 버킷이 없었다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import reports_service as rpt  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class ReturnAmountBranchTests(TestCase):
    def _cell(self) -> dict:
        return {"giqut": 0, "gisum": 0, "gbqut": 0, "gbsum": 0, "gpqut": 0,
                "gjqut": 0, "goqut": 0, "gosum": 0, "gpsum": 0}

    def test_return_accumulates_amount(self) -> None:
        cell = self._cell()
        # 반품은 음수 저장 관례 — 수량/금액 모두 그대로 가산(레거시 동일 연산).
        rpt._apply_book_sales_branch(
            cell, scode="X", gubun="반품", pubun="", gsqut=-2, gssum=-65450,
        )
        self.assertEqual(cell["gbqut"], -2)
        self.assertEqual(cell["gbsum"], -65450, "반품액(GBSUM) 누적 — DEC-141")

    def test_measure_keys_include_gbsum(self) -> None:
        self.assertIn("gbsum", rpt._BOOK_SALES_MEASURE_KEYS,
                      "반품액만 있는 행이 0행 제외 규칙에 걸리면 안 된다")


class FrontendColumnGuards(TestCase):
    def test_column_order_and_new_columns(self) -> None:
        src = (FRONT / "app" / "(app)" / "reports" / "book-sales" / "page.tsx").read_text(
            encoding="utf-8"
        )
        cols = src.split("BOOK_SALES_COLUMNS")[1]
        # ① 증정수가 폐기수 앞 (입고→출고→반품→증정→폐기).
        self.assertLess(cols.index('"gbqut"'), cols.index('"gjqut"'))
        self.assertLess(cols.index('"gjqut"'), cols.index('"gpqut"'))
        # ② 반품액이 출고액 뒤.
        self.assertLess(cols.index('label: "출고액"'), cols.index('label: "반품액"'))
        # ③④ 매출부수/매출액 파생 컬럼.
        for label in ("매출부수", "매출액"):
            self.assertIn(label, cols, f"{label} 컬럼 누락 — DEC-141")
        self.assertIn("sellQut: (r.goqut ?? 0) + (r.gbqut ?? 0)", src)
        self.assertIn("sellSum: (r.gosum ?? 0) + (r.gbsum ?? 0)", src)
        # 저장 컬럼순서 리셋 — 확정 순서를 전 계정 기본 적용(v2 키).
        self.assertIn('"reports.book-sales.v2"', src)


if __name__ == "__main__":
    main()
