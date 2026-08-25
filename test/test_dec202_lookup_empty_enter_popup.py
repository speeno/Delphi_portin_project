"""DEC-202 — 도서/거래처 검색 필드의 빈값 Enter (2026-08-25 사용자 확인 요청).

원문: "도서 검색 창에서 빈입력창 또는 키워드입력해서 엔터 입력하면 검색창이 떠야하지 않나? 또한 값을
선택하면 도서 코드나 도서명이 입력박스에 자동 입력되야하지 않나?"

확인 결과
--------
- 키워드 Enter → 1건 정확 일치면 자동 확정, 그 외 검색 팝업(DEC-134) — 정상.
- 선택 → `onValueChange(code)` 로 입력창에 코드, 옆에 도서명·정가 — 정상.
- **빈값 Enter** — MLF 규약: `onKeyDown` 제공 시 통과(패널 Enter 이동), 미제공 시 검색 팝업.
  도서별수불원장·거래처거래원장은 **빈 핸들러** `onKeyDown={() => {}}` 를 넘기면서 패널에 Enter
  이동 스코프(`advanceFilterOnEnter`/`data-enter-scope`)가 없어 Enter 가 아무 동작도 하지 않았다.
  → 두 화면은 빈 핸들러를 제거해 MLF 기본(빈값 Enter=검색 팝업)이 살아난다.
- 필터 패널에 Enter 이동 스코프가 있는 화면(36개)은 DEC-104/105/144 그대로 빈값 Enter=다음 입력칸.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"

NOOP = re.compile(r"onKeyDown=\{\(\) => \{\}\}")


def _mlf_blocks(src: str) -> list[str]:
    out = []
    i = 0
    while True:
        j = src.find("<MasterLookupField", i)
        if j == -1:
            return out
        k = src.find("/>", j)
        out.append(src[j:k])
        i = k


class EmptyEnterOpensPopupWhereNoScope(TestCase):
    def test_ledger_screens_have_no_noop_handler_on_lookup(self) -> None:
        for rel in ("inventory/ledger/page.tsx", "ledger/customer/page.tsx"):
            src = (APP / rel).read_text(encoding="utf-8")
            blocks = _mlf_blocks(src)
            self.assertTrue(blocks, rel)
            for b in blocks:
                self.assertIsNone(NOOP.search(b), f"{rel}: MLF 에 빈 onKeyDown 이 남아 빈값 Enter 가 죽는다")

    def test_no_screen_leaves_empty_enter_dead(self) -> None:
        """MLF 에 빈 onKeyDown 을 넘기는 화면은 반드시 패널 Enter 이동 스코프를 가져야 한다."""
        dead = []
        for p in sorted(APP.glob("**/page.tsx")):
            src = p.read_text(encoding="utf-8")
            if not any(NOOP.search(b) for b in _mlf_blocks(src)):
                continue
            if not re.search(r"advanceFilterOnEnter|data-enter-scope|advanceFocusOnEnter", src):
                dead.append(str(p.relative_to(APP)))
        self.assertEqual(dead, [], dead)

    def test_mlf_default_empty_enter_is_popup(self) -> None:
        mlf = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "master"
               / "master-lookup-field.tsx").read_text(encoding="utf-8")
        i = mlf.index("// 빈값 Enter — 호출자")
        block = mlf[i : i + 300]
        self.assertIn("if (onKeyDown) {", block)
        self.assertIn("handleDialogOpenChange(true);", block)


if __name__ == "__main__":
    main()
