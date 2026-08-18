"""FastAPI nav / admin / masters 스모크 — 허브 `backend/`(프로토타입) 대상."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE_BACKEND = ROOT / "backend"


def _load_prototype_app():
    """허브 `backend/` 프로토타입의 FastAPI app 을 제품 `app` 패키지와 격리해 로드.

    전체 스위트에서는 conftest 가 제품 백엔드(도서물류관리프로그램/backend)를 먼저
    sys.path 에 올리고 앞선 테스트들이 이미 `app.*` 를 import 해 두므로, 단순
    ``from app.main import app`` 은 *제품* app 을 돌려주어 `/api/v1/nav` 가 404
    (나머지는 JWT 401) 가 된다 — 격리 실행에서만 통과하던 순서 의존.
    sys.modules 의 ``app*`` 항목을 잠시 비우고 허브 backend 를 우선 경로로 import
    한 뒤 원상 복구해, 이후 테스트가 보는 `app` 패키지는 그대로 제품 것이 되게 한다.
    """
    saved_modules = {
        k: v for k, v in sys.modules.items() if k == "app" or k.startswith("app.")
    }
    for k in saved_modules:
        del sys.modules[k]
    saved_path = list(sys.path)
    sys.path.insert(0, str(PROTOTYPE_BACKEND))
    try:
        importlib.invalidate_caches()
        proto_main = importlib.import_module("app.main")
        proto_app = proto_main.app
    finally:
        sys.path[:] = saved_path
        for k in [k for k in sys.modules if k == "app" or k.startswith("app.")]:
            del sys.modules[k]
        sys.modules.update(saved_modules)
        importlib.invalidate_caches()
    return proto_app


app = _load_prototype_app()

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
