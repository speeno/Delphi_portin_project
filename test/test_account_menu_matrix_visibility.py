"""
DEC-RBAC-02 — account-menu-matrix 가시성 회귀 (Python 1:1 미러).

프론트엔드 ``도서물류관리프로그램/frontend/src/lib/account-menu-matrix.ts::isMenuVisible`` (RBAC 전용) 과
백엔드 ``app.core.menu_policy.is_menu_visible_rbac`` 가 동일 규칙을 쓴다.

실행::

    cd /Users/speeno/Delphi_porting && python3 -m pytest test/test_account_menu_matrix_visibility.py -v
"""

from __future__ import annotations

import json
import importlib.util
import sys
from pathlib import Path
from typing import Iterable

import pytest

ROOT = Path(__file__).resolve().parents[1]
MENU_POLICY_PATH = ROOT / "backend" / "app" / "core" / "menu_policy.py"
spec = importlib.util.spec_from_file_location("prototype_menu_policy_matrix", MENU_POLICY_PATH)
assert spec and spec.loader
menu_policy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = menu_policy
spec.loader.exec_module(menu_policy)

is_menu_visible_rbac = menu_policy.is_menu_visible_rbac

MATRIX_JSON = ROOT / "analysis" / "rbac_menu_matrix.json"


@pytest.fixture(scope="module")
def matrix() -> dict:
    with MATRIX_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def _is_menu_visible(
    menu: dict,
    *,
    account_type: str | None = None,
    build_role: str | None = None,
    warehouse_menu_tier: str | None = None,
    login_profile: str | None = None,
    license_keys: Iterable[str] | None = None,
    is_super_user: bool = False,
) -> bool:
    _ = license_keys
    return is_menu_visible_rbac(
        menu,
        account_type=account_type,
        build_role=build_role,
        warehouse_menu_tier=warehouse_menu_tier,
        login_profile=login_profile,
        is_super_user=is_super_user,
    )


def _pick_build_role_for_account(menu: dict, acct: str) -> str | None:
    roles: list[str] = list(menu.get("build_roles") or [])
    if not roles:
        return None
    if acct == "T2_DIST" and "distributor" in roles:
        return "distributor"
    if acct == "T2_PUB" and "publisher" in roles:
        return "publisher"
    if acct == "T3":
        if "warehouse_publisher" in roles:
            return "warehouse_publisher"
        if "publisher" in roles:
            return "publisher"
    if acct == "T1":
        return roles[0]
    return roles[0]


def _pick_warehouse_tier(menu: dict, acct: str, build_role: str | None) -> str:
    tiers: list[str] = list(menu.get("warehouse_menu_tiers") or [])
    if acct == "T3" and (build_role or "").lower() == "warehouse_publisher" and tiers:
        return tiers[0]
    return ""


class TestMatrixDriftGuards:
    def test_matrix_loads(self, matrix):
        assert matrix["version"]
        assert matrix["menus"], "매트릭스 menus 가 비어있다 — 추출 도구 실패"

    def test_decision_refs_present(self, matrix):
        refs = set(matrix.get("decision_refs", []))
        assert "DEC-RBAC-02" in refs
        assert "DEC-RBAC-04" in refs

    def test_known_account_types_complete(self, matrix):
        types = set(matrix.get("account_types", []))
        for required in ("T1", "T2_DIST", "T2_PUB", "T3"):
            assert required in types, f"account_types 정본에서 {required} 누락"


class TestSuperuserBypass:
    def test_super_user_sees_all_rbac(self, matrix):
        for m in matrix["menus"]:
            assert _is_menu_visible(m, is_super_user=True), (
                f"슈퍼유저 우회 실패: {m['id']}"
            )


class TestAccountTypeAxisRegression:
    """4 대표 계정 유형 × 모든 menus — account_type 축만 회귀."""

    @pytest.mark.parametrize("acct", ["T1", "T2_DIST", "T2_PUB", "T3"])
    def test_per_account_type(self, matrix, acct):
        failures = []
        for m in matrix["menus"]:
            br = _pick_build_role_for_account(m, acct)
            wmt = _pick_warehouse_tier(m, acct, br)
            roles = m.get("build_roles") or []
            acc_ok = not m.get("account_types") or acct in m["account_types"]
            br_ok = not roles or (br and br in roles)
            expected = acc_ok and br_ok
            actual = _is_menu_visible(
                m,
                account_type=acct,
                build_role=br,
                warehouse_menu_tier=wmt or None,
            )
            if actual is not expected:
                failures.append((m["id"], expected, actual))
        assert not failures, (
            f"가시성 불일치 ({acct}): {failures[:5]}"
        )


class TestUndefinedMenuClosed:
    def test_unknown_menu_id_false(self, matrix):
        ids = {m["id"] for m in matrix["menus"]}
        assert "ACC-MENU-NAV-NONEXISTENT" not in ids


class TestLoginProfileAllowance:
    def test_department_accounting_profile_opens_nav04(self, matrix):
        nav04 = next(m for m in matrix["menus"] if m["id"] == "ACC-MENU-NAV-04")
        # 기존 RBAC 축만 보면 warehouse_publisher 는 NAV-04 비허용.
        assert not _is_menu_visible(
            nav04,
            account_type="T3",
            build_role="warehouse_publisher",
            warehouse_menu_tier="lite",
        )
        # login_profile 예외는 기존 RBAC 대비 "추가 허용"으로 동작해야 한다.
        assert _is_menu_visible(
            nav04,
            account_type="T3",
            build_role="warehouse_publisher",
            warehouse_menu_tier="lite",
            login_profile="department_accounting",
        )

    def test_pairwise_profile_split_for_same_tenant_shape(self, matrix):
        nav02 = next(m for m in matrix["menus"] if m["id"] == "ACC-MENU-NAV-02")
        nav04 = next(m for m in matrix["menus"] if m["id"] == "ACC-MENU-NAV-04")
        nav09 = next(m for m in matrix["menus"] if m["id"] == "ACC-MENU-NAV-09")

        # same tenant context: T3 + warehouse_publisher + lite
        ctx = {
            "account_type": "T3",
            "build_role": "warehouse_publisher",
            "warehouse_menu_tier": "lite",
        }

        # publisher_main/프로파일 미지정: 기존 RBAC 결과 유지
        assert not _is_menu_visible(nav02, **ctx, login_profile="publisher_main")
        assert not _is_menu_visible(nav04, **ctx, login_profile="publisher_main")
        assert _is_menu_visible(nav09, **ctx, login_profile="publisher_main")
        assert not _is_menu_visible(nav04, **ctx, login_profile=None)

        # department_accounting: NAV-04만 추가 허용
        assert not _is_menu_visible(nav02, **ctx, login_profile="department_accounting")
        assert _is_menu_visible(nav04, **ctx, login_profile="department_accounting")
        assert _is_menu_visible(nav09, **ctx, login_profile="department_accounting")
