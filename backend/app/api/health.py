"""Health check 및 하네스 상태 API"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0",
        "harness": {
            "routing_mode": "legacy_only",
            "comparison_active": False,
        },
    }
