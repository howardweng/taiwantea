"""
Pytest configuration and shared fixtures
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
import asyncio

from src.main import app
from src.database import connect_to_mongo, close_mongo_connection, database


# Configure pytest-asyncio to use function scope
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database(event_loop):
    """
    Setup database connection for entire test session
    Connects once at start, closes at end
    """
    print("\n✓ Connecting to test database...")
    await connect_to_mongo()
    print("✓ Database connection initialized")
    yield

    print("\n✓ Closing test database connection...")
    await close_mongo_connection()


@pytest_asyncio.fixture
async def async_client(setup_test_database) -> AsyncGenerator[AsyncClient, None]:
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
