from __future__ import annotations

from app.repositories.postcodes import PostcodeRepository
from app.schemas.postcodes import PostcodeSearchResponse


class PostcodeService:
    def __init__(self, repository: PostcodeRepository) -> None:
        self.repository = repository

    def search(self, keyword: str) -> PostcodeSearchResponse:
        items = self.repository.search(keyword)
        return PostcodeSearchResponse(items=items, count=len(items))
