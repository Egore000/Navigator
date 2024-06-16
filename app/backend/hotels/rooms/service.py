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
    async def get_room_price(cls, room_id: int) -> int:
        """Получение цены для конкретной комнаты"""
        async with async_session_maker() as session:
            get_price = select(Rooms.price)\
                .filter_by(id=room_id)
            price = await session.execute(get_price)
            return price.scalar()

    @classmethod
    async def search_for_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        """Поиск свободных комнат для определенного отеля на нужный срок"""
        """```
        WITH available_rooms AS (
            WITH booked_rooms AS (
                SELECT room_id, COUNT(room_id) AS count_booked_rooms 
                FROM bookings
                WHERE(date_from >= <date_from> AND date_from <= <date_to>) OR
                    (date_from <= <date_from> AND date_to > <date_from>)
                GROUP BY room_id
            )
            SELECT rooms.*, 
                rooms.quantity - COALESCE(booked_rooms.count_booked_rooms, 0) AS rooms_left,
                rooms.price * (DATE('2023-06-20') - DATE('2023-05-15')) AS total_cost
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        )
        SELECT *
        FROM available_rooms
        WHERE hotel_id = <hotel_id>
        """

        available_rooms = await cls.get_available_rooms(date_from, date_to)

        available_rooms_in_hotel = available_rooms.where(
            Rooms.hotel_id == hotel_id
        )

        async with async_session_maker() as session:
            rooms = await session.execute(available_rooms_in_hotel)
            return rooms.mappings().all()

    @classmethod
    async def get_rooms_left_count(
            cls,
            room_id: int,
            date_from: date,
            date_to: date,
    ) -> int:
        """Получение количества свободных комнат"""
        booked_rooms = await cls.get_booked_rooms(date_from, date_to)

        rooms_left_count = select(
            cls.model.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0)
        ).select_from(
            cls.model,
        ).join(
            booked_rooms,
            cls.model.id == booked_rooms.c.room_id,
            isouter=True,
        ).where(
            cls.model.id == room_id
        )
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
        """
        """```
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
        """
        """```
        SELECT rooms.*,
            rooms.quantity - COALESCE(booked_rooms.count_booked_rooms, 0) AS rooms_left,
            rooms.price * (DATE('2023-06-20') - DATE('2023-05-15')) AS total_cost
        FROM rooms
        LEFT JOIN booked_rooms
        ON rooms.id = booked_rooms.room_id
        """
        booked_rooms = await cls.get_booked_rooms(
                date_from=date_from,
                date_to=date_to
            )
        return select(
            cls.model.__table__.columns,
            (cls.model.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0))\
                .label('rooms_left'),
            (cls.model.price * (date_to - date_from).days).label('total_cost'),
        ).select_from(
            cls.model
        ).join(
            booked_rooms,
            booked_rooms.c.room_id == cls.model.id,
            isouter=True
        ).cte("available_rooms")
