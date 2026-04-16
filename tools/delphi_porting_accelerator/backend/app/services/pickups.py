from __future__ import annotations

from fastapi import HTTPException

from app.repositories.pickups import PickupRepository
from app.schemas.pickups import PickupCreate, PickupListResponse, PickupRecord, PickupUpdate


class PickupService:
    def __init__(self, repository: PickupRepository) -> None:
        self.repository = repository

    def list(self, gdate: str | None = None, publisher: str | None = None, customer: str | None = None) -> PickupListResponse:
        items = self.repository.list(gdate=gdate, publisher=publisher, customer=customer)
        return PickupListResponse(
            items=items,
            count=len(items),
            sum_gqut1=sum(item.gqut1 for item in items),
            sum_gqut2=sum(item.gqut2 for item in items),
        )

    def get(self, record_id: int) -> PickupRecord:
        record = self.repository.get(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail='Record not found')
        return record

    def create(self, payload: PickupCreate) -> PickupRecord:
        return self.repository.create(payload)

    def update(self, record_id: int, payload: PickupUpdate) -> PickupRecord:
        record = self.repository.update(record_id, payload)
        if record is None:
            raise HTTPException(status_code=404, detail='Record not found')
        return record

    def delete(self, record_id: int) -> None:
        if not self.repository.delete(record_id):
            raise HTTPException(status_code=404, detail='Record not found')
