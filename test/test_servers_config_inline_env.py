"""BLS_SERVERS_YAML / BLS_SERVERS_YAML_B64 인라인 servers 설정 (Render 무료·Secret File 대안)."""
from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

SAMPLE_YAML = """
auth:
  query: "SELECT gcode AS user_id FROM Id_Logn WHERE gcode = %s"
  password_field: password
servers:
  - id: remote_test
    label: test
    host: 127.0.0.1
    port: 3306
    user: u
    password: p
    database: db
"""


def test_inline_yaml_env(monkeypatch):
    from app.core import config as cfg

    monkeypatch.delenv("BLS_SERVERS_YAML_B64", raising=False)
    monkeypatch.setenv("BLS_SERVERS_YAML", SAMPLE_YAML)
    cfg._inline_yaml_cache = None
    cfg._cached_config = None
    data = cfg.load_config(force=True)
    assert len(data["servers"]) == 1
    assert data["servers"][0]["id"] == "remote_test"
    assert "auth" in data


def test_inline_yaml_b64_env(monkeypatch):
    from app.core import config as cfg

    b64 = base64.b64encode(SAMPLE_YAML.encode("utf-8")).decode("ascii")
    monkeypatch.delenv("BLS_SERVERS_YAML", raising=False)
    monkeypatch.setenv("BLS_SERVERS_YAML_B64", b64)
    cfg._inline_yaml_cache = None
    data = cfg.load_config(force=True)
    assert data["servers"][0]["host"] == "127.0.0.1"


def test_inline_takes_priority_over_missing_file(monkeypatch, tmp_path):
    from app.core import config as cfg

    missing = tmp_path / "nope.yaml"
    monkeypatch.setenv("BLS_SERVERS_CONFIG", str(missing))
    monkeypatch.setenv("BLS_SERVERS_YAML", SAMPLE_YAML)
    cfg._inline_yaml_cache = None
    data = cfg.load_config(force=True)
    assert data["servers"][0]["id"] == "remote_test"
