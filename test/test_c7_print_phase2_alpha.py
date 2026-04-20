"""
C7 인쇄 Phase 2-α — 거래처 변형 + 라벨 5종 양식 검증 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/print_invoice.yaml v1.1.0 (Sobo27 v0..v9 / Sobo23 v1,v2,v3,v5)
- migration/contracts/print_label.yaml v1.1.0 (form 1..5)
- analysis/layout_mappings/Sobo27.md §11.1 (10 변형)
- analysis/layout_mappings/Sobo23.md §11.1 (4 변형)
- analysis/layout_mappings/Seep13_label.md §8.1 (5 form)

검증 케이스 (~24건 — 18 변형 + 정적 검사 6)
-----------------------------------------------
- TC-P2A-01..10  Sobo27 v0..v9 변형별 PDF + 헤더 텍스트 차이 + 신규 SQL 0
- TC-P2A-11..14  Sobo23 v1/v2/v3/v5 변형별 PDF
- TC-P2A-15      Sobo23 v4 (결번) → 422 PR_VARIANT_UNSUPPORTED
- TC-P2A-16      Sobo27 vX (미정의) → 422 PR_VARIANT_UNSUPPORTED
- TC-P2A-17..21  라벨 form=1..5 PDF (form=1 byte-identical, form=4/5 column-count)
- TC-P2A-22      라벨 form=6 → 422 PR_FORM_UNSUPPORTED (FastAPI le=5 / PR_FORM_UNSUPPORTED)
- TC-P2A-23      base byte-identical 회귀 (variant 미지정 == base == Phase 1)
- TC-P2A-24      정적 검사 — contract / 매핑 노트 / 신규 SQL 0 (DML grep)

설계 정합 (사용자 룰)
---------------------
- C7 Phase 1 패턴(test_c7_print_phase1.py) 재사용 — monkeypatch + dependency_overrides.
- 신규 헬퍼 금지, test 폴더 한 파일.
- Phase 1 산출물과의 byte-identical 회귀 가드 (DEC-019/028 SOLID 원칙).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


# ──────────────────────────────────────────────
# T5 의존성 — 미착수 시점에는 안전 우회 (skipUnless)
# ──────────────────────────────────────────────
_RUNTIME_OK = False
try:
    from fastapi.testclient import TestClient  # noqa: E402
    from app.main import app  # noqa: E402
    from app.routers.auth import get_current_user  # noqa: E402

    def _override_auth() -> dict:
        return {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}

    app.dependency_overrides[get_current_user] = _override_auth

    from app.services import label_service as _label_service  # noqa: F401
    from app.services import outbound_service as _outbound_service  # noqa: F401
    from app.services import returns_service as _returns_service  # noqa: F401

    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]


# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
ORDER_KEY = "20260401|H0001|J00001"
ORDER_KEY_URL = "20260401%7CH0001%7CJ00001"
RETURN_KEY_URL = "G%7C20260401%7CH0001%7CJ00001"
SHIPMENT_KEY_URL = "S1_Ssub%7CK0001"

SAMPLE_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj << /Type /Catalog >> endobj\n"
    b"trailer << /Root 1 0 R >>\n"
    b"%%EOF\n"
)


def _pdf_signature_ok(body: bytes) -> bool:
    return body.startswith(b"%PDF-") and b"%%EOF" in body[-32:]


# ──────────────────────────────────────────────
# 1. Sobo27 (P1-C 출고 거래명세서) v0..v9 변형 (10건)
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 미착수 — 정적 검사만 실행")
class C7Phase2AlphaOutboundVariantsTestCase(TestCase):
    def setUp(self) -> None:
        assert app is not None and TestClient is not None
        self.client = TestClient(app)

    def _call(self, variant: str | None):
        from app.services import outbound_service, print_service
        params: dict = {"serverId": "remote_1"}
        if variant is not None:
            params["variant"] = variant
        captured: dict = {}

        def _capture_render(html: str, **_):
            captured["html"] = html
            return SAMPLE_PDF

        with patch.object(
            outbound_service, "get_order_detail",
            new=AsyncMock(return_value={"order_key": {"gdate": "20260401", "jubun": "J00001"},
                                        "customer": {"gname": "홍길동서점", "hcode": "H0001"},
                                        "lines": [{"gcode": "B1", "gsqut": 1, "gssum": 1000}]}),
        ), patch.object(print_service, "render_pdf", side_effect=_capture_render):
            res = self.client.get(
                f"/api/v1/print/outbound-statement/{ORDER_KEY_URL}.pdf",
                params=params,
            )
        return res, captured.get("html", "")

    def test_TC_P2A_01_to_10_outbound_v0_v9_pdf_signature(self) -> None:
        for i in range(10):
            with self.subTest(variant=f"v{i}"):
                res, html = self._call(f"v{i}")
                self.assertEqual(res.status_code, 200, msg=f"v{i} status")
                self.assertEqual(res.headers["content-type"], "application/pdf")
                self.assertTrue(_pdf_signature_ok(res.content))
                # 변형 헤더 라벨 차이 — '거래처 N' 텍스트가 HTML 에 포함
                self.assertIn(f"거래처 {i}", html, msg=f"v{i} header label not in html")

    def test_TC_P2A_15_outbound_invalid_variant_returns_422(self) -> None:
        res, _ = self._call("vX")
        self.assertEqual(res.status_code, 422)
        body = res.json()
        self.assertEqual(body["detail"]["code"], "PR_VARIANT_UNSUPPORTED")


# ──────────────────────────────────────────────
# 2. Sobo23 (P1-D 반품 영수증) v1/v2/v3/v5 변형 (4건) + v4 결번 422
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 미착수 — 정적 검사만 실행")
class C7Phase2AlphaReturnVariantsTestCase(TestCase):
    def setUp(self) -> None:
        assert app is not None and TestClient is not None
        self.client = TestClient(app)

    def _call(self, variant: str | None):
        from app.services import print_service, returns_service
        params: dict = {"serverId": "remote_1"}
        if variant is not None:
            params["variant"] = variant
        captured: dict = {}

        def _capture_render(html: str, **_):
            captured["html"] = html
            return SAMPLE_PDF

        with patch.object(
            returns_service, "get_return_detail",
            new=AsyncMock(return_value={"return_key": {"gdate": "20260401", "jubun": "J00001"},
                                        "customer": {"hname": "반품거래처", "hcode": "H0001"},
                                        "lines": [{"bcode": "B1", "gsqut": 1, "gssum": 1000, "yesno": "0"}]}),
        ), patch.object(print_service, "render_pdf", side_effect=_capture_render):
            res = self.client.get(
                f"/api/v1/print/return-receipt/{RETURN_KEY_URL}.pdf",
                params=params,
            )
        return res, captured.get("html", "")

    def test_TC_P2A_11_to_14_return_v1235_pdf_signature(self) -> None:
        for v_num in [1, 2, 3, 5]:
            with self.subTest(variant=f"v{v_num}"):
                res, html = self._call(f"v{v_num}")
                self.assertEqual(res.status_code, 200, msg=f"v{v_num} status")
                self.assertTrue(_pdf_signature_ok(res.content))
                self.assertIn(f"거래처 {v_num}", html, msg=f"v{v_num} header label not in html")

    def test_TC_P2A_15a_return_v4_missing_returns_422(self) -> None:
        """v4 결번 (-4 .frf 부재) — 라우터 422 가드."""
        res, _ = self._call("v4")
        self.assertEqual(res.status_code, 422)
        body = res.json()
        self.assertEqual(body["detail"]["code"], "PR_VARIANT_UNSUPPORTED")
        self.assertIn("v4", body["detail"]["message"])  # 결번 명시 안내


# ──────────────────────────────────────────────
# 3. 라벨 (P1-F) form 1..5 + form=6 422
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 미착수 — 정적 검사만 실행")
class C7Phase2AlphaLabelFormsTestCase(TestCase):
    def setUp(self) -> None:
        assert app is not None and TestClient is not None
        self.client = TestClient(app)

    def _call(self, form: int | None):
        from app.services import label_service, print_service
        params: dict = {"serverId": "remote_1"}
        if form is not None:
            params["form"] = form
        captured: dict = {}

        def _capture_render(html: str, **_):
            captured["html"] = html
            return SAMPLE_PDF

        with patch.object(
            label_service, "fetch_label_row",
            new=AsyncMock(return_value={"Gname": "홍길동", "Gposa": "사장",
                                        "Gjice": "직책", "Gadds": "주소", "Gpost": "12345"}),
        ), patch.object(print_service, "render_pdf", side_effect=_capture_render):
            res = self.client.get(
                f"/api/v1/print/label/{SHIPMENT_KEY_URL}.pdf",
                params=params,
            )
        return res, captured.get("html", "")

    def test_TC_P2A_17_to_21_label_form_1_to_5_pdf(self) -> None:
        expected_pages = {
            1: "100mm 148mm",
            2: "148mm 100mm",
            3: "148mm 105mm",
            4: "297mm 210mm",
            5: "210mm 297mm",
        }
        for form, page_size in expected_pages.items():
            with self.subTest(form=form):
                res, html = self._call(form)
                self.assertEqual(res.status_code, 200, msg=f"form={form} status")
                self.assertTrue(_pdf_signature_ok(res.content))
                self.assertIn(page_size, html, msg=f"form={form} @page size not in html")
                if form in (4, 5):
                    self.assertIn("column-count: 2", html, msg=f"form={form} 2단 분할 누락")

    def test_TC_P2A_22_label_form_6_returns_422(self) -> None:
        """form=6 → FastAPI Query(le=5) 가 먼저 막아 422 반환."""
        res, _ = self._call(6)
        # Query(le=5) 검증이면 FastAPI 표준 422 (validation), is_label_form_supported 분기 전에 차단됨.
        self.assertEqual(res.status_code, 422)


# ──────────────────────────────────────────────
# 4. base byte-identical 회귀 — Phase 1 산출물과 동일 (DEC-019/028)
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 미착수 — 정적 검사만 실행")
class C7Phase2AlphaByteIdenticalTestCase(TestCase):
    """variant 미지정 / variant=base / form=1 미지정 호출이 Phase 1 동일 HTML 산출."""

    def test_TC_P2A_23a_outbound_base_html_byte_identical(self) -> None:
        from app.services import outbound_service
        detail = {"order_key": {"gdate": "20260401", "jubun": "J00001"},
                  "customer": {"gname": "홍길동서점", "hcode": "H0001"},
                  "lines": [{"gcode": "B1", "gsqut": 1, "gssum": 1000}]}
        html_default = outbound_service.render_outbound_statement_html(detail)
        html_base = outbound_service.render_outbound_statement_html(detail, variant="base")
        self.assertEqual(html_default, html_base, "variant 미지정 != variant='base' — byte-identical 위반")
        self.assertIn("출고 거래명세서", html_base)
        self.assertNotIn("거래처 0", html_base, "base 변형에 거래처 N 라벨 누설")

    def test_TC_P2A_23b_return_base_html_byte_identical(self) -> None:
        from app.services import returns_service
        detail = {"return_key": {"gdate": "20260401", "jubun": "J00001"},
                  "customer": {"hname": "반품거래처", "hcode": "H0001"},
                  "lines": [{"bcode": "B1", "gsqut": 1, "gssum": 1000, "yesno": "0"}]}
        html_default = returns_service.render_return_receipt_html(detail)
        html_base = returns_service.render_return_receipt_html(detail, variant="base")
        self.assertEqual(html_default, html_base)
        self.assertIn("반품 영수증", html_base)
        self.assertNotIn("거래처 1", html_base)

    def test_TC_P2A_23c_label_form1_html_byte_identical(self) -> None:
        from app.services import label_service
        row = {"Gname": "홍길동", "Gposa": "사장", "Gjice": "직책",
               "Gadds": "주소", "Gpost": "12345"}
        html_default = label_service.render_label_html(row)
        html_form1 = label_service.render_label_html(row, form=1)
        self.assertEqual(html_default, html_form1, "form 미지정 != form=1 — byte-identical 위반")
        # form 2~5 와는 달라야 함
        html_form2 = label_service.render_label_html(row, form=2)
        self.assertNotEqual(html_form1, html_form2)


# ──────────────────────────────────────────────
# 5. 정적 검사 — contract / 매핑 노트 / 신규 SQL 0 (T5 무관)
# ──────────────────────────────────────────────
class C7Phase2AlphaStaticChecksTestCase(TestCase):
    def test_TC_P2A_24a_contract_print_invoice_v110_with_pdf_variants(self) -> None:
        """print_invoice.yaml v1.1.0 + Sobo27.pdf_variants v0..v9 + Sobo23.pdf_variants v1/v2/v3/v5."""
        text = (ROOT / "migration" / "contracts" / "print_invoice.yaml").read_text(encoding="utf-8")
        self.assertIn("version: 1.1.0", text, "print_invoice.yaml 버전 미갱신")
        for v in ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"]:
            self.assertIn(f"{v}:", text, f"Sobo27.pdf_variants.{v} 누락")
        # Sobo23: v1/v2/v3/v5 만 (v4 결번)
        self.assertIn("Report_2_13-1.frf", text)
        self.assertIn("Report_2_13-5.frf", text)
        # 결번 안내 문구 존재
        self.assertIn("결번", text)

    def test_TC_P2A_24b_contract_print_label_v110_with_label_forms(self) -> None:
        text = (ROOT / "migration" / "contracts" / "print_label.yaml").read_text(encoding="utf-8")
        self.assertIn("version: 1.1.0", text)
        self.assertIn("label_forms:", text)
        for f, frf in [
            (1, "Report_1_21.frf"),
            (2, "Report_1_22.frf"),
            (3, "Report_1_23.frf"),
            (4, "Report_1_24.frf"),
            (5, "Report_1_25.frf"),
        ]:
            self.assertIn(f'"{f}":', text, f'label_forms."{f}" 누락')
            self.assertIn(frf, text, f"{frf} 누락")

    def test_TC_P2A_24c_layout_mapping_notes_have_variant_tables(self) -> None:
        sobo27 = (ROOT / "analysis" / "layout_mappings" / "Sobo27.md").read_text(encoding="utf-8")
        sobo23 = (ROOT / "analysis" / "layout_mappings" / "Sobo23.md").read_text(encoding="utf-8")
        seep13 = (ROOT / "analysis" / "layout_mappings" / "Seep13_label.md").read_text(encoding="utf-8")
        self.assertIn("11.1 Phase 2-α 거래처별 변형 표 (10 변형)", sobo27)
        self.assertIn("11.1 Phase 2-α 거래처별 변형 표 (4 변형)", sobo23)
        self.assertIn("8.1 Phase 2-α 라벨 5종 양식 표", seep13)

    def test_TC_P2A_24d_no_new_sql_in_phase2_alpha_services(self) -> None:
        """Phase 2-α 도입으로 신규 SELECT/INSERT/UPDATE/DELETE 0건 — variant 분기는 헤더 라벨/CSS 만."""
        # outbound_service / returns_service / label_service Phase 2-α 패치 영역 (variant/form 추가 부분) 안에
        # SELECT/INSERT/UPDATE/DELETE 가 없어야 한다.
        files = [
            BACKEND / "app" / "services" / "outbound_service.py",
            BACKEND / "app" / "services" / "returns_service.py",
            BACKEND / "app" / "services" / "label_service.py",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            # Phase 2-α 식별 마커 (_OUTBOUND_VARIANT_LABELS / _RETURN_VARIANT_LABELS / _LABEL_FORM_SPECS)
            # 이후 ~80 줄 윈도우 안에 DML 이 들어있지 않은지.
            for marker in ("_OUTBOUND_VARIANT_LABELS", "_RETURN_VARIANT_LABELS", "_LABEL_FORM_SPECS"):
                idx = text.find(marker)
                if idx == -1:
                    continue
                window = text[idx: idx + 4000]
                # 대문자 SQL 키워드 정확 매칭 (Python 문자열 리터럴 안만)
                for kw in (" SELECT ", " INSERT ", " UPDATE ", " DELETE "):
                    self.assertNotIn(kw, window.upper(),
                                     f"{path.name}::{marker} 윈도우에 신규 DML({kw.strip()}) 누설")

    def test_TC_P2A_24e_router_has_variant_and_form_query_params(self) -> None:
        text = (BACKEND / "app" / "routers" / "print.py").read_text(encoding="utf-8")
        self.assertIn('variant: str = Query("base"', text, "outbound/return variant 쿼리 누락")
        self.assertIn("ge=1, le=5", text, "label form 범위 1..5 미확장")
        self.assertIn("PR_VARIANT_UNSUPPORTED", text)
        self.assertIn("PR_FORM_UNSUPPORTED", text)

    def test_TC_P2A_24f_plan_doc_changelog_entry(self) -> None:
        """계획서 §7-C7 또는 §8 변경 이력에 Phase 2-α 가시화."""
        text = (ROOT / "docs" / "core-scenarios-porting-plan.md").read_text(encoding="utf-8")
        # 변경 이력 또는 §7-C7 본문에 Phase 2-α 키워드 1건 이상.
        self.assertTrue(
            re.search(r"Phase 2-α|phase2_alpha|phase 2-α", text, re.IGNORECASE),
            "core-scenarios-porting-plan.md 에 Phase 2-α 흔적 없음 — T7/T8 갱신 누락",
        )


if __name__ == "__main__":
    main(verbosity=2)
