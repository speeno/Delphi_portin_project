"""거래명세서(Sobo21) 신규추가 — DEC-065 1차 검증.

레거시 정본: WeLove_FTP/도서유통-출판/{Subu21,Tong02}.pas.
- 금액 공식 PrinYing (Gssum = Gdang*Gsqut*Grat1/100)
- 비율 선택 PrinZing (Pubun → Grat1~Grat7)
- 라인 자동조회 Button201Click (G1→G4→G6→직전거래가 last-wins)
- 직전거래가 PrinRat1 (G7_Ggeo Chek2/Chek3 게이트)

실 DB 없이 service 내부 execute_query / outbound_service.create_order 만 monkeypatch.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import sales_statement_create_service as svc  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "hcode": "A0001", "role": "admin"}


app.dependency_overrides[get_current_user] = _override_auth


# =====================================================================
# 1) 금액 공식 (PrinYing) + 비율 선택 (PrinZing) — 순수 단위
# =====================================================================

class AmountAndRateTests(TestCase):
    def test_amount_basic_85pct(self) -> None:
        # 영상 검증: 위탁 1 × 30,000 × 85% = 25,500
        self.assertEqual(svc.compute_gssum(30000, 1, 85, gubun="출고", pubun="위탁"), 25500)

    def test_amount_zero_rate_is_zero(self) -> None:
        self.assertEqual(svc.compute_gssum(30000, 5, 0), 0)

    def test_amount_jeungjeong_is_zero(self) -> None:
        # 증정 + 비율 0 → 0
        self.assertEqual(svc.compute_gssum(30000, 5, 0, pubun="증정"), 0)

    def test_amount_return_negates_qty(self) -> None:
        # 반품 → 수량 음수화 후 계산
        self.assertEqual(svc.compute_gssum(10000, 3, 100, gubun="반품"), -30000)

    def test_rate_pubun_selects_correct_grat_column(self) -> None:
        row = {f"grat{i}": i * 10 for i in range(1, 8)}  # grat1=10..grat7=70
        self.assertEqual(svc._rate_for_pubun(row, "위탁"), 10)   # Grat1
        self.assertEqual(svc._rate_for_pubun(row, "현매"), 20)   # Grat2
        self.assertEqual(svc._rate_for_pubun(row, "매절"), 30)   # Grat3
        self.assertEqual(svc._rate_for_pubun(row, "한도"), 70)   # Grat7
        self.assertEqual(svc._rate_for_pubun(row, "증정"), 0)    # 0
        self.assertEqual(svc._rate_for_pubun(row, "위탁", gubun="반품"), 10)  # Gubun 반품 → Grat1


# =====================================================================
# 2) 라인 자동조회 override 계층 (G1 → G4 → G6 → 직전거래가)
# =====================================================================

def _exec_router(handlers):
    """SQL 문자열 → 반환 rows 매핑으로 execute_query 를 모킹."""
    async def fake(_sid, sql, _params=()):
        for needle, rows in handlers:
            if needle in sql:
                return rows() if callable(rows) else rows
        return []
    return fake


class LineDefaultsResolutionTests(IsolatedAsyncioTestCase):
    async def test_g4_book_base_fill(self) -> None:
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "고급영양학", "gjeja": "홍길동", "gdang": 30000,
                               "grat1": 85, "grat2": 0, "grat3": 0, "grat4": 0,
                               "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", []),
            ("FROM G7_Ggeo", []),
        ]
        with patch.object(svc, "execute_query", _exec_router(handlers)):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="A0001", customer="00001", bcode="3411", pubun="위탁")
        self.assertTrue(out["found"])
        self.assertEqual(out["product_name"], "고급영양학")
        self.assertEqual(out["gdang"], 30000)
        self.assertEqual(out["grat1"], 85)
        self.assertEqual(out["source"], "G4_Book")

    async def test_g6_special_overrides_book(self) -> None:
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", [{"grat1": 70, "gssum": 28000}]),  # 특가
            ("FROM G7_Ggeo", []),
        ]
        with patch.object(svc, "execute_query", _exec_router(handlers)):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="A0001", customer="00001", bcode="3411")
        self.assertEqual(out["gdang"], 28000)
        self.assertEqual(out["grat1"], 70)
        self.assertEqual(out["source"], "G6_Ggeo")

    async def test_price_reuse_grat1_overrides_both(self) -> None:
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", []),
            ("FROM G7_Ggeo", [{"chek2": "", "chek3": "grat1"}]),  # 직전거래가(단가+비율)
            ("FROM S1_Ssub", [{"gdang": 27000, "grat1": 80}]),
        ]
        with patch.object(svc, "execute_query", _exec_router(handlers)):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="A0001", customer="00001", bcode="3411")
        self.assertEqual(out["gdang"], 27000)
        self.assertEqual(out["grat1"], 80)
        self.assertIn("last", out["source"])

    async def test_price_reuse_grat2_overrides_rate_only(self) -> None:
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", []),
            ("FROM G7_Ggeo", [{"chek2": "", "chek3": "grat2"}]),  # 비율만
            ("FROM S1_Ssub", [{"gdang": 27000, "grat1": 80}]),
        ]
        with patch.object(svc, "execute_query", _exec_router(handlers)):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="A0001", customer="00001", bcode="3411")
        self.assertEqual(out["gdang"], 30000)  # 단가 유지
        self.assertEqual(out["grat1"], 80)      # 비율만 재사용

    async def test_price_reuse_off_when_not_configured(self) -> None:
        handlers = [
            ("FROM G1_Ggeo", []),
            ("FROM G4_Book", [{"gname": "책", "gjeja": "", "gdang": 30000, "grat1": 85,
                               "grat2": 0, "grat3": 0, "grat4": 0, "grat5": 0, "grat6": 0, "grat7": 0}]),
            ("FROM G6_Ggeo", []),
            ("FROM G7_Ggeo", [{"chek2": "", "chek3": ""}]),  # off
            ("FROM S1_Ssub", [{"gdang": 27000, "grat1": 80}]),  # 무시돼야 함
        ]
        with patch.object(svc, "execute_query", _exec_router(handlers)):
            out = await svc.resolve_line_defaults(
                "remote_1", company_hcode="A0001", customer="00001", bcode="3411")
        self.assertEqual(out["gdang"], 30000)
        self.assertEqual(out["grat1"], 85)


# =====================================================================
# 3) create_sales_statement — 금액 검증 + gubun 고정
# =====================================================================

class CreateServiceTests(IsolatedAsyncioTestCase):
    async def test_amount_recomputed_and_gubun_forced(self) -> None:
        captured: dict = {}

        async def fake_create(*, server_id, header, lines):
            captured["header"] = header
            captured["lines"] = lines
            return {"order_key": {"gdate": "2026.06.11", "hcode": "00001", "jubun": "00003"},
                    "lines": len(lines), "qty": 1, "amount": 25500,
                    "created_at": "2026-06-11T00:00:00+00:00"}

        with patch.object(svc.outbound_service, "create_order", side_effect=fake_create):
            await svc.create_sales_statement(
                server_id="remote_1",
                header={"gdate": "2026-06-11", "hcode": "00001", "gubun": "반품"},
                lines=[{"gcode": "00001", "bcode": "3411", "pubun": "위탁",
                        "gsqut": 1, "gdang": 30000, "grat1": 85, "gssum": 0}],
            )
        self.assertEqual(captured["header"]["gubun"], "출고")          # 강제 출고
        self.assertEqual(captured["lines"][0]["gssum"], 25500)         # 서버 재계산

    async def test_amount_mismatch_raises(self) -> None:
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            return {}
        with patch.object(svc.outbound_service, "create_order", side_effect=fake_create):
            with self.assertRaises(ValueError):
                await svc.create_sales_statement(
                    server_id="remote_1",
                    header={"gdate": "2026-06-11", "hcode": "00001"},
                    lines=[{"gcode": "00001", "bcode": "3411", "pubun": "위탁",
                            "gsqut": 1, "gdang": 30000, "grat1": 85, "gssum": 999}],  # 틀린 금액
                )


# =====================================================================
# 4) HTTP 엔드포인트 — POST 201 / line-defaults 200 / 금액불일치 422
# =====================================================================

class HttpEndpointTests(TestCase):
    def setUp(self) -> None:
        # 다른 테스트 파일이 dependency_overrides 를 비우거나 교체해도(공유 app 격리 취약점)
        # 본 클래스 HTTP 테스트는 항상 인증 우회로 동작하도록 매 테스트마다 재설정.
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_post_create_returns_201(self) -> None:
        async def fake_create(*, server_id, header, lines):  # noqa: ARG001
            return {"order_key": {"gdate": "2026.06.11", "hcode": "00001", "jubun": "00003"},
                    "lines": len(lines), "qty": 1, "amount": 25500,
                    "created_at": "2026-06-11T00:00:00+00:00"}
        with patch.object(svc, "create_sales_statement", side_effect=fake_create):
            res = self.client.post(
                "/api/v1/transactions/sales-statement",
                json={"serverId": "remote_1", "gdate": "2026-06-11", "hcode": "00001",
                      "gjisa": "", "lines": [{"bcode": "3411", "pubun": "위탁", "gsqut": 1,
                                              "gdang": 30000, "grat1": 85, "gssum": 25500}]},
            )
        self.assertEqual(res.status_code, 201, res.text)
        body = res.json()
        self.assertEqual(body["slip_no"], "00003")
        self.assertEqual(body["order_key"]["hcode"], "00001")

    def test_post_amount_mismatch_returns_422(self) -> None:
        async def boom(*, server_id, header, lines):  # noqa: ARG001
            raise ValueError("line amount mismatch")
        with patch.object(svc, "create_sales_statement", side_effect=boom):
            res = self.client.post(
                "/api/v1/transactions/sales-statement",
                json={"serverId": "remote_1", "gdate": "2026-06-11", "hcode": "00001",
                      "lines": [{"bcode": "3411", "gsqut": 1, "gdang": 30000, "grat1": 85, "gssum": 999}]},
            )
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "INQ_VALIDATION")

    def test_line_defaults_returns_200(self) -> None:
        async def fake_resolve(_sid, **kw):  # noqa: ARG001
            return {"bcode": "3411", "product_name": "고급영양학", "gjeja": "홍길동",
                    "gdang": 30000, "grat1": 85.0, "pubun": "위탁", "gssum": 0,
                    "source": "G4_Book", "found": True}
        with patch.object(svc, "resolve_line_defaults", side_effect=fake_resolve):
            res = self.client.get(
                "/api/v1/transactions/sales-statement/line-defaults"
                "?serverId=remote_1&bcode=3411&customer=00001&pubun=위탁&qty=2")
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["product_name"], "고급영양학")
        self.assertEqual(body["gdang"], 30000)
        # qty=2 → gssum 미리보기 재계산: 30000*2*85/100 = 51000
        self.assertEqual(body["gssum"], 51000)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    main()
