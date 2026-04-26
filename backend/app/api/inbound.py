"""
입고 API (prototype)

Migration Contracts:
- api.inbound.list (GET /api/inbound)
- api.inbound.create (POST /api/inbound)
- api.inbound.update (PUT /api/inbound/{id})
- api.inbound.delete (DELETE /api/inbound/{id})

레거시 필드 매핑 (DEC-RBAC-01 / SCH-WELOVE-출판):
    - item_code     ← G4_Book.gcode (도서코드)
    - supplier_code ← G1_Ggeo.gcode (거래처 코드, 입고처)
    - customer_code ← G1_Ggeo.gcode (배본처/주문 거래처)
    - warehouse_code= tenants_directory.primary_server

권장 포팅 순서: 1차(조회) → 2차(등록) → 3차(수정/삭제)
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class InboundItem(BaseModel):
    """입고 라인. ``item_code`` = ``G4_Book.gcode`` (도서코드)."""

    item_code: str
    item_name: str = ""
    qty: int
    location: str = ""
    lot_no: str = ""
    remark: str = ""


class InboundCreateRequest(BaseModel):
    """입고 등록 요청. ``supplier_code`` / ``customer_code`` 모두 ``G1_Ggeo.gcode`` 체계."""

    warehouse_code: str
    supplier_code: str = ""
    items: list[InboundItem]
    customer_code: str = ""


class InboundResponse(BaseModel):
    success: bool
    message: str
    data: dict = {}


@router.get("")
async def list_inbounds(
    warehouse_code: str = Query(""),
    date_from: str = Query(""),
    date_to: str = Query(""),
    status: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """입고 목록 조회 (1차 - 읽기 전용)"""
    # TODO: Legacy DB 조회 구현
    # 가드레일: 기존 컬럼명 유지, SELECT 전용
    return {
        "success": True,
        "data": {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
        },
    }


@router.get("/{inbound_id}")
async def get_inbound(inbound_id: int):
    """입고 상세 조회 (1차 - 읽기 전용)"""
    # TODO: Legacy DB 조회 구현
    return {"success": True, "data": {}}


@router.post("", response_model=InboundResponse)
async def create_inbound(req: InboundCreateRequest):
    """
    입고 등록 (2차 - 신규 등록)

    Validation Rules (Legacy 동작 보존):
    1. item_code 필수
    2. qty > 0
    3. warehouse_code 필수
    Customer Variants:
    - customer_a: lot_no 필수
    - customer_b: location 자동 할당

    Side Effects:
    - INSERT tb_inbound
    - UPDATE tb_stock (qty 증가)
    - INSERT tb_audit
    """
    # Validation (가드레일: 기존 검증 순서 보존)
    if not req.warehouse_code:
        return InboundResponse(success=False, message="창고코드를 입력해 주세요.")

    for item in req.items:
        if not item.item_code:
            return InboundResponse(success=False, message="상품코드를 입력해 주세요.")
        if item.qty <= 0:
            return InboundResponse(success=False, message="수량은 0보다 커야 합니다.")

    # Customer Variant 처리 (가드레일: 고객사 분기 삭제 금지)
    if req.customer_code == "customer_a":
        for item in req.items:
            if not item.lot_no:
                return InboundResponse(success=False, message="LOT 번호를 입력해 주세요. (고객사 A 필수)")

    # TODO: 실제 DB INSERT 구현
    # 트랜잭션: BEGIN → INSERT tb_inbound → UPDATE tb_stock → INSERT tb_audit → COMMIT
    # 가드레일: 기존 트랜잭션 경계 변경 금지

    return InboundResponse(
        success=True,
        message="입고가 등록되었습니다.",
        data={"inbound_id": 0, "created_at": datetime.now().isoformat()},
    )


@router.put("/{inbound_id}", response_model=InboundResponse)
async def update_inbound(inbound_id: int, req: InboundCreateRequest):
    """입고 수정 (3차 - UPDATE 발생, 트랜잭션 경계 검증 필수)"""
    # TODO: Legacy DB UPDATE 구현
    # 가드레일: 기존 트랜잭션 경계 보존
    return InboundResponse(success=True, message="입고가 수정되었습니다.", data={"inbound_id": inbound_id})


@router.delete("/{inbound_id}", response_model=InboundResponse)
async def delete_inbound(inbound_id: int):
    """입고 삭제/취소 (3차 - DELETE 발생, 트랜잭션 경계 검증 필수)"""
    # TODO: Legacy DB DELETE/취소 구현
    return InboundResponse(success=True, message="입고가 취소되었습니다.", data={"inbound_id": inbound_id})
