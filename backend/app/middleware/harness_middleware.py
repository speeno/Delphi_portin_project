"""
하네스 미들웨어

모든 API 요청/응답을 가로채서:
1. 요청 시간 측정 (Efficiency eval용)
2. 요청/응답 로그 기록 (State Tracking L6)
3. Comparison Harness 연동 (Shadow mode)
4. Routing 결정 로그 기록
"""

import time
import json
import logging
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("harness_middleware")


class HarnessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = f"req-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        request.state.request_id = request_id
        request.state.start_time = start_time

        response = await call_next(request)

        elapsed_ms = (time.time() - start_time) * 1000

        response.headers["X-Request-Id"] = request_id
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> {response.status_code} ({elapsed_ms:.1f}ms)"
        )

        return response
