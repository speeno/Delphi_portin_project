"""GET /api/v1/nav — 계정 컨텍스트별 메뉴 가시성·disabled (단일 정책 모듈)."""

from __future__ import annotations

from fastapi import APIRouter, Header
from typing import Annotated

from app.core.menu_policy import MenuPolicyContext, build_nav_payload

router = APIRouter()


@router.get("/nav")
async def get_nav(
    x_account_type: Annotated[str | None, Header(alias="X-Account-Type")] = None,
    x_build_role: Annotated[str | None, Header(alias="X-Build-Role")] = None,
    x_warehouse_menu_tier: Annotated[str | None, Header(alias="X-Warehouse-Menu-Tier")] = None,
    x_license_keys: Annotated[str | None, Header(alias="X-License-Keys")] = None,
    x_active_build_id: Annotated[str | None, Header(alias="X-Active-Build-Id")] = None,
    x_super_user: Annotated[str | None, Header(alias="X-Super-User")] = None,
    section: str | None = None,
):
    """
    프로토타입: 헤더로 JWT 클레임을 모사. X-License-Keys 는 쉼표 구분 F11,F12,...
    """
    lic_set: frozenset[str] = frozenset()
    if x_license_keys:
        lic_set = frozenset(k.strip() for k in x_license_keys.split(",") if k.strip())

    ctx = MenuPolicyContext(
        account_type=(x_account_type or "").strip() or None,
        build_role=(x_build_role or "").strip() or None,
        warehouse_menu_tier=(x_warehouse_menu_tier or "").strip() or None,
        license_keys=lic_set,
        is_super_user=(x_super_user or "").strip().lower() in ("1", "true", "yes"),
        active_build_id=(x_active_build_id or "").strip() or None,
    )
    return build_nav_payload(ctx, section=section)
