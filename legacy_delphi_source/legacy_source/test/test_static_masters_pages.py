"""
Static HTML for masters hub POC: served by FastAPI StaticFiles (no live DB).
"""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)


def _assert_html_200(path: str) -> None:
    r = client.get(path)
    assert r.status_code == 200, (path, r.status_code, r.text[:200])
    ct = (r.headers.get("content-type") or "").lower()
    assert "text/html" in ct, (path, ct)


def test_masters_hub_and_children_static_html():
    _assert_html_200("/masters-hub.html")
    _assert_html_200("/masters-read.html")
    _assert_html_200("/masters-read.html?id=sobo17")
    _assert_html_200("/stub-sobo10.html")
    _assert_html_200("/stub-sobo19.html")
    _assert_html_200("/sobo12.html")
    _assert_html_200("/sobo13.html")


def test_masters_extensionless_redirects():
    r = client.get("/masters-hub", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers.get("location") == "/masters-hub.html"

    r2 = client.get("/masters-read", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers.get("location") == "/masters-read.html"

    r3 = client.get("/masters-read?id=sobo14", follow_redirects=False)
    assert r3.status_code == 307
    assert r3.headers.get("location") == "/masters-read.html?id=sobo14"

    s10 = client.get("/stub-sobo10", follow_redirects=False)
    assert s10.status_code == 307
    assert s10.headers.get("location") == "/stub-sobo10.html"

    s19 = client.get("/stub-sobo19", follow_redirects=False)
    assert s19.status_code == 307
    assert s19.headers.get("location") == "/stub-sobo19.html"
