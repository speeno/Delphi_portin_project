"""DEC-405 — 입출금전표 거래처: 거래처명으로도 찾기 · 빈 코드 Enter 정지 · 입력 중 입력순 (2026-10-15 교문사).

신고 원문
--------
1. "입력 시 «코드»와 «거래처명» 양쪽 어느 걸 입력해도 가능해야 하는데, 현재는 코드만 입력해야 지정되네요."
2. "거래처, 입금금액 후 엔터를 치면 자동으로 정렬이 되는 거 같아요. 입력할 때는 입력 자료 그 순서 그대로 있어야 합니다."
3. "코드에서 엔터를 쳐도 내용이 입력이 안 되면 다음 칸으로 안 넘어가게 해 주세요."

결정
----
- 거래처명 칸도 거래처 찾기(MasterLookupField customer · 자동완성 · 검색 팝업) — 고르면 코드·이름·잔액(applyCustomer).
  코드가 붙어 있으면(confirmed) Enter 는 다음 칸, 이름을 고쳐 쓰면 코드를 푼다.
- 코드·거래처명 칸이 비어 있는데 Enter → preventDefault(컨테이너 Enter=다음 칸 차단) + 안내.
- 저장 후 재조회는 `inputOrder: true` + 「입력순」 체크 켬 — 레거시(Subu41 CheckBox2 Order By Gdate,ID)와 같은 정렬 축,
  웹은 저장마다 재조회하므로 입력 중에는 입력순이 기본.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx"
SERVICE = ROOT / "도서물류관리프로그램" / "backend" / "app" / "services" / "cash_slip_service.py"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


class CustomerNameLookup(unittest.TestCase):
    def setUp(self) -> None:
        self.src = _read(PAGE)

    def test_name_cell_is_customer_lookup_with_both_select_paths(self) -> None:
        cell = self.src.split('key: "gname", label: "거래처명"', 1)[1].split("\n      },\n", 1)[0]
        self.assertIn('lookupKind="customer"', cell)
        self.assertIn("useInlineAutocomplete", cell)
        self.assertIn("value={f?.gname ?? \"\"}", cell)
        self.assertIn("applyCustomer(item.hcode, item.gname);", cell)
        self.assertIn("onSelect={(selection) => applyCustomer(selection.code, selection.name)}", cell)
        self.assertIn('confirmed={Boolean((f?.gcode ?? "").trim())}', cell)
        self.assertIn('inputLegacyId="Sobo41.Edit_GNAME"', cell, "레거시 위젯 id 유지(DEC-028)")
        self.assertNotIn('text("gname"', self.src)

    def test_editing_name_unconfirms_code(self) -> None:
        self.assertIn('gcode: nv.trim() === e.form.gname.trim() ? e.form.gcode : ""', self.src)


class EmptyEnterStays(unittest.TestCase):
    def test_code_and_name_cells_hold_enter_when_empty(self) -> None:
        src = _read(PAGE)
        body = src.split("const holdEnterWhenEmpty = (", 1)[1].split("\n    };\n", 1)[0]
        self.assertIn('if (e.key !== "Enter" || e.currentTarget.value.trim()) return;', body)
        self.assertIn("e.preventDefault();", body)
        self.assertEqual(src.count("onKeyDown={holdEnterWhenEmpty}"), 2, "코드 칸 + 거래처명 칸")
        # 컨테이너의 Enter=다음 칸 은 defaultPrevented 를 존중한다(기존 가드)
        self.assertIn("if (e.defaultPrevented || e.nativeEvent.isComposing) return;", src)


class InputOrderWhileEntering(unittest.TestCase):
    def test_save_refetches_in_input_order_and_turns_checkbox_on(self) -> None:
        src = _read(PAGE)
        tail = src.split("async function saveEditing()", 1)[1]
        self.assertIn("setInputOrder(true);", tail)
        self.assertIn("await fetchData({ inputOrder: true }, { draftDate: f.gdate, focus: true });", tail)

    def test_backend_input_order_axis_matches_legacy(self) -> None:
        src = _read(SERVICE)
        self.assertIn('order = "Gdate, ID" if input_order else "Gdate, Gubun, Scode, Gcode"', src)


if __name__ == "__main__":
    unittest.main()
