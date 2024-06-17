from datetime import date

from sqlalchemy import select, func, and_, or_

from app.backend.bookings.models import Bookings
from app.backend.hotels.rooms.models import Rooms


class RoomsQueries:
    """Запросы для комнат"""
    model = Rooms

    @classmethod
    async def get_price(cls, room_id: int):
        """Запрос на получение цены"""

        """```
        SELECT price
        FROM rooms
        WHERE id == room_id
        """

        return (
            select(cls.model.price)
            .filter_by(id=room_id)
        )

    @classmethod
    async def get_booked_rooms(
            cls,
            date_from: date,
            date_to: date,
    ):
        """
        Запрос на получение забронированных комнат
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

        return (
            select(
                Bookings.room_id,
                func.count(Bookings.room_id).label("count_booked_rooms"))
            .select_from(Bookings)
            .where(
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
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

    @classmethod
    async def get_available_rooms(
            cls,
            date_from: date,
            date_to: date
    ):
        """
        Запрос на получение комнат с количеством свободных номеров
        """

        """```
        SELECT rooms.*,
            rooms.quantity - COALESCE(booked_rooms.count_booked_rooms, 0) AS rooms_left,
            rooms.price * (DATE('2023-06-20') - DATE('2023-05-15')) AS total_cost
        FROM rooms
        LEFT JOIN booked_rooms
        ON rooms.id = booked_rooms.room_id
        """

        booked_rooms = await cls.get_booked_rooms(date_from, date_to)
        return (
            select(
                cls.model.__table__.columns,
                (cls.model.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0))
                .label('rooms_left'),
                (cls.model.price * (date_to - date_from).days)
                .label('total_cost'))
            .select_from(cls.model)
            .join(
                booked_rooms,
                booked_rooms.c.room_id == cls.model.id,
                isouter=True)
        )

    @classmethod
    async def get_rooms_left_count(
            cls,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """Запрос на получение количества свободных комнат"""

        """```
            SELECT quantity - COALESCE(booked_rooms.count_booked_rooms, 0)
            FROM rooms
            LEFT JOIN booked_rooms
            ON id = booked_rooms.room_id
            WHERE id = room_id
        """

        booked_rooms = await cls.get_booked_rooms(date_from, date_to)

        return (
            select(cls.model.quantity - func.coalesce(booked_rooms.c.count_booked_rooms, 0))
            .select_from(cls.model)
            .join(
                booked_rooms,
                cls.model.id == booked_rooms.c.room_id,
                isouter=True,
            )
            .where(cls.model.id == room_id)
        )

    @classmethod
    async def get_available_rooms_in_hotel(
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
        available_rooms_in_hotel = available_rooms.where(cls.model.hotel_id == hotel_id)

        return available_rooms_in_hotel
