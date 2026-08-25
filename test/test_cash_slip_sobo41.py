"""입출금전표(Sobo41 = 입출금전표-거래처, H1_Ssub) 회귀.

요청(2026-08-23): "이 화면이 레거시에서 **일자별 입금 금액 기입용**으로 활용됐다.
이 기능을 입금현황 화면으로 적용하고, 항목을 화면과 맞추고, 입력은 명세서 라인
입력하듯 목록에 항목을 추가하는 방식으로 적용하라."

정본
----
출판 빌드 `한국도서유통출판/출판/Subu41.{dfm,pas}` — 레거시 메뉴 「회계관리 >
입출금전표-거래처」(`Chul.dfm` Menu401 → TSobo41, F41).
분석 원문: `analysis/layout_mappings/Sobo41_cash_slip.md`.

배경 (DEC-186)
--------------
종전 입금 3화면은 `T5_Ssub` 배선인데 라이브에서 도달 가능한 전 서버 0건이었다
(remote_138/153). 실제 데이터는 `H1_Ssub` 에 있다. 본 테스트는 새 배선과
Subu41 고유 규칙(입출금 분리·Scode 축·정렬·잔액 비재계산·hcode 격리)을 고정한다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

import app.services.cash_slip_service as css  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _run(coro):
    return asyncio.run(coro)


# 라이브 교문사(5019) 2026.08.03 실제 행 — 사용자 제공 레거시 스크린샷과 동일.
LIVE_ROWS = [
    {"ID": 1186947, "Idnum": 0, "Gdate": "2026.08.03", "Gubun": "입금", "Scode": "X",
     "Gcode": "3292", "Gname": "#자유서적[파주]", "Tcode": "", "Ocode": "", "Oname": "",
     "Gssum": 48000.0, "Gsumy": 48000.0, "Pubun": "현금", "Gbigo": ""},
    {"ID": 1186946, "Idnum": 0, "Gdate": "2026.08.03", "Gubun": "입금", "Scode": "X",
     "Gcode": "3315", "Gname": "네이버 스마트스토어", "Tcode": "", "Ocode": "", "Oname": "",
     "Gssum": 76290.0, "Gsumy": 17757360.0, "Pubun": "현금", "Gbigo": ""},
]


def _list(rows=None, **kw):
    """execute_query 를 고정하고 목록을 만든다. (sql, params) 도 함께 돌려준다."""
    seen: dict = {}

    async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
        seen["sql"] = sql
        seen["params"] = params
        return list(LIVE_ROWS if rows is None else rows)

    kwargs = {"server_id": "remote_153", "hcode": "5019",
              "date_from": "2026-08-03", "date_to": "2026-08-03"}
    kwargs.update(kw)
    with patch.object(css, "execute_query", new=AsyncMock(side_effect=fake_exec)):
        out = _run(css.list_cash_slips(**kwargs))
    return out, seen


class LiveParityTests(TestCase):
    """§8 라이브 대조 — 레거시 스크린샷 재현."""

    def test_reproduces_legacy_screenshot(self) -> None:
        out, _ = _list()
        self.assertEqual(len(out["rows"]), 2)
        r1, r2 = out["rows"]
        self.assertEqual((r1["gcode"], r1["gname"]), ("3292", "#자유서적[파주]"))
        self.assertEqual((r1["gsumy"], r1["gssum"], r1["gbsum"]), (48000.0, 48000.0, 0.0))
        self.assertEqual((r2["gcode"], r2["gname"]), ("3315", "네이버 스마트스토어"))
        self.assertEqual((r2["gsumy"], r2["gssum"], r2["gbsum"]), (17757360.0, 76290.0, 0.0))

    def test_footer_totals_are_in_and_out_only(self) -> None:
        """하단 합계는 입금·출금 2컬럼만 — 잔액은 합계 대상이 아니다."""
        out, _ = _list()
        self.assertEqual(out["totals"], {"gssum": 124290.0, "gbsum": 0.0})
        self.assertNotIn("gsumy", out["totals"], "잔액을 합산하면 레거시와 어긋난다")


class QueryShapeTests(TestCase):
    """§5 조회 SQL — Subu41.pas Button101Click."""

    def test_reads_h1_ssub_not_t5_ssub(self) -> None:
        """DEC-186 핵심 — T5_Ssub 은 전 서버 0건이라 화면이 항상 비어 있었다."""
        _, seen = _list()
        self.assertIn("FROM H1_Ssub", seen["sql"])
        self.assertNotIn("T5_Ssub", seen["sql"])

    def test_excludes_stock_axis_scodes(self) -> None:
        """`Scode<>'A' and Scode<>'B'` — 재고 축 행 배제(레거시 원문)."""
        _, seen = _list()
        self.assertIn("Scode <> 'A'", seen["sql"])
        self.assertIn("Scode <> 'B'", seen["sql"])

    def test_scope_maps_to_scode(self) -> None:
        """거래구분: 거래처 X / 입고처 Y / 기타 Z (dfm Edit103 ItemIndex)."""
        for label, code in (("거래처", "X"), ("입고처", "Y"), ("기타", "Z")):
            out, seen = _list(scope=label)
            self.assertEqual(out["scode"], code)
            self.assertIn(code, seen["params"])
        # 코드 직접 전달도 허용, 미지정은 거래처(X) — dfm 기본 ItemIndex=0
        self.assertEqual(_list(scope="Y")[0]["scode"], "Y")
        self.assertEqual(_list(scope=None)[0]["scode"], "X")

    def test_unknown_scope_rejected(self) -> None:
        with self.assertRaises(css.CashSlipValidationError):
            _list(scope="없는구분")

    def test_customer_range_applies_only_when_end_code_given(self) -> None:
        """레거시 `if Edit106.Text<>''` — 끝 코드가 없으면 범위 조건 자체가 없다."""
        _, only_start = _list(gcode_from="3000")
        self.assertNotIn("Gcode >=", only_start["sql"], "끝 코드 없이 범위가 걸리면 회귀")
        _, both = _list(gcode_from="3000", gcode_to="3999")
        self.assertIn("Gcode >=", both["sql"])
        self.assertIn("Gcode <=", both["sql"])

    def test_order_switches_on_input_order(self) -> None:
        _, default = _list()
        self.assertIn("ORDER BY Gdate, Gubun, Scode, Gcode", default["sql"])
        _, seq = _list(input_order=True)
        self.assertIn("ORDER BY Gdate, ID", seq["sql"])

    def test_hcode_is_always_bound(self) -> None:
        """H1_Ssub 는 chul_09 4테넌트 공유 — hcode 필터 누락은 테넌트 유출."""
        _, seen = _list()
        self.assertIn("Hcode = %s", seen["sql"])
        self.assertIn("5019", seen["params"])

    def test_date_is_normalized_to_legacy_format(self) -> None:
        _, seen = _list(date_from="2026-08-03", date_to="2026-08-03")
        self.assertIn("2026.08.03", seen["params"])

    def test_row_cap_matches_legacy_limit(self) -> None:
        self.assertEqual(css.SLIP_MAX, 2000, "레거시 LIMIT 0,2000")
        rows = [dict(LIVE_ROWS[0], ID=i) for i in range(css.SLIP_MAX + 5)]
        out, _ = _list(rows=rows)
        self.assertEqual(len(out["rows"]), css.SLIP_MAX)
        self.assertTrue(out["truncated"], "상한 초과는 조용히 자르지 말고 알려야 한다")


class AmountSplitTests(TestCase):
    """§3 입금/출금 분리 — DB 는 금액이 `Gssum` 한 칸이다."""

    def test_deposit_row_puts_amount_in_deposit_column(self) -> None:
        self.assertEqual(css._split_amount("입금", 5000), (5000.0, 0.0))

    def test_non_deposit_row_puts_amount_in_withdrawal_column(self) -> None:
        self.assertEqual(css._split_amount("출금", 5000), (0.0, 5000.0))

    def test_customer_axis_prefers_withdrawal_when_present(self) -> None:
        """Scode X/Z: 출금액이 있으면 출금 (L1345~1351)."""
        self.assertEqual(css._derive_gubun_and_amount(0, 700, "X"), ("출금", 700))
        self.assertEqual(css._derive_gubun_and_amount(500, 0, "X"), ("입금", 500))
        self.assertEqual(css._derive_gubun_and_amount(0, 700, "Z"), ("출금", 700))

    def test_inbound_axis_has_inverted_branch(self) -> None:
        """Scode Y(입고처)만 분기 순서가 뒤집혀 있다 (L1336~1344) — 원문 보존."""
        self.assertEqual(css._derive_gubun_and_amount(500, 0, "Y"), ("입금", 500))
        self.assertEqual(css._derive_gubun_and_amount(0, 700, "Y"), ("출금", 700))

    def test_round_trip_split_then_derive(self) -> None:
        """조회 분리 → 저장 역변환이 원래 (Gubun, Gssum) 로 돌아와야 한다."""
        for gubun, amt in (("입금", 48000), ("출금", 12345)):
            gssum, gbsum = css._split_amount(gubun, amt)
            self.assertEqual(css._derive_gubun_and_amount(gssum, gbsum, "X"), (gubun, amt))


class WriteTests(TestCase):
    """§6 쓰기 — INSERT/UPDATE/DELETE."""

    def _write(self, fn, **kw):
        seen: list = []

        async def fake_tx(server_id, stmts):  # noqa: ANN001
            seen.extend(stmts)
            return 1

        with patch.object(css, "execute_in_transaction", new=AsyncMock(side_effect=fake_tx)):
            out = _run(fn(**kw))
        return out, seen

    def test_insert_targets_h1_ssub_with_hcode(self) -> None:
        _, stmts = self._write(
            css.create_cash_slip, server_id="remote_153", hcode="5019", scope="거래처",
            payload={"gdate": "2026-08-03", "gcode": "3292", "gname": "#자유서적[파주]",
                     "gssum": 48000, "pubun": "현금"})
        sql, vals = stmts[0]
        self.assertIn("INSERT INTO H1_Ssub", sql)
        self.assertIn("5019", vals)
        self.assertIn("입금", vals)
        self.assertIn(48000.0, vals)

    def test_insert_defaults_match_new_record(self) -> None:
        """T4_Sub11NewRecord — Pubun 기본 '현금'."""
        _, stmts = self._write(
            css.create_cash_slip, server_id="remote_153", hcode="5019", scope="거래처",
            payload={"gdate": "2026-08-03", "gcode": "3292", "gssum": 100})
        self.assertIn("현금", stmts[0][1])

    def test_update_and_delete_scope_by_hcode(self) -> None:
        """레거시는 ID(+Gdate)만 쓰지만 공유 테이블이라 Hcode 를 반드시 건다."""
        _, upd = self._write(
            css.update_cash_slip, server_id="remote_153", hcode="5019", row_id=1186947,
            scope="거래처",
            payload={"gdate": "2026-08-03", "gcode": "3292", "gssum": 48000})
        self.assertIn("WHERE ID=%s AND Hcode=%s", upd[0][0])
        _, dele = self._write(
            css.delete_cash_slip, server_id="remote_153", hcode="5019", row_id=1186947)
        self.assertIn("DELETE FROM H1_Ssub WHERE ID=%s AND Hcode=%s", dele[0][0])

    def test_validation_rejects_both_amounts(self) -> None:
        with self.assertRaises(css.CashSlipValidationError):
            self._write(css.create_cash_slip, server_id="remote_153", hcode="5019",
                        payload={"gdate": "2026-08-03", "gcode": "3292",
                                 "gssum": 100, "gbsum": 200})

    def test_validation_requires_customer_and_date(self) -> None:
        for payload in ({"gdate": "", "gcode": "3292", "gssum": 1},
                        {"gdate": "2026-08-03", "gcode": "", "gssum": 1}):
            with self.assertRaises(css.CashSlipValidationError):
                self._write(css.create_cash_slip, server_id="remote_153",
                            hcode="5019", payload=payload)

    def test_validation_rejects_unknown_pubun(self) -> None:
        with self.assertRaises(css.CashSlipValidationError):
            self._write(css.create_cash_slip, server_id="remote_153", hcode="5019",
                        payload={"gdate": "2026-08-03", "gcode": "3292",
                                 "gssum": 1, "pubun": "비트코인"})

    def test_pubun_catalog_matches_dfm_picklist(self) -> None:
        """Subu41.dfm PUBUN PickList (사용자 콤보 스크린샷과 동일)."""
        self.assertEqual(css.PUBUN_CHOICES, ("현금", "어음", "은행", "카드", "공제", "기타"))


class BalanceTests(TestCase):
    def test_balance_is_passed_through_not_recomputed(self) -> None:
        """§4 잔액(Gsumy)은 저장 컬럼 — 조회에서 재계산하면 레거시와 갈린다."""
        rows = [dict(LIVE_ROWS[1])]
        out, _ = _list(rows=rows)
        self.assertEqual(out["rows"][0]["gsumy"], 17757360.0)


class RouteAndScreenTests(TestCase):
    def test_routes_registered(self) -> None:
        from app.routers import settlement  # noqa: PLC0415

        paths = {r.path for r in settlement.router.routes}
        self.assertIn("/api/v1/settlement/cash-slip", paths)
        self.assertIn("/api/v1/settlement/cash-slip/{row_id}", paths)

    def test_route_in_db_smoke_matrix(self) -> None:
        src = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("settlement/cash-slip", src)

    def test_screen_declares_all_ten_grid_columns(self) -> None:
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        for field in ("GDATE", "GCODE", "GNAME", "OCODE", "ONAME",
                      "GSUMY", "GSSUM", "GBSUM", "PUBUN", "GBIGO"):
            self.assertIn(f"Sobo41.DBGrid101.{field}", page, f"컬럼 누락: {field}")
        for label in ("거래일자", "코드", "거래처명", "계정과목", "잔액",
                      "입금", "출금", "결재", "비고", "합계"):
            self.assertIn(label, page, f"라벨 누락: {label}")

    def test_screen_has_inline_row_entry_and_edit(self) -> None:
        """운영 지시 — 입력은 «목록에 행을 추가», 검색된 행도 «그 자리에서 수정».

        레거시 `DBGrid101` 이 인라인 편집 그리드라 신규·수정을 하나의 편집 상태로
        통일했다(`editing.id === DRAFT_ID` 면 신규). 셀 렌더러도 공용이다.
        """
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        self.assertIn("행 추가", page)
        self.assertIn("DRAFT_ID", page, "신규 행 센티넬")
        self.assertIn("formFromRow", page, "기존 행 → 편집 폼 변환(수정 진입)")
        self.assertIn("cashSlipApi.update", page, "행 수정 저장 경로")
        self.assertIn("cashSlipApi.create", page, "신규 행 저장 경로")
        for wid in ("Sobo41.Edit_GDATE", "Sobo41.Edit_GCODE", "Sobo41.Edit_GNAME",
                    "Sobo41.Edit_OCODE", "Sobo41.Edit_ONAME", "Sobo41.Edit_GSSUM",
                    "Sobo41.Edit_GBSUM", "Sobo41.Edit_PUBUN", "Sobo41.Edit_GBIGO"):
            self.assertIn(wid, page, f"인라인 편집 셀 누락: {wid}")

    def test_screen_uses_common_grid_features(self) -> None:
        """운영 요청(2026-08-23) — 페이징·컬럼 순서 변경·정렬 + 제목/합계 줄 고정.

        전부 공통 `DataGrid` 관용으로 얻는다(DEC-091/146/151): sticky 헤더와 sticky
        합계행은 `DataGrid` 가 `totals` 를 받을 때 제공한다.
        """
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        # 손수 짠 <table> 로 되돌아가면 공통 기능이 통째로 사라진다 — 회귀 가드.
        self.assertNotIn("<table", page, "공통 DataGrid 대신 수제 표로 회귀")
        self.assertIn("<DataGrid<CashSlipRow>", page)
        for token, why in (
            ("DataGridPager", "페이징"),
            ("useClientSort", "헤더 클릭 정렬"),
            ("onSortChange", "정렬 콜백"),
            ("onColumnReorder", "컬럼 순서 변경"),
            ("GridColumnSettings", "컬럼 표시/숨김 설정"),
            ("useGridPrefs", "컬럼 너비·순서 저장"),
            ("totals={totals}", "sticky 합계행"),
        ):
            self.assertIn(token, page, f"{why} 누락")

    def test_grid_totals_cover_only_amount_columns(self) -> None:
        """합계행은 입금·출금만 — 잔액을 합산하면 레거시와 어긋난다."""
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        idx = page.index("const totals = useMemo")
        block = page[idx:idx + 320]
        self.assertIn("gssum", block)
        self.assertIn("gbsum", block)
        self.assertNotIn("gsumy", block, "잔액은 합계 대상이 아니다")

    def test_balance_column_is_not_editable(self) -> None:
        """잔액(Gsumy)은 저장 컬럼 — 편집 셀을 주면 레거시와 값이 갈린다(§4)."""
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        self.assertNotIn("Sobo41.Edit_GSUMY", page, "잔액에 편집 입력이 생기면 회귀")

    def test_screen_has_legacy_filter_widgets(self) -> None:
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        for wid in ("Sobo41.Edit101", "Sobo41.Edit102", "Sobo41.Edit103",
                    "Sobo41.Edit104", "Sobo41.Edit106", "Sobo41.CheckBox2",
                    "Sobo41.dxButton1"):
            self.assertIn(wid, page, f"필터 위젯 누락: {wid}")

    def test_superseded_screens_hidden(self) -> None:
        """DEC-186 — T5_Ssub 화면 4종은 사이드바에서 숨긴다(route 는 유지)."""
        src = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        self.assertEqual(src.count('menuId: "ACC-MENU-HIDDEN-SETTLE-CASH-T5"'), 4)
        # 2026-08-24 제품 7699c9d — 레거시 메뉴명 「입출금전표-거래처」에 맞춰 개명.
        self.assertIn('caption: "입출금전표 거래처"', src)

    def test_new_row_scrolls_into_view_and_focuses(self) -> None:
        """행 추가 시 화면이 그 행으로 이동해야 한다 (2026-08-23 사용자 리포트).

        신규 행은 목록 «맨 아래»에 생겨 긴 표에서는 보이지 않는 위치다.
        """
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        self.assertIn("editCodeRef", page, "편집 입력칸 ref")
        self.assertIn("scrollIntoView", page, "신규/수정 행으로 자동 이동")
        self.assertIn("inputRef={editCodeRef}", page, "룩업 입력칸에 ref 연결")
        # 타이핑마다 재스크롤되면 입력이 끊긴다 — 편집 «대상»이 바뀔 때만 이동.
        self.assertIn("}, [editing?.id]);", page)

    def test_edit_actions_reachable_below_grid(self) -> None:
        """표가 가로로 넘치면 행 끝의 저장/취소에 닿지 못한다 — 표 아래에도 노출."""
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        self.assertIn("footerRight={", page)
        idx = page.index("footerRight={")
        block = page[idx:idx + 700]
        self.assertIn("저장", block)
        self.assertIn("취소", block)

    def test_edit_columns_wide_enough_for_inputs(self) -> None:
        """편집 셀이 옆 칸을 침범하지 않을 만큼 컬럼 폭을 잡는다.

        실측(2026-08-23): 거래일자 3분할 DateFieldYMD 내용폭 202px + 셀 패딩 32px.
        좁게 두면 코드 칸을 65px 침범한다(사용자 스크린샷).
        """
        page = (FRONT / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx").read_text(
            encoding="utf-8")
        self.assertIn('legacyId: "Sobo41.DBGrid101.GDATE", minWidthPx: 234,', page)
        # 그리드 셀 룩업 관용 — 긴 버튼 라벨("거래처 검색")은 옆 칸을 침범한다.
        self.assertIn('buttonTitle="검색"', page)
        self.assertNotIn('inputClassName="w-24"\n              inputLegacyId="Sobo41.Edit_GCODE"', page)

    def test_mapping_note_exists(self) -> None:
        self.assertTrue(
            (ROOT / "analysis" / "layout_mappings" / "Sobo41_cash_slip.md").exists(),
            "DEC-028 레이아웃 매핑 노트 필수")


if __name__ == "__main__":
    main()


class DataGridStickyCollisionTests(TestCase):
    """공통 DataGrid — sticky 합계행 vs sticky 하단 페이저 겹침 (2026-08-23).

    합계행(`tfoot td`)은 **스크롤 카드** 바닥에, 하단 페이저는 **뷰포트** 바닥에
    각각 `sticky bottom-0` 이라 같은 자리에서 겹쳤다. 페이저 바가 합계 숫자를 덮는
    스크린샷이 리포트됐다. 합계는 "항상 보여야 하는 값"이고 페이저는 상단에도 있으므로
    **합계행이 있으면 하단 페이저를 sticky 로 띄우지 않는다**.

    `reports/book-sales` 도 totals+pager 조합이라 같은 결함을 공유했다 — 공통 수정.
    """

    GRID = (FRONT / "components" / "data-grid" / "data-grid.tsx")

    def test_bottom_pager_not_sticky_when_totals_present(self) -> None:
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("const stickyBottomPager = showBottomPager && !totals;", src)
        # sticky 클래스는 새 플래그로만 붙어야 한다(구 플래그로 되돌아가면 겹침 재발).
        idx = src.index("sticky bottom-0 z-10 rounded-xl")
        guard = src[max(0, idx - 200):idx]
        self.assertIn("stickyBottomPager", guard)

    def test_totals_row_stays_sticky(self) -> None:
        """합계행 자체의 sticky 는 유지 — 사용자 요구('합계 줄 항상 보이게')."""
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("sticky bottom-0 z-10 border-t border-border bg-muted", src)

    def test_header_row_stays_sticky(self) -> None:
        """제목 줄도 항상 보이게 — DEC-151."""
        src = self.GRID.read_text(encoding="utf-8")
        self.assertIn("sticky top-0 z-10 bg-muted", src)
