from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.repositories.pickups import PickupRepository
from app.schemas.pickups import PickupCreate, PickupListResponse, PickupRecord, PickupUpdate
from app.services.pickups import PickupService


router = APIRouter(prefix='/api/pickups', tags=['pickups'])
service = PickupService(PickupRepository())


@router.get('', response_model=PickupListResponse)
def list_pickups(
    gdate: str | None = Query(default=None),
    publisher: str | None = Query(default=None),
    customer: str | None = Query(default=None),
) -> PickupListResponse:
    return service.list(gdate=gdate, publisher=publisher, customer=customer)


@router.get('/{record_id}', response_model=PickupRecord)
def get_pickup(record_id: int) -> PickupRecord:
    return service.get(record_id)


@router.post('', response_model=PickupRecord, status_code=status.HTTP_201_CREATED)
def create_pickup(payload: PickupCreate) -> PickupRecord:
    return service.create(payload)


@router.put('/{record_id}', response_model=PickupRecord)
def update_pickup(record_id: int, payload: PickupUpdate) -> PickupRecord:
    return service.update(record_id, payload)


@router.delete('/{record_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_pickup(record_id: int) -> Response:
    service.delete(record_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
