"""
델파이 도서 물류 시스템 - 웹 API 서버

계약(Migration Contract) 기반으로 구현된 RESTful API.
Routing Harness와 연동하여 점진적 전환을 지원한다.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.api import auth, inbound, outbound, inventory, health
from app.middleware.harness_middleware import HarnessMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="도서 물류 시스템 API",
    description="델파이 → 웹 포팅 API (8계층 하네스 엔지니어링 기반)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(HarnessMiddleware)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(inbound.router, prefix="/api/inbound", tags=["inbound"])
app.include_router(outbound.router, prefix="/api/outbound", tags=["outbound"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "서버 내부 오류가 발생했습니다.", "error": str(exc)},
    )
