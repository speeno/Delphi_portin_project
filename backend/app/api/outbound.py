"""
출고 API

Migration Contracts:
- api.outbound.list (GET /api/outbound)
- api.outbound.create (POST /api/outbound)
- api.outbound.update (PUT /api/outbound/{id})
- api.outbound.delete (DELETE /api/outbound/{id})
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class OutboundItem(BaseModel):
    item_code: str
    item_name: str = ""
    qty: int
    location: str = ""
    lot_no: str = ""


class OutboundCreateRequest(BaseModel):
    warehouse_code: str
    customer_code: str = ""
    order_no: str = ""
    items: list[OutboundItem]


class OutboundResponse(BaseModel):
    success: bool
    message: str
    data: dict = {}


@router.get("")
async def list_outbounds(
    warehouse_code: str = Query(""),
    date_from: str = Query(""),
    date_to: str = Query(""),
    status: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """출고 목록 조회"""
    # TODO: Legacy DB 조회 구현
    return {
        "success": True,
        "data": {"items": [], "total": 0, "page": page, "page_size": page_size},
    }


@router.post("", response_model=OutboundResponse)
async def create_outbound(req: OutboundCreateRequest):
    """출고 등록"""
    if not req.warehouse_code:
        return OutboundResponse(success=False, message="창고코드를 입력해 주세요.")

    for item in req.items:
        if not item.item_code:
            return OutboundResponse(success=False, message="상품코드를 입력해 주세요.")
        if item.qty <= 0:
            return OutboundResponse(success=False, message="수량은 0보다 커야 합니다.")

    # TODO: 재고 차감 검증 (가용 재고 >= 출고 수량)
    # TODO: 트랜잭션: BEGIN → INSERT tb_outbound → UPDATE tb_stock (qty 감소) → INSERT tb_audit → COMMIT

    return OutboundResponse(
        success=True,
        message="출고가 등록되었습니다.",
        data={"outbound_id": 0, "created_at": datetime.now().isoformat()},
    )


@router.put("/{outbound_id}", response_model=OutboundResponse)
async def update_outbound(outbound_id: int, req: OutboundCreateRequest):
    """출고 수정"""
    # TODO: Legacy DB UPDATE 구현
    return OutboundResponse(success=True, message="출고가 수정되었습니다.", data={"outbound_id": outbound_id})


@router.delete("/{outbound_id}", response_model=OutboundResponse)
async def delete_outbound(outbound_id: int):
    """출고 삭제/취소"""
    # TODO: Legacy DB DELETE/취소 구현
    return OutboundResponse(success=True, message="출고가 취소되었습니다.", data={"outbound_id": outbound_id})
