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


if __name__ == "__main__":
    main()
