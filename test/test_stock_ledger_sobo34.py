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

    def _call(self, *, opening=None, ret_seed=None, meta=None, bcode=None):
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


if __name__ == "__main__":
    main()
