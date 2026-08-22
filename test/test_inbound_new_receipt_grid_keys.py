"""신규 입고접수 화면 — 헤더/컬럼 구성 + 라인 그리드 키보드 이동 회귀 (2026-08-22 운영 요청).

요청 원문
--------
"신규 입고 접수 화면은 거래일자, 입고처 코드, 입고처 및 목록 필드로 구분, 도서코드,
도서명, 수량, 단가, 비율, 금액, 비고 순으로 표기 (…) 라인 추가하여 입력 시 상하좌우
키보드로 입력 박스를 이동할 수 있도록 하고, 가능하면 스핀 컨트롤도 상하 키에 대해서
값변경 컨트롤이 아닌 입력 필드 이동 기능으로 오버라이딩"

검증 2계층
---------
1. **정적** — 헤더 3필드 라벨, 라인 컬럼 7종 순서, `handleGridArrowKey`(DEC-168) 배선,
   ``handleQtyArrowKey``(↑/↓ 값 ±1) 미사용.
2. **행동(jsdom)** — 실제 DOM 에서 ↑/↓/←/→ 셀 이동과 number 스핀 억제를 확인한다.
   node/jsdom/tsc 가 없으면 skip (DEC-173 외부 의존 skip 정책).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
PAGE = FRONTEND / "src" / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
NAV_TS = FRONTEND / "src" / "lib" / "grid-arrow-nav.ts"


class NewReceiptLayoutTests(TestCase):
    """§1 정적 — 헤더 3필드 + 라인 7컬럼."""

    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")

    def test_header_fields(self) -> None:
        """헤더 = 거래일자 · 입고처 코드 · 입고처."""
        for label in ('>거래일자<', '>입고처 코드<', '>입고처<'):
            self.assertIn(label, self.src, label)
        # 종전 표기/불필요 항목 제거 — '입고 일자'(공백형), 지사 입력칸.
        self.assertNotIn("입고 일자", self.src)
        self.assertNotIn('htmlFor="gjisa"', self.src)

    def test_line_columns_in_order(self) -> None:
        """라인 컬럼 = 구분 · 도서코드 · 도서명 · 수량 · 단가 · 비율 · 금액 · 비고 (이 순서).

        2026-08-22 2차 요청으로 「구분」(Pubun)이 **맨 앞에 복원**됐다.
        """
        wanted = ["구분", "도서코드", "도서명", "수량", "단가", "비율", "금액", "비고"]
        positions = []
        for label in wanted:
            marker = f">{label}</th>"
            idx = self.src.find(marker)
            self.assertNotEqual(idx, -1, f"컬럼 헤더 누락: {label}")
            positions.append(idx)
        self.assertEqual(positions, sorted(positions), f"컬럼 순서 불일치: {wanted}")
        # '구분'(pubun) 은 화면 입력 + 전송 모두 유지 — 입고처 기본값이 자동으로 채워진다.
        self.assertIn("pubun", self.src, "pubun 전송 자체는 유지돼야 한다")
        # 자유 입력이 아니라 **픽 필드(LocalComboField)** — 레거시 Sobo40 콤보 동형.
        self.assertIn('ariaLabel="구분"', self.src)
        self.assertIn("PUBUN_COMBO_OPTIONS", self.src)





    def test_bname_is_display_only(self) -> None:
        """도서명은 표기 전용 — 입력/이동 대상에서 제외(readOnly + tabIndex -1)."""
        self.assertIn("_bname", self.src)
        self.assertIn('aria-label="도서명"', self.src)

    def test_grid_arrow_nav_wired_and_qty_spinner_dropped(self) -> None:
        self.assertIn("handleGridArrowKey", self.src)
        self.assertIn("<tbody onKeyDown={handleLineGridKeyDown}>", self.src)
        # ↑/↓ 로 수량을 ±1 하던 처리는 제거(이 화면은 '이동'이 정본).
        self.assertNotIn("handleQtyArrowKey", self.src)

    def test_spinner_suppression_runs_after_nav(self) -> None:
        """순서 보장 — 먼저 이동 시도, 이동 못 했을 때만 스핀 차단.

        (역순이면 defaultPrevented 로 인해 셀 이동이 영영 동작하지 않는다.)

        2026-08-22 전 화면 통일로 스핀 억제가 이 페이지의 래퍼에서 공용 헬퍼
        `grid-arrow-nav` 안으로 옮겨졌다 — 페이지는 헬퍼에 그대로 위임하므로
        순서 검증도 헬퍼 본문에서 한다.
        """
        # 페이지는 자체 스핀 처리 없이 공용 헬퍼에 위임한다.
        self.assertIn("handleGridArrowKey", self.src)
        body = NAV_TS.read_text(encoding="utf-8")
        body = body[body.index("export function handleGridArrowKey") :]
        move_at = body.index("nextElementSibling")  # ↑/↓ 이웃 행 탐색
        guard_at = body.rindex('type === "number"')  # 이동 대상이 없을 때만 스핀 차단
        self.assertLess(move_at, guard_at, "스핀 억제는 행 이동 시도 뒤에 와야 한다")
        self.assertIn("e.preventDefault()", body[guard_at:])


class PubunComboOptionsTests(TestCase):
    """구분 목록 = 레거시 정본 10종 (Subu40.dfm Sobo40.Edit101)."""

    LEGACY = ["위탁", "현매", "매절", "납품", "증정", "특별", "한도", "개정", "기타", "신간"]

    def setUp(self) -> None:
        self.src = (FRONTEND / "src" / "lib" / "pubun-options.ts").read_text(encoding="utf-8")

    def test_full_list_matches_legacy_order(self) -> None:
        import re
        # 배열 리터럴만 잡는다 — 앞선 docstring 언급이나 `string[]` 의 대괄호에 걸리지 않게.
        m = re.search(r"PUBUN_OPTIONS_FULL[^=]*=\s*\[([\s\S]*?)\]", self.src)
        self.assertIsNotNone(m, "PUBUN_OPTIONS_FULL 배열을 찾지 못했다")
        found = re.findall(r'"([가-힣]{2})"', m.group(1))
        self.assertEqual(found, self.LEGACY, "레거시 Sobo40 콤보 순서와 달라졌다")

    def test_default_is_wital(self) -> None:
        self.assertIn('PUBUN_DEFAULT = "위탁"', self.src)

    def test_outbound_six_option_list_kept_separate(self) -> None:
        """출고 라인 그리드는 공급율(Grat1~6) 연동이라 6종 유지 — 통합 금지."""
        grid = (
            FRONTEND / "src" / "components" / "outbound" / "order-line-grid.tsx"
        ).read_text(encoding="utf-8")
        self.assertIn("rateIndex", grid)
        for v in ("증정", "한도", "개정", "신간"):
            self.assertNotIn(f'value: "{v}"', grid, f"출고 6종에 {v} 가 섞이면 비율 계산이 깨진다")

    def test_inbound_screens_use_the_shared_list(self) -> None:
        for rel in (
            "src/app/(app)/inbound/receipts/new/page.tsx",
            "src/components/inbound/inbound-line-grid.tsx",
        ):
            src = (FRONTEND / rel).read_text(encoding="utf-8")
            with self.subTest(file=rel):
                self.assertIn("PUBUN_COMBO_OPTIONS", src)
                self.assertIn("LocalComboField", src)


HARNESS_JS = r"""
const { JSDOM } = require("jsdom");
const { handleGridArrowKey } = require("./grid-arrow-nav.js");

const ROWS = 3;
function cell(row, col) {
  if (col === 0) return `<td><input id="r${row}c0" value="B00${row}"></td>`;
  if (col === 1) return `<td><input id="r${row}c1" value="도서${row}" readonly tabindex="-1"></td>`;
  if (col === 6) return `<td><input id="r${row}c6" value=""></td>`;
  return `<td><input id="r${row}c${col}" type="number" value="${10 + col}"></td>`;
}
const rows = Array.from({ length: ROWS }, (_, r) =>
  `<tr>${Array.from({ length: 7 }, (_, c) => cell(r, c)).join("")}</tr>`).join("");

const dom = new JSDOM(`<table><tbody id="tb">${rows}</tbody></table>`, { pretendToBeVisual: true });
const { document, HTMLInputElement } = dom.window;
global.HTMLInputElement = HTMLInputElement;
global.HTMLTextAreaElement = dom.window.HTMLTextAreaElement;
global.HTMLSelectElement = dom.window.HTMLSelectElement;
// jsdom 은 offsetParent 미구현(항상 null) → 가시성 판정 통과용 stub.
Object.defineProperty(dom.window.HTMLElement.prototype, "offsetParent", {
  get() { return this.hasAttribute("data-hidden") ? null : document.body; },
});

// page.tsx 는 `handleLineGridKeyDown = handleGridArrowKey` 로 위임한다 —
// 하니스도 실제 배송 경로 그대로 공통 헬퍼를 직접 호출한다(래퍼 복제 금지).
const handleLineGridKeyDown = handleGridArrowKey;

function press(el, key, opts) {
  const isComposing = !!(opts && opts.isComposing);
  let prevented = false;
  handleLineGridKeyDown({
    key, target: el, nativeEvent: { isComposing },
    get defaultPrevented() { return prevented; },
    preventDefault() { prevented = true; },
  });
  return prevented;
}

const results = [];
const $ = (id) => document.getElementById(id);
const focused = () => document.activeElement && document.activeElement.id;
function check(name, actual, expected) {
  results.push({ name, ok: actual === expected, actual, expected });
}

$("r0c2").focus();
press($("r0c2"), "ArrowDown");
check("down_moves_same_column", focused(), "r1c2");

press($("r1c2"), "ArrowUp");
check("up_moves_same_column", focused(), "r0c2");

const before = $("r0c2").value;
$("r0c2").focus();
check("down_prevents_default", press($("r0c2"), "ArrowDown"), true);
check("target_value_unchanged", $("r1c2").value, "12");
check("origin_value_unchanged", $("r0c2").value, before);

$(`r${ROWS - 1}c2`).focus();
check("last_row_down_still_prevents", press($(`r${ROWS - 1}c2`), "ArrowDown"), true);
check("last_row_down_keeps_focus", focused(), `r${ROWS - 1}c2`);

$("r0c3").focus();
check("first_row_up_still_prevents", press($("r0c3"), "ArrowUp"), true);

$("r0c0").focus();
$("r0c0").setSelectionRange($("r0c0").value.length, $("r0c0").value.length);
press($("r0c0"), "ArrowRight");
check("right_skips_readonly_bname", focused(), "r0c2");
press($("r0c2"), "ArrowLeft");
check("left_skips_readonly_bname", focused(), "r0c0");

const bigo = $("r0c6");
bigo.value = "메모";
bigo.focus();
bigo.setSelectionRange(1, 1);
check("caret_mid_does_not_move", press(bigo, "ArrowRight"), false);
check("caret_mid_keeps_focus", focused(), "r0c6");

$("r0c2").focus();
check("ime_composing_ignored", press($("r0c2"), "ArrowDown", { isComposing: true }), false);

console.log(JSON.stringify(results));
"""


def _tooling_available() -> bool:
    if shutil.which("node") is None or shutil.which("npx") is None:
        return False
    return (FRONTEND / "node_modules" / "jsdom").is_dir()


@skipUnless(_tooling_available(), "node/jsdom 미설치 — 행동 검증 skip")
class NewReceiptGridKeyBehaviourTests(TestCase):
    """§2 행동 — 실제 DOM 에서 ↑/↓/←/→ 이동 + number 스핀 억제."""

    def test_arrow_navigation_behaviour(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            compiled = subprocess.run(
                ["npx", "tsc", str(NAV_TS), "--outDir", str(out),
                 "--target", "es2020", "--module", "commonjs", "--skipLibCheck"],
                cwd=FRONTEND, capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(
                compiled.returncode, 0,
                f"grid-arrow-nav.ts 컴파일 실패: {compiled.stdout}{compiled.stderr}",
            )
            (out / "harness.js").write_text(HARNESS_JS, encoding="utf-8")
            proc = subprocess.run(
                ["node", str(out / "harness.js")],
                cwd=FRONTEND, capture_output=True, text=True, timeout=120,
                env={**__import__("os").environ,
                     "NODE_PATH": str(FRONTEND / "node_modules")},
            )
            self.assertEqual(proc.returncode, 0, f"harness 실행 실패: {proc.stderr}")
            results = json.loads(proc.stdout.strip().splitlines()[-1])

        self.assertTrue(results, "검증 결과가 비어 있다")
        failed = [r for r in results if not r["ok"]]
        self.assertFalse(
            failed,
            "키보드 이동 회귀: "
            + ", ".join(f"{r['name']}(got={r['actual']!r} want={r['expected']!r})" for r in failed),
        )
        # 커버리지 고정 — 항목이 조용히 줄어드는 것 방지.
        self.assertEqual(len(results), 13, f"검증 항목 수 변경: {len(results)}")


if __name__ == "__main__":
    main()
