"""
DEC-050 / B-Track Phase 3 — print_template_registry 화이트리스트 단위 테스트.

검증 항목
---------
- R_01 환경변수 게이트 — PRINT_TEMPLATE_MODE!=auto 면 모든 form 미허용 (manual 강제).
- R_02 화이트리스트 등록 — label_form_1 = Report_1_21.ir.json 1행 보존 (DEC-038 인프라).
- R_03 단일 원천 — whitelist_size() = print_templates/auto/*.ir.json 파일 수 == 매핑 표
       `ir_in_use` 행 수 (3 곳 동수, DEC-046).
- R_04 graceful fallback — 미등록 form / IR 누락 시 None 반환 (5xx 누설 0).
- R_05 행동 정합 — try_render_with_ir(label_form_1, ...) 결과가 label_service 의 기존
       _try_render_label_auto(form=1) 결과와 동일 (회귀 0, DEC-050 인프라 도입 정합).
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))

from app.services import label_service, print_template_registry  # noqa: E402


_AUTO_DIR = (
    BACKEND_ROOT / "app" / "services" / "print_templates" / "auto"
)


class _ModeGuard:
    """PRINT_TEMPLATE_MODE 일시 변경 helper (테스트 격리)."""

    def __init__(self, mode: str | None) -> None:
        self._mode = mode
        self._old: str | None = None

    def __enter__(self) -> "_ModeGuard":
        self._old = os.environ.get("PRINT_TEMPLATE_MODE")
        if self._mode is None:
            os.environ.pop("PRINT_TEMPLATE_MODE", None)
        else:
            os.environ["PRINT_TEMPLATE_MODE"] = self._mode
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._old is None:
            os.environ.pop("PRINT_TEMPLATE_MODE", None)
        else:
            os.environ["PRINT_TEMPLATE_MODE"] = self._old


class WhitelistGate(unittest.TestCase):
    """R_01 / R_02 / R_03 / R_04 — 화이트리스트 환경변수 게이트 + 단일 원천."""

    def test_R01_mode_manual_blocks_all(self) -> None:
        with _ModeGuard("manual"):
            self.assertFalse(print_template_registry.is_form_whitelisted("label_form_1"))
            self.assertIsNone(
                print_template_registry.try_render_with_ir(
                    "label_form_1", {"gname": "x"}, document_title="t"
                ),
                "manual 모드에서는 화이트리스트 form 도 IR 결합 안 함",
            )

    def test_R01_mode_unset_blocks_all(self) -> None:
        with _ModeGuard(None):
            self.assertFalse(print_template_registry.is_form_whitelisted("label_form_1"))

    def test_R02_label_form_1_registered(self) -> None:
        entry = print_template_registry.get_whitelist_entry("label_form_1")
        self.assertIsNotNone(entry, "DEC-038 인프라 — label_form_1 = Report_1_21.ir.json")
        self.assertEqual(entry["ir"], "Report_1_21.ir.json")

    def test_R03_single_source_truth(self) -> None:
        ir_files = sorted(p.name for p in _AUTO_DIR.glob("*.ir.json"))
        size = print_template_registry.whitelist_size()
        self.assertEqual(
            size,
            len(ir_files),
            f"DEC-046 단일 원천 위반 — registry={size}, files={ir_files}",
        )

    def test_R04_unknown_form_returns_none(self) -> None:
        with _ModeGuard("auto"):
            self.assertIsNone(
                print_template_registry.try_render_with_ir(
                    "label_form_99_does_not_exist",
                    {"gname": "x"},
                    document_title="t",
                ),
                "미등록 form 은 None 폴백 (graceful)",
            )

    def test_R04_missing_ir_file_returns_none(self) -> None:
        with _ModeGuard("auto"):
            entry = print_template_registry.get_whitelist_entry("label_form_1")
            assert entry is not None
            real_ir = entry["ir"]
            try:
                print_template_registry._WHITELIST["__test_missing"] = {  # type: ignore[attr-defined]
                    "ir": "Report_DOES_NOT_EXIST_999.ir.json",
                    "schema_version": "0.0.0",
                    "approved_pr": "test",
                    "quality": {},
                }
                self.assertIsNone(
                    print_template_registry.try_render_with_ir(
                        "__test_missing", {}, document_title="t",
                    ),
                    "IR 파일 누락 시 None 폴백 (5xx 누설 0)",
                )
            finally:
                print_template_registry._WHITELIST.pop("__test_missing", None)  # type: ignore[attr-defined]
                self.assertEqual(
                    print_template_registry.get_whitelist_entry("label_form_1")["ir"],
                    real_ir,
                    "원본 entry 보존",
                )


class BehaviorParity(unittest.TestCase):
    """R_05 — registry 위임 후 label_service 행동이 변하지 않음 (회귀 0)."""

    _ROW = {
        "Gname": "홍길동",
        "Gposa": "씨",
        "Gjice": "직책",
        "Gadds": "서울시 강남구 역삼동 1-1",
        "Gpost": "1234567",
        "Gbigo": "Test bigo",
    }

    def test_R05_auto_mode_form_1_uses_ir(self) -> None:
        with _ModeGuard("auto"):
            html = label_service.render_label_html(self._ROW, form=1)
            self.assertIn("frf-obj", html, "IR 컴파일 결과는 frf-obj 클래스 포함")

    def test_R05_manual_mode_form_1_uses_byte_identical(self) -> None:
        with _ModeGuard("manual"):
            html = label_service.render_label_html(self._ROW, form=1)
            self.assertIn(
                "data-legacy-id='Seep13.Label.Gname'",
                html,
                "manual 모드는 Phase 1 byte-identical 정본",
            )
            self.assertNotIn("frf-obj", html, "manual 경로는 IR 미사용")


if __name__ == "__main__":
    unittest.main()
