"""Sobo21 거래명세서 LIST — gubun(거래구분) 필터가 서비스에 전달되는지 검증."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase
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


class SalesStatementGubunFilterTest(TestCase):
    def test_list_passes_gubun_to_service(self) -> None:
        captured: dict = {}

        async def fake_list(**kwargs):
            captured.update(kwargs)
            return [], 0

        with patch.object(
            transactions_service, "list_sales_statements", side_effect=fake_list
        ):
            res = TestClient(app).get(
                "/api/v1/transactions/sales-statement"
                "?serverId=remote_1&dateFrom=2026-04-01&dateTo=2026-04-18"
                "&gubun=%EC%B6%9C%EA%B3%A0&gcode=00000"
            )

        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured.get("gubun"), "출고")
        self.assertEqual(captured.get("gcode"), "00000")


if __name__ == "__main__":
    import unittest

    unittest.main()
