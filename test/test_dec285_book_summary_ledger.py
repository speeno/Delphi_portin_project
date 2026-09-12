"""DEC-285 — 도서별원장총괄(Sobo36_book_summary · 레거시 출판 빌드 Subu36) 회귀 가드 (2026-09-12).

사용자 요청(교문사) 「북이오웍스_원장관리(위러브솔루션 기능 복원)_260912」 6항 —
원장관리 메뉴에 「도서별원장총괄」 복원. 일자는 년월 → **년월일 범위**, 현재고 컬럼 유지.

레거시 정본
  WeLove_FTP/도서유통-출판/MySQL/도서유통/한국도서유통출판/출판/Subu36.pas
    Button101Click L285~293 (G7_Ggeo.Scode 분기)
    Button102Click L295~611 (상단 — Sv_Ghng 스냅샷 + S1_Ssub 델타 + Sg_Csum, SpaceDel L598)
    Button201Click L978~1163 (하단 — 년월 버킷, 본사출고제외 L1017~1019)
  분석 정본: analysis/layout_mappings/Sobo36_book_summary.md

라이브 대사(remote_153 × chul_09_db, hcode 5019, ~2026.09.30):
  입고 5,571,222 / 출고 5,889,678 / 증정 263,794 / 반품 −1,370,884 / 폐기 −26,644 /
  판매금액 73,491,213,362 / 현재재고 473,579 / 레코드 3,020 — 고객 화면 캡처와 전부 일치.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import book_summary_ledger_service as bs  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


SNAP = "2009.12.31"

# Sv_Ghng 스냅샷 1행 — Gosum+Gbsum 이 판매금액 시드.
SV = [{
    "Gcode": "B1", "giqut": 100, "goqut": 40, "gjqut": 5, "gbqut": -7, "gpqut": -1,
    "gosum": 1_000_000, "gbsum": -50_000,
}]

# S1_Ssub 델타 — Subu36 분기표의 대표 조합.
S1 = [
    {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "정품", "q": 30, "amt": 0},
    {"Bcode": "B1", "Scode": "Y", "Gubun": "반품", "Pubun": "반품", "q": 4, "amt": 0},
    {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 20, "amt": 200_000},
    {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "증정", "q": 3, "amt": 0},
    {"Bcode": "B1", "Scode": "X", "Gubun": "반품", "Pubun": "정품", "q": -6, "amt": -60_000},
    {"Bcode": "B2", "Scode": "Z", "Gubun": "폐기", "Pubun": "정품", "q": -2, "amt": -20_000},
    {"Bcode": "B2", "Scode": "X", "Gubun": "이동", "Pubun": "비품", "q": -9, "amt": -90_000},
    # 도서 마스터(G4_Book)에 없는 코드 — SpaceDel 로 제거돼야 한다.
    {"Bcode": "B9", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 999, "amt": 999_999},
]

# Sg_Csum 델타 — 표시 측정치는 없고 행 집합에만 합류.
SG = [{"Gcode": "B3"}]

BOOKS = [
    {"Gcode": "B1", "Gname": "가나다"},
    {"Gcode": "B2", "Gname": "라마바"},
    {"Gcode": "B3", "Gname": "사아자"},
    # B9 는 일부러 없음.
]


def _fake_exec_factory(capture: list[str] | None = None, *, sv=None, s1=None, sg=None):
    async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
        if capture is not None:
            capture.append(sql)
        if "MAX(Gdate)" in sql and "Sv_Ghng" in sql:
            return [{"d": SNAP}]
        if "FROM Sv_Ghng" in sql:
            return list(SV if sv is None else sv)
        if "FROM S1_Ssub" in sql:
            return list(S1 if s1 is None else s1)
        if "FROM Sg_Csum" in sql:
            return list(SG if sg is None else sg)
        return []

    return fake_exec


async def _fake_in_clause(server_id, *, sql_template, keys, prefix_params=(), **kw):  # noqa: ANN001
    ks = set(keys)
    return [b for b in BOOKS if b["Gcode"] in ks]


def _summary(*, capture=None, stock=None, **kw):
    params = dict(
        server_id="remote_153", hcode="5019", bcode_from=None, bcode_to=None,
        date_to="2026-09-30", scope=None,
    )
    params.update(kw)
    from app.services import reports_service as rs

    with patch.object(bs, "execute_query", new=AsyncMock(side_effect=_fake_exec_factory(capture))), \
         patch.object(bs, "in_clause_lookup", new=AsyncMock(side_effect=_fake_in_clause)), \
         patch.object(rs, "_fetch_stock_asof", new=AsyncMock(return_value=dict(stock or {}))):
        return _run(bs.book_summary(**params))


class BookSummaryUpperGridTests(TestCase):
    """상단(검색자료) — Button102Click 1:1."""

    def test_snapshot_plus_delta_branch_table(self) -> None:
        out = _summary()
        rows = {r["bcode"]: r for r in out["rows"]}
        b1 = rows["B1"]
        # 입고 = 스냅샷 100 + Y/입고 30 + Y/(반품·반품) 4
        self.assertEqual(b1["giqut"], 134)
        # 출고 = 스냅샷 40 + X/출고(위탁) 20 — 증정은 출고수량이 아니다.
        self.assertEqual(b1["goqut"], 60)
        self.assertEqual(b1["gjqut"], 8, "증정 = 스냅샷 5 + Pubun=증정 3")
        self.assertEqual(b1["gbqut"], -13, "반품 = 스냅샷 −7 + X/반품 −6 (음수 저장 그대로)")
        # 판매금액 = 스냅샷(Gosum+Gbsum) 950,000 + 출고 200,000 + 증정 0 + 반품 −60,000
        self.assertEqual(b1["gsumx"], 950_000 + 200_000 + 0 - 60_000)

    def test_discard_and_bipum_buckets(self) -> None:
        """Gubun=폐기 → 폐기수량 / Pubun=비품 → 반품수량 (Subu36 L477~514)."""
        out = _summary()
        b2 = {r["bcode"]: r for r in out["rows"]}["B2"]
        self.assertEqual(b2["gpqut"], -2, "Gubun=폐기 는 폐기수량")
        self.assertEqual(b2["gbqut"], -9, "Pubun=비품 은 반품수량 버킷")
        self.assertEqual(b2["gsumx"], -20_000 - 90_000)

    def test_space_del_drops_rows_without_book_name(self) -> None:
        """SpaceDel(nSqry,'Gcode','Gname') — 도서명 빈 행 제거 (Base01.pas L2826).

        라이브(교문사 5019)에서 이 규칙이 없으면 3,089행이 남아 출고/증정/반품 합계가
        레거시 화면과 어긋난다(3,020행 · 5,889,678 이 정본).
        """
        out = _summary()
        self.assertNotIn("B9", {r["bcode"] for r in out["rows"]})
        self.assertEqual(out["excluded_unknown"]["count"], 1)
        self.assertEqual(out["excluded_unknown"]["codes"], ["B9"])
        self.assertNotIn(999_999, [r["gsumx"] for r in out["rows"]])

    def test_row_set_is_union_of_three_sources(self) -> None:
        """행 집합 = Sv_Ghng ∪ S1_Ssub ∪ Sg_Csum (Sg_Csum 전용 도서도 나온다)."""
        out = _summary()
        self.assertEqual({r["bcode"] for r in out["rows"]}, {"B1", "B2", "B3"})
        self.assertEqual(out["total"], 3)

    def test_totals_cover_whole_result(self) -> None:
        out = _summary(stock={"B1": 7, "B2": 3, "B3": -1})
        for key in ("giqut", "goqut", "gjqut", "gbqut", "gpqut", "gsumx", "gsumy"):
            self.assertEqual(
                out["totals"][key], sum(r[key] for r in out["rows"]), f"합계 불일치: {key}"
            )
        self.assertEqual(out["totals"]["gsumy"], 9, "현재재고 합계")

    def test_current_stock_reuses_fetch_stock_asof(self) -> None:
        """현재재고는 재구현하지 않고 DEC-138/283 검증 함수를 그대로 쓴다."""
        from app.services import reports_service as rs

        mock = AsyncMock(return_value={"B1": 11})
        with patch.object(bs, "execute_query", new=AsyncMock(side_effect=_fake_exec_factory())), \
             patch.object(bs, "in_clause_lookup", new=AsyncMock(side_effect=_fake_in_clause)), \
             patch.object(rs, "_fetch_stock_asof", new=mock):
            out = _run(bs.book_summary(
                server_id="remote_153", hcode="5019", bcode_from=None, bcode_to=None,
                date_to="2026-09-30", scope=None,
            ))
        mock.assert_awaited_once()
        kwargs = mock.await_args.kwargs
        self.assertEqual(kwargs["asof"], "2026.09.30", "현재재고 기준일 = 종료일")
        self.assertIsNone(kwargs["axis_like"], "축 미지정이면 전체")
        self.assertEqual(kwargs["hcode"], "5019")
        self.assertEqual({r["bcode"]: r["gsumy"] for r in out["rows"]}["B1"], 11)


class BookSummaryHcodeIsolationTests(TestCase):
    """ACC-DATA-03 — 다중 테넌트 SQL 전부에 Hcode 필터."""

    def test_every_multi_tenant_sql_filters_hcode(self) -> None:
        cap: list[str] = []
        _summary(capture=cap)
        self.assertTrue(cap)
        for sql in cap:
            if any(t in sql for t in ("S1_Ssub", "Sv_Ghng", "Sg_Csum")):
                self.assertIn("Hcode = %s", sql, f"hcode 필터 누락: {sql}")

    def test_months_sql_filters_hcode(self) -> None:
        cap: list[str] = []
        _months(capture=cap)
        self.assertTrue(cap)
        for sql in cap:
            if any(t in sql for t in ("S1_Ssub", "Sg_Csum")):
                self.assertIn("Hcode = %s", sql, f"hcode 필터 누락: {sql}")


class BookSummaryMysql3Tests(TestCase):
    """DEC-033 — MySQL 3.23 호환: 파생 테이블/CAST/CASE/COALESCE 금지."""

    def test_no_forbidden_sql_constructs(self) -> None:
        cap: list[str] = []
        _summary(capture=cap)
        _months(capture=cap)
        for sql in cap:
            up = sql.upper()
            self.assertNotIn("COALESCE", up, f"COALESCE 사용(IFNULL 로): {sql}")
            self.assertNotIn("CASE WHEN", up, f"CASE WHEN 사용: {sql}")
            self.assertNotIn("CAST(", up, f"CAST 사용: {sql}")
            self.assertNotIn("FROM (", up, f"파생 테이블 사용: {sql}")

    def test_source_uses_ifnull_and_chunked_in(self) -> None:
        src = (_BACKEND / "app" / "services" / "book_summary_ledger_service.py").read_text("utf-8")
        self.assertIn("IFNULL(SUM(", src)
        self.assertNotIn("COALESCE(", src)
        self.assertIn("in_clause_lookup", src, "대량 키 조회는 청크 헬퍼로")


# ---------------------------------------------------------------------------
# 하단 — Button201Click
# ---------------------------------------------------------------------------

MONTH_S1 = [
    {"Gdate": "2026.08.03", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 10, "amt": 100_000},
    {"Gdate": "2026.08.20", "Scode": "X", "Gubun": "출고", "Pubun": "증정", "q": 2, "amt": 0},
    {"Gdate": "2026.08.25", "Scode": "X", "Gubun": "반품", "Pubun": "정품", "q": -3, "amt": -30_000},
    {"Gdate": "2026.09.01", "Scode": "Y", "Gubun": "입고", "Pubun": "정품", "q": 50, "amt": 0},
    {"Gdate": "2026.09.02", "Scode": "Z", "Gubun": "폐기", "Pubun": "정품", "q": -4, "amt": -40_000},
]
MONTH_SG = [{"Gdate": "2026.09.10", "q": 7}]


def _months(*, capture=None, **kw):
    params = dict(
        server_id="remote_153", hcode="5019", bcode="B1",
        date_from="2026-08-01", date_to="2026-09-30", scope=None,
    )
    params.update(kw)
    fake = _fake_exec_factory(capture, s1=MONTH_S1, sg=MONTH_SG)
    with patch.object(bs, "execute_query", new=AsyncMock(side_effect=fake)):
        return _run(bs.book_summary_months(**params))


class BookSummaryMonthGridTests(TestCase):
    def test_buckets_by_year_month(self) -> None:
        out = _months()
        self.assertEqual([r["ym"] for r in out["rows"]], ["2026.08", "2026.09"])

    def test_month_branch_table(self) -> None:
        out = _months()
        aug = out["rows"][0]
        self.assertEqual(aug["goqut"], 10)
        self.assertEqual(aug["gjqut"], 2, "증정은 별도 칸 — 출고수량 아님")
        self.assertEqual(aug["gbqut"], -3)
        self.assertEqual(aug["gsqut"], 10 - 3, "판매수량 = 출고 + 반품(음수) — 증정 제외")
        self.assertEqual(aug["gsumy"], 100_000 - 30_000, "하단 gsumy 는 판매금액")
        sep = out["rows"][1]
        self.assertEqual(sep["giqut"], 50, "Scode=Y 입고")
        self.assertEqual(sep["gpqut"], -4, "Gubun=폐기 는 수량만 — 판매수량/금액 제외")
        self.assertEqual(sep["gsqut"], 0)
        self.assertEqual(sep["gsumx"], 7, "하단 gsumx 는 Sg_Csum 변경수량")

    def test_exclude_hq_out_clause_is_legacy_shape(self) -> None:
        """본사출고제외 = ((Scode='X' AND Gcode<>'00001') OR Scode='Y' OR Scode='Z')."""
        cap: list[str] = []
        _months(capture=cap, exclude_hq_out=True)
        s1 = next(s for s in cap if "FROM S1_Ssub" in s)
        self.assertIn("((Scode = %s AND Gcode <> %s) OR Scode = %s OR Scode = %s)", s1)

        cap2: list[str] = []
        _months(capture=cap2, exclude_hq_out=False)
        s1b = next(s for s in cap2 if "FROM S1_Ssub" in s)
        self.assertNotIn("Gcode <> %s", s1b)

    def test_totals_cover_all_months(self) -> None:
        out = _months()
        for key in ("gsumx", "giqut", "goqut", "gjqut", "gbqut", "gpqut", "gsqut", "gsumy"):
            self.assertEqual(out["totals"][key], sum(r[key] for r in out["rows"]), key)

    def test_bcode_required(self) -> None:
        with self.assertRaises(ValueError):
            _months(bcode="")


class BookSummaryRegistrationTests(TestCase):
    """레지스트리·사이드바·스모크 매트릭스 등록 가드."""

    def test_form_registry_entry(self) -> None:
        src = (
            _HUB / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
        ).read_text("utf-8")
        self.assertIn('id: "Sobo36_book_summary"', src)
        self.assertIn('caption: "도서별원장총괄"', src)
        self.assertIn('route: "/ledger/book-summary"', src)
        self.assertIn('formId: "Sobo36_book_summary"', src, "INVENTORY_SIDEBAR_LAYOUT 등록")
        self.assertEqual(src.count('id: "Sobo36_book_summary"'), 1, "id 중복 금지")
        # menuId/권한/phase 는 같은 엔트리 블록 안에 있어야 한다.
        block = src.split('id: "Sobo36_book_summary"', 1)[1].split("},", 1)[0]
        self.assertIn('menuGroup: "inventory"', block)
        self.assertIn('menuId: "ACC-MENU-NAV-03"', block)
        self.assertIn('phase: "phase1"', block)
        self.assertIn('requiredPermission: "report.inventory.read"', block)

    def test_page_exists_with_legacy_ids(self) -> None:
        page = (
            _HUB / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
            / "ledger" / "book-summary" / "page.tsx"
        )
        self.assertTrue(page.exists())
        src = page.read_text("utf-8")
        # dfm 위젯 ID — 하나라도 빠지면 DEC-028 매핑 위반.
        for wid in (
            "Sobo36.Edit101", "Sobo36.Edit102", "Sobo36.Edit104", "Sobo36.Edit106",
            "Sobo36.Button701", "Sobo36.Button702", "Sobo36.CheckBox2",
            "Sobo36.dxButton1", "Sobo36.Label100", "Sobo36.Panel009",
            "Sobo36.DBGrid101", "Sobo36.DBGrid201",
        ):
            self.assertIn(wid, src, f"레거시 위젯 ID 누락: {wid}")
        # 그리드 컬럼 캡션 — dfm Title.Caption 1:1.
        for cap in ("도 서 명", "입고수량", "출고수량", "증정수량", "반품수량",
                    "폐기수량", "판매금액", "현재재고", "년월", "변경수량", "판매수량"):
            self.assertIn(cap, src, f"그리드 컬럼 캡션 누락: {cap}")

    def test_smoke_matrix_registers_new_routes(self) -> None:
        probe = (_HUB / "debug" / "probe_backend_all_servers.py").read_text("utf-8")
        self.assertIn("/api/v1/ledger/book-summary?", probe)
        self.assertIn("/api/v1/ledger/book-summary/months?", probe)

    def test_router_uses_hcode_isolation_helper(self) -> None:
        router = (_BACKEND / "app" / "routers" / "ledger.py").read_text("utf-8")
        block = router.split('@router.get("/book-summary")', 1)[1]
        self.assertIn("enforce_hcode_isolation", block)

    def test_layout_mapping_note_exists(self) -> None:
        note = _HUB / "analysis" / "layout_mappings" / "Sobo36_book_summary.md"
        self.assertTrue(note.exists(), "DEC-028 의무 — 매핑 노트 선행")
        txt = note.read_text("utf-8")
        self.assertIn("Subu36.pas", txt)
        self.assertIn("473,579", txt, "라이브 대사 수치 기록")


if __name__ == "__main__":
    main()
