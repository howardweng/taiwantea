"""
Pytest configuration and shared fixtures
"""

import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from src.main import app


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing

    Usage:
        async def test_example(async_client):
            response = await async_client.get("/api/categories")
            assert response.status_code == 200
    """
    # Use ASGITransport to properly handle the ASGI app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
