"""
계정유형·메뉴 가시성 + 라이선스 UI(MENUVIS-DEC-06) + Fxx CRUD 베이스 + 수퍼 오버레이.

단일 진입점: nav API·프론트 미러·pytest 가 동일 규칙을 쓰도록 한다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import yaml

# backend/app/core/menu_policy.py → repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MATRIX_PATH = REPO_ROOT / "analysis" / "rbac_menu_matrix.json"
FORCED_PATH = REPO_ROOT / "migration" / "contracts" / "build_forced_hidden_menus.yaml"
CRUD_MAP_PATH = REPO_ROOT / "migration" / "contracts" / "menu_route_crud_map.yaml"
DEFAULT_ID_LOGN_PATH = REPO_ROOT / "migration" / "contracts" / "default_id_logn_permissions.yaml"
OVERRIDES_PATH = REPO_ROOT / "backend" / "data" / "menu_policy_overrides.json"


@dataclass
class NavUiState:
    """네비 항목 UI — MENUVIS-DEC-06: 라이선스 부족 시 보이되 disabled."""

    visible: bool
    disabled: bool
    reasons: list[str] = field(default_factory=list)


@dataclass
class MenuPolicyContext:
    account_type: str | None = None
    build_role: str | None = None
    warehouse_menu_tier: str | None = None
    license_keys: frozenset[str] | None = None
    is_super_user: bool = False
    active_build_id: str | None = None


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _cached_matrix() -> dict[str, Any]:
    return _load_json(MATRIX_PATH)


@lru_cache(maxsize=1)
def _cached_forced() -> dict[str, Any]:
    if not FORCED_PATH.exists():
        return {}
    return yaml.safe_load(FORCED_PATH.read_text(encoding="utf-8")) or {}


@lru_cache(maxsize=1)
def _cached_crud_map() -> dict[str, Any]:
    return yaml.safe_load(CRUD_MAP_PATH.read_text(encoding="utf-8")) or {}


@lru_cache(maxsize=1)
def _cached_id_logn() -> dict[str, Any]:
    return yaml.safe_load(DEFAULT_ID_LOGN_PATH.read_text(encoding="utf-8")) or {}


def load_overrides() -> dict[str, Any]:
    if not OVERRIDES_PATH.exists():
        return {"schema_version": "1.0.0", "rows": []}
    return _load_json(OVERRIDES_PATH)


def save_overrides(doc: dict[str, Any]) -> None:
    OVERRIDES_PATH.parent.mkdir(parents=True, exist_ok=True)
    OVERRIDES_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        load_overrides_cached.cache_clear()
    except Exception:
        pass


@lru_cache(maxsize=8)
def load_overrides_cached(_mtime_ns: int) -> dict[str, Any]:
    return load_overrides()


def _overrides_doc() -> dict[str, Any]:
    if not OVERRIDES_PATH.exists():
        return {"schema_version": "1.0.0", "rows": []}
    mtime = OVERRIDES_PATH.stat().st_mtime_ns
    return load_overrides_cached(mtime)


def menu_by_id(menu_id: str) -> dict[str, Any] | None:
    for m in _cached_matrix().get("menus", []):
        if m.get("id") == menu_id:
            return m
    return None


def is_menu_visible_rbac(
    menu: dict[str, Any],
    *,
    account_type: str | None = None,
    build_role: str | None = None,
    warehouse_menu_tier: str | None = None,
    is_super_user: bool = False,
) -> bool:
    """RBAC 축만 (라이선스·forced_hidden·오버레이 제외)."""
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


def _visibility_override(menu_id: str, account_type: str | None, overrides: dict[str, Any]) -> str | None:
    if not account_type:
        return None
    for row in overrides.get("rows", []):
        if row.get("menu_id") == menu_id and row.get("account_type") == account_type:
            v = (row.get("visibility") or "inherit").strip().lower()
            if v in ("allow", "deny"):
                return v
    return None


def is_forced_hidden(menu_id: str, active_build_id: str | None) -> bool:
    if not active_build_id:
        return False
    cfg = _cached_forced()
    b = (cfg.get("builds") or {}).get(active_build_id) or {}
    hidden = set(b.get("forced_hidden_acc_menu_ids") or [])
    return menu_id in hidden


def effective_menu_visible(
    menu: dict[str, Any],
    ctx: MenuPolicyContext,
    *,
    overrides: dict[str, Any] | None = None,
) -> bool:
    """RBAC + forced_hidden + visibility 오버레이 (라이선스 제외)."""
    if ctx.is_super_user:
        return True
    ovr = overrides if overrides is not None else _overrides_doc()
    base = is_menu_visible_rbac(
        menu,
        account_type=ctx.account_type,
        build_role=ctx.build_role,
        warehouse_menu_tier=ctx.warehouse_menu_tier,
        is_super_user=False,
    )
    if is_forced_hidden(menu["id"], ctx.active_build_id):
        return False
    vo = _visibility_override(menu["id"], ctx.account_type, ovr)
    if vo == "deny":
        return False
    # allow 는 베이스가 이미 true 일 때만 의미 있음
    return base


def license_keys_satisfied(menu: dict[str, Any], license_keys: Iterable[str] | None) -> bool:
    required = menu.get("license_keys") or []
    if not required:
        return True
    user = set(license_keys or [])
    return all(k in user for k in required)


def nav_ui_state_for_menu(
    menu: dict[str, Any],
    ctx: MenuPolicyContext,
    *,
    overrides: dict[str, Any] | None = None,
) -> NavUiState:
    """MENUVIS-DEC-06: RBAC+forced 통과 후 라이선스 없으면 visible+disabled."""
    if ctx.is_super_user:
        return NavUiState(True, False, [])
    ovr = overrides if overrides is not None else _overrides_doc()
    if is_forced_hidden(menu["id"], ctx.active_build_id):
        return NavUiState(False, False, ["build_forced_hidden"])
    rbac_ok = effective_menu_visible(menu, ctx, overrides=ovr)
    if not rbac_ok:
        return NavUiState(False, False, ["rbac"])
    lic = license_keys_satisfied(menu, ctx.license_keys)
    if not lic:
        return NavUiState(True, True, ["license_keys_missing"])
    return NavUiState(True, False, [])


def _resolved_fxx_map(account_type: str | None, build_role: str | None) -> dict[str, str]:
    """account_type 템플릿 + warehouse_publisher variant 패치."""
    doc = _cached_id_logn()
    if not account_type:
        return {}
    templates = doc.get("base_templates") or {}
    t = templates.get(account_type)
    if not t:
        return {}
    fxx: dict[str, str] = dict(t.get("fxx_defaults") or {})
    br = (build_role or "").strip().lower()
    for var in doc.get("customer_variants") or []:
        m = var.get("match") or {}
        if m.get("build_role") and br == str(m["build_role"]).strip().lower():
            for k, v in (var.get("fxx_patch") or {}).items():
                fxx[str(k)] = str(v)
    return fxx


def fxx_allows_operations(fxx: str, account_type: str | None, build_role: str | None) -> bool:
    """R 이면 CRUD 전부 허용 베이스, X 이면 전부 거부 (웹 DEC)."""
    m = _resolved_fxx_map(account_type, build_role)
    val = (m.get(fxx) or "X").strip().upper()
    return val != "X"


def _crud_row_override(menu_id: str, account_type: str | None, overrides: dict[str, Any]) -> dict[str, str] | None:
    if not account_type:
        return None
    for row in overrides.get("rows", []):
        if row.get("menu_id") == menu_id and row.get("account_type") == account_type:
            c = row.get("crud")
            if isinstance(c, dict):
                return {k: str(v).strip().lower() for k, v in c.items()}
    return None


def crud_allowed_for_menu_action(
    menu_id: str,
    action: str,
    ctx: MenuPolicyContext,
    *,
    overrides: dict[str, Any] | None = None,
) -> tuple[bool, list[str]]:
    """
    action: create | read | update | delete
    JWT 라이선스·Fxx 템플릿 R/X 베이스 후 수퍼 CRUD 오버레이 적용.
    """
    if ctx.is_super_user:
        return True, []

    ovr = overrides if overrides is not None else _overrides_doc()
    menu = menu_by_id(menu_id)
    if not menu:
        return False, ["unknown_menu"]

    if not effective_menu_visible(menu, ctx, overrides=ovr):
        return False, ["not_visible_rbac_or_forced"]
    if not license_keys_satisfied(menu, ctx.license_keys):
        return False, ["menu_license_keys_missing"]

    cmap = _cached_crud_map()
    row = None
    for mp in cmap.get("mappings") or []:
        if mp.get("menu_id") == menu_id:
            row = mp
            break
    if not row:
        return False, ["no_crud_mapping"]

    fxx_keys: list[str] = list(row.get("fxx_keys") or [])
    for fk in fxx_keys:
        if not license_keys_satisfied({"license_keys": [fk]}, ctx.license_keys):
            return False, ["fxx_license_keys_missing"]
    fxx_all_r = all(
        fxx_allows_operations(fk, ctx.account_type, ctx.build_role) for fk in fxx_keys
    ) if fxx_keys else True

    if not fxx_all_r:
        return False, ["fxx_template_denied"]

    base_crud = True
    crud_ov = _crud_row_override(menu_id, ctx.account_type, ovr) or {}
    tri = (crud_ov.get(action) or "inherit").strip().lower()
    if tri == "deny":
        return False, ["crud_override_deny"]
    if tri == "grant":
        return base_crud, [] if base_crud else ["grant_blocked_by_base"]
    return base_crud, [] if base_crud else ["crud_base_denied"]


def method_to_action(method: str) -> str | None:
    m = method.upper()
    cmap = _cached_crud_map()
    return (cmap.get("method_to_action") or {}).get(m)


def menu_id_for_api_path(path: str) -> str | None:
    path = path.split("?", 1)[0]
    cmap = _cached_crud_map()
    best: tuple[int, str] | None = None
    for mp in cmap.get("mappings") or []:
        prefix = mp.get("api_prefix") or ""
        if path.startswith(prefix):
            ln = len(prefix)
            if best is None or ln > best[0]:
                best = (ln, mp["menu_id"])
    return best[1] if best else None


def http_crud_allowed(
    path: str,
    method: str,
    ctx: MenuPolicyContext,
    *,
    overrides: dict[str, Any] | None = None,
) -> tuple[bool, str | None, list[str]]:
    mid = menu_id_for_api_path(path)
    if not mid:
        return False, None, ["no_menu_for_path"]
    act = method_to_action(method)
    if not act:
        return False, mid, ["unknown_http_method"]
    ok, reasons = crud_allowed_for_menu_action(mid, act, ctx, overrides=overrides)
    return ok, mid, reasons


def build_nav_payload(
    ctx: MenuPolicyContext,
    *,
    section: str | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """GET /api/v1/nav 용 — menus 와 동일 스키마 + ui 상태."""
    ovr = overrides if overrides is not None else _overrides_doc()
    out = []
    for m in _cached_matrix().get("menus", []):
        if section and m.get("section") != section:
            continue
        ui = nav_ui_state_for_menu(m, ctx, overrides=ovr)
        out.append(
            {
                "id": m["id"],
                "section": m.get("section"),
                "route": m.get("route"),
                "caption": m.get("caption"),
                "visible": ui.visible,
                "disabled": ui.disabled,
                "reasons": ui.reasons,
            }
        )
    return {"version": _cached_matrix().get("version"), "items": out}
