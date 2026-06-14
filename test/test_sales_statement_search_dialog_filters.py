"""거래현황(상세) Subu24 검색 다이얼로그 — 도서코드/도서구분 라인 필터 (DEC-065 P4).

레거시 정본: WeLove_FTP/도서유통-출판/Subu24.{pas,dfm} — 거래일자·거래구분·전표구분·
거래처명·도서구분·도서코드 필터. S1_Ssub 행=라인이므로 Bcode/Pubun 동등 매칭(파생테이블 불요).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
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


class RouterPassesFiltersTest(TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_current_user] = _override_auth
        self.client = TestClient(app)

    def test_list_passes_bcode_and_pubun_to_service(self) -> None:
        captured: dict = {}

        async def fake_list(**kwargs):
            captured.update(kwargs)
            return [], 0

        with patch.object(transactions_service, "list_sales_statements", side_effect=fake_list):
            res = self.client.get(
                "/api/v1/transactions/sales-statement"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-30"
                "&bcode=3411&pubun=%EC%9C%84%ED%83%81"  # 위탁
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("bcode"), "3411")
        self.assertEqual(captured.get("pubun"), "위탁")


class WhereBuilderTest(IsolatedAsyncioTestCase):
    async def test_where_includes_bcode_and_pubun_equality(self) -> None:
        async def _noop_gjisa(where, params, **kwargs):  # noqa: ARG001
            return None

        async def _no_idnum(_sid):  # noqa: ARG001
            return False

        with patch.object(transactions_service, "_append_gjisa_filter_async", side_effect=_noop_gjisa), \
             patch("app.services.s1_ssub_adapt.s1_has_idnum_column", side_effect=_no_idnum), \
             patch.object(transactions_service, "sales_statement_ocode_sql", return_value="Ocode='B'"):
            where_sql, params = await transactions_service._build_sales_statement_list_where(
                server_id="remote_1",
                date_from="2026-04-01",
                date_to="2026-04-30",
                bcode="3411",
                pubun="위탁",
            )
        self.assertIn("Bcode = %s", where_sql)
        self.assertIn("Pubun = %s", where_sql)
        self.assertIn("3411", params)
        self.assertIn("위탁", params)

    async def test_no_bcode_pubun_clause_when_absent(self) -> None:
        async def _noop_gjisa(where, params, **kwargs):  # noqa: ARG001
            return None

        async def _no_idnum(_sid):  # noqa: ARG001
            return False

        with patch.object(transactions_service, "_append_gjisa_filter_async", side_effect=_noop_gjisa), \
             patch("app.services.s1_ssub_adapt.s1_has_idnum_column", side_effect=_no_idnum), \
             patch.object(transactions_service, "sales_statement_ocode_sql", return_value="Ocode='B'"):
            where_sql, _ = await transactions_service._build_sales_statement_list_where(
                server_id="remote_1", date_from="2026-04-01", date_to="2026-04-30",
            )
        self.assertNotIn("Bcode = %s", where_sql)
        self.assertNotIn("Pubun = %s", where_sql)


if __name__ == "__main__":
    main()
