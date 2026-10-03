"""DEC-367 — 검색 팝업: 늦게 도착한 이전 검색 응답이 최신 결과를 덮지 않는다.

보고(교문사, 2026-10-02)
-----------------------
"출고 주문 「도서명」 검색 완료, 커서로 방향으로 도서 선택하러 이동하는데
검색된 도서가 풀리면서 전체 도서로 변경이 됩니다."

원인
----
도서코드 칸이 빈 채 팝업을 열면 빈 검색(전체 200건, 운영 실측 ~7초)이 먼저 나간다.
그 사이 키워드 검색(~1.4초)이 끝나 결과를 보고 ↓ 로 고르는 동안, 늦게 온 빈 검색
응답이 rows 를 덮어 전체 목록으로 바뀌었다(방향키는 원인이 아니라 그 시점에 하던 일).

가드
----
- `doSearchWith` 가 검색 차수(searchSeqRef)를 올리고, 응답 · 오류 · loading 해제 모두
  최신 차수일 때만 반영한다. 팝업을 닫을 때도 차수를 올려 닫힌 뒤 응답을 버린다.
- 출고 라인 도서코드 칸의 감싼 div onBlur 는 포커스가 div 안(팝업 내부)에 머물면
  보충 조회를 하지 않는다(팝업 안에서 포커스가 움직일 때마다 조회가 나가던 부하).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "도서물류관리프로그램" / "frontend" / "src"
DIALOG = SRC / "components" / "master" / "master-lookup-dialog.tsx"
LINE_GRID = SRC / "components" / "outbound" / "order-line-grid.tsx"


def _do_search_body(src: str) -> str:
    start = src.index("const doSearchWith = useCallback(")
    end = src.index("const doSearch = useCallback(", start)
    return src[start:end]


class LookupDialogStaleResponseTests(TestCase):
    def setUp(self) -> None:
        self.src = DIALOG.read_text(encoding="utf-8")
        self.body = _do_search_body(self.src)

    def test_seq_ref_declared(self) -> None:
        self.assertIn("const searchSeqRef = useRef(0);", self.src)

    def test_search_bumps_seq_before_request(self) -> None:
        bump = self.body.index("const seq = ++searchSeqRef.current;")
        req = self.body.index("await config.search(")
        self.assertLess(bump, req)

    def test_result_applied_only_when_latest(self) -> None:
        guard = self.body.index("if (seq !== searchSeqRef.current) return null;")
        set_rows = self.body.index("setRows(res.rows);")
        self.assertLess(guard, set_rows)

    def test_error_applied_only_when_latest(self) -> None:
        catch = self.body.index("} catch (e) {")
        tail = self.body[catch:]
        self.assertLess(
            tail.index("if (seq !== searchSeqRef.current) return null;"),
            tail.index("setRows([]);"),
        )

    def test_loading_cleared_only_by_latest(self) -> None:
        self.assertRegex(
            self.body,
            r"finally \{\s*if \(seq === searchSeqRef\.current\) setLoading\(false\);",
        )

    def test_close_invalidates_pending_search(self) -> None:
        self.assertRegex(
            self.src,
            r"if \(!open\) \{\s*searchSeqRef\.current \+= 1;",
        )


class OutboundBcodeBlurTests(TestCase):
    def test_blur_skips_when_focus_stays_inside(self) -> None:
        src = LINE_GRID.read_text(encoding="utf-8")
        m = re.search(r"onBlur=\{\(e\) => \{(.*?)\}\}", src, re.S)
        self.assertIsNotNone(m)
        body = m.group(1)
        self.assertIn("e.currentTarget.contains(e.relatedTarget", body)
        self.assertLess(body.index("return;"), body.index("lookupTypedBook(idx)"))


if __name__ == "__main__":
    main()
