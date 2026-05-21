"""대표 계정 라우팅 일괄 검증 스크립트 회귀 가드 (DSN-DEC-12).

[`debug/verify_login_routing_matrix.py`](../debug/verify_login_routing_matrix.py)
의 hint 정규화·skip 정책·mismatch 비교 로직을 단위 테스트한다.

라이브 백엔드 모듈은 mock 으로 대체해 read-only 환경에서도 회귀를 잡는다.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "debug" / "verify_login_routing_matrix.py"


_INJECTED_MODULES = (
    "app",
    "app.services",
    "app.services.tenants_directory_service",
    "verify_login_routing_matrix",
)


def _install_fake_backend(
    *,
    route: dict | None,
    ownership: tuple[str, dict | None, list[dict]] = ("unique", {}, [{}]),
) -> None:
    """`app.services.tenants_directory_service` 를 mock 으로 주입."""
    pkg_app = types.ModuleType("app")
    pkg_services = types.ModuleType("app.services")
    mod_tds = types.ModuleType("app.services.tenants_directory_service")

    def _resolve_login_route(*, user_id, hcode=None, tenant_id=None, account_family=None):
        return route

    def _resolve_unique_tenant(server_id, db_name, *, hcode=None, tenant_id_hint=None, account_family_hint=None):
        return ownership

    mod_tds.resolve_login_route = _resolve_login_route
    mod_tds.resolve_unique_tenant = _resolve_unique_tenant
    sys.modules["app"] = pkg_app
    sys.modules["app.services"] = pkg_services
    sys.modules["app.services.tenants_directory_service"] = mod_tds


def _cleanup_injected_modules() -> None:
    """본 모듈의 fake 주입은 다음 테스트 모듈(``app.main`` 등 실제 앱) 에 누수되면
    ``ModuleNotFoundError`` 를 일으킨다 — 매 테스트 종료 시 제거."""
    for name in _INJECTED_MODULES:
        sys.modules.pop(name, None)


def _load_script() -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(
        "verify_login_routing_matrix", SCRIPT_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verify_login_routing_matrix"] = mod
    spec.loader.exec_module(mod)
    return mod


class HintFilledTests(TestCase):
    def setUp(self):
        _install_fake_backend(route=None)
        self.mod = _load_script()

    def tearDown(self):
        _cleanup_injected_modules()

    def test_placeholder_hints_treated_as_unfilled(self):
        for v in ("<운영자_입력>", "  <위러브1_hcode>  ", ""):
            self.assertFalse(self.mod._hint_filled(v), v)

    def test_real_hints_are_filled(self):
        self.assertTrue(self.mod._hint_filled("welove01"))
        self.assertTrue(self.mod._hint_filled("0001"))


class RunOneTests(TestCase):
    def tearDown(self):
        _cleanup_injected_modules()

    def test_skipped_when_login_id_hint_missing(self):
        _install_fake_backend(route=None)
        mod = _load_script()
        sample = {"case": "A1", "label": "x", "login_id_hint": "<운영자_입력>"}
        r = mod._run_one(sample)
        self.assertTrue(r["skipped"])
        self.assertEqual(r["case"], "A1")
        self.assertEqual(r["mismatches"], [])

    def test_no_mismatch_when_route_matches(self):
        route = {
            "remote_id": "remote_153",
            "db_name": "chul_05_db",
            "account_family": "chul_05",
            "tenant_id": "TID-X",
            "via": "tenant_id",
        }
        _install_fake_backend(
            route=route, ownership=("unique", route, [route])
        )
        mod = _load_script()
        sample = {
            "case": "A1",
            "label": "중앙라인",
            "login_id_hint": "operator-id-1",
            "expected": {
                "remote_id": "remote_153",
                "db_name": "chul_05_db",
                "account_family": "chul_05",
                "ownership_status": "unique",
            },
        }
        r = mod._run_one(sample)
        self.assertFalse(r.get("skipped"))
        self.assertNotIn("error", r)
        self.assertEqual(r["mismatches"], [])
        self.assertEqual(r["actual"]["ownership_status"], "unique")

    def test_shared_db_ambiguous_without_hcode(self):
        route = {
            "remote_id": "remote_153",
            "db_name": "chul_09_db",
            "account_family": "chul_09",
            "tenant_id": None,
            "via": "account_family",
        }
        _install_fake_backend(
            route=route, ownership=("ambiguous", None, [{}, {}])
        )
        mod = _load_script()
        sample = {
            "case": "B3",
            "label": "위러브3",
            "login_id_hint": "user-x",
            "expected": {
                "remote_id": "remote_153",
                "db_name": "chul_09_db",
                "account_family": "chul_09",
                "ownership_status_with_hcode": "unique",
                "ownership_status_without_hcode": "ambiguous",
            },
        }
        r = mod._run_one(sample)
        self.assertEqual(r["mismatches"], [])
        self.assertEqual(r["actual"]["ownership_status"], "ambiguous")

    def test_mismatch_emitted_when_route_diverges(self):
        route = {
            "remote_id": "remote_138",  # 잘못된 라우팅
            "db_name": "chul_05_db",
            "account_family": "chul_05",
            "tenant_id": "TID-X",
            "via": "fallback_auth_server",
        }
        _install_fake_backend(
            route=route, ownership=("unique", route, [route])
        )
        mod = _load_script()
        sample = {
            "case": "A1",
            "label": "중앙라인",
            "login_id_hint": "operator-id-1",
            "expected": {"remote_id": "remote_153", "db_name": "chul_05_db"},
        }
        r = mod._run_one(sample)
        fields = [m["field"] for m in r["mismatches"]]
        self.assertIn("remote_id", fields)
        self.assertNotIn("db_name", fields)


if __name__ == "__main__":
    main()
