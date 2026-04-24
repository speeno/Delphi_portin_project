"""
인증/인가 API (prototype)

Migration Contract: api.auth.login / api.auth.logout
레거시 시스템의 로그인 동작을 동일하게 재현한다.

필드 명명 (DEC-RBAC-01, login.yaml v1.1.0):
    - user_id   = Id_Logn.Gcode (Logn2 / 사번 / 로그인 ID)
    - user_name = Id_Logn.Hname (조직명 / 출판사명, 헤더 표시)
    - display_name = Id_Logn.Gname (표시명 / 작업자 이름, 본인 수정 가능)

호환:
    레거시 호출자가 ``username`` 키로 보낼 수 있도록 Pydantic alias 로 양립.
    ``warehouse_code`` 는 Id_Logn 사전에 없는 별도 출처
    (tenants_directory.primary_server) 의 키이므로 명시 docstring.
"""

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter()


class LoginRequest(BaseModel):
    """POST /api/v1/auth/login (prototype) 요청 본문."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(
        ...,
        alias="username",
        description="로그인 ID (Id_Logn.Gcode). 레거시 호환을 위해 'username' alias 도 수용.",
    )
    password: str = Field(..., description="비밀번호 평문")
    warehouse_code: str = Field(
        "",
        description=(
            "선택 — 테넌트/창고 식별 코드. 출처는 tenants_directory.primary_server. "
            "Id_Logn 사전에는 없는 별도 키."
        ),
    )


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str = ""
    user: dict = {}


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    if not req.user_id or not req.password:
        return LoginResponse(
            success=False,
            message="아이디와 비밀번호를 입력해 주세요.",
        )

    return LoginResponse(
        success=True,
        message="로그인 성공",
        token="TODO_JWT_TOKEN",
        user={
            # DEC-RBAC-01 — login.yaml outputs 매핑.
            "user_id": req.user_id,
            "user_name": "",
            "display_name": "",
            "warehouse_code": req.warehouse_code,
            "permissions": [],
        },
    )


@router.post("/logout")
async def logout():
    return {"success": True, "message": "로그아웃 되었습니다."}
