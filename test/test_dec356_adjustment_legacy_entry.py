"""DEC-356 — 원장변경 · 재고변경: 기입 방식을 레거시(위러브솔루션)와 같게 (2026-09-30, 교문사 경리부).

「기입하는 첫 줄은 무조건 생성되어 있어야 하며, 날짜별로 거래처 원장변경하고자 하는 내용을 기입해야 합니다.
위러브솔루션은 날짜별로 거래처 내용을 기입할 수 있습니다.」 / 재고변경: 「기입방법, 검색방법이 원장변경과 동일」.

레거시 정본 — WeLove_FTP/도서유통-출판/Subu51.pas · Subu52.pas (DBGrid101KeyPress/KeyDown), Base01.pas(T5_Sub11NewRecord):
  - DBGrid 맨 아래 빈 삽입행에 곧바로 기입(거래처/도서를 검색칸에서 지정하지 않아도 된다).
  - Enter: 코드(확정 → 이름 · 원장값 채움) → 대조 → 차액(= 대조 − 원장) → 적요 → 다음 줄 거래일자.
  - 원장값은 원장 · 차액이 둘 다 0 인 행만 채운다. 새 줄 거래일자 = 직전 줄 거래일자(없으면 오늘).
  - 원장변경 원장금액 = 그 거래일자(당일 포함)까지의 미수 잔액(Tong40._Sv_Chng_).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
SCREEN = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "ledger" / "adjustment-ledger-screen.tsx"
sys.path.insert(0, str(BACKEND))

from app.services import customer_txn_ledger_service as txn  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class ReceivableAsOfDate(TestCase):
    """원장금액 = 거래일자 당일까지의 미수 잔액. 전일미수(당일 미만)와 창 끝만 다르다."""

    def _capture(self, *, inclusive: bool, snapshot: str = "2026.06.30"):
        seen: list[tuple[str, tuple]] = []

        async def fake_query(server_id, sql, params=()):
            seen.append((sql, tuple(params)))
            if "MAX(Gdate)" in sql:
                return [{"d": snapshot}]
            if "FROM Sv_Chng" in sql:
                return [{"s": 1000, "u": 100}]
            if "FROM S1_Ssub" in sql:
                return [{"s": 500}]
            if "FROM H1_Ssub" in sql:
                return [{"inp": 300, "outp": 0}]
            if "FROM Sg_Gsum" in sql:
                return [{"b": -50}]
            return []

        with patch.object(txn, "execute_query", AsyncMock(side_effect=fake_query)):
            if inclusive:
                total = _run(txn.receivable_asof("s", hcode="5019", gcode="3313", asof="2026.09.30"))
            else:
                total = _run(txn._opening_receivable("s", hcode="5019", gcode="3313", date_from="2026.09.30"))
        return total, seen

    def test_balance_formula(self) -> None:
        total, _ = self._capture(inclusive=True)
        # 스냅샷(1000 − 100) + 출고·반품 500 − 입금 300 + 장부대조 −50
        self.assertEqual(total, 1050)

    def test_window_includes_the_date_itself(self) -> None:
        _, seen = self._capture(inclusive=True)
        windows = [sql for sql, _ in seen if "FROM S1_Ssub" in sql or "FROM H1_Ssub" in sql or "FROM Sg_Gsum" in sql]
        self.assertEqual(len(windows), 3)
        for sql in windows:
            self.assertIn("Gdate > %s AND Gdate <= %s", sql, "창 = (스냅샷, 거래일자] — 당일 포함")
        snap_sql = next(sql for sql, _ in seen if "MAX(Gdate)" in sql)
        self.assertIn("Gdate < %s", snap_sql, "스냅샷은 레거시처럼 거래일자 이전")

    def test_opening_receivable_is_unchanged(self) -> None:
        _, seen = self._capture(inclusive=False)
        for sql, _ in seen:
            self.assertNotIn("<=", sql.replace(">=", ""), "전일미수는 당일 미만 그대로")

    def test_every_query_is_account_scoped(self) -> None:
        _, seen = self._capture(inclusive=True)
        for sql, params in seen:
            self.assertIn("Hcode=%s", sql)
            self.assertIn("5019", params)

    def test_blank_code_is_zero_without_queries(self) -> None:
        with patch.object(txn, "execute_query", AsyncMock(return_value=[])) as q:
            self.assertEqual(_run(txn.receivable_asof("s", hcode="5019", gcode=" ", asof="2026.09.30")), 0)
            q.assert_not_awaited()


class ScreenEntryLikeLegacy(TestCase):
    def setUp(self) -> None:
        self.src = SCREEN.read_text(encoding="utf-8").replace("\r\n", "\n")

    def test_input_row_is_always_appended_after_search(self) -> None:
        load = self.src.split("const load = useCallback(")[1].split("// hydration 후 1회")[0]
        self.assertIn("setRows([...loaded, seeded]);", load, "결과가 0건이어도 · 코드를 확정하지 않아도 입력 줄")
        self.assertNotIn("seeded ? [...loaded, seeded] : loaded", load)
        self.assertIn("pristine: true", load, "건드리기 전엔 저장 대상이 아니다")

    def test_input_row_invariant_is_restored(self) -> None:
        self.assertIn("function isInputRow(r: DraftRow): boolean", self.src)
        self.assertIn("r.origin === null && (r.pristine === true || isBlankNew(r))", self.src)
        effect = self.src.split("// 입력 줄은 항상 맨 아래에 있다(DEC-356).")[1].split("const addRow = useCallback(")[0]
        self.assertIn("if (last && isInputRow(last)) return;", effect, "이미 있으면 붙이지 않는다(반복 없음)")
        self.assertIn("if (!serverId || loading || saving) return;", effect)
        self.assertIn("return tail && isInputRow(tail) ? prev : [...prev, row];", effect)

    def test_new_row_date_follows_the_row_above(self) -> None:
        # 레거시 T5_Sub11NewRecord: 직전 줄 거래일자, 없으면 오늘(웹은 조회 종료일 — 기본 당일).
        self.assertIn("makeInputRow(last && last.origin === null ? last.gdate : dateTo)", self.src)

    def test_add_line_button_does_not_stack_blank_rows(self) -> None:
        add = self.src.split("const addRow = useCallback(")[1].split("}, [dateTo")[0]
        self.assertIn("if (!last || !isInputRow(last)) {", add)
        self.assertIn("focusLastRowStart();", add)

    def test_grid_is_shown_before_any_search(self) -> None:
        self.assertNotIn("<EmptyHint", self.src, "조회 전 안내문 대신 표 + 입력 줄")
        self.assertNotIn("!searched", self.src)

    def test_input_row_is_neither_saved_nor_exported(self) -> None:
        self.assertIn("if (!o) return !r.pristine && !isBlankNew(r);", self.src)
        self.assertIn("displayRows.filter((r) => !isInputRow(r))", self.src)

    def test_enter_order(self) -> None:
        code_col = self.src.split('key: "gcode",')[1].split('key: "gname",')[0]
        self.assertIn('focusSameRowCell(e.currentTarget, ".GSSUM.EDIT")', code_col, "코드 Enter → 대조(이름 칸 건너뜀)")
        self.assertIn("commitCode(row.uid, row.gcode, row.gdate);", code_col, "확정 = 이름 · 원장값 채움")
        self.assertIn("row.gcode.trim()", code_col, "빈 코드는 이름 칸으로(이름으로 찾기)")
        amount = self.src.split("function AmountCell(")[1].split("return [")[0]
        self.assertIn('field === "gssum" && e.key === "Enter"', amount)
        self.assertIn('focusSameRowCell(e.currentTarget, ".GBSUM.EDIT")', amount, "대조 Enter → 차액(원장 칸 건너뜀)")
        memo = self.src.split("patchRow(row.uid, { gbigo: e.target.value })")[1].split("/>")[0]
        self.assertIn("focusNextGridCell(e);", memo, "적요 Enter → 다음 줄 거래일자")
        self.assertIn("isComposing", memo)

    def test_ledger_value_fills_only_untouched_rows(self) -> None:
        self.assertIn("return r.osumAuto === true || (r.gosum === 0 && r.gbsum === 0);", self.src)
        fill = self.src.split("const applyLedgerValue = useCallback(")[1].split("const commitCode = useCallback(")[0]
        self.assertIn("if (r.uid !== uid || !canAutoFillLedger(r)) return r;", fill)
        self.assertIn("osumAuto: true", fill)
        self.assertIn("if (!next.bsumTouched) next.gbsum = next.gssum - next.gosum;", fill)
        self.assertIn("if (patch.gosum !== undefined && !auto) next.osumAuto = false;", self.src,
                      "직접 고친 원장값은 다시 덮지 않는다")

    def test_both_axes_auto_fill(self) -> None:
        customer = self.src.split("export const CUSTOMER_ADJUSTMENT_AXIS")[1].split("};")[0]
        book = self.src.split("export const BOOK_ADJUSTMENT_AXIS")[1].split("};")[0]
        self.assertIn("autoLedgerValue: true", customer)
        self.assertIn("autoLedgerValue: true", book)

    def test_save_stays_explicit(self) -> None:
        """웹은 「저장」을 눌러야 반영된다(레거시는 줄을 떠날 때 자동 Post) — 입력 줄 도입으로 바뀌지 않는다."""
        self.assertIn('{saving ? "저장 중…" : "저장"}', self.src)
        self.assertIn("disabled={saving || !serverId || dirtyCount === 0}", self.src)


if __name__ == "__main__":
    main()
