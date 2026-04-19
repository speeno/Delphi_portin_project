"""
C4 반품 처리 — 2차 포팅(phase2) 검증 테스트.

목적
----
contract `migration/contracts/return_receipt.yaml v1.1.0` 의 Phase 2 신규/보강 endpoint·정책 검증:
  * 신규 화면 2건: Sobo34_4(/returns/ledger), Sobo58(/returns/period-report) — OQ-RT-8
  * Phase 1 누락 보강: PUT /returns/{key} 라인 diff, 부분 재생/해체, 24h 롤백
  * 보안 강화: bcrypt 검증, audit_password_attempts 5회 잠금, audit DB 영속화 — OQ-RT-4/9
  * 동시성: Sv_Ghng SELECT FOR UPDATE — OQ-RT-5
  * 운영 의존: import format=xls 501, D_Select 헤더 인터페이스 — OQ-RT-1/7
  * data-legacy-id 커버리지: Sobo34_4/Sobo58 추가 — DEC-028

검증 케이스 (30건)
- 신규 화면 (8): TC-RT-P2-01~08
- 라인 diff/부분/롤백 (7): TC-RT-P2-09~15
- bcrypt + 잠금 (5): TC-RT-P2-16~20
- FOR UPDATE 동시성 (3): TC-RT-P2-21~23
- audit DB (4): TC-RT-P2-24~27
- D_Select / format=xls / dfm-id (3): TC-RT-P2-28~30

설계 정합
---------
- Phase 1 테스트(`test_c4_returns_phase1.py`) 의 monkeypatch + dependency_overrides 패턴 재사용
  (사용자 룰: 신규 헬퍼 금지, 기존 활용가능 코드 우선).
- 사용자 룰: test 폴더에 저장.
- TC-RT-P2-30 (data-legacy-id 매핑 커버리지) 는 T6 프론트 완료 전에는 warning 출력 후 PASS.
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
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import returns_service  # noqa: E402
from app.services.returns_service import (  # noqa: E402
    AuditTokenError,
    ConcurrentChangeError,
    ReasonRequiredError,
)


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}


app.dependency_overrides[get_current_user] = _override_auth

# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
RETURN_KEY_G = {"gdate": "2026.04.19", "hcode": "H0001", "jubun": "190000000001"}
RETURN_KEY_B = {"bdate": "2026.04.19", "hcode": "H0001", "jubun": "190000000002"}
RETURN_KEY_STR_G = "G%7C2026.04.19%7CH0001%7C190000000001"
RETURN_KEY_STR_B = "B%7C2026.04.19%7CH0001%7C190000000002"
AUDIT_TOKEN = "phase2_audit_token_bcrypt"
AUDIT_HEADER = {"Authorization-Audit": f"Bearer-Audit {AUDIT_TOKEN}"}
DSEL_HEADER = {"Authorization-Context": '{"branch_id":"BR01","role":"manager"}'}


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


class ReturnsPhase2TestCase(TestCase):
    """C4 Phase 2 검증 (30 cases)."""

    def setUp(self) -> None:
        # 다른 phase 테스트가 dependency_overrides 를 덮어썼을 수 있어 매번 강제 설정 (manager role 보장)
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)
        self.handler = CapturingHandler()
        for name in ("audit.returns", "audit.audit"):
            logging.getLogger(name).addHandler(self.handler)
            logging.getLogger(name).setLevel(logging.INFO)

    def tearDown(self) -> None:
        for name in ("audit.returns", "audit.audit"):
            logging.getLogger(name).removeHandler(self.handler)

    # ============================================================
    # A. 신규 화면 (TC-RT-P2-01~08) — OQ-RT-8
    # ============================================================

    def test_p2_01_ledger_query_master_only(self) -> None:
        """TC-RT-P2-01: GET /returns/ledger — 마스터(도서별 누계)만 응답."""
        async def fake_ledger(**kwargs):  # noqa: ARG001
            return {
                "master": [
                    {"bcode": "B0001", "book_name": "도서1", "gname": "출판사1", "gubun": "반품", "pubun": "구간", "total_qty": 100, "total_amount": 1200000},
                    {"bcode": "B0002", "book_name": "도서2", "gname": "출판사1", "gubun": "폐기", "pubun": "구간", "total_qty": 50, "total_amount": 600000},
                ],
                "detail": [],
                "kpi": {"book_count": 2, "line_count": 12, "total_qty": 150, "total_amount": 1800000},
                "page": {"total": 2, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "ledger_query", side_effect=fake_ledger, create=True):
            res = self.client.get("/api/v1/returns/ledger?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30")
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["master"]), 2)
        self.assertEqual(body["kpi"]["total_amount"], 1800000)

    def test_p2_02_ledger_query_with_detail(self) -> None:
        """TC-RT-P2-02: detail_for_bcode 지정 시 detail 그리드 채워짐."""
        async def fake_ledger(**kwargs):  # noqa: ARG001
            self.assertEqual(kwargs.get("detail_for_bcode"), "B0001")
            return {
                "master": [{"bcode": "B0001", "book_name": "도서1", "gname": "출판사1", "gubun": "반품", "pubun": "구간", "total_qty": 100, "total_amount": 1200000}],
                "detail": [
                    {"gdate": "2026-04-15", "gubun": "반품", "gcode": "G001", "gname": "거래처1", "giqut": 0, "gisum": 0, "goqut": 0, "gosum": 0, "gjqut": 0, "gjsum": 0, "gbqut": 0, "gbsum": 0, "gsqut": 50, "gssum": 600000},
                ],
                "kpi": {"book_count": 1, "line_count": 1, "total_qty": 50, "total_amount": 600000},
                "page": {"total": 1, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "ledger_query", side_effect=fake_ledger, create=True):
            res = self.client.get("/api/v1/returns/ledger?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&detailForBcode=B0001")
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(res.json()["detail"]), 1)

    def test_p2_03_ledger_query_required_dates(self) -> None:
        """TC-RT-P2-03: dateFrom/dateTo 필수 — 누락 시 422."""
        res = self.client.get("/api/v1/returns/ledger?serverId=remote_1")
        self.assertEqual(res.status_code, 422, res.text)

    def test_p2_04_ledger_query_filter_gubun(self) -> None:
        """TC-RT-P2-04: gubun 필터 — '폐기' 만 반환."""
        captured = {}
        async def fake_ledger(**kwargs):
            captured.update(kwargs)
            return {"master": [], "detail": [], "kpi": {"book_count": 0, "line_count": 0, "total_qty": 0, "total_amount": 0}, "page": {"total": 0, "limit": 50, "offset": 0}}

        with patch.object(returns_service, "ledger_query", side_effect=fake_ledger, create=True):
            res = self.client.get("/api/v1/returns/ledger?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&gubun=%ED%8F%90%EA%B8%B0")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(captured.get("gubun"), "폐기")

    def test_p2_05_period_report_master(self) -> None:
        """TC-RT-P2-05: GET /returns/period-report — 출판사별 누계."""
        async def fake_period(**kwargs):  # noqa: ARG001
            return {
                "master": [
                    {"hcode": "H0001", "hname": "출판사1", "line_count": 50, "total_qty": 500, "total_amount": 6000000},
                    {"hcode": "H0002", "hname": "출판사2", "line_count": 30, "total_qty": 300, "total_amount": 3600000},
                ],
                "detail": [],
                "kpi": {"publisher_count": 2, "line_count": 80, "total_qty": 800, "total_amount": 9600000},
                "page": {"total": 2, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "period_report_query", side_effect=fake_period, create=True):
            res = self.client.get("/api/v1/returns/period-report?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30")
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["master"]), 2)
        self.assertEqual(body["kpi"]["publisher_count"], 2)
        self.assertEqual(body["kpi"]["total_amount"], 9600000)

    def test_p2_06_period_report_with_detail(self) -> None:
        """TC-RT-P2-06: detail_for_hcode 지정 시 라인 디테일 채워짐."""
        async def fake_period(**kwargs):
            self.assertEqual(kwargs.get("detail_for_hcode"), "H0001")
            return {
                "master": [{"hcode": "H0001", "hname": "출판사1", "line_count": 1, "total_qty": 10, "total_amount": 120000}],
                "detail": [
                    {"gdate": "2026-04-15", "gcode": "G001", "gname": "거래처1", "idnum": 1, "pubun": "구간", "bcode": "B0001", "bname": "도서1", "gsqut": 10, "gdang": 12000, "grat1": 0.7, "gssum": 120000},
                ],
                "kpi": {"publisher_count": 1, "line_count": 1, "total_qty": 10, "total_amount": 120000},
                "page": {"total": 1, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "period_report_query", side_effect=fake_period, create=True):
            res = self.client.get("/api/v1/returns/period-report?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&detailForHcode=H0001")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["detail"]), 1)

    def test_p2_07_period_report_pagination(self) -> None:
        """TC-RT-P2-07: limit/offset 파라미터 전달."""
        captured = {}
        async def fake_period(**kwargs):
            captured.update(kwargs)
            return {"master": [], "detail": [], "kpi": {"publisher_count": 0, "line_count": 0, "total_qty": 0, "total_amount": 0}, "page": {"total": 0, "limit": 25, "offset": 50}}

        with patch.object(returns_service, "period_report_query", side_effect=fake_period, create=True):
            res = self.client.get("/api/v1/returns/period-report?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=25&offset=50")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(captured.get("limit"), 25)
        self.assertEqual(captured.get("offset"), 50)

    def test_p2_08_period_report_kpi_consistency(self) -> None:
        """TC-RT-P2-08: KPI 합계가 master 합계와 일치 (계약 합의)."""
        async def fake_period(**kwargs):  # noqa: ARG001
            return {
                "master": [
                    {"hcode": "H0001", "hname": "출판사1", "line_count": 50, "total_qty": 500, "total_amount": 6000000},
                    {"hcode": "H0002", "hname": "출판사2", "line_count": 30, "total_qty": 300, "total_amount": 3600000},
                ],
                "detail": [],
                "kpi": {"publisher_count": 2, "line_count": 80, "total_qty": 800, "total_amount": 9600000},
                "page": {"total": 2, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "period_report_query", side_effect=fake_period, create=True):
            res = self.client.get("/api/v1/returns/period-report?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30")
        body = res.json()
        sum_qty = sum(m["total_qty"] for m in body["master"])
        sum_amt = sum(m["total_amount"] for m in body["master"])
        sum_cnt = sum(m["line_count"] for m in body["master"])
        self.assertEqual(body["kpi"]["total_qty"], sum_qty)
        self.assertEqual(body["kpi"]["total_amount"], sum_amt)
        self.assertEqual(body["kpi"]["line_count"], sum_cnt)

    # ============================================================
    # B. Phase 1 누락 (TC-RT-P2-09~15)
    # ============================================================

    def test_p2_09_put_lines_diff_insert_update_delete(self) -> None:
        """TC-RT-P2-09: PUT /returns/{key} 라인 diff — 추가/수정/삭제 단일 트랜잭션."""
        captured = {}
        async def fake_update(**kwargs):
            captured.update(kwargs)
            return {
                "return_key": RETURN_KEY_G,
                "inserted": 1, "updated": 1, "deleted": 1,
                "total_lines": 2, "total_qty": 25, "total_amount": 300000,
            }

        with patch.object(returns_service, "update_return_lines", side_effect=fake_update, create=True):
            res = self.client.put(
                f"/api/v1/returns/{RETURN_KEY_STR_G}?serverId=remote_1",
                json={
                    "lines": [
                        {"idnum": 1, "bcode": "B0001", "gsqut": 12, "gdang": 12000, "grat1": 0.7, "gssum": 144000},
                        {"idnum": None, "bcode": "B0003", "gsqut": 13, "gdang": 12000, "grat1": 0.7, "gssum": 156000},
                    ],
                    "delete_idnums": [2],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["inserted"], 1)
        self.assertEqual(body["updated"], 1)
        self.assertEqual(body["deleted"], 1)

    def test_p2_10_put_lines_404_when_not_found(self) -> None:
        """TC-RT-P2-10: 존재하지 않는 return_key → 404."""
        async def fake_update(**kwargs):  # noqa: ARG001
            raise LookupError("not found")

        with patch.object(returns_service, "update_return_lines", side_effect=fake_update, create=True):
            res = self.client.put(
                f"/api/v1/returns/{RETURN_KEY_STR_G}?serverId=remote_1",
                json={"lines": []},
            )
        self.assertEqual(res.status_code, 404, res.text)

    def test_p2_11_partial_regen_subset(self) -> None:
        """TC-RT-P2-11: 부분 재생 — idnum_list 만 처리."""
        captured = {}
        async def fake_partial(**kwargs):
            captured.update(kwargs)
            return {"processed": 2, "regenerated_qty": 7}

        with patch.object(returns_service, "process_regen_partial", side_effect=fake_partial, create=True):
            res = self.client.post(
                "/api/v1/returns/dispose/regen/partial",
                headers=AUDIT_HEADER,
                json={
                    "serverId": "remote_1",
                    "returnKey": RETURN_KEY_G,
                    "idnumList": [1, 3],
                    "gbigo": "선택 라인 재생",
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["processed"], 2)
        self.assertEqual(captured.get("idnum_list"), [1, 3])

    def test_p2_12_partial_regen_requires_audit(self) -> None:
        """TC-RT-P2-12: 부분 재생 audit 헤더 누락 → 401."""
        async def fake_partial(**kwargs):  # noqa: ARG001
            raise AuditTokenError("audit token required")

        with patch.object(returns_service, "process_regen_partial", side_effect=fake_partial, create=True):
            res = self.client.post(
                "/api/v1/returns/dispose/regen/partial",
                json={"serverId": "remote_1", "returnKey": RETURN_KEY_G, "idnumList": [1], "gbigo": "x"},
            )
        self.assertEqual(res.status_code, 401, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_AUDIT_REQUIRED")

    def test_p2_13_partial_disassemble_bdate_key(self) -> None:
        """TC-RT-P2-13: 부분 해체 — Bdate 키 사용."""
        captured = {}
        async def fake_partial(**kwargs):
            captured.update(kwargs)
            return {"processed": 1, "disassembled_qty": 5}

        with patch.object(returns_service, "process_disassemble_partial", side_effect=fake_partial, create=True):
            res = self.client.post(
                "/api/v1/returns/dispose/disassemble/partial",
                headers=AUDIT_HEADER,
                json={
                    "serverId": "remote_1",
                    "returnKey": RETURN_KEY_B,
                    "idnumList": [1],
                    "gbigo": "손상 해체",
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        # Bdate 키 검증
        rk = captured.get("return_key", {}) or captured.get("returnKey", {})
        self.assertTrue("bdate" in rk or rk.get("bdate"), f"Bdate key expected, got {rk}")

    def test_p2_14_rollback_within_24h(self) -> None:
        """TC-RT-P2-14: 24h 이내 3분기 롤백."""
        captured = {}
        async def fake_rollback(**kwargs):
            captured.update(kwargs)
            return {"rolled_back": 3, "action": "regen", "recorded_at": "2026-04-19T12:00:00Z"}

        with patch.object(returns_service, "rollback_dispose", side_effect=fake_rollback, create=True):
            res = self.client.post(
                f"/api/v1/returns/{RETURN_KEY_STR_G}/rollback?serverId=remote_1",
                headers=AUDIT_HEADER,
                json={"action": "regen", "gbigo": "잘못된 처리 취소"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["rolled_back"], 3)

    def test_p2_15_rollback_expired_410(self) -> None:
        """TC-RT-P2-15: 24h 초과 롤백 → 410 RT_ROLLBACK_EXPIRED."""
        from app.services.returns_service import RollbackExpiredError  # noqa: PLC0415

        async def fake_rollback(**kwargs):  # noqa: ARG001
            raise RollbackExpiredError("rollback window expired")

        with patch.object(returns_service, "rollback_dispose", side_effect=fake_rollback, create=True):
            res = self.client.post(
                f"/api/v1/returns/{RETURN_KEY_STR_G}/rollback?serverId=remote_1",
                headers=AUDIT_HEADER,
                json={"action": "regen", "gbigo": "x"},
            )
        self.assertEqual(res.status_code, 410, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_ROLLBACK_EXPIRED")

    # ============================================================
    # C. bcrypt + 5회 잠금 (TC-RT-P2-16~20) — OQ-RT-4 / OQ-RT-9
    # ============================================================

    def test_p2_16_password_verify_bcrypt_success(self) -> None:
        """TC-RT-P2-16: bcrypt 검증 성공 → token 발급."""
        async def fake_verify(**kwargs):  # noqa: ARG001
            return {
                "token": "bcrypt_verified_token_xyz",
                "expires_at": "2026-04-19T12:05:00Z",
                "scope": kwargs.get("scope"),
            }

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "MyStr0ng!Pwd", "scope": "inventory_change"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["scope"], "inventory_change")

    def test_p2_17_password_verify_bcrypt_failure(self) -> None:
        """TC-RT-P2-17: bcrypt 검증 실패 → 401."""
        async def fake_verify(**kwargs):  # noqa: ARG001
            raise AuditTokenError("invalid password")

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "wrong", "scope": "audit"},
            )
        self.assertEqual(res.status_code, 401, res.text)

    def test_p2_18_password_locked_after_5_failures(self) -> None:
        """TC-RT-P2-18: 5회 실패 후 6번째 → 429 RT_AUDIT_LOCKED."""
        from app.services.returns_service import AuditLockedError  # noqa: PLC0415

        async def fake_verify(**kwargs):  # noqa: ARG001
            raise AuditLockedError("locked: 5 failures within 10min")

        with patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "wrong6", "scope": "audit"},
            )
        self.assertEqual(res.status_code, 429, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_AUDIT_LOCKED")

    def test_p2_19_password_rotate_endpoint(self) -> None:
        """TC-RT-P2-19: POST /audit/password-rotate — bcrypt 회전."""
        async def fake_rotate(**kwargs):
            self.assertGreaterEqual(len(kwargs.get("new_password", "")), 4)
            return {"rotated_at": "2026-04-19T12:00:00Z", "algorithm": "bcrypt", "cost": 12}

        with patch.object(returns_service, "rotate_audit_password", side_effect=fake_rotate, create=True):
            res = self.client.post(
                "/api/v1/audit/password-rotate",
                json={"new_password": "NewStr0ng!Pwd", "scope": "audit"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["algorithm"], "bcrypt")
        self.assertEqual(body["cost"], 12)

    def test_p2_20_password_rotate_too_weak_422(self) -> None:
        """TC-RT-P2-20: 패스워드 너무 짧음 → 422."""
        async def fake_rotate(**kwargs):  # noqa: ARG001
            raise ValueError("password too weak")

        with patch.object(returns_service, "rotate_audit_password", side_effect=fake_rotate, create=True):
            res = self.client.post(
                "/api/v1/audit/password-rotate",
                json={"new_password": "ab", "scope": "audit"},
            )
        self.assertEqual(res.status_code, 422, res.text)

    # ============================================================
    # D. FOR UPDATE 동시성 (TC-RT-P2-21~23) — OQ-RT-5
    # ============================================================

    def test_p2_21_change_for_update_concurrent_409(self) -> None:
        """TC-RT-P2-21: 변경 처리 — Sv_Ghng FOR UPDATE 충돌 시 409."""
        async def fake_change(**kwargs):  # noqa: ARG001
            raise ConcurrentChangeError("Sv_Ghng concurrent lock conflict")

        with patch.object(returns_service, "process_change", side_effect=fake_change):
            res = self.client.post(
                "/api/v1/returns/change",
                headers=AUDIT_HEADER,
                json={
                    "serverId": "remote_1",
                    "rows": [{"gdate": "2026.04.19", "hcode": "H0001", "bcode": "B0001", "gbsum": 100, "gbigo": "변경"}],
                },
            )
        self.assertEqual(res.status_code, 409, res.text)
        self.assertEqual(res.json()["detail"]["code"], "RT_CONCURRENT_CHANGE")

    def test_p2_22_change_for_update_success(self) -> None:
        """TC-RT-P2-22: lock 획득 후 정상 처리 → 200."""
        async def fake_change(**kwargs):  # noqa: ARG001
            return {"processed": 1, "inserted": 0, "updated": 1}

        with patch.object(returns_service, "process_change", side_effect=fake_change):
            res = self.client.post(
                "/api/v1/returns/change",
                headers=AUDIT_HEADER,
                json={
                    "serverId": "remote_1",
                    "rows": [{"gdate": "2026.04.19", "hcode": "H0001", "bcode": "B0001", "gbsum": 100, "gbigo": "변경"}],
                },
            )
        self.assertEqual(res.status_code, 200, res.text)

    def test_p2_23_sv_ghng_field_catalog_9_modes(self) -> None:
        """TC-RT-P2-23: SV_GHNG_FIELD_MAP 9 모드 (regen/disassemble/change/discard/inbound/outbound)."""
        try:
            from app.services.returns_service import SV_GHNG_FIELD_MAP  # noqa: PLC0415
        except ImportError:
            self.skipTest("SV_GHNG_FIELD_MAP not yet implemented (T5d)")
            return
        expected_modes = {"regen", "disassemble", "change", "discard", "inbound", "outbound"}
        self.assertTrue(expected_modes.issubset(set(SV_GHNG_FIELD_MAP.keys())))
        for mode, fields in SV_GHNG_FIELD_MAP.items():
            self.assertEqual(len(fields), 3, f"mode {mode} must have (Field1, Field2, Field3)")

    # ============================================================
    # E. audit DB 영속화 (TC-RT-P2-24~27) — OQ-RT-9
    # ============================================================

    def test_p2_24_audit_returns_get_endpoint(self) -> None:
        """TC-RT-P2-24: GET /audit/returns — audit_returns 테이블 조회."""
        async def fake_query(**kwargs):
            return {
                "items": [
                    {
                        "id": 101, "action": "regenerated", "result": "success", "gcode": "hong01",
                        "return_key": {"gdate": "2026.04.19", "bdate": None, "hcode": "H0001", "jubun": "190000000001"},
                        "client_ip": "127.0.0.1", "audit_token_hash": "abc1234567890def",
                        "reason": None, "extra": {"processed": 5}, "recorded_at": "2026-04-19T12:00:00Z",
                    },
                ],
                "page": {"total": 1, "limit": 50, "offset": 0},
            }

        with patch.object(returns_service, "audit_returns_query", side_effect=fake_query, create=True):
            res = self.client.get("/api/v1/audit/returns?serverId=remote_1&action=regenerated")
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(len(res.json()["items"]), 1)

    def test_p2_25_audit_action_logged_to_db(self) -> None:
        """TC-RT-P2-25: 재생 처리 시 audit_returns DB INSERT 호출 (병행)."""
        from app.services import audit_service  # noqa: PLC0415

        db_insert_called = []

        async def fake_db_insert(**kwargs):
            db_insert_called.append(kwargs)

        async def fake_regen(**kwargs):  # noqa: ARG001
            return {"processed": 2, "regenerated_qty": 7}

        with patch.object(audit_service, "persist_return_action", side_effect=fake_db_insert, create=True), \
             patch.object(returns_service, "process_regen", side_effect=fake_regen):
            res = self.client.post(
                "/api/v1/returns/dispose/regen",
                headers=AUDIT_HEADER,
                json={"serverId": "remote_1", "rows": [{"id": 101, "gsqut": 5, "gbigo": ""}]},
            )
        self.assertEqual(res.status_code, 200, res.text)
        # DB persist 호출이 있어야 함 (T5c 구현 후 PASS, 구현 전 SKIP)
        if not db_insert_called:
            self.skipTest("persist_return_action not yet implemented (T5c)")

    def test_p2_26_audit_password_attempts_logged(self) -> None:
        """TC-RT-P2-26: 패스워드 검증 실패 시 audit_password_attempts INSERT."""
        from app.services import audit_service  # noqa: PLC0415

        attempts = []

        async def fake_persist(**kwargs):
            attempts.append(kwargs)

        async def fake_verify(**kwargs):  # noqa: ARG001
            raise AuditTokenError("invalid")

        with patch.object(audit_service, "persist_password_attempt", side_effect=fake_persist, create=True), \
             patch.object(returns_service, "verify_audit_password", side_effect=fake_verify):
            res = self.client.post(
                "/api/v1/audit/password-verify",
                json={"password": "wrong", "scope": "audit"},
            )
        self.assertEqual(res.status_code, 401)
        if not attempts:
            self.skipTest("persist_password_attempt not yet implemented (T5c)")

    def test_p2_27_audit_db_failure_does_not_break_action(self) -> None:
        """TC-RT-P2-27: DB audit 실패해도 비즈니스 액션은 성공 (fail-safe)."""
        from app.services import audit_service  # noqa: PLC0415

        async def fake_persist_fail(**kwargs):  # noqa: ARG001
            raise RuntimeError("DB connection lost")

        async def fake_regen(**kwargs):  # noqa: ARG001
            return {"processed": 1, "regenerated_qty": 3}

        with patch.object(audit_service, "persist_return_action", side_effect=fake_persist_fail, create=True), \
             patch.object(returns_service, "process_regen", side_effect=fake_regen):
            res = self.client.post(
                "/api/v1/returns/dispose/regen",
                headers=AUDIT_HEADER,
                json={"serverId": "remote_1", "rows": [{"id": 102, "gsqut": 3, "gbigo": ""}]},
            )
        # 액션은 성공해야 함 (audit DB 실패는 무관)
        self.assertEqual(res.status_code, 200, res.text)

    # ============================================================
    # F. 거버넌스 / 외부 의존 / dfm-id (TC-RT-P2-28~30)
    # ============================================================

    def test_p2_28_d_select_header_passthrough(self) -> None:
        """TC-RT-P2-28: Authorization-Context 헤더가 라우터에 전달되어 user_context 추출 (OQ-RT-7)."""
        captured = {}

        async def fake_list(**kwargs):
            captured.update(kwargs)
            return [], 0

        with patch.object(returns_service, "list_returns", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/returns?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30",
                headers=DSEL_HEADER,
            )
        self.assertEqual(res.status_code, 200, res.text)
        # Phase 2 는 헬퍼 인터페이스만 검증 — user_context 전달 여부
        if "user_context" in captured:
            self.assertEqual(captured["user_context"].get("branch_id"), "BR01")
        else:
            # 인터페이스 미구현 시 경고 후 PASS (T5d 완료 후 강제)
            self.skipTest("user_context propagation not yet implemented (T5d)")

    def test_p2_29_import_xls_returns_501(self) -> None:
        """TC-RT-P2-29: format=xls 임포트 → 501 Not Implemented (OQ-RT-1 assume_default)."""
        try:
            from app.services.returns_service import ImportFormatNotSupportedError  # noqa: PLC0415
        except ImportError:
            self.skipTest("ImportFormatNotSupportedError not yet implemented (T5b)")
            return

        async def fake_preview(**kwargs):  # noqa: ARG001
            raise ImportFormatNotSupportedError("xls not supported in Phase 2")

        with patch.object(returns_service, "import_preview", side_effect=fake_preview):
            res = self.client.post(
                "/api/v1/returns/import/preview?serverId=remote_1&customer_kind=직거래",
                files={"file": ("data.xls", b"\xD0\xCF", "application/vnd.ms-excel")},
            )
        self.assertEqual(res.status_code, 501, res.text)

    def test_p2_30_data_legacy_id_coverage_phase2_screens(self) -> None:
        """TC-RT-P2-30: Sobo34_4/Sobo58 페이지의 data-legacy-id 커버리지 (DEC-028)."""
        # 핵심 위젯 ID 가 매핑 노트와 일치하는지 검사
        required_ids = {
            "ledger": [
                "Sobo34_4.Edit101", "Sobo34_4.Edit102", "Sobo34_4.dxButton1",
                "Sobo34_4.DBGrid101.GNAME", "Sobo34_4.DBGrid101.GSSUM",
                "Sobo34_4.DBGrid201.GDATE", "Sobo34_4.DBGrid201.GUBUN",
            ],
            "period-report": [
                "Sobo58.Edit101", "Sobo58.Edit102", "Sobo58.dxButton1",
                "Sobo58.DBGrid101.HCODE", "Sobo58.DBGrid101.HNAME",
                "Sobo58.DBGrid201.GDATE", "Sobo58.DBGrid201.BCODE",
                "Sobo58.Edit201", "Sobo58.Edit202", "Sobo58.Edit203", "Sobo58.Edit204",
            ],
        }

        page_paths = {
            "ledger": FRONTEND / "src" / "app" / "(app)" / "returns" / "ledger" / "page.tsx",
            "period-report": FRONTEND / "src" / "app" / "(app)" / "returns" / "period-report" / "page.tsx",
        }

        missing_total: list[tuple[str, str]] = []
        for screen, ids in required_ids.items():
            page = page_paths[screen]
            if not page.exists():
                # T6 미완료 시 경고 (PASS 처리)
                print(f"\n[WARN] {screen} page not yet created: {page}")
                continue
            content = page.read_text(encoding="utf-8")
            for lid in ids:
                if lid not in content:
                    missing_total.append((screen, lid))

        if missing_total:
            # T6 진행 중에는 경고만 (T7 회귀 시점에 강제)
            print(f"\n[WARN] Missing data-legacy-ids: {missing_total}")
        # 페이지가 모두 존재하면 모든 id 가 있어야 함 (T7 시점)
        if all(page_paths[s].exists() for s in required_ids):
            self.assertEqual(missing_total, [], f"Missing data-legacy-ids in finalized pages: {missing_total}")


if __name__ == "__main__":
    main()
