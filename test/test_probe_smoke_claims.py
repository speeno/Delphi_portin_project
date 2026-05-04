"""DEC-062 — probe 스모크 클레임이 슈퍼유저 규칙과 일치하는지 정적 검증."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_probe():
    root = Path(__file__).resolve().parents[1]
    path = root / "debug" / "probe_backend_all_servers.py"
    spec = importlib.util.spec_from_file_location("probe_backend_all_servers", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_smoke_jwt_user_super_claims() -> None:
    p = _load_probe()
    u = p._smoke_jwt_user("remote_138", "")
    assert u["permissions"] == ["*"]
    assert u["role"] == "admin"
    assert u["server_id"] == "remote_138"


def test_smoke_full_user_context_super_claims() -> None:
    p = _load_probe()
    c = p._smoke_full_user_context("remote_153", "t1")
    assert c["permissions"] == ["*"]
    assert c["tenant_id"] == "t1"
