from datetime import date
from sqlalchemy import and_, func, or_, select

from app.backend.database import async_session_maker

from app.backend.core.base import BaseDAO
from app.backend.bookings.models import Bookings
from app.backend.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_all(cls, hotel_id: int, **filter_by):
        """Получение всех комнат отеля из БД"""
        return await super().get_all(hotel_id=hotel_id, **filter_by)

    @classmethod
    async def get_room_price(cls, room_id: int):
        """Получение цены для конкретной комнаты"""
        return select(Rooms.price)\
            .filter_by(id=room_id)

    @classmethod
    async def search_for_rooms(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        """Поиск свободных комнат для определенного отеля на нужный срок"""
        available_rooms = await cls.get_available_rooms(date_from, date_to)

        available_rooms = available_rooms.where(
            Rooms.hotel_id == hotel_id
        )

        async with async_session_maker() as session:
            rooms = await session.execute(available_rooms)
            return rooms.mappings().all()

    @classmethod
    async def get_rooms_left_count(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> int:
        """Получение количества свободных комнат"""
        available_rooms = await cls.get_available_rooms(
            date_from=date_from,
            date_to=date_to
        )
        rooms_left_count = available_rooms.where(available_rooms.c.id == room_id)

        async with async_session_maker() as session:
            rooms_left = await session.execute(rooms_left_count)
            rooms_left = rooms_left.scalar()
            return rooms_left

    @classmethod
    async def get_booked_rooms(
        cls,
        date_from: date,
        date_to: date,
    ):
        """
        Получение забронированных комнат

        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS count_booked_rooms
            FROM bookings
            WHERE (date_from >= <date_from> AND date_from <= <date_to>) OR
                (date_from <= <date_from> AND date_to > <date_from>)
            GROUP BY room_id
        )
        """
        return select(
            Bookings.room_id,
            func.count(Bookings.room_id).label("count_booked_rooms")
        ).select_from(
            Bookings
        ).where(
            or_(
                and_(
                    Bookings.date_from >= date_from,
                    Bookings.date_from <= date_to
                ),
                and_(
                    Bookings.date_from <= date_from,
                    Bookings.date_to > date_from
                )
            )
        ).group_by(
            Bookings.room_id
        ).cte("booked_rooms")
        
    @classmethod
    async def get_available_rooms(
        cls,
        date_from: date,
        date_to: date
    ):
        """
        Получение комнат с количеством свободных номеров

        SELECT rooms.*,
            rooms.quantity - COALESCE(booked_rooms.count_booked_rooms, 0) AS rooms_left
        FROM rooms
        LEFT JOIN booked_rooms
        """
        booked_rooms = await cls.get_booked_rooms(
                date_from=date_from,
                date_to=date_to
            )
        return select(
            Rooms.__table__.columns,
            (Rooms.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0))\
                .label('rooms_left'),
            (Rooms.price * (date_to - date_from).days).label('total_cost')
        ).select_from(
            Rooms
        ).join(
            booked_rooms,
            booked_rooms.c.room_id == Rooms.id,
            isouter=True
        )
