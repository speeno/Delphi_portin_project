from __future__ import annotations

from pydantic import BaseModel, Field


class PickupBase(BaseModel):
    gdate: str = Field(..., description='거래일자')
    hcode: str = Field(..., description='출판사코드')
    hname: str = Field(..., description='출판사명')
    gnumb: str = Field(default='', description='운송장번호')
    name1: str = Field(default='', description='지역명')
    gname: str = Field(default='', description='거래처명')
    name2: str = Field(default='', description='화물명')
    gbigo: str = Field(default='', description='메모')
    gqut1: float = Field(default=0, description='시내')
    gqut2: float = Field(default=0, description='지방')


class PickupRecord(PickupBase):
    id: int


class PickupCreate(PickupBase):
    pass


class PickupUpdate(BaseModel):
    gdate: str | None = None
    hcode: str | None = None
    hname: str | None = None
    gnumb: str | None = None
    name1: str | None = None
    gname: str | None = None
    name2: str | None = None
    gbigo: str | None = None
    gqut1: float | None = None
    gqut2: float | None = None


class PickupListResponse(BaseModel):
    items: list[PickupRecord]
    count: int
    sum_gqut1: float
    sum_gqut2: float
