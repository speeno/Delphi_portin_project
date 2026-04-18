"""
C6 거래/잔액 조회 — 1차 포팅(phase1) 검증 테스트.

목적
----
도서물류관리프로그램 C6 1차 합격선 (`migration/contracts/sales_inquiry.yaml.acceptance_goal`):
  "기존 사용자가 거래명세서 / 도서별수불원장 / 도서별판매 / 거래처판매 4개 화면을
   거래처·도서·일자 범위로 조회하고, S1_Memo 메모를 저장할 수 있다."
에 대해 contract `migration/contracts/sales_inquiry.yaml` v1.0.0 와 실 구현을
1:1 검증.

검증 케이스 (test pack sales_inquiry.json v1.0.0-phase1 의 1차 in_scope 항목)
- TC-INQ-001: 거래명세서 목록 (GET → items/total + customer_name lookup)
- TC-INQ-002: 거래명세서 상세 (GET → 라인 + 메모 + status)
- TC-INQ-003: S1_Memo UPSERT — INSERT 분기 (PATCH → action='inserted')
- TC-INQ-004: S1_Memo UPSERT — UPDATE 분기 (PATCH → action='updated')
- TC-INQ-005: 도서별 수불원장 (GET → opening_date + 누적 rows)
- TC-INQ-006: 도서별 판매 집계 (GET → S1_Ssub GROUP BY 결과)
- TC-INQ-007: 거래처별 판매 집계 (GET → hcode×gcode 집계)
- TC-INQ-008: 합성키 검증 — 잘못된 형식 → 422 INQ_VALIDATION
- TC-INQ-009: 라인 0건 상세 → 404 INQ_NOT_FOUND
- TC-INQ-010: 메모 UPSERT 트랜잭션 실패 → 500 + audit failure
- TC-INQ-011: 메모 UPSERT 성공 시 audit success 1건 (5축 audit 검증)
- TC-INQ-012: 미인증 호출 — 본 테스트는 의존성 override 로 인증 통과.

부수 검증 (DEC-016~018 1차 동결 부합)
- DEC-016: 권한키 미적용 — 라우터 RBAC 미존재.
- DEC-017: 인쇄 기능 미적용 — 인쇄 엔드포인트 미존재.
- DEC-018: 바코드 입력 미적용 — 바코드 엔드포인트 미존재.

주의
----
실 DB 연결 없이 transactions/inventory/reports_service 내부 함수만 monkeypatch.
사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import (  # noqa: E402
    inventory_service,
    reports_service,
    transactions_service,
)


def _override_auth() -> dict:
    """JWT 검증을 우회 — 모든 테스트는 인증된 사용자로 가정."""
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


VALID_KEY_PATH = "2026.04.18%7CA0001%7C120000000001%7C1"  # gdate|hcode|jubun|gjisa
VALID_KEY = {
    "gdate": "2026.04.18",
    "hcode": "A0001",
    "jubun": "120000000001",
    "gjisa": "1",
}


class CapturingHandler(logging.Handler):
    """audit.outbound 로거 (memo UPSERT audit) 캡처."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:  # noqa: D401
        self.records.append(record)

    def parsed(self) -> list[dict]:
        out: list[dict] = []
        for r in self.records:
            msg = r.getMessage()
            idx = msg.find("{")
            if idx < 0:
                continue
            try:
                out.append(json.loads(msg[idx:]))
            except json.JSONDecodeError:
                continue
        return out


# ---------------------------------------------------------------
# 1) 거래명세서 (Sobo21) — 목록 / 상세 / 메모
# ---------------------------------------------------------------

class C6SalesStatementTests(TestCase):
    """SQL-INQ-1 ~ SQL-INQ-4 라우터 검증."""

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        self.audit_logger = logging.getLogger("audit.outbound")
        self.audit_logger.addHandler(self.handler)
        self.audit_logger.setLevel(logging.INFO)

    def tearDown(self) -> None:
        self.audit_logger.removeHandler(self.handler)

    # -- TC-INQ-001 목록 ---------------------------------------------------

    def test_tc_inq_001_list_returns_items_and_total(self) -> None:
        async def fake_list(**kwargs):  # noqa: ARG001
            items = [
                {
                    "order_key": VALID_KEY,
                    "customer_name": "테스트거래처",
                    "row_count": 3,
                    "qty": 12,
                    "amount": 120_000,
                    "status": "active",
                }
            ]
            return items, len(items)

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get(
                "/api/v1/transactions/sales-statement"
                "?serverId=remote_1&hcode=A0001"
                "&dateFrom=2026-04-11&dateTo=2026-04-18"
            )

        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["total"], 1)
        self.assertEqual(body["items"][0]["customer_name"], "테스트거래처")
        self.assertEqual(body["items"][0]["row_count"], 3)
        self.assertEqual(body["items"][0]["status"], "active")

    # -- TC-INQ-002 상세 ---------------------------------------------------

    def test_tc_inq_002_detail_returns_lines_and_memo(self) -> None:
        async def fake_detail(**kwargs):  # noqa: ARG001
            return {
                "order_key": VALID_KEY,
                "customer": {"hcode": "A0001", "gname": "테스트거래처"},
                "status": "active",
                "lines": [
                    {
                        "gcode": "G01", "bcode": "B0001",
                        "product_name": "테스트도서", "pubun": "신간",
                        "gsqut": 5, "gssum": 50_000, "gbigo": "",
                    }
                ],
                "memo": {"gbigo": "테스트", "sbigo": "", "gtel1": "010-0000-0000",
                         "gtel2": "", "gname": "테스트거래처", "gpost": "06000"},
            }

        with patch.object(
            transactions_service, "get_sales_statement_detail",
            side_effect=fake_detail,
        ):
            res = self.client.get(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}"
                "?serverId=remote_1"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["lines"]), 1)
        self.assertEqual(body["lines"][0]["bcode"], "B0001")
        self.assertEqual(body["memo"]["gbigo"], "테스트")
        self.assertEqual(body["customer"]["gname"], "테스트거래처")

    # -- TC-INQ-003 / 004 — UPSERT INSERT/UPDATE 분기 -----------------------

    def test_tc_inq_003_memo_inserted_branch(self) -> None:
        async def fake_upsert(**kwargs):  # noqa: ARG001
            return {
                "order_key": VALID_KEY,
                "action": "inserted",
                "updated_at": "2026-04-18T03:00:00+00:00",
            }

        with patch.object(
            transactions_service, "upsert_memo", side_effect=fake_upsert
        ):
            res = self.client.patch(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}/memo",
                json={"serverId": "remote_1", "gname": "신규입력"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "inserted")

    def test_tc_inq_004_memo_updated_branch(self) -> None:
        async def fake_upsert(**kwargs):  # noqa: ARG001
            return {
                "order_key": VALID_KEY,
                "action": "updated",
                "updated_at": "2026-04-18T04:00:00+00:00",
            }

        with patch.object(
            transactions_service, "upsert_memo", side_effect=fake_upsert
        ):
            res = self.client.patch(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}/memo",
                json={"serverId": "remote_1", "gbigo": "수정"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "updated")

    # -- TC-INQ-008 합성키 검증 -------------------------------------------

    def test_tc_inq_008_invalid_order_key_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/transactions/sales-statement/INVALIDKEY?serverId=remote_1"
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "INQ_VALIDATION")

    # -- TC-INQ-009 라인 0건 → 404 ---------------------------------------

    def test_tc_inq_009_detail_not_found_returns_404(self) -> None:
        async def fake_detail(**kwargs):  # noqa: ARG001
            return None

        with patch.object(
            transactions_service, "get_sales_statement_detail",
            side_effect=fake_detail,
        ):
            res = self.client.get(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}"
                "?serverId=remote_1"
            )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["detail"]["code"], "INQ_NOT_FOUND")

    # -- TC-INQ-010 메모 UPSERT 실패 → 500 + audit failure -----------------

    def test_tc_inq_010_memo_upsert_db_error_returns_500_and_audit_failure(self) -> None:
        async def fake_upsert(**kwargs):  # noqa: ARG001
            raise RuntimeError("simulated db error")

        with patch.object(
            transactions_service, "upsert_memo", side_effect=fake_upsert
        ):
            res = self.client.patch(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}/memo",
                json={"serverId": "remote_1", "gbigo": "fail"},
            )
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json()["detail"]["code"], "INQ_TX_FAILED")

        records = self.handler.parsed()
        failures = [r for r in records if r.get("result") == "failure"]
        self.assertGreaterEqual(len(failures), 1)

    # -- TC-INQ-011 메모 UPSERT 성공 audit 5축 ----------------------------

    def test_tc_inq_011_memo_upsert_success_audit_fields(self) -> None:
        async def fake_upsert(**kwargs):  # noqa: ARG001
            return {
                "order_key": VALID_KEY,
                "action": "updated",
                "updated_at": "2026-04-18T04:00:00+00:00",
            }

        with patch.object(
            transactions_service, "upsert_memo", side_effect=fake_upsert
        ):
            self.client.patch(
                f"/api/v1/transactions/sales-statement/{VALID_KEY_PATH}/memo",
                json={"serverId": "remote_1", "gbigo": "ok"},
                headers={"X-Forwarded-For": "203.0.113.5"},
            )
        records = self.handler.parsed()
        ok = [r for r in records if r.get("result") == "success"]
        self.assertGreaterEqual(len(ok), 1)
        first = ok[0]
        # Contract equivalence.audit.fields 검증 (5축 — actor/action/result/object/ip)
        for field in ("gcode", "action", "result", "order_key", "client_ip"):
            self.assertIn(field, first)


# ---------------------------------------------------------------
# 2) 도서별 수불원장 (Sobo31)
# ---------------------------------------------------------------

class C6InventoryLedgerTests(TestCase):
    """SQL-INQ-5 + SQL-INQ-6 + 누적 로직."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    # -- TC-INQ-005 정상 응답 ---------------------------------------------

    def test_tc_inq_005_ledger_returns_opening_and_rows(self) -> None:
        async def fake_ledger(**kwargs):  # noqa: ARG001
            return {
                "opening_date": "2026.03.31",
                "rows": [
                    {
                        "gdate": "2026.04.01", "gcode": "B0001", "gname": "테스트도서",
                        "giqut": 10, "gbqut": 0, "gpqut": 0, "gjqut": 5,
                        "goqut": 5, "gisum": 100_000, "gosum": 50_000,
                        "gbsum": 0, "gjsum": 0, "gpsum": 0,
                    }
                ],
            }

        with patch.object(
            inventory_service, "get_inventory_ledger", side_effect=fake_ledger
        ):
            res = self.client.get(
                "/api/v1/inventory/ledger"
                "?serverId=remote_1&hcode=A0001&bcode=B0001"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["opening_date"], "2026.03.31")
        self.assertEqual(body["rows"][0]["giqut"], 10)
        self.assertEqual(body["rows"][0]["goqut"], 5)

    # -- 단위: _accumulate_row 분기 -------------------------------------

    def test_inventory_accumulate_row_inbound(self) -> None:
        target: dict[str, int] = {}
        inventory_service._accumulate_row(
            target, scode="Y", gubun="입고", pubun="신간", gsqut=10, gssum=100_000
        )
        self.assertEqual(target.get("giqut"), 10)

    def test_inventory_accumulate_row_outbound(self) -> None:
        target: dict[str, int] = {}
        inventory_service._accumulate_row(
            target, scode="X", gubun="출고", pubun="신간", gsqut=3, gssum=30_000
        )
        self.assertEqual(target.get("goqut"), 3)
        self.assertEqual(target.get("gosum"), 30_000)

    def test_inventory_accumulate_row_returns(self) -> None:
        target: dict[str, int] = {}
        inventory_service._accumulate_row(
            target, scode="Y", gubun="반품", pubun="반품", gsqut=2, gssum=20_000
        )
        # Subu31 L401 — Scode='Y' AND Pubun='반품' → gisum += gsqut
        self.assertEqual(target.get("gisum"), 2)


# ---------------------------------------------------------------
# 3) 도서별 / 거래처별 판매 (Sobo61 / Sobo62)
# ---------------------------------------------------------------

class C6ReportsTests(TestCase):
    """SQL-INQ-7 + SQL-INQ-8 + SQL-INQ-9."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    # -- TC-INQ-006 도서별 판매 -------------------------------------------

    def test_tc_inq_006_book_sales_returns_rows(self) -> None:
        async def fake_book(**kwargs):  # noqa: ARG001
            return {
                "rows": [
                    {
                        "gcode": "B0001", "gname": "테스트도서",
                        "giqut": 10, "gbqut": 1, "gpqut": 0, "gjqut": 4,
                        "goqut": 5, "gosum": 50_000, "gpsum": 0,
                    }
                ],
                "total": 1,
            }

        with patch.object(
            reports_service, "get_book_sales", side_effect=fake_book
        ):
            res = self.client.get(
                "/api/v1/reports/book-sales"
                "?serverId=remote_1&hcode=A0001"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["total"], 1)
        self.assertEqual(body["rows"][0]["gcode"], "B0001")

    # -- TC-INQ-007 거래처별 판매 ----------------------------------------

    def test_tc_inq_007_customer_sales_returns_rows(self) -> None:
        async def fake_cust(**kwargs):  # noqa: ARG001
            return {
                "rows": [
                    {
                        "hcode": "A0001", "gcode": "B0001", "gname": "테스트도서",
                        "gjisa": "1", "goqut": 5, "gosum": 50_000,
                        "gbqut": 0, "gbsum": 0, "gjqut": 4, "gjsum": 40_000,
                        "gsusu": 0, "gssum": 0,
                    }
                ],
                "total": 1,
            }

        with patch.object(
            reports_service, "get_customer_sales", side_effect=fake_cust
        ):
            res = self.client.get(
                "/api/v1/reports/customer-sales"
                "?serverId=remote_1"
                "&dateFrom=2026-04-01&dateTo=2026-04-30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["total"], 1)
        self.assertEqual(body["rows"][0]["hcode"], "A0001")


# ---------------------------------------------------------------
# 4) DEC-016/017/018 — 1차 제외 항목 부재 확인
# ---------------------------------------------------------------

class C6DeferralsTests(TestCase):
    """1차 제외 결정 (권한키/인쇄/바코드) 의 코드 부재 확인."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_dec_016_no_permission_branch(self) -> None:
        """모든 인증 사용자가 권한키 분기 없이 통과."""
        async def fake_list(**kwargs):  # noqa: ARG001
            return [], 0

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get(
                "/api/v1/transactions/sales-statement"
                "?serverId=remote_1&hcode=A0001"
                "&dateFrom=2026-04-11&dateTo=2026-04-18"
            )
        self.assertEqual(res.status_code, 200)

    def test_dec_017_no_print_endpoint(self) -> None:
        """`/print` 보조 엔드포인트가 없어야 한다 (DEC-017)."""
        res = self.client.get(
            "/api/v1/transactions/sales-statement/print?serverId=remote_1"
        )
        # 라우트 부재 → 404 또는 405. 200 이 나오면 DEC-017 위반.
        self.assertNotEqual(res.status_code, 200)

    def test_dec_018_no_barcode_endpoint(self) -> None:
        """`/barcode` 보조 엔드포인트가 없어야 한다 (DEC-018)."""
        res = self.client.get(
            "/api/v1/transactions/sales-statement/barcode?serverId=remote_1"
        )
        self.assertNotEqual(res.status_code, 200)


# ---------------------------------------------------------------
# 5) 서비스 내부 헬퍼 단위 (transactions_service)
# ---------------------------------------------------------------

class C6ServiceUnitTests(TestCase):
    """헬퍼 함수 정합성 — 1차 OQ-OUT-2 기반."""

    def test_normalize_gdate_dash_to_dot(self) -> None:
        self.assertEqual(
            transactions_service._normalize_gdate("2026-04-25"), "2026.04.25"
        )
        self.assertEqual(
            transactions_service._normalize_gdate("2026.04.25"), "2026.04.25"
        )
        self.assertEqual(transactions_service._normalize_gdate(""), "")

    def test_safe_int_handles_str_and_none(self) -> None:
        self.assertEqual(transactions_service._safe_int("42"), 42)
        self.assertEqual(transactions_service._safe_int(None), 0)
        self.assertEqual(transactions_service._safe_int("xx", default=7), 7)

    def test_line_status_from_yesno_max(self) -> None:
        # 모든 라인이 '2' 일 때만 cancelled
        self.assertEqual(
            transactions_service._line_status_from_yesno_max("2"), "cancelled"
        )
        self.assertEqual(
            transactions_service._line_status_from_yesno_max("1"), "active"
        )
        self.assertEqual(
            transactions_service._line_status_from_yesno_max(None), "active"
        )


if __name__ == "__main__":
    main()
