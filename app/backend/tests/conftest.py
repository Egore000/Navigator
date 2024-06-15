import asyncio
from datetime import datetime
import json

import pytest
from sqlalchemy import insert
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import config
from app.config import settings
from app.backend.database import Model, async_session_maker, engine

from app.backend.users.models import User
from app.backend.hotels.models import Hotels
from app.backend.hotels.rooms.models import Rooms
from app.backend.bookings.models import Bookings

from app.main import app as fastapi_app


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.project.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/backend/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    bookings = open_mock_json("bookings")
    users = open_mock_json("users")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(User).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac() -> AsyncClient:
    async with AsyncClient(
            app=fastapi_app,
            base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def authenticates_ac() -> AsyncClient:
    async with AsyncClient(
            app=fastapi_app,
            base_url="http://test",
    ) as ac:
        await ac.post("/auth/register", params={
            "email": "test@test.com",
            "password": "test",
        })
        assert ac.cookies.get(config.booking_access_token)
        yield ac
