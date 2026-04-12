"""
인증/인가 API

Migration Contract: api.auth.login / api.auth.logout
레거시 시스템의 로그인 동작을 동일하게 재현한다.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str
    warehouse_code: str = ""


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str = ""
    user: dict = {}


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    # TODO: 실제 인증 로직 구현 (Legacy DB 연동)
    # 가드레일: 기존 사용자 테이블 구조 유지
    if not req.username or not req.password:
        return LoginResponse(
            success=False,
            message="아이디와 비밀번호를 입력해 주세요.",
        )

    return LoginResponse(
        success=True,
        message="로그인 성공",
        token="TODO_JWT_TOKEN",
        user={
            "username": req.username,
            "warehouse_code": req.warehouse_code,
            "permissions": [],
        },
    )


@router.post("/logout")
async def logout():
    return {"success": True, "message": "로그아웃 되었습니다."}
