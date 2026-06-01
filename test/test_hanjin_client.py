from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.carriers import hanjin_client


class _FakeResponse:
    def __init__(self, payload: dict):
        self._raw = json.dumps(payload).encode("utf-8")
        self.status = 200

    def read(self, _size: int = -1) -> bytes:
        return self._raw

    def getcode(self) -> int:
        return self.status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        return None


class HanjinClientTest(TestCase):
    def test_is_enabled_false_without_required_settings(self) -> None:
        with patch("app.services.carriers.hanjin_client.config.HANJIN_API_ENABLED", False):
            self.assertFalse(hanjin_client.is_enabled())

    def test_fetch_tracking_maps_delivered_status(self) -> None:
        payload = {
            "data": {
                "statusName": "배송완료",
            }
        }
        with patch("app.services.carriers.hanjin_client.is_enabled", return_value=True), patch(
            "app.services.carriers.hanjin_client.open_api_http.urlopen",
            return_value=_FakeResponse(payload),
        ):
            out = hanjin_client.fetch_tracking("1234567890")
        self.assertEqual(out["tracking_no"], "1234567890")
        self.assertEqual(out["status"], "delivered")
        self.assertEqual(out["status_text"], "배송완료")
