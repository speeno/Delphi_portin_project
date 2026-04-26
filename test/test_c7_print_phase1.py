"""
C7 인쇄 Phase 1 — 5종 양식 PDF + 라벨 PDF 검증 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/settlement_billing.yaml v1.2.0 (P1-A 청구서 / P1-B 세금계산서 PDF 흡수)
- migration/contracts/print_invoice.yaml v1.0.0 (P1-C 출고/P1-D 반품/P1-E 매출 거래명세서 PDF)
- migration/contracts/print_label.yaml v1.0.0 (P1-F 라벨 PDF)
- analysis/print_specs/c7_phase1.md (5종 양식 + 라벨 사양 단일 출처)
- analysis/handlers/c7_phase1.md (SQL-PR-1~6 인덱스)
- i18n/messages/c7.ko.json (PDF 다운로드 / 엔진 / .frf 정책 메시지)

검증 케이스 (~25건)
-------------------
- TC-PR-P1-01~05  PDF 시그니처 + Content-Type (5종 양식)
- TC-PR-P1-06     라벨 PDF 시그니처 (P1-F)
- TC-PR-P1-07~11  텍스트 추출 (pypdf — 가능 시) + 빈 데이터 200
- TC-PR-P1-12~13  마감 워터마크 (P1-A/P1-B)
- TC-PR-P1-14     WeasyPrint 미설치 → 503 + PR_ENGINE_UNAVAILABLE
- TC-PR-P1-15~25  정적 검사 (i18n / 매핑 노트 / contract / DEC-028 / 신규 SQL 0)

설계 정합 (사용자 룰)
---------------------
- C5 Phase 2 패턴(test_c5_settlement_phase2.py) 그대로 재사용 — monkeypatch + dependency_overrides.
- 신규 헬퍼 금지, test 폴더 한 파일.
- T5 미착수 시점에는 서비스 import 실패 가능 → unittest.skipUnless 로 안전 우회.
- 정적 검사(TC-PR-P1-15~25) 는 T5 무관하게 항상 실행 — DEC-028 / DEC-037 / DEC-038 / DEC-039 가시화.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))


# ──────────────────────────────────────────────
# T5 의존성 — 미착수 시점에는 안전 우회 (skipUnless)
# 런타임 PDF 검증은 print_service 와 label_service 둘 다 import 가능해야 활성.
# ──────────────────────────────────────────────
_RUNTIME_OK = False
try:
    from fastapi.testclient import TestClient  # noqa: E402
    from app.main import app  # noqa: E402
    from app.routers.auth import get_current_user  # noqa: E402

    def _override_auth() -> dict:
        return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}

    app.dependency_overrides[get_current_user] = _override_auth

    # T5 핵심 서비스가 없으면 런타임 PDF 검증 비활성 (정적 검사만 수행).
    from app.services import print_service as _print_service  # noqa: F401
    from app.services import label_service as _label_service  # noqa: F401

    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]


# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
GDATE_MONTH = "202604"
HCODE = "H0001"
BILLING_KEY = f"{GDATE_MONTH}|{HCODE}"
BILLING_KEY_URL = f"{GDATE_MONTH}%7C{HCODE}"
ORDER_KEY = "20260401|H0001|J00001"
ORDER_KEY_URL = "20260401%7CH0001%7CJ00001"
# 빈 Jubun / 빈 Jubun+Gjisa — 레거시 NULL·빈 값 키 PDF 라우트 수용 (PR_VALIDATION 회귀 가드).
ORDER_KEY_EMPTY_JUBUN_URL = "2026.04.24%7C5049%7C"
ORDER_KEY_EMPTY_STMT_URL = "2026.04.24%7C5049%7C%7C"
RETURN_KEY = "G|20260401|H0001|J00001"
RETURN_KEY_URL = "G%7C20260401%7CH0001%7CJ00001"
SHIPMENT_KEY = "S1_Ssub|K0001"
SHIPMENT_KEY_URL = "S1_Ssub%7CK0001"

# 최소 PDF 바이트 (테스트 모킹용 — `%PDF-` 매직 + 본문 + EOF)
SAMPLE_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj << /Type /Catalog >> endobj\n"
    b"trailer << /Root 1 0 R >>\n"
    b"%%EOF\n"
)


def _pdf_signature_ok(body: bytes) -> bool:
    """PDF 매직 바이트 + EOF 마커 검사."""
    return body.startswith(b"%PDF-") and b"%%EOF" in body[-32:]


# ──────────────────────────────────────────────
# 1. 런타임 PDF 응답 검증 (T5 착수 후 활성)
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 (print_service / routers/print.py) 미착수 — 정적 검사만 실행")
class C7PrintRuntimeTestCase(TestCase):
    """양식 5종 + 라벨 1종 PDF 응답 검증."""

    def setUp(self) -> None:
        assert app is not None and TestClient is not None
        self.client = TestClient(app)

    # ────── P1-A 청구서 (settlement_billing.yaml v1.2.0) ──────
    def test_TC_PR_P1_01_invoice_pdf_signature(self) -> None:
        from app.services import print_service, settlement_print_service
        with patch.object(
            settlement_print_service, "render_invoice_pdf_html",
            return_value="<html><body data-legacy-id='Sobo46.Header.Hname'>OK</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "application/pdf")
        self.assertTrue(_pdf_signature_ok(res.content))

    # ────── P1-B 세금계산서 ──────
    def test_TC_PR_P1_02_tax_invoice_pdf_signature(self) -> None:
        from app.services import print_service, tax_invoice_service
        with patch.object(
            tax_invoice_service, "render_tax_invoice_pdf_html",
            return_value="<html><body data-legacy-id='Sobo49.Print.Sum27'>0</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "application/pdf")
        self.assertTrue(_pdf_signature_ok(res.content))

    # ────── P1-C 출고 거래명세서 ──────
    def test_TC_PR_P1_03_outbound_statement_pdf_signature(self) -> None:
        from unittest.mock import AsyncMock
        from app.services import outbound_service, print_service
        with patch.object(
            outbound_service, "get_order_detail",
            new=AsyncMock(return_value={"order_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            outbound_service, "render_outbound_statement_html",
            return_value="<html><body data-legacy-id='Sobo27.DBGrid101.GCODE'>OK</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/outbound-statement/{ORDER_KEY_URL}.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    def test_TC_PR_P1_03b_outbound_statement_pdf_empty_jubun_key_ok(self) -> None:
        """합성키 세그먼트 3개 중 Jubun 빈 값 — 422 가 아니라 정상 PDF 경로."""
        from unittest.mock import AsyncMock
        from app.services import outbound_service, print_service
        with patch.object(
            outbound_service, "get_order_detail",
            new=AsyncMock(return_value={"order_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            outbound_service, "render_outbound_statement_html",
            return_value="<html><body data-legacy-id='Sobo27.DBGrid101.GCODE'>OK</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/outbound-statement/{ORDER_KEY_EMPTY_JUBUN_URL}.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    def test_TC_PR_P1_03c_outbound_statement_style_param_routes_renderer(self) -> None:
        """style=legacy|modern 은 렌더러에 전달되고, 생략 시 modern 기본값을 유지한다."""
        from unittest.mock import AsyncMock
        from app.services import outbound_service, print_service

        captured: list[dict] = []

        def _capture_html(detail, *, variant="base", style="modern"):
            captured.append({"variant": variant, "style": style, "detail": detail})
            return f"<html><body>{style}</body></html>"

        with patch.object(
            outbound_service, "get_order_detail",
            new=AsyncMock(return_value={"order_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            outbound_service, "render_outbound_statement_html",
            side_effect=_capture_html,
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res_default = self.client.get(
                f"/api/v1/print/outbound-statement/{ORDER_KEY_URL}.pdf",
                params={"serverId": "remote_1"},
            )
            res_legacy = self.client.get(
                f"/api/v1/print/outbound-statement/{ORDER_KEY_URL}.pdf",
                params={"serverId": "remote_1", "style": "legacy", "variant": "v1"},
            )

        self.assertEqual(res_default.status_code, 200)
        self.assertEqual(res_legacy.status_code, 200)
        self.assertEqual(captured[0]["style"], "modern")
        self.assertEqual(captured[0]["variant"], "base")
        self.assertEqual(captured[1]["style"], "legacy")
        self.assertEqual(captured[1]["variant"], "v1")
        self.assertIn("_v1_legacy.pdf", res_legacy.headers["content-disposition"])

    def test_TC_PR_P1_03d_outbound_statement_invalid_style_returns_422(self) -> None:
        """지원하지 않는 출력 style 은 PR_STYLE_UNSUPPORTED 로 차단한다."""
        res = self.client.get(
            f"/api/v1/print/outbound-statement/{ORDER_KEY_URL}.pdf",
            params={"serverId": "remote_1", "style": "classic"},
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "PR_STYLE_UNSUPPORTED")

    # ────── P1-D 반품 영수증 ──────
    def test_TC_PR_P1_04_return_receipt_pdf_signature(self) -> None:
        from unittest.mock import AsyncMock
        from app.services import print_service, returns_service
        with patch.object(
            returns_service, "get_return_detail",
            new=AsyncMock(return_value={"return_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            returns_service, "render_return_receipt_html",
            return_value="<html><body data-legacy-id='Sobo23.DBGrid101.GSQUT'>0</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/return-receipt/{RETURN_KEY_URL}.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    def test_TC_PR_P1_04b_return_receipt_style_param_routes_renderer(self) -> None:
        """Sobo23도 style=legacy|modern 을 렌더러에 전달하고 파일명 suffix 를 유지한다."""
        from unittest.mock import AsyncMock
        from app.services import print_service, returns_service

        captured: list[dict] = []

        def _capture_html(detail, *, variant="base", style="modern"):
            captured.append({"variant": variant, "style": style, "detail": detail})
            return f"<html><body>{style}</body></html>"

        with patch.object(
            returns_service, "get_return_detail",
            new=AsyncMock(return_value={"return_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            returns_service, "render_return_receipt_html",
            side_effect=_capture_html,
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res_default = self.client.get(
                f"/api/v1/print/return-receipt/{RETURN_KEY_URL}.pdf",
                params={"serverId": "remote_1"},
            )
            res_legacy = self.client.get(
                f"/api/v1/print/return-receipt/{RETURN_KEY_URL}.pdf",
                params={"serverId": "remote_1", "style": "legacy", "variant": "v1"},
            )

        self.assertEqual(res_default.status_code, 200)
        self.assertEqual(res_legacy.status_code, 200)
        self.assertEqual(captured[0]["style"], "modern")
        self.assertEqual(captured[0]["variant"], "base")
        self.assertEqual(captured[1]["style"], "legacy")
        self.assertEqual(captured[1]["variant"], "v1")
        self.assertIn("_v1_legacy.pdf", res_legacy.headers["content-disposition"])

    def test_TC_PR_P1_04c_return_receipt_invalid_style_returns_422(self) -> None:
        """지원하지 않는 반품 출력 style 은 PR_STYLE_UNSUPPORTED 로 차단한다."""
        res = self.client.get(
            f"/api/v1/print/return-receipt/{RETURN_KEY_URL}.pdf",
            params={"serverId": "remote_1", "style": "classic"},
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["detail"]["code"], "PR_STYLE_UNSUPPORTED")

    # ────── P1-E 거래명세서 ──────
    def test_TC_PR_P1_05_sales_statement_pdf_signature(self) -> None:
        from unittest.mock import AsyncMock
        from app.services import print_service, transactions_service
        with patch.object(
            transactions_service, "get_sales_statement_detail",
            new=AsyncMock(return_value={"order_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            transactions_service, "render_sales_statement_html",
            return_value="<html><body data-legacy-id='Sobo21.DBGrid101.GBIGO'>OK</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/sales-statement/{ORDER_KEY_URL}.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    def test_TC_PR_P1_05b_sales_statement_pdf_empty_jubun_gjisa_key_ok(self) -> None:
        """거래명세 4튜플 중 Jubun·Gjisa 빈 값 — 422 회귀 방지."""
        from unittest.mock import AsyncMock
        from app.services import print_service, transactions_service
        with patch.object(
            transactions_service, "get_sales_statement_detail",
            new=AsyncMock(return_value={"order_key": {}, "customer": {}, "lines": [{"gsqut": 1, "gssum": 1000}]}),
        ), patch.object(
            transactions_service, "render_sales_statement_html",
            return_value="<html><body data-legacy-id='Sobo21.DBGrid101.GBIGO'>OK</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/sales-statement/{ORDER_KEY_EMPTY_STMT_URL}.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    # ────── P1-F 라벨 ──────
    def test_TC_PR_P1_06_label_pdf_signature(self) -> None:
        from unittest.mock import AsyncMock
        from app.services import label_service, print_service
        with patch.object(
            label_service, "fetch_label_row",
            new=AsyncMock(return_value={"Gname": "홍길동", "Gposa": "사장", "Gadds": "주소"}),
        ), patch.object(
            label_service, "render_label_html",
            return_value="<html><body data-legacy-id='Seep13.Label.Gname'>홍길동</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/label/{SHIPMENT_KEY_URL}.pdf",
                params={"serverId": "remote_1", "form": 1},
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "application/pdf")
        self.assertTrue(_pdf_signature_ok(res.content))

    # ────── 빈 데이터 / 마감 워터마크 / fallback ──────
    def test_TC_PR_P1_07_invoice_pdf_empty_data_returns_200_placeholder(self) -> None:
        """detail 빈 응답이라도 200 + placeholder PDF (DEC-037 운영자 안내)."""
        from app.services import print_service, settlement_print_service
        with patch.object(
            settlement_print_service, "render_invoice_pdf_html",
            return_value="<html><body>인쇄할 자료가 없습니다.</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))

    def test_TC_PR_P1_08_invoice_pdf_closed_watermark(self) -> None:
        """마감 (T2_Ssub.Yesno='1') 자료 → HTML 에 '마감' 워터마크 포함 → PDF 정상 반환."""
        from app.services import print_service, settlement_print_service
        watermark_html = (
            "<html><body>"
            "<div class='watermark'>마감</div>"
            "<span data-legacy-id='Sobo46.Header.Hname'>홍길동서점</span>"
            "</body></html>"
        )
        captured: dict = {}

        def _capture_render(html: str, **_):
            captured["html"] = html
            return SAMPLE_PDF

        with patch.object(
            settlement_print_service, "render_invoice_pdf_html",
            return_value=watermark_html,
        ), patch.object(print_service, "render_pdf", side_effect=_capture_render):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn("마감", captured.get("html", ""))

    def test_TC_PR_P1_09_tax_invoice_pdf_closed_watermark(self) -> None:
        from app.services import print_service, tax_invoice_service
        captured: dict = {}

        def _capture_render(html: str, **_):
            captured["html"] = html
            return SAMPLE_PDF

        with patch.object(
            tax_invoice_service, "render_tax_invoice_pdf_html",
            return_value="<html><body><div class='watermark'>마감</div>OK</body></html>",
        ), patch.object(print_service, "render_pdf", side_effect=_capture_render):
            res = self.client.get(
                f"/api/v1/settlement/tax-invoice/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn("마감", captured.get("html", ""))

    def test_TC_PR_P1_10_engine_unavailable_returns_503(self) -> None:
        """WeasyPrint 미설치 → 503 + 코드 PR_ENGINE_UNAVAILABLE (DEC-037 fallback)."""
        from fastapi import HTTPException
        from app.services import print_service, settlement_print_service
        with patch.object(
            settlement_print_service, "render_invoice_pdf_html",
            return_value="<html></html>",
        ), patch.object(
            print_service, "render_pdf",
            side_effect=HTTPException(503, {
                "code": "PR_ENGINE_UNAVAILABLE",
                "detail": "PDF 엔진이 설치되지 않았습니다.",
            }),
        ):
            res = self.client.get(
                f"/api/v1/settlement/billing/{BILLING_KEY_URL}/print.pdf",
                params={"serverId": "remote_1"},
            )
        self.assertEqual(res.status_code, 503)
        body = res.json()
        # FastAPI HTTPException 의 detail 이 dict 인 경우 그대로 노출
        detail = body.get("detail", body)
        if isinstance(detail, dict):
            self.assertEqual(detail.get("code"), "PR_ENGINE_UNAVAILABLE")
        else:
            self.assertIn("PR_ENGINE_UNAVAILABLE", str(detail))

    def test_TC_PR_P1_11_label_pdf_form_param_phase1_only_form1(self) -> None:
        """DEC-038 — Phase 1 라벨은 form=1 우편엽서만 정상. form 인자는 1~1 범위로 검증."""
        from unittest.mock import AsyncMock
        from app.services import label_service, print_service
        with patch.object(
            label_service, "fetch_label_row",
            new=AsyncMock(return_value={"Gname": "홍길동", "Gposa": "사장", "Gadds": "주소"}),
        ), patch.object(
            label_service, "render_label_html",
            return_value="<html><body data-legacy-id='Seep13.Label.Gname'>홍길동</body></html>",
        ), patch.object(print_service, "render_pdf", return_value=SAMPLE_PDF):
            res = self.client.get(
                f"/api/v1/print/label/{SHIPMENT_KEY_URL}.pdf",
                params={"serverId": "remote_1", "form": 1, "include_oversea": "true"},
            )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(_pdf_signature_ok(res.content))


# ──────────────────────────────────────────────
# 2. 정적 검사 (T5 무관 — 항상 실행)
# ──────────────────────────────────────────────
class C7PrintStaticTestCase(TestCase):
    """contracts / mappings / handlers / i18n 정합 정적 검사."""

    def test_TC_PR_P1_26_print_order_key_parsers_allow_empty_jubun_gjisa(self) -> None:
        """print.py 합성키 파서 — gdate/hcode 만 필수, 빈 Jubun·Gjisa 허용."""
        from fastapi import HTTPException
        from app.routers.print import _parse_order_key_3, _parse_order_key_4

        self.assertEqual(_parse_order_key_3("2026.04.24|5049|"), ("2026.04.24", "5049", ""))
        self.assertEqual(_parse_order_key_4("2026.04.24|5049|"), ("2026.04.24", "5049", "", ""))
        self.assertEqual(_parse_order_key_4("2026.04.24|5049||"), ("2026.04.24", "5049", "", ""))
        self.assertEqual(_parse_order_key_4("2026.04.24|5049|J|G"), ("2026.04.24", "5049", "J", "G"))
        with self.assertRaises(HTTPException) as ctx:
            _parse_order_key_3("a|b")
        self.assertEqual(ctx.exception.status_code, 422)
        with self.assertRaises(HTTPException) as ctx4:
            _parse_order_key_4("a|b|c|d|e")
        self.assertEqual(ctx4.exception.status_code, 422)

    # ────── i18n ──────
    def test_TC_PR_P1_15_i18n_c7_messages_present(self) -> None:
        i18n_path = ROOT / "i18n" / "messages" / "c7.ko.json"
        self.assertTrue(i18n_path.exists(), "missing i18n/messages/c7.ko.json")
        data = json.loads(i18n_path.read_text(encoding="utf-8"))
        msgs = data["messages"]
        for key in (
            "c7.print.downloading", "c7.print.ready", "c7.print.failed",
            "c7.print.no_data", "c7.print.preview_only_native",
            "c7.label.single_form_only", "c7.label.postal_format",
            "c7.engine.unavailable", "c7.engine.weasyprint_required",
            "c7.frf.reference_only",
        ):
            self.assertIn(key, msgs, f"missing i18n key {key}")

    def test_TC_PR_P1_16_i18n_dec_references(self) -> None:
        data = json.loads((ROOT / "i18n" / "messages" / "c7.ko.json").read_text(encoding="utf-8"))
        for dec in ("DEC-037", "DEC-038", "DEC-039"):
            self.assertIn(dec, data["decisions"], f"missing decision {dec} in c7.ko.json")

    # ────── 매핑 노트 ──────
    def test_TC_PR_P1_17_layout_mappings_present(self) -> None:
        for fname in (
            "Sobo46_billing.md", "Sobo49_tax.md",
            "Sobo27.md", "Sobo23.md", "Sobo21.md",
            "Seep13_label.md",
        ):
            path = ROOT / "analysis" / "layout_mappings" / fname
            self.assertTrue(path.exists(), f"missing layout mapping: {fname}")
            content = path.read_text(encoding="utf-8")
            self.assertIn("data-legacy-id", content, f"{fname}: data-legacy-id 누락")
            self.assertIn("DEC-028", content, f"{fname}: DEC-028 미참조")

    def test_TC_PR_P1_18_mapping_notes_have_pdf_section(self) -> None:
        """5종 양식 매핑 노트에 PDF 절 (C7 Phase 1) 보강 확인."""
        for fname in ("Sobo46_billing.md", "Sobo49_tax.md", "Sobo27.md", "Sobo23.md", "Sobo21.md"):
            content = (ROOT / "analysis" / "layout_mappings" / fname).read_text(encoding="utf-8")
            self.assertIn("PDF 절", content, f"{fname}: PDF 절 미보강")
            self.assertIn("DEC-037", content, f"{fname}: DEC-037 미참조")

    # ────── print_specs / handlers ──────
    def test_TC_PR_P1_19_print_specs_phase1_present(self) -> None:
        path = ROOT / "analysis" / "print_specs" / "c7_phase1.md"
        self.assertTrue(path.exists(), "missing analysis/print_specs/c7_phase1.md")
        content = path.read_text(encoding="utf-8")
        for marker in ("P1-A", "P1-B", "P1-C", "P1-D", "P1-E", "P1-F", "WeasyPrint", "@page"):
            self.assertIn(marker, content, f"print_specs/c7_phase1.md: {marker} 미포함")

    def test_TC_PR_P1_20_handlers_c7_phase1_present(self) -> None:
        path = ROOT / "analysis" / "handlers" / "c7_phase1.md"
        self.assertTrue(path.exists(), "missing analysis/handlers/c7_phase1.md")
        content = path.read_text(encoding="utf-8")
        for sql_id in ("SQL-PR-1", "SQL-PR-2", "SQL-PR-3", "SQL-PR-4", "SQL-PR-5", "SQL-PR-6"):
            self.assertIn(sql_id, content, f"c7_phase1.md: {sql_id} 미포함")

    # ────── contracts ──────
    def test_TC_PR_P1_21_settlement_contract_v120_includes_pdf_endpoints(self) -> None:
        contract = (ROOT / "migration" / "contracts" / "settlement_billing.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("version: 1.3.0", contract)
        for path in (
            "/billing/{billing_key}/print.pdf",
            "/tax-invoice/{billing_key}/print.pdf",
        ):
            self.assertIn(path, contract, f"settlement_billing.yaml: {path} 미포함")
        for dec in ("DEC-037", "D-ST-12"):
            self.assertIn(dec, contract, f"settlement_billing.yaml: {dec} 미참조")

    def test_TC_PR_P1_22_print_invoice_contract_present(self) -> None:
        path = ROOT / "migration" / "contracts" / "print_invoice.yaml"
        self.assertTrue(path.exists(), "missing print_invoice.yaml")
        content = path.read_text(encoding="utf-8")
        for endpoint in (
            "/print/outbound-statement/{order_key}.pdf",
            "/print/return-receipt/{return_key}.pdf",
            "/print/sales-statement/{order_key}.pdf",
        ):
            self.assertIn(endpoint, content, f"print_invoice.yaml: {endpoint} 미포함")
        # Phase 1 = v1.0.0, Phase 2-α 이후 minor 갱신 허용 (v1.x.y).
        self.assertRegex(content, r"version:\s*1\.\d+\.\d+", "print_invoice.yaml: version 미준수 (1.x.y 기대)")
        self.assertIn("DEC-037", content)

    def test_TC_PR_P1_23_print_label_contract_present(self) -> None:
        path = ROOT / "migration" / "contracts" / "print_label.yaml"
        self.assertTrue(path.exists(), "missing print_label.yaml")
        content = path.read_text(encoding="utf-8")
        self.assertIn("/print/label/{shipment_key}.pdf", content)
        self.assertIn("DEC-038", content)
        self.assertIn("DEC-039", content)

    # ────── DEC-028 / 신규 SQL 0 ──────
    def test_TC_PR_P1_24_no_new_sql_in_print_services(self) -> None:
        """DEC-037 §7 — print_service / label_service / render_*_html 빌더 모두 신규 SELECT/INSERT/UPDATE 0건.

        (T5 미착수 시 services 디렉토리에 파일 부재 → skip 대신 통과 — 회귀는 T5 착수 후 활성)
        """
        services_dir = BACKEND / "app" / "services"
        if not services_dir.exists():
            self.skipTest("backend services 디렉토리 부재")
        # DEC-037 §7: 핵심 PDF 엔진(print_service)은 SQL 0건 — 출력 변환만.
        # label_service 는 SQL-PR-6 (신규 1건) 보유 허용 — handlers/c7_phase1.md §7.
        candidates = ("print_service.py",)
        sql_pattern = re.compile(
            r"\b(SELECT|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM)\b",
            re.IGNORECASE,
        )
        for fname in candidates:
            path = services_dir / fname
            if not path.exists():
                continue  # T5 착수 전 — skip
            text = path.read_text(encoding="utf-8")
            # SQL 키워드는 doc/comment 만 허용 (코드는 불허) — 단순화 위해 코드 라인에 SQL 키워드가 있으면 fail
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                if sql_pattern.search(stripped):
                    self.fail(
                        f"{fname}: 신규 SQL 발견 — {stripped[:80]} (DEC-037 §7 위반: 빌더는 출력 변환만)"
                    )

    def test_TC_PR_P1_25_label_service_uses_seep13_legacy_ids(self) -> None:
        """DEC-028 — label 빌더는 Seep13.Label.* data-legacy-id 7개 모두 흡수해야 한다."""
        path = BACKEND / "app" / "services" / "label_service.py"
        if not path.exists():
            self.skipTest("T5b label_service.py 미작성")
        text = path.read_text(encoding="utf-8")
        for legacy_id in (
            "Seep13.Label.Gname",
            "Seep13.Label.Gjice",
            "Seep13.Label.Gposa",
            "Seep13.Label.Gadds",
            "Seep13.Label.Gpost",
        ):
            self.assertIn(legacy_id, text, f"label_service: {legacy_id} 미포함")

    def test_TC_PR_P1_27_pdf_download_buttons_use_auth_helper(self) -> None:
        """Bearer 인증 환경에서 PDF 저장이 직접 <a download>가 아닌 공통 helper를 사용한다."""
        helper = FRONTEND / "src" / "lib" / "print-api.ts"
        helper_text = helper.read_text(encoding="utf-8")
        self.assertIn("downloadPdfWithAuth", helper_text)
        self.assertIn("blob.size === 0", helper_text)
        self.assertIn("0x25", helper_text)  # %PDF magic
        self.assertIn("setTimeout(() => URL.revokeObjectURL", helper_text)

        app_dir = FRONTEND / "src" / "app" / "(app)"
        checked = 0
        for page in app_dir.rglob("*.tsx"):
            text = page.read_text(encoding="utf-8")
            if "PdfUrl" not in text and "downloadPdfWithAuth" not in text:
                continue
            checked += 1
            self.assertIn("downloadPdfWithAuth", text, f"{page}: auth helper 누락")
            self.assertNotRegex(text, r"href=\{.*PdfUrl", f"{page}: 직접 PDF href 금지")
            self.assertNotRegex(text, r"download=\{`(?:outbound|sales|return|invoice|tax_invoice|label)_", f"{page}: 직접 download 금지")
        self.assertGreaterEqual(checked, 6)

    def test_TC_PR_P1_27b_outbound_print_page_exposes_legacy_and_modern_buttons(self) -> None:
        """Sobo27 출력 페이지는 기존 서식/새 서식 PDF를 명시적으로 분리한다."""
        helper = FRONTEND / "src" / "lib" / "print-api.ts"
        page = (
            FRONTEND
            / "src"
            / "app"
            / "(app)"
            / "outbound"
            / "orders"
            / "[orderKey]"
            / "print"
            / "page.tsx"
        )
        helper_text = helper.read_text(encoding="utf-8")
        page_text = page.read_text(encoding="utf-8")

        self.assertIn("OutboundPrintStyle", helper_text)
        self.assertIn("style?: OutboundPrintStyle", helper_text)
        self.assertIn('params.set("style", options.style)', helper_text)
        self.assertIn("기존 서식 PDF", page_text)
        self.assertIn("새 서식 PDF", page_text)
        self.assertIn('onDownloadPdf("legacy")', page_text)
        self.assertIn('onDownloadPdf("modern")', page_text)
        self.assertIn("Sobo27.Button.PrintPdf.Legacy", page_text)
        self.assertIn("Sobo27.Button.PrintPdf.Modern", page_text)

    def test_TC_PR_P1_27c_return_print_page_exposes_legacy_and_modern_buttons(self) -> None:
        """Sobo23 출력 페이지도 기존 서식/새 서식 PDF를 명시적으로 분리한다."""
        helper = FRONTEND / "src" / "lib" / "print-api.ts"
        page = (
            FRONTEND
            / "src"
            / "app"
            / "(app)"
            / "returns"
            / "receipts"
            / "[returnKey]"
            / "print"
            / "page.tsx"
        )
        helper_text = helper.read_text(encoding="utf-8")
        page_text = page.read_text(encoding="utf-8")

        self.assertIn("ReturnReceiptPdfOptions", helper_text)
        self.assertIn("style?: PrintStyle", helper_text)
        self.assertIn('params.set("style", options.style)', helper_text)
        self.assertIn("기존 서식 PDF", page_text)
        self.assertIn("새 서식 PDF", page_text)
        self.assertIn('onDownloadPdf("legacy")', page_text)
        self.assertIn('onDownloadPdf("modern")', page_text)
        self.assertIn("Sobo23.Button.PrintPdf.Legacy", page_text)
        self.assertIn("Sobo23.Button.PrintPdf.Modern", page_text)

    def test_TC_PR_P1_28_pdf_filename_sanitizer_handles_empty_and_unsafe(self) -> None:
        """서버 파일명은 빈 Jubun·경로문자·구분자를 안전하게 정규화한다."""
        from app.routers.print import _safe_pdf_filename_part

        self.assertEqual(_safe_pdf_filename_part(""), "none")
        self.assertEqual(_safe_pdf_filename_part("A/B|C:D"), "A_B_C_D")
        self.assertEqual(_safe_pdf_filename_part(" 2026.04.24 "), "2026.04.24")

    def test_TC_PR_P1_29_pdf_legacy_equivalence_audit_present(self) -> None:
        """레거시 .frf 부족 자료와 기능 동등성 기준을 감사 문서로 고정한다."""
        path = ROOT / "analysis" / "audit" / "pdf-legacy-equivalence.md"
        self.assertTrue(path.exists(), "missing analysis/audit/pdf-legacy-equivalence.md")
        content = path.read_text(encoding="utf-8")
        for marker in (
            "Report_4_51.frf",
            "Report_2_11.frf",
            "기능 동등성 체크리스트",
            "Sobo67",
        ):
            self.assertIn(marker, content)

    def test_TC_PR_P1_30_statement_html_contains_equivalence_header_meta(self) -> None:
        """Sobo27/Sobo21 PDF HTML 이 문서화된 헤더 보조정보를 포함한다."""
        from app.services import outbound_service, transactions_service

        with patch.dict(os.environ, {"PRINT_TEMPLATE_MODE": "manual"}):
            outbound_html = outbound_service.render_outbound_statement_html(
                {
                    "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11"},
                    "customer": {"gname": "서점"},
                    "lines": [{"gcode": "G", "product_name": "책", "pubun": "A", "gsqut": 1, "gssum": 1000}],
                },
                variant="v1",
            )
            sales_html = transactions_service.render_sales_statement_html(
                {
                    "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11", "gjisa": "G1"},
                    "customer": {"gname": "서점"},
                    "lines": [{"gcode": "G", "product_name": "책", "pubun": "A", "gsqut": 1, "gssum": 1000, "gbigo": ""}],
                }
            )
        self.assertIn("Sobo27.Header.Variant", outbound_html)
        self.assertIn("양식: v1", outbound_html)
        self.assertIn("Sobo21.Header.Gjisa", sales_html)
        for marker in (
            "공급받는자보관용",
            "공급자보관용",
            "사업자등록",
            "합계금액",
            "총 부 수",
            "Sobo21.Header.Gjisa",
            "G1",
        ):
            self.assertIn(marker, sales_html)

    def test_TC_PR_P1_31_frf_template_candidate_inventory_present(self) -> None:
        """C7 FRF 후보 분류 산출물이 form_id/variant/품질 신호를 고정한다."""
        json_path = ROOT / "analysis" / "audit" / "frf-template-candidates.json"
        md_path = ROOT / "analysis" / "audit" / "frf-template-candidates.md"
        self.assertTrue(json_path.exists(), "missing frf-template-candidates.json")
        self.assertTrue(md_path.exists(), "missing frf-template-candidates.md")
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        entries = payload.get("entries") or []
        self.assertGreaterEqual(payload.get("entry_count", 0), 1)
        self.assertTrue(
            any(
                e.get("form_id") == "sales_statement_base"
                and (e.get("quality") or {}).get("required_pass") is True
                for e in entries
            ),
            "Sobo21 Report_2_11 계열은 라벨 기준 후보로 분류되어야 함",
        )
        self.assertTrue(
            any(e.get("form_id") == "outbound_statement_base" for e in entries),
            "Sobo27 Report_4_51 계열은 후보 목록에 남겨 후속 분류해야 함",
        )
        self.assertIn("sales_statement_base", md_path.read_text(encoding="utf-8"))

    def test_TC_PR_P1_32_sales_statement_context_adapter_maps_frf_fields(self) -> None:
        """Sobo21 detail 응답은 FRF placeholder 컨텍스트로 SQL 없이 변환된다."""
        from app.services.print_context_adapters import sales_statement_context

        ctx = sales_statement_context(
            {
                "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11", "gjisa": "G1"},
                "customer": {"hcode": "5053", "gname": "서점"},
                "lines": [
                    {"gcode": "G1", "bcode": "B1", "product_name": "책1", "pubun": "초판", "gsqut": 2, "gssum": 3000},
                    {"gcode": "G2", "bcode": "B2", "product_name": "책2", "pubun": "재판", "gsqut": 3, "gssum": 4000},
                ],
            }
        )
        self.assertEqual(ctx["Gdate"], "2026.04.24")
        self.assertEqual(ctx["Pubun1"], "초판")
        self.assertEqual(ctx["Pubun2"], "재판")
        self.assertEqual(ctx["Gsqut"], 5)
        self.assertEqual(ctx["Gssum"], 7000)

    def test_TC_PR_P1_33b_sales_statement_manual_layout_is_table_fixed(self) -> None:
        """Sobo21 manual builder 는 WeasyPrint 폭 추정 회귀(2026-04-27)를 막기 위해
        헤더/메타를 table-layout:fixed 로 짜고 grid/flex 의존을 두지 않는다.

        회귀 배경: WeasyPrint 68.x 의 ``display: grid`` 트랙 폭이 콘텐츠 기반으로
        무너져 우측 메타 영역 ``나들목꿈틀물류센터`` 가 페이지 우측을 넘어가
        ``센터`` 까지 잘리는 사례 보고. ``table-layout: fixed`` + colgroup 으로
        결정적 폭 제어를 강제한다.
        """
        from app.services import transactions_service

        detail = {
            "order_key": {"gdate": "2026.04.27", "hcode": "5053", "jubun": "1", "gjisa": ""},
            "customer": {"hcode": "5053", "gname": "나들목꿈틀물류센터"},
            "lines": [
                {"gcode": "001", "product_name": "tv에서 볼 수 없는 북한", "pubun": "위탁", "gsqut": 1, "gssum": 13500, "gbigo": ""},
            ],
        }
        with patch.dict(os.environ, {"PRINT_TEMPLATE_MODE": "manual"}):
            html = transactions_service.render_sales_statement_html(detail)

        self.assertNotIn("display: grid", html, "manual builder 는 grid 사용 금지 (WeasyPrint 트랙 폭 회귀 가드)")
        self.assertNotIn("display:grid", html)
        self.assertNotIn("display: flex", html, "manual builder 헤더는 flex 대신 table 로 폭 제어")
        self.assertNotIn("display:flex", html)

        self.assertIn("table-layout: fixed", html, "table-layout:fixed 로 결정적 폭 강제")
        self.assertIn("class='header-table'", html)
        self.assertIn("class='meta-table'", html)
        self.assertIn("class='lines-table'", html)
        self.assertIn("colgroup", html)
        self.assertIn("class='header-right-col'", html, "우측 메타 col 폭 가드")
        self.assertIn("class='meta-label-col'", html, "메타 라벨 col 폭 가드")

        for legacy_id in (
            "Sobo21.Header.BusinessNo",
            "Sobo21.Header.Hname",
            "Sobo21.Header.Address",
            "Sobo21.Header.Gdate",
            "Sobo21.Header.Slip",
            "Sobo21.Header.Customer",
            "Sobo21.Header.Gjisa",
        ):
            self.assertIn(legacy_id, html, f"위젯 ID {legacy_id} 누락")

        self.assertIn("나들목꿈틀물류센터", html)
        self.assertIn("공급받는자보관용", html)
        self.assertIn("공급자보관용", html)

    def test_TC_PR_P1_33_sales_statement_low_quality_ir_falls_back_to_manual(self) -> None:
        """Sobo21 저품질 IR 후보는 auto 모드에서도 실출력에 쓰지 않고 manual 로 폴백한다."""
        from app.services import print_template_registry, transactions_service

        detail = {
            "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11", "gjisa": "G1"},
            "customer": {"hcode": "5053", "gname": "서점"},
            "lines": [
                {"gcode": "G1", "bcode": "B1", "product_name": "책1", "pubun": "초판", "gsqut": 2, "gssum": 3000, "gbigo": ""},
                {"gcode": "G2", "bcode": "B2", "product_name": "책2", "pubun": "재판", "gsqut": 3, "gssum": 4000, "gbigo": ""},
            ],
        }
        entry = print_template_registry.get_whitelist_entry("sales_statement_base")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["ir"], "Report_2_11.ir.json")
        self.assertFalse(entry.get("auto_enabled"))
        self.assertIn("base", entry.get("variants", {}))

        with patch.dict(os.environ, {"PRINT_TEMPLATE_MODE": "auto"}):
            auto_html = transactions_service.render_sales_statement_html(detail)
        self.assertIn("Sobo21.Header.Gjisa", auto_html)
        self.assertNotIn("frf-obj", auto_html)
        self.assertIn("초판", auto_html)
        self.assertNotIn("{{ ctx.", auto_html)

        with patch.dict(os.environ, {"PRINT_TEMPLATE_MODE": "manual"}):
            manual_html = transactions_service.render_sales_statement_html(detail)
        self.assertIn("Sobo21.Header.Gjisa", manual_html)
        self.assertNotIn("frf-obj", manual_html)

        try:
            print_template_registry._WHITELIST["__c7_missing"] = {  # type: ignore[attr-defined]
                "ir": "Report_2_11_DOES_NOT_EXIST.ir.json",
                "schema_version": "0.1.0",
                "approved_pr": "test",
                "quality": {},
            }
            with patch.dict(os.environ, {"PRINT_TEMPLATE_MODE": "auto"}):
                self.assertIsNone(
                    print_template_registry.try_render_with_ir(
                        "__c7_missing", {}, document_title="missing"
                    )
                )
        finally:
            print_template_registry._WHITELIST.pop("__c7_missing", None)  # type: ignore[attr-defined]

    def test_TC_PR_P1_34_outbound_dual_style_render_paths(self) -> None:
        """Sobo27은 modern 기본 경로와 legacy FRF/IR 직접 요청 경로를 모두 제공한다."""
        from app.services import outbound_service, print_template_registry
        from app.services.print_context_adapters import outbound_statement_context

        detail = {
            "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11"},
            "customer": {"hcode": "5053", "gname": "서점"},
            "lines": [
                {"gcode": "G1", "bcode": "B1", "product_name": "책1", "pubun": "현매", "gsqut": 2, "gssum": 3000},
                {"gcode": "G2", "bcode": "B2", "product_name": "책2", "pubun": "외상", "gsqut": 3, "gssum": 4000},
            ],
        }
        modern_html = outbound_service.render_outbound_statement_html(detail, style="modern")
        self.assertIn("Sobo27.DBGrid101.GCODE", modern_html)
        self.assertNotIn("frf-obj", modern_html)

        legacy_html = outbound_service.render_outbound_statement_html(detail, style="legacy")
        self.assertIn("frf-obj", legacy_html)
        self.assertIn("출고내역", legacy_html)
        self.assertNotIn("{{ ctx.", legacy_html)

        entry = print_template_registry.get_whitelist_entry("outbound_statement_base")
        self.assertIsNotNone(entry)
        self.assertIn("ir_path", entry)
        self.assertIn("v1", entry.get("variants", {}))

        ctx = outbound_statement_context(detail)
        self.assertEqual(ctx["Gdate"], "2026.04.24")
        self.assertEqual(ctx["Gsqut"], 5)
        self.assertEqual(ctx["Gssum"], 7000)
        self.assertEqual(ctx["Line1_Bname"], "책1")
        self.assertEqual(ctx["Sum_Gssum"], 7000)

    def test_TC_PR_P1_35_outbound_legacy_style_falls_back_to_modern(self) -> None:
        """legacy 템플릿 렌더 실패는 500이 아니라 modern HTML 폴백으로 처리한다."""
        from app.services import outbound_service

        detail = {
            "order_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11"},
            "customer": {"hcode": "5053", "gname": "서점"},
            "lines": [{"gcode": "G", "product_name": "책", "pubun": "A", "gsqut": 1, "gssum": 1000}],
        }
        with patch("app.services.print_template_registry.try_render_with_ir", return_value=None):
            html = outbound_service.render_outbound_statement_html(detail, style="legacy")
        self.assertIn("Sobo27.DBGrid101.GCODE", html)
        self.assertNotIn("frf-obj", html)

    def test_TC_PR_P1_36_return_dual_style_render_paths(self) -> None:
        """Sobo23은 modern 수동 빌더와 legacy FRF/IR 직접 요청 경로를 모두 제공한다."""
        from app.services import print_template_registry, returns_service
        from app.services.print_context_adapters import return_receipt_context

        detail = {
            "return_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11"},
            "customer": {"hcode": "5053", "hname": "반품거래처"},
            "memo": {"gbigo": "메모"},
            "lines": [
                {"bcode": "B1", "bname": "책1", "pubun": "반품", "gsqut": 2, "gdang": 1000, "grat1": 10, "gssum": 1800, "yesno": "0"},
                {"bcode": "B2", "bname": "책2", "pubun": "반품", "gsqut": 3, "gdang": 2000, "grat1": 0, "gssum": 6000, "yesno": "0"},
            ],
        }
        modern_html = returns_service.render_return_receipt_html(detail, style="modern")
        self.assertIn("Sobo23.DBGrid101.GSQUT", modern_html)
        self.assertNotIn("frf-obj", modern_html)

        legacy_html = returns_service.render_return_receipt_html(detail, style="legacy")
        self.assertIn("frf-obj", legacy_html)
        self.assertNotIn("{{ ctx.", legacy_html)

        entry = print_template_registry.get_whitelist_entry("return_receipt_base")
        self.assertIsNotNone(entry)
        self.assertIn("ir_path", entry)
        self.assertIn("v1", entry.get("variants", {}))

        ctx = return_receipt_context(detail)
        self.assertEqual(ctx["Gdate"], "2026.04.24")
        self.assertEqual(ctx["Gsqut"], 5)
        self.assertEqual(ctx["Gssum"], 7800)
        self.assertEqual(ctx["Line1_Bname"], "책1")

    def test_TC_PR_P1_37_return_legacy_style_falls_back_to_modern(self) -> None:
        """Sobo23 legacy 템플릿 렌더 실패도 500이 아니라 modern HTML로 폴백한다."""
        from app.services import returns_service

        detail = {
            "return_key": {"gdate": "2026.04.24", "hcode": "5053", "jubun": "11"},
            "customer": {"hcode": "5053", "hname": "반품거래처"},
            "lines": [{"bcode": "B", "bname": "책", "pubun": "A", "gsqut": 1, "gssum": 1000, "yesno": "0"}],
        }
        with patch("app.services.print_template_registry.try_render_with_ir", return_value=None):
            html = returns_service.render_return_receipt_html(detail, style="legacy")
        self.assertIn("Sobo23.DBGrid101.GSQUT", html)
        self.assertNotIn("frf-obj", html)


if __name__ == "__main__":
    main()
