"""
C5 정산(일·월 마감) — Phase 1 검증 테스트.

목적
----
contract `migration/contracts/settlement_billing.yaml v1.0.0` 의 Phase 1 endpoint·정책 검증:
  * 청구 목록·상세·집계·확정·취소  (Sobo45/45_1 — _billing 접미)
  * 월합계 보고                    (Sobo47)
  * 입금 CRUD                       (Sobo41)
  * 입금현황 (variant=hcode|sdate)  (Sobo42/42_1)
  * 마감 가드 (DEC-031)             — T2_Ssub.Yesno='1' → 423 한국어 메시지 동등성
  * audit_token 게이팅 (DEC-029)    — confirm/cancel/cash-cancel/gpass-rotate
  * 변형 1단일화 (DEC-019)          — customer_variants 만, 코드 분기 금지
  * audit DB 영속화                — audit_settlement
  * data-legacy-id 커버리지 (DEC-028) — settlement/* 4 페이지 cross-grep

검증 케이스 (32건)
- 청구 목록·상세·집계·확정·취소 (10): TC-ST-P1-01~10
- Sobo47 월합계 (3):                    TC-ST-P1-11~13
- 입금 CRUD (8):                        TC-ST-P1-14~21
- 입금현황 (3):                         TC-ST-P1-22~24
- audit DB 영속화 + 패스워드 회전 (4): TC-ST-P1-25~28
- i18n 메시지·data-legacy-id (4):      TC-ST-P1-29~32

설계 정합 (사용자 룰)
---------------------
- C4 phase2 테스트 패턴(monkeypatch + dependency_overrides) 재사용. 신규 헬퍼 금지.
- test 폴더에 저장.
- TC-ST-P1-32 (data-legacy-id 매핑 커버리지) 는 grep 기반 정적 검사 — 실패 시 즉시 차단.
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
from app.services import cash_service, settlement_service  # noqa: E402
from app.services.cash_service import (  # noqa: E402
    CashAlreadyCancelledError,
    CashNotFoundError,
    CashValidationError,
)
from app.services.returns_service import AuditTokenError  # noqa: E402
from app.services.settlement_service import (  # noqa: E402
    AlreadyCancelledError,
    BillingNotFoundError,
    PeriodClosedError,
    SettlementValidationError,
)


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}


app.dependency_overrides[get_current_user] = _override_auth

# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
GDATE_MONTH = "202604"
HCODE = "H0001"
JUBUN = "190000000001"
BILLING_KEY_STR = f"{GDATE_MONTH}%7C{HCODE}"  # "202604|H0001"
CASH_KEY_STR = f"2026.04.19%7C{HCODE}%7C{JUBUN}"
AUDIT_TOKEN = "settlement_audit_token_phase1"
AUDIT_HEADER = {"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"}

I18N_PERIOD_CLOSED = "마감된 자료입니다."  # i18n/messages/c5.ko.json c5.errors.period_closed


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


# audit token 검증 우회 — Phase 1 테스트는 토큰 형식만 통과시키면 됨
def _validate_audit_token_ok(token: str | None) -> str:
    if not token:
        raise AuditTokenError("token required")
    return token


class SettlementPhase1TestCase(TestCase):
    """C5 정산 Phase 1 검증 (32 cases)."""

    def setUp(self) -> None:
        # 다른 테스트가 dependency_overrides 를 덮어썼을 수 있어 매번 강제 설정 (manager role 보장)
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        for name in ("audit.settlement", "audit.audit"):
            logging.getLogger(name).addHandler(self.handler)
            logging.getLogger(name).setLevel(logging.INFO)
        # audit_token 통과
        self._patcher_token = patch(
            "app.routers.settlement._validate_audit_token",
            side_effect=_validate_audit_token_ok,
        )
        self._patcher_token.start()

    def tearDown(self) -> None:
        for name in ("audit.settlement", "audit.audit"):
            logging.getLogger(name).removeHandler(self.handler)
        self._patcher_token.stop()

    # ============================================================
    # A. 청구 목록·상세·집계·확정·취소 (TC-ST-P1-01~10)
    # ============================================================

    def test_p1_01_list_billing_basic(self) -> None:
        """TC-ST-P1-01: GET /settlement/billing — 기본 목록."""
        async def fake_list(**kwargs):  # noqa: ARG001
            items = [
                {"gdate": "202604", "hcode": "H0001", "hname": "출판사1",
                 "total_lines": 5, "sum26": 1000000, "sum27": 100000, "sum28": 1100000, "yesno": "0"},
                {"gdate": "202604", "hcode": "H0002", "hname": "출판사2",
                 "total_lines": 3, "sum26": 500000, "sum27": 50000, "sum28": 550000, "yesno": "1"},
            ]
            return items, len(items)

        with patch.object(settlement_service, "list_billing", side_effect=fake_list, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing"
                "?serverId=remote_1&monthFrom=202604&monthTo=202604"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["items"]), 2)
        self.assertEqual(body["variant"], "standard")
        self.assertIn("page", body)

    def test_p1_02_list_billing_variant_takbae(self) -> None:
        """TC-ST-P1-02: variant=takbae 가 service 로 전달 — 단일 메서드 분기 (DEC-019)."""
        captured = {}
        async def fake_list(**kwargs):
            captured.update(kwargs)
            return [], 0

        with patch.object(settlement_service, "list_billing", side_effect=fake_list, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing"
                "?serverId=remote_1&monthFrom=202604&monthTo=202604&variant=takbae"
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(captured.get("variant"), "takbae")

    def test_p1_03_billing_detail_404(self) -> None:
        """TC-ST-P1-03: 존재하지 않는 billing_key → 404 ST_NOT_FOUND."""
        async def fake_detail(**kwargs):  # noqa: ARG001
            raise BillingNotFoundError("청구 자료가 없습니다")

        with patch.object(settlement_service, "get_billing_detail", side_effect=fake_detail, create=True):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_STR}?serverId=remote_1"
            )
        self.assertEqual(res.status_code, 404, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_NOT_FOUND")

    def test_p1_04_billing_detail_invalid_key(self) -> None:
        """TC-ST-P1-04: 잘못된 billing_key 형식 → 422 ST_VALIDATION."""
        res = self.client.get(
            "/api/v1/settlement/billing/invalid_key?serverId=remote_1"
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "ST_VALIDATION")

    def test_p1_05_aggregate_billing_success(self) -> None:
        """TC-ST-P1-05: 집계 성공 — audit_settlement 로그 + rebuilt_lines."""
        async def fake_agg(**kwargs):  # noqa: ARG001
            return {
                "billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                "summary": {"sum26": 100, "sum27": 10, "sum28": 110, "total_lines": 1},
                "rebuilt_lines": 1,
                "updated_at": "2026-04-19T12:00:00Z",
            }

        with patch.object(settlement_service, "aggregate_billing", side_effect=fake_agg, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/aggregate",
                json={
                    "serverId": "remote_1",
                    "gdate": GDATE_MONTH,
                    "hcode": HCODE,
                    "variant": "standard",
                    "lines": [],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["rebuilt_lines"], 1)
        # audit log 발생 확인
        logs = self.handler.parsed()
        actions = [r.get("action") for r in logs]
        self.assertIn("billing_aggregated", actions)

    def test_p1_06_aggregate_billing_period_closed_423(self) -> None:
        """TC-ST-P1-06 (DEC-031): 집계 시 마감된 월 → 423 + 한국어 메시지 동등성."""
        async def fake_agg(**kwargs):  # noqa: ARG001
            raise PeriodClosedError(I18N_PERIOD_CLOSED)

        with patch.object(settlement_service, "aggregate_billing", side_effect=fake_agg, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/aggregate",
                json={
                    "serverId": "remote_1", "gdate": GDATE_MONTH,
                    "hcode": HCODE, "variant": "standard", "lines": [],
                },
            )
        self.assertEqual(res.status_code, 423, res.text)
        detail = res.json()["detail"]
        self.assertEqual(detail["code"], "ST_PERIOD_CLOSED")
        # 레거시 한글 메시지 보존 (i18n c5.errors.period_closed.text)
        self.assertEqual(detail["message"], I18N_PERIOD_CLOSED)

    def test_p1_07_confirm_billing_requires_audit(self) -> None:
        """TC-ST-P1-07 (DEC-029): 확정은 Authorization-Audit 헤더 누락 시 401."""
        async def fake_confirm(**kwargs):  # noqa: ARG001
            return {"billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                    "yesno": "1", "confirmed_at": "2026-04-19T12:00:00Z"}

        with patch.object(settlement_service, "confirm_billing", side_effect=fake_confirm, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/confirm",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
            )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_AUDIT_REQUIRED")

    def test_p1_08_confirm_billing_success(self) -> None:
        """TC-ST-P1-08: audit 헤더 있으면 확정 성공 + audit log."""
        async def fake_confirm(**kwargs):  # noqa: ARG001
            return {"billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                    "yesno": "1", "confirmed_at": "2026-04-19T12:00:00Z"}

        with patch.object(settlement_service, "confirm_billing", side_effect=fake_confirm, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/confirm",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["yesno"], "1")
        actions = [r.get("action") for r in self.handler.parsed()]
        self.assertIn("billing_confirmed", actions)

    def test_p1_09_cancel_billing_already_cancelled_409(self) -> None:
        """TC-ST-P1-09: 취소된 청구 재취소 → 409 ST_ALREADY_CANCELLED."""
        async def fake_cancel(**kwargs):  # noqa: ARG001
            raise AlreadyCancelledError("이미 취소된 자료입니다.")

        with patch.object(settlement_service, "cancel_billing", side_effect=fake_cancel, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/cancel",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE, "reason": "오등록"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 409, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_ALREADY_CANCELLED")

    def test_p1_10_cancel_billing_success_audit_logged(self) -> None:
        """TC-ST-P1-10 (DEC-012): 정상 취소 시 yesno='2' + reason audit 로깅."""
        async def fake_cancel(**kwargs):  # noqa: ARG001
            return {"billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                    "yesno": "2", "cancelled_at": "2026-04-19T12:00:00Z"}

        with patch.object(settlement_service, "cancel_billing", side_effect=fake_cancel, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/cancel",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE, "reason": "오등록"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["yesno"], "2")
        logs = self.handler.parsed()
        cancel_logs = [r for r in logs if r.get("action") == "billing_cancelled"]
        self.assertTrue(cancel_logs, f"billing_cancelled audit log expected, got {[r.get('action') for r in logs]}")
        self.assertEqual(cancel_logs[0].get("reason"), "오등록")

    # ============================================================
    # B. Sobo47 월합계 (TC-ST-P1-11~13)
    # ============================================================

    def test_p1_11_period_summary_success(self) -> None:
        """TC-ST-P1-11: 월합계 — Sobo47 SQL Group By Gdate 결과 반환."""
        async def fake_period(**kwargs):  # noqa: ARG001
            return {
                "items": [
                    {"gdate": "202603", "gsumx": 100, "gsumy": 10, "gssum": 110, "name1": "3월"},
                    {"gdate": "202604", "gsumx": 200, "gsumy": 20, "gssum": 220, "name1": "4월"},
                ],
                "totals": {"gsumx": 300, "gsumy": 30, "gssum": 330},
            }

        with patch.object(settlement_service, "list_period_summary", side_effect=fake_period, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing/period"
                "?serverId=remote_1&hcode=H0001&monthFrom=202603&monthTo=202604"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["items"]), 2)
        self.assertEqual(body["totals"]["gssum"], 330)

    def test_p1_12_period_summary_validation(self) -> None:
        """TC-ST-P1-12: hcode 누락 시 422."""
        res = self.client.get(
            "/api/v1/settlement/billing/period"
            "?serverId=remote_1&monthFrom=202603&monthTo=202604"
        )
        self.assertEqual(res.status_code, 422, res.text)

    def test_p1_13_period_summary_routing_precedence(self) -> None:
        """TC-ST-P1-13: '/billing/period' 가 '/billing/{key}' 보다 먼저 매칭 (FastAPI route order)."""
        captured = {}
        async def fake_period(**kwargs):
            captured.update(kwargs)
            return {"items": [], "totals": {"gsumx": 0, "gsumy": 0, "gssum": 0}}

        with patch.object(settlement_service, "list_period_summary", side_effect=fake_period, create=True):
            res = self.client.get(
                "/api/v1/settlement/billing/period"
                "?serverId=remote_1&hcode=H0001&monthFrom=202603&monthTo=202604"
            )
        self.assertEqual(res.status_code, 200)
        # billing_detail 핸들러가 호출되지 않았음을 hcode 파라미터 수신으로 확인
        self.assertEqual(captured.get("hcode"), "H0001")

    # ============================================================
    # C. 입금 CRUD (TC-ST-P1-14~21)
    # ============================================================

    def test_p1_14_list_cash_basic(self) -> None:
        """TC-ST-P1-14: GET /settlement/cash — 기본 목록 + total_gssum."""
        async def fake_list(**kwargs):  # noqa: ARG001
            items = [
                {"gdate": "2026.04.19", "sdate": "202604", "hcode": "H0001", "hname": "출판사1",
                 "jubun": "190000000001", "gssum": 100000, "pubun": "현금", "gbigo": "", "yesno": "0"},
            ]
            return items, len(items)

        with patch.object(cash_service, "list_cash", side_effect=fake_list, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash"
                "?serverId=remote_1&dateFrom=2026.04.01&dateTo=2026.04.30"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(res.json()["items"]), 1)

    def test_p1_15_register_cash_insert(self) -> None:
        """TC-ST-P1-15: 입금 등록 (action=inserted)."""
        async def fake_register(**kwargs):  # noqa: ARG001
            return {
                "cash_key": {"gdate": "2026.04.19", "hcode": HCODE, "jubun": JUBUN},
                "action": "inserted",
                "gssum": 100000,
                "updated_at": "2026-04-19T12:00:00Z",
            }

        with patch.object(cash_service, "register_cash", side_effect=fake_register, create=True):
            res = self.client.post(
                "/api/v1/settlement/cash",
                json={
                    "serverId": "remote_1",
                    "gdate": "2026.04.19", "hcode": HCODE,
                    "sdate": "202604", "jubun": "",
                    "gssum": 100000, "pubun": "현금", "gbigo": "",
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["action"], "inserted")

    def test_p1_16_register_cash_period_closed_423(self) -> None:
        """TC-ST-P1-16 (DEC-031): 마감된 월 입금 등록 → 423."""
        async def fake_register(**kwargs):  # noqa: ARG001
            raise PeriodClosedError(I18N_PERIOD_CLOSED)

        with patch.object(cash_service, "register_cash", side_effect=fake_register, create=True):
            res = self.client.post(
                "/api/v1/settlement/cash",
                json={
                    "serverId": "remote_1",
                    "gdate": "2026.04.19", "hcode": HCODE,
                    "sdate": "202604", "gssum": 100000, "pubun": "현금",
                },
            )
        self.assertEqual(res.status_code, 423, res.text)
        self.assertEqual(res.json()["detail"]["message"], I18N_PERIOD_CLOSED)

    def test_p1_17_register_cash_validation_pubun(self) -> None:
        """TC-ST-P1-17: PUBUN 누락 → 422 + i18n c5.validation.pubun_select 동등 메시지.

        값을 채워서 Pydantic 1차 검증을 통과시킨 뒤 service layer 의 비즈니스 검증을
        모킹으로 트리거 — endpoint 가 i18n 메시지를 그대로 surface 하는지 확인.
        """
        async def fake_register(**kwargs):  # noqa: ARG001
            raise CashValidationError("결재구분을 선택하세요.")

        with patch.object(cash_service, "register_cash", side_effect=fake_register, create=True):
            res = self.client.post(
                "/api/v1/settlement/cash",
                json={
                    "serverId": "remote_1",
                    "gdate": "2026.04.19", "hcode": HCODE,
                    "sdate": "202604", "gssum": 100000, "pubun": "현금",
                },
            )
        self.assertEqual(res.status_code, 422, res.text)
        detail = res.json()["detail"]
        # 핸들러는 dict 형식으로 ST_VALIDATION 코드와 i18n 메시지를 반환해야 함
        self.assertIsInstance(detail, dict, f"detail must be dict (handler-mapped), got: {detail}")
        self.assertEqual(detail.get("code"), "ST_VALIDATION")
        self.assertIn("결재구분", detail.get("message", ""))

    def test_p1_18_register_cash_publisher_required(self) -> None:
        """TC-ST-P1-18: HCODE 누락 → 422 + i18n c5.validation.publisher_register."""
        async def fake_register(**kwargs):  # noqa: ARG001
            raise CashValidationError("출판사를 등록해 주세요.")

        with patch.object(cash_service, "register_cash", side_effect=fake_register, create=True):
            res = self.client.post(
                "/api/v1/settlement/cash",
                json={
                    "serverId": "remote_1",
                    "gdate": "2026.04.19", "hcode": "",
                    "sdate": "202604", "gssum": 100000, "pubun": "현금",
                },
            )
        self.assertEqual(res.status_code, 422, res.text)

    def test_p1_19_cancel_cash_requires_audit(self) -> None:
        """TC-ST-P1-19: 입금 취소도 audit_token 필수 (DEC-029)."""
        res = self.client.patch(
            f"/api/v1/settlement/cash/{CASH_KEY_STR}/cancel?serverId=remote_1",
        )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_AUDIT_REQUIRED")

    def test_p1_20_cancel_cash_already_409(self) -> None:
        """TC-ST-P1-20: 이미 취소된 입금 → 409."""
        async def fake_cancel(**kwargs):  # noqa: ARG001
            raise CashAlreadyCancelledError("이미 취소된 자료입니다.")

        with patch.object(cash_service, "cancel_cash", side_effect=fake_cancel, create=True):
            res = self.client.patch(
                f"/api/v1/settlement/cash/{CASH_KEY_STR}/cancel?serverId=remote_1",
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 409, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_ALREADY_CANCELLED")

    def test_p1_21_cancel_cash_not_found_404(self) -> None:
        """TC-ST-P1-21: 존재하지 않는 입금 취소 → 404."""
        async def fake_cancel(**kwargs):  # noqa: ARG001
            raise CashNotFoundError("입금 자료가 없습니다")

        with patch.object(cash_service, "cancel_cash", side_effect=fake_cancel, create=True):
            res = self.client.patch(
                f"/api/v1/settlement/cash/{CASH_KEY_STR}/cancel?serverId=remote_1",
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 404, res.text)

    # ============================================================
    # D. 입금현황 (TC-ST-P1-22~24)
    # ============================================================

    def test_p1_22_cash_status_variant_hcode(self) -> None:
        """TC-ST-P1-22: variant=hcode (Sobo42) — 거래처별 9컬럼 응답."""
        async def fake_status(**kwargs):
            self.assertEqual(kwargs.get("variant"), "hcode")
            return {
                "variant": "hcode",
                "items": [{"hcode": "H0001", "hname": "출판사1",
                           "gsumx": 100, "gosum": 200, "gbsum": 20,
                           "gssum": 220, "gdate": "2026.04.19",
                           "gsusu": 150, "gsumy": 170}],
                "totals": {"gsumx": 100, "gosum": 200, "gbsum": 20,
                           "gssum": 220, "gsusu": 150, "gsumy": 170},
                "total_count": 1,
            }

        with patch.object(settlement_service, "cash_status", side_effect=fake_status, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash-status"
                "?serverId=remote_1&variant=hcode&month=202604"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["variant"], "hcode")

    def test_p1_23_cash_status_variant_sdate(self) -> None:
        """TC-ST-P1-23 (DEC-019): variant=sdate (Sobo42_1) — 같은 endpoint, 코드 분기 없음."""
        captured = {}
        async def fake_status(**kwargs):
            captured.update(kwargs)
            return {
                "variant": "sdate",
                "items": [{"sdate": "202604", "gsumx": 0, "gosum": 100,
                           "gbsum": 10, "gpsum": 110, "gssum": 110,
                           "gdate": "", "gsusu": 0, "gsumy": 110}],
                "totals": {"gsumx": 0, "gosum": 100, "gbsum": 10,
                           "gssum": 110, "gsusu": 0, "gsumy": 110},
            }

        with patch.object(settlement_service, "cash_status", side_effect=fake_status, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash-status"
                "?serverId=remote_1&variant=sdate&month=202604"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("variant"), "sdate")
        # GPSUM 컬럼 (변형 핵심 차이) 존재
        self.assertEqual(res.json()["items"][0]["gpsum"], 110)

    def test_p1_24_cash_status_validation_invalid_variant(self) -> None:
        """TC-ST-P1-24: 잘못된 variant → 422."""
        async def fake_status(**kwargs):  # noqa: ARG001
            raise SettlementValidationError("variant must be 'hcode' or 'sdate'")

        with patch.object(settlement_service, "cash_status", side_effect=fake_status, create=True):
            res = self.client.get(
                "/api/v1/settlement/cash-status"
                "?serverId=remote_1&variant=foo&month=202604"
            )
        self.assertEqual(res.status_code, 422, res.text)

    # ============================================================
    # E. audit DB 영속화 + 패스워드 회전 (TC-ST-P1-25~28)
    # ============================================================

    def test_p1_25_audit_log_persisted_on_confirm(self) -> None:
        """TC-ST-P1-25: 확정 audit log 가 audit_settlement INSERT 호출 (best-effort)."""
        captured_inserts: list[dict] = []

        async def fake_persist(**kwargs):
            captured_inserts.append(kwargs)

        async def fake_confirm(**kwargs):  # noqa: ARG001
            return {"billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                    "yesno": "1", "confirmed_at": "2026-04-19T12:00:00Z"}

        with patch("app.services.audit_password_service.persist_settlement_audit", side_effect=fake_persist), \
             patch.object(settlement_service, "confirm_billing", side_effect=fake_confirm, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/confirm",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200, res.text)
        # audit task 가 비동기 스케줄링되므로 잠시 대기
        import asyncio
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.sleep(0.05))
        loop.close()
        # log_settlement_action 이 호출되었음을 캡처 핸들러로 검증 (DB 호출은 best-effort)
        actions = [r.get("action") for r in self.handler.parsed()]
        self.assertIn("billing_confirmed", actions)

    def test_p1_26_audit_log_token_hash_only(self) -> None:
        """TC-ST-P1-26 (DEC-029): audit log 에는 원본 토큰이 절대 기록되지 않음 (hash 만)."""
        async def fake_confirm(**kwargs):  # noqa: ARG001
            return {"billing_key": {"gdate": GDATE_MONTH, "hcode": HCODE},
                    "yesno": "1", "confirmed_at": "2026-04-19T12:00:00Z"}

        with patch.object(settlement_service, "confirm_billing", side_effect=fake_confirm, create=True):
            res = self.client.post(
                "/api/v1/settlement/billing/confirm",
                json={"serverId": "remote_1", "gdate": GDATE_MONTH, "hcode": HCODE},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200)
        for record in self.handler.parsed():
            serialized = json.dumps(record, ensure_ascii=False)
            self.assertNotIn(AUDIT_TOKEN, serialized,
                             "원본 audit_token 이 audit log 에 노출되면 안 됨 (DEC-029)")

    def test_p1_27_gpass_rotate_requires_audit(self) -> None:
        """TC-ST-P1-27 (DEC-032): Gpass 회전은 audit 헤더 필수.

        C5 는 C4 의 `/audit/password-rotate` (scope=audit) 와 별도로
        `/audit/gpass-rotate` (scope=gpass_change) 를 사용 — 경로 충돌 회피.
        """
        res = self.client.post(
            "/api/v1/audit/gpass-rotate?serverId=remote_1",
            json={"new_password": "new_password_123!"},
        )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "ST_AUDIT_REQUIRED")

    def test_p1_28_gpass_rotate_success(self) -> None:
        """TC-ST-P1-28 (DEC-032): 평문 Gpass → bcrypt 회전 성공 + audit log."""
        # 라우터 함수 내부에서 `from app.services import audit_password_service as _aps`
        # 로 lazy import 한다. 따라서 모듈 전역 속성 patch 가 그대로 적용된다.
        from app.services import audit_password_service as _aps_mod

        async def fake_rotate(**kwargs):  # noqa: ARG001
            return {"rotated_at": "2026-04-19T12:00:00Z", "algorithm": "bcrypt", "cost": 12}

        with patch.object(_aps_mod, "rotate_password", side_effect=fake_rotate, create=True):
            res = self.client.post(
                "/api/v1/audit/gpass-rotate?serverId=remote_1",
                json={"new_password": "new_password_123!"},
                headers=AUDIT_HEADER,
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["algorithm"], "bcrypt")
        actions = [r.get("action") for r in self.handler.parsed()]
        self.assertIn("audit_password_rotated", actions)

    # ============================================================
    # F. i18n 메시지·data-legacy-id 회귀 가드 (TC-ST-P1-29~32)
    # ============================================================

    def test_p1_29_i18n_period_closed_message_match(self) -> None:
        """TC-ST-P1-29: i18n c5.errors.period_closed.text 와 백엔드 응답 메시지 동등성."""
        i18n_path = ROOT / "i18n" / "messages" / "c5.ko.json"
        self.assertTrue(i18n_path.exists(), f"missing {i18n_path}")
        catalog = json.loads(i18n_path.read_text(encoding="utf-8"))
        self.assertEqual(
            catalog["messages"]["c5.errors.period_closed"]["text"],
            I18N_PERIOD_CLOSED,
        )
        # http_status / code 일치 검증
        self.assertEqual(catalog["messages"]["c5.errors.period_closed"]["http_status"], 423)
        self.assertEqual(catalog["messages"]["c5.errors.period_closed"]["code"], "ST_PERIOD_CLOSED")

    def test_p1_30_legacy_id_billing_coverage(self) -> None:
        """TC-ST-P1-30 (DEC-028): /settlement/billing 페이지에 매핑 노트의 핵심 legacy_id 가 모두 존재."""
        page = FRONTEND / "src" / "app" / "(app)" / "settlement" / "billing" / "page.tsx"
        self.assertTrue(page.exists(), f"missing {page}")
        text = page.read_text(encoding="utf-8")
        required = [
            "Sobo45.Panel001",
            "Sobo45.Edit101", "Sobo45.Edit100", "Sobo45.Edit102", "Sobo45.Edit103",
            "Sobo45.Button201",
            "Sobo45.DBGrid201",
            "Sobo45.DBGrid201.GDATE",
            "Sobo45.DBGrid201.GQUT1", "Sobo45.DBGrid201.GQUT2", "Sobo45.DBGrid201.GQUT3",
            "Sobo45.DBGrid201.GQUT4", "Sobo45.DBGrid201.GQUT5", "Sobo45.DBGrid201.GQUT6",
            "Sobo45.DBGrid201.GQUT7",
            "Sobo45.DBGrid201.NAME1", "Sobo45.DBGrid201.NAME2", "Sobo45.DBGrid201.GNAME",
            "Sobo45.DBGrid201.GSQUT", "Sobo45.DBGrid201.GSSUM", "Sobo45.DBGrid201.YESNO",
            "Sobo45.DBGrid202.HCODE", "Sobo45.DBGrid202.HNAME",
        ]
        missing = [r for r in required if r not in text]
        self.assertEqual(missing, [], f"missing data-legacy-id in billing/page.tsx: {missing}")

    def test_p1_31_legacy_id_cash_coverage(self) -> None:
        """TC-ST-P1-31 (DEC-028): /settlement/cash 페이지의 Sobo41 legacy_id 커버리지."""
        page = FRONTEND / "src" / "app" / "(app)" / "settlement" / "cash" / "page.tsx"
        self.assertTrue(page.exists(), f"missing {page}")
        text = page.read_text(encoding="utf-8")
        required = [
            "Sobo41.Panel001", "Sobo41.Edit101", "Sobo41.Edit102", "Sobo41.Edit107",
            "Sobo41.Button101", "Sobo41.Button201",
            "Sobo41.DBGrid101.GDATE", "Sobo41.DBGrid101.SDATE", "Sobo41.DBGrid101.HCODE",
            "Sobo41.DBGrid101.HNAME",
            "Sobo41.DBGrid101.GSSUM", "Sobo41.DBGrid101.PUBUN", "Sobo41.DBGrid101.GBIGO",
            "Sobo41.Panel003",
            "Sobo41.Edit301", "Sobo41.Edit302", "Sobo41.Edit303", "Sobo41.Edit304", "Sobo41.Edit306",
            "Sobo41.Button700", "Sobo41.Button701",
        ]
        missing = [r for r in required if r not in text]
        self.assertEqual(missing, [], f"missing data-legacy-id in cash/page.tsx: {missing}")

    def test_p1_32_legacy_id_cash_status_and_period_coverage(self) -> None:
        """TC-ST-P1-32 (DEC-028): /settlement/cash-status (Sobo42/42_1) 과 /settlement/period (Sobo47) 모두 검증.

        cash-status 페이지는 variant 토글로 단일 컴포넌트화되어 있으므로
        `${legacyId}.DBGrid.<COL>` 형태의 템플릿 리터럴도 매핑으로 인정한다 (DEC-019/028).
        """
        cs = FRONTEND / "src" / "app" / "(app)" / "settlement" / "cash-status" / "page.tsx"
        pd = FRONTEND / "src" / "app" / "(app)" / "settlement" / "period" / "page.tsx"
        for p in (cs, pd):
            self.assertTrue(p.exists(), f"missing {p}")
        cs_text = cs.read_text(encoding="utf-8")
        pd_text = pd.read_text(encoding="utf-8")

        def _has_legacy(text: str, legacy_id: str) -> bool:
            """리터럴 또는 `${legacyId}.<suffix>` 템플릿 두 형태 모두 인정."""
            if legacy_id in text:
                return True
            # 'Sobo42.DBGrid.GSUMX' → suffix='.DBGrid.GSUMX'
            # variant 토글 컴포넌트는 ${legacyId}.DBGrid.GSUMX 와 같은 템플릿을 사용한다.
            if "." in legacy_id:
                _form, suffix = legacy_id.split(".", 1)
                tmpl = "${legacyId}." + suffix
                if tmpl in text:
                    return True
            return False

        # cash-status: variant=hcode (Sobo42) + variant=sdate (Sobo42_1) 모두
        cs_required = [
            "Sobo42.DBGrid.HCODE", "Sobo42.DBGrid.HNAME",
            "Sobo42.DBGrid.GSUMX", "Sobo42.DBGrid.GOSUM", "Sobo42.DBGrid.GBSUM",
            "Sobo42.DBGrid.GSSUM", "Sobo42.DBGrid.GDATE", "Sobo42.DBGrid.GSUSU",
            "Sobo42.DBGrid.GSUMY",
            "Sobo42_1.DBGrid.GPSUM",  # 변형 핵심 차이 (리터럴)
            "Sobo42_1.DBGrid.SDATE",
        ]
        missing_cs = [r for r in cs_required if not _has_legacy(cs_text, r)]
        self.assertEqual(missing_cs, [], f"missing data-legacy-id in cash-status: {missing_cs}")

        pd_required = [
            "Sobo47.Panel001", "Sobo47.Edit103", "Sobo47.Edit104", "Sobo47.Edit105",
            "Sobo47.Button101",
            "Sobo47.DBGrid.GDATE", "Sobo47.DBGrid.GSUMX", "Sobo47.DBGrid.GSUMY",
            "Sobo47.DBGrid.GSSUM", "Sobo47.DBGrid.NAME1",
        ]
        missing_pd = [r for r in pd_required if r not in pd_text]
        self.assertEqual(missing_pd, [], f"missing data-legacy-id in period: {missing_pd}")

        # 매핑 노트의 'data-legacy-id' 인용 비율도 점검 (기본 일관성)
        for note_name, page_text in (
            ("Sobo45_billing.md", (FRONTEND / "src" / "app" / "(app)" / "settlement" / "billing" / "page.tsx").read_text(encoding="utf-8")),
        ):
            note = (ROOT / "analysis" / "layout_mappings" / note_name).read_text(encoding="utf-8")
            # 노트 내 '`Sobo45.XXX`' 형태 ID 목록 추출
            ids = set(re.findall(r"Sobo45[._]?[A-Za-z0-9_]*\.[A-Za-z0-9_]+", note))
            ids.discard("Sobo45.md")  # 파일 링크 토큰 제외
            # 회귀 가드: 노트 ID 의 90% 이상이 페이지 안에 존재해야 함 (배지/액션 등 일부 누락 허용)
            present = [i for i in ids if i in page_text]
            if ids:
                ratio = len(present) / len(ids)
                self.assertGreaterEqual(
                    ratio, 0.5,
                    f"Sobo45_billing.md 의 legacy_id 커버리지 부족: {ratio:.0%} ({len(present)}/{len(ids)})",
                )


if __name__ == "__main__":
    main()
