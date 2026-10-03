"""DEC-372 — 판매 통계 전표 분류: chul_09 계열은 출판 빌드 규칙(Subu61 · Subu67).

요청(교문사, 2026-10-03)
-----------------------
"통계관리 : 자료 매칭이 잘 되어있는지 확인요청드립니다."

실측(교문사 5019, 2026.01~09, 수정 전)
-------------------------------------
- 도서별년말집계 반품 0부 / 0원 ↔ 도서별판매 · 거래처별판매 −12,434부 / −322,577,035원.
- 도서별판매 폐기수량 0 ↔ 폐기현황 −2,158부(2026.01).
원인: 웹은 유통 빌드 Subu61/Subu67 분기만 포팅. chul_09(도서유통-출판 트리)는 반품 · 폐기를 ``Gubun`` 으로 저장한다.

가드
----
- 어느 규칙을 쓸지는 계약(sales_classification.yaml, 허브 정본 == 번들 사본)이 고른다.
- 출판 규칙: 증정 → 출고 → Gubun 폐기 → Pubun 비품/폐기 → Gubun 반품, 입고처(Y) 「이동」 · 입고 중 Pubun 반품 제외.
- 유통 규칙(기본)은 종전 그대로.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from app.services import reports_service as rs
from app.services import sales_classify_profile as scp

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "migration" / "contracts" / "sales_classification.yaml"
BUNDLE = ROOT / "도서물류관리프로그램" / "backend" / "data" / "contracts" / "sales_classification.yaml"
BACK = ROOT / "도서물류관리프로그램" / "backend" / "app"


def _bucket() -> dict[str, Any]:
    return rs._empty_year_end_bucket("도서")  # noqa: SLF001


def _cell() -> dict[str, int]:
    return {k: 0 for k in ("giqut", "gisum", "gbqut", "gpqut", "gjqut", "goqut", "gosum", "gbsum", "gpsum")}


class ContractTests(TestCase):
    def setUp(self) -> None:
        scp.reload_for_tests()

    def tearDown(self) -> None:
        scp.reload_for_tests()

    def test_bundle_copy_matches_hub(self) -> None:
        self.assertEqual(HUB.read_text(encoding="utf-8"), BUNDLE.read_text(encoding="utf-8"))

    def test_profile_by_account_family(self) -> None:
        self.assertEqual(scp.resolve_sales_classify_profile({"account_family": "chul_09"}), "publisher")
        self.assertEqual(scp.resolve_sales_classify_profile({"account_family": "book_07"}), "distributor")
        self.assertEqual(scp.resolve_sales_classify_profile({}), "distributor")
        self.assertEqual(scp.current_sales_classify_profile(), "distributor")

    def test_request_context_is_set_by_user_context(self) -> None:
        deps = (BACK / "core" / "deps.py").read_text(encoding="utf-8")
        self.assertIn("set_request_sales_classify_profile(ctx)", deps)
        router = (BACK / "routers" / "reports.py").read_text(encoding="utf-8")
        self.assertEqual(router.count("classify_profile=resolve_sales_classify_profile(current),"), 2)


class YearEndPublisherRule(TestCase):
    def _run(self, **kw: Any) -> dict[str, Any]:
        b = _bucket()
        rs._classify_sobo67_line_publisher(b, **kw)  # noqa: SLF001
        return b

    def test_return_by_gubun(self) -> None:
        b = self._run(scode="X", gubun="반품", pubun="정품", t01=-3, t02=-3000)
        self.assertEqual((b["gbqut"], b["gbsum"], b["goqut"]), (-3, -3000, 0))
        # 유통 규칙은 같은 행을 버린다(Pubun 이 '반품' 이 아니므로) — 종전 0 의 원인.
        d = _bucket()
        rs._classify_sobo67_line(d, scode="X", gubun="반품", pubun="정품", t01=-3, t02=-3000)  # noqa: SLF001
        self.assertEqual((d["gbqut"], d["gbsum"]), (0, 0))

    def test_gift_before_out_and_scrap_by_gubun(self) -> None:
        self.assertEqual(self._run(scode="X", gubun="출고", pubun="증정", t01=2, t02=0)["gjqut"], 2)
        self.assertEqual(self._run(scode="X", gubun="출고", pubun="위탁", t01=5, t02=500)["goqut"], 5)
        b = self._run(scode="X", gubun="폐기", pubun="정품", t01=-60, t02=0)
        self.assertEqual((b["gpqut"], b["gbqut"], b["gbsum"]), (-60, 0, 0))

    def test_bipum_and_scrap_pubun(self) -> None:
        b = self._run(scode="X", gubun="반품", pubun="비품", t01=-1, t02=-100)
        self.assertEqual((b["gbqut"], b["gbsum"]), (-1, -100))
        x = self._run(scode="X", gubun="반품", pubun="폐기", t01=-1, t02=-100)
        self.assertEqual((x["gpqut"], x["gbsum"], x["gbqut"]), (-1, -100, 0))
        z = self._run(scode="Z", gubun="반품", pubun="폐기", t01=-1, t02=-100)
        self.assertEqual((z["gpqut"], z["gbsum"]), (-1, 0))  # 「폐기금액적용」 해제 기본

    def test_vendor_side(self) -> None:
        self.assertEqual(self._run(scode="Y", gubun="입고", pubun="정품", t01=10, t02=0)["giqut"], 10)
        self.assertEqual(self._run(scode="Y", gubun="입고", pubun="반품", t01=10, t02=0)["giqut"], 0)
        self.assertEqual(self._run(scode="Y", gubun="반품", pubun="정품", t01=4, t02=0)["giqut"], -4)


class BookSalesPublisherRule(TestCase):
    def setUp(self) -> None:
        scp.reload_for_tests()

    def tearDown(self) -> None:
        scp.reload_for_tests()

    def _run(self, **kw: Any) -> dict[str, int]:
        c = _cell()
        rs._apply_book_sales_branch(c, **kw)  # noqa: SLF001
        return c

    def test_default_rule_unchanged(self) -> None:
        c = self._run(scode="X", gubun="폐기", pubun="정품", gsqut=-60, gssum=0)
        self.assertEqual(c["gpqut"], 0)  # 유통 Subu61 — Gubun 폐기 행은 어느 칸에도 안 들어간다
        self.assertEqual(self._run(scode="X", gubun="반품", pubun="정품", gsqut=-3, gssum=-300)["gbqut"], -3)

    def test_publisher_rule_from_request_context(self) -> None:
        self.assertEqual(scp.set_request_sales_classify_profile({"account_family": "chul_09"}), "publisher")
        c = self._run(scode="X", gubun="폐기", pubun="정품", gsqut=-60, gssum=0)
        self.assertEqual(c["gpqut"], -60)
        r = self._run(scode="X", gubun="반품", pubun="정품", gsqut=-3, gssum=-300)
        self.assertEqual((r["gbqut"], r["gbsum"]), (-3, -300))
        self.assertEqual(self._run(scode="Y", gubun="입고", pubun="이동", gsqut=9, gssum=0)["giqut"], 0)
        self.assertEqual(self._run(scode="Y", gubun="입고", pubun="반품", gsqut=9, gssum=0)["giqut"], 0)
        self.assertEqual(self._run(scode="Y", gubun="입고", pubun="정품", gsqut=9, gssum=90)["giqut"], 9)
        self.assertEqual(self._run(scode="W", gubun="출고", pubun="위탁", gsqut=9, gssum=90)["goqut"], 0)


class YearEndAggregateUsesProfile(IsolatedAsyncioTestCase):
    DETAIL = [
        {"bcode": "B1", "gdate": "2026.09.15", "scode": "X", "gubun": "출고", "pubun": "위탁", "gsqut": 10, "gssum": 1000},
        {"bcode": "B1", "gdate": "2026.09.20", "scode": "X", "gubun": "반품", "pubun": "정품", "gsqut": -3, "gssum": -300},
        {"bcode": "B2", "gdate": "2026.09.20", "scode": "X", "gubun": "폐기", "pubun": "정품", "gsqut": -5, "gssum": 0},
    ]

    async def _run(self, profile: str | None) -> tuple[dict[str, Any], str]:
        seen: list[str] = []

        async def fake_exec(server_id: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
            if "S1_Ssub" in sql:
                seen.append(sql)
                return list(self.DETAIL)
            return []

        with patch.object(rs, "execute_query", AsyncMock(side_effect=fake_exec)), \
             patch.object(rs, "in_clause_lookup", AsyncMock(return_value=[])), \
             patch.object(rs, "_attach_meta_soft", AsyncMock(return_value=None)):
            res = await rs.get_year_end_book_aggregate(
                server_id="remote_153", hcode="5019", date_from="2026-09", date_to="2026-09",
                classify_profile=profile, limit=2000,
            )
        return res["totals"], seen[0]

    async def test_publisher_counts_returns_and_scrap(self) -> None:
        totals, sql = await self._run("publisher")
        self.assertEqual((totals["goqut"], totals["gbqut"], totals["gbsum"], totals["gpqut"]), (10, -3, -300, -5))
        self.assertEqual((totals["sale_qty"], totals["sale_amt"]), (7, 700))
        self.assertIn("(s.Scode='Y' AND IFNULL(s.Pubun,'')<>%s) OR s.Scode='X' OR s.Scode='Z'", sql)

    async def test_distributor_default_unchanged(self) -> None:
        scp.reload_for_tests()
        totals, sql = await self._run(None)
        self.assertEqual((totals["goqut"], totals["gbqut"], totals["gpqut"]), (10, 0, 0))
        self.assertNotIn("IFNULL(s.Pubun,'')<>%s", sql)


if __name__ == "__main__":
    main()
