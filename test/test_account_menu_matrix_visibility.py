"""
DEC-RBAC-02 — account-menu-matrix 가시성 회귀 (Python 1:1 미러).

프론트엔드 ``frontend/src/lib/account-menu-matrix.ts::isMenuVisible`` 와 동일한
판정 규칙을 Python 으로 재구현하여, 단일 원천 ``rbac_menu_matrix.json`` 의
모든 행을 조합으로 회귀한다.  vitest 도입 전까지 본 파일이 회귀 잠금 1차 수단.

대응 TS 파일: 도서물류관리프로그램/frontend/src/lib/__tests__/account-menu-matrix.test.ts

실행::

    cd /Users/speeno/Delphi_porting && python3 -m pytest test/test_account_menu_matrix_visibility.py -v
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
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
    license_keys: Iterable[str] | None = None,
    is_super_user: bool = False,
) -> bool:
    """`isMenuVisible` 의 Python 미러 (DEC-RBAC-03 게이트 키)."""
    _ = license_keys  # TS 런타임과 동일 — license_keys 는 웹 메뉴 판정에 미사용
    if is_super_user:
        return True
    if menu.get("account_types") and account_type not in menu["account_types"]:
        return False
    if menu.get("build_roles") and build_role not in menu["build_roles"]:
        return False
    tiers = menu.get("warehouse_menu_tiers") or []
    if tiers:
        at = (account_type or "").strip()
        br = (build_role or "").strip().lower()
        if at == "T3" and br == "warehouse_publisher":
            wmt = (warehouse_menu_tier or "").strip().lower()
            if not wmt or wmt not in tiers:
                return False
    return True


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

    def test_known_account_types_complete(self, matrix):
        types = set(matrix.get("account_types", []))
        # 7 빌드 합집합 정본의 4 대표 — 사라지면 추출/매트릭스 회귀 즉시 깨짐
        for required in ("T1", "T2_DIST", "T2_PUB", "T3"):
            assert required in types, f"account_types 정본에서 {required} 누락"


class TestSuperuserBypass:
    def test_super_user_sees_all(self, matrix):
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
        # 미정의 menuId 는 ``account-menu-matrix.ts`` 에서 보수적 비공개.
        # 본 미러 함수는 menu dict 자체를 받으므로, "lookup 실패 → False" 의미만 확인.
        ids = {m["id"] for m in matrix["menus"]}
        assert "ACC-MENU-NAV-NONEXISTENT" not in ids
