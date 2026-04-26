"""
C5 정산 Phase 2 — Sobo46/49 + 재집계 + audit 회전 UI 검증 테스트.

검증 범위 (contract `migration/contracts/settlement_billing.yaml v1.1.0`)
-----------------------------------------------------------------------
- P2-A 청구서 인쇄 (Sobo46) — DEC-034 HTML 미리보기까지
- P2-B 세금계산서 (Sobo49) — DEC-035 외부 stub / DEC-036 Chek3 토글
- P2-C 재집계 잡 (D-ST-10)   — DEC-031 마감 가드 재사용
- P2-D audit_settlement 조회 — T5d (audit 회전 UI 보조)

검증 케이스 (~31건)
-------------------
- TC-ST-P2-01~07  Sobo46 print-data + HTML 미리보기 (7건)
- TC-ST-P2-08~17  Sobo49 목록 + 토글(단건/일괄) + Sdate + issue stub + 보관본 (10건)
- TC-ST-P2-18~22  재집계 잡 (5건)
- TC-ST-P2-23~26  audit_settlement 조회 (4건)
- TC-ST-P2-27~31  i18n / data-legacy-id / DEC 정합 정적 검사 (5건)

설계 정합 (사용자 룰)
---------------------
- Phase 1 테스트(test_c5_settlement_phase1.py) 패턴 그대로 재사용 — monkeypatch + dependency_overrides.
- 신규 헬퍼 금지, 신규 fixture 디렉토리 금지. test 폴더 한 파일.
- TC-ST-P2-31 (data-legacy-id 매핑 커버리지) 는 grep 기반 정적 검사 — 실패 시 즉시 차단.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import (  # noqa: E402
    settlement_print_service,
    settlement_service,
    tax_invoice_service,
)
from app.services.returns_service import AuditTokenError  # noqa: E402
from app.services.settlement_print_service import (  # noqa: E402
    PrintDataNotFoundError,
)
from app.services.settlement_service import (  # noqa: E402
    PeriodClosedError,
    SettlementValidationError,
)
from app.services.tax_invoice_service import TaxInvoiceNotFoundError  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}


app.dependency_overrides[get_current_user] = _override_auth


# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
GDATE_MONTH = "202604"
HCODE = "H0001"
HCODE2 = "H0002"
BILLING_KEY = f"{GDATE_MONTH}|{HCODE}"
BILLING_KEY_URL = f"{GDATE_MONTH}%7C{HCODE}"
AUDIT_TOKEN = "settlement_audit_token_phase2"
AUDIT_HEADER = {"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"}

I18N_PERIOD_CLOSED = "마감된 자료입니다."
I18N_NOT_INTEGRATED = "세금계산서 외부 발행 채널이 연결되지 않았습니다. 발행 기록만 저장됩니다."


def _sample_print_data(*, gdate: str = GDATE_MONTH, hcode: str = HCODE) -> dict:
    """settlement_print_service.get_print_data 정형 응답."""
    return {
        "billing_key": {"gdate": gdate, "hcode": hcode},
        "customer": {
            "hcode": hcode, "hname": "홍길동서점", "bname": "테스트점",
            "gadd1": "서울시", "gadd2": "강남구", "gtel1": "02-0000-0000",
        },
        "summary": {
            **{f"sum{n:02d}": n * 10 for n in range(1, 49)},
            **{f"sum{n:02d}": n * 100 for n in range(51, 60)},
            **{f"sum{n:02d}": n * 1000 for n in range(61, 70)},
            "gsusu": 0, "vdate": "", "bigo1": "", "bigo2": "", "sdate": "", "chek3": "0",
        },
        "lines": [
            {
                "idx": i, "gdate": f"2026.04.{i:02d}",
                "gqut1": i, "gqut2": 0, "gqut3": 0, "gqut4": 0,
                "gqut5": 0, "gqut6": 0, "gqut7": 0,
                "name1": "강남", "name2": "테스트", "gname": "테스트화물",
                "gcode": "G01", "gsqut": 1, "gssum": 1000, "yesno": "0",
            }
            for i in range(1, 4)
        ],
        "status": {"yesno": "0", "preview_only": True},
    }


def _sample_tax_list() -> dict:
    return {
        "gdate": GDATE_MONTH,
        "items": [
            {"hcode": HCODE,  "hname": "홍길동서점", "sum26": 100000, "sum27": 10000,
             "sum28": 110000, "chek3": "0", "sdate": "", "yesno": "0"},
            {"hcode": HCODE2, "hname": "테스트서점",  "sum26": 50000,  "sum27": 5000,
             "sum28": 55000,  "chek3": "1", "sdate": "2026-04-30", "yesno": "0"},
        ],
        "total": 2,
        "totals": {"sum26": 150000, "sum27": 15000, "sum28": 165000,
                   "issued": 1, "pending": 1},
    }


class CapturingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
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


def _validate_audit_token_ok(token: str | None) -> str:
    if not token:
        raise AuditTokenError("token required")
    return token


class SettlementPhase2TestCase(TestCase):
    """C5 정산 Phase 2 검증 (~31 cases)."""

    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        for name in ("audit.settlement", "audit.audit"):
            logging.getLogger(name).addHandler(self.handler)
            logging.getLogger(name).setLevel(logging.INFO)
        self._patcher_token = patch(
            "app.routers.settlement._validate_audit_token",
            side_effect=_validate_audit_token_ok,
        )
        self._patcher_token.start()

    def tearDown(self) -> None:
        self._patcher_token.stop()
        for name in ("audit.settlement", "audit.audit"):
            logging.getLogger(name).removeHandler(self.handler)

    # ────────────────────────────────────────────────
    # P2-A Sobo46 청구서 인쇄 (DEC-034)
    # ────────────────────────────────────────────────
    def test_TC_ST_P2_01_print_data_returns_67_summary_fields(self) -> None:
        """print-data 응답에 67개 sumXX (sum01~48 + sum51~59 + sum61~69) 모두 포함."""
        with patch.object(
            settlement_print_service, "get_print_data",
            return_value=_sample_print_data(),
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print-data",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        summary = body["summary"]
        expected_keys = (
            [f"sum{n:02d}" for n in range(1, 49)]
            + [f"sum{n:02d}" for n in range(51, 60)]
            + [f"sum{n:02d}" for n in range(61, 70)]
        )
        for k in expected_keys:
            self.assertIn(k, summary, f"missing summary key {k}")
        self.assertEqual(len(expected_keys), 66)
        # 부가 67번째 = gsusu
        self.assertIn("gsusu", summary)

    def test_TC_ST_P2_02_print_data_status_preview_only(self) -> None:
        with patch.object(
            settlement_print_service, "get_print_data",
            return_value=_sample_print_data(),
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print-data",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["status"]["preview_only"])

    def test_TC_ST_P2_03_print_data_404_when_not_found(self) -> None:
        with patch.object(
            settlement_print_service, "get_print_data",
            side_effect=PrintDataNotFoundError("해당 거래처의 청구 자료가 없습니다."),
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print-data",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["detail"]["code"], "ST_NOT_FOUND")

    def test_TC_ST_P2_04_print_data_invalid_billing_key(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/billing/invalid_key/print-data",
            params={"serverId": "remote_1"},
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "ST_VALIDATION")

    def test_TC_ST_P2_05_print_html_returns_html(self) -> None:
        sample_html = "<html><body data-legacy-id='Sobo46.Header.Hname'>OK</body></html>"
        with patch.object(
            settlement_print_service, "render_preview_html",
            return_value=sample_html,
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.headers["content-type"])
        self.assertIn("data-legacy-id", res.text)

    def test_TC_ST_P2_06_print_html_includes_preview_banner(self) -> None:
        """DEC-034 — 미리보기 안내 배너 포함."""
        # 실제 render_preview_html 의 텍스트 부분을 직접 호출하여 확인
        with patch.object(
            settlement_print_service, "get_print_data",
            return_value=_sample_print_data(),
        ):
            from asyncio import new_event_loop
            loop = new_event_loop()
            try:
                html = loop.run_until_complete(
                    settlement_print_service.render_preview_html(
                        server_id="remote_1", gdate=GDATE_MONTH, hcode=HCODE,
                    )
                )
            finally:
                loop.close()
        self.assertIn("미리보기", html)
        self.assertIn("data-legacy-id='Sobo46.Header.Hname'", html)
        # 67 합계 중 핵심 3건 노출
        for key in ("Sobo46.Summary.Sum26", "Sobo46.Summary.Sum27", "Sobo46.Summary.Sum28"):
            self.assertIn(key, html)

    def test_TC_ST_P2_07_print_data_does_not_apply_period_close_guard(self) -> None:
        """DEC-034 — 미리보기는 읽기 전용이므로 마감(yesno='1') 이어도 200."""
        sample = _sample_print_data()
        sample["status"]["yesno"] = "1"
        with patch.object(
            settlement_print_service, "get_print_data", return_value=sample,
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print-data",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"]["yesno"], "1")

    # ────────────────────────────────────────────────
    # P2-B Sobo49 세금계산서 (DEC-035 / DEC-036)
    # ────────────────────────────────────────────────
    def test_TC_ST_P2_08_tax_list_returns_items_with_chek3(self) -> None:
        with patch.object(
            tax_invoice_service, "list_tax_invoices",
            return_value=_sample_tax_list(),
        ):
            res = self.client.get(
                "/api/v1/settlement/tax-invoice",
                params={"serverId": "remote_1", "gdate": GDATE_MONTH},
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["total"], 2)
        self.assertEqual(body["items"][1]["chek3"], "1")
        self.assertEqual(body["totals"]["issued"], 1)

    def test_TC_ST_P2_09_tax_list_validation_when_gdate_missing(self) -> None:
        res = self.client.get(
            "/api/v1/settlement/tax-invoice",
            params={"serverId": "remote_1"},
        )
        self.assertEqual(res.status_code, 422)

    def test_TC_ST_P2_10_chek3_toggle_single(self) -> None:
        """DEC-036 단일 진실원 — 단건 토글: scope='single', audit action='tax_chek3_toggled'."""
        with patch.object(
            tax_invoice_service, "update_chek3",
            return_value={"gdate": GDATE_MONTH, "hcode": HCODE,
                          "chek3": "1", "scope": "single"},
        ):
            res = self.client.post(
                "/api/v1/settlement/tax-invoice/chek3",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                      "hcode": HCODE, "newValue": "1"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["chek3"], "1")
        self.assertEqual(body["scope"], "single")
        actions = [r["action"] for r in self.handler.parsed()]
        self.assertIn("tax_chek3_toggled", actions)

    def test_TC_ST_P2_11_chek3_toggle_bulk(self) -> None:
        """DEC-036 일괄 — hcode 미제공 시 scope='bulk', audit action='tax_chek3_bulk'."""
        with patch.object(
            tax_invoice_service, "update_chek3",
            return_value={"gdate": GDATE_MONTH, "hcode": None,
                          "chek3": "0", "scope": "bulk"},
        ):
            res = self.client.post(
                "/api/v1/settlement/tax-invoice/chek3",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                      "hcode": None, "newValue": "0"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["scope"], "bulk")
        actions = [r["action"] for r in self.handler.parsed()]
        self.assertIn("tax_chek3_bulk", actions)

    def test_TC_ST_P2_12_chek3_toggle_period_closed_returns_423(self) -> None:
        with patch.object(
            tax_invoice_service, "update_chek3",
            side_effect=PeriodClosedError("마감된 자료입니다."),
        ):
            res = self.client.post(
                "/api/v1/settlement/tax-invoice/chek3",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                      "hcode": HCODE, "newValue": "1"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 423)
        body = res.json()
        self.assertEqual(body["detail"]["code"], "ST_PERIOD_CLOSED")
        self.assertEqual(body["detail"]["message"], I18N_PERIOD_CLOSED)

    def test_TC_ST_P2_13_chek3_toggle_requires_audit_token(self) -> None:
        res = self.client.post(
            "/api/v1/settlement/tax-invoice/chek3",
            json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                  "hcode": HCODE, "newValue": "1"},
        )
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["detail"]["code"], "ST_AUDIT_REQUIRED")

    def test_TC_ST_P2_14_chek3_invalid_value(self) -> None:
        res = self.client.post(
            "/api/v1/settlement/tax-invoice/chek3",
            json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                  "hcode": HCODE, "newValue": "X"},
            headers=AUDIT_HEADER,
        )
        # Pydantic Literal 검증 — 422
        self.assertEqual(res.status_code, 422)

    def test_TC_ST_P2_15_sdate_update_logs_audit(self) -> None:
        with patch.object(
            tax_invoice_service, "update_sdate",
            return_value={"gdate": GDATE_MONTH, "hcode": HCODE, "sdate": "2026-05-31"},
        ):
            res = self.client.post(
                "/api/v1/settlement/tax-invoice/sdate",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH,
                      "hcode": HCODE, "sdate": "2026-05-31"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["sdate"], "2026-05-31")
        actions = [r["action"] for r in self.handler.parsed()]
        self.assertIn("tax_sdate_updated", actions)

    def test_TC_ST_P2_16_issue_external_stub_returns_not_integrated(self) -> None:
        """DEC-035 — 외부 발행 채널 미연동: 200 + code='NOT_INTEGRATED' + 메시지."""
        with patch.object(
            tax_invoice_service, "issue_external_stub",
            return_value={
                "gdate": GDATE_MONTH, "hcode": HCODE, "chek3": "1",
                "external": {
                    "channel": None, "code": "NOT_INTEGRATED",
                    "message": I18N_NOT_INTEGRATED,
                },
            },
        ):
            res = self.client.post(
                f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/issue",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["chek3"], "1")
        self.assertEqual(body["external"]["code"], "NOT_INTEGRATED")
        self.assertEqual(body["external"]["message"], I18N_NOT_INTEGRATED)
        # audit 로그에 tax_issued_stub 액션 + reason 포함
        records = self.handler.parsed()
        stubs = [r for r in records if r["action"] == "tax_issued_stub"]
        self.assertTrue(stubs, "tax_issued_stub audit log missing")
        self.assertIn("DEC-035", stubs[-1].get("reason", ""))

    def test_TC_ST_P2_17_issue_billing_key_body_mismatch_returns_422(self) -> None:
        res = self.client.post(
            f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/issue",
            json={"serverId": "remote_1", "gdate": "999999", "hcode": "OTHER"},
            headers=AUDIT_HEADER,
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "ST_VALIDATION")

    def test_TC_ST_P2_18_tax_print_returns_html(self) -> None:
        sample = (
            "<html><body><span data-legacy-id='Sobo49.Print.Sum27'>0</span>"
            "<span data-legacy-id='Sobo49.Print.Chek3'>발행됨</span></body></html>"
        )
        with patch.object(
            tax_invoice_service, "render_tax_invoice_html", return_value=sample,
        ):
            res = self.client.get(
                f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/print",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.headers["content-type"])
        self.assertIn("Sobo49.Print.Chek3", res.text)

    def test_TC_ST_P2_19_tax_print_404_when_not_found(self) -> None:
        with patch.object(
            tax_invoice_service, "render_tax_invoice_html",
            side_effect=TaxInvoiceNotFoundError("해당 거래처의 세금계산서 대상이 없습니다."),
        ):
            res = self.client.get(
                f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/print",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["detail"]["code"], "ST_NOT_FOUND")

    # ────────────────────────────────────────────────
    # P2-C 재집계 잡 (D-ST-10)
    # ────────────────────────────────────────────────
    def test_TC_ST_P2_20_recalc_billing_success(self) -> None:
        sample = {
            "billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
            "updated": 1, "skipped_closed": [],
            "summary": {"sum26": 100000, "sum27": 10000, "sum28": 110000},
            "recalculated_at": "2026-04-19T00:00:00+00:00",
        }
        with patch.object(
            settlement_service, "recalc_billing", return_value=sample,
        ):
            res = self.client.post(
                "/api/v1/settlement/billing/recalc",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["updated"], 1)
        actions = [r["action"] for r in self.handler.parsed()]
        self.assertIn("billing_recalculated", actions)

    def test_TC_ST_P2_21_recalc_period_closed_returns_423(self) -> None:
        with patch.object(
            settlement_service, "recalc_billing",
            side_effect=PeriodClosedError("마감된 자료입니다."),
        ):
            res = self.client.post(
                "/api/v1/settlement/billing/recalc",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 423)
        body = res.json()
        self.assertEqual(body["detail"]["code"], "ST_PERIOD_CLOSED")
        # 마감 실패도 audit 로그 기록 (failure)
        records = [r for r in self.handler.parsed() if r["action"] == "billing_recalculated"]
        self.assertTrue(any(r["result"] == "failure" for r in records))

    def test_TC_ST_P2_22_recalc_bulk_when_hcode_none(self) -> None:
        sample = {
            "billing_key": {"gdate": GDATE_MONTH, "hcode": None},
            "updated": 5, "skipped_closed": ["H0099"],
            "summary": {"sum26": 0, "sum27": 0, "sum28": 0},
            "recalculated_at": "2026-04-19T00:00:00+00:00",
        }
        with patch.object(
            settlement_service, "recalc_billing", return_value=sample,
        ):
            res = self.client.post(
                "/api/v1/settlement/billing/recalc",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["updated"], 5)
        self.assertEqual(body["skipped_closed"], ["H0099"])

    def test_TC_ST_P2_23_recalc_validation_error(self) -> None:
        with patch.object(
            settlement_service, "recalc_billing",
            side_effect=SettlementValidationError("gdate(YYYYMM) 필수"),
        ):
            res = self.client.post(
                "/api/v1/settlement/billing/recalc",
                json={"serverId": "remote_1", "gdate": "BAD"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "ST_VALIDATION")

    def test_TC_ST_P2_24_recalc_requires_audit_token(self) -> None:
        res = self.client.post(
            "/api/v1/settlement/billing/recalc",
            json={"serverId": "remote_1", "gdate": GDATE_MONTH},
        )
        self.assertEqual(res.status_code, 401)

    # ────────────────────────────────────────────────
    # P2-D audit_settlement 조회 (T5d)
    # ────────────────────────────────────────────────
    def test_TC_ST_P2_25_audit_settlement_list(self) -> None:
        sample_items = [
            {"id": 1, "gcode": "hong01", "action": "billing_recalculated",
             "result": "success", "settlement_key": f"{GDATE_MONTH}|{HCODE}",
             "client_ip": "127.0.0.1", "server_id": "remote_1",
             "audit_token_hash": None, "reason": None,
             "extra": {"updated": 1}, "created_at": "2026-04-19T00:00:00+00:00"},
        ]
        with patch(
            "app.services.audit_password_service.list_settlement_audit",
            return_value=(sample_items, 1),
        ):
            res = self.client.get(
                "/api/v1/audit/settlement",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(len(body["items"]), 1)
        self.assertEqual(body["items"][0]["action"], "billing_recalculated")
        self.assertEqual(body["page"]["total"], 1)

    def test_TC_ST_P2_26_audit_settlement_filters_by_action(self) -> None:
        captured: dict = {}

        async def fake_list(**kwargs):
            captured.update(kwargs)
            return [], 0

        with patch(
            "app.services.audit_password_service.list_settlement_audit",
            side_effect=fake_list,
        ):
            res = self.client.get(
                "/api/v1/audit/settlement",
                params={"serverId": "remote_1", "action": "tax_chek3_toggled",
                        "gcode": "hong01", "limit": 10, "offset": 5},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(captured["action"], "tax_chek3_toggled")
        self.assertEqual(captured["gcode"], "hong01")
        self.assertEqual(captured["limit"], 10)
        self.assertEqual(captured["offset"], 5)

    def test_TC_ST_P2_27_audit_settlement_pagination_meta(self) -> None:
        with patch(
            "app.services.audit_password_service.list_settlement_audit",
            return_value=([], 0),
        ):
            res = self.client.get(
                "/api/v1/audit/settlement",
                params={"serverId": "remote_1", "limit": 50, "offset": 0},
            )
        self.assertEqual(res.status_code, 200)
        page = res.json()["page"]
        self.assertEqual(page["total"], 0)
        self.assertEqual(page["limit"], 50)
        self.assertEqual(page["offset"], 0)

    # ────────────────────────────────────────────────
    # i18n / data-legacy-id / DEC 정합 정적 검사
    # ────────────────────────────────────────────────
    def test_TC_ST_P2_28_i18n_phase2_messages_present(self) -> None:
        i18n_path = ROOT / "i18n" / "messages" / "c5.ko.json"
        data = json.loads(i18n_path.read_text(encoding="utf-8"))
        msgs = data["messages"]
        for key in (
            "c5.print.no_data",
            "c5.tax.external_not_integrated",
            "c5.recalc.started",
            "c5.recalc.completed",
            "c5.audit_rotate.gpass_done",
        ):
            self.assertIn(key, msgs, f"missing i18n key {key}")
        # DEC-035 메시지의 한국어 텍스트 일치 (NOT_INTEGRATED stub 응답 정합)
        self.assertEqual(msgs["c5.tax.external_not_integrated"]["text"], I18N_NOT_INTEGRATED)

    def test_TC_ST_P2_29_layout_mappings_files_present(self) -> None:
        for fname in ("Sobo46_billing.md", "Sobo49_tax.md"):
            path = ROOT / "analysis" / "layout_mappings" / fname
            self.assertTrue(path.exists(), f"missing layout mapping: {fname}")
            content = path.read_text(encoding="utf-8")
            self.assertIn("data-legacy-id", content)
            self.assertIn("DEC-028", content)

    def test_TC_ST_P2_30_contract_v110_includes_phase2_endpoints(self) -> None:
        """settlement_billing.yaml v1.1.0 에 Phase 2 8개 endpoint 모두 존재."""
        contract = (ROOT / "migration" / "contracts" / "settlement_billing.yaml").read_text(
            encoding="utf-8"
        )
        for path in (
            "/billing/{billing_key}/print-data",
            "/billing/recalc",
            "/tax-invoice",
            "/tax-invoice/chek3",
            "/tax-invoice/sdate",
            "/tax-invoice/{billing_key}/issue",
            "/tax-invoice/{billing_key}/print",
            "/audit/settlement",
        ):
            self.assertIn(path, contract, f"missing contract path: {path}")
        # DEC-034/035/036 모두 contract 본문에 등장
        for dec in ("DEC-034", "DEC-035", "DEC-036"):
            self.assertIn(dec, contract, f"missing decision id: {dec}")

    def test_TC_ST_P2_31_chek3_helper_is_single_source_of_truth(self) -> None:
        """DEC-036 — Chek3 토글 SQL 은 tax_invoice_service.py 에만 존재 (코드 중복 0)."""
        services_dir = BACKEND / "app" / "services"
        chek3_files: list[str] = []
        pattern = re.compile(r"UPDATE\s+T2_Ssub\s+SET\s+Chek3\s*=", re.IGNORECASE)
        for py in services_dir.glob("*.py"):
            text = py.read_text(encoding="utf-8")
            if pattern.search(text):
                chek3_files.append(py.name)
        self.assertEqual(
            chek3_files, ["tax_invoice_service.py"],
            f"Chek3 UPDATE 가 다중 파일에 존재: {chek3_files}",
        )


class StaticSettlementPrintBundleRegistryTests(TestCase):
    """정산·인쇄 잔여 4폼 + billing 별칭 — form-registry phase1 승격 정합 (T7 고정)."""

    def test_TC_ST_P2_32_form_registry_phase1_promoted(self) -> None:
        reg = (FRONTEND / "src" / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        ids = (
            "Sobo46_billing",
            "Sobo49_tax",
            "Sobo46_billing_bill",
            "Sobo49_tax_bill",
            "Settle_outstanding",
            "Sobo41_slip",
        )
        for sid in ids:
            block = re.search(rf"\{{\s*id:\s*\"{re.escape(sid)}\".*?\}}", reg, re.DOTALL)
            self.assertIsNotNone(block, f"missing FORM_REGISTRY entry: {sid}")
            self.assertIn(
                'phase: "phase1"',
                block.group(0),
                f"{sid} must be phase1 after settlement/print reclassification",
            )

    def test_TC_ST_P2_33_outstanding_slip_pages_have_legacy_root(self) -> None:
        """DEC-028 최소 루트 — 미수현황·입금전표 페이지에 data-legacy-id 존재."""
        out_p = FRONTEND / "src" / "app" / "(app)" / "settlement" / "outstanding" / "page.tsx"
        slip_p = FRONTEND / "src" / "app" / "(app)" / "settlement" / "payment-slip" / "page.tsx"
        out_src = out_p.read_text(encoding="utf-8")
        slip_src = slip_p.read_text(encoding="utf-8")
        self.assertIn('data-legacy-id="Settle_outstanding.Page"', out_src)
        self.assertIn("Settle_outstanding.Filter", out_src)
        self.assertIn("Settle_outstanding.Grid", out_src)
        self.assertIn('data-legacy-id="Sobo41_slip.Page"', slip_src)
        self.assertIn("Sobo41_slip.Card.", slip_src)


if __name__ == "__main__":
    main()
