from datetime import date

from sqlalchemy import func, select, and_

from app.backend.database import async_session_maker
from app.backend.hotels.queries import HotelsQueries
from app.backend.hotels.rooms.models import Rooms

from app.backend.hotels.rooms.service import RoomsDAO
from app.backend.hotels.models import Hotels
from app.backend.core.base import BaseDAO


class HotelDAO(BaseDAO):
    model = Hotels
    query = HotelsQueries

    @classmethod
    async def search_for_hotels(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ) -> list[Hotels]:
        """Поиск отелей по заданным параметрам местоположения и времени"""

        query = await cls.query.get_available_hotels_in_location(location, date_from, date_to)

        hotels = await cls.execute(query)
        return hotels.mappings().all()

    @classmethod
    async def booked_hotels(
            cls,
            date_from: date,
            date_to: date,
    ) -> list[Hotels]:
        """Получение списка забронированных отелей"""
        query = await cls.query.get_booked_hotels(date_from, date_to)

        hotels = await cls.execute(query)
        return hotels.mappings().all()

