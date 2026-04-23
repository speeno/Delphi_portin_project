"""delphi_form_screen_matrix.py 회귀 가드 (DEC-061).

- 모듈 로드·스캔·파서 스모크
- ``--check`` 기본(DFM 존재) exit 0
- Subu45 루트 Caption 이 청구서관리 (DEC-060 정합)
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]

_SPEC = importlib.util.spec_from_file_location(
    "delphi_form_screen_matrix",
    ROOT / "tools" / "delphi_form_screen_matrix.py",
)
assert _SPEC and _SPEC.loader
_m = importlib.util.module_from_spec(_SPEC)
sys.modules["delphi_form_screen_matrix"] = _m
_SPEC.loader.exec_module(_m)


class DelphiFormScreenMatrixTests(TestCase):
    def test_subu45_dfm_caption_is_billing_not_logistics(self) -> None:
        dfm = ROOT / "legacy_delphi_source" / "legacy_source" / "Subu45.dfm"
        _obj, cap = _m.extract_root_form_and_caption(dfm)
        self.assertIn("청구", cap, cap)
        self.assertIn("관리", cap, cap)
        self.assertNotIn("물류", cap)

    def test_parse_registry_has_billing_and_customer(self) -> None:
        ts = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
        entries = _m.parse_form_registry_entries(ts)
        ids = {e["id"] for e in entries}
        self.assertIn("Sobo45_billing", ids)
        self.assertIn("Sobo11", ids)
        self.assertNotIn("Sobo45", ids, "구 물류비 잘못 ID는 제거되어야 함")

    def test_scan_legacy_has_subu45(self) -> None:
        inv = _m.scan_legacy_dfms()
        self.assertIn("Subu45", inv)
        self.assertEqual(inv["Subu45"]["form_object"], "Sobo45")

    def test_cli_check_exits_zero(self) -> None:
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "delphi_form_screen_matrix.py"), "--check"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)


if __name__ == "__main__":
    main()
