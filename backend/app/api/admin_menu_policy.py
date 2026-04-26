"""T1 전용 메뉴·CRUD 정책 오버레이 API (프로토타입: X-BLS-Super-User 헤더)."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.core.menu_policy import load_overrides, save_overrides

router = APIRouter()


class OverridesBody(BaseModel):
    schema_version: str = "1.0.0"
    rows: list[dict[str, Any]] = Field(default_factory=list)


def _require_super(x_account_type: str | None, x_super: str | None) -> None:
    if (x_super or "").strip() != "1":
        raise HTTPException(status_code=403, detail="SUPER_HEADER_REQUIRED")
    if (x_account_type or "").strip().upper() != "T1":
        raise HTTPException(status_code=403, detail="T1_ONLY")


@router.get("/menu-policy/overrides")
async def get_overrides(
    x_account_type: Annotated[str | None, Header(alias="X-Account-Type")] = None,
    x_bls_super_user: Annotated[str | None, Header(alias="X-BLS-Super-User")] = None,
):
    _require_super(x_account_type, x_bls_super_user)
    return load_overrides()


@router.put("/menu-policy/overrides")
async def put_overrides(
    body: OverridesBody,
    x_account_type: Annotated[str | None, Header(alias="X-Account-Type")] = None,
    x_bls_super_user: Annotated[str | None, Header(alias="X-BLS-Super-User")] = None,
):
    _require_super(x_account_type, x_bls_super_user)
    doc = body.model_dump()
    save_overrides(doc)
    return {"success": True, "row_count": len(doc.get("rows", []))}
