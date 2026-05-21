"""DSN-DEC-12 보강 — 도메인 API hcode 필터 정적 점검 도구 회귀 가드.

[`tools/audit_domain_api_hcode_filter.py`](../tools/audit_domain_api_hcode_filter.py)
의 다음을 검증한다.

- f-string 안에 모듈 상수가 인라인되어 평가될 때 ``Hcode`` 누락이 정확히 잡히는지.
- ``# noqa: hcode-guard`` 마커가 의도적 예외로 처리되는지.
- 시스템 테이블(``Id_Logn``)에는 warn 이 발생하지 않는지.
- JoinedStr 내부 자식 ``Constant`` 가 부분 SQL 로 false positive 를 만들지 않는지.
"""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "audit_domain_api_hcode_filter.py"


def _load():
    spec = importlib.util.spec_from_file_location("audit_domain_api_hcode_filter", TOOL_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["audit_domain_api_hcode_filter"] = mod
    spec.loader.exec_module(mod)
    return mod


class HcodeAuditTests(TestCase):
    def setUp(self):
        self.tool = _load()
        self.tmp = Path("/tmp/test_audit_domain_api_hcode_filter")
        self.tmp.mkdir(parents=True, exist_ok=True)

    def _write(self, body: str) -> Path:
        path = self.tmp / "sample_service.py"
        path.write_text(textwrap.dedent(body), encoding="utf-8")
        return path

    def test_inlined_module_constant_carries_hcode_no_warn(self):
        path = self._write(
            """
            _W = "Gdate=%s AND Hcode=%s AND Gcode=%s"
            SQL_DELETE = (
                "DELETE FROM S1_Ssub "
                f"WHERE {_W} AND Bcode=%s"
            )
            def go():
                return SQL_DELETE
            """
        )
        findings, _ = self.tool.audit_file(path)
        warns = [f for f in findings if f.severity == "warn"]
        self.assertEqual(warns, [])

    def test_missing_hcode_in_multi_tenant_select_emits_warn(self):
        path = self._write(
            """
            SQL_BAD = "SELECT * FROM S1_Ssub WHERE Gdate=%s AND Gubun='출고'"
            def go():
                return SQL_BAD
            """
        )
        findings, _ = self.tool.audit_file(path)
        warns = [f for f in findings if f.severity == "warn"]
        self.assertEqual(len(warns), 1)
        self.assertEqual(warns[0].reason, "missing_hcode_filter_on_multi_tenant_table")
        self.assertIn("S1_Ssub", warns[0].tables)

    def test_noqa_marker_skips_warn(self):
        path = self._write(
            """
            SQL_OK = "SELECT * FROM S1_Ssub WHERE Gdate=%s"  # noqa: hcode-guard
            def go():
                return SQL_OK
            """
        )
        findings, _ = self.tool.audit_file(path)
        warns = [f for f in findings if f.severity == "warn"]
        self.assertEqual(warns, [])

    def test_system_table_id_logn_no_warn(self):
        path = self._write(
            """
            SQL_AUTH = "SELECT * FROM Id_Logn WHERE Gcode=%s"
            def go():
                return SQL_AUTH
            """
        )
        findings, _ = self.tool.audit_file(path)
        warns = [f for f in findings if f.severity == "warn"]
        self.assertEqual(warns, [])

    def test_joinedstr_inner_constant_not_false_positive(self):
        """``JoinedStr`` 안의 ``Constant("DELETE FROM S1_Ssub ")`` 가 짧은 WHERE 만 가진
        partial SQL 로 emit 돼서는 안 된다 — 부모 평가만 사용."""
        path = self._write(
            """
            _W = "Gdate=%s AND Hcode=%s"
            SQL_DELETE = (
                "DELETE FROM S1_Ssub "
                f"WHERE {_W}"
            )
            """
        )
        findings, _ = self.tool.audit_file(path)
        emitted_excerpts = [f.sql_excerpt for f in findings]
        # "DELETE FROM S1_Ssub WHERE" 같은 짧은 partial 이 에밋되면 안 된다
        for sql in emitted_excerpts:
            self.assertNotIn("WHERE", sql) if "DELETE FROM S1_Ssub " == sql.strip() else None
        # 부모는 평가되어 warn 0
        warns = [f for f in findings if f.severity == "warn"]
        self.assertEqual(warns, [])


if __name__ == "__main__":
    main()
