"""
Rate Limiting Middleware

Prevents abuse by limiting the number of requests per client
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from src.logger import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware

    For production, consider using Redis-based rate limiting
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.cleanup_interval = timedelta(minutes=5)
        self.last_cleanup = datetime.now()

    def cleanup_old_requests(self):
        """Remove old request records to prevent memory leak"""
        now = datetime.now()
        if now - self.last_cleanup > self.cleanup_interval:
            cutoff_time = now - timedelta(minutes=1)
            for client_ip in list(self.requests.keys()):
                self.requests[client_ip] = [
                    req_time for req_time in self.requests[client_ip]
                    if req_time > cutoff_time
                ]
                # Remove empty entries
                if not self.requests[client_ip]:
                    del self.requests[client_ip]
            self.last_cleanup = now

    async def dispatch(self, request: Request, call_next: Callable):
        # Only rate limit admin endpoints
        if not request.url.path.startswith("/api/admin"):
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Cleanup old requests periodically
        self.cleanup_old_requests()

        # Get current time
        now = datetime.now()
        cutoff_time = now - timedelta(minutes=1)

        # Get requests from this client in the last minute
        recent_requests = [
            req_time for req_time in self.requests[client_ip]
            if req_time > cutoff_time
        ]

        # Check if rate limit exceeded
        if len(recent_requests) >= self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for {client_ip} on {request.url.path}",
                extra={
                    "client_ip": client_ip,
                    "path": request.url.path,
                    "requests_count": len(recent_requests),
                }
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after": 60
                }
            )

        # Add current request
        self.requests[client_ip].append(now)

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - len(recent_requests) - 1)
        )

        return response


def add_rate_limiting(app, requests_per_minute: int = 60):
    """
    Add rate limiting middleware to FastAPI app

    Args:
        app: FastAPI application
        requests_per_minute: Maximum requests per minute per IP (default: 60)

    Usage:
        from src.middleware.rate_limit import add_rate_limiting
        add_rate_limiting(app, requests_per_minute=30)
    """
    app.add_middleware(RateLimitMiddleware, requests_per_minute=requests_per_minute)
    logger.info(f"✓ Rate limiting enabled: {requests_per_minute} requests/minute for admin endpoints")
