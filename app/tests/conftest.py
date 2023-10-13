"""This module contains common Pytest Fixtures"""
import pytest_asyncio
from app.main import app_factory, app_startup, app_shutdown


@pytest_asyncio.fixture
async def app():
    """Helper method to create the FastAPI app object"""
    my_app = app_factory()
    await app_startup(my_app)
    yield my_app
    await app_shutdown(my_app)
