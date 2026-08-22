"""콤보(픽 필드) 키 규약 — Enter=목록, 방향키=입력 컨트롤 이동 (2026-08-22 사용자).

요청 원문
--------
"콤보 입력의 경우, 사용자가 엔터를 입력하면 목록이 나와서 선택하도록 하고 그렇지 않은
경우, 상하좌우 키는 입력 컨트롤 이동이 될 수 있도록 모든 화면에서 수정이 필요하다."

증상
----
신규 출고 주문 라인 그리드의 「구분」(LocalComboField) 에서 ↓ 를 누르면 다음 행으로
내려가지 않고 **콤보 목록이 펼쳐졌다**. 닫힘 상태 핸들러가 `Enter || ArrowDown` 을 모두
"팝업 열기"로 처리하고 `stopPropagation()` 까지 해서, 표의 `handleGridArrowKey` 가
이벤트를 아예 보지 못했다(DEC-119 의 "닫힘 ↓=열기" 규약).

수정
----
- 닫힘 상태에서 목록을 여는 키는 **Enter 뿐**.
- 닫힘 상태 ↑↓←→: 표 안이면 `grid-arrow-nav` 에 양보(버블링), 표 밖이면
  `moveFocusBy` 로 이전/다음 컨트롤 이동.
- `LocalComboField` 는 16개 화면이 공유하므로 이 한 곳 수정으로 전 화면에 적용된다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase, main, skipUnless

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
COMBO = FRONTEND / "src" / "components" / "shared" / "local-combo-field.tsx"
FOCUS_TS = FRONTEND / "src" / "lib" / "focus-advance.ts"
NAV_TS = FRONTEND / "src" / "lib" / "grid-arrow-nav.ts"


class ComboClosedStateKeyRuleTests(TestCase):
    """§1 정적 — 닫힘 상태 키 규약."""

    def setUp(self) -> None:
        self.src = COMBO.read_text(encoding="utf-8")
        # 닫힘 상태 블록 = handleKeyDown 안에서 `if (open) { ... }` 이후.
        body = self.src[self.src.index("function handleKeyDown") :]
        # handleKeyDown 본문만 — 뒤 함수(handleBlur 등)까지 딸려오면 단언이 헐거워진다.
        body = body[: body.index("function handleBlur")]
        self.closed = body[body.index("// ── 닫힘 상태 ──") :]

    def test_only_enter_opens_the_menu(self) -> None:
        """닫힘 상태에서 openMenu 는 Enter 분기에서만 호출된다."""
        self.assertIn('if (e.key === "Enter")', self.closed)
        # 종전 결함: Enter 와 ArrowDown 을 같은 분기에서 처리.
        self.assertNotIn('e.key === "Enter" || e.key === "ArrowDown"', self.src)
        enter_at = self.closed.index('if (e.key === "Enter")')
        open_at = self.closed.index("openMenu()")
        arrow_at = self.closed.index('e.key === "ArrowDown" || e.key === "ArrowUp"')
        self.assertLess(enter_at, open_at, "openMenu 는 Enter 분기 안에 있어야 한다")
        self.assertLess(open_at, arrow_at, "방향키 분기는 Enter 분기 뒤")

    def test_arrows_yield_to_grid_inside_table(self) -> None:
        """표 안(td)에서는 preventDefault/stopPropagation 없이 버블링만 시킨다."""
        self.assertIn('if (el.closest("td")) return;', self.closed)

    def test_arrows_move_focus_outside_table(self) -> None:
        self.assertIn("moveFocusBy(el, dir)", self.closed)

    def test_no_stop_propagation_on_arrows(self) -> None:
        """방향키 분기에 stopPropagation 이 있으면 그리드 이동이 다시 죽는다."""
        arrow_block = self.closed[self.closed.index('e.key === "ArrowDown" || e.key === "ArrowUp"') :]
        # 주석(설명문)에 등장하는 단어는 제외 — 실제 호출만 본다.
        code = "\n".join(
            ln for ln in arrow_block.splitlines() if not ln.strip().startswith("//")
        )
        self.assertNotIn("stopPropagation", code)

    def test_combo_input_is_reachable_by_arrow_nav(self) -> None:
        """픽 필드 입력은 readOnly + role=combobox — 이동 대상 판정에 포함돼야 한다."""
        self.assertIn("readOnly", self.src)
        self.assertIn('role="combobox"', self.src)
        nav = NAV_TS.read_text(encoding="utf-8")
        self.assertIn('getAttribute("role") !== "combobox"', nav)
        focus = FOCUS_TS.read_text(encoding="utf-8")
        self.assertIn('input[role="combobox"]', focus)


HARNESS_JS = r"""
const { JSDOM } = require("jsdom");
const { handleGridArrowKey } = require("./grid-arrow-nav.js");

// 라인 그리드 재현: 열0 = 구분 픽 필드(readOnly + role=combobox), 열1 = 수량(number)
function row(r) {
  return `<tr>
    <td><input id="c${r}" value="위탁" readonly role="combobox"></td>
    <td><input id="q${r}" type="number" value="1"></td>
  </tr>`;
}
const dom = new JSDOM(`<table><tbody>${row(0)}${row(1)}${row(2)}</tbody></table>`,
  { pretendToBeVisual: true });
const { document, HTMLInputElement } = dom.window;
global.HTMLInputElement = HTMLInputElement;
global.HTMLTextAreaElement = dom.window.HTMLTextAreaElement;
global.HTMLSelectElement = dom.window.HTMLSelectElement;
Object.defineProperty(dom.window.HTMLElement.prototype, "offsetParent", {
  get() { return this.hasAttribute("data-hidden") ? null : document.body; },
});

// LocalComboField 닫힘 상태 핸들러(수정본)와 동일한 조건 — 표 안이면 양보.
function comboClosedKeyDown(e) {
  if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); return "open"; }
  if (["ArrowDown","ArrowUp","ArrowLeft","ArrowRight"].includes(e.key)) {
    if (e.target.closest("td")) return "yield";   // 그리드에 양보
    return "moveFocus";
  }
  return null;
}

function press(el, key) {
  let prevented = false, stopped = false;
  const e = {
    key, target: el, nativeEvent: { isComposing: false },
    get defaultPrevented() { return prevented; },
    preventDefault() { prevented = true; },
    stopPropagation() { stopped = true; },
  };
  const comboResult = comboClosedKeyDown(e);      // 자식(콤보) 먼저
  if (!stopped) handleGridArrowKey(e);            // 그 다음 tbody
  return { comboResult, prevented, stopped };
}

const results = [];
const $ = (id) => document.getElementById(id);
const focused = () => document.activeElement && document.activeElement.id;
const check = (name, actual, expected) =>
  results.push({ name, ok: actual === expected, actual, expected });

// 1) 닫힌 콤보에서 ↓ → 목록이 열리지 않고 다음 행 콤보로 이동
$("c0").focus();
const r1 = press($("c0"), "ArrowDown");
check("down_does_not_open_menu", r1.comboResult, "yield");
check("down_moves_to_next_row_combo", focused(), "c1");

// 2) ↑ → 이전 행 콤보
press($("c1"), "ArrowUp");
check("up_moves_to_prev_row_combo", focused(), "c0");

// 3) → → 같은 행 수량 칸(콤보는 readOnly 라 캐럿 편집 없음)
$("c0").focus();
press($("c0"), "ArrowRight");
check("right_moves_within_row", focused(), "q0");

// 4) 수량에서 ← → 콤보로 돌아온다(픽 필드가 이동 대상에 포함)
press($("q0"), "ArrowLeft");
check("left_returns_to_combo", focused(), "c0");

// 5) Enter → 목록 열기(그리드로 전파되지 않음)
$("c0").focus();
const r5 = press($("c0"), "Enter");
check("enter_opens_menu", r5.comboResult, "open");
check("enter_stops_propagation", r5.stopped, true);
check("enter_keeps_focus", focused(), "c0");

console.log(JSON.stringify(results));
"""


def _tooling_available() -> bool:
    if shutil.which("node") is None or shutil.which("npx") is None:
        return False
    return (FRONTEND / "node_modules" / "jsdom").is_dir()


@skipUnless(_tooling_available(), "node/jsdom 미설치 — 행동 검증 skip")
class ComboArrowBehaviourTests(TestCase):
    """§2 행동(jsdom) — 닫힌 콤보에서 방향키가 셀 이동으로 흐른다."""

    def test_arrow_navigation_through_combo_cells(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            compiled = subprocess.run(
                ["npx", "tsc", str(NAV_TS), "--outDir", str(out),
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
            "콤보 방향키 회귀: "
            + ", ".join(f"{r['name']}(got={r['actual']!r} want={r['expected']!r})" for r in failed),
        )
        self.assertEqual(len(results), 8, f"검증 항목 수 변경: {len(results)}")


class ComboUsageBreadthTests(TestCase):
    """§3 — 이 수정이 전 화면에 적용되는지(공용 컴포넌트 단일 수정) 확인."""

    def test_combo_is_shared_by_many_screens(self) -> None:
        src_dir = FRONTEND / "src"
        users = [
            p for p in src_dir.rglob("*.tsx")
            if p.name != "local-combo-field.tsx"
            and "LocalComboField" in p.read_text(encoding="utf-8", errors="replace")
        ]
        self.assertGreaterEqual(
            len(users), 10,
            "LocalComboField 사용처가 급감했다면 콤보 규약이 다른 곳으로 흩어진 것",
        )
        # 신규 출고 주문(스크린샷 화면)의 라인 그리드가 포함돼 있어야 한다.
        names = {p.name for p in users}
        self.assertIn("order-line-grid.tsx", names)


if __name__ == "__main__":
    main()
