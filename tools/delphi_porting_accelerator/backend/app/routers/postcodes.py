from __future__ import annotations

from fastapi import APIRouter, Query

from app.repositories.postcodes import PostcodeRepository
from app.schemas.postcodes import PostcodeSearchResponse
from app.services.postcodes import PostcodeService


router = APIRouter(prefix='/api/postcodes', tags=['postcodes'])
service = PostcodeService(PostcodeRepository())


@router.get('/search', response_model=PostcodeSearchResponse)
def search_postcodes(keyword: str = Query('', description='우편번호 또는 주소 검색어')) -> PostcodeSearchResponse:
    return service.search(keyword)
