"""기초관리 masters 스텁 — ACC-DATA hcode 스코프 의존성."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

from app.core.menu_policy import MenuPolicyContext, http_crud_allowed

router = APIRouter()


def _parse_ctx(
    x_account_type: str | None,
    x_build_role: str | None,
    x_warehouse_menu_tier: str | None,
    x_license_keys: str | None,
    x_super_user: str | None,
) -> MenuPolicyContext:
    lic_set: frozenset[str] = frozenset()
    if x_license_keys:
        lic_set = frozenset(k.strip() for k in x_license_keys.split(",") if k.strip())
    return MenuPolicyContext(
        account_type=(x_account_type or "").strip() or None,
        build_role=(x_build_role or "").strip() or None,
        warehouse_menu_tier=(x_warehouse_menu_tier or "").strip() or None,
        license_keys=lic_set,
        is_super_user=(x_super_user or "").strip().lower() in ("1", "true", "yes"),
        active_build_id=None,
    )


@router.get("/inbound-vendors")
async def list_inbound_vendors(
    x_account_type: Annotated[str | None, Header(alias="X-Account-Type")] = None,
    x_build_role: Annotated[str | None, Header(alias="X-Build-Role")] = None,
    x_warehouse_menu_tier: Annotated[str | None, Header(alias="X-Warehouse-Menu-Tier")] = None,
    x_license_keys: Annotated[str | None, Header(alias="X-License-Keys")] = None,
    x_user_hcode: Annotated[str | None, Header(alias="X-User-Hcode")] = None,
    x_super_user: Annotated[str | None, Header(alias="X-Super-User")] = None,
):
    ctx = _parse_ctx(
        x_account_type,
        x_build_role,
        x_warehouse_menu_tier,
        x_license_keys,
        x_super_user,
    )
    hcode = (x_user_hcode or "").strip() or None
    if ctx.account_type == "T2_PUB" and not hcode:
        raise HTTPException(status_code=400, detail="HCODE_REQUIRED_FOR_T2_PUB")

    ok, mid, reasons = http_crud_allowed("/api/v1/masters/inbound-vendors", "GET", ctx)
    if not ok:
        raise HTTPException(status_code=403, detail={"menu_id": mid, "reasons": reasons})
    return {
        "success": True,
        "scope": {"hcode_filter": hcode},
        "message": "스텁 목록 — M4 시 WHERE hcode 자동 부착",
    }
