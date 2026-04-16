from __future__ import annotations

from copy import deepcopy

from app.schemas.pickups import PickupCreate, PickupRecord, PickupUpdate


class PickupRepository:
    def __init__(self) -> None:
        self._rows: list[PickupRecord] = [
            PickupRecord(id=1, gdate='2026.04.16', hcode='P001', hname='열린책들', gnumb='A-1001', name1='서울', gname='광화문점', name2='박스', gbigo='오전 회수', gqut1=12, gqut2=3),
            PickupRecord(id=2, gdate='2026.04.16', hcode='P002', hname='문학동네', gnumb='A-1002', name1='부산', gname='센텀점', name2='파렛트', gbigo='착불 확인', gqut1=4, gqut2=9),
        ]
        self._next_id = 3

    def list(self, gdate: str | None = None, publisher: str | None = None, customer: str | None = None) -> list[PickupRecord]:
        rows = self._rows
        if gdate:
            rows = [row for row in rows if row.gdate == gdate]
        if publisher:
            query = publisher.lower()
            rows = [row for row in rows if query in row.hname.lower() or query in row.hcode.lower()]
        if customer:
            query = customer.lower()
            rows = [row for row in rows if query in row.gname.lower()]
        return deepcopy(rows)

    def get(self, record_id: int) -> PickupRecord | None:
        for row in self._rows:
            if row.id == record_id:
                return deepcopy(row)
        return None

    def create(self, payload: PickupCreate) -> PickupRecord:
        row = PickupRecord(id=self._next_id, **payload.model_dump())
        self._next_id += 1
        self._rows.append(row)
        return deepcopy(row)

    def update(self, record_id: int, payload: PickupUpdate) -> PickupRecord | None:
        for idx, row in enumerate(self._rows):
            if row.id == record_id:
                updated = row.model_copy(update={k: v for k, v in payload.model_dump().items() if v is not None})
                self._rows[idx] = updated
                return deepcopy(updated)
        return None

    def delete(self, record_id: int) -> bool:
        before = len(self._rows)
        self._rows = [row for row in self._rows if row.id != record_id]
        return len(self._rows) != before
