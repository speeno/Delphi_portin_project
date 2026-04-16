from __future__ import annotations

from pydantic import BaseModel, Field


class PostcodeSearchResult(BaseModel):
    post: str = Field(..., description='우편번호')
    addr: str = Field(..., description='주소')
    dddd: str | None = Field(default=None, description='추가 구분값')
    dong: str | None = Field(default=None, description='지역')
    city: str | None = Field(default=None, description='도시')


class PostcodeSearchResponse(BaseModel):
    items: list[PostcodeSearchResult]
    count: int
