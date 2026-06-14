"""`_build_stmt_line_where` — LIST 와 동일 Ocode 필터 회귀 (DEC-064 §Idnum 상세수정)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


class StmtLineWhereOcodeTest(TestCase):
    def test_chul09_remote_153_includes_ocode_a(self) -> None:
        from app.services import transactions_service as svc

        sql, _params = svc._build_stmt_line_where(
            "2026.06.04",
            "5019",
            "11",
            "",
            idnum=1,
            gubun="출고",
            gcode="00405",
            server_id="remote_153",
        )
        self.assertIn("Ocode = 'A'", sql)

    def test_non_chul09_server_includes_ocode_b(self) -> None:
        from app.services import transactions_service as svc

        sql, _params = svc._build_stmt_line_where(
            "2026.06.04",
            "5019",
            "11",
            "",
            server_id="remote_no_such",
        )
        self.assertIn("Ocode = 'B'", sql)

    def test_memo_path_without_server_id_omits_ocode(self) -> None:
        from app.services import transactions_service as svc

        sql, _params = svc._build_stmt_line_where(
            "2026.06.04",
            "5019",
            "",
            "",
        )
        self.assertNotIn("Ocode =", sql)

    def test_jubun_uses_variants_in_clause(self) -> None:
        from app.services import transactions_service as svc

        sql, params = svc._build_stmt_line_where(
            "2026.06.04",
            "5019",
            "11",
            "",
            server_id="remote_153",
        )
        self.assertIn("COALESCE(Jubun,'') IN", sql)
        self.assertIn("11", params)


if __name__ == "__main__":
    from unittest import main

    main()
