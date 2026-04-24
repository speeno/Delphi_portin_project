"""
재고 API (prototype)

Migration Contracts:
- api.inventory.list (GET /api/inventory)
- api.inventory.adjust (POST /api/inventory/adjust)

레거시 필드 매핑 (DEC-RBAC-01 / SCH-WELOVE-출판):
    - item_code     ← G4_Book.gcode (도서코드)
    - customer_code ← G1_Ggeo.gcode (거래처 코드)
    - warehouse_code= tenants_directory.primary_server
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


class InventoryAdjustRequest(BaseModel):
    """재고 조정 요청. ``item_code`` = ``G4_Book.gcode``, ``customer_code`` = ``G1_Ggeo.gcode``."""

    warehouse_code: str
    item_code: str
    adjust_qty: int
    reason: str = ""
    customer_code: str = ""


class InventoryResponse(BaseModel):
    success: bool
    message: str
    data: dict = {}


@router.get("")
async def list_inventory(
    warehouse_code: str = Query(""),
    item_code: str = Query(""),
    location: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """재고 조회 (1차 - 읽기 전용)"""
    # TODO: Legacy DB 조회 구현
    return {
        "success": True,
        "data": {"items": [], "total": 0, "page": page, "page_size": page_size},
    }


@router.post("/adjust", response_model=InventoryResponse)
async def adjust_inventory(req: InventoryAdjustRequest):
    """재고 조정 (3차 - UPDATE, 트랜잭션 경계 검증 필수)"""
    if not req.warehouse_code:
        return InventoryResponse(success=False, message="창고코드를 입력해 주세요.")
    if not req.item_code:
        return InventoryResponse(success=False, message="상품코드를 입력해 주세요.")
    if req.adjust_qty == 0:
        return InventoryResponse(success=False, message="조정 수량을 입력해 주세요.")

    # TODO: 트랜잭션: BEGIN → UPDATE tb_stock → INSERT tb_stock_adjust → INSERT tb_audit → COMMIT

    return InventoryResponse(
        success=True,
        message="재고가 조정되었습니다.",
        data={"item_code": req.item_code, "adjust_qty": req.adjust_qty},
    )
