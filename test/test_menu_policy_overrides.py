"""menu_policy — 강제 숨김, 라이선스 UI, CRUD, 수퍼 오버레이 회귀."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.menu_policy import (
    MenuPolicyContext,
    crud_allowed_for_menu_action,
    effective_menu_visible,
    http_crud_allowed,
    nav_ui_state_for_menu,
    menu_by_id,
)

MATRIX = ROOT / "analysis" / "rbac_menu_matrix.json"


@pytest.fixture(scope="module")
def masters_02():
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    for m in data["menus"]:
        if m["id"] == "ACC-MENU-MASTERS-02":
            return m
    raise RuntimeError("ACC-MENU-MASTERS-02 missing")


def test_forced_hidden_hides_nav_item():
    m = menu_by_id("ACC-MENU-NAV-10")
    assert m
    ctx = MenuPolicyContext(
        account_type="T2_DIST",
        build_role="distributor",
        warehouse_menu_tier=None,
        license_keys=frozenset(),
        is_super_user=False,
        active_build_id="BLD-PUB-WAREHOUSE-MS",
    )
    assert not effective_menu_visible(m, ctx)
    ui = nav_ui_state_for_menu(m, ctx)
    assert not ui.visible
    assert "build_forced_hidden" in ui.reasons


def test_license_missing_disabled_not_hidden(masters_02):
    ctx = MenuPolicyContext(
        account_type="T1",
        build_role="distributor",
        warehouse_menu_tier=None,
        license_keys=frozenset(),
        is_super_user=False,
        active_build_id=None,
    )
    ui = nav_ui_state_for_menu(masters_02, ctx)
    assert ui.visible
    assert ui.disabled
    assert "license_keys_missing" in ui.reasons


def test_crud_read_denied_without_f12_license():
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        warehouse_menu_tier=None,
        license_keys=frozenset(),
        is_super_user=False,
    )
    ok, reasons = crud_allowed_for_menu_action(
        "ACC-MENU-MASTERS-02", "read", ctx
    )
    assert not ok
    assert "menu_license_keys_missing" in reasons


def test_crud_read_ok_with_f12():
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        warehouse_menu_tier=None,
        license_keys=frozenset(["F12"]),
        is_super_user=False,
    )
    ok, _ = crud_allowed_for_menu_action("ACC-MENU-MASTERS-02", "read", ctx)
    assert ok


def test_http_crud_mapping():
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        license_keys=frozenset(["F12"]),
        is_super_user=False,
    )
    ok, mid, _ = http_crud_allowed("/api/v1/masters/inbound-vendors", "GET", ctx)
    assert ok and mid == "ACC-MENU-MASTERS-02"


def test_visibility_override_deny():
    m = menu_by_id("ACC-MENU-NAV-01")
    ovr = {
        "rows": [
            {
                "account_type": "T2_PUB",
                "menu_id": "ACC-MENU-NAV-01",
                "visibility": "deny",
                "crud": {},
            }
        ]
    }
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        license_keys=frozenset(),
        is_super_user=False,
    )
    assert not effective_menu_visible(m, ctx, overrides=ovr)


def test_fxx_template_x_denies_t2_pub_special():
    """T2_PUB 베이스에서 F18=X 인 특별관리(MASTERS-11)."""
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        license_keys=frozenset(["F18"]),
        is_super_user=False,
    )
    ok, reasons = crud_allowed_for_menu_action(
        "ACC-MENU-MASTERS-11", "read", ctx
    )
    assert not ok
    assert "fxx_template_denied" in reasons


def test_crud_override_deny_read():
    ctx = MenuPolicyContext(
        account_type="T2_PUB",
        build_role="publisher",
        license_keys=frozenset(["F12"]),
        is_super_user=False,
    )
    ovr = {
        "rows": [
            {
                "account_type": "T2_PUB",
                "menu_id": "ACC-MENU-MASTERS-02",
                "visibility": "inherit",
                "crud": {"read": "deny", "create": "inherit", "update": "inherit", "delete": "inherit"},
            }
        ]
    }
    ok, reasons = crud_allowed_for_menu_action(
        "ACC-MENU-MASTERS-02", "read", ctx, overrides=ovr
    )
    assert not ok
    assert "crud_override_deny" in reasons
