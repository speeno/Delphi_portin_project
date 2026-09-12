"""DEC-275 — 반품 접수 헤더 «상대처 축»: 거래처(G1_Ggeo→Gcode) 선택 + 회사/출판사(Hcode) 프로필 (2026-09-12).

교문사(출판, hcode 5019) 리포트: 「출판사 찾기」 팝업이 출판사(G7_Ggeo)를 검색해 자사만 나오고
거래처 「홍익」은 0건. 레거시는 두 빌드 모두 거래처(Seek10=G1_Ggeo)를 S1_Ssub.Gcode 에,
회사/출판사를 Hcode 에 쓴다(출판 Base01.pas L6081/L6086 · 유통 Subu23.pas L1268/L1271).

가드
- 프로필 해석은 계약 return_receipt.yaml customer_variants.counterparty_axis 데이터로만(코드 분기 없음).
- INSERT 가 Gcode 를 기록하고, 상세가 거래처(gcode/gname)를 hcode 스코프로 돌려준다.
- POST /returns 의 hcode 는 로그인 스코프 강제(타사 403, 빈값 주입). GET /returns/entry-profile 200.
- 화면: 상대처 룩업 = customer kind(출고 접수 재사용), publisher 룩업은 인라인 금지(DEC-193).
- 번들 사본(backend/data/contracts) == 허브 정본, probe 매트릭스 등록.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "도서물류관리프로그램"
BACKEND = PRODUCT / "backend"
FRONT = PRODUCT / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import returns_entry_profile as rep  # noqa: E402
from app.services import returns_service as svc  # noqa: E402

PUB_CTX = {
    "user_id": "kmsa01", "server_id": "remote_153", "hcode": "5019", "role": "user",
    "permissions": ["returns.read"], "account_type": "T2_PUB", "build_role": "publisher",
    "account_family": "chul_09",
}
SUPER_CTX = {
    "user_id": "admin", "server_id": "remote_153", "hcode": "0000", "role": "admin",
    "permissions": ["*"], "account_type": "T1", "build_role": "super",
}


class ProfileResolutionTests(TestCase):
    def setUp(self) -> None:
        rep.reload_for_tests()

    def test_publisher_and_unknown_get_fixed_login_hcode(self) -> None:
        for ctx in (
            {"build_role": "publisher", "account_type": "T2_PUB"},
            {"build_role": "warehouse_publisher", "account_type": "T3"},
            {"account_type": "", "account_family": "chul_09"},  # 공유 DB 미분류 — fail-closed
            {},
        ):
            p = rep.resolve_return_entry_profile(ctx)
            self.assertEqual(p["id"], "publisher_fixed", ctx)
            self.assertEqual(p["publisher"]["mode"], "login", ctx)
            self.assertEqual(p["customer"]["lookup"], "customer")
            self.assertEqual(p["customer"]["table"], "G1_Ggeo")
            self.assertEqual(p["customer"]["saves_to"], "S1_Ssub.Gcode")
            self.assertTrue(p["customer"]["required"])

    def test_distributor_and_super_select_publisher(self) -> None:
        for ctx in ({"build_role": "distributor", "account_type": "T2_DIST"}, {"build_role": "super"}):
            p = rep.resolve_return_entry_profile(ctx)
            self.assertEqual(p["id"], "distributor_select", ctx)
            self.assertEqual(p["publisher"]["mode"], "select")
            self.assertEqual(p["publisher"]["table"], "G7_Ggeo")
            self.assertEqual(p["customer"]["table"], "G1_Ggeo")  # 거래처 축은 빌드 불문 G1_Ggeo

    def test_unknown_mode_and_missing_contract_fail_closed(self) -> None:
        with patch.object(rep, "_load_axis", return_value={
            "profiles": {"publisher_fixed": {"publisher": {"mode": "anything-goes"}}},
            "variants": [{"match": {}, "profile": "publisher_fixed"}],
        }):
            self.assertEqual(rep.resolve_return_entry_profile({})["publisher"]["mode"], "login")
        with patch.object(rep, "_load_axis", return_value={}):
            p = rep.resolve_return_entry_profile({"build_role": "distributor"})
            self.assertEqual(p["id"], "publisher_fixed")
            self.assertEqual(p["publisher"]["mode"], "login")

    def test_bundled_copy_matches_hub_source(self) -> None:
        hub = ROOT / "migration" / "contracts" / "return_receipt.yaml"
        bundled = BACKEND / "data" / "contracts" / "return_receipt.yaml"
        self.assertTrue(bundled.is_file(), f"번들 사본 누락: {bundled}")
        h = yaml.safe_load(hub.read_text(encoding="utf-8"))
        b = yaml.safe_load(bundled.read_text(encoding="utf-8"))
        self.assertEqual(
            h, b, "허브 정본과 번들 사본이 다릅니다 — 허브 편집 후 backend/data/contracts/ 로 복사하세요.",
        )
        names = [i["name"] for i in h["inputs"]["return_header"]]
        self.assertIn("gcode", names)
        self.assertIn("hcode", names)


class InsertWritesGcodeTests(IsolatedAsyncioTestCase):
    def test_sql_has_gcode_column(self) -> None:
        cols = svc.SQL_INSERT_LINE.split("VALUES")[0]
        self.assertIn("Gcode", cols)
        self.assertIn("Hcode", cols)

    async def test_create_binds_customer_gcode_on_every_line(self) -> None:
        captured: list = []

        async def fake_txn(server_id, ops):  # noqa: ARG001
            captured.extend(ops)

        with patch.object(svc, "_generate_jubun", AsyncMock(return_value="190000000001")), \
                patch.object(svc, "_default_outbound_ocode", return_value="A"), \
                patch.object(svc, "execute_in_transaction", side_effect=fake_txn):
            res = await svc.create_return(
                server_id="remote_153",
                header={"gdate": "2026-09-12", "hcode": "5019", "gcode": "H0001", "gjisa": ""},
                memo=None,
                lines=[{"bcode": "B0001", "gsqut": 3}, {"bcode": "B0002", "gsqut": 1}],
            )
        self.assertEqual(res["gcode"], "H0001")
        self.assertEqual(res["return_key"]["hcode"], "5019")
        self.assertEqual(len(captured), 2)
        for sql, params in captured:
            self.assertIs(sql, svc.SQL_INSERT_LINE)
            self.assertEqual(sql.count("%s"), len(params), "placeholder 수 = 바인딩 수")
            self.assertEqual(params[1], "5019")   # Hcode = 회사/출판사
            self.assertEqual(params[7], "H0001")  # Gcode = 상대 거래처 (Scode 'X' 다음)

    async def test_create_without_hcode_is_rejected(self) -> None:
        with patch.object(svc, "_generate_jubun", AsyncMock(return_value="1")), \
                patch.object(svc, "execute_in_transaction", AsyncMock()):
            with self.assertRaises(ValueError):
                await svc.create_return(
                    server_id="remote_153", header={"gdate": "2026-09-12", "gcode": "H0001"},
                    memo=None, lines=[{"bcode": "B0001", "gsqut": 1}],
                )


class DetailReturnsCustomerTests(IsolatedAsyncioTestCase):
    async def test_detail_exposes_gcode_and_scoped_g1_name(self) -> None:
        calls: list = []

        async def fake_query(server_id, sql, params=None):  # noqa: ARG001
            calls.append((sql, tuple(params or ())))
            if sql is svc.SQL_DETAIL_LINES:
                return [{"Gdate": "2026.09.12", "Hcode": "5019", "Jubun": "1", "Bcode": "B0001",
                         "Pubun": "정품", "Gsqut": 2, "Gdang": 10000, "Grat1": 0.7, "Gssum": 14000,
                         "Gbigo": "", "Yesno": "1", "Gcode": "H0001"}]
            if sql is svc.SQL_PUBLISHER_BY_HCODE:
                return [{"hcode": "5019", "hname": "(주)교문사"}]
            if sql is svc.SQL_CUSTOMER_BY_GCODE:
                return [{"gcode": "H0001", "gname": "홍익문고"}]
            return []

        with patch.object(svc, "execute_query", side_effect=fake_query), \
                patch.object(svc, "_attach_book_meta_grouped", AsyncMock()):
            d = await svc.get_return_detail(server_id="remote_153", return_key_str="G|2026.09.12|5019|1")
        self.assertEqual(d["customer"]["hcode"], "5019")
        self.assertEqual(d["customer"]["gcode"], "H0001")
        self.assertEqual(d["customer"]["gname"], "홍익문고")
        g1 = [c for c in calls if c[0] is svc.SQL_CUSTOMER_BY_GCODE]
        self.assertEqual(len(g1), 1)
        self.assertEqual(g1[0][1], ("H0001", "5019"))  # 전표 Hcode(회사)로 격리
        self.assertIn("Hcode=%s", svc.SQL_CUSTOMER_BY_GCODE)
        self.assertNotIn("CASE", svc.SQL_CUSTOMER_BY_GCODE)  # MySQL 3.23 안전


class RouterTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.pop(get_current_user, None)

    def _as(self, ctx: dict) -> None:
        app.dependency_overrides[get_current_user] = lambda: dict(ctx)

    def _post(self, hcode: str) -> tuple[int, dict, dict | None]:
        seen: dict = {}

        async def fake_create(*, server_id, header, memo, lines):  # noqa: ARG001
            seen.update(header)
            return {"return_key": {"gdate": "2026.09.12", "bdate": None, "hcode": header["hcode"], "jubun": "1"},
                    "gcode": header.get("gcode", ""), "lines": len(lines), "qty": 1, "amount": 0,
                    "created_at": "2026-09-12T00:00:00+00:00"}

        with patch.object(svc, "create_return", side_effect=fake_create):
            res = self.client.post("/api/v1/returns", json={
                "serverId": "remote_153",
                "returnHeader": {"gdate": "2026-09-12", "hcode": hcode, "gcode": "H0001"},
                "returnLines": [{"bcode": "B0001", "gsqut": 1}],
            })
        return res.status_code, (res.json() if res.content else {}), (seen or None)

    def test_publisher_other_hcode_forbidden(self) -> None:
        self._as(PUB_CTX)
        code, body, seen = self._post("9999")
        self.assertEqual(code, 403, body)
        self.assertIsNone(seen)

    def test_publisher_empty_hcode_gets_login_scope(self) -> None:
        self._as(PUB_CTX)
        code, body, seen = self._post("")
        self.assertEqual(code, 201, body)
        self.assertEqual(seen["hcode"], "5019")
        self.assertEqual(seen["gcode"], "H0001")
        self.assertEqual(body["gcode"], "H0001")

    def test_publisher_own_hcode_ok(self) -> None:
        self._as(PUB_CTX)
        code, body, seen = self._post("5019")
        self.assertEqual(code, 201, body)
        self.assertEqual(seen["hcode"], "5019")

    def test_entry_profile_publisher(self) -> None:
        self._as(PUB_CTX)
        res = self.client.get("/api/v1/returns/entry-profile")
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["id"], "publisher_fixed")
        self.assertEqual(body["publisher"]["mode"], "login")
        self.assertEqual(body["login_hcode"], "5019")
        self.assertEqual(body["customer"]["lookup"], "customer")

    def test_entry_profile_super(self) -> None:
        self._as(SUPER_CTX)
        res = self.client.get("/api/v1/returns/entry-profile")
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["publisher"]["mode"], "select")
        self.assertEqual(body["login_hcode"], "")


class FrontendStaticGuardTests(TestCase):
    NEW = FRONT / "app" / "(app)" / "returns" / "receipts" / "new" / "page.tsx"
    DETAIL = FRONT / "app" / "(app)" / "returns" / "receipts" / "[returnKey]" / "page.tsx"

    def test_new_page_picks_customer_and_saves_gcode(self) -> None:
        src = self.NEW.read_text(encoding="utf-8")
        self.assertIn('lookupKind="customer"', src)
        self.assertIn("gcode: customer", src)
        self.assertIn("hcode: company", src)
        self.assertIn(".entryProfile()", src)
        self.assertIn('inputLegacyId="Sobo23.Edit104"', src)
        self.assertIn("applyCustomerToGcode(", src)
        # 상대처 룩업은 출고 접수와 같은 G1 인라인+팝업.
        cust = src[src.index('lookupKind="customer"'): src.index('inputLegacyId="Sobo23.Edit104"')]
        self.assertIn("useInlineAutocomplete", cust)

    def test_publisher_lookup_is_popup_only_and_profile_gated(self) -> None:
        src = self.NEW.read_text(encoding="utf-8")
        i = src.index('lookupKind="publisher"')
        block = src[i: src.index("refocusAfterSelect", i)]
        self.assertNotIn("useInlineAutocomplete", block)  # DEC-193 — publisher 인라인은 거래처를 돌려준다
        self.assertIn('inputLegacyId="Sobo23.Edit107"', block)
        gate = src[src.rindex("publisherMode", 0, i): i]
        self.assertIn('publisherMode === "select"', gate)
        # 계정/hcode 코드 분기 금지 — 프로필 데이터로만.
        for needle in ('"5019"', "T2_PUB", "T2_DIST", "build_role ==", "account_type =="):
            self.assertNotIn(needle, src, needle)

    def test_detail_shows_customer(self) -> None:
        src = self.DETAIL.read_text(encoding="utf-8")
        self.assertIn("detail.customer?.gcode", src)

    def test_api_client_and_probe_registered(self) -> None:
        api = (FRONT / "lib" / "returns-api.ts").read_text(encoding="utf-8")
        self.assertIn("/api/v1/returns/entry-profile", api)
        self.assertIn("gcode?: string; gname?: string", api)
        probe = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn('"group": "returns.entry_profile"', probe)
        self.assertIn('"/api/v1/returns/entry-profile"', probe)


if __name__ == "__main__":
    main()
