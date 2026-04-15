"""
Phase-1 HTTP surface (no live DB): health capabilities, query validation, HTML redirects.

153/154 manual smoke steps: docs/phase1-structure/00-phase1-poc-stage1-checklist.md (S6).
"""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)


def test_health_includes_phase1_sobo_flags():
    r = client.get("/api/health")
    assert r.status_code == 200
    caps = r.json().get("capabilities") or {}
    assert caps.get("sobo12G2Gbun") is True
    assert caps.get("sobo13T1Gbun") is True
    assert caps.get("phase2MastersRead") is True


def test_sobo13_missing_server_id_422():
    r = client.get("/api/sobo13/t1-gbun", params={"hcode": "H1"})
    assert r.status_code == 422


def test_sobo13_optional_hcode_no_422_unknown_server_404():
    """Empty hcode is valid; route still requires a known server profile."""
    r = client.get(
        "/api/sobo13/t1-gbun",
        params={"serverId": "__no_such_server__", "limit": 1},
    )
    assert r.status_code == 404


def test_sobo12_optional_hcode_no_422_unknown_server_404():
    r = client.get(
        "/api/sobo12/g2-gbun",
        params={"serverId": "__no_such_server__", "limit": 1},
    )
    assert r.status_code == 404


def test_redirect_sobo12_sobo13():
    r12 = client.get("/sobo12", follow_redirects=False)
    assert r12.status_code == 307
    assert r12.headers.get("location") == "/sobo12.html"
    r13 = client.get("/sobo13", follow_redirects=False)
    assert r13.status_code == 307
    assert r13.headers.get("location") == "/sobo13.html"
