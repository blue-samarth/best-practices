# test/conftest.py:
# Here is the conftest.py file that sets up the test environment for the test_valid_token test:
import asyncio
from contextlib import asynccontextmanager

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.server import app as main_app
from src.db import close_connection, generate_schema, init_db

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create a new event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_app():
    """Create a test instance of the app with the test database."""
    test_app = FastAPI(
        title = main_app.title,
        description = main_app.description,
        version = main_app.version,
    )

    for middleware in main_app.user_middleware:
        test_app.add_middleware(middleware.cls, **middleware.options)
    
    for route in main_app.router.routes:
        test_app.include_router(route)
    
    @asynccontextmanager
    async def test_lifespan(app: FastAPI):
        await init_db(TEST_DB_URL)
        await generate_schema()
        yield
        await close_connection()
    
    test_app.router.lifespan_context = test_lifespan
    yield test_app


@pytest.fixture(scope="function")
async def client(test_app):
    """Provide an async test client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def reset_db():
    """Reset the database schema before each test function."""
    await generate_schema()
    yield
