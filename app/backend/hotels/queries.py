from datetime import date

from sqlalchemy import select, func

from app.backend.hotels.models import Hotels
from app.backend.hotels.rooms.models import Rooms
from app.backend.hotels.rooms.queries import RoomsQueries


class HotelsQueries:
    model = Hotels

    @classmethod
    async def get_booked_hotels(
            cls,
            date_from: date,
            date_to: date,
    ):
        """Запрос для получения отелей и количества забронированных в них комнатах"""

        """```
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

        booked_rooms = await RoomsQueries.get_booked_rooms(date_from=date_from, date_to=date_to)

        return (
            select(
                Rooms.hotel_id,
                func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0)
                ).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(
                booked_rooms,
                Rooms.id == booked_rooms.c.room_id,
                isouter=True,
            )
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

    @classmethod
    async def get_available_hotels(
            cls,
            date_from: date,
            date_to: date,
    ):
        """Запрос на получение всех доступных отелей"""

        """```
        SELECT hotels.*, booked_hotels.rooms_left
        FROM hotels
        LEFT JOIN booked_hotels
        ON hotels.id = booked_hotels.hotel_id,
        WHERE booked_hotels.rooms_left > 0
        """

        booked_hotels = await cls.get_booked_hotels(date_from, date_to)

        return (
            select(
                cls.model.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .select_from(cls.model)
            .join(
                booked_hotels,
                booked_hotels.c.hotel_id == cls.model.id,
                isouter=True,
            )
            .where(booked_hotels.c.rooms_left > 0)
        )

    @classmethod
    async def get_available_hotels_in_location(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ):
        """Запрос на получение всех доступных отелей в определённом месте"""

        """```
        SELECT hotels.*, booked_hotels.rooms_left
        FROM hotels
        LEFT JOIN booked_hotels
        ON hotels.id = booked_hotels.hotel_id,
        WHERE (booked_hotels.rooms_left > 0) AND
            (hotels.location LIKE '%LOCATION%')
        """
        available_hotels = await cls.get_available_hotels(date_from, date_to)
        hotels_in_location = available_hotels.where(cls.model.location.like(f"%{location}%"))

        return hotels_in_location
