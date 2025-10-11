"""
Request/Response Logging Middleware

Logs all incoming requests and outgoing responses with timing information
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests and responses

    Logs:
    - HTTP method and path
    - Status code
    - Response time
    - Client IP
    - User agent (optional)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timer
        start_time = time.time()

        # Get client info
        client_host = request.client.host if request.client else "unknown"

        # Log incoming request
        logger.info(
            f"→ {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": client_host,
                "query_params": str(request.query_params),
            }
        )

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"✗ {request.method} {request.url.path} - ERROR - {process_time:.2f}ms",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "process_time_ms": f"{process_time:.2f}",
                },
                exc_info=True
            )
            raise

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000

        # Add custom header with processing time
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        # Log response
        status_emoji = "✓" if response.status_code < 400 else "✗"
        logger.info(
            f"{status_emoji} {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_ms": f"{process_time:.2f}",
                "client_ip": client_host,
            }
        )

        return response


def add_logging_middleware(app):
    """
    Add logging middleware to FastAPI app

    Usage:
        from src.middleware.logging import add_logging_middleware
        add_logging_middleware(app)
    """
    app.add_middleware(LoggingMiddleware)
    logger.info("✓ Request logging middleware enabled")
