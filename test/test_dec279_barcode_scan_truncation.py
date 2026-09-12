"""바코드 스캔 «앞 3자리(978) 유실» 회귀 — DEC-279 (2026-09-12 사용자 신고).

신고 원문
--------
"바코드 스케너 입력 결과에서 987 등 앞 3자리가 빠져서 입력이 되는데 이유가 있나?"
→ 신규도서 추가(`master/book/new`) 화면에서 사용.

원인 (두 겹)
-----------
1. **전역 캡처 버퍼가 앞부분을 버렸다.** `barcode-scanner.ts` 는 키 간격이 `NEW_SEQ_MS=60ms`
   만 벌어져도 버퍼를 그 글자로 리셋했다(80ms idle 타이머도 동일). 스캔 버스트 도중 메인
   스레드가 한 번만 막히면 앞부분이 통째로 버려지고 **꼬리만** 남는다.
2. **잘린 값이 검증을 통과했다.** `parseIsbn` 이 체크디지트를 보지 않아, 13자리에서 앞
   3자리가 잘린 **10자리 꼬리**가 ISBN-10 패턴(`^\\d{9}[0-9Xx]$`)에 그대로 걸려 «정상 스캔»
   으로 ISBN 칸에 입력됐다. (1자리만 잘리면 12자리라 인식 실패로 보여 눈에 띄었다.)

수정
----
- 버퍼 규칙을 공용 상태기계 `lib/wedge-buffer.ts` 로 분리: `splitMs=300ms` 이내 끊김은 같은
  시퀀스로 이어 붙이고, 그보다 벌어져 앞부분을 잃으면 값을 확정하지 않고 `truncated` 로
  보고(화면은 "다시 스캔하세요" 안내).
- 파싱을 순수 모듈 `lib/barcode-parse.ts` 로 분리하고 **체크디지트 검증**(EAN-13 mod10 /
  ISBN-10 mod11) 추가. 스캔 경로는 `parseScanned=parseIsbn13` 으로 **13자리만** 인정 —
  스캐너의 「ISBN 변환」 설정으로 10자리가 와도 조용히 들어가지 않는다.
- 전용 스캔칸(출고/입고/반품 `ScanInput`)은 키스트로크 버퍼를 아예 쓰지 않고 **input 의 DOM
  값**을 읽는다 → 잘림 불가 + 수기 입력("ISBN 입력 후 Enter")도 비로소 동작.

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
PARSE_TS = LIB / "barcode-parse.ts"
WEDGE_TS = LIB / "wedge-buffer.ts"
HOOK_TS = LIB / "barcode-scanner.ts"
SCANNER_TS = LIB / "scanner.ts"
FIELD_TSX = FRONTEND / "src" / "components" / "shared" / "barcode-scanner-field.tsx"
BOOK_NEW = FRONTEND / "src" / "app" / "(app)" / "master" / "book" / "new" / "page.tsx"


class ModuleLayoutTests(TestCase):
    """§1 정적 — 파싱/버퍼가 순수 모듈로 분리되어 있고 화면 import 가 살아 있다."""

    def test_pure_modules_exist_without_react(self) -> None:
        for p in (PARSE_TS, WEDGE_TS):
            self.assertTrue(p.exists(), f"missing {p.name}")
            src = p.read_text(encoding="utf-8")
            self.assertNotIn("from \"react\"", src, f"{p.name} 은 React 비의존이어야 한다")
            self.assertNotIn("use client", src)

    def test_hook_reexports_formats_for_existing_imports(self) -> None:
        """화면들은 `@/lib/barcode-scanner` 에서 포맷을 가져온다 — 경로 호환 유지."""
        src = HOOK_TS.read_text(encoding="utf-8")
        self.assertIn("from \"@/lib/barcode-parse\"", src)
        for name in ("ISBN_FORMAT", "EAN13_FORMAT", "ANY_BARCODE", "parseIsbn"):
            self.assertIn(name, src)
        self.assertIn("ISBN_FORMAT", BOOK_NEW.read_text(encoding="utf-8"))


class WedgeBufferRuleTests(TestCase):
    """§2 정적 — 60ms 리셋 규칙이 사라지고 공용 상태기계를 쓴다."""

    def test_hook_uses_shared_wedge_buffer(self) -> None:
        src = HOOK_TS.read_text(encoding="utf-8")
        self.assertIn("createWedgeBuffer", src)
        self.assertNotIn("NEW_SEQ_MS", src, "60ms 새 시퀀스 리셋이 남아 있으면 앞자리가 다시 잘린다")

    def test_split_threshold_is_not_tiny(self) -> None:
        src = WEDGE_TS.read_text(encoding="utf-8")
        self.assertIn("splitMs = 300", src)
        self.assertIn("truncated", src, "앞부분 유실 보고 경로가 있어야 한다")

    def test_dedicated_input_reads_dom_value(self) -> None:
        """전용 스캔칸은 키스트로크 버퍼 대신 input 값을 읽는다(잘림 원천 차단)."""
        src = SCANNER_TS.read_text(encoding="utf-8")
        code = "\n".join(
            ln for ln in src.splitlines()
            if not ln.lstrip().startswith(("*", "//", "/*"))
        )
        self.assertNotIn("bufferRef", code)
        self.assertNotIn("resetIdleMs", code, "50ms idle 버퍼 폐기가 남아 있으면 앞자리가 다시 잘린다")
        self.assertNotIn("setTimeout", code)
        self.assertIn("el?.value", code)


class ChecksumGuardTests(TestCase):
    """§3 정적 — 체크디지트 검증과 스캔 전용 엄격 파서."""

    def test_parse_validates_check_digits(self) -> None:
        src = PARSE_TS.read_text(encoding="utf-8")
        self.assertIn("isValidEan13", src)
        self.assertIn("isValidIsbn10", src)
        self.assertIn("export function parseIsbn13", src)
        self.assertIn("parseScanned: parseIsbn13", src)

    def test_field_explains_both_failure_reasons(self) -> None:
        src = FIELD_TSX.read_text(encoding="utf-8")
        self.assertIn('lastScan.reason === "truncated"', src)
        self.assertIn('lastScan.reason === "scanner_isbn10"', src)


HARNESS_JS = r"""
const { createWedgeBuffer } = require("./wedge-buffer.js");
const { parseIsbn, parseIsbn13, isValidEan13, isValidIsbn10 } = require("./barcode-parse.js");

const results = [];
const check = (name, actual, expected) =>
  results.push({ name, ok: JSON.stringify(actual) === JSON.stringify(expected), actual, expected });

// 스캔 1건을 키 이벤트 열로 만든다. stallAfter 번째 글자 뒤에 stallMs 만큼 끊김을 넣는다.
function burst(code, { gap = 12, stallAfter = null, stallMs = 0 } = {}) {
  let t = 1000; // performance.now() 는 0 이 아니다
  const keys = [];
  code.split("").forEach((c, i) => {
    keys.push({ k: c, t });
    t += i === stallAfter ? stallMs : gap;
  });
  keys.push({ k: "Enter", t });
  return keys;
}

function feed(keys, opts) {
  const wedge = createWedgeBuffer(opts);
  let out = { swallow: false };
  const swallowed = [];
  for (const { k, t } of keys) {
    out = wedge.key(k, t);
    if (out.swallow && !out.scan && !out.truncated) swallowed.push(k);
  }
  return { last: out, swallowed: swallowed.join("") };
}

const ISBN13 = "9788954601252";      // 체크디지트 유효
const TAIL = ISBN13.slice(3);        // "8954601252" — 앞 3자리 유실 시 남는 꼬리

// 1) 정상 스캔 — 13자리 그대로 확정
check("clean_scan", feed(burst(ISBN13)).last.scan, ISBN13);

// 2) 신고 재현: 3번째 글자 뒤 100ms 끊김 — 종전엔 꼬리 10자리가 확정됐다.
const stalled = feed(burst(ISBN13, { stallAfter: 2, stallMs: 100 })).last;
check("stall_100ms_keeps_full_code", stalled.scan, ISBN13);
check("stall_100ms_not_truncated", stalled.truncated, undefined);

// 3) 300ms 를 넘는 끊김 — 앞부분을 잃었으므로 «확정 금지 + 재스캔 안내»
const broken = feed(burst(ISBN13, { stallAfter: 2, stallMs: 500 })).last;
check("stall_500ms_no_scan", broken.scan, undefined);
check("stall_500ms_reports_truncated", broken.truncated, TAIL);

// 4) 사람 타이핑(120ms 간격) + Enter → 스캔으로 오인하지 않는다
const human = feed(burst(ISBN13, { gap: 120 })).last;
check("human_typing_not_a_scan", human.scan, undefined);
check("human_typing_not_truncated", human.truncated, undefined);

// 5) 사람이 치던 중(끊김 1.5s 초과) 스캔이 들어오면 정상 스캔 — 헛경고 없음
{
  const wedge = createWedgeBuffer();
  let t = 1000;
  for (const c of "메모") { wedge.key(c, t); t += 150; }
  t += 3000;
  let out;
  ISBN13.split("").forEach((c) => { out = wedge.key(c, t); t += 12; });
  out = wedge.key("Enter", t);
  check("scan_after_idle_typing", out.scan, ISBN13);
}

// 6) 스캔 문자는 포커스 필드로 새지 않는다(첫 글자 1개만 흘리고 호출자가 되돌린다)
check("only_first_char_leaks", feed(burst(ISBN13)).swallowed, ISBN13.slice(1));

// 7) 체크디지트 — 잘린 꼬리/오타는 형식 검사만으로 통과하면 안 된다
check("valid_ean13", isValidEan13(ISBN13), true);
check("tail_fails_isbn10_checksum", isValidIsbn10(TAIL), false);
check("parse_rejects_tail", parseIsbn(TAIL), null);
check("parse_accepts_full", parseIsbn(ISBN13), ISBN13);
check("parse_accepts_addon", parseIsbn(ISBN13 + "13900"), ISBN13);
check("parse_rejects_wrong_check_digit", parseIsbn("9788954601253"), null);
check("parse_accepts_valid_isbn10_manual", parseIsbn("8934912340"), "8934912340");

// 8) 스캔 경로는 13자리만 — 스캐너 「ISBN 변환」 설정(체크디지트까지 유효한 10자리)도 거부
check("scan_parser_rejects_isbn10", parseIsbn13("8934912340"), null);
check("scan_parser_accepts_isbn13", parseIsbn13(ISBN13), ISBN13);

console.log(JSON.stringify(results));
"""


def _tooling_available() -> bool:
    return shutil.which("node") is not None and shutil.which("npx") is not None


@skipUnless(_tooling_available(), "node/npx 미설치 — 행동 검증 skip")
class WedgeBufferBehaviourTests(TestCase):
    """§4 행동(node) — 끊긴 스캔이 «꼬리만 확정» 되지 않는다."""

    def test_scan_buffer_and_isbn_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            compiled = subprocess.run(
                ["npx", "tsc", str(WEDGE_TS), str(PARSE_TS), "--outDir", str(out),
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
            "스캔 버퍼/ISBN 검증 회귀: "
            + ", ".join(f"{r['name']}(got={r['actual']!r} want={r['expected']!r})" for r in failed),
        )
        self.assertEqual(len(results), 18, f"검증 항목 수 변경: {len(results)}")


if __name__ == "__main__":
    main()
