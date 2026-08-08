"""DEC-134 — 검색 Enter 확정 규칙 최종형 + 신규 컬럼 기본위치 삽입 회귀 가드.

1) MLF Enter 자동확정 = **결과 1건 + 코드 일치/접두·명칭 정확 일치**일 때만.
   한글 단어형 도서코드 테넌트(코드 "기계"/"기계설비"/"축산기계"…)에서 검색어
   "기계"가 실존 코드와 정확 일치 → 다건인데도 그 도서가 자동확정되던 결함
   (2026-08-08 3차 보고, jsdom red/green 재현). 다건은 검색 팝업(정확 일치 행
   우선 강조)으로.
2) useGridPrefs.applyOrder — 저장 순서가 있는 계정에서 신설 컬럼이 맨 끝으로
   밀리던 것을 **기본 정의 위치**(직전 컬럼 뒤) 삽입으로 교정 (도서별판매 '정가'
   가 도서명 다음에 나오도록).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))


class MlfConfirmRuleTests(TestCase):
    def setUp(self) -> None:
        self.src = (
            FRONTEND / "src/components/master/master-lookup-field.tsx"
        ).read_text("utf-8")

    def test_no_multi_item_exact_code_pick(self) -> None:
        # 다건 정확 코드 일치 자동확정 제거 — findIndex 기반 exactIdx 픽이 없어야 한다.
        self.assertNotIn("exactIdx", self.src)
        self.assertIn("items.length === 1", self.src)

    def test_single_item_conditions_kept(self) -> None:
        self.assertIn("code.startsWith(term)", self.src)
        self.assertIn("name === term", self.src)

    def test_dialog_prefers_exact_code_row(self) -> None:
        dialog = (
            FRONTEND / "src/components/master/master-lookup-dialog.tsx"
        ).read_text("utf-8")
        self.assertIn("row.code ?? \"\").trim() === query.trim()", dialog)


# ── applyOrder 파이썬 미러 (use-grid-prefs.ts 와 동일 알고리즘) ──────────────
def apply_order(cols: list[str], order: list[str]) -> list[str]:
    if not order:
        return cols
    seen: set[str] = set()
    ordered: list[str] = []
    for k in order:
        if k in cols and k not in seen:
            ordered.append(k)
            seen.add(k)
    for i, c in enumerate(cols):
        if c in seen:
            continue
        insert_at = 0
        for j in range(i - 1, -1, -1):
            if cols[j] in ordered:
                insert_at = ordered.index(cols[j]) + 1
                break
        ordered.insert(insert_at, c)
        seen.add(c)
    return ordered


class ApplyOrderMirrorTests(TestCase):
    DEFAULTS = ["gcode", "gname", "gdang", "gdate", "giqut", "goqut"]

    def test_new_column_inserted_at_default_position(self) -> None:
        saved = ["gcode", "gname", "gdate", "goqut", "giqut"]  # 정가 신설 전 저장 순서
        out = apply_order(self.DEFAULTS, saved)
        self.assertEqual(out.index("gdang"), out.index("gname") + 1,
                         "신설 '정가'는 저장 순서가 있어도 도서명 다음")
        # 사용자 저장 순서(출고수↔입고수 스왑)는 보존.
        self.assertLess(out.index("goqut"), out.index("giqut"))

    def test_new_head_column_goes_front(self) -> None:
        out = apply_order(["new0", "a", "b"], ["b", "a"])
        self.assertEqual(out, ["new0", "b", "a"])

    def test_multiple_new_columns_keep_relative_order(self) -> None:
        out = apply_order(["a", "n1", "n2", "b"], ["a", "b"])
        self.assertEqual(out, ["a", "n1", "n2", "b"])

    def test_no_saved_order_passthrough(self) -> None:
        self.assertEqual(apply_order(self.DEFAULTS, []), self.DEFAULTS)

    def test_ts_source_has_insertion_loop(self) -> None:
        src = (FRONTEND / "src/components/data-grid/use-grid-prefs.ts").read_text("utf-8")
        self.assertIn("기본 정의 위치", src)
        self.assertIn("ordered.splice(insertAt, 0, c)", src)
        self.assertNotIn("return [...ordered, ...rest]", src)


if __name__ == "__main__":
    main()
