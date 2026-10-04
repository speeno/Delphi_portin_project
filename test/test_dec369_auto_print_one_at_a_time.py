"""DEC-369 — 자동출력: 여러 건을 한 번에 한 장씩, 장 사이 간격을 두고 인쇄한다.

보고(2026-10-02)
---------------
경리부 계정으로 여러 건 출고요청 → 교문사 계정 PC(자동출력 탭)에서 **한두 건만** 출력.

원인(코드 기준)
--------------
- 자동출력 탭은 전표마다 숨김 iframe 을 만들어 print() 를 부르고, 인쇄가 끝나기를 기다리지
  않은 채 곧바로 다음 전표로 넘어갔다. PDF 렌더가 빨라진 뒤(DEC-157 이후) 연달아 들어오는
  print() 는 앞 인쇄가 끝나기 전이라 Chrome 이 조용히 버릴 수 있다.
- 실시간 스트림 · 3분 폴 · 바로출고 세 경로가 서로 기다리지 않고 동시에 인쇄를 걸 수 있었다.
- 버려진 장도 「인쇄 요청 성공」으로 보고 완료 전이 → 재시도되지 않는다.

가드
----
- 세 경로는 하나의 인쇄 줄(printChainRef)로 차례로 실행.
- 장마다 ``printPdfFromUrl(url, { settleMs })`` 로 간격(기본 5초, ``?printGapSec=``)을 둔다.
- 다른 화면의 수동 인쇄는 종전대로(settleMs 기본 0).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PAGE = SRC / "app" / "(app)" / "transactions" / "sales-statement" / "auto-print" / "page.tsx"
PRINT_API = SRC / "lib" / "print-api.ts"


class AutoPrintOneAtATimeTests(TestCase):
    def setUp(self) -> None:
        self.page = PAGE.read_text(encoding="utf-8")
        self.api = PRINT_API.read_text(encoding="utf-8")

    def test_all_paths_go_through_print_chain(self) -> None:
        self.assertIn("const printChainRef = useRef<Promise<void>>(Promise.resolve());", self.page)
        # DEC-375 — 바로출고 보관 해제 콜백(onKeyTried)이 인자로 추가됐다.
        self.assertIn(
            "const run = printChainRef.current.then(() => printFreshKeysNow(fresh, onKeyTried));", self.page
        )
        self.assertIn("printChainRef.current = run.catch(() => undefined);", self.page)
        # 스트림 · 폴 · 바로출고는 줄 세운 printFreshKeys 를 쓴다(직접 Now 호출 금지).
        self.assertEqual(self.page.count("printFreshKeysNow("), 1)

    def test_each_page_waits_gap(self) -> None:
        self.assertIn("printPdfFromUrl(url, { settleMs: printGapMs })", self.page)
        self.assertIn('get("printGapSec")', self.page)
        self.assertIn("const DEFAULT_PRINT_GAP_MS = 5_000;", self.page)

    def test_print_api_settle_option_defaults_to_zero(self) -> None:
        self.assertIn("settleMs?: number;", self.api)
        self.assertIn("const settleMs = Math.max(0, opts.settleMs ?? 0);", self.api)
        self.assertIn("if (settleMs > 0) window.setTimeout(resolve, settleMs);", self.api)


if __name__ == "__main__":
    main()
