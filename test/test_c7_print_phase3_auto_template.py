"""
C7 비-FastReport 트랙 — 자동 템플릿 회귀 게이트 (R5 단계 정적/동작 회귀).

본 테스트는 [c7-nofr-porting](../) 계획의 § "5) 회귀 게이트 (성공 조건)" 의
**정적 + 동작** 차원 게이트. 시각 픽셀 diff (3 차원 중 시각) 는 WeasyPrint /
pdftoppm 의 시스템 의존성으로 본 PoC 단계에서는 *마커 테스트* 로만 가드하고,
운영 도입 시 실제 픽셀 diff 게이트를 추가한다.

검증 항목 (정적/동작/거버넌스):

[정적]
  - S_01 신규 비즈니스 SQL 0건 — print_ir_compiler / label_service 의 R&D 분기에
        SELECT/INSERT/UPDATE/DELETE 문 추가 0건
  - S_02 외부 SaaS / 상용 SDK 의존 0건 — FastReport / .NET / Pascal 런타임 호출 0건
  - S_03 Jinja2 / FastAPI 외부 의존성 require 0건 (운영 OPS 유지)
  - S_04 OSS NOTICE 의무 — frf_decoder_poc.py 헤더에 BSD-2 저작권 표시 보존

[동작]
  - B_01 PRINT_TEMPLATE_MODE=manual (기본) — render_label_html 결과가 Phase 1 의
        byte-identical 정본 (data-legacy-id=Seep13.* 포함) 과 동일 경로
  - B_02 PRINT_TEMPLATE_MODE=auto — 컴파일된 자동 HTML 산출 (frf-obj 클래스 + Memo*
        legacy id + 모든 placeholder 치환 완료)
  - B_03 PRINT_TEMPLATE_MODE=auto + IR 누락 양식 → manual fallback (graceful)
  - B_04 컴파일러 단위 — 임의 IR 입력에 대한 안정성 (빈 IR / Picture 객체 skip)

[거버넌스]
  - G_01 IR 스키마 / shortlist / license matrix / discovery log 4 산출물 존재
  - G_02 자동 템플릿 디렉토리 (`print_templates/auto/`) 에 최소 1 IR 적재
"""
from __future__ import annotations

import json
import os
import re
import sys
import unittest
from html import escape
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))

from app.services import label_service  # noqa: E402
from app.services import print_ir_compiler  # noqa: E402


_AUTO_DIR = BACKEND_ROOT / "app" / "services" / "print_templates" / "auto"


# ---------------------------------------------------------------------------
# Static gates
# ---------------------------------------------------------------------------


class StaticGatesC7AutoTemplate(unittest.TestCase):
    """정적 차원 회귀 게이트 (단순 텍스트 기반 확인)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler_src = (BACKEND_ROOT / "app" / "services" / "print_ir_compiler.py").read_text(encoding="utf-8")
        cls.label_src = (BACKEND_ROOT / "app" / "services" / "label_service.py").read_text(encoding="utf-8")
        cls.decoder_src = (REPO_ROOT / "debug" / "frf_decoder_poc.py").read_text(encoding="utf-8")

    def test_S_01_no_new_business_sql_in_compiler(self) -> None:
        forbidden = re.compile(
            r"\b(SELECT|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM)\b",
            re.IGNORECASE,
        )
        self.assertFalse(
            forbidden.search(self.compiler_src),
            msg="print_ir_compiler.py 는 데이터 조회/변경 책임 없음 — SQL 0",
        )

    def test_S_02_no_external_saas_or_commercial_sdk(self) -> None:
        forbidden_tokens = (
            "FastReport.dll",
            "frxClass",
            "frxExportPDF",
            "frxExportHTML",
            "fast-report.com",
            "stimulsoft",
            "DocuSign",
            "AWS_ACCESS_KEY",
        )
        for src_name, src in (
            ("print_ir_compiler.py", self.compiler_src),
            ("label_service.py", self.label_src),
            ("frf_decoder_poc.py", self.decoder_src),
        ):
            for token in forbidden_tokens:
                self.assertNotIn(
                    token,
                    src,
                    msg=f"{src_name} 에 외부 SaaS/상용 SDK 토큰 발견: {token}",
                )

    def test_S_03_no_jinja2_or_fastapi_runtime_dep(self) -> None:
        forbidden_imports = (
            "from jinja2",
            "import jinja2",
            "from fastapi",
            "import fastapi",
        )
        for token in forbidden_imports:
            self.assertNotIn(
                token,
                self.compiler_src,
                msg=f"print_ir_compiler 는 운영 의존성 0 정책 — '{token}' 금지",
            )

    def test_S_04_decoder_header_bsd2_notice(self) -> None:
        head = self.decoder_src[:3000]
        for token in ("BSD-2", "Fast Reports", "Redistribution"):
            self.assertIn(token, head, msg=f"BSD-2 NOTICE 토큰 누락: {token}")


# ---------------------------------------------------------------------------
# Behavior gates
# ---------------------------------------------------------------------------


_SAMPLE_ROW = {
    "Gname": "홍길동",
    "Gposa": "대표이사",
    "Gjice": "본사",
    "Gadds": "서울시 강남구 테헤란로 123",
    "Gpost": "0612345",
    "Gbigo": "메모",
}

_AUTO_ROW = {
    **_SAMPLE_ROW,
    "Gadd1": "서울시 강남구",
    "Gadd2": "테헤란로 123",
}


class BehaviorGatesC7AutoTemplate(unittest.TestCase):
    def setUp(self) -> None:
        self._mode_backup = os.environ.get("PRINT_TEMPLATE_MODE")

    def tearDown(self) -> None:
        if self._mode_backup is None:
            os.environ.pop("PRINT_TEMPLATE_MODE", None)
        else:
            os.environ["PRINT_TEMPLATE_MODE"] = self._mode_backup

    def test_B_01_manual_default_path(self) -> None:
        os.environ.pop("PRINT_TEMPLATE_MODE", None)
        html = label_service.render_label_html(_SAMPLE_ROW, form=1)
        self.assertIn("data-legacy-id='Seep13.Label.Gname'", html)
        self.assertIn("홍길동", html)
        self.assertNotIn("frf-obj", html)
        self.assertNotIn("{{ ctx.", html)

    def test_B_02_auto_path_full_render(self) -> None:
        os.environ["PRINT_TEMPLATE_MODE"] = "auto"
        html = label_service.render_label_html(_AUTO_ROW, form=1)
        self.assertIn("frf-obj", html)
        self.assertRegex(html, r"data-legacy-id='Memo\d+'")
        self.assertNotIn("{{ ctx.", html, msg="placeholder 치환 누락")
        self.assertIn("홍길동", html)
        self.assertIn(escape("대표이사"), html)
        self.assertIn(escape("서울시 강남구"), html)
        self.assertIn(escape("테헤란로 123"), html)

    def test_B_03_auto_fallback_when_ir_missing(self) -> None:
        os.environ["PRINT_TEMPLATE_MODE"] = "auto"
        html = label_service.render_label_html(_SAMPLE_ROW, form=4)
        self.assertIn("data-legacy-id='Seep13.Label.Gname'", html)
        self.assertNotIn("frf-obj", html, msg="manual fallback 실패")

    def test_B_04_compiler_handles_empty_ir(self) -> None:
        empty_ir = {"schema_version": "0.1.0", "pages": [], "report": {"title": "Empty"}, "source": {}}
        html = print_ir_compiler.compile_ir_to_html(empty_ir)
        self.assertIn("(빈 IR)", html)
        self.assertNotIn("Traceback", html)

    def test_B_05_compiler_renders_picture_placeholder_and_text(self) -> None:
        """v0.2: Picture/Line/Rect 등 비텍스트 객체도 placeholder 로 렌더된다.

        v0.1 까지는 Picture 가 HTML 주석으로 skip 되었지만, v0.2 부터 시각 가시성을 위해
        `frf-pic` placeholder 를 출력한다 (analysis/print_specs/frf_ir_schema.md §8 참조).
        """
        ir = {
            "schema_version": "0.1.0",
            "source": {"filename": "x.frf"},
            "report": {"title": "T"},
            "pages": [
                {
                    "name": "P1",
                    "size_mm": {"width": 100.0, "height": 148.0},
                    "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                    "bands": [
                        {
                            "name": "B1",
                            "type": "MasterData",
                            "objects": [
                                {
                                    "name": "Pic1",
                                    "type": "Picture",
                                    "rect_mm": {"x": 0, "y": 0, "w": 10, "h": 10},
                                    "binding": {"kind": "literal", "raw": ""},
                                    "unsupported_props": {},
                                    "style": {},
                                },
                                {
                                    "name": "T1",
                                    "type": "Text",
                                    "rect_mm": {"x": 0, "y": 0, "w": 50, "h": 6},
                                    "binding": {"kind": "literal", "value": "hello"},
                                    "unsupported_props": {},
                                    "style": {"font_size_pt": 12.0, "halign": "left", "color": "#222"},
                                },
                            ],
                        }
                    ],
                }
            ],
        }
        html = print_ir_compiler.compile_ir_to_html(ir)
        self.assertIn("frf-pic", html)
        self.assertIn("data-legacy-id='Pic1'", html)
        self.assertIn("hello", html)


# ---------------------------------------------------------------------------
# Governance gates
# ---------------------------------------------------------------------------


class GovernanceGatesC7AutoTemplate(unittest.TestCase):
    def test_G_01_oss_gate_deliverables_exist(self) -> None:
        for rel in (
            "analysis/research/c7_oss_discovery_log_20260420.md",
            "analysis/research/c7_oss_shortlist.md",
            "analysis/research/c7_oss_license_matrix.md",
            "analysis/print_specs/frf_ir_schema.md",
        ):
            path = REPO_ROOT / rel
            self.assertTrue(path.is_file(), msg=f"missing: {rel}")
            self.assertGreater(path.stat().st_size, 1500, msg=f"too small: {rel}")

    def test_G_02_at_least_one_ir_staged(self) -> None:
        irs = list(_AUTO_DIR.glob("*.ir.json"))
        self.assertGreaterEqual(len(irs), 1, msg=f"no IR staged in {_AUTO_DIR}")
        for path in irs:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("schema_version", data)
            self.assertIn("pages", data)


if __name__ == "__main__":
    unittest.main()
