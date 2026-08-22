"""기간별재고원장(Sobo34) 백엔드 — 분류/도서 2단 + 재고(반) 회귀.

요청(2026-08-22): "원장관리의 재고현황을 레거시 화면에 맞춰 구성" →
"레거시 그대로 분류/도서 2단으로, 재고(반) 포함해서 진행".

정본
----
출판 빌드 `한국도서유통/출판/MySQL/Subu34.pas` Button102Click.
분석 원문: `analysis/layout_mappings/Sobo34_inventory_ledger.md`.

- 누적 분기표: L415~484
- 마감 산식:   L1147~1159
    GsumY = GsumX + 입고 − 출고 − 증정 + 반입 + Gbsum + 변경 − (Gosum≠0 이면 Gosum)
    Gssum = 스냅샷Gbqut − 반입 + Gjsum + Gosum
- 2단 구조:    L1166~1204 — 하단=도서(Ocode 병합), 상단=분류(G4_Book.Gubun → G4_Gbun.Gname)

전·현재고 산식은 **재구현하지 않는다** — DEC-138 에서 Tong04 TTong40 을 1:1 포팅하고
라이브 대사까지 끝낸 `reports_service._fetch_stock_asof` 를 재사용한다. 본 테스트는
그 재사용과 Subu34 고유 부분(분기표·마감 산식·2단 롤업)을 고정한다.

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

import app.services.inventory_service as inv  # noqa: E402


class Subu34BranchTableTests(TestCase):
    """§분기표 — Subu34.pas L415~484 1:1."""

    def _apply(self, scode, gubun, pubun, q=10):
        b = inv._blank_stock_bucket()
        inv._apply_subu34_branch(b, scode, gubun, pubun, q)
        return {k: v for k, v in b.items() if v}

    def test_inbound_branches(self) -> None:
        self.assertEqual(self._apply("Y", "입고", ""), {"giqut": 10})
        self.assertEqual(self._apply("Y", "반품", "반품"), {"giqut": 10}, "반품/반품은 입고")
        self.assertEqual(self._apply("Y", "출고", "반품"), {"gisum": 10}, "그 외 반품은 반입")
        self.assertEqual(self._apply("Y", "입고", "이동"), {"gpsum": 10}, "이동은 변경")

    def test_outbound_branches(self) -> None:
        self.assertEqual(self._apply("X", "출고", ""), {"goqut": 10})
        self.assertEqual(self._apply("X", "출고", "증정"), {"gjqut": 10}, "증정이 출고보다 우선")
        self.assertEqual(self._apply("X", "반품", ""), {"gbqut": 10, "gbsum": -10})

    def test_scrap_branches(self) -> None:
        self.assertEqual(self._apply("X", "폐기", ""), {"gpqut": 10, "gbsum": 10})
        self.assertEqual(self._apply("X", "폐기", "비품"), {"gpqut": 10, "gjsum": 10})
        # Gubun 이 폐기가 아니면서 Pubun 만 비품/폐기인 경로
        self.assertEqual(self._apply("X", "", "비품"), {"gbqut": 10, "gjsum": -10})
        self.assertEqual(self._apply("X", "", "폐기"), {"gpqut": 10, "gjsum": 10})

    def test_unknown_combo_is_noop(self) -> None:
        self.assertEqual(self._apply("Y", "기타", "기타"), {})
        self.assertEqual(self._apply("X", "기타", "기타"), {})


class ShiftGdateTests(TestCase):
    def test_previous_day_across_month(self) -> None:
        self.assertEqual(inv._shift_gdate("2026.08.01", -1), "2026.07.31")
        self.assertEqual(inv._shift_gdate("2026-03-01", -1), "2026.02.28")

    def test_malformed_input_is_passed_through(self) -> None:
        self.assertEqual(inv._shift_gdate("", -1), "")


def _run(coro):
    return asyncio.run(coro)


class StockLedgerAggregationTests(TestCase):
    """§마감 산식 + 2단 롤업."""

    RAW = [
        # 도서 B1 (분류 C1): 입고 100, 출고 30, 증정 5, 반입 7, 변경 3
        {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "", "q": 100},
        {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "", "q": 30},
        {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "증정", "q": 5},
        {"Bcode": "B1", "Scode": "Y", "Gubun": "출고", "Pubun": "반품", "q": 7},
        {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "이동", "q": 3},
        # 도서 B2 (분류 C1): 입고 50
        {"Bcode": "B2", "Scode": "Y", "Gubun": "입고", "Pubun": "", "q": 50},
        # 도서 B3 (분류 C2): 반품 20
        {"Bcode": "B3", "Scode": "X", "Gubun": "반품", "Pubun": "", "q": 20},
    ]
    META = {
        "B1": {"Gcode": "B1", "Gname": "도서1", "Ocode": "", "Gubun": "C1", "Gdang": 10000},
        "B2": {"Gcode": "B2", "Gname": "도서2", "Ocode": "", "Gubun": "C1", "Gdang": 8000},
        "B3": {"Gcode": "B3", "Gname": "도서3", "Ocode": "", "Gubun": "C2", "Gdang": 5000},
    }

    def _call(self, *, opening=None, ret_seed=None, meta=None, bcode=None,
             snapshot_bcodes=None):
        meta = meta or self.META

        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            return list(self.RAW) if "FROM S1_Ssub" in sql else []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):  # noqa: ANN001
            if "G4_Book" in sql_template:
                return [meta[k] for k in keys if k in meta]
            if "G4_Gbun" in sql_template:
                return [{"Gcode": "C1", "Gname": "분류하나"}, {"Gcode": "C2", "Gname": "분류둘"}]
            return []

        async def fake_stock(server_id, *, hcode, asof, axis_like, bcodes):  # noqa: ANN001
            return dict(opening or {})

        async def fake_ret(server_id, *, hcode, asof, bcodes):  # noqa: ANN001
            return dict(ret_seed or {})

        with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
             patch.object(inv, "in_clause_lookup", new=AsyncMock(side_effect=fake_in)), \
             patch.object(inv, "_fetch_snapshot_bcodes",
                          new=AsyncMock(return_value=list(snapshot_bcodes or []))), \
             patch.object(inv, "_fetch_return_stock_asof", new=AsyncMock(side_effect=fake_ret)), \
             patch("app.services.reports_service._fetch_stock_asof",
                   new=AsyncMock(side_effect=fake_stock)):
            return _run(inv.get_stock_ledger(
                server_id="remote_153", hcode="5019", bcode=bcode,
                date_from="2026-08-01", date_to="2026-08-31", scope="ALL",
            ))

    def test_book_measures_follow_branch_table(self) -> None:
        out = self._call()
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["giqut"], 100)
        self.assertEqual(b1["goqut"], 30)
        self.assertEqual(b1["gjqut"], 5)
        self.assertEqual(b1["gisum"], 7, "반입")
        self.assertEqual(b1["gpsum"], 3, "변경")

    def test_closing_stock_formula(self) -> None:
        """현재고 = 전재고 + 입고 − 출고 − 증정 + 반입 + Gbsum + 변경."""
        out = self._call(opening={"B1": 1000})
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["gsumx"], 1000, "전재고")
        self.assertEqual(b1["gsumy"], 1000 + 100 - 30 - 5 + 7 + 0 + 3)

    def test_return_stock_formula(self) -> None:
        """재고(반) = 스냅샷Gbqut − 반입 + Gjsum + Gosum."""
        out = self._call(ret_seed={"B1": 40})
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["gssum"], 40 - 7 + 0 + 0)

    def test_opening_uses_day_before_period_start(self) -> None:
        seen: dict = {}

        async def capture(server_id, *, hcode, asof, axis_like, bcodes):  # noqa: ANN001
            seen["asof"] = asof
            return {}

        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            return list(self.RAW) if "FROM S1_Ssub" in sql else []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):  # noqa: ANN001
            return [self.META[k] for k in keys if k in self.META] if "G4_Book" in sql_template else []

        with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
             patch.object(inv, "in_clause_lookup", new=AsyncMock(side_effect=fake_in)), \
             patch.object(inv, "_fetch_return_stock_asof", new=AsyncMock(return_value={})), \
             patch("app.services.reports_service._fetch_stock_asof",
                   new=AsyncMock(side_effect=capture)):
            out = _run(inv.get_stock_ledger(
                server_id="remote_153", hcode="5019", bcode=None,
                date_from="2026-08-01", date_to="2026-08-31", scope="ALL"))
        self.assertEqual(seen["asof"], "2026.07.31", "전재고는 기간 시작 **직전** 시점")
        self.assertEqual(out["opening_asof"], "2026.07.31")

    def test_class_rollup_sums_member_books(self) -> None:
        out = self._call(opening={"B1": 1000, "B2": 200})
        by_class = {c["class_code"]: c for c in out["by_class"]}
        self.assertEqual(set(by_class), {"C1", "C2"})
        self.assertEqual(by_class["C1"]["gname"], "분류하나", "이름은 G4_Gbun")
        self.assertEqual(by_class["C1"]["giqut"], 150, "B1 100 + B2 50")
        self.assertEqual(by_class["C1"]["gsumx"], 1200)
        self.assertEqual(by_class["C2"]["gbqut"], 20)

    def test_ocode_merges_into_representative_book(self) -> None:
        """G4_Book.Ocode 가 있으면 대표 도서로 합친다 (Subu34 L385~412)."""
        meta = dict(self.META)
        meta["B2"] = {**meta["B2"], "Ocode": "B1"}
        out = self._call(meta=meta)
        codes = {r["bcode"] for r in out["by_book"]}
        self.assertNotIn("B2", codes, "대표 도서(B1)로 병합돼야 한다")
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["giqut"], 150, "B1 100 + B2 50 합산")

    def test_search_matches_code_or_name(self) -> None:
        """검색 한 칸 — 코드/도서명 부분일치, 미지정 시 전체(운영 요청)."""
        self.assertEqual(len(self._call()["by_book"]), 3, "미지정 = 전체")
        self.assertEqual(
            [r["bcode"] for r in self._call(bcode="B3")["by_book"]], ["B3"])
        self.assertEqual(
            [r["bcode"] for r in self._call(bcode="도서2")["by_book"]], ["B2"],
            "도서명으로도 찾을 수 있어야 한다")

    def test_snapshot_books_appear_without_period_movement(self) -> None:
        """기간 거래가 없어도 재고를 들고 있는 도서는 행에 남는다 (Subu34 L1046~1055).

        2026-08-22 리포트: "시작일=기준일 로 맞추면 분류 수가 3개로 급감" —
        행 집합을 S1_Ssub 기간 거래로만 시드해 재고 보유 도서가 통째로 빠졌던 회귀.
        """
        meta = dict(self.META)
        meta["B9"] = {"Gcode": "B9", "Gname": "무거래도서", "Ocode": "",
                      "Gubun": "C3", "Gdang": 3000}
        out = self._call(meta=meta, snapshot_bcodes=["B9"], opening={"B9": 55})
        b9 = next((r for r in out["by_book"] if r["bcode"] == "B9"), None)
        self.assertIsNotNone(b9, "스냅샷 도서가 행에서 사라졌다")
        self.assertEqual(b9["gsumx"], 55, "전재고는 살아 있어야 한다")
        self.assertEqual(b9["giqut"], 0, "기간 거래는 0")
        self.assertEqual(b9["gsumy"], 55, "현재고 = 전재고 + 증감 0")
        self.assertIn("C3", {c["class_code"] for c in out["by_class"]},
                      "그 도서의 분류도 상단에 나와야 한다")

    def test_totals_match_book_sum(self) -> None:
        out = self._call(opening={"B1": 1000, "B2": 200})
        self.assertEqual(out["totals"]["giqut"], 150)
        self.assertEqual(
            out["totals"]["gsumy"], sum(r["gsumy"] for r in out["by_book"]))


class StockLedgerEndpointTests(TestCase):
    """라우터 배선 — 멀티테넌트 격리 포함."""

    def test_router_exposes_stock_ledger(self) -> None:
        src = (BACKEND / "app" / "routers" / "inventory.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/stock-ledger")', src)
        self.assertIn("inventory_service.get_stock_ledger", src)
        # 비-슈퍼는 로그인 출판사만 — 공유 DB 테넌트 격리(DEC-136 계열).
        i = src.index('@router.get("/stock-ledger")')
        block = src[i : i + 1800]
        self.assertIn("enforce_hcode_isolation(hcode, current)", block)



class SnapshotSeedQueryTests(TestCase):
    """§행 시드 쿼리 자체 — 컬럼/스코프 (DEC-183).

    `_fetch_snapshot_bcodes` 는 예외를 삼키고 빈 목록을 돌려주므로, 컬럼명이 틀리면
    수정이 **조용히 무효화**된다(증상은 원래 버그와 동일). 그래서 쿼리 문자열을 고정한다.
    검증 기준은 `reports_service._fetch_stock_asof` — 라이브 대사를 마친 동일 테이블 접근.
    """

    def _capture(self, **kw):
        seen: list[tuple] = []

        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            seen.append((sql, params))
            return [{"d": "2026.07.31"}] if "MAX(Gdate)" in sql else [{"Gcode": "B7"}]

        with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)):
            out = _run(inv._fetch_snapshot_bcodes(
                "remote_153", hcode="5019", asof="2026.07.31", **kw))
        return out, seen

    def test_columns_match_verified_stock_reader(self) -> None:
        out, seen = self._capture()
        self.assertEqual(out, ["B7"])
        self.assertIn("MAX(Gdate)", seen[0][0])
        self.assertIn("FROM Sv_Ghng", seen[1][0])
        self.assertIn("Gcode", seen[1][0], "도서코드 컬럼은 Gcode (Sv_Ghng)")
        self.assertIn("Gdate = %s", seen[1][0], "스냅샷 일자 고정")
        self.assertIn("Hcode = %s", seen[1][0], "테넌트 격리 필수")

    def test_scope_filters_on_scode(self) -> None:
        """본사/창고 축은 Sv_Ghng.Scode — 빠지면 반대 축 도서가 0 행으로 딸려 나온다."""
        _, seen = self._capture(axis_like="%A%")
        self.assertIn("Scode LIKE %s", seen[1][0])
        self.assertIn("%A%", seen[1][1])

    def test_no_snapshot_returns_empty(self) -> None:
        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            return [{"d": None}]

        with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)):
            self.assertEqual(
                _run(inv._fetch_snapshot_bcodes("r", hcode="5019", asof="2026.07.31")), [])

    def test_missing_table_degrades_quietly(self) -> None:
        """Sv_Ghng 부재 테넌트 — 예외를 던지지 않고 기간 거래만으로 진행한다."""
        with patch.object(inv, "execute_query",
                          new=AsyncMock(side_effect=RuntimeError("no such table"))):
            self.assertEqual(
                _run(inv._fetch_snapshot_bcodes("r", hcode="5019", asof="2026.07.31")), [])

if __name__ == "__main__":
    main()
