"""DSN-DEC-09 — Gcode lookup 키 (``_이름_`` = 만료 잠금, 별칭 아님)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


@pytest.fixture
def index_svc(tmp_path, monkeypatch):
    target = tmp_path / "login_id_index.json"
    monkeypatch.setenv("BLS_LOGIN_ID_INDEX_PATH", str(target))
    monkeypatch.setenv("BLS_LOGIN_INDEX_REFRESH_MIN_INTERVAL_SECS", "1")
    svc = importlib.import_module("app.services.login_id_index_service")
    importlib.reload(svc)
    svc.reset_refresh_state_for_tests()
    svc.reload()
    return svc


def test_login_id_lookup_keys_plain_exact_only(index_svc):
    """평문 입력 시 ``_이름_`` 잠금 Gcode 로 확장하지 않는다."""
    assert index_svc.login_id_lookup_keys("책만드는토우") == ["책만드는토우"]
    assert index_svc.login_id_lookup_keys("미래가치") == ["미래가치"]


def test_login_id_lookup_keys_wrapped_exact_only(index_svc):
    """``_이름_`` 입력 시 평문 ``이름`` 으로 역매핑하지 않는다."""
    assert index_svc.login_id_lookup_keys("_미래가치_") == ["_미래가치_"]
    assert index_svc.login_id_lookup_keys("_책만드는토우_") == ["_책만드는토우_"]
