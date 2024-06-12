from datetime import date

from sqlalchemy import func, select, and_

from app.backend.database import async_session_maker
from app.backend.hotels.rooms.models import Rooms

from app.backend.hotels.rooms.service import RoomsDAO
from app.backend.hotels.models import Hotels
from app.backend.core.base import BaseDAO


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        """Поиск отелей по заданным параметрам местоположения и времени"""

        hotels_with_available_rooms = await cls.get_hotels_with_available_rooms(
            location=location,
            date_from=date_from,
            date_to=date_to,
        )
        async with async_session_maker() as session:
            hotels = await session.execute(hotels_with_available_rooms)
            return hotels.mappings().all()

    @classmethod
    async def get_booked_hotels(
        cls,
        date_from: date,
        date_to: date,
    ):
        """
        Возвращает отели и количество забронированных в них комнатах

        WITH booked_hotels AS (
            SELECT rooms.hotel_id,
                SUM(rooms.quantity - COALESCE(booked_rooms.count_booked_rooms, 0))
                AS rooms_available
            FROM rooms
            LEFT JOIN booked_rooms
            ON rooms.id = booked_rooms.room_id
            GROUP BY rooms.hotel_id
        )
        """
        booked_rooms = await RoomsDAO.get_booked_rooms(
            date_from=date_from,
            date_to=date_to
        )

        return select(
            Rooms.hotel_id,
            func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0))\
                .label("rooms_left")
        ).select_from(
            Rooms
        ).join(
            booked_rooms,
            Rooms.id == booked_rooms.c.room_id,
            isouter=True,
        ).group_by(
            Rooms.hotel_id
        ).cte("booked_hotels")

    @classmethod
    async def get_hotels_with_available_rooms(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        """
        Получение отелей со свободными номерами

        SELECT hotels.*, booked_hotels.rooms_left
        FROM hotels
        LEFT JOIN booked_hotels
        ON hotels.id = booked_hotels.hotel_id,
        WHERE (booked_hotels.rooms_left > 0) AND
            (hotels.location LIKE '%LOCATION%')
        """
        booked_hotels = await cls.get_booked_hotels(
            date_from=date_from,
            date_to=date_to,
        )

        return select(
            Hotels.__table__.columns,
            booked_hotels.c.rooms_left,
        ).select_from(
            Hotels
        ).join(
            booked_hotels,
            booked_hotels.c.hotel_id == Hotels.id,
            isouter=True,
        ).where(
            and_(
                booked_hotels.c.rooms_left > 0,
                Hotels.location.like(f"%{location}%")
            )
        )