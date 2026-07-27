"""DateFieldYMD 수기 입력 한자리 인식 버그 회귀 가드 (2026-07-27).

증상: 통계관리 도서별판매/거래처별판매 등 기본값이 채워진 날짜 필터에서
`2026. 06. 30` 수기 입력 시 `2026-01-03` 류로 저장 — 월/일 첫 자리만 인식.

원인(도서물류관리프로그램/frontend/src/components/shared/date-field-ymd.tsx):
1. emit() 이 세그먼트 1자리 시점부터 부분 입력을 정규화("0"→"01")해 부모로 올리고,
2. 부모 value 에코를 동기화 useEffect 가 그대로 세그먼트에 되써서("0"→"01"),
3. 다음 키가 onlyDigits(slice(0,2)) 에서 잘려("016"→"01") 두 번째 자리가 소실.

수정 불변식(이 테스트가 지키는 것):
- (A) 동기화 effect 는 자기 emit 의 에코를 스킵 — `composeEmitted(segsRef.current) === value`.
- (B) 세그먼트 미러(segsRef) effect 가 동기화 effect 보다 먼저 선언(같은 커밋에서 먼저 실행).
- (C) blur 정규화는 state 클로저가 아니라 blur 이벤트 대상 DOM 값(`e.currentTarget.value`)을
  읽는다 — 월 2자리 완성 자동이동(월→일 focus)이 onChange 와 같은 이벤트에서 blur 를
  동기 발생시키므로 클로저는 한 키 이전 값("0")일 수 있다.

+ composeEmitted / emit 클램프 규칙 파이썬 미러 (TS 로직 동기 유지).
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


def compose_emitted(y: str, mo: str, d: str, month_only: bool = False):
    """Mirror of ``composeEmitted`` — 부분 입력 포함 emit 정규형. 미완성이면 None."""
    if len(y) != 4 or len(mo) < 1:
        return None
    mm = min(12, max(1, int(mo) if mo.isdigit() and int(mo) else 1))
    if month_only:
        return f"{y}-{mm:02d}"
    if len(d) < 1:
        return None
    dd = min(31, max(1, int(d) if d.isdigit() and int(d) else 1))
    return f"{y}-{mm:02d}-{dd:02d}"


class TestDateFieldYmdSource(TestCase):
    """정적 소스 가드 — 에코 스킵/미러 선언 순서/blur DOM 값 사용."""

    @classmethod
    def setUpClass(cls):
        cls.src = COMPONENT.read_text(encoding="utf-8")

    def test_component_exists(self):
        self.assertTrue(COMPONENT.exists(), COMPONENT)

    def test_sync_effect_skips_own_emit_echo(self):
        # (A) 에코 스킵 가드가 동기화 effect 의 parseYmd 재주입보다 앞에 있어야 한다.
        self.assertIn("composeEmitted(segsRef.current) === value", self.src)
        skip_pos = self.src.index("composeEmitted(segsRef.current) === value")
        # 스킵 이후에 나오는 parseYmd(value, ...) 재주입이 존재(동기화 자체는 유지)
        self.assertIn("parseYmd(value, monthOnly)", self.src[skip_pos:])

    def test_segs_mirror_declared_before_sync_effect(self):
        # (B) segsRef 미러 effect 가 value 동기화 effect 보다 먼저 선언 — effect 실행 순서 보장.
        mirror = self.src.index("segsRef.current = { y, mo, d }")
        sync = self.src.index("composeEmitted(segsRef.current) === value")
        self.assertLess(mirror, sync)

    def test_blur_normalize_reads_dom_value_not_state_closure(self):
        # (C) onBlur 는 e.currentTarget.value 를 normalizeSeg 로 전달해야 한다.
        self.assertRegex(
            self.src, re.compile(r'normalizeSeg\(\s*"mo",\s*e\.currentTarget\.value\s*\)')
        )
        self.assertRegex(
            self.src, re.compile(r'normalizeSeg\(\s*"d",\s*e\.currentTarget\.value\s*\)')
        )
        # 인자 없이 state 클로저만 읽는 구버전 시그니처 금지.
        self.assertNotRegex(self.src, re.compile(r'normalizeSeg\(\s*"(?:mo|d)"\s*\)'))


class TestComposeEmittedMirror(TestCase):
    """composeEmitted 파이썬 미러 — 부분 입력 정규화 규칙 동결."""

    def test_partial_month_zero_clamps_to_january(self):
        # "0" 입력 순간의 emit 정규형 — 에코 판별의 근거값.
        self.assertEqual(compose_emitted("2026", "0", "26"), "2026-01-26")

    def test_full_input_passthrough(self):
        self.assertEqual(compose_emitted("2026", "06", "30"), "2026-06-30")
        self.assertEqual(compose_emitted("2026", "12", "31"), "2026-12-31")

    def test_partial_day_single_digit(self):
        self.assertEqual(compose_emitted("2026", "06", "3"), "2026-06-03")

    def test_clamps(self):
        self.assertEqual(compose_emitted("2026", "13", "32"), "2026-12-31")
        self.assertEqual(compose_emitted("2026", "00", "00"), "2026-01-01")

    def test_incomplete_returns_none(self):
        self.assertIsNone(compose_emitted("202", "06", "30"))
        self.assertIsNone(compose_emitted("2026", "", "30"))
        self.assertIsNone(compose_emitted("2026", "06", ""))

    def test_month_only(self):
        self.assertEqual(compose_emitted("2026", "6", "", month_only=True), "2026-06")
        self.assertIsNone(compose_emitted("2026", "", "", month_only=True))
