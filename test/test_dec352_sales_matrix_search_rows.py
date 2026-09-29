"""DEC-352 — 년/월 세분화 판매 6화면 검색 부분 레이아웃 (2026-09-30 사용자 「13번 화면은 검색 부분 레이아웃 수정이 필요」).

거래처판매(월별) 캡처에서 ① 거래년월 칸의 달력 아이콘이 알약 밖으로 나오고 ② 「검색」 버튼만 다음 줄에 혼자 떨어져 있었다.
공용 이름 알약(`LedgerNamePill`, 최소 14~18rem · 최대 22rem)이 이 화면(조건 7~9개)에는 너무 넓고, 넓은 칸은 최대 폭에 걸렸다.

- 알약은 내용 폭(화면 전용 PILL_* 클래스, 칸마다 명시 폭).
- 1줄 = 기간 | 출력조건 · 보기 / 2줄 = (구분) · 코드 범위 · 교차 필터 · 본사출고제외 · 검색.
- 「검색」은 Enter 순서의 마지막 칸이므로 마지막 줄 끝 — 화면 순서 = Enter 순서.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

SRC = (
    Path(__file__).resolve().parents[1]
    / "도서물류관리프로그램" / "frontend" / "src" / "components" / "stats" / "sales-matrix-screen.tsx"
)
LINE = re.compile(r'<LedgerSearchLine wrap align="start">(?P<body>[\s\S]*?)</LedgerSearchLine>')
ID = re.compile(r"L\((?:\"([^\"]+)\"|`([^`]+)`)\)")


class SearchRows(TestCase):
    def setUp(self) -> None:
        self.src = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.rows = [m.group("body") for m in LINE.finditer(self.src.split("<PageHeader")[1])]

    def _ids(self, body: str) -> list[str]:
        return [a or b for a, b in ID.findall(body)]

    def test_two_rows(self) -> None:
        self.assertEqual(len(self.rows), 2)

    def test_row1_is_period_and_view_options(self) -> None:
        ids = self._ids(self.rows[0])
        for wid in ("Edit_Hcode", "Edit101", "Edit102", "ComboBox2", "ComboBox1"):
            self.assertIn(wid, ids, wid)
        for wid in ("Panel102", "Edit105", "Edit107", "Edit109", "CheckBox2", "dxButton1"):
            self.assertNotIn(wid, ids, f"{wid} 는 2줄")

    def test_row2_ends_with_search_button(self) -> None:
        ids = self._ids(self.rows[1])
        self.assertEqual(ids, ["Panel102", "Edit105", "Edit107", "Edit109", "CheckBox2", "dxButton1"])
        self.assertTrue(self.rows[1].rstrip().endswith("disabled={loading} />"), "「검색」이 마지막 요소")

    def test_screen_order_equals_enter_order(self) -> None:
        stops = self.src.split("const stopIds = [")[1].split("];")[0]
        stop_ids = [a or b for a, b in ID.findall(stops)]
        screen_ids = [i for i in self._ids(self.rows[0]) + self._ids(self.rows[1]) if "${" not in i]
        # 기간 칸(periodStops)은 기간 방식마다 달라 스톱 목록에 전개식으로 들어간다 — 나머지 순서만 비교.
        fixed = [i for i in screen_ids if i not in ("Edit101", "Edit102")]
        self.assertEqual(fixed, stop_ids)

    def test_pills_are_content_sized(self) -> None:
        header = self.src.split("<PageHeader")[1].split("</PageHeader>")[0]
        self.assertNotIn("<LedgerNamePill", header, "공용 이름 알약(최소/최대 폭)은 이 화면에 쓰지 않는다")
        self.assertNotIn("SEARCH_PILL_INPUT_CLASS", self.src, "w-full 입력 클래스는 명시 폭과 충돌한다")
        pill = self.src.split("const PILL_CLASS =")[1].split(";")[0]
        self.assertNotRegex(pill, r"min-w-|max-w-|flex-1")
        for cls in ("PILL_INPUT_CLASS", "PILL_SELECT_CLASS"):
            body = self.src.split(f"const {cls} =")[1].split(";")[0]
            self.assertNotRegex(body, r"\bw-full\b|flex-1", cls)

    def test_every_control_has_an_explicit_width(self) -> None:
        header = self.src.split("<PageHeader")[1].split("</PageHeader>")[0]
        uses = re.findall(r"\$\{PILL_(?:INPUT|SELECT)_CLASS\}([^`]*)`", header)
        self.assertGreaterEqual(len(uses), 9)
        for extra in uses:
            self.assertRegex(extra, r"\bw-\d+\b", f"폭 미지정: {extra!r}")

    def test_month_inputs_fit_inside_the_pill(self) -> None:
        months = re.findall(r'<input type="month" className=\{`([^`]+)`\}', self.src)
        self.assertEqual(len(months), 2)
        for cls in months:
            self.assertIn("w-36", cls)
            self.assertNotIn("w-full", cls)


if __name__ == "__main__":
    main()
