"""DEC-274 — 재고현황(Sobo34) 도서 마스터에 없는 코드 행 제외 (레거시 SpaceDel 동등, 2026-09-12).

교문사(remote_153/5019) 실측: 도서코드 칸에 '고급'·'11/13'·ISBN 조각 같은 값이 들어간 거래 라인이
69개 코드, Σ전재고 −107. 레거시 Subu34 는 집계 뒤 ``SpaceDel(nSqry,'Gcode','Gname')`` 로 도서명이 빈
행을 지워 474,386 을, 웹은 남겨 474,279 를 보였다. 웹도 같은 규칙으로 빼되 ``excluded_unknown`` 으로
건수·수량·예시 코드를 돌려준다. 메타 조회가 실패하면 제외하지 않는다(전 행 증발 방지).
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

from app.services import inventory_service as inv  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


RAW = [
    {"Bcode": "B1", "Scode": "Y", "Gubun": "입고", "Pubun": "신간", "q": 100},
    {"Bcode": "B1", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 30},
    # 마스터에 없는 «코드» — 도서명 조각이 코드 칸에 들어간 레거시 데이터 오류 행.
    {"Bcode": "고급", "Scode": "X", "Gubun": "출고", "Pubun": "위탁", "q": 5},
    {"Bcode": "11/13", "Scode": "X", "Gubun": "반품", "Pubun": "정품", "q": -1},
]
META = {
    "B1": {"Gcode": "B1", "Gname": "도서1", "Ocode": "", "Gubun": "C1", "Gdang": 10000},
}
OPENING = {"B1": 1000, "고급": -80, "11/13": -27}


def _call(*, meta_raises: bool = False):
    async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
        return list(RAW) if "FROM S1_Ssub" in sql else []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):  # noqa: ANN001
        if "G4_Book" in sql_template:
            if meta_raises:
                raise RuntimeError("G4_Book 조회 실패")
            return [META[k] for k in keys if k in META]
        if "G4_Gbun" in sql_template:
            return [{"Gcode": "C1", "Gname": "분류하나"}]
        return []

    async def fake_stock(server_id, *, hcode, asof, axis_like, bcodes):  # noqa: ANN001
        return {b: OPENING.get(b, 0) for b in bcodes}

    with patch.object(inv, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
         patch.object(inv, "in_clause_lookup", new=AsyncMock(side_effect=fake_in)), \
         patch.object(inv, "_fetch_snapshot_bcodes", new=AsyncMock(return_value=[])), \
         patch.object(inv, "_fetch_return_stock_asof", new=AsyncMock(return_value={})), \
         patch("app.services.reports_service._fetch_stock_asof", new=AsyncMock(side_effect=fake_stock)):
        return _run(inv.get_stock_ledger(
            server_id="remote_153", hcode="5019", bcode=None,
            date_from="2026-09-11", date_to="2026-09-11", scope="ALL",
        ))


class UnknownCodeExclusionTests(TestCase):
    def test_unknown_codes_are_excluded_like_legacy_spacedel(self) -> None:
        out = _call()
        codes = [r["bcode"] for r in out["by_book"]]
        self.assertEqual(codes, ["B1"], "마스터에 없는 코드 행은 원장에서 빠진다")
        self.assertEqual(out["totals"]["gsumx"], 1000, "전재고 합계에 −80/−27 이 섞이면 안 된다")
        self.assertEqual(out["totals"]["goqut"], 30, "출고 합계도 제외 행 몫(5)이 빠진다")
        ex = out["excluded_unknown"]
        self.assertEqual(ex["count"], 2)
        self.assertEqual(ex["gsumx"], -107)
        self.assertEqual(ex["codes"], ["11/13", "고급"])

    def test_no_exclusion_when_meta_lookup_fails(self) -> None:
        """메타 조회 실패 = 이름을 모를 뿐 — 전 행을 지우면 안 된다(페일세이프)."""
        out = _call(meta_raises=True)
        codes = sorted(r["bcode"] for r in out["by_book"])
        self.assertEqual(codes, ["11/13", "B1", "고급"])
        self.assertEqual(out["excluded_unknown"], {"count": 0, "gsumx": 0, "codes": []})

    def test_value_ledger_propagates_exclusion(self) -> None:
        src = (_BACKEND / "app" / "services" / "inventory_service.py").read_text(encoding="utf-8")
        self.assertIn('"excluded_unknown": base.get("excluded_unknown")', src)

    def test_frontend_shows_exclusion_notice(self) -> None:
        page = (_HUB / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "inventory" / "status" / "page.tsx")
        self.assertIn("excluded_unknown", page.read_text(encoding="utf-8"))
        api = (_HUB / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "inquiry-api.ts").read_text(encoding="utf-8")
        self.assertIn("excluded_unknown", api)


if __name__ == "__main__":
    main()
