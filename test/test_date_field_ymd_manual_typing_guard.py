"""DateFieldYMD 수기 입력 회귀 가드 (2026-07-27 최초 / 2026-09-17 단일 입력 재작성).

원래 증상(2026-07-27)
--------------------
통계관리 도서별판매/거래처별판매 등 기본값이 채워진 날짜 필터에서 `2026. 06. 30` 수기
입력 시 `2026-01-03` 류로 저장 — 월/일 첫 자리만 인식. 원인은 3분할(년/월/일) 구현이
**부분 입력**을 정규화해 부모로 올리고("0"→"01"), 그 에코를 동기화 effect 가 세그먼트에
되써서 다음 키가 잘린 것이었다.

현재 구현(2026-09 UI 통일)
-------------------------
컴포넌트가 «한 칸짜리 날짜 입력 + 달력»으로 재작성됐다. 같은 버그를 **구조적으로**
막는 방식이 달라졌으므로, 문자열 검사도 새 불변식으로 갱신한다(요구사항은 동일 —
수기로 연속 입력한 숫자가 중간에 잘리거나 되돌아가면 안 된다).

불변식
------
- (A) 부분 입력은 부모로 올리지 않는다 — ``normalizeComplete`` 는 자리수가 다 차야 값을
      돌려주고, ``handleChange`` 는 그때(또는 빈 값일 때)만 ``onChange`` 를 호출한다.
      → 부분 입력 에코 자체가 발생하지 않는다.
- (B) 부모 값 동기화 effect 는 ``value``/``monthOnly`` 가 바뀔 때만 표시를 덮어쓴다.
      (입력 중 매 키마다 되쓰면 옛 버그가 되살아난다.)
- (C) blur/Enter 커밋은 state 클로저가 아니라 **현재 표시 문자열**을 정규화한다
      (``commit(raw = display)``) — 커밋 시점의 마지막 키까지 반영.
- (D) 완성 시 정규화 규칙(월 1~12, 일 1~말일, 윤년 포함) 파이썬 미러로 동결.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = (
    ROOT
    / "도서물류관리프로그램"
    / "frontend"
    / "src"
    / "components"
    / "shared"
    / "date-field-ymd.tsx"
)


def _max_day(year: int, month: int) -> int:
    if month == 2:
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        return 29 if leap else 28
    return 30 if month in (4, 6, 9, 11) else 31


def normalize_complete(raw: str, month_only: bool = False):
    """Mirror of ``normalizeComplete`` — 자리수가 다 찼을 때만 (표시, 값)."""
    digits = re.sub(r"\D", "", raw)[: 6 if month_only else 8]
    if len(digits) != (6 if month_only else 8):
        return None
    year_text = digits[:4]
    year = int(year_text)
    month = min(12, max(1, int(digits[4:6]) or 1))
    month_text = f"{month:02d}"
    if month_only:
        return f"{year_text}.{month_text}", f"{year_text}-{month_text}"
    day = min(_max_day(year, month), max(1, int(digits[6:8]) or 1))
    return f"{year_text}.{month_text}.{day:02d}", f"{year_text}-{month_text}-{day:02d}"


class TestDateFieldYmdSource(TestCase):
    """정적 소스 가드 — 부분 입력 무-emit / 동기화 deps / 커밋 시 표시값 사용."""

    @classmethod
    def setUpClass(cls):
        cls.src = COMPONENT.read_text(encoding="utf-8")

    def test_component_exists(self):
        self.assertTrue(COMPONENT.exists(), COMPONENT)

    def test_partial_input_is_not_emitted(self):
        # (A) 완성 전에는 onChange 없음 — normalizeComplete 가 null 이면 표시만 갱신.
        self.assertIn("if (digits.length !== (monthOnly ? 6 : 8)) return null;", self.src)
        block = self.src[self.src.index("function handleChange("): self.src.index("function handleBlur(")]
        self.assertIn("const normalized = normalizeComplete(digits, monthOnly);", block)
        self.assertIn("if (normalized) {", block)
        # 빈 입력(전체 지움)만 예외적으로 빈 값 emit.
        self.assertIn('onChange("");', block)
        # 부분 입력을 그대로 올리는 코드가 없어야 한다.
        self.assertNotIn("onChange(digits)", block)
        self.assertNotIn("onChange(nextDisplay)", block)

    def test_sync_effect_depends_on_value_only(self):
        # (B) 표시 동기화는 value/monthOnly 변경에만 반응.
        self.assertRegex(
            self.src,
            re.compile(
                r"useEffect\(\(\) => \{\s*setDisplay\(displayFromValue\(value, monthOnly\)\);\s*\}, \[value, monthOnly\]\);"
            ),
        )

    def test_commit_reads_current_display_not_stale_state(self):
        # (C) 커밋은 인자 기본값이 현재 표시 문자열 — blur/Enter 모두 같은 경로.
        self.assertIn("function commit(raw = display): boolean {", self.src)
        self.assertIn("const normalized = normalizeComplete(raw, monthOnly);", self.src)
        self.assertIn("onBlur={handleBlur}", self.src)
        self.assertIn("if (commit()) return;", self.src)

    def test_single_input_with_calendar(self):
        """한 칸 입력 + 달력 버튼(레거시 3분할에서 전환) — 숫자만 연속 입력 가능."""
        self.assertIn('inputMode="numeric"', self.src)
        self.assertIn('placeholder={monthOnly ? "YYYY.MM" : "YYYY.MM.DD"}', self.src)
        self.assertIn('aria-label="달력 열기"', self.src)
        self.assertIn("data-date-field", self.src)


class TestNormalizeCompleteMirror(TestCase):
    """(D) 완성 시 정규화 규칙 동결 — 파이썬 미러."""

    def test_full_input_passthrough(self):
        self.assertEqual(normalize_complete("2026.06.30")[1], "2026-06-30")
        self.assertEqual(normalize_complete("20261231")[1], "2026-12-31")

    def test_partial_returns_none(self):
        self.assertIsNone(normalize_complete("2026.06.3"))
        self.assertIsNone(normalize_complete("2026"))
        self.assertIsNone(normalize_complete(""))

    def test_clamps_month_and_day(self):
        self.assertEqual(normalize_complete("20261332")[1], "2026-12-31")
        self.assertEqual(normalize_complete("20260000")[1], "2026-01-01")

    def test_clamps_day_to_month_end(self):
        self.assertEqual(normalize_complete("20260231")[1], "2026-02-28")
        self.assertEqual(normalize_complete("20240231")[1], "2024-02-29")  # 윤년
        self.assertEqual(normalize_complete("20260431")[1], "2026-04-30")

    def test_month_only(self):
        self.assertEqual(normalize_complete("2026.06", month_only=True)[1], "2026-06")
        self.assertIsNone(normalize_complete("20260", month_only=True))

    def test_display_form(self):
        self.assertEqual(normalize_complete("20260630")[0], "2026.06.30")
        self.assertEqual(normalize_complete("202606", month_only=True)[0], "2026.06")
