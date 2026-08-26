"""DEC-219 — 거래 현황 공용 화면의 모든 표가 DataGrid + 컬럼 설정 (2026-08-27 사용자 지적).

"입고현황 양쪽 목록표 필드 정렬, 이동, 보이기옵션 처리 등이 누락된 부분이 존재한다."
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "transactions" / "transaction-status-screen.tsx"


class StatusScreenGrids(TestCase):
    def setUp(self) -> None:
        self.src = SRC.read_text(encoding="utf-8")

    def test_no_manual_tables_left(self) -> None:
        self.assertNotIn("<table", self.src, "현황 화면의 표는 전부 DataGrid")
        self.assertNotIn("HScrollBox", self.src)

    def test_detail_lines_and_rollup_are_data_grids(self) -> None:
        for lid, prefs in (("Sobo24.DBGrid102", "transactions.outbound-status.detail-lines"),
                           ("Sobo24.DBGrid202", "transactions.outbound-status.rollup")):
            i = self.src.index(f'legacyId="{lid}"')
            block = self.src[self.src.rindex("<DataGrid<", 0, i): self.src.index("/>", i)]
            for tok in ("sort=", "onSortChange=", "columnWidths=", "onColumnResize=", "onColumnReorder=", "enableKeyboardNav"):
                self.assertIn(tok, block, f"{lid}: {tok}")
            self.assertIn(f'"{prefs}"', self.src)
        self.assertIn("totals={detailLineRows.length > 0 ? detailLineTotals : undefined}", self.src, "DEC-161 합계 행 유지")
        self.assertIn('label: "ISBN"', self.src, "DEC-169 ISBN 컬럼 유지")

    def test_column_settings_for_every_axis(self) -> None:
        """좌측 전표 표의 컬럼 설정이 isOutbound 블록 밖에 있어야 입고·신간 현황에서도 보인다."""
        i = self.src.index("hidden={detailPrefs.hidden}")
        before = self.src[self.src.rindex("{isOutbound && (", 0, i): i]
        # isOutbound 블록은 컬럼 설정 앞에서 닫혀 있어야 한다
        self.assertIn("                )}\n                {/* 컬럼 표시/폭/순서 설정 — 모든 축", before)
        self.assertEqual(self.src.count("hidden={detailLinePrefs.hidden}"), 1)
        self.assertEqual(self.src.count("hidden={rollupPrefs.hidden}"), 1)


if __name__ == "__main__":
    main()
