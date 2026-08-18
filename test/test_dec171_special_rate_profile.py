"""DEC-171 — 특별관리 계정(빌드)별 비율 프로필(총판 single / 출판 by_pubun) 회귀 가드.

- 프로필 해석은 계약 special_master.yaml 데이터로만(코드 분기 없음).
- 목록/생성/수정은 Grat2~6 을 컬럼 드리프트 안전하게 다룬다.
- 라인 자동조회(G6 단계)는 프로필에 따라 Grat1 또는 판매유형별 컬럼을 적용한다.
- 번들 사본(backend/data/contracts) == 허브 정본.
"""
import asyncio
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from app.services import g6_ggeo_adapt, masters_service
from app.services import sales_statement_create_service as svc
from app.services import special_rate_profile as srp

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"


class ProfileResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        srp.reload_for_tests()

    def test_distributor_and_unknown_get_single(self) -> None:
        for ctx in ({"build_role": "distributor", "account_type": "T2_DIST"}, {}, {"build_role": ""}):
            p = srp.resolve_special_rate_profile(ctx)
            self.assertEqual(p["id"], "single", ctx)
            self.assertEqual(p["columns"], ["grat1"])
            self.assertEqual(p["apply"], "grat1")

    def test_publisher_builds_get_by_pubun(self) -> None:
        for role in ("publisher", "warehouse_publisher"):
            p = srp.resolve_special_rate_profile({"build_role": role, "account_type": "T3"})
            self.assertEqual(p["id"], "by_pubun", role)
            self.assertEqual(p["columns"], ["grat1", "grat2", "grat3", "grat4", "grat5", "grat6"])
            self.assertEqual(p["column_labels"]["grat2"], "현매")

    def test_pubun_column_mapping_matches_legacy_prinrat1(self) -> None:
        p = srp.resolve_special_rate_profile({"build_role": "warehouse_publisher"})
        col = lambda pu, gu="": srp.rate_column_for_pubun(p, pu, gu)  # noqa: E731
        self.assertEqual(col("위탁"), "grat1")
        self.assertEqual(col("신간"), "grat1")
        self.assertEqual(col("현매"), "grat2")
        self.assertEqual(col("매절"), "grat3")
        self.assertEqual(col("납품"), "grat4")
        self.assertEqual(col("특별"), "grat5")
        self.assertEqual(col("한도"), "grat6")
        self.assertEqual(col("기타"), "grat6")   # DEC-171 명시 결정(그리드 라벨 기타=Grat6)
        self.assertIsNone(col("증정"))            # 비율 0
        self.assertEqual(col("현매", "반품"), "grat1")  # Gubun=반품 → Grat1
        self.assertEqual(col("모름"), "grat1")     # 미지정 = 위탁 취급
        single = srp.resolve_special_rate_profile({"build_role": "distributor"})
        self.assertEqual(srp.rate_column_for_pubun(single, "현매"), "grat1")

    def test_bundled_copy_matches_hub_source(self) -> None:
        hub = _HUB / "migration" / "contracts" / "special_master.yaml"
        bundled = _BACKEND / "data" / "contracts" / "special_master.yaml"
        self.assertTrue(bundled.is_file(), f"번들 사본 누락: {bundled}")
        h = yaml.safe_load(hub.read_text(encoding="utf-8"))
        b = yaml.safe_load(bundled.read_text(encoding="utf-8"))
        self.assertEqual(h["rate_profiles"], b["rate_profiles"])
        self.assertEqual(h["customer_variants"], b["customer_variants"])


class _Cap:
    def __init__(self, rows_by_needle):
        self.calls = []
        self.rows_by_needle = rows_by_needle

    async def __call__(self, server_id, sql, params=None):
        self.calls.append((sql, tuple(params or ())))
        for needle, rows in self.rows_by_needle:
            if needle in sql:
                return rows
        return []


class G6AdaptAndCrudTests(unittest.TestCase):
    def setUp(self) -> None:
        g6_ggeo_adapt.clear_g6_column_cache_for_tests()

    def test_select_fragments_follow_column_drift(self) -> None:
        full = {"id", "hcode", "gcode", "bcode", "grat1", "grat2", "grat3", "grat4", "grat5", "grat6", "gssum"}
        frag = g6_ggeo_adapt.rate_select_fragments(full, alias="g")
        self.assertIn("IFNULL(g.Grat2,0) AS grat2", frag)
        self.assertNotIn("COALESCE", frag)
        slim = {"id", "hcode", "gcode", "bcode", "grat1", "gssum"}
        frag2 = g6_ggeo_adapt.rate_select_fragments(slim, alias="g")
        self.assertIn("0 AS grat2", frag2)
        self.assertNotIn("Grat2", frag2)
        self.assertEqual(
            g6_ggeo_adapt.writable_rate_columns(slim, {"grat2": 30, "grat3": 40}), [],
        )
        self.assertEqual(
            g6_ggeo_adapt.writable_rate_columns(full, {"grat2": 30, "grat3": None, "grat6": "55"}),
            [("Grat2", 30.0), ("Grat6", 55.0)],
        )

    def test_create_and_update_write_extra_rate_columns_when_present(self) -> None:
        full = {"id", "hcode", "gcode", "bcode", "grat1", "grat2", "grat3", "grat4", "grat5", "grat6", "gssum"}

        async def fake_cols(server_id):
            return full

        cap = _Cap([("SELECT ID FROM G6_Ggeo WHERE Hcode", []), ("SELECT ID AS id", [{"id": 7}]),
                    ("SELECT ID FROM G6_Ggeo WHERE ID", [{"ID": 7}])])
        tx = []

        async def fake_tx(server_id, stmts):
            tx.extend(stmts)
            return [1] * len(stmts)

        with patch.object(g6_ggeo_adapt, "g6_column_names", fake_cols), \
             patch.object(masters_service, "execute_query", cap), \
             patch.object(masters_service, "execute_in_transaction", fake_tx):
            asyncio.run(masters_service.create_special_master(
                server_id="remote_1", hcode="5019",
                payload={"gcode": "00001", "bcode": "3411", "grat1": "75", "gssum": 30000, "grat2": 70, "grat5": 60},
            ))
            asyncio.run(masters_service.update_special_master(
                server_id="remote_1", row_id=7, hcode="5019", payload={"grat3": 65, "gssum": 29000},
            ))
        ins_sql, ins_params = tx[0]
        self.assertIn("Grat2", ins_sql)
        self.assertIn("Grat5", ins_sql)
        self.assertEqual(ins_params[-2:], (70.0, 60.0))
        upd_sql, upd_params = tx[1]
        self.assertIn("Grat3=%s", upd_sql)
        self.assertIn("Gssum=%s", upd_sql)
        self.assertEqual(upd_params[:2], (29000.0, 65.0))


def _exec_router(handlers):
    async def fake(_sid, sql, _params=()):
        for needle, rows in handlers:
            if needle in sql:
                return rows
        return []
    return fake


class LineDefaultsByPubunTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        srp.reload_for_tests()
        g6_ggeo_adapt.clear_g6_column_cache_for_tests()

    async def _resolve(self, pubun, profile):
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", [{"grat1": 70, "grat2": 60, "grat3": 55, "grat4": 50, "grat5": 45, "grat6": 40, "gssum": 28000}]),
            ("FROM G7_Ggeo", []),
        ]

        async def fake_cols(server_id):
            return {"grat1", "grat2", "grat3", "grat4", "grat5", "grat6", "gssum"}

        with patch.object(svc, "execute_query", _exec_router(handlers)), \
             patch.object(g6_ggeo_adapt, "g6_column_names", fake_cols):
            return await svc.resolve_line_defaults(
                "remote_1", company_hcode="5019", customer="00001", bcode="3411",
                pubun=pubun, special_profile=profile,
            )

    async def test_by_pubun_profile_applies_pubun_column_and_gssum_price(self) -> None:
        prof = srp.resolve_special_rate_profile({"build_role": "warehouse_publisher"})
        out = await self._resolve("현매", prof)
        self.assertEqual(out["grat1"], 60)          # G6.Grat2
        self.assertEqual(out["gdang"], 28000)       # 단가 = G6.Gssum
        self.assertEqual(out["source"], "G6_Ggeo:grat2")
        self.assertEqual((await self._resolve("납품", prof))["grat1"], 50)
        self.assertEqual((await self._resolve("증정", prof))["grat1"], 0)
        self.assertEqual((await self._resolve("위탁", prof))["grat1"], 70)

    async def test_by_pubun_zero_column_falls_back_to_grat1(self) -> None:
        # 웹 기존 특가 행(Grat1 만 입력)에서 현매 전표가 0% 가 되지 않도록 Grat1 폴백(DEC-171 명시 결정).
        prof = srp.resolve_special_rate_profile({"build_role": "publisher"})
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", [{"grat1": 75, "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "gssum": 46000}]),
            ("FROM G7_Ggeo", []),
        ]

        async def fake_cols(server_id):
            return {"grat1", "grat2", "grat3", "grat4", "grat5", "grat6", "gssum"}

        with patch.object(svc, "execute_query", _exec_router(handlers)), \
             patch.object(g6_ggeo_adapt, "g6_column_names", fake_cols):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="5019", customer="00001", bcode="3392",
                pubun="현매", special_profile=prof,
            )
        self.assertEqual(out["grat1"], 75)
        self.assertEqual(out["gdang"], 46000)
        self.assertEqual(out["source"], "G6_Ggeo")

    async def test_single_profile_and_none_apply_grat1_only(self) -> None:
        single = srp.resolve_special_rate_profile({"build_role": "distributor"})
        out = await self._resolve("현매", single)
        self.assertEqual(out["grat1"], 70)
        self.assertEqual(out["source"], "G6_Ggeo")
        out2 = await self._resolve("현매", None)
        self.assertEqual(out2["grat1"], 70)


if __name__ == "__main__":
    unittest.main()
