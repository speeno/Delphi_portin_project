from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    api_title: str = 'Delphi Porting API'
    api_version: str = '0.1.0'
    cors_origins: list[str] = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]


settings = Settings()
