"""S1_Ssub 쓰기 경로 hcode 격리 가드 — noqa(hcode-guard) 마커의 근거를 강제.

배경: hcode 정적 감사(critical 6건, 2026-07-03)는 동적 WHERE 빌더(f-string) 내부를
볼 수 없어 오탐이었다. 각 사이트에 ``# noqa: hcode-guard`` 를 달되, 그 근거인
"빌더가 반드시 Hcode=%s 를 포함한다" 를 본 테스트가 기능적으로 강제한다.
빌더에서 Hcode 절이 제거되면 noqa 와 무관하게 여기서 즉시 실패한다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import outbound_service, transactions_service  # noqa: E402


class OutboundHdrWhereGuard(TestCase):
    def test_hdr_where_includes_hcode_bind(self) -> None:
        # cancel_order / _transition_yesno 의 UPDATE WHERE 원천.
        self.assertIn("Hcode=%s", outbound_service._SQL_OUTBOUND_ORDER_HDR_WHERE)
        self.assertIn("Hcode=%s", outbound_service._hdr_where("00001"))
        self.assertIn("Hcode=%s", outbound_service._hdr_where(""))

    def test_hdr_params_binds_hcode_in_position(self) -> None:
        where = outbound_service._hdr_where("00001")
        params = outbound_service._hdr_params("2026.07.03", "H1", "00001", "00001")
        # Hcode=%s 가 몇 번째 바인드인지 → 같은 위치의 파라미터가 hcode 여야 한다.
        idx = [m.start() for m in re.finditer(r"%s", where)]
        hpos = len(re.findall(r"%s", where[: where.index("Hcode=%s")]))
        self.assertEqual(params[hpos], "H1")


class StmtLineWhereGuard(TestCase):
    def test_stmt_line_where_includes_hcode_bind(self) -> None:
        # mark_sales_statement_completed / delete_sales_statement 의 WHERE 원천.
        where, params = transactions_service._build_stmt_line_where(
            "2026.07.03", "H1", "00001", "",
        )
        self.assertIn("Hcode=%s", where)
        hpos = len(re.findall(r"%s", where[: where.index("Hcode=%s")]))
        self.assertEqual(params[hpos], "H1")


class CreateServiceKeyWhereGuard(TestCase):
    def test_update_statement_key_where_literal_has_hcode(self) -> None:
        # update_sales_statement 의 key_where 는 로컬 리터럴 — 소스 스캔으로 강제.
        src = (BACKEND / "app" / "services" / "sales_statement_create_service.py").read_text(
            encoding="utf-8"
        )
        self.assertRegex(src, r'key_where\s*=\s*f?"Gdate=%s AND Hcode=%s')


class NextJubunAndAuthorHistoryGuard(TestCase):
    """noqa 근거 — 로컬 WHERE 리터럴들의 Hcode 포함을 소스 스캔으로 강제."""

    def test_next_jubun_where_literal_has_hcode(self) -> None:
        src = (BACKEND / "app" / "services" / "outbound_service.py").read_text(encoding="utf-8")
        self.assertIn('where = "Gdate=%s AND Hcode=%s"', src)

    def test_author_history_where_has_hcode(self) -> None:
        src = (BACKEND / "app" / "services" / "author_history_service.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('"Hcode = %s"', src)
