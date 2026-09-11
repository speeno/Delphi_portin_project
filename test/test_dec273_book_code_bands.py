"""DEC-273 — 도서코드 «분류별 대역» 자동채번 회귀 가드 (2026-09-11).

교문사 요청서(북이오웍스_거래처_도서 구별코드 260911) + 고객 회신 결정 ①②④⑤:
- 도서분류(G4_Gbun 코드)로 대역을 찾아 «대역 안 숫자 최대값+1». 예외코드는 «없는 번호»로 카운팅.
- 0-패딩 없음(3431 → 3432). 대역 소진 = 빈 값 + BAND_EXHAUSTED. 대역표 없는 테넌트 = 종전 채번.
- 계약 데이터 무결성: 대역 겹침 없음, 예외코드는 자기 대역 안, 예약코드(99999)는 어떤 대역에도 없음,
  번들 사본 == 허브 정본. 서비스 코드에 테넌트 식별자 리터럴 없음(코드 분기 금지).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

import yaml

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import book_code_bands as bcb  # noqa: E402

_KYOMUN_CTX = {"server_id": "remote_153", "hcode": "5019"}


class ContractIntegrityTests(TestCase):
    def setUp(self) -> None:
        bcb.reload_for_tests()

    def test_bundled_copy_matches_hub_source(self) -> None:
        hub = _HUB / "migration" / "contracts" / "book_code_bands.yaml"
        bundled = _BACKEND / "data" / "contracts" / "book_code_bands.yaml"
        self.assertTrue(bundled.is_file(), f"번들 사본 누락: {bundled}")
        h = yaml.safe_load(hub.read_text(encoding="utf-8"))
        b = yaml.safe_load(bundled.read_text(encoding="utf-8"))
        self.assertEqual(h["band_sets"], b["band_sets"])
        self.assertEqual(h["customer_variants"], b["customer_variants"])

    def test_bands_do_not_overlap_and_reserved_outside(self) -> None:
        for sid, bs in bcb.band_sets().items():
            bands = sorted(bs["bands"], key=lambda x: x["lo"])
            for a, b in zip(bands, bands[1:]):
                self.assertLess(a["hi"], b["lo"], f"{sid}: {a['id']} 와 {b['id']} 대역이 겹친다")
            for code in bs["reserved_codes"]:
                n = int(code)
                for band in bands:
                    self.assertFalse(band["lo"] <= n <= band["hi"], f"{sid}: 예약코드 {code} 가 {band['id']} 안")

    def test_ignore_codes_live_inside_their_band_and_are_numeric(self) -> None:
        for sid, bs in bcb.band_sets().items():
            for band in bs["bands"]:
                for code in band["ignore_codes"]:
                    self.assertTrue(code.isdigit(), f"{sid}/{band['id']}: 예외코드 {code} 숫자 아님")
                    self.assertTrue(band["lo"] <= int(code) <= band["hi"], f"{sid}/{band['id']}: {code} 대역 밖")

    def test_each_gubun_maps_to_at_most_one_band(self) -> None:
        bs = bcb.resolve_band_set(_KYOMUN_CTX)
        self.assertIsNotNone(bs)
        for g in range(10001, 10026):
            hits = [b["id"] for b in bs["bands"] if bcb._gubun_in_band(str(g), b)]
            self.assertEqual(len(hits), 1, f"분류 {g} → {hits}")
        for g in ("80000", "89000", "99000", "90001", "90012", "90013", "90014", "99717"):
            hits = [b["id"] for b in bs["bands"] if bcb._gubun_in_band(g, b)]
            self.assertEqual(len(hits), 1, f"분류 {g} → {hits}")

    def test_kyomun_decisions_are_encoded(self) -> None:
        """고객 회신(2026-09-11) 결정 ①②⑤ 가 계약 데이터에 그대로 실려 있다."""
        bs = bcb.resolve_band_set(_KYOMUN_CTX)
        self.assertIsNone(bs["padding"], "결정 ② 패딩 없음")
        team1 = bcb.band_for_gubun(bs, "10001")
        self.assertEqual((team1["lo"], team1["hi"]), (1, 79999))
        self.assertEqual(len(team1["ignore_codes"]), 12, "결정 ① 예외코드 12건")
        self.assertIn("20019", team1["ignore_codes"])
        self.assertEqual((bcb.band_for_gubun(bs, "89000")["lo"], bcb.band_for_gubun(bs, "89000")["hi"]), (89000, 90000))
        self.assertEqual((bcb.band_for_gubun(bs, "90005")["lo"], bcb.band_for_gubun(bs, "90005")["hi"]), (90001, 99000))
        self.assertEqual(bcb.band_for_gubun(bs, "99000")["id"], bcb.band_for_gubun(bs, "80000")["id"])
        self.assertIn("99999", bs["reserved_codes"])

    def test_other_tenants_get_no_band_set(self) -> None:
        self.assertIsNone(bcb.resolve_band_set({"server_id": "remote_138", "hcode": "5019"}))
        self.assertIsNone(bcb.resolve_band_set({"server_id": "remote_153", "hcode": "5056"}))
        self.assertIsNone(bcb.resolve_band_set({}))
        self.assertIsNone(bcb.resolve_band_set(None))

    def test_service_has_no_tenant_literals(self) -> None:
        """코드 분기 금지 — 테넌트·대역 값은 계약 데이터에만."""
        src = (_BACKEND / "app" / "services" / "book_code_bands.py").read_text(encoding="utf-8")
        for needle in ("5019", "remote_153", "chul_09", "교문사", "79999", "90001"):
            self.assertNotIn(needle, src, f"서비스 코드에 테넌트/대역 리터럴 {needle}")

    def test_sql_is_mysql3_safe(self) -> None:
        src = (_BACKEND / "app" / "services" / "book_code_bands.py").read_text(encoding="utf-8")
        self.assertNotRegex(src, re.compile(r"\bCAST\s*\(|\bCASE\s+WHEN\b|COALESCE\s*\(", re.I))
        self.assertNotRegex(src, re.compile(r"FROM\s*\(\s*SELECT", re.I), "파생 테이블 금지(1064)")


class _Db:
    """execute_query 스텁 — MAX 질의와 taken 질의를 구분해 응답한다."""

    def __init__(self, mx, taken=()):
        self.mx = mx
        self.taken = {int(t) for t in taken}
        self.calls: list[tuple[str, tuple]] = []

    async def __call__(self, server_id, sql, params):
        self.calls.append((sql, tuple(params)))
        if "MAX(" in sql:
            return [{"mx": self.mx}]
        # taken: WHERE ... Gcode+0=%s ... Hcode=%s → params[0]
        return [{"Gcode": str(params[0])}] if int(params[0]) in self.taken else []


class AllocationTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        bcb.reload_for_tests()
        self.bs = bcb.resolve_band_set(_KYOMUN_CTX)

    async def _propose(self, gubun, db):
        with patch.object(bcb, "execute_query", db):
            return await bcb.propose_book_code(
                server_id="remote_153", ctx=_KYOMUN_CTX, gubun=gubun, scope_hcode="5019"
            )

    async def test_team1_continues_main_series_without_padding(self) -> None:
        db = _Db(mx=3431)
        r = await self._propose("10002", db)
        self.assertEqual(r["code"], "3432")
        self.assertEqual(r["band"]["id"], "team1-main")
        self.assertIsNone(r["reason"])
        sql, params = db.calls[0]
        self.assertIn("NOT IN", sql, "예외코드는 «없는 번호»로 집계에서 제외")
        self.assertIn("09021", params)
        self.assertIn("20019", params)
        self.assertIn("Hcode=%s", sql)
        self.assertEqual(params[-1], "5019", "hcode 격리")
        self.assertIn("REGEXP", sql)
        self.assertNotIn("CAST", sql.upper())

    async def test_taken_number_is_skipped(self) -> None:
        db = _Db(mx=91786, taken=[91787, 91788])
        r = await self._propose("90007", db)
        self.assertEqual(r["code"], "91789")
        self.assertEqual(r["band"]["id"], "team2-main")

    async def test_empty_band_starts_at_lower_bound(self) -> None:
        db = _Db(mx=None)
        r = await self._propose("90013", db)
        self.assertEqual(r["code"], "99001")

    async def test_max_below_lower_bound_is_floored(self) -> None:
        # 대역 하한 아래 코드만 있는 경우(있을 수 없지만 방어) → 하한부터
        db = _Db(mx=5)
        r = await self._propose("10025", db)
        self.assertEqual(r["code"], "80063")

    async def test_band_exhausted_returns_empty_with_reason(self) -> None:
        db = _Db(mx=90000)
        r = await self._propose("89000", db)
        self.assertEqual(r["code"], "")
        self.assertEqual(r["reason"], "BAND_EXHAUSTED")
        self.assertEqual(r["band"]["id"], "nonsale-standalone-paprika")

    async def test_unknown_gubun_or_other_tenant_falls_back(self) -> None:
        db = _Db(mx=3431)
        self.assertIsNone(await self._propose("12345", db))
        self.assertIsNone(await self._propose("", db))
        with patch.object(bcb, "execute_query", db):
            r = await bcb.propose_book_code(
                server_id="remote_138", ctx={"server_id": "remote_138", "hcode": "5019"}, gubun="10001", scope_hcode="5019"
            )
        self.assertIsNone(r)
        self.assertEqual(db.calls, [], "대역표 없으면 DB 를 건드리지 않는다")

    async def test_nine_prefix_band_is_allowed_for_books(self) -> None:
        """종전 채번의 9-접두 예약은 도서 대역표에는 적용되지 않는다(2팀 90001~ 자동)."""
        db = _Db(mx=None)
        r = await self._propose("90001", db)
        self.assertEqual(r["code"], "90001")


class RouterWiringTests(TestCase):
    def test_next_code_route_passes_gubun_code_to_band_service(self) -> None:
        src = (_BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        self.assertIn('alias="gubunCode"', src)
        self.assertIn("propose_book_code", src)
        self.assertIn('"band": band', src)

    def test_frontend_reproposes_on_category_change(self) -> None:
        page = (_HUB / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)" / "master" / "book" / "new" / "page.tsx")
        src = page.read_text(encoding="utf-8")
        self.assertIn("data.gubun", src)
        self.assertRegex(src, re.compile(r'nextCode\(\s*"book"'))
        api = (_HUB / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "master-api.ts").read_text(encoding="utf-8")
        self.assertIn("gubunCode", api)


if __name__ == "__main__":
    main()
