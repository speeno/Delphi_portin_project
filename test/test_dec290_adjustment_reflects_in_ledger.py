"""DEC-290 — 원장변경 저장분이 거래처거래원장에 나타난다 + 조정 화면 입력 동선 (2026-09-12).

사용자 리포트(스크린샷 5건, 2026-09-12):
  1) 조회 기간 기본값을 «당일~당일» 로.
  2) 「행 추가」·「저장」을 그리드 위가 아니라 **검색 옆 필터 줄**에.
  3) 행을 추가하면 **그 행의 첫 칸(거래일자)** 으로 포커스가 간다.
  4) 적요에서 Enter 를 치면 다음 칸이 없으니 **새 행**으로 이어 간다.
  5) 「내용 저장 후 거래처거래원장에 반영되어야 함」 ← 웹이 Sg_Gsum 기간 행을 안 읽고 있었다.

(5)의 레거시 정본 = ``Subu31.pas`` L646~675:
  Sg_Gsum 을 기간으로 읽어 라벨 ``---적요---``(적요가 비면 ``---장부대조---``), Jubun='YY',
  **금액은 Gbsum 필드** = 그리드의 «반품금액» 칸(``Subu31.dfm`` L605 GBSUM).
  미수 running 이 ``+ rtn_amt`` 이므로 전일미수(``_opening_receivable``, ``+Σ Gbsum``)와 부호가 같다.

일별 원장(``customer_ledger_daily``)과 기간 요약(``customer_ledger_summary``) **둘 다** 읽어야
「기간별미수원장(DEC-286)의 합계」와 「거래처거래원장의 running」 이 서로 어긋나지 않는다.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import customer_txn_ledger_service as svc  # noqa: E402

_SCREEN = (
    _HUB / "도서물류관리프로그램" / "frontend" / "src" / "components" / "ledger"
    / "adjustment-ledger-screen.tsx"
)


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


async def _fake(server_id, sql, params=None):
    return _stub(sql, params)


def _stub(sql: str, params):
    """기간 2026.09.01~2026.09.30, 거래처 1001 — 매출 1건 + 장부대조 2건."""
    if "FROM S1_Ssub" in sql and "Jubun" in sql:
        return [{
            "Gdate": "2026.09.05", "Gubun": "출고", "Pubun": "", "Jubun": "1",
            "Gjisa": "", "Bcode": "B1", "Gbigo": "", "qty": 3, "amt": 30000,
        }]
    if "FROM G4_Book" in sql:
        return [{"Gcode": "B1", "Gname": "국어"}]
    if "FROM Sg_Gsum" in sql:
        if "Gdate >= %s" in sql:            # 기간 내 조정 — 이 결정으로 새로 읽는 것
            return [
                {"Gdate": "2026.09.12", "Gbigo": "잔액대조", "amt": -1000},
                {"Gdate": "2026.09.20", "Gbigo": "", "amt": 500},
            ]
        return [{"b": 0}]                    # 기간 전(전일미수용)
    return []


class AdjustmentRowsAppearInDailyLedger(TestCase):
    def setUp(self) -> None:
        self._p = patch.object(svc, "execute_query", side_effect=_fake)
        self._p.start()
        self.addCleanup(self._p.stop)
        self.res = _run(svc.customer_ledger_daily(
            server_id="remote_x", hcode="5019", gcode="1001",
            date_from="2026-09-01", date_to="2026-09-30",
        ))

    def test_adjustment_rows_are_listed(self) -> None:
        adj = [i for i in self.res["items"] if i["kind"] == 4]
        self.assertEqual(len(adj), 2, "원장변경으로 저장한 2건이 원장에 보여야 한다")

    def test_label_wraps_memo_and_falls_back(self) -> None:
        labels = [i["label"] for i in self.res["items"] if i["kind"] == 4]
        self.assertIn("---잔액대조---", labels)
        self.assertIn("---장부대조---", labels, "적요가 비면 레거시 기본 문구")

    def test_amount_lands_in_return_column_with_sign_kept(self) -> None:
        by = {i["label"]: i for i in self.res["items"] if i["kind"] == 4}
        self.assertEqual(by["---잔액대조---"]["rtn_amt"], -1000)
        self.assertEqual(by["---장부대조---"]["rtn_amt"], 500)
        for row in by.values():
            self.assertEqual((row["out_qty"], row["out_amt"], row["collect"]), (0, 0, 0))
            self.assertEqual(row["jubun"], "YY", "레거시 Subu31 의 전표번호 자리")

    def test_running_balance_moves_by_the_adjustment(self) -> None:
        # 출고 30,000 → 조정 −1,000 → 조정 +500. 일자순이므로 running 이 이 순서로 간다.
        running = [i["balance"] for i in self.res["items"]]
        self.assertEqual(running, [30000, 29000, 29500])
        self.assertEqual(self.res["totals"]["balance"], 29500)
        self.assertEqual(self.res["totals"]["rtn_amt"], -500)

    def test_dates_stay_sorted_with_the_rest(self) -> None:
        dates = [i["gdate"] for i in self.res["items"]]
        self.assertEqual(dates, sorted(dates))


class SummaryReadsTheSamePeriodSource(TestCase):
    def test_summary_query_is_period_bounded_and_scoped(self) -> None:
        src = (_BACKEND / "app" / "services" / "customer_txn_ledger_service.py").read_text(
            encoding="utf-8"
        )
        head, _, tail = src.partition("async def customer_ledger_summary(")
        body = tail.split("\ndef _group_slip_rows")[0]
        self.assertIn("FROM Sg_Gsum", body, "기간 요약도 같은 원천을 읽어야 running 과 안 어긋난다")
        self.assertIn("Scode='X'", body, "거래처 축만")
        self.assertIn('_cell(gc2)["rtn_amt"]', body, "레거시와 같이 반품금액 칸에 더한다")

    def test_daily_helper_is_shared_and_hcode_bound(self) -> None:
        src = (_BACKEND / "app" / "services" / "customer_txn_ledger_service.py").read_text(
            encoding="utf-8"
        )
        head, _, tail = src.partition("async def _adjust_rows(")
        body = tail.split("\ndef _finalize_slip_items")[0]
        self.assertIn("{h_and}", body, "회사(Hcode) 바인딩이 빠지면 다른 회사 조정이 섞인다")
        self.assertIn("Scode='X'", body)

    def test_labelled_rows_survive_finalize(self) -> None:
        rows = [{
            "gdate": "2026.09.12", "jubun": "YY", "gjisa": "", "kind": 4,
            "extra": 0, "out_qty": 0, "out_amt": 0, "rtn_qty": 0, "rtn_amt": -1000,
            "collect": 0, "label": "---잔액대조---", "first_bcode": "", "first_bigo": "",
        }]
        items, _totals, _running = svc._finalize_slip_items(rows, opening=0, names={})
        self.assertEqual(items[0]["label"], "---잔액대조---", "도서명 라벨이 덮어쓰면 안 된다")


class AdjustmentScreenInputFlow(TestCase):
    """화면 4건(기본 기간·버튼 위치·포커스·Enter) 정적 가드."""

    def setUp(self) -> None:
        self.src = _SCREEN.read_text(encoding="utf-8")

    def test_default_period_is_today_to_today(self) -> None:
        block = self.src.split("const defaults = useMemo(")[1].split("}, []);")[0]
        self.assertIn("formatIsoDay(new Date())", block)
        self.assertIn("{ dateFrom: today, dateTo: today }", block)
        self.assertNotIn("-01-01", block, "연초~오늘 기본값은 사용자 요청으로 폐기")

    def test_action_buttons_sit_in_the_filter_row(self) -> None:
        header = self.src.split("<PageHeader")[1].split("</PageHeader>")[0]
        for needle in ("행 추가", '{saving ? "저장 중…" : "저장"}'):
            self.assertIn(needle, header, "검색 옆 필터 줄에 있어야 한다")
        panel = self.src.split("legacyId={`${lf}.Panel002`}")[1].split("/>")[0]
        self.assertNotIn("행 추가", panel, "그리드 헤더에는 남기지 않는다")

    def test_new_row_takes_focus_at_its_first_cell(self) -> None:
        block = self.src.split("const focusLastRowStart = useCallback(")[1].split("}, []);")[0]
        self.assertIn("requestAnimationFrame", block, "행이 그려진 다음 프레임에 잡는다")
        self.assertIn("tbody tr", block)
        self.assertIn("focus()", block)
        add = self.src.split("const addRow = useCallback(")[1].split("}, [dateTo")[0]
        self.assertIn("focusLastRowStart();", add)

    def test_enter_on_memo_starts_a_new_row(self) -> None:
        block = self.src.split("patchRow(row.uid, { gbigo: e.target.value })")[1].split("/>")[0]
        self.assertIn("isComposing", block, "한글 조합 중 Enter 는 무시한다")
        self.assertIn("addRow();", block)
        self.assertIn("document.activeElement === before", block, "다음 칸이 있으면 그리로 간다")

    def test_no_internal_table_names_on_screen(self) -> None:
        # 주석(레거시 근거)은 남겨도 되고, **그려지는 문자열**에만 없어야 한다.
        code = re.sub(r"/\*.*?\*/", "", self.src, flags=re.S)
        code = re.sub(r"(?m)^\s*//.*$", "", code)
        for needle in ("Sg_Gsum", "Sg_Csum", "Scode=", "legacySource"):
            self.assertNotIn(needle, code, "내부 테이블명 노출 금지(사용자 2026-09-12)")


if __name__ == "__main__":
    main()
