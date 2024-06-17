from datetime import date

from app.backend.database import async_session_maker

from app.backend.core.base import BaseDAO
from app.backend.hotels.rooms.models import Rooms
from app.backend.hotels.rooms.queries import RoomsQueries


class RoomsDAO(BaseDAO):
    model = Rooms
    query = RoomsQueries

    @classmethod
    async def get_all(cls, hotel_id: int, **filter_by):
        """Получение всех комнат отеля из БД"""
        return await super().get_all(hotel_id=hotel_id, **filter_by)

    @classmethod
    async def get_room_price(cls, room_id: int) -> int:
        """Получение цены для конкретной комнаты"""
        query = await cls.query.get_price(room_id)

        price = await cls.execute(query)
        return price.scalar()

    @classmethod
    async def search_for_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        """Поиск свободных комнат для определенного отеля на нужный срок"""
        query = await cls.query.get_available_rooms_in_hotel(hotel_id, date_from, date_to)

        rooms = await cls.execute(query)
        return rooms.mappings().all()

    @classmethod
    async def get_rooms_left_count(
            cls,
            room_id: int,
            date_from: date,
            date_to: date,
    ) -> int:
        """Получение количества свободных комнат"""
        query = await cls.query.get_rooms_left_count(room_id, date_from, date_to)

        rooms_left = await cls.execute(query)
        return rooms_left.scalar()
