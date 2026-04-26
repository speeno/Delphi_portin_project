"""FastAPI nav / admin / masters 스모크."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.main import app

client = TestClient(app)


def test_nav_returns_items():
    r = client.get(
        "/api/v1/nav",
        headers={
            "X-Account-Type": "T2_PUB",
            "X-Build-Role": "publisher",
            "X-License-Keys": "F12",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert len(body["items"]) > 0


def test_admin_overrides_requires_super_header():
    r = client.get(
        "/api/v1/admin/menu-policy/overrides",
        headers={"X-Account-Type": "T1"},
    )
    assert r.status_code == 403


def test_masters_t2_pub_requires_hcode():
    r = client.get(
        "/api/v1/masters/inbound-vendors",
        headers={
            "X-Account-Type": "T2_PUB",
            "X-Build-Role": "publisher",
            "X-License-Keys": "F12",
        },
    )
    assert r.status_code == 400
