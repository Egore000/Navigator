from datetime import date

from sqlalchemy import CTE, func, insert, select, and_, or_

from core.base import BaseService
from bookings.models import Bookings
from hotels.rooms.models import Rooms

from database import engine, async_session_maker



class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """Бронирование комнаты пользователем на некоторый период времени"""
        async with async_session_maker() as session:
            rooms_left_query = await cls._get_rooms_left( 
                room_id=room_id,
                date_from=date_from,
                date_to=date_to
            )
            rooms_left = await session.execute(rooms_left_query)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = await cls.get_room_price(room_id)
                price = await session.execute(get_price)
                price = price.scalar()

                new_booking_query = await cls._add_booking(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                )
                new_booking = await session.execute(new_booking_query)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
            
    @classmethod
    async def _get_booked_rooms(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> CTE:
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

    @classmethod
    async def get_room_price(
        cls,
        room_id: int
    ):
        return select(
                Rooms.price
            ).filter_by(
                id=room_id
            )
        
    @classmethod
    async def _add_booking(
        cls,
        room_id: int,
        user_id: int,
        date_from: date,
        date_to: date,
        price: int
    ):
        return insert(
                Bookings
            ).values(
                room_id=room_id, 
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(
                Bookings
            )