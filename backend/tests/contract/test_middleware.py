"""
Contract tests for Middleware

Tests for:
- Authentication middleware
"""

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestAuthMiddleware:

    async def test_missing_cookie_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 when cookie is missing"""
        response = await async_client.get("/api/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_invalid_token_format_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 with invalid token format"""
        # Set invalid token in cookie
        async_client.cookies.set("accessToken", "invalid-token-format")

        response = await async_client.get("/api/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_expired_token_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 with expired token"""
        # This is an expired JWT token (exp in the past)
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.4Adcj0vt50jRJmH-xN3BkrJcNHmvpXX0V8Y8gNZ-Z_w"

        async_client.cookies.set("accessToken", expired_token)

        response = await async_client.get("/api/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
