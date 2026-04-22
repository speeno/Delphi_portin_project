"""
C6 거래/잔액 조회 — Phase 2 보강 검증.

대상 화면 (phase2-32screens-t1-t2-index.md §6~8):
  - Sobo21_status_list   /transactions/status?view=list
  - Sobo21_status_summary /transactions/status?view=summary
  - Sobo21_status_memo   /transactions/status?view=memo

계약: migration/contracts/sales_inquiry.yaml §11 phase2_addendum.transactions_status_view
테스트팩: migration/test-cases/_phase2_addendum.json TC-INQ-P2-001~006

전략
----
실제 DB 없이 ``transactions_service.list_sales_statements`` 와
``summarize_sales_statements_by_customer`` 를 monkeypatch 하여 facade 라우터의
view 분기·파라미터 매핑·응답 형태만 검증한다 (test_c6_inquiry_phase1 와 동일
패턴). DB 의존 회귀(서브쿼리/요약 정렬)는 ``test_list_count_grouped_mysql3.py``
와 별도 통합 스모크에서 다룬다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

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
from app.services import transactions_service  # noqa: E402


def _override_auth() -> dict:
    return {"user_id": "hong01", "server_id": "remote_1"}


app.dependency_overrides[get_current_user] = _override_auth


COMMON_QUERY = (
    "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30&limit=10&offset=0"
)

KEY_A = {"gdate": "2026.04.18", "hcode": "A0001", "jubun": "120000000001", "gjisa": "1"}
KEY_B = {"gdate": "2026.04.20", "hcode": "B0002", "jubun": "120000000099", "gjisa": ""}


def _list_item(
    key: dict,
    *,
    customer_name: str,
    qty: int,
    amount: int,
    memo_preview: str = "",
    status: str = "active",
    row_count: int = 1,
) -> dict:
    return {
        "order_key": key,
        "customer_name": customer_name,
        "row_count": row_count,
        "qty": qty,
        "amount": amount,
        "status": status,
        "memo_preview": memo_preview,
    }


# ---------------------------------------------------------------
# AC-INQ-P2-1 / TC-INQ-P2-001 — view=list 기본 동작 + 1:1 매핑
# ---------------------------------------------------------------

class StatusViewListTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_view_list_equivalent(self) -> None:
        """view=list 호출이 sales-statement 와 동일 서비스 함수를 호출하고
        동일 응답 형태를 surface 하는지 검증."""

        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            items = [
                _list_item(KEY_A, customer_name="A상사", qty=12, amount=120_000),
            ]
            return items, len(items)

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res_facade = self.client.get(
                "/api/v1/transactions/status" + COMMON_QUERY + "&view=list"
            )
            res_canonical = self.client.get(
                "/api/v1/transactions/sales-statement" + COMMON_QUERY
            )

        self.assertEqual(res_facade.status_code, 200, res_facade.text)
        self.assertEqual(res_canonical.status_code, 200, res_canonical.text)
        body_facade = res_facade.json()
        body_canonical = res_canonical.json()
        self.assertEqual(body_facade["items"], body_canonical["items"])
        self.assertEqual(body_facade["total"], body_canonical["total"])
        # facade 의 list 분기는 memoPresence 미부착 (canonical 과 동일)
        facade_kwargs = captured[0]
        self.assertIsNone(facade_kwargs.get("memo_presence"))
        self.assertFalse(facade_kwargs.get("include_memo_preview"))


# ---------------------------------------------------------------
# AC-INQ-P2-4 / TC-INQ-P2-004 — view 미지정 → 기본 list (하위 호환)
# ---------------------------------------------------------------

class StatusViewDefaultTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_view_default_list(self) -> None:
        async def fake_list(**kwargs):  # noqa: ARG001
            return [_list_item(KEY_A, customer_name="A상사", qty=1, amount=10_000)], 1

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get("/api/v1/transactions/status" + COMMON_QUERY)
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        # list 응답 형태: items + page + total/limit/offset (BC 평면 필드)
        for k in ("items", "page", "total", "limit", "offset"):
            self.assertIn(k, body)
        # summary 응답에만 있는 truncated 가 없어야 한다
        self.assertNotIn("truncated", body)


# ---------------------------------------------------------------
# AC-INQ-P2-2 / TC-INQ-P2-002 — view=summary 응답 형태 + amount_desc 정렬
# ---------------------------------------------------------------

class StatusViewSummaryTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_view_summary_aggregation(self) -> None:
        async def fake_summary(**kwargs):  # noqa: ARG001
            items = [
                {
                    "customer_code": "B0002",
                    "customer_name": "B상사",
                    "slip_count": 5,
                    "total_qty": 50,
                    "total_amount": 500_000,
                },
                {
                    "customer_code": "A0001",
                    "customer_name": "A상사",
                    "slip_count": 3,
                    "total_qty": 30,
                    "total_amount": 300_000,
                },
            ]
            return items, len(items), False

        with patch.object(
            transactions_service,
            "summarize_sales_statements_by_customer",
            side_effect=fake_summary,
        ):
            res = self.client.get(
                "/api/v1/transactions/status" + COMMON_QUERY + "&view=summary"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(len(body["items"]), 2)
        # amount_desc 정렬 보존
        amounts = [it["total_amount"] for it in body["items"]]
        self.assertEqual(amounts, sorted(amounts, reverse=True))
        # summary 응답 전용 필드
        self.assertIn("truncated", body)
        self.assertFalse(body["truncated"])
        # facade 가 summary 분기로 진입했음을 검증 — items 키들이 customer_code 기반
        self.assertEqual(body["items"][0]["customer_code"], "B0002")

    def test_view_summary_truncated_flag_propagates(self) -> None:
        async def fake_summary(**kwargs):  # noqa: ARG001
            return [], 0, True

        with patch.object(
            transactions_service,
            "summarize_sales_statements_by_customer",
            side_effect=fake_summary,
        ):
            res = self.client.get(
                "/api/v1/transactions/status" + COMMON_QUERY + "&view=summary"
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["truncated"])


# ---------------------------------------------------------------
# AC-INQ-P2-3 / TC-INQ-P2-003 — view=memo 가 has_memo + preview 자동 부착
# ---------------------------------------------------------------

class StatusViewMemoTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_view_memo_filter(self) -> None:
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            items = [
                _list_item(
                    KEY_A,
                    customer_name="A상사",
                    qty=2,
                    amount=20_000,
                    memo_preview="첫 100자 메모 미리보기",
                ),
            ]
            return items, len(items)

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get(
                "/api/v1/transactions/status" + COMMON_QUERY + "&view=memo"
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        # facade 가 memo_presence='has_memo' + include_memo_preview=True 자동 부착
        kw = captured[0]
        self.assertEqual(kw.get("memo_presence"), "has_memo")
        self.assertTrue(kw.get("include_memo_preview"))
        # 모든 행이 비어있지 않은 memo_preview 를 가진다 (서비스가 보장하는 계약)
        for it in body["items"]:
            self.assertTrue(it["memo_preview"])

    def test_view_memo_like_filter(self) -> None:
        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            return [
                _list_item(KEY_A, customer_name="A", qty=1, amount=1, memo_preview="키워드 포함"),
            ], 1

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = self.client.get(
                "/api/v1/transactions/status"
                + COMMON_QUERY
                + "&view=memo&memoLike=%ED%82%A4%EC%9B%8C%EB%93%9C"  # "키워드"
            )
        self.assertEqual(res.status_code, 200, res.text)
        kw = captured[0]
        self.assertEqual(kw.get("memo_like"), "키워드")
        self.assertEqual(kw.get("memo_presence"), "has_memo")


# ---------------------------------------------------------------
# AC-INQ-P2-6 / TC-INQ-P2-006 — canonical /sales-statement 동등성
# ---------------------------------------------------------------

class CanonicalEquivalenceTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_canonical_memo_equivalent(self) -> None:
        """canonical /sales-statement?memoPresence=has_memo&includeMemoPreview=true
        가 facade ?view=memo 와 동일 서비스 호출 + 동일 응답 형태인지 검증."""

        captured: list[dict] = []

        async def fake_list(**kwargs):
            captured.append(kwargs)
            return [
                _list_item(KEY_B, customer_name="B상사", qty=3, amount=33_000, memo_preview="hi"),
            ], 1

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res_canonical = self.client.get(
                "/api/v1/transactions/sales-statement"
                + COMMON_QUERY
                + "&memoPresence=has_memo&includeMemoPreview=true"
            )
            res_facade = self.client.get(
                "/api/v1/transactions/status" + COMMON_QUERY + "&view=memo"
            )

        self.assertEqual(res_canonical.status_code, 200, res_canonical.text)
        self.assertEqual(res_facade.status_code, 200, res_facade.text)
        self.assertEqual(res_canonical.json()["items"], res_facade.json()["items"])
        # 두 호출 모두 같은 키워드 인자 조합으로 service 호출
        self.assertEqual(len(captured), 2)
        for kw in captured:
            self.assertEqual(kw.get("memo_presence"), "has_memo")
            self.assertTrue(kw.get("include_memo_preview"))


# ---------------------------------------------------------------
# Validation — view 값이 enum 외이면 422 INQ_VALIDATION
# ---------------------------------------------------------------

class StatusViewValidationTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_invalid_view_returns_422(self) -> None:
        res = self.client.get(
            "/api/v1/transactions/status" + COMMON_QUERY + "&view=bogus"
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "INQ_VALIDATION")


# ---------------------------------------------------------------
# 서비스 단위 — 메모 미리보기/요약 헬퍼 (DB 없이 순수 로직)
# ---------------------------------------------------------------

class MemoPreviewHelperTests(TestCase):
    """``_memo_preview_text`` 100자 캡 + 줄바꿈 정규화."""

    def test_picks_gbigo_first_then_sbigo(self) -> None:
        from app.services.transactions_service import _memo_preview_text
        self.assertEqual(_memo_preview_text("first", "second"), "first")
        self.assertEqual(_memo_preview_text("", "second"), "second")
        self.assertEqual(_memo_preview_text(None, None), "")

    def test_truncates_to_100_chars(self) -> None:
        from app.services.transactions_service import _memo_preview_text
        long_text = "가" * 200
        self.assertEqual(len(_memo_preview_text(long_text, "")), 100)

    def test_normalizes_newlines_to_space(self) -> None:
        from app.services.transactions_service import _memo_preview_text
        self.assertEqual(_memo_preview_text("a\nb\r\nc", ""), "a b c")


class LikifyMemoTests(TestCase):
    def test_empty_returns_none(self) -> None:
        from app.services.transactions_service import _likify_memo
        self.assertIsNone(_likify_memo(""))
        self.assertIsNone(_likify_memo(None))
        self.assertIsNone(_likify_memo("   "))

    def test_wraps_with_percent(self) -> None:
        from app.services.transactions_service import _likify_memo
        self.assertEqual(_likify_memo("hello"), "%hello%")

    def test_escapes_wildcards(self) -> None:
        from app.services.transactions_service import _likify_memo
        # 사용자 입장에서 literal % / _ 가 매칭되도록 escape
        self.assertEqual(_likify_memo("a%b_c"), "%a\\%b\\_c%")


if __name__ == "__main__":
    main()
