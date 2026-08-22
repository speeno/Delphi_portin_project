"""입고현황 교문사(공유 chul_09) 정합 회귀 — 2026-08-22 사용자 리포트.

배경
----
교문사 계정의 웹 입고현황이 레거시 Subu25_2(입고현황(상세), chul_09 위러브 출판 빌드)와
다른 데이터를 보였다. 원인 4건:

1. `/transactions/inbound-status?view=summary` facade 가 `period_report` 에 hcode 를
   전달하지 않아 공유 chul_09_db 에서 4개 테넌트(교문사·위러브1·2·3) 입고가 합산됨.
2. `_fetch_vendor_names` 가 입고처 마스터 G2_Ggwo 가 아닌 거래처 G1_Ggeo 를,
   그것도 Hcode 무스코프로 조회 — 코드 충돌 시 타 테넌트/거래처 명이 입고처명 자리에 표시.
   레거시 정본: `G2_Ggwo.Locate(Hcode=로그인)` → 실패 시 `Hcode=''` 폴백 (Subu25_2 L455-475).
3. 입고현황 LIST 가 `Gubun='입고'` 하드필터 — 레거시 고정 조건은 `Scode='Y'`+`Gcode<>''` 뿐
   (Subu25_2 Button101Click L396-420), Gubun(입고/반품)은 검색 콤보.
4. `HAVING MAX(Yesno)<>'2'` 기본 제외 — 레거시는 Yesno 무필터(2=접수완료 잠금, 취소 아님).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import inbound_service, masters_service  # noqa: E402


def _tenant_auth() -> dict:
    # 비슈퍼 + JWT hcode 보유 (교문사 계열 시나리오) → enforce_hcode_isolation 이
    # 빈 요청 hcode 에 스코프를 자동 주입한다.
    return {"user_id": "kyomun01", "server_id": "remote_1", "hcode": "K0001"}


COMMON_QUERY = "?serverId=remote_1&dateFrom=2026-07-01&dateTo=2026-08-22&limit=10&offset=0"

_G2_META = ({"gcode", "gname", "hcode"}, {"gcode": "Gcode", "gname": "Gname", "hcode": "Hcode"})


class SummaryHcodeIsolationTests(TestCase):
    """원인 1 — 요약 뷰 hcode 전달."""

    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _tenant_auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides[get_current_user] = _tenant_auth

    def test_summary_view_passes_tenant_hcode(self) -> None:
        captured: list[dict] = []

        async def fake_period(**kwargs):
            captured.append(kwargs)
            return {
                "by_publisher": [], "by_vendor": [],
                "totals": {"qty": 0, "amount": 0},
                "page": {"limit": 10, "offset": 0, "total": 0, "has_more": False},
            }

        with patch.object(inbound_service, "period_report", side_effect=fake_period):
            res = self.client.get(
                "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=summary"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0].get("hcode"), "K0001")

    def test_list_view_uses_legacy_status_scope(self) -> None:
        """원인 3 — facade 는 Gubun 무필터 + Gcode<>'' (레거시 고정 조건)."""
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            return [], 0

        with patch.object(inbound_service, "list_receipts", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/transactions/inbound-status" + COMMON_QUERY + "&view=list"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(captured), 1)
        self.assertIsNone(captured[0].get("gubun"))
        self.assertTrue(captured[0].get("require_vendor"))
        self.assertEqual(captured[0].get("hcode"), "K0001")


class ListReceiptsScopeSqlTests(TestCase):
    """원인 3 — list_receipts WHERE 조립 (기본/입고현황 스코프)."""

    def _run_list(self, **kwargs) -> list[tuple[str, tuple]]:
        calls: list[tuple[str, tuple]] = []

        async def fake_exec(server_id, sql, params=()):
            calls.append((sql, tuple(params)))
            return []

        async def fake_count(server_id, **kw):
            calls.append((f"COUNT {kw.get('where_sql', '')}", tuple(kw.get("params") or ())))
            return 0

        async def fake_cols(server_id):
            return set()

        with patch.object(inbound_service, "execute_query", side_effect=fake_exec), \
             patch.object(inbound_service, "count_grouped", side_effect=fake_count), \
             patch.object(inbound_service, "_present_cols", side_effect=fake_cols):
            asyncio.run(
                inbound_service.list_receipts(
                    server_id="remote_1",
                    date_from="2026-07-01",
                    date_to="2026-08-22",
                    **kwargs,
                )
            )
        return calls

    def test_default_keeps_gubun_inbound(self) -> None:
        """입고접수/입고명세서 현행 — Gubun='입고' 파라미터 바인딩 유지."""
        calls = self._run_list()
        sql, params = calls[0]
        self.assertIn("Gubun = %s", sql)
        self.assertIn("입고", params)
        self.assertNotIn("Gcode <> ''", sql)

    def test_status_scope_drops_gubun_and_requires_vendor(self) -> None:
        calls = self._run_list(gubun=None, require_vendor=True)
        sql, params = calls[0]
        self.assertNotIn("Gubun", sql)
        self.assertNotIn("입고", params)
        self.assertIn("Gcode <> ''", sql)
        self.assertIn("Scode = 'Y'", sql)

    def test_param_order_with_hcode_filter(self) -> None:
        """Gubun 바인딩이 Gdate 2개 뒤·Hcode 앞 순서를 지킨다 (파라미터 어긋남 회귀 가드)."""
        calls = self._run_list(hcode="K0001")
        sql, params = calls[0]
        self.assertEqual(params[:3], ("2026.07.01", "2026.08.22", "입고"))
        self.assertIn("K0001", params)


class VendorNameLookupTests(TestCase):
    """원인 2 — 입고처명 G2_Ggwo + Hcode(로그인→'') 폴백."""

    def test_scoped_lookup_targets_g2_with_hcode_fallback(self) -> None:
        captured: dict = {}

        async def fake_meta(server_id):
            return _G2_META

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            captured["sql"] = sql_template
            captured["prefix"] = tuple(prefix_params)
            return [
                {"gcode": "V001", "gname": "공유입고처", "hcode": ""},
                {"gcode": "V001", "gname": "중원아트(랩핑)", "hcode": "K0001"},
                {"gcode": "V002", "gname": "타테넌트입고처", "hcode": "W0001"},
                {"gcode": "V003", "gname": "태성제책사(공유)", "hcode": ""},
            ]

        with patch.object(inbound_service, "g2_ggwo_column_meta", side_effect=fake_meta), \
             patch.object(inbound_service, "in_clause_lookup", side_effect=fake_lookup):
            names = asyncio.run(
                inbound_service._fetch_vendor_names(
                    "remote_1", ["V001", "V002", "V003"], scope_hcode="K0001"
                )
            )

        self.assertIn("G2_Ggwo", captured["sql"])
        self.assertNotIn("G1_Ggeo", captured["sql"])
        self.assertIn("Hcode IN (%s, '')", captured["sql"])
        self.assertEqual(captured["prefix"], ("K0001",))
        # 정확 일치(Hcode=로그인) 행이 '' 폴백 행보다 우선.
        self.assertEqual(names["V001"], "중원아트(랩핑)")
        self.assertEqual(names["V003"], "태성제책사(공유)")

    def test_unscoped_lookup_still_uses_g2(self) -> None:
        captured: dict = {}

        async def fake_lookup(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):
            captured["sql"] = sql_template
            return [{"gcode": "V001", "gname": "중원아트(랩핑)"}]

        with patch.object(inbound_service, "in_clause_lookup", side_effect=fake_lookup):
            names = asyncio.run(
                inbound_service._fetch_vendor_names("remote_1", ["V001"], scope_hcode=None)
            )
        self.assertIn("G2_Ggwo", captured["sql"])
        self.assertNotIn("Hcode IN", captured["sql"])
        self.assertEqual(names["V001"], "중원아트(랩핑)")


class InboundVendorSearchScopeTests(TestCase):
    """원인 2 확장 — 입고처 자동완성도 공유 DB 에서 Hcode IN (<scope>,'') 격리."""

    def test_scoped_autocomplete_sql(self) -> None:
        captured: dict = {}

        async def fake_meta(server_id):
            return _G2_META

        async def fake_exec(server_id, sql, params=()):
            captured["sql"] = sql
            captured["params"] = tuple(params)
            return [{"gcode": "V001", "gname": "중원아트(랩핑)"}]

        with patch.object(masters_service, "g2_ggwo_column_meta", side_effect=fake_meta), \
             patch.object(masters_service, "execute_query", side_effect=fake_exec):
            items = asyncio.run(
                masters_service.search_inbound_vendors(
                    server_id="remote_1", q="중원", scope_hcode="K0001"
                )
            )
        self.assertIn("Hcode IN (%s, '')", captured["sql"])
        self.assertIn("K0001", captured["params"])
        self.assertEqual(items[0]["gname"], "중원아트(랩핑)")

    def test_unscoped_autocomplete_unchanged(self) -> None:
        captured: dict = {}

        async def fake_exec(server_id, sql, params=()):
            captured["sql"] = sql
            return []

        with patch.object(masters_service, "execute_query", side_effect=fake_exec):
            asyncio.run(
                masters_service.search_inbound_vendors(server_id="remote_1", q="중원")
            )
        self.assertNotIn("Hcode IN", captured["sql"])


class FrontendDefaultsTests(TestCase):
    """원인 4 — 입고현황 페이지는 완료(Yesno=2) 전표 기본 포함."""

    def test_include_cancelled_defaults_true(self) -> None:
        page = FRONT / "app" / "(app)" / "transactions" / "inbound-status" / "page.tsx"
        src = page.read_text(encoding="utf-8")
        self.assertIn("includeCancelled: true", src)


if __name__ == "__main__":
    main()
