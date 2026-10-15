"""신규도서 등록 «숫자가 입력이 안 된다» + 금액 콤마 + 인세비율 % — DEC-403 (2026-10-15 교문사 신고).

신고 원문
--------
"신규도서 등록 시, 입력칸에 숫자가 입력이 안되고 여러번 누르면 숫자 두번째 자리입력이 됩니다.
 전체적으로 입력에 오류없이 입력될 수 있게 확인요청드립니다."
추가: "금액은 (콤마,) 기능이 있어야합니다. 그리고 인세비율도 자동 (%) 표기 될 수 있게"

원인
----
DEC-279(2026-09-12)가 전역 바코드 캡처 버퍼(`lib/wedge-buffer.ts`)의 시퀀스 분리를 60ms → 300ms 로
넓히면서, **300ms 이내로 이어진 글자를 모두 삼켰다**(`swallow` → preventDefault). 사람 타이핑은
80~250ms 간격이라 첫 글자만 들어가고 두 번째부터 사라졌다. 한글은 IME 조합 중(`isComposing`)이라
제외돼 «숫자·영문만 안 되는» 것처럼 보였고, 300ms 넘게 쉬고 다시 누르면 새 시퀀스의 첫 글자로
들어가 「여러 번 누르면 두 번째 자리가 입력된다」 가 되었다. 신규 도서 등록(`master/book/new`)만
`captureGlobal` 이라 이 화면에서만 났다.

수정
----
- 글자를 삼키는 조건은 **웨지 연타가 확인된 뒤**(빠른 간격 ≤30ms 가 `minFastGaps=2` 회) 뿐.
  사람 타이핑은 기본값으로는 절대 삼켜지지 않는다. 흘려보낸 글자 수(`leaked`)를 스캔 확정과 함께
  돌려줘 호출자가 그만큼 되돌린다(종전 «첫 글자 1개» 고정 → 일반화, 재포맷 입력칸 대응).
- 자동 반복(키 누르고 있기)·Ctrl/Cmd/Alt 조합은 버퍼에 넣지 않는다.
- 금액(정가·전자책 정가·원가·매입가)은 `AmountField` — 콤마 표시 · 숫자만 · 캐럿 보존
  (순수 로직 `lib/amount-format.ts`). 상태값은 정수 그대로.
- 인세비율은 `%` 접미사(`data-field-suffix`, 표시만) + 숫자·소수점만 받는다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
LIB = FRONTEND / "src" / "lib"
WEDGE_TS = LIB / "wedge-buffer.ts"
AMOUNT_TS = LIB / "amount-format.ts"
HOOK_TS = LIB / "barcode-scanner.ts"
SCANNER_TS = LIB / "scanner.ts"
FORM_TSX = FRONTEND / "src" / "components" / "master" / "book-detail-form.tsx"
BOOK_NEW = FRONTEND / "src" / "app" / "(app)" / "master" / "book" / "new" / "page.tsx"


class WedgeBufferStaticTests(TestCase):
    """§1 정적 — 사람 타이핑 보호 규칙이 코드에 있다."""

    def test_buffer_requires_confirmed_wedge_before_swallowing(self) -> None:
        src = WEDGE_TS.read_text(encoding="utf-8")
        self.assertIn("minFastGaps = 2", src, "웨지 확인 전에는 삼키지 않는다(기본 2회)")
        self.assertIn("fastGaps >= minFastGaps : wedgeish()", src)
        self.assertIn("leaked", src, "흘려보낸 글자 수를 돌려줘야 호출자가 되돌린다")
        self.assertNotIn("return { swallow: true };", src, "«300ms 이내면 무조건 삼킴» 규칙이 되살아났다")

    def test_hook_ignores_repeat_and_shortcuts_and_restores_all_leaked(self) -> None:
        src = HOOK_TS.read_text(encoding="utf-8")
        self.assertIn("ev.repeat || ev.ctrlKey || ev.metaKey || ev.altKey", src)
        self.assertIn("restoreLeakedChars(leak, out.leaked ?? 0)", src)
        self.assertNotIn("el.value.length !== value.length + 1", src, "길이 +1 판별은 콤마 재포맷 입력칸에서 복원을 놓친다")
        s2 = SCANNER_TS.read_text(encoding="utf-8")
        self.assertIn("e.repeat || e.ctrlKey || e.metaKey || e.altKey", s2)

    def test_only_book_new_uses_global_capture(self) -> None:
        """신고 화면 = 전역 캡처 화면. 다른 화면으로 전역 캡처가 번지면 같은 회귀 범위가 넓어진다."""
        self.assertIn("captureGlobal", BOOK_NEW.read_text(encoding="utf-8"))


class BookFormStaticTests(TestCase):
    """§2 정적 — 금액 콤마 · 인세비율 % 접미사."""

    def test_amount_fields_use_comma_field_not_number_input(self) -> None:
        src = FORM_TSX.read_text(encoding="utf-8")
        for label, legacy in (("정가", "Sobo14.Edit109"), ("원가", "Sobo14.Edit130"), ("매입가", "Sobo14.Edit131")):
            self.assertRegex(src, rf'<AmountField label="{label}"[^\n]*legacyId="{legacy}"', f"{label} 은 AmountField")
        self.assertIn('<AmountField\n          label="전자책 정가"', src)
        self.assertNotIn('<NumField label="정가"', src)
        # AmountField 본체 — 콤마 포맷 · 숫자 키패드 · 캐럿 보존 · number 타입 아님
        body = src[src.index("function AmountField(") : src.index("function NumField(")]
        self.assertIn("formatAmount(value)", body)
        self.assertIn('inputMode="numeric"', body)
        self.assertIn('type="text"', body)
        self.assertNotIn('type="number"', body)
        self.assertIn("caretAfterDigits(", body)
        self.assertIn("useLayoutEffect(", body)
        self.assertIn('data-amount-field=""', body)

    def test_royalty_rate_has_percent_suffix_and_numeric_sanitizer(self) -> None:
        src = FORM_TSX.read_text(encoding="utf-8")
        line = next(l for l in src.splitlines() if 'legacyId="Sobo14.Ext.RoyaltyRate"' in l)
        self.assertIn('suffix="%"', line)
        self.assertIn("sanitize={sanitizeRateInput}", line)
        self.assertIn('label="인세비율(%)"', line, "목록 열 이름과 같은 라벨 유지(DEC-366)")
        self.assertIn('{suffix ? <span data-field-suffix="">{suffix}</span> : null}', src)

    def test_amount_module_is_pure(self) -> None:
        src = AMOUNT_TS.read_text(encoding="utf-8")
        self.assertNotIn('from "react"', src)
        self.assertNotIn("use client", src)
        for fn in ("formatAmount", "parseAmountInput", "digitsBeforeCaret", "caretAfterDigits", "sanitizeRateInput"):
            self.assertIn(f"export function {fn}(", src)


HARNESS_JS = r"""
const { createWedgeBuffer } = require("./wedge-buffer.js");
const { formatAmount, parseAmountInput, digitsBeforeCaret, caretAfterDigits, sanitizeRateInput } = require("./amount-format.js");

const results = [];
const check = (name, actual, expected) =>
  results.push({ name, ok: JSON.stringify(actual) === JSON.stringify(expected), actual, expected });

// 키 열을 넣고 삼켜진 글자·마지막 결과를 돌려준다.
function feedKeys(keys, opts) {
  const wedge = createWedgeBuffer(opts);
  let out = { swallow: false };
  const swallowed = [];
  for (const { k, t } of keys) {
    out = wedge.key(k, t);
    if (out.swallow && !out.scan && !out.truncated) swallowed.push(k);
  }
  return { last: out, swallowed: swallowed.join("") };
}
// 글자열을 간격 배열(gaps[i] = i번째와 i+1번째 사이)로 키 열을 만든다. enter=true 면 끝에 Enter.
function seq(text, gaps, enter = false) {
  let t = 1000;
  const keys = [];
  text.split("").forEach((c, i) => {
    keys.push({ k: c, t });
    t += gaps[i] ?? gaps[gaps.length - 1];
  });
  if (enter) keys.push({ k: "Enter", t });
  return keys;
}
const ISBN13 = "9788954601252";

// ── 신고 재현: 사람이 정가 350 을 150ms 간격으로 침 → 종전엔 "5","0" 이 삼켜져 "3" 만 남았다
check("human_150ms_nothing_swallowed", feedKeys(seq("350", [150])).swallowed, "");
check("human_80ms_nothing_swallowed", feedKeys(seq("123456", [80])).swallowed, "");
check("human_250ms_nothing_swallowed", feedKeys(seq("9788", [250])).swallowed, "");
// 사람이 Enter 까지 쳐도 스캔으로 오인하지 않는다
check("human_enter_not_scan", feedKeys(seq("3500", [150], true)).last.scan, undefined);
// 한글 첫 글자(조합 시작 keydown 은 isComposing=false) 뒤 150ms 에 숫자 — 숫자가 들어가야 한다
check("korean_then_digit_not_swallowed", feedKeys(seq("ㅎ3", [150])).swallowed, "");
// 키 겹침(롤오버) 1회(20ms) — 한 글자도 잃지 않는다
check("single_rollover_not_swallowed", feedKeys(seq("the", [20, 150])).swallowed, "");
check("rollover_mid_word_not_swallowed", feedKeys(seq("abcd", [150, 20, 150])).swallowed, "");

// ── 스캐너(12ms 연타)는 여전히 인식된다: 앞 2글자만 흘리고(leaked=2) 나머지는 삼킨다
{
  const r = feedKeys(seq(ISBN13, [12], true));
  check("scan_recognised", r.last.scan, ISBN13);
  check("scan_leaks_two_leading_chars", r.last.leaked, 2);
  check("scan_swallows_rest", r.swallowed, ISBN13.slice(2));
}
// 스캔 도중 100ms 끊김(렌더 지연) — 확인된 웨지라 느린 글자도 삼키고 값은 온전
{
  const gaps = Array(12).fill(12); gaps[5] = 100;
  const r = feedKeys(seq(ISBN13, gaps, true));
  check("scan_stall_after_wedge_confirmed_full_value", r.last.scan, ISBN13);
  check("scan_stall_after_wedge_confirmed_still_swallows", r.swallowed, ISBN13.slice(2));
}
// 스캔 첫 글자 직후 끊김 — 웨지 확인이 늦어 3글자가 새지만, leaked 로 되돌릴 수 있고 값은 온전
{
  const gaps = Array(12).fill(12); gaps[0] = 100;
  const r = feedKeys(seq(ISBN13, gaps, true));
  check("scan_early_stall_full_value", r.last.scan, ISBN13);
  check("scan_early_stall_reports_leaked", r.last.leaked, 3);
}
// DEC-279 — 500ms 끊김은 여전히 «잘림» 보고(leaked 동반)
{
  const gaps = Array(12).fill(12); gaps[2] = 500;
  const r = feedKeys(seq(ISBN13, gaps, true));
  check("dec279_truncated_still_reported", r.last.truncated, ISBN13.slice(3));
  check("dec279_truncated_carries_leaked", typeof r.last.leaked, "number");
}

// ── 금액 콤마 · 캐럿
check("fmt_zero", formatAmount(0), "0");
check("fmt_grouping", formatAmount(1234567), "1,234,567");
check("fmt_three_digits", formatAmount(350), "350");
check("fmt_nan", formatAmount(NaN), "0");
check("fmt_negative_abs", formatAmount(-1200), "1,200");
check("parse_strips_commas", parseAmountInput("1,234,5"), 12345);
check("parse_leading_zero", parseAmountInput("03"), 3);
check("parse_letters", parseAmountInput("abc"), 0);
check("parse_empty", parseAmountInput(""), 0);
check("parse_mixed", parseAmountInput("3a5,0"), 350);
check("digits_before_caret", digitsBeforeCaret("1,234", 4), 3);
check("caret_after_digits_skips_comma", caretAfterDigits("1,234", 3), 4);
check("caret_after_digits_before_comma", caretAfterDigits("12,345", 2), 2);
check("caret_zero", caretAfterDigits("1,234", 0), 0);
check("caret_overflow_to_end", caretAfterDigits("1,234", 9), 5);
// 타이핑 시나리오: "0" 칸 끝에서 "3","5","0" 입력 → 3 → 35 → 350, "1234" 뒤에 "5" → 12,345 캐럿 끝
check("typing_350", ["03", "35", "350"].map(parseAmountInput), [3, 35, 350]);
check("typing_12345_caret_end", caretAfterDigits(formatAmount(parseAmountInput("1,2345")), digitsBeforeCaret("1,2345", 6)), 6);

// ── 인세비율 — % 는 버리고 숫자·소수점 하나만
check("rate_strips_percent", sanitizeRateInput("10%"), "10");
check("rate_decimal", sanitizeRateInput("7.5"), "7.5");
check("rate_single_dot", sanitizeRateInput("1.2.3"), "1.23");
check("rate_letters", sanitizeRateInput("a1b"), "1");
check("rate_empty", sanitizeRateInput(""), "");

console.log(JSON.stringify(results));
"""


def _tooling_available() -> bool:
    return shutil.which("node") is not None and shutil.which("npx") is not None


@skipUnless(_tooling_available(), "node/npx 미설치 — 행동 검증 skip")
class BehaviourTests(TestCase):
    """§3 행동(node) — 사람 타이핑은 삼켜지지 않고, 스캔은 여전히 인식되며, 금액/비율 포맷이 맞다."""

    def test_wedge_buffer_and_amount_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            compiled = subprocess.run(
                ["npx", "tsc", str(WEDGE_TS), str(AMOUNT_TS), "--outDir", str(out),
                 "--target", "es2020", "--module", "commonjs", "--skipLibCheck"],
                cwd=FRONTEND, capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
            (out / "harness.js").write_text(HARNESS_JS, encoding="utf-8")
            proc = subprocess.run(
                ["node", str(out / "harness.js")],
                cwd=FRONTEND, capture_output=True, text=True, timeout=120,
                env={**os.environ, "NODE_PATH": str(FRONTEND / "node_modules")},
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            results = json.loads(proc.stdout.strip().splitlines()[-1])

        failed = [r for r in results if not r["ok"]]
        self.assertFalse(
            failed,
            "DEC-403 회귀: "
            + ", ".join(f"{r['name']}(got={r['actual']!r} want={r['expected']!r})" for r in failed),
        )
        self.assertEqual(len(results), 38, f"검증 항목 수 변경: {len(results)}")


if __name__ == "__main__":
    main()
