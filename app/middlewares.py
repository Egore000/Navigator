import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import jsonLogger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable):
        start = time.time()

        response: Response = await call_next(request)
        process_time = time.time() - start

        jsonLogger.info("Request execution time", extra={
            "process_time": round(process_time, 4),
            "method": request.method,
            "endpoint": request.url,
            "status": response.status_code
        })
        return response
