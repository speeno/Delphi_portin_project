"""DEC-137 — 원장 축 교정(Gcode=거래처/Hcode=출판사) + 도서별판매 0권 제외 + 메뉴 통합.

배경(2026-08-11 교문사-경리부 요청, 스크린샷 5매):
1. 도서별판매 — 기간 검색 시 해당 기간 판매 0권(전 컬럼 0) 도서까지 전부 노출.
2. 거래처원장 — "조회" 시 HCODE_FORBIDDEN 403. 뿌리 원인은 축 오배선: 모던 포트가
   ``customerCode`` 를 ``S1_Ssub.Hcode`` 에 바인딩했으나, 레거시 정본은 전 빌드에서
   **Gcode=거래처 / Hcode=출판사** (총판 Subu31 ``Gcode = Edit103``, 출판 Subu31
   ``Gcode=거래처 and Hcode=Hnnnn``; Subu32 Edit107 라벨 = '출판사명').
3. 재고관리·재고원장 그룹 통합 + 수불 메뉴 3개 → 도서별수불원장 1개.

규칙(DEC-137):
- 거래처원장/통합: 거래처 축 = Gcode. 격리 계정은 ``resolve_g7_ggeo_list_scope`` 가
  산출한 자사 Hcode 를 추가 강제(403 아님), 총판/슈퍼는 Hcode 절 없음(전체 출판사).
- 도서별판매: 기간 내 전 측정치 0 인 도서 행 제외(반품 등 하나라도 비0 이면 유지).
- 메뉴: (구)ledger 그룹 → inventory 통합, 원장 폼은 폼 단위 NAV-03 게이트 유지,
  Sobo33_ledger/Sobo33_1_ledger 는 레이아웃 화이트리스트에서 감춤(Sobo15 선례).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.core.hcode_isolation import SCOPE_DENIED_HCODE  # noqa: E402
from app.routers import ledger as ledger_router  # noqa: E402
from app.services import customer_ledger_service as cls_svc  # noqa: E402
from app.services import reports_service as rpt_svc  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _ctx(**kw) -> dict:
    base = {"user_id": "u1", "role": "operator", "permissions": []}
    base.update(kw)
    return base


def _kyomunsa_ctx() -> dict:
    """공유 좌표(remote_153×chul_09)의 격리 계정 — DEC-136 매트릭스와 동일."""
    return _ctx(server_id="remote_153", account_family="chul_09",
                account_type="", hcode="5019")


def _distributor_ctx() -> dict:
    """단일 테넌트 좌표 운영(T1) — 전체 합산 보존(DEC-085/090)."""
    return _ctx(server_id="remote_155", account_family="chul_09",
                account_type="T1", hcode="7777")


# ---------------------------------------------------------------
# 1) 도서별판매 — 기간 내 전 측정치 0 도서 제외
# ---------------------------------------------------------------


class BookSalesZeroRowTests(IsolatedAsyncioTestCase):
    async def _run(self, s1_rows):
        async def fake_execute(server_id, sql, params=()):
            low = sql.lower()
            if "from s1_ssub" in low:
                return s1_rows
            if "from sg_csum" in low:
                return []
            return []

        async def fake_in_clause(server_id, *, sql_template, keys, prefix_params=()):
            return [{"bcode": k, "gname": f"도서{k}", "gdang": 1000} for k in keys]

        with patch.object(rpt_svc, "execute_query", fake_execute), \
                patch.object(rpt_svc, "in_clause_lookup", fake_in_clause):
            return await rpt_svc.get_book_sales(
                server_id="remote_153", hcode="5019",
                date_from="2026.01.01", date_to="2026.08.10",
            )

    async def test_all_zero_book_excluded(self) -> None:
        rows = [
            # A: 출고 5 → 유지
            {"Bcode": "A", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gdate": "2026.01.14", "Gsqut": 5, "Gssum": 17000},
            # B: 분기표 밖(이동) → 전 측정치 0 → 제외 (스크린샷 1 의 80041 케이스)
            {"Bcode": "B", "Scode": "X", "Gubun": "이동", "Pubun": "",
             "Gdate": "2026.01.31", "Gsqut": 3, "Gssum": 0},
            # C: 반품만 -1 → 측정치 비0 → 유지 (제외 규칙이 과도하지 않음을 가드)
            {"Bcode": "C", "Scode": "X", "Gubun": "반품", "Pubun": "",
             "Gdate": "2026.01.21", "Gsqut": -1, "Gssum": 0},
        ]
        res = await self._run(rows)
        codes = [r["gcode"] for r in res["rows"]]
        self.assertIn("A", codes)
        self.assertIn("C", codes)
        self.assertNotIn("B", codes, "전 컬럼 0 도서가 목록에 남음 — DEC-137 회귀")
        self.assertEqual(res["total"], 2)

    async def test_zero_quantity_rows_only_excluded(self) -> None:
        rows = [
            {"Bcode": "Z", "Scode": "X", "Gubun": "출고", "Pubun": "",
             "Gdate": "2026.02.01", "Gsqut": 0, "Gssum": 0},
        ]
        res = await self._run(rows)
        self.assertEqual(res["rows"], [])
        self.assertEqual(res["total"], 0)


# ---------------------------------------------------------------
# 2) 거래처원장(단일) — Gcode=거래처 + 격리 계정 Hcode=자사
# ---------------------------------------------------------------


class CustomerLedgerAxisTests(IsolatedAsyncioTestCase):
    def _capture_db(self, captured):
        async def fake_execute(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            low = sql.lower()
            if "sv_ghng" in low:
                return [{"opening_date": "2026.03.31"}]
            if "count(distinct gdate)" in low:
                return [{"cnt": 0}]
            if "from sb_csum" in low:
                return [{"qty": 7}]
            return []
        return fake_execute

    async def test_isolated_account_scoped_both_axes(self) -> None:
        captured: list = []
        async def fake_cols(server_id, table):
            return {"gcode", "hcode", "gsqut"}
        with patch.object(cls_svc, "execute_query", self._capture_db(captured)), \
                patch.object(cls_svc, "table_columns", fake_cols):
            await cls_svc.get_customer_ledger(
                server_id="remote_153", customer_code="00227",
                publisher_scope_hcode="5019",
                date_from="2026.01.01", date_to="2026.08.10",
            )
        count_sql, count_params = next(
            (s, p) for s, p in captured if "count(distinct gdate)" in s.lower()
        )
        self.assertIn("Gcode = %s", count_sql)
        self.assertIn("Hcode = %s", count_sql)
        self.assertIn("00227", count_params)
        self.assertIn("5019", count_params)
        # 이월 기준일(Sv_Ghng)도 자사 Hcode 스코프.
        ghng_sql, ghng_params = next(
            (s, p) for s, p in captured if "sv_ghng" in s.lower()
        )
        self.assertIn("Hcode = %s", ghng_sql)
        self.assertIn("5019", ghng_params)
        # Sb_Csum 이월 — Hcode 컬럼 보유 테넌트는 스코프 SQL.
        csum_sql, csum_params = next(
            (s, p) for s, p in captured if "sb_csum" in s.lower()
        )
        self.assertIn("Hcode = %s", csum_sql)
        self.assertEqual(("00227", "5019"), csum_params)

    async def test_distributor_no_hcode_clause(self) -> None:
        captured: list = []
        async def fake_cols(server_id, table):
            return {"gcode", "gsqut"}
        with patch.object(cls_svc, "execute_query", self._capture_db(captured)), \
                patch.object(cls_svc, "table_columns", fake_cols):
            await cls_svc.get_customer_ledger(
                server_id="remote_155", customer_code="00227",
                publisher_scope_hcode=None,
                date_from="2026.01.01", date_to="2026.08.10",
            )
        count_sql, count_params = next(
            (s, p) for s, p in captured if "count(distinct gdate)" in s.lower()
        )
        self.assertIn("Gcode = %s", count_sql)
        self.assertNotIn("Hcode = %s", count_sql)
        self.assertIn("00227", count_params)

    async def test_scope_denied_sentinel_yields_zero_rows_not_403(self) -> None:
        # sentinel 은 실존 불가 코드 — SQL 로 흘러 0건이 정상 경로(예외 없음).
        captured: list = []
        async def fake_cols(server_id, table):
            return set()
        with patch.object(cls_svc, "execute_query", self._capture_db(captured)), \
                patch.object(cls_svc, "table_columns", fake_cols):
            res = await cls_svc.get_customer_ledger(
                server_id="remote_153", customer_code="00227",
                publisher_scope_hcode=SCOPE_DENIED_HCODE,
                date_from="2026.01.01", date_to="2026.08.10",
            )
        self.assertEqual(res["rows"], [])
        count_params = next(
            p for s, p in captured if "count(distinct gdate)" in s.lower()
        )
        self.assertIn(SCOPE_DENIED_HCODE, count_params)


# ---------------------------------------------------------------
# 3) 통합 거래처원장 — Gcode 축 + 패턴은 거래처 LIKE
# ---------------------------------------------------------------


class IntegratedLedgerAxisTests(IsolatedAsyncioTestCase):
    async def test_axes_and_pattern(self) -> None:
        captured: list = []

        async def fake_execute(server_id, sql, params=()):
            captured.append((sql, tuple(params)))
            low = sql.lower()
            if "sv_ghng" in low:
                return [{"opening_date": "2026.03.31"}]
            if "count(distinct gcode)" in low:
                return [{"cnt": 0}]
            return []

        with patch.object(cls_svc, "execute_query", fake_execute):
            res = await cls_svc.get_integrated_customer_ledger(
                server_id="remote_153",
                date_from="2026.01.01", date_to="2026.08.10",
                customer_pattern="22", scope="ALL", scope_hcode="5019",
            )
        self.assertEqual(res["rows"], [])
        count_sql, count_params = next(
            (s, p) for s, p in captured if "count(distinct" in s.lower()
        )
        self.assertIn("COUNT(DISTINCT Gcode)", count_sql)
        self.assertIn("Hcode = %s", count_sql)
        self.assertIn("Gcode LIKE %s", count_sql)
        self.assertIn("5019", count_params)
        self.assertIn("%22%", count_params)


# ---------------------------------------------------------------
# 4) 라우터 배선 — 격리 계정 403 제거 + 스코프 전달
# ---------------------------------------------------------------


_EMPTY_SINGLE = {
    "opening_date": None,
    "rows": [],
    "summary": {"opening_qty": 0, "total_in": 0, "total_out": 0, "closing_qty": 0},
    "page": {"limit": 100, "offset": 0, "total": 0, "has_more": False},
    "truncated": False,
}

_EMPTY_INTEGRATED = {
    "opening_date": None,
    "rows": [],
    "page": {"limit": 100, "offset": 0, "total": 0, "has_more": False},
    "truncated": False,
}


class RouterWiringTests(IsolatedAsyncioTestCase):
    async def test_isolated_account_no_403_and_scope_passed(self) -> None:
        seen: dict = {}

        async def fake_svc(**kw):
            seen.update(kw)
            return dict(_EMPTY_SINGLE)

        with patch.object(cls_svc, "get_customer_ledger", fake_svc):
            await ledger_router.get_customer_ledger(
                server_id="remote_153", customer_code="00227",
                date_from="2026.01.01", date_to="2026.08.10",
                bcode_from=None, bcode_to=None, scope="ALL",
                sort_by=None, sort_dir=None, limit=100, offset=0,
                current=_kyomunsa_ctx(),
            )
        # 종전: enforce_hcode_identity("00227") → 403. 현재: 거래처 코드는 그대로,
        # 격리는 출판사 축 스코프로 전달된다.
        self.assertEqual(seen.get("customer_code"), "00227")
        self.assertEqual(seen.get("publisher_scope_hcode"), "5019")

    async def test_distributor_scope_none(self) -> None:
        seen: dict = {}

        async def fake_svc(**kw):
            seen.update(kw)
            return dict(_EMPTY_SINGLE)

        with patch.object(cls_svc, "get_customer_ledger", fake_svc):
            await ledger_router.get_customer_ledger(
                server_id="remote_155", customer_code="00227",
                date_from="2026.01.01", date_to="2026.08.10",
                bcode_from=None, bcode_to=None, scope="ALL",
                sort_by=None, sort_dir=None, limit=100, offset=0,
                current=_distributor_ctx(),
            )
        self.assertIsNone(seen.get("publisher_scope_hcode"))

    async def test_integrated_scope_and_pattern_passthrough(self) -> None:
        seen: dict = {}

        async def fake_svc(**kw):
            seen.update(kw)
            return dict(_EMPTY_INTEGRATED)

        with patch.object(cls_svc, "get_integrated_customer_ledger", fake_svc):
            await ledger_router.get_integrated_customer_ledger(
                server_id="remote_153",
                date_from="2026.01.01", date_to="2026.08.10",
                customer_pattern="22", scope="ALL",
                sort_by=None, sort_dir=None, limit=100, offset=0,
                current=_kyomunsa_ctx(),
            )
        self.assertEqual(seen.get("scope_hcode"), "5019")
        self.assertEqual(seen.get("customer_pattern"), "22")


# ---------------------------------------------------------------
# 5) 프론트 소스 가드 — 도서코드 제거·라벨 교정·메뉴 통합
# ---------------------------------------------------------------


class FrontendSourceGuards(TestCase):
    def test_customer_ledger_page_has_no_book_code_filter(self) -> None:
        src = (FRONT / "app" / "(app)" / "ledger" / "customer" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("bcodeFrom", src, "거래처원장 도서코드 필터 부활 — DEC-137 회귀")
        self.assertNotIn("도서코드 (선택)", src)
        self.assertNotIn("Sobo32.Edit103", src)

    def test_inventory_ledger_label_is_publisher_axis(self) -> None:
        src = (FRONT / "app" / "(app)" / "inventory" / "ledger" / "page.tsx").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("거래처/지사 hcode", src, "S1_Ssub.Hcode=출판사 축 오라벨 회귀")
        self.assertIn('lookupKind="publisher"', src)

    def test_menu_groups_merged_and_ledger_forms_gated(self) -> None:
        src = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        self.assertNotIn('menuGroup: "ledger"', src, "재고원장 그룹 분리 부활 — DEC-137 회귀")
        self.assertNotIn('{ id: "ledger", label: "재고원장"', src)
        # 원장 4폼(NAV-03 폼 단위 게이트) — 그룹 통합 후에도 권한 축 보존.
        self.assertGreaterEqual(src.count('menuId: "ACC-MENU-NAV-03"'), 4)
        # 수불 중복 메뉴 감춤 — 통합 레이아웃 화이트리스트에 Sobo33 계열 부재.
        self.assertIn("INVENTORY_SIDEBAR_LAYOUT", src)
        layout = src.split("INVENTORY_SIDEBAR_LAYOUT")[1].split("];")[0]
        self.assertNotIn("Sobo33_ledger", layout)
        self.assertNotIn("Sobo33_1_ledger", layout)
        self.assertIn("Sobo31", layout)
        self.assertIn("Sobo32_ledger", layout)
        self.assertIn("Sobo48_compare", layout)


if __name__ == "__main__":
    main()
