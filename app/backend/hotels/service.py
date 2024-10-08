from datetime import date

from app.backend.core.base import BaseDAO
from app.backend.hotels.models import Hotels
from app.backend.hotels.queries import HotelsQueries


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
