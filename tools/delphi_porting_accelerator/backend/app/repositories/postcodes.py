from __future__ import annotations

from app.schemas.postcodes import PostcodeSearchResult


class PostcodeRepository:
    def __init__(self) -> None:
        self._rows = [
            PostcodeSearchResult(post='04524', addr='서울특별시 중구 세종대로 110', dddd='-', dong='태평로1가', city='서울'),
            PostcodeSearchResult(post='06164', addr='서울특별시 강남구 영동대로 513', dddd='-', dong='삼성동', city='서울'),
            PostcodeSearchResult(post='48058', addr='부산광역시 해운대구 센텀동로 45', dddd='-', dong='우동', city='부산'),
            PostcodeSearchResult(post='63309', addr='제주특별자치도 제주시 첨단로 242', dddd='-', dong='영평동', city='제주'),
        ]

    def search(self, keyword: str) -> list[PostcodeSearchResult]:
        keyword = keyword.strip().lower()
        if not keyword:
            return self._rows
        return [
            row for row in self._rows
            if keyword in row.post.lower() or keyword in row.addr.lower() or keyword in (row.dong or '').lower() or keyword in (row.city or '').lower()
        ]
