"""MENUVIS-DEC-07 — show-first 네비 + 사용자별 hidden_menu_ids 회귀.

검증 포인트:
- 미매핑(account_type 빈) 계정에서도 기초관리 3 화면(MASTERS-02/03/06) 노출.
- 사용자별 hidden_menu_ids 가 해당 메뉴만 사이드바에서 숨김(user_hidden).
- forced_hidden / 오버레이 deny 는 여전히 숨김.
- user_menu_visibility_service 4-key 저장/조회/삭제 + 동일 hcode·다른 gcode 분리.

실행::

    cd /Users/speeno/Delphi_porting && python3 -m pytest test/test_menu_visibility_show_first.py -v
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MENU_POLICY_PATH = ROOT / "backend" / "app" / "core" / "menu_policy.py"
spec = importlib.util.spec_from_file_location("prototype_menu_policy_showfirst", MENU_POLICY_PATH)
assert spec and spec.loader
menu_policy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = menu_policy
spec.loader.exec_module(menu_policy)

MenuPolicyContext = menu_policy.MenuPolicyContext
nav_ui_state_for_menu = menu_policy.nav_ui_state_for_menu
menu_by_id = menu_policy.menu_by_id

TARGET_MENUS = ["ACC-MENU-MASTERS-02", "ACC-MENU-MASTERS-03", "ACC-MENU-MASTERS-06"]


@pytest.mark.parametrize("account_type", [None, "", "T1", "T2_DIST", "T2_PUB", "T3"])
@pytest.mark.parametrize("menu_id", TARGET_MENUS)
def test_target_menus_visible_for_any_account(account_type, menu_id):
    """입고처/기타거래처/저자 — 미매핑 포함 모든 계정에서 노출."""
    m = menu_by_id(menu_id)
    assert m is not None, f"{menu_id} 가 매트릭스에 없다"
    ctx = MenuPolicyContext(
        account_type=account_type or None,
        license_keys=frozenset(),
        is_super_user=False,
    )
    ui = nav_ui_state_for_menu(m, ctx)
    assert ui.visible, f"{menu_id} 가 {account_type!r} 에서 숨겨짐 — show-first 위반"


def test_unmapped_account_sees_full_sidebar():
    """account_type 빈 계정도 전 메뉴 노출(과거엔 사이드바 0건)."""
    ctx = MenuPolicyContext(account_type=None, license_keys=frozenset(), is_super_user=False)
    hidden = [
        m["id"]
        for m in menu_policy._cached_matrix()["menus"]
        if not nav_ui_state_for_menu(m, ctx).visible
    ]
    assert hidden == [], f"미매핑 계정에서 숨겨진 메뉴: {hidden[:5]}"


def test_user_hidden_menu_ids_hides_only_that_menu():
    ctx = MenuPolicyContext(
        account_type="T1",
        license_keys=frozenset(),
        is_super_user=False,
        hidden_menu_ids=frozenset({"ACC-MENU-MASTERS-02"}),
    )
    hidden_ui = nav_ui_state_for_menu(menu_by_id("ACC-MENU-MASTERS-02"), ctx)
    assert not hidden_ui.visible
    assert "user_hidden" in hidden_ui.reasons
    # 같은 컨텍스트에서 다른 메뉴는 영향 없음.
    other_ui = nav_ui_state_for_menu(menu_by_id("ACC-MENU-MASTERS-03"), ctx)
    assert other_ui.visible


def test_super_user_ignores_hidden_menu_ids():
    ctx = MenuPolicyContext(
        is_super_user=True,
        hidden_menu_ids=frozenset({"ACC-MENU-MASTERS-02"}),
    )
    ui = nav_ui_state_for_menu(menu_by_id("ACC-MENU-MASTERS-02"), ctx)
    assert ui.visible and not ui.disabled


def test_forced_hidden_still_hides_under_show_first():
    m = menu_by_id("ACC-MENU-NAV-10")
    ctx = MenuPolicyContext(
        account_type="T2_DIST",
        build_role="distributor",
        license_keys=frozenset(),
        is_super_user=False,
        active_build_id="BLD-PUB-WAREHOUSE-MS",
    )
    ui = nav_ui_state_for_menu(m, ctx)
    assert not ui.visible
    assert "build_forced_hidden" in ui.reasons


def test_override_deny_still_hides_under_show_first():
    m = menu_by_id("ACC-MENU-NAV-01")
    ovr = {"rows": [{"account_type": "T2_PUB", "menu_id": "ACC-MENU-NAV-01", "visibility": "deny"}]}
    ctx = MenuPolicyContext(account_type="T2_PUB", license_keys=frozenset(), is_super_user=False)
    ui = nav_ui_state_for_menu(m, ctx, overrides=ovr)
    assert not ui.visible
    assert "override_deny" in ui.reasons


# ── user_menu_visibility_service 4-key 저장소 (admin 영속) ──


@pytest.fixture()
def svc(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
    monkeypatch.setenv("BLS_USER_MENU_VISIBILITY_PATH", str(tmp_path / "umv.json"))
    import importlib

    import app.services.user_menu_visibility_service as mod

    importlib.reload(mod)
    return mod


def test_service_4key_set_get_and_clear(svc):
    out = svc.set_hidden_menu_ids(
        server_id="remote_153", hcode="5019", gcode="gyomunsa", gname="교문사",
        hidden_menu_ids=["ACC-MENU-MASTERS-02"], actor="admin",
    )
    assert out["hidden_menu_ids"] == ["ACC-MENU-MASTERS-02"]
    assert svc.get_hidden_menu_ids(server_id="remote_153", hcode="5019", gcode="gyomunsa") == [
        "ACC-MENU-MASTERS-02"
    ]
    # 빈 목록 → 행 제거(전체 노출 복귀)
    svc.set_hidden_menu_ids(
        server_id="remote_153", hcode="5019", gcode="gyomunsa", hidden_menu_ids=[], actor="admin"
    )
    assert svc.get_hidden_menu_ids(server_id="remote_153", hcode="5019", gcode="gyomunsa") == []


def test_service_same_hcode_distinct_gcode(svc):
    """동일 hcode·다른 gcode 계정은 서로 다른 감춤 설정을 가진다 (account-menu-fidelity 5019 분리)."""
    svc.set_hidden_menu_ids(
        server_id="remote_153", hcode="5019", gcode="gyomunsa",
        hidden_menu_ids=["ACC-MENU-MASTERS-02"], actor="admin",
    )
    svc.set_hidden_menu_ids(
        server_id="remote_153", hcode="5019", gcode="accounting",
        hidden_menu_ids=["ACC-MENU-NAV-04"], actor="admin",
    )
    assert svc.get_hidden_menu_ids(server_id="remote_153", hcode="5019", gcode="gyomunsa") == [
        "ACC-MENU-MASTERS-02"
    ]
    assert svc.get_hidden_menu_ids(server_id="remote_153", hcode="5019", gcode="accounting") == [
        "ACC-MENU-NAV-04"
    ]


def test_service_rejects_bad_menu_id(svc):
    with pytest.raises(ValueError):
        svc.set_hidden_menu_ids(
            server_id="r", hcode="h", gcode="g", hidden_menu_ids=["not-a-menu"], actor="admin"
        )
