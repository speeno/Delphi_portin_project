"""
Phase-2 HTTP surface (no live DB): health flag, query validation, redirects.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

import main as main_mod  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)


def test_health_includes_phase2_flag():
    r = client.get("/api/health")
    assert r.status_code == 200
    caps = r.json().get("capabilities") or {}
    assert caps.get("phase2MastersRead") is True


def test_phase2_missing_server_id_422():
    r = client.get("/api/phase2/sobo11/list", params={"limit": 1})
    assert r.status_code == 422


def test_phase2_unknown_server_404():
    r = client.get(
        "/api/phase2/sobo11/list",
        params={"serverId": "__no_such_server__", "limit": 1},
    )
    assert r.status_code == 404
    detail = r.json().get("detail")
    assert isinstance(detail, dict)
    assert detail.get("stage") == "config"
    assert "servers.yaml" in str(detail.get("message", ""))


def test_phase2_unknown_form_404_before_db():
    """Unknown form_id returns 404 without opening MySQL (resolve_form is first in handler path)."""
    fake_profile = {
        "id": "fake-srv",
        "user": "u",
        "password": "",
        "database": "d",
        "charset": "utf8mb4",
    }
    with patch.object(main_mod, "_profile_by_id", return_value=fake_profile):
        r = client.get(
            "/api/phase2/sobo99/list",
            params={"serverId": "fake-srv", "limit": 1},
        )
    assert r.status_code == 404
    detail = r.json().get("detail")
    assert isinstance(detail, dict)
    assert detail.get("stage") == "validation"


def test_redirect_masters_and_phase2():
    rm = client.get("/masters", follow_redirects=False)
    assert rm.status_code == 307
    assert rm.headers.get("location") == "/masters-hub.html"
    rp = client.get("/phase2", follow_redirects=False)
    assert rp.status_code == 307
    assert rp.headers.get("location") == "/masters-hub.html"
