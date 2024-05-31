from datetime import date
from sqlalchemy import and_, func, or_, select

from app.database import async_session_maker

from app.core.base import BaseService
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def get_all(cls, hotel_id: int, **filter_by):
        return await super().get_all(hotel_id=hotel_id, **filter_by)

    @classmethod
    async def get_room_price(cls, room_id: int):
        return select(
                Rooms.price
            ).filter_by(
                id=room_id
            )
    
    @classmethod
    async def get_rooms_left(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            rooms_left_query = await cls._get_rooms_left( 
                room_id=room_id,
                date_from=date_from,
                date_to=date_to
            )
            rooms_left = await session.execute(rooms_left_query)
            rooms_left = rooms_left.scalar()
            return rooms_left

    @classmethod
    async def _get_booked_rooms(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = <room_id> AND
            (date_from >= <date_from> AND date_from <= <date_to>) OR
            (date_from <= <date_from> AND date_to > <date_from>)
        )
        """
        return select(
            Bookings
        ).where(
            and_(
                Bookings.room_id == room_id,
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
        ).cte("booked_rooms")
        
    @classmethod
    async def _get_rooms_left(
        cls,
        room_id: int,
        date_from: date,
        date_to: date
    ) -> int:
        """
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms 
        ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        booked_rooms = await cls._get_booked_rooms(
                room_id=room_id, 
                date_from=date_from, 
                date_to=date_to
            )
        return select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(
                Rooms
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(
                Rooms.id == room_id
            ).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
